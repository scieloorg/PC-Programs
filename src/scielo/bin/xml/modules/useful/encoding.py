# coding=utf-8


def is_unicode(content):
    try:
        r = isinstance(content, unicode)
    except:
        r = True
    return r


def decode(content, encoding='utf-8'):
    if content is None:
        return
    if not is_unicode(content):
        try:
            content = content.decode(encoding)
        except Exception as e:
            print('decode:', e)
    return content


def encode(content, encoding='utf-8', error_handler=None):
    """
    position 0: ordinal not in range(128)
    >>> u.encode('ascii', 'ignore')
    'abcd'
    >>> u.encode('ascii', 'replace')
    '?abcd?'
    >>> u.encode('ascii', 'xmlcharrefreplace')
    '&#40960;abcd&#1972;'
    """
    if content is None:
        return
    if is_unicode(content):
        if error_handler in ['xmlcharrefreplace', 'replace', 'ignore']:
            try:
                content = content.encode(encoding, error_handler)
            except Exception as e:
                print(e)
        else:
            try:
                content = content.encode(encoding)
            except Exception as e:
                try:
                    content = content.encode(encoding, 'xmlcharrefreplace')
                    print('xmlcharrefreplace')
                except Exception as e:
                    try:
                        content = content.encode(encoding, 'replace')
                        print('replace')
                    except Exception as e:
                        try:
                            content = content.encode(encoding, 'ignore')
                            print('ignore')
                        except Exception as e:
                            print('encode: ', e)
    return content
