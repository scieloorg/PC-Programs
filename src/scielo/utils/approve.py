ISSUETOC = '/scielo.php?script=sci_issuetoc&pid=<PID>&lng=<LANG>'


def diff_position(homolog, prod):
    coord = None
    if not homolog == prod:
        h_lines = break_lines(homolog)
        prod_lines = break_lines(prod)
        row, h, p = diff_items(h_lines, prod_lines)
        if row > 0:
            pos, h_words, p_words = diff_items(h[0], p[0])
            coord = (row, pos, h[0], h_words, p_words)
            open('./file1.txt', 'w').write('\n'.join(h_lines).encode('utf-8'))
            open('./file2.txt', 'w').write('\n'.join(prod_lines).encode('utf-8'))
    return coord


def break_lines(content):
    content = content.replace('</HEAD>', '')
    content = content.replace('\n', '~BREAK~')
    content = content.replace('<', '~BREAK~<')
    content = content.replace('>', '>~BREAK~')
    return [item.strip() for item in content.split('~BREAK~')]


def diff_items(f1, f2):
    pos = 0
    n = len(f1)
    if n > len(f2):
        n = len(f2)
    i = 0
    while i < n:
        if f1[i] == f2[i]:
            pass
        else:
            pos = i + 1
            f1 = f1[i:]
            f2 = f2[i:]
            break
        i += 1
    return (pos, f1, f2)


def normalize(content, term, norm):
    if content is None:
        content = ''
    return content.replace(term, norm)


def request(url, _timeout=30, debug=False):
    import urllib2
    r = None
    try:
        r = urllib2.urlopen(url, timeout=_timeout).read()
    except urllib2.URLError, e:
        if debug:
            print(" Oops, timed out?")
    except urllib2.socket.timeout:
        if debug:
            print(" Timed out!")
    except:
        if debug:
            print(" unknown")
    if debug:
        if r is None:
            print(' ' + url)
    return r


def find_internal_urls(content, site_uri):
    content = normalize(content, site_uri, '')
    content = content.replace(' href="/', ' href="~BREAK~~/')
    content = content.replace(' src="/', ' src="~BREAK~~/')
    internal_url_items = []
    for item in content.split('~BREAK~'):
        if item.startswith('~'):
            item = item[1:]
            item = item[0:item.find('"')]
            internal_url_items.append(item)
    return internal_url_items


def build_url(uri, script, pid, i_lang):
    return uri + script.replace('<PID>', pid).replace('<LANG>', i_lang)


def get_page(page_uri, script, pid, lang):
    url = build_url(page_uri, script, pid, lang)
    page_content = request(url, 30, True)
    if page_content is not None:
        if not isinstance(page_content, unicode):
            page_content = page_content.decode('utf-8')
        page_content = normalize(page_content, page_uri, '')
    return (url, page_content)


def main():
    homolog_uri = 'http://homolog.xml.scielosp.org'
    prod_uri = 'http://homolog.scielosp.org'
    pid = '0042-968620150006'
    script = ISSUETOC
    #['en', 'es', 'pt']
    for lang in ['en']:
        homolog_url, homolog_page = get_page(homolog_uri, script, pid, lang)
        prod_url, prod_page = get_page(prod_uri, script, pid, lang)
        if prod_page is None and homolog_page is None:
            print('Unable to get ')
            print(homolog_url)
            print(prod_url)
        else:
            coord = diff_position(homolog_page, prod_page)
            if not coord is None:
                row, pos, line, h, p = coord
                print('-'*10)
                print(str(row) + ':' + str(pos))
                print(line)
                print('-'*10)
                print(homolog_url)
                print(h)
                print('.'*10)
                print(prod_url)
                print(p)
                print('-'*10)

main()
