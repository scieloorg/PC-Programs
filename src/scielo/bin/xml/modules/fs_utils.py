# coding=utf-8
import os
import shutil
import tempfile

import files_extractor


def read_file(filename, encode='utf-8'):
    content = open(filename, 'r').read()
    if not isinstance(content, unicode):
        content = content.decode(encode)
    return content


def write_file(filename, content, encode='utf-8'):
    if isinstance(content, unicode):
        content = content.encode(encode)
    open(filename, 'w').write(content)


def append_file(filename, content, encode='utf-8'):
    if isinstance(content, unicode):
        content = content.encode(encode)
    open(filename, 'a+').write(content + '\n')


def delete_file_or_folder(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_file_or_folder(path + '/' + item)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.unlink(path)


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


def fix_path(path):
    path = path.replace('\\', '/')
    if path.endswith('/'):
        path = path[0:-1]
    return path


def zip_report(report_filename):
    import zipfile
    zip_path = report_filename.replace('.html', '.zip')
    myZipFile = zipfile.ZipFile(zip_path, "w")
    myZipFile.write(report_filename, os.path.basename(report_filename), zipfile.ZIP_DEFLATED)
    return zip_path


def get_downloaded_data(url, downloaded_filename):
    import urllib2

    current_content = u''
    if os.path.isfile(downloaded_filename):
        current_content = open(downloaded_filename, 'r').read()
    if not isinstance(current_content, unicode):
        current_content = current_content.decode('utf-8')
    current_items = current_content.split('\n')
    try:
        new = urllib2.urlopen(url).read()
    except:
        new = u''
    if not isinstance(new, unicode):
        new = new.decode('utf-8')
    new_items = new.split('\n')

    content = current_content
    if len(new_items) > len(current_items):
        write_file(downloaded_filename, new)
        content = new

    return content


def last_modified_datetime(filename):
    from datetime import datetime
    return datetime.fromtimestamp(os.path.getmtime(filename))
