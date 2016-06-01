# coding=utf-8

import os
import shutil
import time
from datetime import datetime
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
        self.ftp_folder = config.get('FTP', 'folder')
        self.download_path = config.get('RECEPTION', 'download_path')
        self.serial_path = config.get('ORGANIZER', 'serial_path')
        self.unidentified_path = config.get('ORGANIZER', 'unidentified_path')
        self.control_path = config.get('ORGANIZER', 'control_path')
        self.status_file = config.get('RECEPTION', 'status')
        self.frequency = int(config.get('RECEPTION', 'frequency'))
        self.weekdays = config.get('RECEPTION', 'weekdays').split(',')
        self.hours_range = config.get('RECEPTION', 'hours_range').split('-')
        self.start_hour = int(self.hours_range[0])
        self.end_hour = int(self.hours_range[1])

    def status(self):
        s = open(self.status_file).read().strip()
        return s if s in ['ON', 'OFF'] else 'ON'

    @property
    def is_valid(self):
        return all([self.ftp_server, os.path.isfile(self.status_file), os.path.isfile(self.accounts_filename), self.ftp_folder, self.download_path, self.serial_path, self.unidentified_path, self.control_path])


class Accounts(object):

    def __init__(self, config_filename):
        self.items = {}
        for line in open(config_filename, 'r').readlines():
            k, v = line.strip().split('\t')
            self.items[k] = v


class Reception(object):

    def __init__(self, control_path, download_path):
        self.date_and_time = utils.now()
        self._filename = control_path + '/' + self.day_month_folders + '/' + self.fname + '.csv'
        self._download_path = download_path

    def register(self, downloaded, destination):
        fs_utils.append_file(self.filename, '\t'.join([utils.now()[0], utils.now()[1], downloaded, destination]))

    @property
    def filename(self):
        if not os.path.isfile(self._filename):
            p = os.path.dirname(self._filename)
            if not os.path.isdir(p):
                os.makedirs(p)
        return self._filename

    @property
    def dateiso(self):
        return self.date_and_time[0]

    @property
    def hour(self):
        return self.date_and_time[1][:2]

    @property
    def dateiso_hour(self):
        return self.dateiso + '-' + self.hour

    @property
    def dateiso_time(self):
        return self.dateiso + '-' + self.date_and_time[1]

    @property
    def fname(self):
        return self.dateiso + '-' + self.hour

    @property
    def day_month_folders(self):
        return self.dateiso[6:] + '/' + self.dateiso[4:6]

    @property
    def download_path(self):
        return self._download_path + '/' + self.hour


class Organizer(object):

    def __init__(self, destination_path, unidentified_path):
        self.destination_path = destination_path
        self.unidentified_path = unidentified_path

    def organize(self, reception):
        for f in os.listdir(reception.download_path):
            downloaded_item = DownloadedItem(f)
            folders = self.get_folders(downloaded_item, reception)
            for item in folders:
                if not os.path.isdir(item):
                    os.makedirs(item)
            if fs_utils.unzip(reception.download_path + '/' + f, folders[1]):
                shutil.copy(reception.download_path + '/' + f, folders[0])
                if os.path.isfile(reception.download_path + '/' + f):
                    reception.register(f, folders[1])
                    os.unlink(reception.download_path + '/' + f)
        try:
            fs_utils.delete_file_or_folder(reception.download_path)
        except:
            pass

    def get_folders(self, downloaded_item, reception):
        if downloaded_item.is_identified:
            fullpath = '/'.join([self.destination_path, downloaded_item.folder, reception.dateiso_time])
        else:
            fullpath = '/'.join([self.unidentified_path, reception.dateiso_hour, downloaded_item.alternative_issueid])

        return [fullpath + '/zip', fullpath + '/unzip']


def receive_and_organize(config, organizer):
    accounts = Accounts(config.accounts_filename)
    if len(accounts.items) > 0:
        reception = Reception(config.control_path, config.download_path)
        for items in accounts.items.items():
            account = None
            key = None
            folder = 'entrega'
            if len(items) == 2:
                account, key = items
            elif len(items) == 3:
                account, key, folder = items
            if account is not None:
                ftp_service.download_files(config.ftp_server, account, key, folder, reception.download_path)
    organizer.organize(reception)


def execute_download_and_extraction(config_filename):
    config = ReceptionConfiguration(config_filename)
    if config.is_valid:
        print('running')
        organizer = Organizer(config.serial_path, config.unidentified_path)

        while config.status() == 'ON':
            sleep = 0
            if str(datetime.today().weekday()) in config.weekdays:
                h = int(utils.now()[1][0:2])
                if config.start_hour <= h <= config.end_hour:
                    receive_and_organize(config, organizer)
                    sleep = 60*config.frequency
                elif h < config.start_hour:
                    sleep = 60*60*(config.start_hour - h)
                elif h > config.end_hour:
                    sleep = 60*60*(24 - h + config.start_hour)
            else:
                # volta em 24h
                sleep = 60*60*24
            if sleep > 0:
                print(sleep)
            time.sleep(sleep)
        print('stopped')
    else:
        print('configuration problem')
