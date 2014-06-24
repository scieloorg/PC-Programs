# coding=utf-8

from modules.isis_models import DOCTOPIC

import modules.attributes as attributes


def display_value(label, value):
    return label + ': ' + value if value is None else 'None'


def display_values(label, values):
    return label + ': ' + '\n'.join(values)


def display_attributes(label, attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        r.append('@' + key + ': ' + value)
    return label + '\n' + '\n'.join(r)


def display_items_with_attributes(label, items_with_attributes):
    r = label + ': ' + '\n'
    for item_name, item_values in items_with_attributes.items():
        r += display_values_with_attributes(item_name, item_values)
    return r


def display_values_with_attributes(label, values_with_attributes):
    return label + ': ' + '\n' + '\n'.join([display_attributes('=>', item) for item in values_with_attributes])


def required(label, value):
    return display_value(label, value) if value is not None else 'ERROR: Required ' + label + '. '


def expected_values(label, value, expected):
    return display_value(label, value) if value in expected else 'ERROR: ' + value + ' - Invalid value for ' + label + '. Expected values ' + ', '.join(expected)


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
        return display_values_with_attributes('related objects', self.article.related_objects)

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
        return display_values_with_attributes('related articles', self.article.related_objects)

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
        return required('journal-id (nlm-ta)', self.article.journal_id_nlm_ta)

    @property
    def journal_issns(self):
        return display_attributes('ISSN', self.article.journal_issns)

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section)

    @property
    def keywords(self):
        return display_values_with_attributes('keywords', self.article.keywords)

    @property
    def contrib_names(self):
        return display_values_with_attributes('contrib_names', self.article.contrib_names)

    @property
    def contrib_collabs(self):
        return display_values_with_attributes('contrib_collabs', self.article.contrib_collabs)

    @property
    def titles(self):
        return display_values_with_attributes('titles', self.article.titles)

    @property
    def trans_titles(self):
        return display_values_with_attributes('trans_titles', self.article.trans_titles)

    @property
    def trans_languages(self):
        return display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        return required('doi', self.article.doi)

    @property
    def article_id_publisher_id(self):
        return display_value('article id (previous pid)', self.article.article_id_publisher_id)

    @property
    def order(self):
        return required('order', self.article.order)

    @property
    def article_id_other(self):
        return display_value('article-id (other)', self.article.article_id_other)

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.issue and not self.article.supplement:
            return 'ERROR: Required one of volume, issue, supplement'
        else:
            return self.volume + self.issue + self.supplement

    @property
    def volume(self):
        return display_value('volume', self.article.volume)

    @property
    def issue(self):
        return display_value('issue', self.article.issue)

    @property
    def supplement(self):
        return display_value('supplement', self.article.supplement)

    @property
    def is_issue_press_release(self):
        return display_value('is_issue_press_release', self.article.is_issue_press_release)

    @property
    def funding_source(self):
        return display_values('funding_source', self.article.funding_source)

    @property
    def principal_award_recipient(self):
        return display_values('principal_award_recipient', self.article.principal_award_recipient)

    @property
    def principal_investigator(self):
        return display_values('principal_investigator', self.article.principal_investigator)

    @property
    def award_id(self):
        return display_values('award_id', self.article.award_id)

    @property
    def funding_statement(self):
        return display_values('funding_statement', self.article.funding_statement)

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
        return display_values_with_attributes('affiliations', self.article.affiliations)

    @property
    def clinical_trial(self):
        return display_value('clinical_trial', self.article.clinical_trial)

    @property
    def total_of_references(self):
        return display_value('total_of_references', self.article.total_of_references)

    @property
    def total_of_tables(self):
        return display_value('total_of_tables', self.article.total_of_tables)

    @property
    def total_of_figures(self):
        return display_value('total_of_figures', self.article.total_of_figures)

    @property
    def abstracts(self):
        return display_values_with_attributes('abstracts', self.article.abstracts)

    @property
    def history(self):
        return display_items_with_attributes('history', self.article.history)

    @property
    def references(self):
        r = ''
        for ref in self.article.references:
            r += ReferenceContentValidation(ref).report
        return r

    @property
    def press_release_id(self):
        return display_value('press_release_id', self.article.press_release_id)

    @property
    def issue_pub_date(self):
        return display_attributes('issue_pub_date', self.article.issue_pub_date)

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
        return display_values('illustrative_materials', self.article.illustrative_materials)

    @property
    def is_text(self):
        return display_value('is_text', self.article.is_text)

    @property
    def previous_pid(self):
        return display_value('previous_pid', self.article.previous_pid)


class ReferenceContentValidation(object):

    def __init__(self, reference):
        self.reference = reference

    @property
    def report(self):
        r = self.xml
        r += self.publication_type
        r += self.mixed_citation
        r += self.source
        r += self.year
        return r

    @property
    def source(self):
        return required('source', self.reference.source)

    @property
    def language(self):
        return display_value('language', self.reference.language)

    @property
    def data_related_to_publication_type(self, label, value, status):
        status = attributes.article_title_status()
        if self.reference.publication_type in status['required']:
            return required(label, value)
        elif self.reference.publication_type in status['not_allowed']:
            return 'ERROR: ' + label + ' is not allowed in ' + self.reference.publication_type
        elif self.reference.publication_type in status['allowed']:
            return display_value(label, value)
        else:
            return 'WARNING: ' + label + ' is not expected in ' + self.reference.publication_type

    @property
    def article_title(self):
        return self.data_related_to_publication_type('article_title', self.reference.article_title, attributes.article_title_status())

    @property
    def chapter_title(self):
        return self.data_related_to_publication_type('chapter_title', self.reference.chapter_title, attributes.chapter_title_status())

    @property
    def trans_title(self):
        return display_value('trans_title', self.reference.trans_title)

    @property
    def trans_title_language(self):
        return display_value('trans_title_language', self.reference.trans_title_language)

    @property
    def publication_type(self):
        return expected_values('publication_type', self.reference.publication_type, attributes.PUBLICATION_TYPE)

    @property
    def xml(self):
        return display_value('xml', self.reference.xml)

    @property
    def mixed_citation(self):
        return required('mixed_citation', self.reference.mixed_citation)

    @property
    def person_groups(self):
        return display_items_with_attributes('person_groups', self.reference.person_groups)

    @property
    def issue(self):
        return display_value('issue', self.reference.issue)

    @property
    def volume(self):
        return display_value('volume', self.reference.volume)

    @property
    def supplement(self):
        return display_value('supplement', self.reference.supplement)

    @property
    def edition(self):
        return display_value('edition', self.reference.edition)

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
        return display_value('fpage', self.reference.fpage)

    @property
    def lpage(self):
        return display_value('lpage', self.reference.lpage)

    @property
    def page_range(self):
        return display_value('page_range', self.reference.page_range)

    @property
    def size(self):
        return display_attributes('size', self.reference.size)

    @property
    def label(self):
        return display_value('label', self.reference.label)

    @property
    def etal(self):
        return display_value('etal', self.reference.etal)

    @property
    def cited_date(self):
        return display_value('cited_date', self.reference.cited_date)

    @property
    def ext_link(self):
        return display_value('ext_link', self.reference.ext_link)

    @property
    def comments(self):
        return display_value('comments', self.reference.comments)

    @property
    def notes(self):
        return display_value('notes', self.reference.notes)

    @property
    def contract_number(self):
        return display_value('contract_number', self.reference.contract_number)

    @property
    def doi(self):
        return display_value('doi', self.reference.doi)

    @property
    def pmid(self):
        return display_value('pmid', self.reference.pmid)

    @property
    def pmcid(self):
        return display_value('pmcid', self.reference.pmcid)

    @property
    def conference_name(self):
        return display_value('conference_name', self.reference.conference_name)

    @property
    def conference_location(self):
        return display_value('conference_location', self.reference.conference_location)

    @property
    def conference_date(self):
        return display_value('conference_date', self.reference.conference_date)
