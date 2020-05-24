# coding=utf-8
import logging
import logging.config
import sys
import locale
from prodtools.utils.logging import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

LOCALE_LANG, LOCALE_ENCODING = locale.getdefaultlocale()
SYS_DEFAULT_ENCODING = sys.getfilesystemencoding()


"""

logging.basicConfig(
    filename='./app.log',
    format=u'%(asctime)s %(message)s')
logger = logging.getLogger('App')
logger.setLevel(logging.DEBUG)
"""

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
    logger.exception(
            'Exception at {}'.format(function_name))
    try:
        logger.exception(
            'Exception at {}'.format(function_name), exc_info=True)
    except:
        pass
    try:
        logger.info(encode(data))
    except:
        logger.info('EXCEPTION at report_exception()')
        logger.info(e)


def debugging(function_name, data):
    try:
        logger.info('DEBUG: {}'.format(function_name))
        logger.info(data)
    except:
        logger.info('EXCEPTION at debugging()')


def display_message(msg):
    print(msg)


def fix_args(args):
    return [decode(arg.replace('\\', '/'), SYS_DEFAULT_ENCODING) for arg in args]
