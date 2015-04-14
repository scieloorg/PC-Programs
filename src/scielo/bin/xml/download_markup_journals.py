# code utf-8
import sys
import os
import csv
import urllib2
import codecs


#http://static.scielo.org/sps/titles-tab-utf-8.csv
def read_source(filename):
    collections = {}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            if len(item) == 11:
                if item[1] != 'ISSN':
                    j = {}
                    j['collection'] = item[0]
                    j['issn-id'] = item[1]
                    j['pissn'] = item[2]
                    j['eissn'] = item[3]
                    j['acron'] = item[5]
                    j['short-title'] = item[6]
                    j['journal-title'] = item[7]
                    j['nlm-title'] = item[8]
                    j['publisher-name'] = item[9]
                    if not j['collection'] in collections.keys():
                        collections[j['collection']] = []
                    collections[j['collection']].append(j)
    return collections


def journal_data_for_markup(collections):
    collections_data = {}
    for collection_key, collection_journals in collections.items():
        r = {}
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
            r[item['journal-title']] = '|'.join(column)
        keys = r.keys()
        keys.sort()
        collections_data[collection_key] = '\r\n'.join([r[key] for key in keys])
    return collections_data


def write_files(path, collections_data):
    for key, file_content in collections_data.items():
        print('creating ' + path + '/markup_journals_' + key + '.csv')
        print('total: ' + str(len(file_content.split('\n'))))
        print('')
        write(path + '/markup_journals_' + key + '.csv', file_content)


def write_file(path, collection_name, file_content):
    print('creating ' + path + '/markup_journals.csv for ' + collection_name)
    write(path + '/markup_journals.csv', file_content)


def write(filename, content):
    f = codecs.open(filename, mode='w+')
    f.write(content)
    f.close()


def read_current(source):
    try:
        current = open(source, 'r').read()
    except:
        current = ''
    return current


def download_content(url):
    try:
        new = urllib2.urlopen(url).read()
    except:
        new = ''
    return new


def main(url, source, dest_path, collection_name=None):
    path = os.path.dirname(source)
    if not os.path.isdir(path):
        os.makedirs(path)
    current = ''
    if not os.path.isfile(source):
        current = read_current(source)
    new = download_content(url)

    if len(new) > len(current):
        open(source, 'w').write(new)
    r = read_source(source)
    r = journal_data_for_markup(r)
    if collection_name is None:
        write_files(dest_path, r)
    else:
        write_file(dest_path, collection_name, r[collection_name])

collection_name = None
print(sys.argv)
if len(sys.argv) > 1:
    collection_name = sys.argv[1]

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
source = CURRENT_PATH + '/markup/markup_journals.csv'
main('http://static.scielo.org/sps/markup_journals.csv', source, os.path.dirname(source), collection_name)
