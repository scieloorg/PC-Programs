
# coding=utf-8

from datetime import datetime
import json

from PIL import Image

import validation_status
import utils
import institutions_service
import article as article_module


URL_CHECKED = []

MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }
_MONTHS = {v: k for k, v in MONTHS.items()}
MONTHS_ABBREV = '|' + '|'.join([_MONTHS[k] for k in sorted(_MONTHS.keys()) if k != '00']) + '|'


def display_date(dateiso):
    if dateiso is None:
        dateiso = ''
    else:
        dateiso = dateiso[0:4] + '/' + dateiso[4:6] + '/' + dateiso[6:8]
    return dateiso


def dateiso2datetime(dateiso):
    r = None
    if dateiso is not None:
        dateiso = dateiso + '0'*8
        dateiso = dateiso[0:8]
        y = int(dateiso[0:4])
        m = int(dateiso[4:6])
        d = int(dateiso[6:8])
        if y == 0:
            y = 1
        if d == 0:
            d = 1
        if m == 0:
            m = 1
        r = datetime(y, m, d)
    return r


def normalize_number(number):
    if number is not None:
        number = number.strip()
        if number.isdigit():
            number = str(int(number))
    return number


def get_number_suppl_compl(issue_element_content):
    number = None
    suppl = None
    compl = None
    if issue_element_content is not None:
        parts = issue_element_content.strip().lower().split(' ')
        if len(parts) == 1:
            # suppl or n
            if parts[0].startswith('sup'):
                suppl = parts[0]
            else:
                number = parts[0]
        elif len(parts) == 2:
            #n suppl or suppl s or n pr
            if parts[0].startswith('sup'):
                suppl = parts[1]
            elif parts[1].startswith('sup'):
                number, suppl = parts
            else:
                number, compl = parts
        elif len(parts) == 3:
            # n suppl s
            number, ign, suppl = parts
    if suppl is not None:
        if suppl.startswith('sup'):
            suppl = '0'
    return (number, suppl, compl)


def format_issue_label(year, volume, number, volume_suppl, number_suppl, compl):
    year = year if number == 'ahead' else ''
    v = 'v' + volume if volume is not None else None
    vs = 's' + volume_suppl if volume_suppl is not None else None
    n = 'n' + number if number is not None else None
    ns = 's' + number_suppl if number_suppl is not None else None
    return ''.join([i for i in [year, v, vs, n, ns, compl] if i is not None])


def u_encode(u, encoding):
    r = u
    if isinstance(u, unicode):
        try:
            r = u.encode(encoding, 'xmlcharrefreplace')
        except Exception as e:
            try:
                r = u.encode(encoding, 'replace')
            except Exception as e:
                r = u.encode(encoding, 'ignore')
    return r


def format_dateiso_from_date(year, month, day):
    return year + month + day


def format_dateiso(adate):
    if adate is not None:
        month = adate.get('season')
        if month is None:
            month = adate.get('month')
        if month is None:
            month = '00'
        else:
            if '-' in month:
                month = month[month.find('-')+1:]
            if not month.isdigit():
                month = MONTHS.get(month, '00')
            month = '00' + month
            month = month[-2:]
        y = adate.get('year', '0000')
        if y is None:
            y = '0000'
        d = adate.get('day', '00')
        if d is None:
            d = '00'
        d = '00' + d
        d = d[-2:]
        return y + month + d


def display_pages(fpage, lpage):
    if fpage is not None and lpage is not None:
        n = lpage
        if len(fpage) == len(lpage):
            i = 0
            n = ''
            for i in range(0, len(fpage)):
                if fpage[i:i+1] != lpage[i:i+1]:
                    n = lpage[i:]
                    break
                i += 1
        lpage = n if n != '' else None
    r = []
    if fpage is not None:
        r.append(fpage)
    if lpage is not None:
        r.append(lpage)
    return '-'.join(r)


def display_value(label, value):
    return label + ': ' + value + '\n' if value is not None else 'None\n'


def display_values(label, values):
    return label + ': ' + '\n'.join(values) + '\n'


def display_attributes(label, attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        r.append(display_value(key, value))
    return label + '\n' + '\n'.join(r) + '\n'


def display_items_with_attributes(label, items_with_attributes):
    r = label + ': ' + '\n'
    for item_name, item_values in items_with_attributes.items():
        r += display_values_with_attributes(item_name, item_values)
    return r + '\n'


def display_values_with_attributes(label, values_with_attributes):
    return label + ': ' + '\n' + '\n'.join([display_attributes('=>', item) for item in values_with_attributes]) + '\n'


def conditional_required(label, value):
    return display_value(label, value) if value is not None else validation_status.STATUS_WARNING + ': Required ' + label + ', if exists. '


def required(label, value):
    return display_value(label, value) if value is not None else validation_status.STATUS_ERROR + ': Required ' + label + '. '


def required_one(label, value):
    return display_attributes(label, value) if value is not None else validation_status.STATUS_ERROR + ': Required ' + label + '. '


#FIXME apagar
def add_new_value_to_index(dict_key_and_values, key, value, normalize_key=True):
    def normalize_value(value):
        if not isinstance(value, unicode):
            value = value.decode('utf-8')
        return ' '.join(value.split())
    if key is None:
        key = 'None'
    if key is not None:
        if normalize_key:
            key = normalize_value(key)
        if not key in dict_key_and_values.keys():
            dict_key_and_values[key] = []
        dict_key_and_values[key].append(value)
    return dict_key_and_values


def format_date(dates):
    r = ''
    if dates is not None:
        r = ' '.join([k + ': ' + v for k, v in dates.items() if v is not None])
    return r


def remove_xref(article_title):
    text = article_title
    if text is not None:
        text = text.replace('<xref', '_BREAK_<xref')
        text = text.replace('</xref>', '</xref>_BREAK_')
        parts = text.split('_BREAK_')
        new = []
        for part in parts:
            if '<xref' in part and '</xref>' in part:
                pass
            else:
                new.append(part)

        text = ''.join(new)
        text = text.replace('<sup></sup>', '')
        text = text.replace('<sup/>', '')
        text = text.strip()
    return text


def four_digits_year(year):
    if year is not None:
        if not year.isdigit():
            if not 's/d' in year and not 's.d' in year:
                year = year.replace('/', '-')
                splited = None
                if '-' in year:
                    splited = year.split('-')
                elif ' ' in year:
                    splited = year.split(' ')
                if splited is None:
                    splited = [year]
                splited = [y for y in splited if len(y) == 4 and y.isdigit()]
                if len(splited) > 0:
                    year = splited[0]
        if len(year) > 4:
            if year[0:4].isdigit():
                year = year[0:4]
            elif year[1:5].isdigit():
                year = year[1:5]
    return year


def normalize_affiliations(article):
    article.normalized_affiliations = {}
    for aff in article.affiliations:
        norm_aff, ign = normalized_institution(aff)
        if norm_aff is not None:
            article.normalized_affiliations[aff.id] = norm_aff


def normalized_institution(aff):
    norm_aff = None
    found_institutions = None
    orgnames = [item.upper() for item in [aff.orgname, aff.norgname] if item is not None]
    if aff.norgname is not None or aff.orgname is not None:
        found_institutions = institutions_service.validate_organization(aff.orgname, aff.norgname, aff.country, aff.i_country, aff.state, aff.city)

    if found_institutions is not None:
        if len(found_institutions) == 1:
            valid = found_institutions
        else:
            valid = []
            # identify i_country
            if aff.i_country is None and aff.country is not None:
                country_info = {norm_country_name: norm_country_code for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in found_institutions if norm_country_name is not None and norm_country_code is not None}
                aff.i_country = country_info.get(aff.country)

            # match norgname and i_country in found_institutions
            for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in found_institutions:
                if norm_orgname.upper() in orgnames:
                    if aff.i_country is None:
                        valid.append((norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name))
                    elif aff.i_country == norm_country_code:
                        valid.append((norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name))

            # mais de uma possibilidade, considerar somente norgname e i_country, desconsiderar city, state, etc
            if len(valid) > 1:
                valid = list(set([(norm_orgname, None, None, norm_country_code, None) for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in valid]))

        if len(valid) == 1:
            norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name = valid[0]

            if norm_orgname is not None and norm_country_code is not None:
                norm_aff = article_module.Affiliation()
                norm_aff.id = aff.id
                norm_aff.norgname = norm_orgname
                norm_aff.city = norm_city
                norm_aff.state = norm_state
                norm_aff.i_country = norm_country_code
                norm_aff.country = norm_country_name
    return (norm_aff, found_institutions)


def image_heights(path, href_list):
    items = []
    for href in href_list:
        img = utils.tiff_image(path + '/' + href.src)
        if img is not None:
            items.append(img.size[1])
    return sorted(items)
