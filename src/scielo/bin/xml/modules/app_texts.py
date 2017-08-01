# coding=utf-8
import locale
import os
import gettext


def get_locale_path(locale_relative_path):
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    return CURRENT_PATH + '/' + locale_relative_path


def get_current_locale(locale_path):
    current_locale, encoding = locale.getdefaultlocale()
    if encoding is None:
        encoding = 'UTF-8'
    if current_locale is None:
        current_locale = 'en_US'
    if current_locale not in os.listdir(locale_path):
        lang, country = current_locale.split('_')
        if lang in os.listdir(locale_path):
            current_locale = lang
    if current_locale not in os.listdir(locale_path):
        current_locale = 'en_US'

    return current_locale


def get_texts(locale_relative_path):
    locale_path = get_locale_path(locale_relative_path)
    current_locale = get_current_locale(locale_path)
    t = gettext.translation('xpm-xc', locale_path, [current_locale])
    try:
        return t.ugettext
    except:
        return t.gettext
