# coding=utf-8
import logging
import sys
import locale


logger = logging.getLogger()

LOCALE_LANG, LOCALE_ENCODING = locale.getdefaultlocale()
SYS_DEFAULT_ENCODING = sys.getfilesystemencoding()


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
        logger.debug('DEBUG: {}'.format(function_name))
        logger.debug(data)
    except:
        logger.info('EXCEPTION at debugging()')


def display_message(msg):
    print(msg)


def fix_args(args):
    return [decode(arg.replace('\\', '/'), SYS_DEFAULT_ENCODING) for arg in args]
