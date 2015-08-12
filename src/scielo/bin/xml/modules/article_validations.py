# coding=utf-8

import os
from datetime import datetime

from __init__ import _
import attributes
import article_utils
import xml_utils
import utils
import article

import institutions_service


def format_value(value):
    if value is None:
        value = 'None'
    return value


def validate_value(value):
    result = []
    status = 'OK'
    if value is not None:
        _value = value.strip()
        if _value == value:
            pass
        elif _value.startswith('<') and _value.endswith('>'):
            pass
        else:
            status = 'ERROR'
            if value.startswith(' '):
                result.append(value + _(' starts with') + _(' "space"'))
            if value.endswith(' '):
                result.append(value + _(' ends with') + _(' "space"'))
            if value.startswith('.'):
                status = 'WARNING'
                result.append(value + _(' starts with') + ' "."')
            differ = value.replace(_value, '')
            if len(differ) > 0:
                result.append('<data>' + value + '</data> ' + _('contains invalid characteres:') + ' "' + differ + '"')
    if status == 'OK':
        message = format_value(value)
    else:
        message = ';\n'.join(result)
    return (status, message)


def display_value(label, value):
    status, message = validate_value(value)
    return (label, status, message)


def conditional_required(label, value):
    status, message = validate_value(value)
    return (label, status, message) if value is not None else (label, 'WARNING', _('Required, if exists.'))


def required_one(label, value):
    return (label, 'OK', display_attributes(value)) if value is not None else (label, 'ERROR', _('Required at least one ') + label + '.')


def required(label, value, default_status, validate_content=True):
    if value is None:
        result = (label, default_status, _('Required'))
    elif value == '':
        result = (label, default_status, _('Required'))
    else:
        if validate_content:
            status, message = validate_value(value)
            result = (label, status, message)
        else:
            result = (label, 'OK', value)
    return result


def expected_values(label, value, expected, fatal=''):
    return (label, 'OK', value) if value in expected else (label, fatal + 'ERROR', format_value(value) + ' - ' + _('Invalid value for ') + label + '. ' + _('Expected values') + ': ' + ', '.join(expected))


def display_attributes(attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        status, message = validate_value(value)
        r.append(key + ' (' + status + '): ' + message)
    return '; '.join(r)


def invalid_terms_in_value(label, value, invalid_terms, error_or_warning):
    r = True
    invalid = ''
    b = value.decode('utf-8') if not isinstance(value, unicode) else value

    for term in invalid_terms:
        a = term.decode('utf-8') if not isinstance(term, unicode) else term

        if term.upper() in value.upper() or term in value or a in b:
            r = False
            invalid = term
            break
    if not r:
        return (label, error_or_warning, _('Invalid character/word') + ' (' + invalid + ') ' + _('in') + ' ' + label + ': ' + value)
    else:
        return (label, 'OK', value)


def validate_name(label, value, invalid_terms):
    r = []
    result = required(label, value, 'ERROR')
    label, status, msg = result
    if status == 'OK':
        result = invalid_terms_in_value(label, value, invalid_terms, 'ERROR')
    r.append(result)
    _test_number = warn_unexpected_numbers(label, value)
    if _test_number is not None:
        r.append(_test_number)
    return r


def warn_unexpected_numbers(label, value, max_number=0):
    r = None
    if value is not None:
        value = xml_utils.htmlent2char(value)
        q_numbers = len([c for c in value if c.isdigit()])
        q_others = len(value) - q_numbers
        if q_numbers > q_others:
            r = (label, 'WARNING', _('Be sure that') + ' <' + label + '>' + value + '</' + label + '> ' + _('is correct') + '.')
    return r


def validate_surname(label, value):
    r = []
    label, status, msg = required(label, value, 'ERROR')
    if status == 'OK':
        msg = value
        suffix_list = [u'Nieto', u'Sobrino', u'Hijo', u'Neto', u'Sobrinho', u'Filho', u'Júnior', u'JÚNIOR', u'Junior', u'Senior', u'Sr', u'Jr']

        parts = value.split(' ')
        if len(parts) > 0:
            rejected = [item for item in parts if item in suffix_list]
            suffix = ' '.join(rejected)

            if len(suffix) > 0:
                msg = _('Invalid terms') + ' (' + suffix + ') ' + _('in') + ' ' + value + '. '
                msg += suffix + ' ' + _('must be identified as') + ' <suffix>' + suffix + '</suffix>.'
                status = 'ERROR'
                r.append((label, status, msg))
    _test_number = warn_unexpected_numbers(label, value)
    if _test_number is not None:
        r.append(_test_number)
    return r


def validate_contrib_names(author, aff_ids=[]):
    results = validate_surname('surname', author.surname) + validate_name('given-names', author.fname, ['_'])
    if len(aff_ids) > 0:
        if len(author.xref) == 0:
            results.append(('xref', 'ERROR', _('Author') + ' "' + author.fname + ' ' + author.surname + '" ' + _('has no') + ' xref' + '. ' + _('Expected values') + ': ' + '|'.join(aff_ids)))
        else:
            for xref in author.xref:
                if not xref in aff_ids:
                    results.append(('xref', 'FATAL ERROR', xref + ' ' + _('of') + ' "' + author.fname + ' ' + author.surname + '" ' + ': ' + _('Invalid value of') + ' xref[@ref-type="aff"]/@rid' + '. ' + _('Valid values: ') + '|'.join(aff_ids)))
    return results


class ArticleContentValidation(object):

    def __init__(self, org_manager, article, validate_order, check_url):
        self.org_manager = org_manager
        self.article = article
        self.validate_order = validate_order
        self.check_url = check_url
        #self.check_url = validate_order

    def normalize_validations(self, validations_result_list):
        r = []
        if isinstance(validations_result_list, list):
            for item in validations_result_list:
                r += self.normalize_validations(item)
        else:
            r.append(validations_result_list)
        return r

    @property
    def validations(self):
        performance = []
        #utils.debugging(datetime.now().isoformat() + ' validations 1')
        items = []
        items.append(self.sps)
        items.append(self.language)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_title)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.publisher_name)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_id)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_id_nlm_ta)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_issns)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.issue_label)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.article_type)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.article_date_types)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.toc_section)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.order)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.doi)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.pagination)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_pages)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_equations)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_tables)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_figures)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_references)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.refstats)

        items.append(self.ref_display_only_stats)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.contrib)
        items.append(self.contrib_names)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.contrib_collabs)
        #utils.debugging(datetime.now().isoformat() + ' validations affiliations')
        items.append(self.affiliations)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.funding)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.license_text)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.license_url)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.license_type)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.history)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.titles_abstracts_keywords)
        items.append(self.validate_xref_reftype)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.missing_xref_list)

        #utils.debugging(datetime.now().isoformat() + ' validations 2')
        r = self.normalize_validations(items)
        #utils.debugging(datetime.now().isoformat() + ' validations 3')
        return (r, performance)

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        return expected_values('@article-type', self.article.article_type, attributes.DOCTOPIC_IN_USE, 'FATAL ')

    @property
    def sps(self):
        label, status, msg = required('article/@specific-use', self.article.sps, 'ERROR')
        if status == 'OK':
            if not 'sps-' in self.article.sps:
                label, status, msg = (label, 'FATAL ERROR', _('Invalid value of') + ' ' + label + ': ' + self.article.sps + '.')
        return (label, status, msg)

    @property
    def language(self):
        label, status, msg = required('@xml:lang', self.article.language, 'FATAL ERROR')
        if status == 'OK':
            if not self.article.language.lower() == self.article.language or len(self.article.language) != 2:
                status = 'FATAL ERROR'
                msg = _('Invalid format for language. It requires two lower case letters.')
        return (label, status, msg)

    @property
    def related_articles(self):
        """
        @id k
        @xlink:href i
        @ext-link-type n
        . t article
        @related-article-type
        @id k
        . t pr
        """
        return article_utils.display_values_with_attributes('related articles', self.article.related_articles)

    @property
    def refstats(self):
        r = []
        non_scholar_types = [k for k in self.article.refstats.keys() if not k in attributes.BIBLIOMETRICS_USE]
        sch1 = sum([t for k, t in self.article.refstats.items() if k in attributes.scholars_level1])
        sch2 = sum([t for k, t in self.article.refstats.items() if k in attributes.scholars_level2])
        total = sum(self.article.refstats.values())
        nonsch = total - sch1 - sch2
        msg = '; '.join([str(k) + ': ' + str(t) for k, t in self.article.refstats.items()])
        status = 'INFO'
        if total > 0:
            if (nonsch >= sch1 + sch2) or (sch1 < sch2):
                status = 'WARNING'
                msg += '. ' + _('Check the value of') + ' element-citation/@publication-type.'
        r.append(('quantity of reference types', status, msg))
        return r

    @property
    def ref_display_only_stats(self):
        r = []
        if self.article.display_only_stats > 0:
            r.append(('element-citation/@specific-use="display-only"', 'WARNING', self.article.display_only_stats))
        return r

    @property
    def journal_title(self):
        return required('journal title', self.article.journal_title, 'FATAL ERROR')

    @property
    def publisher_name(self):
        return required('publisher name', self.article.publisher_name, 'FATAL ERROR')

    @property
    def journal_id(self):
        return required('journal-id', self.article.journal_id, 'FATAL ERROR')

    @property
    def journal_id_nlm_ta(self):
        return conditional_required('journal-id (nlm-ta)', self.article.journal_id_nlm_ta)

    @property
    def journal_issns(self):
        _valid = []
        for k, v in self.article.journal_issns.items():
            valid = False
            if v[4:5] == '-':
                if len(v) == 9:
                    valid = True
            status = 'OK' if valid else 'FATAL ERROR'
            _valid.append((k + ' ISSN', status, v))
        if len(_valid) == 0:
            _valid.append(('ISSN', 'FATAL ERROR', _('Missing ISSN. Required at least one.')))
        return _valid

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section, 'FATAL ERROR')

    @property
    def contrib(self):
        r = []
        if self.article.article_type in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC:
            if len(self.article.contrib_names) == 0 and len(self.article.contrib_collabs) == 0:
                r.append(('contrib', 'FATAL ERROR', self.article.article_type + _(' requires contrib names or collabs.')))
        for item in self.article.article_type_and_contrib_items:
            if item[0] in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC and len(item[1]) == 0:
                r.append(('contrib', 'FATAL ERROR', item[0] + _(' requires contrib names or collabs.')))
        return r

    @property
    def contrib_names(self):
        r = []
        author_xref_items = []
        aff_ids = [aff.id for aff in self.article.affiliations if aff.id is not None]
        for item in self.article.contrib_names:
            for xref in item.xref:
                author_xref_items.append(xref)
            for result in validate_contrib_names(item, aff_ids):
                r.append(result)
        for affid in aff_ids:
            if not affid in author_xref_items:
                r.append(('aff/@id', 'FATAL ERROR', _('Missing') + ' xref[@ref-type="aff"]/@rid="' + affid + '".'))
        return r

    @property
    def contrib_collabs(self):
        return [('collab', 'OK', collab.collab) for collab in self.article.contrib_collabs]

    @property
    def trans_languages(self):
        return article_utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        r = []
        if self.article.is_ahead:
            r.append(required('doi', self.article.doi, 'FATAL ERROR'))
        else:
            r.append(required('doi', self.article.doi, 'WARNING'))

        if self.article.doi is not None:

            journal_titles, article_titles = self.article.doi_journal_and_article

            if not journal_titles is None:
                status = 'INFO'
                if not self.article.journal_title in journal_titles:
                    max_rate, items = utils.most_similar(utils.similarity(journal_titles, self.article.journal_title))
                    if max_rate < 0.7:
                        status = 'FATAL ERROR'
                r.append(('doi', status, self.article.doi + ' ' + _('belongs to') + ' ' + '|'.join(journal_titles)))

            if not article_titles is None:
                status = 'INFO'
                max_rate = 0
                selected = None
                for t in self.article.titles:
                    rate, items = utils.most_similar(utils.similarity(article_titles, t.title))
                    if rate > max_rate:
                        max_rate = rate
                if max_rate < 0.7:
                    status = 'FATAL ERROR'

                r.append(('doi', status, self.article.doi + ' ' + _('is already registered to') + ' ' + '|'.join(article_titles)))

            if journal_titles is None:
                found = False
                for issn in [self.article.print_issn, self.article.e_issn]:
                    if issn is not None:
                        if issn in self.article.doi:
                            found = True
                if not found:
                    r.append(('doi', 'ERROR', _('Be sure that this DOI') + ' "' + self.article.doi + '" ' + _('belongs to this journal.')))
        return r

    @property
    def article_previous_id(self):
        return display_value('article-id[@specific-use="previous-pid"]', self.article.article_previous_id)

    @property
    def order(self):
        def valid(order, status):
            r = ('OK', order)
            if order is None:
                r = (status, _('Missing order. Expected number 1 to 99999.'))
            else:
                if order.isdigit():
                    if int(order) < 1 or int(order) > 99999:
                        r = (status, order + ': ' + _('Invalid format of order. Expected number 1 to 99999.'))
                else:
                    r = (status, order + ': ' + _('Invalid format of order. Expected number 1 to 99999.'))
            return r
        if self.validate_order:
            status = 'FATAL ERROR'
        else:
            status = 'ERROR'
        status, msg = valid(self.article.order, status)
        return ('order', status, msg)

    @property
    def article_id_other(self):
        r = ('article-id[@pub-id-type="other"]', 'OK', self.article.article_id_other)
        if self.article.fpage is not None:
            if self.article.fpage == '00' or not self.article.fpage.isdigit():
                r = ('article-id[@pub-id-type="other"]', 'FATAL ERROR', 'article-id[@pub-id-type="other"] ' + _('is required if there is no fpage > 0 or fpage is not number.'))
        return r

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return ('issue label', 'ERROR', _('Required volume and/or number'))
        else:
            return [self.volume, self.number]

    @property
    def volume(self):
        return display_value('volume', self.article.volume)

    @property
    def number(self):
        return display_value('number', self.article.number)

    @property
    def supplement(self):
        return display_value('supplement', self.article.supplement)

    @property
    def is_issue_press_release(self):
        return display_value('is_issue_press_release', self.article.is_issue_press_release)

    @property
    def funding_source(self):
        return article_utils.display_values('funding_source', self.article.funding_source)

    @property
    def principal_award_recipient(self):
        return article_utils.display_values('principal_award_recipient', self.article.principal_award_recipient)

    @property
    def principal_investigator(self):
        return article_utils.display_values('principal_investigator', self.article.principal_investigator)

    @property
    def funding(self):
        def has_number(content):
            found = False
            r = ''
            if content is None:
                content = ''

            s = content
            if '<' in s:
                content = ''
                s = s.replace('<', 'BREAK<').replace('>', '>BREAK')
                for item in s.split('BREAK'):
                    if '<' in item and '>' in item:
                        pass
                    else:
                        content += item

            if '&#' in content:
                content = content.replace('&#', '_BREAK_AMPNUM').replace(';', '_BREAK_PONT-VIRG')
                s = content.split('_BREAK_')
                content = ''.join([a for a in s if not 'AMPNUM' in a])

            for c in '0123456789':
                if c in content:
                    found = True
                    r = c
                    break
            return (found, r)

        r = []
        if len(self.article.award_id) == 0:
            found, c = has_number(self.article.ack_xml)
            if found is True:
                r.append(('award-id', 'ERROR', _('Found') + ' "' + c + '" ' + _('in') + ' ack. ' + self.article.ack_xml))
            found, c = has_number(self.article.financial_disclosure)
            if found is True:
                r.append(('award-id', 'ERROR', _('Found') + ' "' + c + '" ' + _('in') + ' fn[@fn-type="financial-disclosure"]. ' + self.article.fn_financial_disclosure))
        else:
            for item in self.article.award_id:
                r.append(('award-id', 'OK', item))
        return r

    @property
    def award_id(self):
        return article_utils.display_values('award-id', self.article.award_id)

    @property
    def funding_statement(self):
        return article_utils.display_values('funding statement', self.article.funding_statement)

    @property
    def ack_xml(self):
        return display_value('ack xml', self.article.ack_xml)

    @property
    def pagination(self):
        r = ('fpage', 'OK', self.article.fpage)
        if self.article.fpage is None:
            r = required('elocation-id', self.article.elocation_id, 'ERROR')
        return r

    @property
    def affiliations(self):
        r = []

        labels = []
        labels.append('institution[@content-type="original"]')
        labels.append('institution[@content-type="normalized"]')
        labels.append('institution[@content-type="orgname"]')
        labels.append('institution[@content-type="orgdiv1"]')
        labels.append('institution[@content-type="orgdiv2"]')
        labels.append('institution[@content-type="orgdiv3"]')
        labels.append('addr-line/named-content[@content-type="city"]')
        labels.append('addr-line/named-content[@content-type="state"]')
        labels.append('country')
        labels.append('country/@country')

        for aff in self.article.affiliations:
            text = aff.original if aff.original is not None else aff.xml
            r.append(('aff xml', 'INFO', aff.xml))
            r.append(required('aff/@id', aff.id, 'FATAL ERROR'))

            r.append(required('aff/institution/[@content-type="original"]', aff.original, 'ERROR', False))
            r.append(required('aff/country/@country', aff.i_country, 'FATAL ERROR'))
            if aff.i_country is not None:
                if len(aff.i_country) != 2 or aff.i_country.upper() != aff.i_country:
                    r.append(('aff/country/@country', 'FATAL ERROR', aff.i_country + ': ' + _('Invalid value') + '. ' + _('It must be ISO code of ') + aff.country))

            r.append(required('aff/institution/[@content-type="orgname"]', aff.orgname, 'ERROR'))
            r.append(required('aff/institution/[@content-type="normalized"]', aff.norgname, 'ERROR'))

            if aff.norgname is not None or aff.orgname is not None:
                normalized_items = institutions_service.validate_organization(self.org_manager, aff.orgname, aff.norgname, aff.country, aff.i_country, aff.state, aff.city)
                if len(normalized_items) == 1:
                    orgname, city, state, country_code, country_name = normalized_items[0]
                    if orgname in [aff.orgname, aff.norgname] and country_code in [aff.i_country]:
                        status = 'INFO'
                        r.append(('normalized aff', status, _('Normalized institution name is valid: ') + '; '.join([', '.join(list(item)) for item in normalized_items])))
                    else:
                        status = 'ERROR'
                        r.append(('normalized aff', status, _('Similar normalized institution names: ') + orgname + ', ' + country_code + ' (' + ', '.join([orgname, city, state, country_code, country_name]) + ')'))
                else:
                    msg = _('Unable to confirm/find the normalized institution name for ') + ' or '.join(item for item in [aff.orgname, aff.norgname] if item is not None)
                    if len(normalized_items) == 0:
                        r.append(('normalized aff', 'ERROR', msg + _('. Ask for normalized institution name by email: scielo-xml@googlegroups.com')))
                    else:
                        r.append(('normalized aff', 'ERROR', msg + _('. Similar valid institution names are: ') + '<OPTIONS/>' + '|'.join([', '.join(list(item)) for item in normalized_items])))

            values = [aff.original, aff.norgname, aff.orgname, aff.orgdiv1, aff.orgdiv2, aff.orgdiv3, aff.city, aff.state, aff.i_country, aff.country]
            i = 0
            for label in labels:
                if values[i] is not None:
                    if '|' in values[i]:
                        r.append((label, 'FATAL ERROR', _('only one occurrence of ') + label + _(' is allowed.')))
                i += 1

        return r

    @property
    def clinical_trial_url(self):
        return display_value('clinical trial url', self.article.clinical_trial_url)

    @property
    def clinical_trial_text(self):
        return display_value('clinical trial text', self.article.clinical_trial_text)

    def _total(self, total, count, label_total, label_count):
        if count is None:
            count = 0
        elif count.isdigit():
            count = int(count)

        if total == count:
            r = (label_total, 'OK', str(total))
        else:
            r = (label_count + ' (' + str(count) + ') x ' + label_total + ' (' + str(total) + ')', 'ERROR', _('They must have the same value'))
        return r

    @property
    def total_of_pages(self):
        if self.article.total_of_pages is not None:
            return self._total(self.article.total_of_pages, self.article.page_count, 'total of pages', 'page-count')
        elif self.article.elocation_id:
            return (_('total of pages of ') + self.article.elocation_id, 'WARNING', _('Unable to calculate'))
        else:
            pages = [self.article.fpage, self.article.lpage]
            pages = '-'.join([item for item in pages if item is not None])
            if pages != '':
                return (_('total of pages of ') + pages, 'WARNING', _('Unable to calculate'))

    @property
    def total_of_references(self):
        r = []
        r.append(self._total(self.article.total_of_references, self.article.ref_count, _('total of references'), 'ref-count'))
        if self.article.article_type in attributes.REFS_REQUIRED_FOR_DOCTOPIC:
            if self.article.total_of_references == 0:
                r.append((_('total of references'), 'FATAL ERROR', self.article.article_type + ' ' + _('requires references')))
        return r

    @property
    def total_of_tables(self):
        return self._total(self.article.total_of_tables, self.article.table_count, _('total of tables'), 'table-count')

    @property
    def total_of_equations(self):
        return self._total(self.article.total_of_equations, self.article.equation_count, _('total of equations'), 'equation-count')

    @property
    def total_of_figures(self):
        return self._total(self.article.total_of_figures, self.article.fig_count, _('total of figures'), 'fig-count')

    @property
    def titles_abstracts_keywords(self):
        r = []

        for lang in self.article.title_abstract_kwd_languages:
            err_level = 'ERROR' if lang != self.article.language else 'FATAL ERROR'
            found = []
            not_found = []
            t = self.article.titles_by_lang.get(lang)
            if t is None:
                not_found.append(('title-group (@xml:lang=' + lang + ')', err_level, _('not found')))
            else:
                text = None if t.title == '' else t.title
                if text is None:
                    not_found.append(('article title (@xml:lang=' + lang + ')', err_level, _('not found')))
                else:
                    found.append(('title-group (@xml:lang=' + lang + ')', 'INFO', text))
                    if lang is None:
                        not_found.append(('@xml:lang of title-group', err_level, _('Invalid value') + ': None' + ':' + text))

            if self.article.article_type in attributes.ABSTRACT_REQUIRED_FOR_DOCTOPIC:
                t = self.article.abstracts_by_lang.get(lang)
                if t is None:
                    not_found.append(('abstract (@xml:lang=' + lang + ')', err_level, _('not found')))
                else:
                    text = None if t.text == '' else t.text
                    if text is None:
                        not_found.append(('abstract (@xml:lang=' + lang + ')', err_level, _('not found')))
                    else:
                        found.append(('abstract (@xml:lang=' + lang + ')', 'INFO', text))
                        if lang is None:
                            not_found.append(('@xml:lang of abstract', err_level, _('Invalid value') + ': None') + ': ' + text)

                t = self.article.keywords_by_lang.get(lang)
                if t is None:
                    not_found.append(('kwd-group (@xml:lang=' + lang + ')', err_level, _('not found')))
                elif len(t) == 1:
                    not_found.append(('kwd (@xml:lang=' + lang + ')', err_level, _('Required at least more than one kwd')))
                else:
                    if len(t) == 0:
                        not_found.append(('kwd (@xml:lang=' + lang + ')', err_level, _('not found')))
                    else:
                        found.append(('kwd-group (@xml:lang=' + lang + ')', 'INFO', '; '.join([item.text for item in t])))
                        if lang is None:
                            not_found.append(('@xml:lang of kwd-group', err_level, _('Invalid value') + ': None') + ': ' + '; '.join([item.text for item in t]))
            else:
                a = self.article.abstracts_by_lang.get(lang)
                b = self.article.keywords_by_lang.get(lang)
                a = 0 if a is None else 1
                b = 0 if b is None else 1
                if a + b > 0:
                    article_type = '@article-type=' + self.article.article_type
                    not_found.append(('abstract/kwd-group', 'WARNING', _('Unexpected {unexpected} for {demander}. Be sure that {demander} is correct.').format(unexpected='abstract/kwd-group', demander=article_type)))
            if len(not_found) > 0:
                if len(found) > 0:
                    for item in found:
                        r.append(item)
                for item in not_found:
                    r.append(item)
        return r

    @property
    def titles(self):
        r = []
        for item in self.article.titles:
            if item.title is not None and item.language is not None:
                r.append(('title', 'OK', item.language + ': ' + item.title))
            else:
                if item.language is None:
                    r.append(('title language', 'ERROR', _('Missing {required} for {demander}').format(required='@xml:lang', demander=item.title)))
                elif item.title is None:
                    r.append(('title', 'ERROR', _('Missing {required} for {demander}').format(required='title', demander=item.language)))
                else:
                    r.append('title', 'ERROR', _('Missing titles'))
        return r

    @property
    def abstracts(self):
        r = []
        for item in self.article.abstracts:
            if item.language is not None and item.text is not None:
                r.append(('abstract: ', 'OK', item.language + ':' + item.text))
            else:
                if item.language is None:
                    r.append(('abstract: ', 'ERROR', _('Missing @xml:lang for ') + item.text))
                if item.text is None:
                    r.append(('abstract: ', 'ERROR', _('Missing text for ') + item.language))
        return r

    @property
    def keywords(self):
        r = []
        for item in self.article.keywords:
            r.append(('kwd: ' + item['l'], 'OK', item['k']))
        return r

    @property
    def history(self):
        received = self.article.received_dateiso
        accepted = self.article.accepted_dateiso
        r = []
        if received is not None and accepted is not None:
            if not received < accepted:
                r = 'received (' + received + '); accepted (' + accepted + '); pub-date (' + self.article.pub_date_year + ').'
                r = [('history', 'ERROR', r)]
        elif received is None and accepted is None:
            r = [('history', 'INFO', 'there is no history dates')]
        else:
            if received is None:
                r.append(required('history: received', received, 'ERROR'))
            if accepted is None:
                r.append(required('history: accepted', accepted, 'ERROR'))

        return r

    @property
    def received(self):
        return display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return display_attributes('accepted', self.article.accepted)

    @property
    def license_text(self):
        return required('license-p', self.article.license_text, 'FATAL ERROR', False)

    @property
    def license_url(self):
        return required('license/@href', self.article.license_url, 'FATAL ERROR', False)

    @property
    def license_type(self):
        return expected_values('@license-type', self.article.license_type, ['open-access'], 'FATAL ')

    @property
    def references(self):
        r = []
        year = self.article.received.get('year') if self.article.received is not None else None
        if year is None:
            year = self.article.accepted.get('year') if self.article.accepted is not None else None
        if year is None:
            year = self.article.pub_date_year
        if year is None:
            year = datetime.now().isoformat()[0:4]
        for ref in self.article.references:
            r.append((ref, ReferenceContentValidation(ref).evaluate(year)))
        return r

    @property
    def press_release_id(self):
        return display_value(_('press release id'), self.article.press_release_id)

    @property
    def article_date_types(self):
        r = []
        date_types = []
        expected = ['epub-ppub', 'epub' + _(' and ') + 'collection', 'epub']
        if self.article.epub_date is not None:
            date_types.append('epub')
        if self.article.collection_date is not None:
            date_types.append('collection')
        if self.article.epub_ppub_date is not None:
            date_types.append('epub-ppub')
        c = _(' and ').join(date_types)
        if c in expected:
            r.append(('article dates', 'OK', c))
        else:
            r.append(('article dates', 'ERROR', _('Invalid combination of date types: ') + c + '. ' + _('Expected values') + ': ' + ' | '.join(expected)))
        return r

    @property
    def issue_pub_date(self):
        return required_one(_('issue pub-date'), self.article.issue_pub_date)

    @property
    def article_pub_date(self):
        return display_attributes(_('article pub-date'), self.article.article_pub_date)

    @property
    def is_ahead(self):
        return display_value(_('is aop'), self.article.is_ahead)

    @property
    def ahpdate(self):
        return display_value(_('aop'), self.article.ahpdate)

    @property
    def is_article_press_release(self):
        return display_value(_('is press_release'), self.article.is_article_press_release)

    @property
    def illustrative_materials(self):
        return article_utils.display_values(_('illustrative materials'), self.article.illustrative_materials)

    @property
    def is_text(self):
        return display_value(_('is text'), self.article.is_text)

    @property
    def previous_pid(self):
        return display_value(_('previous pid'), self.article.previous_pid)

    @property
    def validate_xref_reftype(self):
        message = []
        reftypes_and_tag = {'aff': 'aff', 'app': 'app', 'author-notes': 'fn', 'bibr': 'ref', 'boxed-text': 'boxed-text', 'contrib': 'fn', 'corresp': 'corresp', 'disp-formula': 'disp-formula', 'fig': 'fig', 'fn': 'fn', 'list': 'list', 'other': '?', 'supplementary-material': 'supplementary-material', 'table': 'table-wrap'}

        id_and_elem_name = {node.attrib.get('id'): node.tag for node in self.article.elements_which_has_id_attribute if node.attrib.get('id') is not None}

        for xref in self.article.xref_nodes:
            if xref['rid'] is None:
                message.append(('xref/@rid', 'FATAL ERROR', _('Missing') + ' @rid in ' + xref['xml']))
            if xref['ref-type'] is None:
                message.append(('xref/@ref-type', 'ERROR', _('Missing') + ' @ref-type in ' + xref['xml']))
            if xref['rid'] is not None and xref['ref-type'] is not None:
                tag = id_and_elem_name.get(xref['rid'])
                if tag is None:
                    message.append(('xref/@rid', 'FATAL ERROR', _('Missing') + ' element[@id=' + xref['rid'] + _(' and ') + '@ref-type=' + xref['ref-type'] + ']'))
                elif reftypes_and_tag.get(xref['ref-type']) is None:
                    # no need to validate
                    valid = True
                elif tag == reftypes_and_tag.get(xref['ref-type']):
                    valid = True
                elif tag != reftypes_and_tag.get(xref['ref-type']):
                    reftypes = [reftype for reftype, _tag in reftypes_and_tag.items() if _tag == tag]
                    _msg = _('Unmatched')
                    _msg += ' @ref-type (' + xref['ref-type'] + ')'
                    _msg += _(' and ') + tag + ': '
                    _msg += 'xref[@ref-type="' + xref['ref-type'] + '"] '
                    _msg += _('is for') + ' ' + reftypes_and_tag.get(xref['ref-type'])
                    _msg += _(' and ') + _('valid values of') + ' @ref-type ' + _('of') + ' '
                    _msg += tag + ' ' + _('are') + ' '
                    _msg += '|'.join(reftypes)

                    #_msg = _('Unmatched @ref-type (%s), and %s: xref[@ref-type="%s"] is for %s and valid values of  @ref-type of %s are %s') % (xref['ref-type'], tag, xref['ref-type'], reftypes_and_tag.get(xref['ref-type']), tag, '|'.join(reftypes))

                    message.append(('xref/@rid', 'FATAL ERROR', _msg))
        return message

    @property
    def missing_xref_list(self):
        alert_tags = ['fig', 'table-wrap', 'ref', ]
        rid_list = [node['rid'] for node in self.article.xref_nodes]
        message = []
        missing = {}
        for node in self.article.elements_which_has_id_attribute:
            _id = node.attrib.get('id')
            if _id is None:
                message.append((node.tag, 'ERROR', _('Missing') + ' @id'))
            else:
                if not _id in rid_list:
                    if node.tag in alert_tags:
                        if not node.tag in missing.keys():
                            missing[node.tag] = []
                        missing[node.tag].append(_id)

        for tag, not_found in missing.items():
            msg = ', '.join(['xref[@rid="' + _id + '"]' for _id in sorted(not_found)])
            message.append((tag, 'ERROR', _('Missing') + ': ' + msg))

        return message

    def href_list(self, path):
        href_items = {'ok': [], 'warning': [], 'error': [], 'fatal error': []}
        for hrefitem in self.article.hrefs:
            if hrefitem.is_internal_file:
                file_location = hrefitem.file_location(path)
                if os.path.isfile(file_location):
                    if not '.' in hrefitem.src:
                        href_items['warning'].append(hrefitem)
                    else:
                        href_items['ok'].append(hrefitem)
                else:
                    href_items['fatal error'].append(hrefitem)
            else:
                if self.check_url:
                    if article_utils.url_check(hrefitem.src, 1):
                        href_items['ok'].append(hrefitem)
                    else:
                        href_items['warning'].append(hrefitem)
                #else:
                #    href_items['ok'].append(hrefitem)
        return href_items


class ReferenceContentValidation(object):

    def __init__(self, reference):
        self.reference = reference

    def evaluate(self, article_year):
        r = []
        r.append(self.xml)
        r.append(self.mixed_citation)
        r.append(self.publication_type)

        for item in self.publication_type_dependence:
            r.append(item)
        for item in self.authors_list:
            r.append(item)
        for item in self.year(article_year):
            r.append(item)
        for item in self.source:
            r.append(item)
        return r

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        r = []
        if self.reference.source is not None:
            _test_number = warn_unexpected_numbers('source', self.reference.source, 4)
            if _test_number is not None:
                r.append(_test_number)
            if self.reference.source is not None:
                if self.reference.source[0:1] != self.reference.source[0:1].upper():
                    r.append(('source', 'ERROR', self.reference.source + '-' + _('Invalid value for ') + 'source' + '. '))
        return r

    def validate_element(self, label, value, error_level='FATAL ERROR'):
        if not self.reference.publication_type is None:
            res = attributes.validate_element(self.reference.publication_type, label, value)
            if res != '':
                return (label, error_level, res)
            else:
                if not value is None and value != '':
                    return (label, 'OK', value)

    @property
    def publication_type_dependence(self):
        r = []
        if not self.reference.publication_type is None:
            authors = None
            if len(self.reference.authors_list) > 0:
                for item in self.reference.authors_list:
                    if isinstance(item, article.PersonAuthor):
                        authors = item.surname + ' ...'
                    elif isinstance(item, article.CorpAuthor):
                        authors = item.collab

            items = [
                    self.validate_element('person-group', authors), 
                    self.validate_element('article-title', self.reference.article_title), 
                    self.validate_element('chapter-title', self.reference.chapter_title), 
                    self.validate_element('publisher-name', self.reference.publisher_name), 
                    self.validate_element('publisher-loc', self.reference.publisher_loc), 
                    self.validate_element('comment[@content-type="degree"]', self.reference.degree), 
                    self.validate_element('conf-name', self.reference.conference_name), 
                    self.validate_element('date-in-citation[@content-type="access-date"] ' + _('or') + ' date-in-citation[@content-type="update"]', self.reference.cited_date), 
                    self.validate_element('ext-link', self.reference.ext_link), 
                    self.validate_element('volume', self.reference.volume), 
                    self.validate_element('issue', self.reference.issue), 
                    self.validate_element('fpage', self.reference.fpage), 
                    self.validate_element('source', self.reference.source), 
                    self.validate_element('year', self.reference.year), 
                ]

            looks_like = None
            _mixed = self.reference.mixed_citation.lower() if self.reference.mixed_citation is not None else ''
            _source = self.reference.source.lower() if self.reference.source is not None else ''
            if self.reference.publication_type != 'journal':
                if self.reference.source is not None:
                    if 'journal' in _source or 'revista' in _source or 'J ' in self.reference.source or self.reference.source.endswith('J') or 'J. ' in self.reference.source or self.reference.source.endswith('J.'):
                        looks_like = 'journal'
            if self.reference.issue is None and self.reference.volume is None:
                if self.reference.fpage is None:
                    if 'thesis' in _mixed or 'dissert' in _mixed or 'master' in _mixed or 'doctor' in _mixed or 'mestrado' in _mixed or 'doutorado' in _mixed or 'maestr' in _mixed or 'tese' in _mixed:
                        if self.reference.publication_type != 'thesis':
                            looks_like = 'thesis'
                if not 'legal' in self.reference.publication_type:
                    if self.reference.source is not None:
                        if 'Lei' in self.reference.source or ('Di' in self.reference.source and 'Oficial' in self.reference.source):
                            looks_like = 'legal-doc'
                        if 'portaria' in _source:
                            looks_like = 'legal-doc'
                if 'conference' in _mixed or 'proceeding' in _mixed or 'meeting' in _mixed:
                    if self.reference.publication_type != 'confproc':
                        looks_like = 'confproc'
            if looks_like is not None:
                r.append(('@publication-type', 'ERROR', _('Check if @publication-type is correct. This reference looks like') + ' ' + looks_like))

            for item in items:
                if item is not None:
                    r.append(item)
        return r

    @property
    def ignore_publication_type_dependence(self):
        r = []
        authors = None
        if len(self.reference.authors_list) > 0:
            for item in self.reference.authors_list:
                if isinstance(item, article.PersonAuthor):
                    authors = item.surname + ' ...'
                elif isinstance(item, article.CorpAuthor):
                    authors = item.collab

        items = [
                self.validate_element('person-group', authors), 
                self.validate_element('article-title', self.reference.article_title), 
                self.validate_element('chapter-title', self.reference.chapter_title), 
                self.validate_element('publisher-name', self.reference.publisher_name), 
                self.validate_element('publisher-loc', self.reference.publisher_loc), 
                self.validate_element('comment[@content-type="degree"]', self.reference.degree), 
                self.validate_element('conf-name', self.reference.conference_name), 
                self.validate_element('date-in-citation[@content-type="access-date"] ' + _('or') + ' date-in-citation[@content-type="update"]', self.reference.cited_date), 
                self.validate_element('ext-link', self.reference.ext_link), 
                self.validate_element('volume', self.reference.volume), 
                self.validate_element('issue', self.reference.issue), 
                self.validate_element('fpage', self.reference.fpage), 
                self.validate_element('source', self.reference.source), 
                self.validate_element('year', self.reference.year), 
            ]

        if self.reference.issue is None and self.reference.volume is None:
            _mixed = self.reference.mixed_citation.lower()
            if 'conference' in _mixed or 'proceeding' in _mixed:
                if self.reference.publication_type != 'confproc':
                    r.append(('@publication-type', 'WARNING', _('Check if @publication-type is correct. This reference looks like') + ' confproc.'))
            if ' dissert' in _mixed or 'master' in _mixed or 'doctor' in _mixed or 'mestrado' in _mixed or 'doutorado' in _mixed or 'maestr' in _mixed:
                if self.reference.publication_type != 'thesis':
                    r.append(('@publication-type', 'WARNING', _('Check if @publication-type is correct. This reference looks like') + ' thesis.'))

        for item in items:
            if item is not None:
                r.append(item)

        any_error_level = list(set([status for label, status, message in r if status in ['FATAL ERROR']]))
        if len(any_error_level) == 0:
            if self.reference.ref_status == 'display-only':
                minimum_required_elements = attributes.REFERENCE_REQUIRED_SUBELEMENTS.get(self.reference.publication_type)
                if minimum_required_elements is None:
                    r.append(('@specific-use', 'ERROR', _('Remove @specific-use="display-only". It is required to identify incomplete references which @publication-type is equal to ') + ' | '.join(attributes.REFERENCE_REQUIRED_SUBELEMENTS.keys())))
                else:
                    r.append(('@specific-use', 'FATAL ERROR', _('Remove @specific-use="display-only". It is required to identify incomplete references which @publication-type is equal to ') + ' | '.join(attributes.REFERENCE_REQUIRED_SUBELEMENTS.keys()) + '. ' + _('Expected at least the elements: ') + ' | '.join(minimum_required_elements)))

        else:
            if self.reference.ref_status == 'display-only':
                items.append((_('Incomplete Reference'), 'WARNING', _('Check if the elements of this reference is properly identified.')))
                items = []
                for label, status, message in r:
                    if status != 'OK':
                        items.append((label, 'WARNING' + _(' ignored ') + status.lower(), message))
                r = items
        return r

    @property
    def ext_link(self):
        r = None
        if self.reference.ext_link is not None:
            if not self.reference.ext_link.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').strip() in self.reference.mixed_citation:
                r = ('ext-link', 'ERROR', '"' + self.reference.ext_link + '" ' + _('is missing in') + ' "' + self.reference.mixed_citation + '"')
        return r

    @property
    def publication_type(self):
        return expected_values('@publication-type', self.reference.publication_type, attributes.PUBLICATION_TYPE, 'FATAL ')

    @property
    def xml(self):
        return ('xml', 'OK', self.reference.xml)

    @property
    def mixed_citation(self):
        return required('mixed-citation', self.reference.mixed_citation, 'FATAL ERROR', False)

    @property
    def authors_list(self):
        r = []
        for person in self.reference.authors_list:
            if isinstance(person, article.PersonAuthor):
                for item in validate_contrib_names(person):
                    r.append(item)
            elif isinstance(person, article.CorpAuthor):
                r.append(('collab', 'OK', person.collab))
            else:
                r.append((_('invalid author'), 'WARNING', str(type(person))))
        return r

    def year(self, article_year):
        r = []
        if article_year is None:
            article_year = datetime.now().isoformat()[0:4]
        _y = self.reference.formatted_year
        if _y is not None:
            if _y.isdigit():
                if int(_y) > article_year:
                    r.append(('year', 'FATAL ERROR', _y + _(' must not be greater than ') + datetime.now().isoformat()[0:4]))
            elif 's.d' in _y:
                r.append(('year', 'INFO', _y))
            elif 's/d' in _y:
                r.append(('year', 'INFO', _y))
            else:
                r.append(('year', 'FATAL ERROR', _y + _(' is not a number nor in an expected format.')))
        return r

    @property
    def publisher_name(self):
        return display_value('publisher-name', self.reference.publisher_name)

    @property
    def publisher_loc(self):
        return display_value('publisher-loc', self.reference.publisher_loc)

    @property
    def fpage(self):
        return conditional_required('fpage', self.reference.fpage)
