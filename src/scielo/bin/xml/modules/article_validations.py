# coding=utf-8

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


def required(label, value, default_status):
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
        return (label, error_or_warning, 'Invalid character/word (' + invalid + ') in ' + label + ': ' + value)
    else:
        return (label, 'OK', value)


def validate_name(label, value, invalid_terms):
    r = []
    result = required(label, value, 'WARNING')
    label, status, msg = result
    if status == 'OK':
        result = invalid_terms_in_value(label, value, invalid_terms, 'WARNING')
    r.append(result)
    return r


def validate_surname(label, value):
    result = []
    reject = []
    suffix_list = [u'Nieto', u'Sobrino', u'Hijo', u'Neto', u'Sobrinho', u'Filho', u'Júnior', u'JÚNIOR', u'Junior', u'Senior', u'Sr', u'Jr']
    r = []
    label, status, msg = required(label, value, 'ERROR')
    if status == 'OK':

        parts = value.split(' ')
        for i in range(0, len(parts)-2):
            if not parts[i][0:1] == parts[i][0:1].lower():
                reject.append(parts[i])
        u = parts[len(parts)-1]

        suffix = ''
        if u in suffix_list:
            reject.append(parts[len(parts)-1])
            suffix = parts[len(parts)-1]

        if len(reject) > 0:
            status = 'WARNING'
            msg = 'Invalid terms (' + ','.join(reject) + ') in ' + value + '. '
            if len(suffix) > 0:
                msg += suffix + ' must be identified as <suffix>' + suffix + '</suffix>.'
            r.append((label, status, msg))

    if status == 'OK':
        msg = value
        r.append((label, status, msg))
    return r


def validate_contrib_names(author, affiliations=[]):
    results = validate_surname('surname', author.surname) + validate_name('given-names', author.fname, ['_'])
    if len(affiliations) > 0:
        aff_ids = [aff.id for aff in affiliations if aff.id is not None]
        if len(author.xref) == 0:
            results.append(('xref', 'FATAL ERROR', 'Author has no xref. Expected values: ' + '|'.join(aff_ids)))
        else:
            for xref in author.xref:
                if not xref in aff_ids:
                    results.append(('xref', 'ERROR', 'Invalid value of xref/@rid. Valid values: ' + '|'.join(aff_ids)))
    return results


class ArticleContentValidation(object):

    def __init__(self, article, validate_order):
        self.article = article
        self.validate_order = validate_order

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
        items = [self.journal_title,
                    self.publisher_name,
                    self.journal_id,
                    self.journal_id_nlm_ta,
                    self.journal_issns,
                    self.issue_label,
                    self.language,
                    self.article_type,
                    self.article_date_types,
                    self.toc_section,
                    self.order,
                    self.doi,
                    self.pagination,
                    self.total_of_pages,
                    self.total_of_equations,
                    self.total_of_tables,
                    self.total_of_figures,
                    self.total_of_references,
                    self.titles,
                    self.contrib_names,
                    self.contrib_collabs,
                    self.affiliations,
                    self.funding,
                    self.license_text,
                    self.license_url,
                    self.license_type,
                    self.history,
                    self.abstracts,
                    self.keywords,
                    self.validate_xref_reftype,
                    self.missing_xref_list
                ]
        return self.normalize_validations(items)

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        return expected_values('@article-type', self.article.article_type, attributes.DOCTOPIC.keys(), 'FATAL ')

    @property
    def language(self):
        return expected_values('@xml:lang', self.article.language, ['en', 'es', 'pt', 'de', 'fr'], 'FATAL ')

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
            _valid.append(('ISSN', 'FATAL ERROR', 'Missing ISSN. Required at least one.'))
        return _valid

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section, 'FATAL ERROR')

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
        return [('collab', 'OK', collab.collab) for collab in self.article.contrib_collabs]

    @property
    def titles(self):
        r = []
        for item in self.article.titles:
            if item.title is not None and item.language is not None:
                r.append(('title', 'OK', item.language + ': ' + item.title))
            else:
                if item.language is None:
                    r.append(('title language', 'ERROR', 'Missing language for ' + item.title))
                elif item.title is None:
                    r.append(('title', 'ERROR', 'Missing title for ' + item.language))
                else:
                    r.append('title', 'ERROR', 'Missing titles')
        return r

    @property
    def trans_languages(self):
        return article_utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        if self.article.is_ahead:
            return required('doi', self.article.doi, 'FATAL ERROR')
        else:
            return required('doi', self.article.doi, 'WARNING')

    @property
    def article_previous_id(self):
        return display_value('article-id (previous pid)', self.article.article_previous_id)

    @property
    def order(self):
        def valid(order, status):
            r = ('OK', order)
            if order is None:
                r = (status, 'Missing order. Expected number 1 to 99999.')
            else:
                if order.isdigit():
                    if int(order) < 1 or int(order) > 99999:
                        r = (status, order + ': Invalid format of order. Expected number 1 to 99999.')
                else:
                    r = (status, order + ': Invalid format of order. Expected number 1 to 99999.')
            return r
        if self.validate_order:
            status = 'FATAL ERROR'
        else:
            status = 'ERROR'
        status, msg = valid(self.article.order, status)
        return ('order', status, msg)

    @property
    def article_id_other(self):
        r = ('article-id (other)', 'OK', self.article.article_id_other)
        if self.article.fpage is not None:
            if self.article.fpage == '00' or not self.article.fpage.isdigit():
                r = ('article-id (other)', 'FATAL ERROR', 'article-id[@pub-id-type="other"] is required if there is no fpage > 0 or fpage is not number.')
        return r

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return ('issue label', 'ERROR', 'Required one of volume and/or number')
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
    def pagination(self):
        r = ('fpage', 'OK', self.article.fpage)
        if self.article.fpage is None:
            r = required('elocation-id', self.article.elocation_id, 'ERROR')
        return r

    @property
    def affiliations(self):
        import affiliations_services

        r = []
        labels = ['institution[@content-type="normalized"]', 'country', 'country/@country', 'state', 'city']
        for aff in self.article.affiliations:
            text = aff.original if aff.original is not None else aff.xml
            r.append(('aff xml', 'INFO', aff.xml))
            r.append(required('aff id', aff.id, 'FATAL ERROR'))
            r.append(required('aff original', aff.original, 'ERROR'))

            norgname, ncountry, icountry, state, city, errors = affiliations_services.validate_affiliation(aff.orgname, aff.norgname, aff.country, aff.i_country, aff.state, aff.city)
            suggestions = [norgname, ncountry, icountry, state, city]
            values = [aff.norgname, aff.country, aff.i_country, aff.state, aff.city]

            if aff.orgname is None and aff.norgname is None and norgname is None:
                r.append(('institution[@content-type="normalized"] or institution[@content-type="orgname"]', 'FATAL ERROR', 'Required'))
            if aff.country is None and aff.i_country is None and ncountry is None and icountry is None:
                r.append(('country or country/@country', 'FATAL ERROR', 'Required'))

            for i in range(0, len(labels)):
                if suggestions[i] is None:
                    if values[i] is not None:
                        r.append((labels[i], 'WARNING', values[i] + ' was not found in the normalized ' + labels[i] + ' list.'))
                else:
                    if suggestions[i] != values[i]:
                        if values[i] is None:
                            r.append((labels[i], 'WARNING', 'it was suggested ' + suggestions[i] + '.'))
                        else:
                            r.append((labels[i], 'WARNING', suggestions[i] + ' was suggested instead of ' + values[i] + '.'))
            if len(errors) > 0:
                r.append(('aff orgname and country', 'WARNING', errors))
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
                r = 'received (' + received + ')  must be a date before accepted (' + accepted + ').'
                r = [('history', 'FATAL ERROR', r)]
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
        return required('license-p', self.article.license_text, 'ERROR')

    @property
    def license_url(self):
        return required('license/@href', self.article.license_url, 'ERROR')

    @property
    def license_type(self):
        return expected_values('@license-type', self.article.license_type, ['open-access'])

    @property
    def references(self):
        r = []
        for ref in self.article.references:
            r.append((ref, ReferenceContentValidation(ref).evaluate()))
        return r

    @property
    def press_release_id(self):
        return display_value('press_release_id', self.article.press_release_id)

    @property
    def article_date_types(self):
        r = []
        date_types = []
        expected = ['epub-ppub', 'epub and collection', 'epub']
        if self.article.epub_date is not None:
            date_types.append('epub')
        if self.article.collection_date is not None:
            date_types.append('collection')
        if self.article.epub_ppub_date is not None:
            date_types.append('epub-ppub')
        c = ' and '.join(date_types)
        if c in expected:
            r.append(('article dates', 'OK', c))
        else:
            r.append(('article dates', 'ERROR', 'Invalid combination of date types: ' + c + '. Expected values: ' + ' | '.join(expected)))
        return r

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

    @property
    def validate_xref_reftype(self):
        message = []
        reftypes_and_tag = {'aff': 'aff', 'app': 'app', 'author-notes': 'fn', 'bibr': 'ref', 'boxed-text': 'boxed-text', 'contrib': 'fn', 'corresp': 'corresp', 'disp-formula': 'disp-formula', 'fig': 'fig', 'fn': 'fn', 'list': 'list', 'other': '?', 'supplementary-material': 'supplementary-material', 'table': 'table-wrap'}

        id_and_elem_name = {node.attrib.get('id'):node.tag for node in self.article.elements_which_has_id_attribute if node.attrib.get('id') is not None}

        for xref in self.article.xref_nodes:
            if xref['rid'] is None:
                message.append('xref/@rid', 'FATAL ERROR', 'Missing @rid in ' + xref['xml'])
            if xref['ref-type'] is None:
                message.append('xref/@ref-type', 'FATAL ERROR', 'Missing @ref-type in ' + xref['xml'])
            if xref['rid'] is not None and xref['ref-type'] is not None:
                tag = id_and_elem_name.get(xref['rid'])
                if tag is None:
                    message.append(('xref/@rid', 'FATAL ERROR', 'Missing element[@id=' + xref['rid'] + ' and @ref-type=' + xref['ref-type'] + ']'))
                elif reftypes_and_tag.get(xref['ref-type']) is None:
                    # no need to validate
                    valid = True
                elif tag == reftypes_and_tag.get(xref['ref-type']):
                    valid = True
                elif tag != reftypes_and_tag.get(xref['ref-type']):
                    reftypes = [reftype for reftype, _tag in reftypes_and_tag.items() if _tag == tag]
                    message.append(('xref/@ref-type', 'ERROR', 'Unmatched @ref-type (' + xref['ref-type'] + ') and tag (' + tag + '): xref[@ref-type=' + xref['ref-type'] + '] is for ' + reftypes_and_tag.get(xref['ref-type']) + ', and valid values of @ref-type of ' + tag + '  is ' + '|'.join(reftypes)))
        return message

    @property
    def missing_xref_list(self):
        alert_tags = ['fig', 'table-wrap', 'ref', ]
        rid_list = [node['rid'] for node in self.article.xref_nodes]
        message = []
        for node in self.article.elements_which_has_id_attribute:
            _id = node.attrib.get('id')
            if _id is None:
                message.append((node.tag, 'ERROR', 'Missing @id'))
            else:
                if not _id in rid_list:
                    if node.tag in alert_tags:
                        message.append((node.tag, 'ERROR', 'Missing xref[@rid="' + _id + '"]'))
        return message


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
        return required('source', self.reference.source, 'ERROR')

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
        return required('mixed-citation', self.reference.mixed_citation, 'ERROR')

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
        return required('year', self.reference.year, 'ERROR')

    @property
    def publisher_name(self):
        return display_value('publisher-name', self.reference.publisher_name)

    @property
    def publisher_loc(self):
        return display_value('publisher-loc', self.reference.publisher_loc)

    @property
    def fpage(self):
        return conditional_required('fpage', self.reference.fpage)
