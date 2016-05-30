# coding=utf-8

import os
import shutil
import ConfigParser

import ftp_service
import fs_utils
import utils


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


class DownloadedItem(object):

    def __init__(self, zip_filename):
        zip_filename = zip_filename[:zip_filename.rfind('.zip')]
        parts = zip_filename.split('-')
        self.issn = None
        self.acron = None
        self.volume = None
        self.issue = None
        self.suppl = None
        self.alternative_issueid = zip_filename

        volume = None
        issue = None
        suppl = None

        if len(parts) > 3:
            self.issn = parts[0] + '-' + parts[1]
            self.acron = parts[2]

            if len(parts) == 5:
                issn1, issn2, acron, volume, issue = parts
                if issue[0] == 's' and not 'spe' in issue:
                    suppl = issue
                    issue = None
            elif len(parts) == 6:
                issn1, issn2, acron, volume, issue, suppl = parts
            elif len(parts) == 4:
                issn1, issn2, acron, volume = parts

            if volume is not None:
                if volume.isdigit():
                    volume = str(int(volume))
                if len(volume) > 3:
                    volume = None
            if issue is not None:
                if issue.isdigit():
                    issue = str(int(issue))
                if len(issue) > 3:
                    issue = None
            if suppl is not None:
                if len(suppl) > 2:
                    suppl = None
        self.volume = volume
        self.issue = issue
        self.suppl = suppl

    @property
    def is_identified(self):
        return self.issue is not None or self.suppl is not None

    @property
    def issue_id(self):
        if self.is_identified:
            prefixes = ['v', 'n', '']
            values = [self.volume, self.issue, self.suppl]
            name = []
            for prefix, value in zip(prefixes, values):
                if value is not None:
                    name.append(prefix + value)
            return ''.join(name)

    @property
    def folder(self):
        r = ''
        if self.acron is not None:
            r += self.acron + '/'
        r += self.issue_id if self.issue_id is not None else self.alternative_issueid
        return r


class ReceptionConfiguration(object):

    def __init__(self, config_filename):
        self.config_filename = config_filename

        config = ConfigParser.ConfigParser()
        config.read(config_filename)

        self.ftp_server = config.get('FTP', 'server')
        self.accounts_filename = config.get('FTP', 'users')
        self.ftp_folder = 'entrega'
        self.download_path = config.get('RECEPTION', 'download_path')
        self.serial_path = config.get('ORGANIZER', 'serial_path')
        self.unidentified_path = config.get('ORGANIZER', 'unidentified_path')
        self.control_path = config.get('ORGANIZER', 'control_path')

    @property
    def status(self):
        config = ConfigParser.ConfigParser()
        config.read(self.config_filename)
        s = config.get('RECEPTION', 'status')
        return s if s in ['ON', 'OFF'] else 'ON'

    @property
    def is_valid(self):
        return all([self.ftp_server, os.path.isfile(self.accounts_filename), self.ftp_folder, self.download_path, self.serial_path, self.unidentified_path, self.control_path])


class Accounts(object):

    def __init__(self, config_filename):
        self.items = {}
        for line in open(config_filename, 'r').readlines():
            k, v = line.strip().split('\t')
            self.items[k] = v


class Reception(object):

    def __init__(self, control_path, download_path):
        self.date_and_time = utils.now()
        self.control_path = control_path + '/' + self.year_month_day_folders
        if not os.path.isdir(self.control_path):
            os.makedirs(self.control_path)
        self.filename = self.control_path + '/' + self.hour + '.log'
        self._download_path = download_path

    def register(self, downloaded, destination):
        fs_utils.append_file(self.filename, ' '.join(utils.now()) + ' | ' + downloaded + ' | ' + destination)

    @property
    def hour(self):
        return self.date_and_time[1][:2]

    @property
    def year_month_day_folders(self):
        return self.date_and_time[0][:4] + '/' + self.date_and_time[0][4:6] + '/' + self.date_and_time[0][6:]

    @property
    def download_path(self):
        return self._download_path + '/' + '_'.join(self.date_and_time)


class Organizer(object):

    def __init__(self, destination_path, unidentified_path):
        self.destination_path = destination_path
        self.unidentified_path = unidentified_path

    def organize(self, reception):
        for f in os.listdir(reception.download_path):
            downloaded_item = DownloadedItem(f)

            dest_path = self.destination_path if downloaded_item.is_identified else self.unidentified_path
            issue_path = dest_path + '/' + downloaded_item.folder

            date_path = issue_path + '/' + '-'.join(reception.date_and_time)

            download_path = date_path + '/zip'
            extracted_path = date_path + '/unzip'

            if not os.path.isdir(extracted_path):
                os.makedirs(extracted_path)

            if fs_utils.unzip(self.reception_path + '/' + f, extracted_path):
                if not os.path.isdir(download_path):
                    os.makedirs(download_path)
                shutil.copy(self.reception_path + '/' + f, download_path)
                if os.path.isfile(download_path + '/' + f):
                    reception.register(f, extracted_path)
                    os.unlink(self.reception_path + '/' + f)
        fs_utils.delete_file_or_folder(reception.download_path)


def execute_download_and_extraction(config_filename):
    config = ReceptionConfiguration(config_filename)
    if config.is_valid:
        print('running')
        organizer = Organizer(config.serial_path, config.unidentified_path)
        while config.status == 'ON':
            accounts = Accounts(config.accounts_filename)

            if len(accounts.items) > 0:
                reception = Reception(config.control_path, config.download_path)
                if not os.path.isdir(reception.download_path):
                    os.makedirs(reception.download_path)
                for account, key in accounts.items.items():
                    ftp_service.download_files(config.ftp_server, account, key, config.ftp_folder, reception.download_path)
                organizer.organize(reception)
        print('stopped')
    else:
        print('configuration problem')
