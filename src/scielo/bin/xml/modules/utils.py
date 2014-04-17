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
