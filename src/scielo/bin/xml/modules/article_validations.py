# coding=utf-8

from isis_models import DOCTOPIC

import attributes
import article_utils

import article


def format_value(value):
    if value is None:
        value = 'None'
    return value


def validate_value(value):
    result = []
    status = 'OK'
    if value is not None:
        if value.endswith(' '):
            status = 'WARNING'
            result.append(value + ' ends with "space"')
        if value.startswith('.'):
            status = 'WARNING'
            result.append(value + ' starts with "."')
        if value.startswith(' '):
            status = 'WARNING'
            result.append(value + ' starts with "space"')
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
    return (label, status, message) if value is not None else (label, 'WARNING', 'Required, if exists.')


def required_one(label, value):
    return (label, 'OK', display_attributes(value)) if value is not None else (label, 'ERROR', 'Required at least one ' + label + '.')


def required(label, value, default_status='ERROR'):
    status, message = validate_value(value)
    if not (value is None or value == ''):
        result = (label, status, message)
    else:
        result = (label, default_status, 'Required')
    return result


def expected_values(label, value, expected, fatal=''):
    return (label, 'OK', value) if value in expected else (label, fatal + 'ERROR', format_value(value) + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected))


def display_attributes(attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        status, message = validate_value(value)
        r.append(key + ' (' + status + '): ' + message)
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


def validate_name(label, value, invalid_characters):
    r = []
    result = required(label, value)
    label, status, msg = result
    if status == 'ERROR':
        result = (label, 'WARNING', 'Missing ' + label)
    if status == 'OK':
        result = invalid_characters_in_value(label, value, invalid_characters, 'WARNING')
    r.append(result)
    return r


def validate_contrib_names(author, affiliations=[]):
    results = validate_name('surname', author.surname, [' ', '_']) + validate_name('given-names', author.fname, ['_'])
    if len(affiliations) > 0:
        aff_ids = [aff.id for aff in affiliations if aff.id is not None]
        if len(author.xref) == 0:
            results.append(('xref', 'WARNING', 'Author has no xref. Expected values: ' + '|'.join(aff_ids)))
        else:
            for xref in author.xref:
                if not xref in aff_ids:
                    results.append(('xref', 'ERROR', 'Invalid value of xref/@rid. Valid values: ' + '|'.join(aff_ids)))
    return results


class ArticleContentValidation(object):

    def __init__(self, article, validate_order):
        self.article = article
        self.validate_order = validate_order

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        return expected_values('@article-type', self.article.article_type, DOCTOPIC.keys())

    @property
    def language(self):
        return expected_values('@xml:lang', self.article.language, ['en', 'es', 'pt', 'de', 'fr'], 'FATAL ')

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
        return article_utils.display_values_with_attributes('related objects', self.article.related_objects)

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
        return article_utils.display_values_with_attributes('related articles', self.article.related_objects)

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
            for result in validate_contrib_names(item, self.article.affiliations):
                r.append(result)
        return r

    @property
    def contrib_collabs(self):
        return [('collab', 'OK', collab) for collab in self.article.contrib_collabs]

    @property
    def titles(self):
        r = []
        for item in self.article.titles:
            if item.title is not None and item.language is not None:
                r.append(('title', 'OK', item.language + ': ' + item.title))
            else:
                if item.language is None:
                    r.append(('title language', 'ERROR', 'Missing language for ' + item.title))
                if item.title is None:
                    r.append(('title', 'ERROR', 'Missing title for ' + item.title))
        return r

    @property
    def trans_languages(self):
        return article_utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        return required('doi', self.article.doi)

    @property
    def article_previous_id(self):
        return display_value('article id (previous pid)', self.article.article_previous_id)

    @property
    def order(self):
        def valid(order):
            r = ('?', order)
            if order is not None:
                if order.isdigit():
                    if len(order) != 5:
                        r = ('FATAL ERROR', 'Invalid format of order. Expected 99999.')
                    if int(order) < 1 or int(order) > 99999:
                        r = ('FATAL ERROR', 'Invalid format of order. Expected number 1 to 99999.')
                else:
                    r = ('FATAL ERROR', 'Invalid format of order. Expected 99999.')
            return r
        r = ('order', 'OK', self.article.order)
        if self.validate_order:
            r = valid(self.article.order)
            if r[0] == '?':
                r = required('order', self.article.order)
            elif r[0] == 'FATAL ERROR':
                r = ('order', 'FATAL ERROR', r[1])
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
                r.append(('award-id', 'WARNING', 'Found number ' + c + ' in ack. ' + self.article.ack_xml))
            found, c = has_number(self.article.financial_disclosure)
            if found is True:
                r.append(('award-id', 'WARNING', 'Found number ' + c + ' in fn[@fn-type="financial-disclosure"]. ' + self.article.fn_financial_disclosure))
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
    def fpage(self):
        return conditional_required('fpage', self.article.fpage)

    @property
    def fpage_seq(self):
        return conditional_required('fpage/@seq', self.article.fpage_seq)

    @property
    def lpage(self):
        return display_value('lpage', self.article.lpage)

    @property
    def elocation_id(self):
        return conditional_required('elocation-id', self.article.elocation_id)

    @property
    def affiliations(self):
        r = []
        for aff in self.article.affiliations:
            r.append(('aff xml', 'OK', aff.xml))
            r.append(required('aff id', aff.id, 'FATAL ERROR'))
            r.append(required('aff original', aff.original))
            r.append(required('aff normalized', aff.norgname, 'WARNING'))
            r.append(required('aff orgname', aff.orgname))
            r.append(required('aff country', aff.country, 'FATAL ERROR'))
        return r

    @property
    def clinical_trial(self):
        return display_value('clinical_trial', self.article.clinical_trial)

    def _total(self, total, count, label_total, label_count):
        if count is None:
            count = 0
        elif count.isdigit():
            count = int(count)

        if total == count:
            r = (label_total, 'OK', str(total))
        else:
            r = (label_count + ' (' + str(count) + ') x ' + label_total + ' (' + str(total) + ')', 'ERROR', 'They must have the same value')
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
            if item.language is not None and item.text is not None:
                r.append(('abstract: ', 'OK', item.language + ':' + item.text))
            else:
                if item.language is None:
                    r.append(('abstract: ', 'WARNING', 'Missing language for ' + item.text))
                if item.text is None:
                    r.append(('abstract: ', 'ERROR', 'Missing text for ' + item.language))
        return r

    @property
    def history(self):
        received = article_utils.format_dateiso(self.article.received)
        accepted = article_utils.format_dateiso(self.article.accepted)

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
    def license_text(self):
        return required('license-p', self.article.license_text)

    @property
    def license_url(self):
        return required('license/@href', self.article.license_url)

    @property
    def license_type(self):
        return expected_values('@license-type', self.article.license_type, ['open-access'])

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
        return article_utils.display_values('illustrative_materials', self.article.illustrative_materials)

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
        for item in self.publication_type_dependence:
            r.append(item)
        for item in self.authors_list:
            r.append(item)
        return r

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        return required('source', self.reference.source)

    def validate_element(self, label, value):
        res = attributes.validate_element(self.reference.publication_type, label, value)
        if res != '':
            return (label, 'ERROR', res)
        else:
            if not value is None and value != '':
                return (label, 'OK', value)

    @property
    def publication_type_dependence(self):
        r = []
        items = [
                self.validate_element('article-title', self.reference.article_title), 
                self.validate_element('chapter-title', self.reference.chapter_title), 
                self.validate_element('conf-name', self.reference.conference_name), 
                self.validate_element('date-in-citation[@content-type="access-date"]', self.reference.cited_date), 
                self.validate_element('ext-link', self.reference.ext_link), 
            ]
        for item in items:
            if item is not None:
                r.append(item)
        return r

    @property
    def publication_type(self):
        return expected_values('@publication-type', self.reference.publication_type, attributes.PUBLICATION_TYPE)

    @property
    def xml(self):
        return ('xml', 'OK', self.reference.xml)

    @property
    def mixed_citation(self):
        return required('mixed-citation', self.reference.mixed_citation)

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
                r.append(('invalid person', 'WARNING', type(person)))
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
