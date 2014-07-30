# coding=utf-8

from isis_models import DOCTOPIC

import attributes as attributes
import utils as utils

import article


def invalid_characters_in_value(label, value, invalid_characters):
    r = True
    for c in value:
        if c in invalid_characters:
            r = False
            break
    if not r:
        return 'ERROR: Invalid characteres (' + ';'.join(invalid_characters) + ') in ' + label + ': ' + value
    else:
        return value


def validate_author(author):
    r = utils.required('surname', author.surname)
    if r == author.surname:
        author.surname = invalid_characters_in_value('surname', author.surname, [' '])
    else:
        author.surname = r
    author.fname = utils.required('given-names', author.fname)
    return author


class ArticleContentValidation(object):

    def __init__(self, article):
        self.article = article

    @property
    def dtd_version(self):
        return utils.expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        return utils.expected_values('@article-type', self.article.article_type, DOCTOPIC.keys())

    @property
    def language(self):
        return utils.expected_values('@xml:lang', self.article.language, ['en', 'es', 'pt', 'de', 'fr'])

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
        return utils.required('journal title', self.article.journal_title)

    @property
    def publisher_name(self):
        return utils.required('publisher name', self.article.publisher_name)

    @property
    def journal_id(self):
        return utils.required('journal-id', self.article.journal_id)

    @property
    def journal_id_nlm_ta(self):
        return utils.conditional_required('journal-id (nlm-ta)', self.article.journal_id_nlm_ta)

    @property
    def journal_issns(self):
        return utils.required_one('ISSN', self.article.journal_issns)

    @property
    def toc_section(self):
        return utils.required('subject', self.article.toc_section)

    @property
    def keywords(self):
        r = []
        for item in self.article.keywords:
            r.append(item['l'] + ': ' + item['k'])
        return r

    @property
    def contrib_names(self):
        r = []
        for item in self.article.contrib_names:
            item = validate_author(item)
            r.append(item)
        return r

    @property
    def contrib_collabs(self):
        return self.article.contrib_collabs

    @property
    def titles(self):
        r = []
        for item in self.article.title:
            r.append(item.language + ': ' + item.title)
        return r

    @property
    def trans_titles(self):
        r = []
        for item in self.article.trans_titles:
            if item.language is None:
                item.language = 'None'
            if item.title is None:
                item.title = 'None'
            r.append(item.language + ': ' + item.title)
        return r

    @property
    def trans_languages(self):
        return utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        return utils.required('doi', self.article.doi)

    @property
    def article_id_publisher_id(self):
        return utils.display_value('article id (previous pid)', self.article.article_id_publisher_id)

    @property
    def order(self):
        if self.article.order is not None:
            if self.article.order.isdigit():
                if len(self.article.order) != 5:
                    return 'ERROR: Invalid format of order. Expected 99999.'
                else:
                    return 'order: ' + self.article.order
            else:
                return 'ERROR: Invalid format of order. Expected 99999.'
        else:
            return utils.required('order', self.article.order)

    @property
    def article_id_other(self):
        return utils.display_value('article-id (other)', self.article.article_id_other)

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return 'ERROR: Required one of volume and/or number'
        else:
            return self.volume + self.number

    @property
    def volume(self):
        return utils.display_value('volume', self.article.volume)

    @property
    def number(self):
        return utils.display_value('number', self.article.number)

    @property
    def supplement(self):
        return utils.display_value('supplement', self.article.supplement)

    @property
    def is_issue_press_release(self):
        return utils.display_value('is_issue_press_release', self.article.is_issue_press_release)

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
        r = ''
        if self.article.award_id is None:
            found = False
            for c in self.article.ack_xml:
                if c in '0123456789':
                    found = True
                    break
            if found:
                r = 'WARNING: ack has contract number.' + self.article.ack_xml
        else:
            r = utils.display_values('Funding number', self.article.award_id)
        return r

    @property
    def award_id(self):
        return utils.display_values('award_id', self.article.award_id)

    @property
    def funding_statement(self):
        return utils.display_values('funding_statement', self.article.funding_statement)

    @property
    def ack_xml(self):
        return utils.display_value('ack_xml', self.article.ack_xml)

    @property
    def fpage(self):
        return utils.required('fpage', self.article.fpage)

    @property
    def fpage_seq(self):
        return utils.display_value('fpage_seq', self.article.fpage_seq)

    @property
    def lpage(self):
        return utils.display_value('lpage', self.article.lpage)

    @property
    def elocation_id(self):
        return utils.display_value('elocation_id', self.article.elocation_id)

    @property
    def affiliations(self):
        r = []
        for a in self.article.affiliations:
            a.id = utils.required('id', a.id)
            a.original = utils.required('original', a.original)
            a.norgname = utils.required('normalized', a.norgname)
            a.orgname = utils.required('orgname', a.orgname)
            a.country = utils.required('country', a.country)
            r.append(a)
        return r

    @property
    def clinical_trial(self):
        return utils.display_value('clinical_trial', self.article.clinical_trial)

    @property
    def total_of_references(self):
        return utils.display_value('total_of_references', self.article.total_of_references)

    @property
    def total_of_tables(self):
        return utils.display_value('total_of_tables', self.article.total_of_tables)

    @property
    def total_of_figures(self):
        return utils.display_value('total_of_figures', self.article.total_of_figures)

    @property
    def abstracts(self):
        r = []
        for item in self.article.abstracts:
            r.append(item.language + ': ' + item.text)
        return r

    @property
    def history(self):
        received = utils.format_dateiso(self.article.received)
        accepted = utils.format_dateiso(self.article.accepted)

        r = ''
        if received is not None and accepted is not None:
            if received > accepted:
                r = 'Invalid value for received (' + received + ') and accepted (' + accepted + '). Received date must be previous than accepted date.'
        return r

    @property
    def received(self):
        return utils.display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return utils.display_attributes('accepted', self.article.accepted)

    @property
    def license(self):
        return utils.required('license', self.article.license)

    @property
    def references(self):
        r = []
        for ref in self.article.references:
            r.append(ReferenceContentValidation(ref))
        return r

    @property
    def press_release_id(self):
        return utils.display_value('press_release_id', self.article.press_release_id)

    @property
    def issue_pub_date(self):
        return utils.required_one('issue_pub_date', self.article.issue_pub_date)

    @property
    def article_pub_date(self):
        return utils.display_attributes('article_pub_date', self.article.article_pub_date)

    @property
    def is_ahead(self):
        return utils.display_value('is_ahead', self.article.is_ahead)

    @property
    def ahpdate(self):
        return utils.display_value('ahpdate', self.article.ahpdate)

    @property
    def is_article_press_release(self):
        return utils.display_value('is_article_press_release', self.article.is_article_press_release)

    @property
    def illustrative_materials(self):
        return utils.display_values('illustrative_materials', self.article.illustrative_materials)

    @property
    def is_text(self):
        return utils.display_value('is_text', self.article.is_text)

    @property
    def previous_pid(self):
        return utils.display_value('previous_pid', self.article.previous_pid)


class ReferenceContentValidation(object):

    def __init__(self, reference):
        self.reference = reference

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        return utils.required('source', self.reference.source)

    @property
    def language(self):
        return utils.display_value('language', self.reference.language)

    def data_related_to_publication_type(self, label, value, status):
        status = attributes.article_title_status()
        if self.reference.publication_type in status['required']:
            return utils.required(label, value)
        elif self.reference.publication_type in status['not_allowed']:
            return 'ERROR: ' + label + ' is not allowed in ' + self.reference.publication_type
        elif self.reference.publication_type in status['allowed']:
            return utils.display_value(label, value)
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
        return utils.display_value('trans_title', self.reference.trans_title)

    @property
    def trans_title_language(self):
        return utils.display_value('trans_title_language', self.reference.trans_title_language)

    @property
    def publication_type(self):
        return utils.expected_values('publication_type', self.reference.publication_type, attributes.PUBLICATION_TYPE)

    @property
    def xml(self):
        return utils.display_value('xml', self.reference.xml)

    @property
    def mixed_citation(self):
        return utils.required('mixed_citation', self.reference.mixed_citation)

    @property
    def person_groups(self):
        r = []
        for person in self.reference.person_groups:
            if isinstance(person, article.PersonAuthor):
                r.append(validate_author(person))
            elif isinstance(person, article.CorpAuthor):
                r.append(person)
        return r

    @property
    def issue(self):
        return utils.display_value('issue', self.reference.issue)

    @property
    def volume(self):
        return utils.display_value('volume', self.reference.volume)

    @property
    def supplement(self):
        return utils.display_value('supplement', self.reference.supplement)

    @property
    def edition(self):
        return utils.display_value('edition', self.reference.edition)

    @property
    def year(self):
        return utils.required('year', self.reference.year)

    @property
    def publisher_name(self):
        return utils.display_value('publisher_name', self.reference.publisher_name)

    @property
    def publisher_loc(self):
        return utils.display_value('publisher_loc', self.reference.publisher_loc)

    @property
    def fpage(self):
        return utils.display_value('fpage', self.reference.fpage)

    @property
    def lpage(self):
        return utils.display_value('lpage', self.reference.lpage)

    @property
    def page_range(self):
        return utils.display_value('page_range', self.reference.page_range)

    @property
    def size(self):
        return utils.display_attributes('size', self.reference.size)

    @property
    def label(self):
        return utils.display_value('label', self.reference.label)

    @property
    def etal(self):
        return utils.display_value('etal', self.reference.etal)

    @property
    def cited_date(self):
        return utils.display_value('cited_date', self.reference.cited_date)

    @property
    def ext_link(self):
        return utils.display_value('ext_link', self.reference.ext_link)

    @property
    def comments(self):
        return utils.display_value('comments', self.reference.comments)

    @property
    def notes(self):
        return utils.display_value('notes', self.reference.notes)

    @property
    def contract_number(self):
        return utils.display_value('contract_number', self.reference.contract_number)

    @property
    def doi(self):
        return utils.display_value('doi', self.reference.doi)

    @property
    def pmid(self):
        return utils.display_value('pmid', self.reference.pmid)

    @property
    def pmcid(self):
        return utils.display_value('pmcid', self.reference.pmcid)

    @property
    def conference_name(self):
        return utils.display_value('conference_name', self.reference.conference_name)

    @property
    def conference_location(self):
        return utils.display_value('conference_location', self.reference.conference_location)

    @property
    def conference_date(self):
        return utils.display_value('conference_date', self.reference.conference_date)
