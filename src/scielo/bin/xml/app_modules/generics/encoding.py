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


def decode(content, encoding='utf-8'):
    try:
        content = content.decode(encoding)
    except UnicodeDecodeError as e:
        report_exception('decode()', e, type(content))
    except AttributeError as e:
        return content
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
    errors = ('xmlcharrefreplace', 'replace', 'ignore')
    if hasattr(content, "encode"):
        _content = content
        if error_handler in errors:
            try:
                _content = content.encode(encoding, error_handler)
            except UnicodeEncodeError as e:
                report_exception('encode()', e, error_handler)
        else:
            try:
                _content = content.encode(encoding)
            except UnicodeEncodeError as e:
                for error in errors:
                    try:
                        _content = content.encode(encoding, error)
                    except UnicodeEncodeError:
                        continue
                    else:
                        debugging("encode", _content)
                        debugging("encode", error)
                        break
        return _content
    return content


def report_exception(function_name, e, data=None):
    app_logger.debug("Exception at %s" % function_name)
    app_logger.exception(e, exc_info=True)
    if data:
        app_logger.debug(data)


def debugging(function_name, data):
    app_logger.debug(function_name)
    try:
        app_logger.debug(data)
    except TypeError:
        app_logger.debug('Unable to log data')
    except ValueError:
        app_logger.debug('Unable to log data')


def display_message(msg):
    try:
        print(decode(encode(msg, SYS_DEFAULT_ENCODING), SYS_DEFAULT_ENCODING))
    except UnicodeError as e:
        print(e)


def fix_args(args):
    return [decode(arg.replace('\\', '/'), SYS_DEFAULT_ENCODING) for arg in args]
