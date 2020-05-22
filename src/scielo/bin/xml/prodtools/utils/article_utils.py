
# coding=utf-8

from datetime import datetime

from prodtools import _

from prodtools.utils import img_utils
from prodtools.reports import validation_status


URL_CHECKED = []

MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }
_MONTHS = {v: k for k, v in MONTHS.items()}
MONTHS_ABBREV = '|' + '|'.join([_MONTHS[k] for k in sorted(_MONTHS.keys()) if k != '00']) + '|'


def days(begin_label, begin_dateiso, end_label, end_dateiso):
    if begin_dateiso is not None and end_dateiso is not None:
        errors = []
        errors.extend(is_fulldate(begin_label, begin_dateiso))
        errors.extend(is_fulldate(end_label, end_dateiso))
        if len(errors) == 0:
            return (dateiso2datetime(end_dateiso) - dateiso2datetime(begin_dateiso)).days


def is_fulldate(label, dateiso):
    y, m, d = dateiso[0:4], dateiso[4:6], dateiso[6:8]
    y = int(dateiso[0:4]) if y.isdigit() else 0
    m = int(dateiso[4:6]) if m.isdigit() else 0
    d = int(dateiso[6:8]) if d.isdigit() else 0
    msg = []
    if not y > 0:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=y, label='year (' + label + ')'))
    if not 0 < m <= 12:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=m, label='month (' + label + ')'))
    if not d <= 31:
        msg.append(_('{value} is an invalid value for {label}. ').format(value=d, label='day (' + label + ')'))
    if len(msg) == 0:
        try:
            r = datetime(y, m, d)
        except:
            msg.append(_('{value} is an invalid value for {label}. ').format(value=d, label=label + ': day '))
    return msg


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
        if number.strip().isdigit():
            return str(int(number))
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
            if 's/d' not in year and 's.d' not in year:
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


def image_heights(path, href_list):
    items = []
    for href in href_list:
        img = img_utils.tiff_image(path + '/' + href.src)
        if img is not None:
            items.append(img.size[1])
    return sorted(items)
