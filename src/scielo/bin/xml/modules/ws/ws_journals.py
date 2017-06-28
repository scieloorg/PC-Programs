# code: utf-8

import os

from ..utils import fs_utils


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
JOURNALS_CSV_URL = 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv'


class Journals(object):

    def __init__(self, _ws_requester):
        self.journals_url = JOURNALS_CSV_URL
        self.journals_file_content = ''
        self.ws_requester = _ws_requester

    def update_journals_file(self):
        self.journals_file_content = self.ws_requester.request(self.journals_url)
        fs_utils.update_file_content_if_there_is_new_items(self.journals_file_content, self.downloaded_journals_filename)

    @property
    def downloaded_journals_filename(self):
        downloaded_filename = CURRENT_PATH + '/../../markup/downloaded_markup_journals.csv'
        if not os.path.isdir(CURRENT_PATH + '/../../markup'):
            os.makedirs(CURRENT_PATH + '/../../markup')
        return downloaded_filename
