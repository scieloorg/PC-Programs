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
    except AttributeError:
        return content
    return content


def encode(content, encoding='utf-8'):
    """
    No python 3, converte string para bytes
    No python 2, converte unicode para string
    """
    try:
        _content = content.encode(encoding)
    except AttributeError:
        return content
    except UnicodeEncodeError:
        _content = content.encode(encoding, 'xmlcharrefreplace')
    return _content


def report_exception(function_name, e, data):
    app_logger.exception(
            'Exception at {}'.format(function_name))
    try:
        app_logger.exception(
            'Exception at {}'.format(function_name), exc_info=True)
    except:
        pass
    try:
        app_logger.info(encode(data))
    except:
        app_logger.info('EXCEPTION at report_exception()')
        app_logger.info(e)


def debugging(function_name, data):
    try:
        app_logger.info('DEBUG: {}'.format(function_name))
        app_logger.info(data)
    except:
        app_logger.info('EXCEPTION at debugging()')


def display_message(msg):
    print(msg)


def fix_args(args):
    return [decode(arg.replace('\\', '/'), SYS_DEFAULT_ENCODING) for arg in args]
