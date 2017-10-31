# coding=utf-8

from ..__init__ import _

from . import xml_utils
from . import utils
from .ws import ws_doi
from .reports import validation_status


class DOIValidator(object):

    def __init__(self, app_ws_requester):
        self.ws_doi = ws_doi.DOIWebServicesRequester(app_ws_requester)

    def validate(self, article):
        self.messages = []
        self.validate_format(article.doi)
        self._validate_doi_prefix(article)
        doi_data = self.ws_doi.doi_data(article.doi)
        if doi_data is None:
            if self.ws_doi.is_working():
                msg = _('{} is not registered for any article. ').format(article.doi)
            else:
                msg = _('{} is not working. ').format(self.ws_doi.URL)
            self.messages.append(('doi', validation_status.STATUS_WARNING, msg))
        else:
            self._validate_journal_title(article, doi_data)
            self._validate_article_title(article, doi_data)
            self._validate_issn(article, doi_data)
        return self.messages

    def validate_format(self, doi):
        errors = []
        if doi is not None:
            for item in doi:
                if item.isdigit():
                    pass
                elif item in '-.-;()/':
                    pass
                elif item in 'abcdefghijklmnopqrstuvwxyz' or item in 'abcdefghijklmnopqrstuvwxyz'.upper():
                    pass
                else:
                    errors.append(item)
        if len(errors) > 0:
            self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} has {q} invalid characteres ({invalid}). Valid characters are: {valid_characters}. ').format(value=doi, valid_characters=_('numbers, letters no diacritics, and -._;()/'), invalid=' '.join(errors), q=str(len(errors)))))

    def _validate_doi_prefix(self, article):
        prefix = article.doi[:article.doi.find('/')]
        valid_prefixes = []
        for issn in [article.e_issn, article.print_issn]:
            if issn is not None:
                doi_prefix = self.ws_doi.journal_prefix(issn, article.pub_date_year)
                if doi_prefix is not None:
                    valid_prefixes.append(doi_prefix)
        if len(valid_prefixes) > 0 and prefix not in valid_prefixes:
            self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} is an invalid value for {label}. ').format(value=prefix, label=_('doi prefix')) + _('{label} must starts with: {expected}. ').format(label='doi', expected=_(' or ').join(valid_prefixes))))

    def _validate_journal_title(self, article, doi_data):
        if doi_data.journal_titles is not None:
            status = validation_status.STATUS_INFO
            if article.journal_title not in doi_data.journal_titles:
                max_rate, items = utils.most_similar(utils.similarity(doi_data.journal_titles, article.journal_title))
                if max_rate < 0.7:
                    status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=article.doi, owner='|'.join(doi_data.journal_titles))))

    def _validate_article_title(self, article, doi_data):
        if doi_data.article_titles is not None:
            status = validation_status.STATUS_INFO
            max_rate = 0
            print('\n'*3)
            print(article.doi)
            print(doi_data.article_titles)
            for t in article.titles:
                print(t.title)
                rate, items = utils.most_similar(utils.similarity(doi_data.article_titles, xml_utils.remove_tags(t.title)))
                if rate > max_rate:
                    max_rate = rate
            if max_rate < 0.7:
                status = validation_status.STATUS_FATAL_ERROR
            print(max_rate)
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=article.doi, owner='|'.join(doi_data.article_titles))))

    def _validate_issn(self, article, doi_data):
        if doi_data.journal_titles is None:
            found = False
            for issn in [article.print_issn, article.e_issn]:
                if issn is not None:
                    if issn.upper() in article.doi.upper():
                        found = True
            if not found:
                self.messages.append(('doi', validation_status.STATUS_ERROR, _('Be sure that {item} belongs to this journal. ').format(item='DOI=' + article.doi)))
