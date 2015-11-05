# coding=utf-8

IMDEBUGGING = False


def display_datetime(dateiso, timeiso):
    y = dateiso[0:4]
    md = dateiso[4:]
    return y + '-' + '-'.join([md[i*2:i*2+2] for i in range(0, 2)]) + ' ' + ':'.join([timeiso[i*2:i*2+2] for i in range(0, 2)])


def is_similar(text, items, min_rate=0.8):
    if not isinstance(items, list):
        items = [items]
    highiest_rate, most_similar_items = most_similar(similarity(items, text, min_rate))
    print([highiest_rate, most_similar_items])
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
