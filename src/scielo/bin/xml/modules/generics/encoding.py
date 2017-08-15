# coding=utf-8


def is_encodable(content):
    try:
        r = isinstance(content, unicode)
    except:
        r = False
    return r


def decode(content, encoding='utf-8'):
    if content is None:
        return
    if not is_encodable(content) and hasattr(content, 'decode'):
        try:
            content = content.decode(encoding)
        except Exception as e:
            print('decode:', type(content), e)
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
    if is_encodable(content):
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
                    print(e)
                    print(content[content.find('&')-10:content.find('&')+10])
                except Exception as e:
                    try:
                        content = content.encode(encoding, 'replace')
                        print('replace')
                        print(content)
                    except Exception as e:
                        try:
                            content = content.encode(encoding, 'ignore')
                            print('ignore')
                            print(content)
                        except Exception as e:
                            print('encode: ', e)
                            print(content)

    return content
