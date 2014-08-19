# code utf-8


import csv
import urllib2
import codecs


#http://static.scielo.org/sps/titles-tab-utf-8.csv
def read_source(filename):
    r = []
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for item in spamreader:
            if len(item) == 10:
                if item[1] != 'ISSN':
                    j = {}
                    j['issn-id'] = item[1]
                    j['pissn'] = item[2]
                    j['eissn'] = item[3]
                    j['acron'] = item[5]
                    j['short-title'] = item[6]
                    j['journal-title'] = item[7]
                    j['nlm-title'] = item[8]
                    j['publisher-name'] = item[9]
                    r.append(j)
    return r


def journal_data_for_markup(lines):
    r = {}
    for item in lines:
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
    return '\r\n'.join([r[key] for key in keys])


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


def main(url, source, dest):
    current = read_current(source)
    new = download_content(url)
    #new = ''
    if len(new) > len(current):
        open(source, 'w').write(new)
    r = read_source(source)
    r = journal_data_for_markup(r)

    write(dest, r)


main('http://static.scielo.org/sps/markup_journals.csv', './table.csv', './markup_journals.csv')
