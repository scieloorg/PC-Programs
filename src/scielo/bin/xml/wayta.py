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
            if item.get('country') is not None and item.get('value') is not None:
                r.append(item.get('country') + ' - ' + item.get('value'))
    except Exception as e:
        print(e)
    return r


def save_result(results, filename):
    r = '\n'.join(results)
    print(r)
    if isinstance(r, unicode):
        r = r.encode('cp1252')
    open(filename, 'w').write(r)


def search(text):
    text = remove_tags(text)
    parts = text.split(',')
    results = []
    for part in parts:
        print(part)
        wayta_result = run_wayta(part)
        result = format_results(wayta_result)
        print(result)
        results += result
    print(results)
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
    save_result(search(text), filename)
    if os.path.isfile(filename):
        shutil.copyfile(filename, ctrl_filename)
    else:
        open(ctrl_filename, 'w').write('fim1')
else:
    open(ctrl_filename, 'w').write('fim')
    print('invalid parameters')
