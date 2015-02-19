import os
import sys
import shutil


def remove_tags(text):
    text = text.replace('[', '***BREAK***IGNORE[')
    text = text.replace(']', ']IGNORE***BREAK***')
    items = text.split('***BREAK***')
    r = ''
    for item in items:
        if item.endswith(']IGNORE') or item.startswith('IGNORE['):
            r += ''
        else:
            r += item
    return r


def run_wayta(text):
    import urllib
    import urllib2

    result = None
    values = {
                'q': text,
              }
    url = 'http://wayta.scielo.org/api/v1/institution'
    try:
        data = urllib.urlencode(values)
        full_url = url + '?' + data
        print(full_url)
        response = urllib2.urlopen(full_url, timeout=5)
        result = response.read()
    except Exception as e:
        print(e)
    return result


def format_results(result):
    import json
    r = []

    try:
        results = json.loads(result)
        for item in results.get('choices'):
            if item.get('country', '') != '' and item.get('value', '') != '':
                r.append(item.get('country') + ' - ' + item.get('value'))
    except Exception as e:
        print(e)
    return r


def encode_results(results):
    r = []
    for item in results:
        text = ''
        if isinstance(item, unicode):
            try:
                text = item.encode('cp1252')
            except Exception as e:
                try:
                    text = item.encode('cp1252', 'xmlcharrefreplace')
                except Exception as e:
                    print(e)
                    print(item)
        if len(text) > 0:
            r.append(text)
    return '\n'.join(r)


def search(text):
    text = remove_tags(text)
    text = text.replace(' - ', ',')
    text = text.replace(';', ',')
    parts = text.split(',')
    results = []
    for part in parts:
        wayta_result = run_wayta(part)
        result = format_results(wayta_result)
        results += result
    r = sorted(list(set(results)))
    return r


text = None
filename = None
ctrl_filename = None

if len(sys.argv) == 4:
    ign, filename, ctrl_filename, text = sys.argv
    if os.path.isfile(filename):
        os.unlink(filename)
    if os.path.isfile(ctrl_filename):
        os.unlink(ctrl_filename)
    open(filename, 'w').write(encode_results(search(text)))
    if os.path.isfile(filename):
        shutil.copyfile(filename, ctrl_filename)
    else:
        open(ctrl_filename, 'w').write('fim1')
else:
    open(ctrl_filename, 'w').write('fim')
    print('invalid parameters')
