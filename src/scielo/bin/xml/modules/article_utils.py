
# coding=utf-8

from datetime import datetime
import urllib2
import json

import utils

MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def display_date(dateiso):
    if dateiso is None:
        dateiso = ''
    else:
        dateiso = dateiso[0:4] + '/' + dateiso[4:6] + '/' + dateiso[6:8]
    return dateiso


def dateiso2datetime(dateiso):
    y = int(dateiso[0:4])
    m = int(dateiso[4:6])
    d = int(dateiso[6:8])
    if d == 0:
        d = 1
    if m == 0:
        m = 1
    return datetime(y, m, d)


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


def url_check(url, _timeout=30):
    utils.display_message(datetime.now().isoformat() + ' url checking ' + url)
    try:
        r = urllib2.urlopen(url, timeout=_timeout).read()
    except urllib2.URLError, e:
        r = None
        utils.display_message(datetime.now().isoformat() + " Oops, timed out?")
    except urllib2.socket.timeout:
        r = None
        utils.display_message(datetime.now().isoformat() + " Timed out!")
    except:
        r = None
        utils.display_message(datetime.now().isoformat() + " unknown")
    return (r is not None)


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


def doi_pid(doi_query_result):
    pid = None
    if doi_query_result is not None:
        article_json = json.loads(doi_query_result)
        alt_id_items = article_json.get('message', {}).get('alternative-id')
        pid = None
        if alt_id_items is not None:
            if isinstance(alt_id_items, list):
                pid = alt_id_items[0]
            else:
                pid = alt_id_items
    return pid


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
    return display_value(label, value) if value is not None else 'WARNING: Required ' + label + ', if exists. '


def required(label, value):
    return display_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '


def required_one(label, value):
    return display_attributes(label, value) if value is not None else 'ERROR: Required ' + label + '. '


def expected_values(label, value, expected):
    return display_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)


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
                if '-' in year:
                    year = year.split('-')
                    year = [y for y in year if len(y) == 4]
                    if len(year) == 1:
                        year = year[0]
                    else:
                        year = ''
                if len(year) > 4:
                    if year[0:4].isdigit():
                        year = year[0:4]
                    elif year[1:5].isdigit():
                        year = year[1:5]
    return year


def doi_query(doi):
    r = None
    if doi is not None:
        if 'dx.doi.org' in doi:
            doi = doi[doi.find('dx.doi.org/')+len('dx.doi.org/'):]
        _url = 'http://api.crossref.org/works/' + doi
        try:
            r = urllib2.urlopen(_url, timeout=20).read()
        except urllib2.URLError, e:
            r = '{}'
            utils.display_message(_url)
            utils.display_message(datetime.now().isoformat() + " Oops, timed out?")
        except urllib2.socket.timeout:
            r = None
            utils.display_message(_url)
            utils.display_message(datetime.now().isoformat() + " Timed out!")
        except:
            utils.display_message(_url)
            r = None
            utils.display_message(datetime.now().isoformat() + " unknown")
    return r


def doi_journal_and_article(doi_query_result):
    journal_titles = None
    article_titles = None
    if doi_query_result is not None:
        article_json = json.loads(doi_query_result)
        journal_titles = article_json.get('message', {}).get('container-title')
        if journal_titles is not None:
            if not isinstance(journal_titles, list):
                journal_titles = [journal_titles]
        article_titles = article_json.get('message', {}).get('title')
        if article_titles is not None:
            if not isinstance(article_titles, list):
                article_titles = [article_titles]
    return (journal_titles, article_titles)
