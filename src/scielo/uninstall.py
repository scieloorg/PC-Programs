import os
import shutil


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def delete_file_or_folder(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_file_or_folder(path + '/' + item)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.unlink(path)

del_list = ['bin', 'export', 'help', 'xml_scielo', 'backup']

for item in os.listdir(CURRENT_PATH):
    if item.lower() in del_list:
        if os.path.isdir(CURRENT_PATH + '/' + item):
            delete_file_or_folder(CURRENT_PATH + '/' + item)
