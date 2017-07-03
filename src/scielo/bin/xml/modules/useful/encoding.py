# coding=utf-8


def notuni2uni(content, encoding='utf-8'):
    if content is None:
        return
    if not isinstance(content, unicode):
        try:
            content = content.decode(encoding)
        except:
            try:
                content = content.decode('iso-8859-1')
            except Exception as e:
                print(e)
    return content


def uni2notuni(content, encoding='utf-8', error_handler=None):
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
    if isinstance(content, unicode):
        if error_handler in ['xmlcharrefreplace', 'replace', 'ignore']:
            try:
                content = content.encode(encoding, error_handler)
            except Exception as e:
                print(e)
        else:
            try:
                content = content.encode(encoding)
            except Exception as e:
                if error_handler is not None:
                    try:
                        content = content.encode(encoding, 'xmlcharrefreplace')
                    except Exception as e:
                        try:
                            content = content.encode(encoding, 'replace')
                        except Exception as e:
                            try:
                                content = content.encode(encoding, 'ignore')
                            except Exception as e:
                                print(e)
    return content
