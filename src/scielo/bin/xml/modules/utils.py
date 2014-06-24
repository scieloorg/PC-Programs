# coding=utf-8

MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def u_encode(u, encoding):
    r = u
    if type(u) is unicode:
        try:
            r = u.encode(encoding, 'replace')
        except Exception as e:
            try:
                r = u.encode(encoding, 'xmlcharrefreplace')
            except Exception as e:
                r = u.encode(encoding, 'ignore')
    return r


def doi_pid(doi):
    pid = None

    if doi is not None:
        import urllib2
        import json

        try:
            f = urllib2.urlopen('http://dx.doi.org/' + doi)
            url = f.geturl()

            if 'scielo.php?script=sci_arttext&amp;pid=' in url:
                pid = url[url.find('pid=')+4:]
                pid = pid[0:23]

                try:
                    f = urllib2.urlopen('http://200.136.72.162:7000/api/v1/article?code=' + pid + '&format=json')
                    article_json = json.loads(f.read())
                    v880 = article_json['article'].get('v880')
                    v881 = article_json['article'].get('v881')

                    pid = v881 if v881 is not None else v880
                except:
                    pass
        except:
            pass
    return pid


def format_dateiso(adate):
    if adate is not None:
        month = adate.get('season')
        if month is None:
            month = adate.get('month')
        else:
            if '-' in month:
                month = month[0:month.find('-')]
            month = MONTHS.get(month, '00')

        if month == '' or month is None:
            month = '00'
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
    return label + ': ' + value if value is None else 'None'


def display_values(label, values):
    return label + ': ' + '\n'.join(values)


def display_attributes(label, attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        r.append('@' + key + ': ' + value)
    return label + '\n' + '\n'.join(r)


def display_items_with_attributes(label, items_with_attributes):
    r = label + ': ' + '\n'
    for item_name, item_values in items_with_attributes.items():
        r += display_values_with_attributes(item_name, item_values)
    return r


def display_values_with_attributes(label, values_with_attributes):
    return label + ': ' + '\n' + '\n'.join([display_attributes('=>', item) for item in values_with_attributes])


def conditional_required(label, value):
    return display_value(label, value) if value is not None else 'WARNING: Required ' + label + ', if exists. '


def required(label, value):
    return display_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '


def required_one(label, value):
    return display_attributes(label, value) if value is not None else 'ERROR: Required ' + label + '. '


def expected_values(label, value, expected):
    return display_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)


def update_values(filename, values, value):
    if not value in values.keys():
        values[value] = []
    values[value].append(filename)
    return values


def article_data(article):
    data = {}
    data['journal-title'] = article.journal_title
    data['journal_id_nlm_ta'] = article.journal_id_nlm_ta
    data['journal_issns'] = article.journal_issns
    data['publisher_name'] = article.publisher_name
    data['issue_label'] = article.issue_label
    data['issue_date'] = article.issue_date
    data['order'] = article.order
    data['doi'] = article.doi
    data['fpage'] = article.fpage
    data['fpage_seq'] = article.fpage_seq
    data['elocation_id'] = article.elocation_id
    return data
