# coding=utf-8

from datetime import datetime
import urllib2


MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def url_check(url, _timeout=30):
    print(datetime.now().isoformat() + ' url checking ' + url)
    try:
        r = urllib2.urlopen(url, timeout=_timeout).read()
    except urllib2.URLError, e:
        r = None
        print(datetime.now().isoformat() + " Oops, timed out?")
    except urllib2.socket.timeout:
        r = None
        print(datetime.now().isoformat() + " Timed out!")
    except:
        r = None
        print(datetime.now().isoformat() + " unknown")
    return (r is not None)


def how_similar(this, that):
    import difflib
    if this is None:
        this = ''
    if that is None:
        that = ''
    return difflib.SequenceMatcher(None, this.lower(), that.lower()).ratio()


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


def doi_pid(doi):
    pid = None

    if doi is not None:
        import json

        try:
            f = urllib2.urlopen('http://dx.doi.org/' + doi, timeout=1)
            url = f.geturl()

            if 'scielo.php?script=sci_arttext&amp;pid=' in url:
                pid = url[url.find('pid=')+4:]
                pid = pid[0:23]

                try:
                    f = urllib2.urlopen('http://200.136.72.162:7000/api/v1/article?code=' + pid + '&format=json', timeout=60)
                    article_json = json.loads(f.read())
                    v880 = article_json['article'].get('v880')
                    v881 = article_json['article'].get('v881')

                    pid = v881 if v881 is not None else v880
                except:
                    pass
        except:
            pass
    return pid


def format_dateiso_from_date(year, month, day):
    return year + month + day


def format_dateiso(adate):
    if adate is not None:
        month = adate.get('season')
        if month is None:
            month = adate.get('month')
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
    return '-'.join(r) + '\n'


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
        text = text.replace('>', '>_BREAK_IGNORE1')
        text = text.replace('</', 'IGNORE2_BREAK_</')
        parts = text.split('_BREAK_')
        new = []
        for part in parts:
            if 'IGNORE2' in part and 'IGNORE1' in part:
                c = part.replace('IGNORE1', '').replace('IGNORE2', '')
                if len(c.strip()) > 1:
                    new.append(c)
            else:
                new.append(part.replace('IGNORE1', '').replace('IGNORE2', ''))

        text = ''.join(new)
        while '<xref' in text:
            xref = text[text.find('<xref'):]
            xref = xref[0:xref.find('>')+1]
            text = text.replace(xref, '')
        text = text.replace('</xref>', '')
        text = text.replace('</sup>', '')
        text = text.replace('<sup>', '')
        text = text.replace('<sup/>', '')
        text = text.strip()
        if article_title != text:
            print(article_title)
            print(text)
    return text
