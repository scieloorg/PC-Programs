# coding=utf-8

import sys
import os

import fs_utils
import utils


curr_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

source = 'https://raw.githubusercontent.com/scieloorg/wayta/master/processing/normalized_aff.csv'
wayta_normalized_aff = curr_path + '/../tables/wayta_normalized_aff.csv'

wayta_orgname_location_country = curr_path + '/../tables/wayta_orgname_location_country.csv'
local_orgname_location_country = curr_path + '/../tables/orgname_location_country.csv'
fixed_report = curr_path + '/../tables/diff_fixed.txt'
replaced_report = curr_path + '/../tables/diff_replaced.txt'
deleted_report = curr_path + '/../tables/diff_deleted.txt'
added_report = curr_path + '/../tables/diff_added.txt'


def found_similar(text, items):
    rate, similar_items = utils.most_similar(utils.similarity(items, text, min_ratio=0.96))

    if len(similar_items) > 0:
        return similar_items[0]


def found_similar_2(text, items):
    ranking = {}
    for item in items:
        item_chars = list(item)
        i = 0
        differences = 0
        for c in text:
            if not c.lower() == item_chars[i].lower():
                differences += 1
        if not differences in ranking.keys():
            ranking[differences] = []
        ranking[differences].append(item)
    if len(ranking) > 0:
        order = sorted(ranking.keys())
        if order[0] <= 2:
            return ranking[order[0]][0]


def classify_items_by_len(items):
    organized = {}
    for item in items:
        n = len(item)
        if not n in organized.keys():
            organized[n] = []
        organized[n].append(item)
    return organized


def remove_exceding_blank_spaces(content):
    lines = []
    for row in content.split('\n'):
        while ' '*2 in row:
            row = row.replace(' '*2, ' ')
        lines.append('\t'.join([col.strip() for col in row.strip().split('\t')]))
    return '\n'.join(lines)


def report_differences(old, new, deleted_report, added_report, fixed_report, replaced_report):
    old_items = fs_utils.read_file(old)
    old_items = old_items.split('\n')
    print('current:')
    print(len(old_items))

    new_items = fs_utils.read_file(new)
    new_items = new_items.split('\n')
    print('new:')
    print(len(new_items))

    maybe_deleted = []
    for item in old_items:
        if not item in new_items:
            maybe_deleted.append(item)

    maybe_added = []
    for item in new_items:
        if not item in old_items:
            maybe_added.append(item)

    print('=>')
    print([len(maybe_deleted), len(maybe_added)])
    organized_items = classify_items_by_len(maybe_added)

    deleted = []
    replaced = []
    fixed = []
    total = '/' + str(len(maybe_deleted))
    i = 0
    for item in maybe_deleted:
        i += 1
        if str(i).endswith('500') or str(i).endswith('000'):
            print(str(i) + total)

        similar = found_similar(item, maybe_added)
        if similar is None:
            similar = found_similar_2(item, organized_items.get(len(item), []))
        if similar is None:
            deleted.append(item)
        else:
            replaced.append(item + '\n' + similar + '\n')
            fixed.append(similar)

    added = [item for item in maybe_added if not item in fixed]

    fs_utils.write_file(replaced_report, '\n'.join(replaced))
    fs_utils.write_file(fixed_report, '\n'.join(fixed))
    fs_utils.write_file(deleted_report, '\n'.join(deleted))
    fs_utils.write_file(added_report, '\n'.join(added))

    return [len(deleted), len(added), len(fixed)]


def fix_endoflines(filename, destination):
    r = []
    items = fs_utils.read_file(filename)
    for item in items.split('\n'):
        r.append(item.strip())
    fs_utils.write_file(destination, '\n'.join(sorted(items)))


def update_wayta_orgname_location_country(source, wayta_normalized_aff, wayta_orgname_location_country):
    items = fs_utils.get_downloaded_data(source, wayta_normalized_aff)
    print('wayta normalized aff')
    print(len(items.split('\n')))

    items = items.replace(';', '\t')
    print(1)
    print(len(items.split('\n')))

    items = remove_exceding_blank_spaces(items)
    print(2)
    print(len(items.split('\n')))

    items = items.split('\n')
    print(3)
    print(len(items))

    results = []
    for item in items:
        if item.startswith('"') and '"\t' in item:
            item = item[1:].replace('"\t', '\t')
        item = item.replace('""', '"')
        parts = item.split('\t')
        if len(parts) == 6:
            bad, correct, country_name, country_code, state, city = parts
            results.append('\t'.join([correct, city, state, country_code, country_name]))
    results = list(set(results))
    print('downloaded:')
    print(len(results))
    fs_utils.write_file(wayta_orgname_location_country, '\n'.join(sorted(results)))


execute_update = False
if len(sys.argv) == 1:
    update_wayta_orgname_location_country(source, wayta_normalized_aff, wayta_orgname_location_country)
    counts = report_differences(local_orgname_location_country, wayta_orgname_location_country, deleted_report, added_report, fixed_report, replaced_report)

    print('->')
    print(counts)
    print(sum(counts))

elif len(sys.argv) == 2:
    execute_update = (sys.argv[1] == 'update')
    if sys.argv[1] == 'fix_local':
        fs_utils.write_file(local_orgname_location_country, remove_exceding_blank_spaces(fs_utils.read_file(local_orgname_location_country)))

if execute_update is True:
    import institutions_service
    a = institutions_service.OrgManager()
    a.create_db()
    print('db updated')
else:
    print('No update')
