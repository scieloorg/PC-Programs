# coding=utf-8

from prodtools import _

from prodtools.utils import xml_utils
from prodtools.utils import utils
from prodtools.utils.ws import ws_doi
from prodtools.reports import validation_status


LETTERS = 'abcdefghijklmnopqrstuvwxyz'


class DOIValidator(object):

    def __init__(self, app_ws_requester):
        self.ws_doi = ws_doi.DOIWebServicesRequester(app_ws_requester)
        self.is_working = self.ws_doi.is_working()

    def validate(self, article):
        self.messages = []
        journal_issns = [issn.lower()
                         for issn in [article.print_issn, article.e_issn]
                         if issn is not None]
        year = (
            article.real_pubdate or article.expected_pubdate or {}).get('year')
        journal_prefixes = self.journal_prefixes(journal_issns, year)
        for lang, doi in article.doi_and_lang:
            if not doi:
                continue
            self.validate_issn_in_doi(journal_issns, doi)
            self.validate_doi_prefix(journal_prefixes, journal_issns,
                                     article.journal_title, doi)
            if self.validate_format(doi):
                msg = ''
                if self.is_working:
                    doi_data = self.ws_doi.doi_data(doi)
                    if doi_data is None:
                        msg = _(
                            '{} is not registered for any article. ').format(
                                doi)
                    else:
                        self.validate_journal_title(
                            article.journal_title, doi, doi_data)
                        self.validate_article_title(
                            article.titles, doi, doi_data)
                else:
                    msg = _('{} is not working. ').format(self.ws_doi.URL)
                if msg:
                    self.messages.append(
                        ('doi', validation_status.STATUS_WARNING, msg))
        return self.messages

    def validate_format(self, doi):
        errors = []
        if doi is not None:
            for item in doi:
                if item.isdigit():
                    pass
                elif item in '-._;()/':
                    pass
                elif item in LETTERS or item in LETTERS.upper():
                    pass
                else:
                    errors.append(item)
        if len(errors) > 0:
            self.messages.append(
                ('doi', validation_status.STATUS_FATAL_ERROR,
                    _('{value} has {q} invalid characteres ({invalid}). Valid characters are: {valid_characters}. ').format(value=doi, valid_characters=_('numbers, letters no diacritics, and -._;()/'), invalid=' '.join(errors), q=str(len(errors)))))
        return len(errors) == 0

    def journal_prefixes(self, journal_issns, pub_date_year):
        valid_prefixes = []
        for issn in journal_issns:
            registered_prefix = self.ws_doi.journal_prefix(issn, pub_date_year)
            if registered_prefix is not None:
                valid_prefixes.append(registered_prefix)
        return set(valid_prefixes)

    def validate_doi_prefix(self, journal_prefixes, journal_issns,
                            journal_title,
                            article_doi):
        prefix = article_doi[:article_doi.find('/')]
        if len(journal_prefixes) > 0 and \
                prefix not in journal_prefixes:
            self.messages.append(
                ('doi',
                 validation_status.STATUS_FATAL_ERROR,
                 _('{value} is an invalid value for {label}. ').format(
                        value=prefix,
                        label=_('doi prefix')
                        ) +
                 _('{label} must starts with: {expected}. ').format(
                        label='doi',
                        expected=_(' or ').join(journal_prefixes)))
            )
        elif len(journal_prefixes) == 0:
            publisher_by_issn = self.ws_doi.journal_publisher_by_issn(
                                    journal_issns) or ''
            publisher_by_prefix = self.ws_doi.journal_publisher_by_doi_prefix(
                                    prefix) or ''
            _publisher_by_issn = publisher_by_issn.lower()
            _publisher_by_prefix = publisher_by_prefix.lower()
            if (_publisher_by_issn not in _publisher_by_prefix and
                    _publisher_by_prefix not in _publisher_by_issn):
                msgs = [
                    article_doi,
                    _('{value} is an invalid value for {label}. ').format(
                            value=prefix,
                            label=_('doi prefix')),
                    _('"{}" belongs to {}. ').format(
                        prefix, publisher_by_prefix),
                    _('DOI Publisher for {}: {}. ').format(
                        journal_title, publisher_by_issn)
                ]
                self.messages.append(
                    ('doi',
                     validation_status.STATUS_FATAL_ERROR,
                     msgs))

    def validate_journal_title(self, article_journal_title, article_doi,
                               doi_data):
        if doi_data.journal_titles is not None:
            status = validation_status.STATUS_ERROR
            if article_journal_title not in doi_data.journal_titles:
                max_rate, items = utils.most_similar(
                    utils.similarity(
                        doi_data.journal_titles, article_journal_title))
                if max_rate < 0.7:
                    status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(
                ('doi', status,
                    _('{item} is registered as belonging to {owner}. ').format(
                        item=article_doi,
                        owner='|'.join(list(doi_data.journal_titles)))))

    def validate_article_title(self, article_titles, article_doi, doi_data):
        if doi_data.article_titles is not None:
            status = validation_status.STATUS_ERROR
            max_rate = 0
            for t in article_titles:
                rate, items = utils.most_similar(
                    utils.similarity(
                        doi_data.article_titles,
                        xml_utils.remove_tags(t.title)))
                if rate > max_rate:
                    max_rate = rate
            if max_rate < 0.7:
                status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(
                ('doi', status,
                    _('{item} is registered as belonging to {owner}. ').format(
                        item=article_doi,
                        owner='|'.join(doi_data.article_titles))))

    def validate_issn_in_doi(self, article_issns, doi):
        issn_in_doi = [issn for issn in article_issns if issn in doi]
        if not issn_in_doi:
            self.messages.append(
                ('doi', validation_status.STATUS_WARNING,
                 _('Unable to check if {} belongs'
                   ' to this journal. ').format(doi)))
