# coding=utf-8

from isis_models import DOCTOPIC

import attributes as attributes
import utils as utils

import article


def format_xml_in_html(xml):
    return '<pre>' + xml.replace('<', '&lt;').replace('>', '&gt;') + '</pre>'


def format_value(value):
    return 'None' if value is None else value


def display_value(label, value):
    return (label, 'OK', format_value(value))


def conditional_required(label, value):
    return (label, 'OK', format_value(value)) if value is not None else (label, 'WARNING', 'Required, if exists.')


def required_one(label, value):
    return (label, 'OK', display_attributes(value)) if value is not None else (label, 'ERROR', 'Required at least one ' + label + '.')


def required(label, value):
    return (label, 'OK', format_value(value)) if not (value is None or value == '') else (label, 'ERROR', 'Required.')


def expected_values(label, value, expected):
    return (label, 'OK', format_value(value)) if value in expected else (label, 'ERROR', format_value(value) + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected))


def display_attributes(attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        r.append(key + ': ' + format_value(value))
    return '; '.join(r)


def invalid_characters_in_value(label, value, invalid_characters, error_or_warning):
    r = True
    for c in value:
        if c in invalid_characters:
            r = False
            break
    if not r:
        return (label, error_or_warning, 'Invalid characteres (' + ';'.join(invalid_characters) + ') in ' + label + ': ' + value)
    else:
        return (label, 'OK', value)


def validate_contrib_names(author):
    r = []
    result = required('surname', author.surname)
    if result[1] == 'OK':
        result = invalid_characters_in_value('surname', author.surname, [' '], 'WARNING')
    r.append(result)
    r.append(required('given-names', author.fname))
    return r


class ArticleContentValidation(object):

    def __init__(self, article):
        self.article = article

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        return expected_values('@article-type', self.article.article_type, DOCTOPIC.keys())

    @property
    def language(self):
        return expected_values('@xml:lang', self.article.language, ['en', 'es', 'pt', 'de', 'fr'])

    @property
    def related_objects(self):
        """
        @id k
        @document-id i
        @document-id-type n
        @document-type t
        @object-id i
        @object-id-type n
        @object-type t
        @source-id i
        @source-id-type n
        @source-type t
        @link-type r
        """
        return utils.display_values_with_attributes('related objects', self.article.related_objects)

    @property
    def related_articles(self):
        """
        @id k
        @xlink:href i
        @ext-link-type n
        . t article
        .//article-meta/related-article[@related-article-type='press-release' and @specific-use='processing-only'] 241
        @id k
        . t pr
        """
        return utils.display_values_with_attributes('related articles', self.article.related_objects)

    @property
    def journal_title(self):
        return required('journal title', self.article.journal_title)

    @property
    def publisher_name(self):
        return required('publisher name', self.article.publisher_name)

    @property
    def journal_id(self):
        return required('journal-id', self.article.journal_id)

    @property
    def journal_id_nlm_ta(self):
        return conditional_required('journal-id (nlm-ta)', self.article.journal_id_nlm_ta)

    @property
    def journal_issns(self):
        return required_one('ISSN', self.article.journal_issns)

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section)

    @property
    def keywords(self):
        r = []
        for item in self.article.keywords:
            r.append(('keyword: ' + item['l'], 'OK', item['k']))
        return r

    @property
    def contrib_names(self):
        r = []
        for item in self.article.contrib_names:
            for result in validate_contrib_names(item):
                r.append(result)
        return r

    @property
    def contrib_collabs(self):
        return [('collab', 'OK', collab) for collab in self.article.contrib_collabs]

    @property
    def titles(self):
        r = []
        for item in self.article.title:
            r.append(('title', 'OK', item.language + ': ' + item.title))
        return r

    @property
    def trans_titles(self):
        r = []
        for item in self.article.trans_titles:
            if item.language is None:
                item.language = 'None'
            if item.title is None:
                item.title = 'None'
            r.append(('title', 'OK', item.language + ': ' + item.title))
        return r

    @property
    def trans_languages(self):
        return utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        return required('doi', self.article.doi)

    @property
    def article_id_publisher_id(self):
        return display_value('article id (previous pid)', self.article.article_id_publisher_id)

    @property
    def order(self):
        def valid(order):
            r = ('?', order)     
            if order is not None:
                if order.isdigit():
                    if len(order) != 5:
                        r = ('ERROR', 'Invalid format of order. Expected 99999.')
                else:
                    r = ('ERROR', 'Invalid format of order. Expected 99999.')
            return r
        r = valid(self.article.order)
        if r[0] == '?':
            r = required('order', self.article.order)
        elif r[0] == 'ERROR':
            r = ('order', 'ERROR', r[1])
        else:
            r = ('order', 'OK', self.article.order)
        return r

    @property
    def article_id_other(self):
        return display_value('article-id (other)', self.article.article_id_other)

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return 'ERROR: Required one of volume and/or number'
        else:
            return self.volume + self.number

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
        return utils.display_values('funding_source', self.article.funding_source)

    @property
    def principal_award_recipient(self):
        return utils.display_values('principal_award_recipient', self.article.principal_award_recipient)

    @property
    def principal_investigator(self):
        return utils.display_values('principal_investigator', self.article.principal_investigator)

    @property
    def funding(self):
        def has_number(content):
            found = False
            if content is None:
                content = ''
            for c in '0123456789':
                if c in content:
                    found = True
                    break
            return found

        r = []
        if len(self.article.award_id) == 0:
            if has_number(self.article.ack_xml):
                r.append(('award-id', 'WARNING', 'ack has contract number.'))
            if has_number(self.article.fn_financial_disclosure):
                r.append(('award-id', 'WARNING', 'fn[@fn-type="financial_disclosure"] has contract number.'))
        else:
            for item in self.article.award_id:
                r.append(('award-id', 'OK', item))
        return r

    @property
    def award_id(self):
        return utils.display_values('award_id', self.article.award_id)

    @property
    def funding_statement(self):
        return utils.display_values('funding_statement', self.article.funding_statement)

    @property
    def ack_xml(self):
        return display_value('ack_xml', self.article.ack_xml)

    @property
    def fpage(self):
        return required('fpage', self.article.fpage)

    @property
    def fpage_seq(self):
        return display_value('fpage_seq', self.article.fpage_seq)

    @property
    def lpage(self):
        return display_value('lpage', self.article.lpage)

    @property
    def elocation_id(self):
        return display_value('elocation_id', self.article.elocation_id)

    @property
    def affiliations(self):
        r = []
        for a in self.article.affiliations:
            r.append(('xml', 'OK', a.xml))
            r.append(required('id', a.id))
            r.append(required('original', a.original))
            r.append(required('normalized', a.norgname))
            r.append(required('orgname', a.orgname))
            r.append(required('country', a.country))
        return r

    @property
    def clinical_trial(self):
        return display_value('clinical_trial', self.article.clinical_trial)

    def _total(self, total, count, label_total, label_count):
        if total == '0' and count == 'None':
            r = (label_total, 'OK', total)
        elif total == count:
            r = (label_total, 'OK', total)
        else:
            r = (label_count + ' (' + count + ') x ' + label_total + ' (' + total + ')', 'ERROR', 'They must have the same value')
        return r

    @property
    def total_of_pages(self):
        return self._total(self.article.total_of_pages, self.article.page_count, 'total of pages', 'page-count')

    @property
    def total_of_references(self):
        return self._total(self.article.total_of_references, self.article.ref_count, 'total of references', 'ref-count')

    @property
    def total_of_tables(self):
        return self._total(self.article.total_of_tables, self.article.table_count, 'total of tables', 'table-count')

    @property
    def total_of_equations(self):
        return self._total(self.article.total_of_equations, self.article.equation_count, 'total of equations', 'equation-count')

    @property
    def total_of_figures(self):
        return self._total(self.article.total_of_figures, self.article.fig_count, 'total of figures', 'fig-count')

    @property
    def abstracts(self):
        r = []
        for item in self.article.abstracts:
            r.append(('abstract: ' + item.language, 'OK', item.text))
        return r

    @property
    def history(self):
        received = utils.format_dateiso(self.article.received)
        accepted = utils.format_dateiso(self.article.accepted)

        if received is not None and accepted is not None:
            r = [('history', 'OK', received + ' - ' + accepted)]
            if received > accepted:
                r = 'received (' + received + ')  must be a previous date than accepted (' + accepted + ').'
                r = [('history', 'ERROR', r)]
        else:
            r = []
            r.append(conditional_required('history: received', received))
            r.append(conditional_required('history: accepted', accepted))
        return r

    @property
    def received(self):
        return display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return display_attributes('accepted', self.article.accepted)

    @property
    def license(self):
        return required('license', self.article.license)

    @property
    def references(self):
        r = []
        for ref in self.article.references:
            r.append(ReferenceContentValidation(ref))
        return r

    @property
    def press_release_id(self):
        return display_value('press_release_id', self.article.press_release_id)

    @property
    def issue_pub_date(self):
        return required_one('issue_pub_date', self.article.issue_pub_date)

    @property
    def article_pub_date(self):
        return display_attributes('article_pub_date', self.article.article_pub_date)

    @property
    def is_ahead(self):
        return display_value('is_ahead', self.article.is_ahead)

    @property
    def ahpdate(self):
        return display_value('ahpdate', self.article.ahpdate)

    @property
    def is_article_press_release(self):
        return display_value('is_article_press_release', self.article.is_article_press_release)

    @property
    def illustrative_materials(self):
        return utils.display_values('illustrative_materials', self.article.illustrative_materials)

    @property
    def is_text(self):
        return display_value('is_text', self.article.is_text)

    @property
    def previous_pid(self):
        return display_value('previous_pid', self.article.previous_pid)


class ReferenceContentValidation(object):

    def __init__(self, reference):
        self.reference = reference

    def evaluate(self):
        r = []
        r.append(self.xml)
        r.append(self.mixed_citation)
        r.append(self.publication_type)
        r.append(self.year)
        r.append(self.source)
        r.append(self.article_title)
        r.append(self.chapter_title)
        for item in self.person_groups:
            r.append(item)
        return r

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        return required('source', self.reference.source)

    def data_related_to_publication_type(self, label, value, status):
        status = attributes.article_title_status()
        if self.reference.publication_type in status['required']:
            return required(label, value)
        elif self.reference.publication_type in status['not_allowed']:
            return (label, 'ERROR', label + ' is not allowed in ' + self.reference.publication_type)
        elif self.reference.publication_type in status['allowed']:
            return display_value(label, value)
        else:
            return (label, 'WARNING', label + ' is not expected in ' + self.reference.publication_type)

    @property
    def article_title(self):
        return self.data_related_to_publication_type('article_title', self.reference.article_title, attributes.article_title_status())

    @property
    def chapter_title(self):
        return self.data_related_to_publication_type('chapter_title', self.reference.chapter_title, attributes.chapter_title_status())

    @property
    def publication_type(self):
        return expected_values('publication_type', self.reference.publication_type, attributes.PUBLICATION_TYPE)

    @property
    def xml(self):
        return display_value('xml', format_xml_in_html(self.reference.xml))

    @property
    def mixed_citation(self):
        return required('mixed_citation', format_xml_in_html(self.reference.mixed_citation))

    @property
    def person_groups(self):
        r = []
        for person in self.reference.person_groups:
            if isinstance(person, article.PersonAuthor):
                for item in validate_contrib_names(person):
                    r.append(item)
            elif isinstance(person, article.CorpAuthor):
                r.append('collab', 'OK', item)
        return r

    @property
    def year(self):
        return required('year', self.reference.year)

    @property
    def publisher_name(self):
        return display_value('publisher_name', self.reference.publisher_name)

    @property
    def publisher_loc(self):
        return display_value('publisher_loc', self.reference.publisher_loc)

    @property
    def fpage(self):
        return conditional_required('fpage', self.reference.fpage)
