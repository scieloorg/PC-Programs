# coding=utf-8
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
import csv

from . import files_extractor
from . import encoding


def read_file(filename, encode='utf-8'):
    if os.path.isfile(filename):
        r = open(filename, 'r').read()
        return encoding.decode(r, encode)


def read_file_lines(filename, encode='utf-8'):
    if os.path.isfile(filename):
        content = read_file(filename, encode)
        return content.replace('\r', '').split('\n')


def write_file(filename, content, encode='utf-8'):
    open(filename, 'w').write(encoding.encode(content, encode))


def append_file(filename, content, encode='utf-8'):
    open(filename, 'a+').write(encoding.encode(content, encode) + '\n')


def read_csv_file(filename, encode='utf-8'):
    lines = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            lines.append([encoding.decode(elem, encode).strip() for elem in item])
    return lines


def delete_file_or_folder(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_file_or_folder(path + '/' + item)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        try:
            os.unlink(path)
        except:
            encoding.display_message('Unable to delete: ')
            encoding.display_message(path)


def move_file(src, dest):
    errors = []
    if os.path.isfile(src):
        src_folder = os.path.dirname(dest)
        if not os.path.isdir(src_folder):
            os.makedirs(src_folder)
        if os.path.isfile(dest):
            try:
                os.unlink(dest)
            except:
                errors.append(dest + ' is already exists.')
        try:
            shutil.move(src, src_folder)
        except:
            errors.append('Unable to move ' + src + ' to ' + src_folder + '.')
    else:
        errors.append('Source ' + src + ' does not exist.')
    return errors


def extract_package(pkg_file, pkg_work_path):
    """
    Extract files to pkg_work_path from compressed files that are in compressed_path
    """
    r = False

    if os.path.isfile(pkg_file):
        if files_extractor.is_compressed_file(pkg_file):
            if os.path.exists(pkg_work_path):
                delete_file_or_folder(pkg_work_path)

            os.makedirs(pkg_work_path)
            # delete content of destination path
            # create tempdir
            temp_dir = tempfile.mkdtemp().replace('\\', '/')

            # extract in tempdir
            if files_extractor.extract_file(pkg_file, temp_dir):
                # eliminate folders
                for item in os.listdir(temp_dir):
                    _file = temp_dir + '/' + item
                    if os.path.isfile(_file):
                        shutil.copyfile(_file, pkg_work_path + '/' + item)
                        delete_file_or_folder(_file)
                    elif os.path.isdir(_file):
                        for f in os.listdir(_file):
                            if os.path.isfile(_file + '/' + f):
                                shutil.copyfile(_file + '/' + f, pkg_work_path + '/' + f)
                                delete_file_or_folder(_file + '/' + f)
                        shutil.rmtree(_file)
                shutil.rmtree(temp_dir)
                r = True
    return r


def unzip(compressed_filename, destination_path):
    """
    Extract files to destination_path from compressed files that are in compressed_path
    """
    r = False

    if os.path.isfile(compressed_filename):
        if files_extractor.is_compressed_file(compressed_filename):
            if not os.path.isdir(destination_path):
                os.makedirs(destination_path)
            # delete content of destination path
            # create tempdir
            # extract in tempdir
            r = files_extractor.extract_file(compressed_filename, destination_path)
    return r


def zip(zip_filename, files):
    dest_path = os.path.dirname(zip_filename)
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    try:
        zipf = zipfile.ZipFile(zip_filename, 'w')
        for item in list(set(files)):
            zipf.write(item, arcname=os.path.basename(item))
        zipf.close()
    except:
        pass


def fix_path(path):
    path = path.replace('\\', '/')
    if path.endswith('/'):
        path = path[0:-1]
    return path


def zip_report(report_filename):
    zip_path = report_filename.replace('.html', '.zip')
    myZipFile = zipfile.ZipFile(zip_path, "w")
    myZipFile.write(report_filename, os.path.basename(report_filename), zipfile.ZIP_DEFLATED)
    return zip_path


def update_file_content_if_there_is_new_items(new_content, filename):
    current_content = ''
    if not os.path.isfile(filename):
        write_file(filename, '')

    if os.path.isfile(filename):
        current_content = read_file(filename)
    current_items = current_content.split('\n')

    if new_content is None:
        new_content = ''
    new_items = new_content.split('\n')

    allow_update = (len(new_items) != len(current_items)) or (len(new_items) == len(current_items) and new_content != current_content)

    if allow_update is True:
        write_file(filename, new_content)


def last_modified_datetime(filename):
    return datetime.fromtimestamp(os.path.getmtime(filename))


class ProcessLogger(object):

    def __init__(self):
        self.logged_items = []

    def register(self, text):
        self.logged_items.append(datetime.now().isoformat() + ' ' + text)

    def write(self, filename):
        write_file(filename, '\n'.join(self.logged_items))

    def display(self):
        encoding.display_message('\n'.join(self.logged_items))


def is_compressed_file(path):
    r = False
    if path.endswith('.zip'):
        r = True
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        r = True
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        r = True
    return r
