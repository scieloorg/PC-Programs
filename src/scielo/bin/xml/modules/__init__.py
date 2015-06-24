# coding=utf-8
import locale
import os
import gettext

locale_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/../locale'

current_locale, encoding = locale.getdefaultlocale()

if not current_locale in os.listdir(locale_path):
    lang, country = current_locale.split('_')
    encoding = 'UTF-8'
    for name in os.listdir(locale_path):
        if name.startswith(lang):
            current_locale = name

if not current_locale in os.listdir(locale_path):
    current_locale = 'en_US'
    encoding = 'UTF-8'

t = gettext.translation('xpm-xc', locale_path, [current_locale])
_ = t.ugettext
