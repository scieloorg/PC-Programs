# coding=utf-8
import os

from .app.config import app_texts


THIS_LOCATION = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

LOCALE_PATH = THIS_LOCATION + '/../locale'

_ = app_texts.get_texts(LOCALE_PATH)
