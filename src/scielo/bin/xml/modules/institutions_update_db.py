# coding=utf-8

import sys
import os

import fs_utils


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

source = 'https://raw.githubusercontent.com/scieloorg/wayta/master/processing/normalized_aff.csv'
wayta_normalized_aff = curr_path + '/../tables/wayta_normalized_aff.csv'

wayta_orgname_location_country = curr_path + '/../tables/wayta_orgname_location_country.csv'
local_orgname_location_country = curr_path + '/../tables/orgname_location_country.csv'
deleted_report = curr_path + '/../tables/diff_deleted.txt'
added_report = curr_path + '/../tables/diff_added.txt'


def find_diff(old, new, deleted_report, added_report):
    old_items = fs_utils.read_file(old)
    old_items = old_items.split('\n')
    print(len(old_items))
    new_items = fs_utils.read_file(new)
    new_items = new_items.split('\n')
    print(len(new_items))
    print(new_items[0])
    print(old_items[0])

    old_items = [item.strip() for item in old_items]
    new_items = [item.strip() for item in new_items]

    deleted = []
    for item in old_items:
        if not item in new_items:
            print(item)
            deleted.append(item)
    print('deleted')
    print(len(deleted))

    added = []
    for item in new_items:
        if not item in old_items:
            print(item)
            added.append(item)
    print('added')
    print(len(added))

    #added = [item for item in new_items if not item in old_items]
    #print('added')
    #print(len(added))
    fs_utils.write_file(deleted_report, '\n'.join(deleted))
    fs_utils.write_file(added_report, '\n'.join(added))

    print(deleted_report)
    print(added_report)


def fix_endoflines(filename, destination):
    r = []
    items = fs_utils.read_file(filename)
    for item in items.split('\n'):
        r.append(item.strip())
    fs_utils.write_file(destination, '\n'.join(sorted(items)))


def wayta_csv(source, wayta_normalized_aff, wayta_orgname_location_country):
    items = fs_utils.get_downloaded_data(source, wayta_normalized_aff)
    results = []
    for item in items.split('\n'):
        parts = item.split(';')
        if len(parts) == 6:
            bad, correct, country_name, country_code, state, city = parts
            results.append('\t'.join([correct, city, state, country_code, country_name]))
    results = list(set(results))
    print(len(results))
    fs_utils.write_file(wayta_orgname_location_country, '\n'.join(sorted(results)))
    print('downloaded')


if len(sys.argv) > 0:
    if sys.argv[1] == 'download':
        wayta_csv()
    elif sys.argv[1] == 'diff':
        find_diff(local_orgname_location_country, wayta_orgname_location_country, deleted_report, added_report)
    elif sys.argv[1] == 'updatedb':
        if fs_utils.read_file(wayta_orgname_location_country) == fs_utils.read_file(local_orgname_location_country):
            import institutions_service
            a = institutions_service.OrgManager()
            a.create_db()
            print('db updated')
    else:
        print('invalid parameters')
