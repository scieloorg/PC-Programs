# code: utf-8

import os

from ...generics import fs_utils
from ...__init__ import BIN_MARKUP_PATH


JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


class Journals(object):

    def __init__(self, _ws_requester):
        self.journals_url = JOURNALS_CSV_URL
        self.ws_requester = _ws_requester

    def update_journals_file(self):
        data = self.ws_requester.request(self.journals_url)
        if data:
            fs_utils.write_file(self.downloaded_journals_filename, data)

    @property
    def downloaded_journals_filename(self):
        downloaded_filename = BIN_MARKUP_PATH + '/downloaded_markup_journals.csv'
        if not os.path.isdir(BIN_MARKUP_PATH):
            os.makedirs(BIN_MARKUP_PATH)
        return downloaded_filename
