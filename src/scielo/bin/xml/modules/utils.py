# coding=utf-8

IMDEBUGGING = False


def display_datetime(dateiso, timeiso):
    y = dateiso[0:4]
    md = dateiso[4:]
    return y + '-' + '-'.join([md[i*2:i*2+2] for i in range(0, 2)]) + ' ' + ':'.join([timeiso[i*2:i*2+2] for i in range(0, 2)])


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
        print(text)


def display_message(text):
    print(text)
