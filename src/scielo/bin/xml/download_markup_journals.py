# coding=cp1252
import sys
import os
import urllib2
import csv
import codecs
import shutil


def journals_by_collection(filename):
    collections = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            if len(item) >= 10:
                if item[1] != 'ISSN':
                    j = {}
                    j['collection'] = item[0]
                    j['collection-name'] = item[4]
                    j['issn-id'] = item[1]
                    j['pissn'] = item[2]
                    j['eissn'] = item[3]
                    j['acron'] = item[5]
                    j['short-title'] = item[6]
                    j['journal-title'] = item[7]
                    j['nlm-title'] = item[8]
                    j['publisher-name'] = item[9]
                    _col = j.get('collection-name')
                    if _col == '':
                        _col = j.get('collection')
                    if not _col in collections.keys():
                        collections[_col] = []
                    collections[_col].append(j)
            else:
                print('ignored:')
                print(item)
        if 'Symbol' in collections.keys():
            del collections['Symbol']
        if 'Collection Name' in collections.keys():
            del collections['Collection Name']

    return collections


def get_journals_list(collections, collection_name=None):
    journals = {}
    if collection_name is not None:
        journals = get_collection_journals_list(collections, collection_name)
        if len(journals) == 0:
            _k = collections.keys()[0]
            journals = get_collection_journals_list(collections, _k)
    if len(journals) == 0:
        journals = get_all_journals_list(collections)
    c = []
    for k in sorted(journals.keys()):
        c.append(journals[k])
    return c


def get_collection_journals_list(collections, collection_name):
    journals = {}
    for item in collections.get(collection_name, []):
        column = []
        column.append(item['journal-title'])
        column.append(item['nlm-title'])
        column.append(item['short-title'])
        column.append(item['acron'])
        column.append(item['issn-id'])
        column.append(item['pissn'])
        column.append(item['eissn'])
        column.append(item['publisher-name'])
        journals[item['journal-title'].lower()] = '|'.join(column)
    return journals


def get_all_journals_list(collections):
    journals = {}
    for collection_key, collection_journals in collections.items():
        for item in collection_journals:
            column = []
            column.append(item['journal-title'])
            column.append(item['nlm-title'])
            column.append(item['short-title'])
            column.append(item['acron'])
            column.append(item['issn-id'])
            column.append(item['pissn'])
            column.append(item['eissn'])
            column.append(item['publisher-name'])
            journals[item['journal-title'].lower()] = '|'.join(column)
    return journals


def generate_input_for_markup(journals, filename):
    c = '\n'.join(journals)
    codecs.open(filename, mode='w+').write(c)


def download_content(url):
    try:
        new = urllib2.urlopen(url).read()

    except:
        new = ''
    return new


def main(url, downloaded_filename, dest_filename, collection_name=None):
    new = download_content(url)
    codecs.open(downloaded_filename, mode='w+').write(new)
    print(downloaded_filename)
    journals_collections = journals_by_collection(downloaded_filename)
    codecs.open(dest_filename.replace('.csv', '_collections.csv'), mode='w+').write('\n'.join(sorted(journals_collections.keys())))
    journals = get_journals_list(journals_collections, collection_name)
    generate_input_for_markup(journals, dest_filename)


collection_name = None
ctrl_file = None

if len(sys.argv) > 1:
    collection_name_or_ctrl_file = sys.argv[1]
    if not '/' in collection_name_or_ctrl_file:
        collection_name = collection_name_or_ctrl_file
    elif os.path.isdir(os.path.dirname(collection_name_or_ctrl_file)):
        ctrl_file = collection_name_or_ctrl_file
if len(sys.argv) > 2:
    ctrl_file = sys.argv[2]
    if os.path.isfile(ctrl_file):
        os.unlink(ctrl_file)

print('ctrl_file')
print(ctrl_file)


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
downloaded_filename = CURRENT_PATH + '/markup/downloaded_markup_journals.csv'
markup_journals_filename = CURRENT_PATH + '/../markup/markup_journals.csv'
temp_markup_journals_filename = CURRENT_PATH + '/markup/_markup_journals.csv'

temp_path = os.path.dirname(temp_markup_journals_filename)
if not os.path.isdir(temp_path):
    os.makedirs(temp_path)

temp_path = os.path.dirname(downloaded_filename)
if not os.path.isdir(temp_path):
    os.makedirs(temp_path)

temp_path = os.path.dirname(markup_journals_filename)
if not os.path.isdir(temp_path):
    os.makedirs(temp_path)

if os.path.isfile(temp_markup_journals_filename):
    try:
        os.unlink(temp_markup_journals_filename)
    except:
        pass

main('http://static.scielo.org/sps/markup_journals.csv', downloaded_filename, temp_markup_journals_filename, collection_name)

while not os.path.isfile(temp_markup_journals_filename):
    pass

if os.path.isfile(temp_markup_journals_filename):
    shutil.copyfile(temp_markup_journals_filename, markup_journals_filename)

if ctrl_file is not None:
    open(ctrl_file, 'w').write('end')
    print('end')
