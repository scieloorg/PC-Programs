# coding=utf-8
import os
from datetime import datetime

from PIL import Image

IMDEBUGGING = False


def now():
    now = datetime.now().isoformat().replace('-', '').replace(':', '').replace('T', ' ')[0:13]
    return now.split(' ')


def display_datetime(dateiso, timeiso):
    y = dateiso[0:4]
    md = dateiso[4:]
    y = y + '-' + '-'.join([md[i*2:i*2+2] for i in range(0, 2)])
    if timeiso is not None:
        if len(timeiso) > 0:
            y += ' ' + ':'.join([timeiso[i*2:i*2+2] for i in range(0, 2)])
    return y


def is_similar(text, items, min_rate=0.8):
    if not isinstance(items, list):
        items = [items]
    highiest_rate, most_similar_items = most_similar(similarity(items, text, min_rate))
    return (highiest_rate > min_rate)


def how_similar(this, that):
    import difflib
    if this is None:
        this = 'None'
    if that is None:
        that = 'None'
    return difflib.SequenceMatcher(None, this.lower(), that.lower()).ratio()


def similarity(items, text, min_ratio=0):
    r = {}
    for item in items:
        rate = how_similar(item, text)
        if rate > min_ratio:
            if not rate in r.keys():
                r[rate] = []
            r[rate].append(item)
    return r


def most_similar(similarity):
    items = []
    highiest_rate = 0
    ratio_list = similarity.keys()
    if len(ratio_list) > 0:
        ratio_list = sorted(ratio_list)
        ratio_list.reverse()
        highiest_rate = ratio_list[0]
        items = similarity[highiest_rate]

    return (highiest_rate, items)


def debugging(text):
    if IMDEBUGGING:
        display_message(text)


def display_message(text):
    try:
        print(text)
    except Exception as e:
        import sys
        try:
            print(text.encode(encoding=sys.getfilesystemencoding()))
        except:
            print('error in display_message')
            print(sys.getfilesystemencoding())


def is_tiff(img_filename):
    return os.path.splitext(img_filename)[1] in ['.tiff', '.tif']


def tiff_image(img_filename):
    if is_tiff(img_filename):
        if os.path.isfile(img_filename):
            return Image.open(img_filename)


def valid_formula_min_max_height(values, percent=0.25):
    m = 0
    if len(values) > 0:
        m = values[int(len(values)/2)]
    r = int(m * percent)
    _min = m - r
    _max = m + r
    if _min < 16:
        m = 16 + r
    if _max > 200:
        m = 200 - r
    return (m - r, m + r)


def words_not_found(sentence, other_sentence):
    not_found = []
    for word in sentence.split():
        if not word in other_sentence:
            not_found.append(word)
    return not_found


def hightlight_equal(sentence1, sentence2):
    s2 = ''
    s1 = []
    diff = ''
    for item in sentence1.split():
        if item in sentence2:
            diff = sentence2[0:sentence2.find(item)]
            #if len(diff.strip()) > 0:
            #    diff = ' {{' + diff + '}} '
            s2 += diff + ' **' + item + '** '
            sentence2 = sentence2[sentence2.find(item)+len(item):]
            item = ' **' + item + '** '
        s1.append(item)
    return [' ' + ' '.join(s1) + ' ', s2 + ' ' + sentence2]


def repl(matchobj):
    return matchobj.group(0).replace(matchobj.group(1), u'')

