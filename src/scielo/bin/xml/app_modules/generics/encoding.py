# coding=utf-8

import os
import sys
import locale

from . import logger

LOCALE_LANG, LOCALE_ENCODING = locale.getdefaultlocale()
SYS_DEFAULT_ENCODING = sys.getfilesystemencoding()


"""

logging.basicConfig(
    filename='./app.log',
    format=u'%(asctime)s %(message)s')
logger = logging.getLogger('App')
logger.setLevel(logging.DEBUG)
"""

try:
    os.unlink('./app.log')
except:
    pass
app_logger = logger.get_logger('./app.log', 'App')


def is_encodable(content):
    try:
        r = isinstance(content, unicode)
    except:
        r = False
    return r


def decode(content, encoding='utf-8'):
    if content is not None:
        if not is_encodable(content) and hasattr(content, 'decode'):
            try:
                content = content.decode(encoding)
            except Exception as e:
                report_exception('decode()', e, type(content))
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
    if content is not None:
        if is_encodable(content):
            if error_handler in ['xmlcharrefreplace', 'replace', 'ignore']:
                try:
                    content = content.encode(encoding, error_handler)
                except Exception as e:
                    report_exception('encode() 1', e)
            else:
                try:
                    content = content.encode(encoding)
                except Exception as e:
                    try:
                        content = content.encode(encoding, 'xmlcharrefreplace')
                        report_exception(
                            'encode(): xmlcharrefreplace',
                            e,
                            content[content.find('&')-10:content.find('&')+10])
                    except Exception as e:
                        try:
                            content = content.encode(encoding, 'replace')
                            report_exception('encode(): replace', e, content)
                        except Exception as e:
                            try:
                                content = content.encode(encoding, 'ignore')
                                report_exception('encode(): ignore', e, content)
                            except Exception as e:
                                report_exception('encode() n', e, content)

    return content


def report_exception(function_name, e, data):
    try:
        app_logger.exception(
            'Exception at {}'.format(function_name), exc_info=True)
        app_logger.info(data)
    except:
        app_logger.info('EXCEPTION at report_exception()')
        app_logger.info(data)


def debugging(function_name, data):
    try:
        app_logger.info('DEBUG: {}'.format(function_name))
        app_logger.info(data)
    except:
        app_logger.info('EXCEPTION at debugging()')


def display_message(msg):
    try:
        app_logger.info(msg)
    except:
        app_logger.info('EXCEPTION at display_message()')
    try:
        print(decode(encode(msg, SYS_DEFAULT_ENCODING), SYS_DEFAULT_ENCODING))
    except Exception as e:
        print(e)


def fix_args(args):
    return [decode(arg, SYS_DEFAULT_ENCODING) for arg in args]
