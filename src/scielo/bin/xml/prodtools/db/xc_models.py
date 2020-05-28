# coding=utf-8

import os
import shutil

from prodtools import _

from prodtools.utils import utils
from prodtools.utils import xml_utils
from prodtools.utils import fs_utils
from prodtools.utils import encoding
from prodtools.reports import html_reports
from prodtools.reports import validation_status
from prodtools.data.article import Issue, Article, Journal
from prodtools.data.article import PersonAuthor, CorpAuthor, AnonymousAuthor
from prodtools.data import attributes
from prodtools.data import article_utils
from prodtools.db import serial
from prodtools.validations import article_data_reports


ISSN_TYPE_CONVERSION = {
    'ONLIN': 'epub',
    'PRINT': 'ppub',
    'epub': 'ONLIN',
    'ppub': 'PRINT',
}

FREQ = dict([
    ("?", "Unknown"),
    ("A", "Annual"),
    ("B", "Bimonthly (every two months)"),
    ("C", "Semiweekly (twice a week)"),
    ("D", "Daily"),
    ("E", "Biweekly (every two weeks)"),
    ("F", "Semiannual (twice a year)"),
    ("G", "Biennial (every two years)"),
    ("H", "Triennial (every three years)"),
    ("I", "Three times a week"),
    ("J", "Three times a month"),
    ("K", "Irregular (known to be so)"),
    ("M", "Monthly"),
    ("Q", "Quarterly"),
    ("S", "Semimonthly (twice a month)"),
    ("T", "Three times a year"),
    ("W", "Weekly"),
    ("Z", "Other frequencies"),
])


def author_tag(is_person, is_analytic_author):
    r = {}
    r[True] = {True: '10', False: '16'}
    r[False] = {True: '11', False: '17'}
    return r[is_person][is_analytic_author]


def title_issns(record):
    issn_items = registered_issn_items(record.get('435'))
    if issn_items is None:
        issn_items = {}
        issn = record.get('935')
        if issn is None:
            issn = record.get('400')
        issn_type = record.get('35')
        if issn_type is None:
            issn_type = 'UNKNOWN_ISSN_TYPE'
        issn_items[issn_type] = issn
    return issn_items


def issue_issns(record):
    issn_items = registered_issn_items(record.get('435'))
    if issn_items is None:
        issn_items = {}
        issn = record.get('935')
        if issn is None:
            issn = record.get('35')
        issn_type = 'UNKNOWN_ISSN_TYPE'
        issn_items[issn_type] = issn
    return issn_items


def registered_issn_items(issns_field):
    issn_items = issns_field
    if issns_field is not None:
        issn_items = {}
        if not isinstance(issns_field, list):
            issns_field = [issns_field]
        if isinstance(issns_field, list):
            for occ in issns_field:
                issn_items[ISSN_TYPE_CONVERSION.get(occ.get('t'))] = occ.get('_')
    return issn_items


def format_issn_fields(issn_items, convert_issn_type):
    fields = []
    if issn_items is not None:
        if isinstance(issn_items, dict):
            for issn_type, issn_value in issn_items.items():
                if convert_issn_type:
                    issn_type = ISSN_TYPE_CONVERSION.get(issn_type, issn_type)
                fields.append({'_': issn_value, 't': issn_type})
    return fields


class RegisteredArticle(object):
    def __init__(self, article_records, i_record):
        self._issue = None
        self.i_record = i_record
        self.article_records = article_records

    @property
    def pid(self):
        #FIXME
        i_order = '0'*4 + self.i_record.get('36')[4:]
        r = 'S' + self.i_record.get('35') + self.i_record.get('36')[0:4] + i_order[-4:] + self.order
        return r if len(r) == 23 else None

    @property
    def dates(self):
        return [item for item in sorted([self.article_records[0].get('91'), self.article_records[0].get('93')]) if item is not None]

    @property
    def creation_date_display(self):
        return '' if self.creation_date is None else utils.display_datetime(self.creation_date, '')

    @property
    def last_update_display(self):
        return '' if self.last_update_date is None else utils.display_datetime(self.last_update_date, self.last_update_time)

    @property
    def creation_date(self):
        if len(self.dates) > 0:
            return self.dates[0]

    @property
    def last_update_date(self):
        if len(self.dates) > 0:
            return self.dates[-1]

    @property
    def last_update_time(self):
        return self.article_records[0].get('92', '')

    @property
    def order(self):
        _order = '0'*5 + self.article_records[1]['121']
        return _order[-5:]

    @property
    def scielo_id(self):
        return self.article_records[1].get('885')

    @property
    def xml_name(self):
        names = self.filename
        if names.endswith('.xml'):
            names = names[0:-4]
        names = names.split('/')
        if len(names) > 0:
            return names[-1]

    @property
    def filename(self):
        return self.article_records[1]['702']


class ArticleRecords(object):

    def __init__(self, article, i_record, article_files):
        self.article = article
        self.article_files = article_files
        self.i_record = i_record
        self.import_from_i_record()
        self.add_issue_data()
        self.add_article_data()
        self.set_common_data(article_files.filename, article_files.issue_files.issue_folder, article_files.relative_xml_filename)

    def import_from_i_record(self):
        self._metadata = {}
        for k in ['30', '42', '62', '130', '35', '435', '421', '65', '480']:
            if k in self.i_record.keys():
                self._metadata[k] = self.i_record[k]

    def add_issue_data(self):
        if '130' not in self._metadata.keys():
            self._metadata['130'] = self.article.journal_title
        if '62' not in self._metadata.keys():
            self._metadata['62'] = self.article.publisher_name
        if '421' not in self._metadata.keys():
            self._metadata['421'] = self.article.journal_id_nlm_ta
        #FIXME
        #if not '435' in self._metadata.keys():
        #    self._metadata['435'] = self.article.journal_issns

    def fix_issue_data(self):
        if '130' in self._metadata.keys():
            self._metadata['100'] = self._metadata['130']
            del self._metadata['130']
        self._metadata['435'] = format_issn_fields(self.article.journal_issns, False)
        if '480' in self._metadata.keys():
            del self._metadata['480']

    @property
    def metadata(self):
        return self._metadata

    def add_article_data(self):
        if self.article.is_provisional:
            self._metadata['742'] = 'provisional'
        if self.article.dtd_version is not None:
            self._metadata['120'] = 'XML_' + self.article.dtd_version
        self._metadata['71'] = attributes.normalize_doctopic(self.article.article_type)
        self._metadata['40'] = self.article.language
        self._metadata['38'] = self.article.illustrative_materials
        self._metadata['709'] = 'text' if self.article.is_text else 'article'

        #registro de artigo, link para pr
        #<related-article related-article-type="press-release" id="01" specific-use="processing-only"/>
        # ^i<PID>^tpr^rfrom-article-to-press-release
        #
        #registro de pr, link para artigo
        #<related-article related-article-type="in-this-issue" id="pr01" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="10.1590/S0102-311X2013000500014 " ext-link-type="doi"/>
        # ^i<doi>^tdoi^rfrom-press-release-to-article
        #
        #registro de errata, link para artigo
        #<related-article related-article-type="corrected-article" vol="29" page="970" id="RA1" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="10.1590/S0102-311X2013000500014" ext-link-type="doi"/>
        # ^i<doi>^tdoi^rfrom-corrected-article-to-article
        self._metadata['241'] = []

        for item in self.article.related_articles:
            new = {}
            new['i'] = item.get('href') if item.get('href') is not None else item.get('id')
            _t = item.get('related-article-type')
            if _t == 'press-release':
                _t = 'pr'
            elif _t == 'in-this-issue':
                _t = 'article'
            if _t == 'commentary':
                _t = 'pr'
            elif _t == 'article-reference':
                _t = 'article'
            new['t'] = _t
            new['n'] = item.get('ext-link-type')
            self._metadata['241'].append(new)

        if self.article.is_article_press_release or self.article.is_issue_press_release:
            self._metadata['41'] = 'pr'

        self._metadata['85'] = self.article.keywords
        self._metadata['49'] = 'nd' if self.article.section_code is None else self.article.section_code

        self._metadata['10'] = []
        #self._metadata['10?'] = []
        for item in self.article.contrib_names:
            surname_and_suffix = item.surname
            if item.suffix is not None:
                if item.suffix != '':
                    surname_and_suffix += ' ' + item.suffix
            new = {}
            new['n'] = item.fname
            new['s'] = surname_and_suffix
            new['p'] = item.prefix
            new['r'] = attributes.normalize_role(item.role)
            new['1'] = ' '.join(item.xref)
            new['k'] = item.contrib_id.get('orcid')
            new['l'] = item.contrib_id.get('lattes')
            self._metadata['10'].append(new)

            #for contrib_id_type, contrib_id in item.contrib_id.items():
            #    self._metadata['10?'].append({'n': item.fname, 's': surname_and_suffix, 'i': contrib_id, 't': contrib_id_type})

        self._metadata['11'] = [c.collab for c in self.article.contrib_collabs]
        self._metadata['12'] = []
        for item in self.article.titles:
            new = {}
            new['_'] = item.title
            new['s'] = item.subtitle
            new['l'] = item.language
            self._metadata['12'].append(new)

        self._metadata['601'] = self.article.trans_languages
        self._metadata['237'] = self.article.doi
        self._metadata['337'] = [
            {'l': lang, 'd': doi}
            for lang, doi in self.article.doi_and_lang
            if doi and lang
            ]

        self._metadata['121'] = self.article.order
        self._metadata['881'] = self.article.previous_pid
        self._metadata['885'] = (
            self.article.scielo_id or
            self.article.registered_scielo_id)

        if self.article.is_ahead:
            self._metadata['32'] = 'ahead'
        else:
            self._metadata['31'] = self.article.volume
            self._metadata['32'] = self.article.number
            self._metadata['131'] = self.article.volume_suppl
            self._metadata['132'] = self.article.number_suppl
        epub_date = self.article.raw_pubdate_pubtype_epub or self.article.raw_pubdate_datetype_pub
        if epub_date:
            self._metadata['223'] = article_utils.format_dateiso(epub_date)

        self._metadata['265'] = self.article.publication_dates

        self._metadata['58'] = self.article.funding_source
        self._metadata['591'] = [{'_': item for item in self.article.principal_award_recipient}]
        self._metadata['591'] += [{'n': item for item in self.article.principal_investigator}]
        self._metadata['60'] = self.article.award_id
        self._metadata['102'] = self.article.funding_statement

        #self._metadata['65'] = article_utils.format_dateiso(self.article.issue_pub_date)

        self._metadata['14'] = {}
        self._metadata['14']['f'] = self.article.fpage
        self._metadata['14']['s'] = self.article.fpage_seq
        self._metadata['14']['l'] = self.article.lpage
        self._metadata['14']['e'] = self.article.elocation_id

        self._metadata['70'] = format_affiliations(self.article.affiliations)
        self._metadata['240'] = format_normalized_affiliations(self.article.affiliations)
        #CT^uhttp://www.clinicaltrials.gov/ct2/show/NCT01358773^aNCT01358773
        self._metadata['770'] = {'u': self.article.clinical_trial_url}
        self._metadata['72'] = str(0 if self.article.total_of_references is None else self.article.total_of_references)
        #self._metadata['901'] = str(0 if self.article.total_of_tables is None else self.article.total_of_tables)
        #self._metadata['902'] = str(0 if self.article.total_of_figures is None else self.article.total_of_figures)

        self._metadata['83'] = []
        for item in self.article.abstracts:
            self._metadata['83'].append({'l': item.language, 'a': item.text})

        self._metadata['112'] = self.article.received_dateiso
        self._metadata['114'] = self.article.accepted_dateiso

    @property
    def references(self):
        records_c = []
        for ref_xml in self.article.references_xml:
            item = ref_xml.reference
            rec_c = {}
            rec_c['865'] = self._metadata.get('65')
            rec_c['71'] = item.publication_type

            if item.article_title or item.chapter_title:
                rec_c['12'] = {'_': item.article_title or item.chapter_title, 'l': item.language}
            if item.article_title is not None:
                rec_c['30'] = item.source
            else:
                rec_c['18'] = {}
                rec_c['18']['_'] = item.source
                rec_c['18']['l'] = item.language
            #rec_c['40'] = item.language
            rec_c['10'] = []
            rec_c['11'] = []
            rec_c['16'] = []
            rec_c['17'] = []

            grp_idx = 0
            etals = []
            for grptype, grp, etal in item.person_group_xml_items:
                is_analytic = (grp_idx == 0) and (item.article_title is not None or item.chapter_title is not None)

                grp_idx += 1
                etals.append(etal)
                for contrib_xml in grp:
                    author = contrib_xml.contrib()
                    field = author_tag(isinstance(author, PersonAuthor), is_analytic)
                    a = None
                    if isinstance(author, PersonAuthor):
                        a = {}
                        a['n'] = author.fname
                        a['s'] = author.surname
                        if author.suffix is not None:
                            if a['s'] is None:
                                a['s'] = ''
                            if author.suffix != '':
                                a['s'] += ' ' + author.suffix
                        #a['z'] = author.suffix
                        a['r'] = attributes.normalize_role(author.role)
                    elif isinstance(author, CorpAuthor):
                        # collab
                        a = author.collab
                    elif isinstance(author, AnonymousAuthor):
                        # collab
                        a = author.fullname
                    if a is not None:
                        rec_c[field].append(a)

            rec_c['31'] = item.volume
            rec_c['32'] = {}
            rec_c['32']['_'] = item.issue
            rec_c['32']['s'] = item.supplement
            rec_c['63'] = item.edition
            rec_c['95'] = item.version
            rec_c['64'] = item.year
            if item.formatted_year is not None:
                y = item.formatted_year
                if y.isdigit() and len(y) == 8:
                    rec_c['65'] = y
                else:
                    y = y[0:4]
                    if y.isdigit():
                        rec_c['65'] = y + '0000'
            rec_c['66'] = item.publisher_loc
            rec_c['62'] = item.publisher_name
            rec_c['514'] = {'f': item.fpage, 'l': item.lpage, 'r': item.page_range, 'e': item.elocation_id}

            if item.fpage is not None or item.lpage is not None:
                rec_c['14'] = article_utils.display_pages(item.fpage, item.lpage)
            elif item.page_range is not None:
                rec_c['14'] = item.page_range
            elif item.elocation_id is not None:
                rec_c['14'] = item.elocation_id
            if item.size:
                rec_c['20'] = {}
                rec_c['20']['_'] = item.size['size']
                rec_c['20']['u'] = item.size['units']
            rec_c['118'] = item.label
            rec_c['810'] = etals[0] if len(etals) > 0 else None
            rec_c['37'] = item.ext_link

            rec_c['109'] = item.cited_date
            rec_c['61'] = item.notes if item.notes else item.comments
            rec_c['237'] = item.doi
            rec_c['238'] = item.pmid
            rec_c['239'] = item.pmcid
            rec_c['53'] = item.conference_name
            rec_c['56'] = item.conference_location
            rec_c['54'] = item.conference_date

            rec_c['51'] = item.degree
            records_c.append(rec_c)
        return records_c

    def outline(self, total_of_records):
        rec_o = {}
        d, t = utils.now()
        rec_o['91'] = d
        rec_o['92'] = t
        rec_o['93'] = d or self.article.creation_date
        rec_o['703'] = total_of_records
        return rec_o

    @property
    def records(self):
        r = []
        self.fix_issue_data()
        rec = self.outline(str(4 + len(self.references)))
        rec.update(self.common_data)
        rec.update(self.record_info('1', 'o', '1', '1'))
        r.append(rec)

        rec = {}
        rec.update(self.common_data)
        rec.update(self.metadata)
        rec.update(self.record_info('2', 'h', '1', '1'))
        r.append(rec)

        rec = {}
        rec.update(self.common_data)
        rec.update(self.metadata)
        rec.update(self.record_info('3', 'f', '1', '1'))
        r.append(rec)

        rec = {}
        rec.update(self.common_data)
        rec.update(self.metadata)
        rec.update(self.record_info('4', 'l', '1', '1'))
        r.append(rec)

        c_total = str(len(self.references))
        c_index = 0
        k = 4
        for item in self.references:
            c_index += 1
            k += 1
            rec = item
            rec.update(self.common_data)
            rec.update(self.record_info(str(k), 'c', str(c_index), c_total))
            r.append(rec)
        return r

    def set_common_data(self, xml_name, issue_folder, relative_xml_filename):
        r = {}
        r['2'] = xml_name
        r['4'] = issue_folder
        r['702'] = relative_xml_filename
        r['705'] = 'S'
        self.common_data = r

    def record_info(self, record_index, record_name, record_name_index, record_name_total):
        r = {}
        r['706'] = record_name
        r['700'] = record_index # starts with 0
        r['701'] = record_name_index # starts with 1
        r['708'] = record_name_total
        # r.update(dict)
        return r


class RegisteredTitle(object):

    def __init__(self, record):
        self.record = record
        self._issns = title_issns(record)

    @property
    def acron(self):
        if self.record is not None:
            return self.record.get('68', '')

    @property
    def journal_id_nlm_ta(self):
        if self.record is not None:
            return self.record.get('421')

    @property
    def license(self):
        if self.record is not None:
            return self.record.get('541')

    @property
    def print_issn(self):
        if self._issns is None:
            self._issns = title_issns(self.record)
        return self._issns.get('ppub')

    @property
    def e_issn(self):
        if self._issns is None:
            self._issns = title_issns(self.record)
        return self._issns.get('epub')

    @property
    def abbrev_title(self):
        if self.record is not None:
            return self.record.get('30', '').lower()

    @property
    def publisher_name(self):
        if self.record is not None:
            return self.record.get('480')

    @property
    def issn_id(self):
        if self.record is not None:
            return self.record.get('400')

    @property
    def frequency(self):
        if self.record is not None:
            return FREQ.get(self.record.get('380'), "None")


class IssueModels(object):

    def __init__(self, record):
        self.record = record
        self._issue = None
        self.seccode_items = {}
        self.sectitle_items = {}

    @property
    def sections(self):
        v49 = self.record.get('49', [])
        if isinstance(v49, dict):
            v49 = [v49]
        return v49

    @property
    def section_titles(self):
        return [sec.get('t') for sec in self.sections]

    def most_similar_section_code(self, section_title, acceptable_result=0.85):
        items = [sec.get('t', '') for sec in self.sections]
        most_similar = utils.similarity(items, section_title, acceptable_result)
        ratio, similar_list = utils.most_similar(most_similar)
        seccode = None
        similar = None
        if similar_list is not None:
            for sec in self.sections:
                if sec.get('t') in similar_list:
                    seccode = sec.get('c')
                    similar = sec.get('t')
                    break
        return (seccode, ratio, similar)

    @property
    def issue(self):
        if self._issue is None:
            self._issue = self.__issue(self.record)
        return self._issue

    def __issue(self, record):
        acron = record.get('930').lower()
        dateiso = record.get('65', '')
        volume = record.get('31')
        volume_suppl = record.get('131')
        number = record.get('32')
        number_suppl = record.get('132')
        compl = record.get('41')

        i = Issue(acron, volume, number, dateiso, volume_suppl, number_suppl, compl)

        i.issn_id = record.get('35')
        i.journal_title = record.get('130')
        i.journal_id_nlm_ta = record.get('421')
        i.journal_id_publisher_id = record.get('930').lower()
        i.journal_issns = issue_issns(record)
        i.publisher_name = record.get('62', record.get('480'))
        if isinstance(i.publisher_name, list):
            i.publisher_name = '; '.join(i.publisher_name)
        i.license = record.get('541')
        return i

    def complete_issue_info(self, registered_title):
        if self._issue is not None:
            unknown_issn = self._issue.journal_issns.get('UNKNOWN_ISSN_TYPE')
            if unknown_issn is not None and registered_title._issns is not None:
                if registered_title._issns.get('UNKNOWN_ISSN_TYPE') is None:
                    for k, v in registered_title._issns.items():
                        if v == unknown_issn:
                            self._issue.journal_issns[k] = v
                        if 'UNKNOWN_ISSN_TYPE' in self._issue.journal_issns.keys():
                            del self._issue.journal_issns['UNKNOWN_ISSN_TYPE']
            if self._issue.journal_id_nlm_ta is None:
                self._issue.journal_id_nlm_ta = registered_title.journal_id_nlm_ta
            if self._issue.license is None:
                self._issue.license = registered_title.license

    def validate_article_issue_data(self, article, is_rolling_pass=False):
        results = []
        section_code = None
        if article.tree is not None:
            validations = []
            validations.append((_('journal title'), article.journal_title, self.issue.journal_title, validation_status.STATUS_BLOCKING_ERROR))
            validations.append((_('issue label'), article.issue_label, self.issue.issue_label, validation_status.STATUS_BLOCKING_ERROR))

            labels = [_('journal-id (nlm-ta)'), _('journal e-ISSN'), _('journal print ISSN'), _('issue year')]
            article_items = [article.journal_id_nlm_ta, article.e_issn, article.print_issn]
            issue_items = [self.issue.journal_id_nlm_ta, self.issue.e_issn, self.issue.print_issn]

            if article.expected_pubdate:
                a_year = (article.expected_pubdate or {}).get('year', '')
                i_year = (self.issue.dateiso or ' '*4)[:4].strip()
                article_items.append(a_year)
                issue_items.append(i_year)

            for label, article_data, issue_data in zip(labels, article_items, issue_items):
                if article_data is not None:
                    validations.append((label, article_data, issue_data, validation_status.STATUS_BLOCKING_ERROR))

            # check issue data
            for label, article_data, issue_data, status in validations:
                if article_data != issue_data:
                    error = True
                    if issue_data is None:
                        status = validation_status.STATUS_WARNING
                    elif label == _('journal title'):
                        if (article_data or '').strip() == issue_data.strip():
                            error = False
                        elif (article.is_ahead or is_rolling_pass) and (article_data.startswith(issue_data) or issue_data.startswith(article_data)):
                            error = False
                    if error is True:
                        _msg = _('{label}: "{value1}" ({label1}) and "{value2}" ({label2}) do not match. ').format(label=label, value1=article_data, label1=_('article'), value2=issue_data, label2=_('issue'))
                        results.append((label, status, _msg))

            validations = []
            validations.append(('publisher', article.publisher_name, self.issue.publisher_name, validation_status.STATUS_ERROR))
            for label, article_data, issue_data, status in validations:
                if utils.how_similar(article_data, issue_data) < 0.8:
                    if article_data not in issue_data:
                        _msg = _('{label}: "{value1}" ({label1}) and "{value2}" ({label2}) do not match. ').format(label=label, value1=article_data, label1=_('article'), value2=issue_data, label2=_('issue'))
                        results.append((label, status, _msg))

            # license
            article_license_code_and_versions = ' | '.join(article.article_license_code_and_versions)
            if self.issue.license is None:
                results.append(('license', validation_status.STATUS_WARNING, _('Unable to identify {item}').format(item=_('issue license'))))
            elif article_license_code_and_versions is not None:
                if self.issue.license.lower() not in article_license_code_and_versions:
                    _msg = _('{label}: "{value1}" ({label1}) and "{value2}" ({label2}) do not match. ').format(label=label, value1=article_license_code_and_versions, label1=_('article'), value2=self.issue.license, label2=_('issue'))
                    results.append(('license', validation_status.STATUS_ERROR, _msg))

            # section
            article_sectitle = None
            article_seccode = None
            fixed_sectitle = None

            if len(self.section_titles) == 0:
                if article.toc_section is not None:
                    results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('Issue has no table of contents sections. ')))
            else:
                if article.toc_section is None:
                    results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('Article has no subject. ') + _('Expected values: {expected}. ').format(expected=_(' or ').join(self.section_titles))))
                else:
                    for name in article.toc_sections:
                        if name in self.seccode_items.keys():
                            article_seccode = self.seccode_items.get(name)
                            article_sectitle = self.sectitle_items.get(name)
                            break
                    if article_seccode is None:
                        rate = 0
                        article_section_titles = _(' or ').join(article.toc_sections)
                        for a_section in article.toc_sections:
                            section_code, matched_rate, section_title = self.most_similar_section_code(a_section)
                            if matched_rate == 1:
                                rate = matched_rate
                                article_seccode = section_code
                                article_sectitle = section_title
                                break
                            elif section_code is not None:
                                if matched_rate > rate:
                                    rate = matched_rate
                                    article_seccode = section_code
                                    article_sectitle = section_title
                                    fixed_sectitle = section_title
                    if article_seccode is None:
                        results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('{value} is a invalid value for {label}. ').format(value=article_section_titles, label=_('table of contents section'))))
                    if fixed_sectitle is not None:
                        results.append((_('table of contents section'), validation_status.STATUS_WARNING, _('{incorrect} was changed to {fixed}. ').format(incorrect=article_section_titles, fixed=fixed_sectitle)))
                    results.append((_('table of contents section'), validation_status.STATUS_INFO, _('Expected values: {expected}. ').format(expected=' | '.join(self.section_titles))))
                    if article_seccode is not None:
                        for name in article.toc_sections:
                            self.seccode_items[name] = article_seccode
                            self.sectitle_items[name] = name

            # @article-type
            #_sectitle = article_section if fixed_sectitle is None else fixed_sectitle
            if article_sectitle is not None:
                results.extend(attributes.validate_article_type_and_section(article.article_type, article_sectitle, len(article.abstracts) > 0))
            article.section_code = article_seccode

        return html_reports.tag('div', article_data_reports.validations_table(results))


class IssueArticlesRecords(object):

    def __init__(self, records):
        self.records = records

    def articles(self):
        i_record = None

        record_types = list(set([record.get('706') for record in self.records]))
        articles_records = {}
        for record in self.records:
            if record.get('706') == 'i':
                i_record = record
            elif record.get('706') == 'o':
                # new article
                xml_name = record.get('2')
                if xml_name.endswith('.xml'):
                    xml_name = xml_name[0:-4]
                articles_records[xml_name] = []
                articles_records[xml_name].append(record)
            elif record.get('706') == 'h':
                if 'o' not in record_types:
                    xml_name = record.get('2')
                    if xml_name.endswith('.xml'):
                        xml_name = xml_name[0:-4]
                    articles_records[xml_name] = []
                articles_records[xml_name].append(record)

        items = {}
        for xml_name, records in articles_records.items():
            if len(records) > 1:
                a = RegisteredArticle(records, i_record)
                items[a.xml_name] = a
        return (i_record, items)


class ArticlesManager(object):

    def __init__(self, db_isis, issue_files):
        self.issue_files = issue_files
        self.base_manager = BaseManager(db_isis, issue_files)
        self.ex_aop_manager = None
        self.aop_db_manager = AopManager(db_isis, issue_files.journal_files)
        self.articles_conversion_status = {}
        self.articles_aop_status = {}
        self.articles_aop_exclusion_status = {}
        self.articles_conversion_messages = {}
        self.aop_pdf_replacements = {}

        if self.issue_files.is_aop:
            self.ex_aop_manager = BaseManager(db_isis, serial.IssueFiles(issue_files.journal_files, 'ex-' + issue_files.issue_folder))

    @property
    def serial_path(self):
        return self.issue_files.journal_files.serial_path

    @property
    def registered_articles(self):
        r = {}
        if self.ex_aop_manager is not None:
            r = self.ex_aop_manager.registered_articles
        r.update(self.base_manager.registered_articles)
        return r

    def exclude_articles(self, excluded_orders):
        return self.base_manager.exclude_articles(excluded_orders)

    def get_valid_aop(self, article):
        valid_aop, aop_status, messages = self.aop_db_manager.get_validated_aop(article)
        self.xc_messages.extend(messages)
        if valid_aop is not None:
            article.registered_aop_pid = valid_aop.pid
        return (aop_status, valid_aop)

    def exclude_aop(self, valid_aop):
        is_excluded_aop, messages, aop_issue_folder_name = self.aop_db_manager.manage_ex_aop(valid_aop)

        if valid_aop.is_ex_aop and is_excluded_aop is False:
            self.xc_messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + _('{item} is already excluded. ').format(item='ex aop: ' + valid_aop.order)))
            is_excluded_aop = True
        elif is_excluded_aop is True:
            self.xc_messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + _('Excluded {item}').format(item='ex aop: ' + valid_aop.order)))
        else:
            self.xc_messages.append(html_reports.p_message(validation_status.STATUS_ERROR + ': ' + _('Unable to exclude {item}. ').format(item='ex aop: ' + valid_aop.order)))
            if messages is not None:
                self.xc_messages.extend(messages)
        return is_excluded_aop, aop_issue_folder_name

    def convert_article(self, article, i_record, xml_name):
        self.xc_messages = []
        excluded_aop = None
        aop_status = None
        valid_aop = None
        if not article.is_ahead:
            aop_status, valid_aop = self.get_valid_aop(article)
        id_created = self.base_manager.save_article(article, i_record)
        article_converted = id_created
        if id_created is True:
            self.xc_messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + _('created/updated {order}.id').format(order=article.order)))
            if valid_aop is not None:
                excluded_aop, aop_issue_folder_name = self.exclude_aop(valid_aop)
                if aop_issue_folder_name is not None:
                    self.aop_pdf_replacements[xml_name] = (self.issue_files.journal_files.acron + '/' + aop_issue_folder_name, valid_aop.xml_name)

                article_converted = excluded_aop
        else:
            self.xc_messages.append(html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to create/update {order}.id').format(order=article.order)))
        self.articles_conversion_status[xml_name] = article_converted
        self.articles_aop_exclusion_status[xml_name] = excluded_aop
        self.articles_aop_status[xml_name] = aop_status
        self.articles_conversion_messages[xml_name] = ''.join(self.xc_messages)

    @property
    def db_conversion_status(self):
        status = {}
        status['converted'] = [xml_name for xml_name, result in self.articles_conversion_status.items() if result is True]
        status['not converted'] = [xml_name for xml_name, result in self.articles_conversion_status.items() if result is False]
        return status

    @property
    def db_aop_status(self):
        status_items = {}
        for name, status in self.articles_aop_exclusion_status.items():
            if status is not None:
                status = 'excluded ex-aop' if status is True else 'not excluded ex-aop'
                if status not in status_items.keys():
                    status_items[status] = []
                status_items[status].append((self.articles_orders[name], name))
        for name, status in self.articles_aop_status.items():
            if status is not None:
                if status not in status_items.keys():
                    status_items[status] = []
                status_items[status].append((self.articles_orders[name], name))
        for k in status_items.keys():
            status_items[k].sort()
        for k in status_items.keys():
            status_items[k] = [item[1] for item in status_items[k]]

        status_items['aop'] = self.aop_db_manager.still_aop_items()
        return status_items

    def convert_articles(self, acron_issue_label, articles, i_record, create_windows_base):
        self.articles_conversion_status = {}
        self.articles_aop_status = {}
        self.articles_aop_exclusion_status = {}
        self.articles_conversion_messages = {}
        self.articles_orders = {}
        scilista_items = []

        error = False

        for xml_name, article in articles.items():
            if not article.marked_to_delete:
                self.articles_orders[xml_name] = article.order
                self.convert_article(article, i_record, xml_name)
                if self.articles_conversion_status[xml_name] is False:
                    error = True

        if not error:
            q_registered = self.finish_conversion(i_record)
            encoding.debugging('convert_articles()', q_registered)
            converted = q_registered >= len(articles) and q_registered > 0
            if converted:
                if create_windows_base:
                    self.base_manager.generate_windows_version()

                scilista_items.extend(self.aop_db_manager.scilista_items)
                scilista_items.append(acron_issue_label)
        return scilista_items

    def finish_conversion(self, i_record):
        self.base_manager.finish_conversion(i_record)

        self.aop_db_manager.update_all_aop_db()
        return len(self.registered_articles)


class BaseManager(object):

    def __init__(self, db_isis, issue_files):
        self.db_isis = db_isis
        self.issue_files = issue_files
        self.articles_by_id = {}
        if self.issue_files.is_ex_aop:
            if not os.path.isfile(self.issue_files.base_filename):
                self.create_db()

    def restore_missing_id_file(self):
        for name, registered_article in self.registered_articles.items():
            article_files = serial.ArticleFiles(self.issue_files, registered_article.order, registered_article.xml_name)
            if not os.path.isfile(article_files.id_filename):
                self.db_isis.save_id(article_files.id_filename, registered_article.article_records)

    def registered_records(self):
        if not os.path.isfile(self.issue_files.base_filename):
            self.create_db()
        records = self.db_isis.get_records(self.issue_files.base)
        self.registered_i_record, self.registered_articles_records = IssueArticlesRecords(records).articles()

    def registered_xml_file(self, xml_name):
        f = self.issue_files.base_source_path + '/' + xml_name + '.xml'
        if not os.path.isfile(f):
            folders = []
            for folder in f.split('/'):
                if 'ahead' in folder:
                    folder = 'ex-' + folder
                folders.append(folder)
            f = '/'.join(folders)
        return f

    @property
    def registered_articles(self):
        self.registered_records()
        _registered_articles = {}
        for xml_name, registered_article in self.registered_articles_records.items():
            f = self.registered_xml_file(xml_name)
            if os.path.isfile(f):
                xml, e = xml_utils.load_xml(f)
            else:
                xml = None
            doc = Article(xml, xml_name)
            doc.pid = registered_article.pid
            doc.creation_date_display = registered_article.creation_date_display
            doc.creation_date = registered_article.creation_date
            doc.last_update_date = registered_article.last_update_date
            doc.last_update_display = registered_article.last_update_display
            doc.article_records = registered_article.article_records
            doc.is_ex_aop = self.issue_files.is_ex_aop
            doc.registered_scielo_id = registered_article.scielo_id
            if doc.article_id is not None:
                self.articles_by_id[doc.article_id] = xml_name
            _registered_articles[xml_name] = doc
        return _registered_articles

    def content_formatter(self, content):

        def reduce_content(content):
            languages = ['ru', 'zh', 'ch', 'cn', 'fr', 'es', ]
            alternative = [u'абстрактный доступен в Полный текст', u'抽象是在全文可', u'抽象是在全文可', u'抽象是在全文可', u'résumé est disponible dans le document', u'resumen está disponible en el texto completo']
            i = 0
            while (len(content) > 10000) and (i < len(languages)):
                content = remove_abstract(content, languages[i], alternative[i])
                i += 1
            return content

        def remove_abstract(content, language, alternative):
            new = content
            if len(content) > 10000:
                new = ''
                abstract = content.replace('!v', 'BREAK-ABSTRACT!v')
                for a in abstract.split('BREAK-ABSTRACT'):
                    l = '^l' + language
                    if a.startswith('!v083') and l in a:
                        new += '!v083!^a' + alternative + l + '\n'
                    else:
                        new += a
            return new

        if '!v706!f' in content:
            content = content.replace('<italic>', '<em>')
            content = content.replace('</italic>', '</em>')
            content = content.replace('<bold>', '<strong>')
            content = content.replace('</bold>', '</strong>')
        elif '!v706!c' in content or '!v706!h' in content:
            content = xml_utils.remove_tags(content)
        if len(content) > 10000:
            content = reduce_content(content)
        return content

    def create_db(self):
        if os.path.isfile(self.issue_files.id_filename):
            self.db_isis.save_id_records(self.issue_files.id_filename, self.issue_files.base)
            for f in os.listdir(self.issue_files.id_path):
                if f == '00000.id':
                    fs_utils.delete_file_or_folder(self.issue_files.id_path + '/' + f)
                if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                    self.db_isis.append_id_records(self.issue_files.id_path + '/' + f, self.issue_files.base)
        #self.reset_registered_records()

    def article_records(self, i_record, article, article_files):
        _article_records = None
        if article.order != '00000':
            _article_records = ArticleRecords(article, i_record, article_files)
        return _article_records

    def create_issue_id_file(self, i_record):
        self.db_isis.save_id(self.issue_files.id_filename, [i_record])

    def create_article_id_file(self, article_records, article_files):
        saved = False
        previous = False
        if not os.path.isdir(article_files.issue_files.id_path):
            os.makedirs(article_files.issue_files.id_path)
        if not os.path.isdir(article_files.issue_files.base_path):
            os.makedirs(article_files.issue_files.base_path)

        if article_records is not None:
            if os.path.isfile(article_files.id_filename):
                try:
                    fs_utils.delete_file_or_folder(article_files.id_filename)
                except:
                    encoding.display_message(_('Unable to exclude {item}. ').format(item=article_files.id_filename))
            previous = os.path.isfile(article_files.id_filename)

            self.db_isis.save_id(article_files.id_filename, article_records.records, self.content_formatter)
            saved = os.path.isfile(article_files.id_filename)
        return saved and not previous

    def save_article(self, article, i_record):
        article_files = serial.ArticleFiles(self.issue_files, article.order, article.xml_name)
        article_records = self.article_records(i_record, article, article_files)
        return self.create_article_id_file(article_records, article_files)

    def exclude_articles(self, excluded_orders):
        messages = []
        if len(excluded_orders) > 0:
            not_excluded_items = self.issue_files.delete_id_files(excluded_orders)
            if len(not_excluded_items) == 0:
                messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + _('Excluded: ') + html_reports.format_html_data(excluded_orders)))
            else:
                messages.append(html_reports.p_message(validation_status.STATUS_ERROR + ': ' + _('Exclude: ') + html_reports.format_html_data(excluded_orders)))
                messages.append(html_reports.p_message(validation_status.STATUS_ERROR + ': ' + _('Unable to exclude {item}. ').format(item=', '.join(not_excluded_items))))
        return ''.join(messages)

    def finish_conversion(self, i_record):
        self.create_issue_id_file(i_record)
        self.create_db()

    def generate_windows_version(self):
        if not os.path.isdir(self.issue_files.windows_base_path):
            os.makedirs(self.issue_files.windows_base_path)
        self.db_isis.cisis.mst2iso(self.issue_files.base, self.issue_files.windows_base + '.iso')
        self.db_isis.cisis.crunchmf(self.issue_files.base, self.issue_files.windows_base)


class AopManager(object):

    def __init__(self, db_isis, journal_files):
        self.db_isis = db_isis
        self.journal_files = journal_files
        self.xmlname_indexed_by_issueid_and_order = {}
        self.xmlname_indexed_by_article_id = {}
        self.issueid_indexed_by_xmlname = {}
        self.updated_issue_bases = []
        self.setup()

    def journal_has_aop(self):
        return len(self.xmlname_indexed_by_issueid_and_order) > 0

    def journal_publishes_aop(self):
        return self.journal_files.publishes_aop()

    def setup(self):
        self.load_aop_db_items()
        self.load_ex_aop_db_items()

    def load_aop_db_items(self):
        self.aop_db_items = {}
        for name, issue_files in self.journal_files.aop_issue_files.items():
            self.aop_db_items[issue_files.issue_folder] = BaseManager(self.db_isis, issue_files)
            for xml_name, registered in self.aop_db_items[issue_files.issue_folder].registered_articles.items():
                if registered.article_id is not None:
                    self.xmlname_indexed_by_article_id[registered.article_id] = registered.xml_name
                self.xmlname_indexed_by_issueid_and_order[issue_files.issue_folder + '|' + registered.order] = registered.xml_name
                self.issueid_indexed_by_xmlname[xml_name] = issue_files.issue_folder

    def load_ex_aop_db_items(self):
        self.ex_aop_db_items = {}
        for name, issue_files in self.journal_files.ex_aop_issues_files.items():
            self.ex_aop_db_items[issue_files.issue_folder] = BaseManager(self.db_isis, issue_files)
            for xml_name, registered in self.ex_aop_db_items[issue_files.issue_folder].registered_articles.items():
                if registered.article_id is not None:
                    self.xmlname_indexed_by_article_id[registered.article_id] = registered.xml_name
                if xml_name not in self.issueid_indexed_by_xmlname.keys():
                    self.xmlname_indexed_by_issueid_and_order[issue_files.issue_folder + '|' + registered.order] = registered.xml_name
                    self.issueid_indexed_by_xmlname[xml_name] = issue_files.issue_folder

    def get_aop_by_article_id(self, article_id):
        xml_name = self.xmlname_indexed_by_article_id.get(article_id.lower())
        if xml_name is not None:
            issueid = self.issueid_indexed_by_xmlname[xml_name]
            found_issue = self.aop_db_items.get(issueid, self.ex_aop_db_items.get(issueid))
            if found_issue is not None:
                found = found_issue.registered_articles.get(xml_name)
            return found

    def get_aop_by_xmlname(self, xml_name):
        issueid = self.issueid_indexed_by_xmlname.get(xml_name)
        if issueid is not None:
            return self.aop_db_items.get(issueid, self.ex_aop_db_items.get(issueid)).registered_articles.get(xml_name)

    def bkp_still_aop_items(self):
        articles = []
        for issue_id in sorted(self.aop_db_items.keys()):
            items = []
            for xml_name, article in self.aop_db_items[issue_id].registered_articles.items():
                items.append((article.order, xml_name))
            items.sort()

            for order, xml_name in items:
                #articles.append((issue_id, xml_name, self.aop_db_items[issue_id].registered_articles[xml_name]))
                if self.aop_db_items[issue_id].registered_articles.get(xml_name) is not None:
                    articles.append((issue_id, xml_name, self.aop_db_items[issue_id].registered_articles[xml_name]))
                # else:
                #    print(('still_aop_items', issue_id, xml_name))
        return articles

    def still_aop_items(self):
        articles = []
        for issue_id in sorted(self.aop_db_items.keys()):
            items = {(article.order, xml_name): article for xml_name, article in self.aop_db_items[issue_id].registered_articles.items()}
            for key in sorted(items.keys()):
                articles.append((issue_id, key[1], items.get(key)))
                # print(('still_aop_items', issue_id, key[1]))
        return articles

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def find_aop(self, article_id, xml_name):
        aop = None
        if article_id is not None:
            aop = self.get_aop_by_article_id(article_id)
        if aop is None:
            aop = self.get_aop_by_xmlname(xml_name)
        return aop

    def get_validated_aop(self, article):
        found_aop = None
        status = 'regular article'
        messages = []
        if self.journal_publishes_aop():
            found_aop = self.find_aop(article.article_id, article.xml_name)
            if found_aop is not None:
                # ex aop ou current aop
                status = self.compare_article_and_aop(article, found_aop)
                messages.append(self.check_aop_message(article, found_aop, status))
                if status not in ['matched aop', 'partially matched aop']:
                    found_aop = None
        #status = (status in ['matched aop', 'partially matched aop', 'regular article'])
        return (found_aop, status, messages)

    def compare_article_and_aop(self, article, aop):
        rate = self.similarity_rate(article, aop)
        rate = self.is_acceptable_rate(rate, 80)
        if rate > 0:
            if aop.pid is None:
                status = 'aop missing PID'
            else:
                status = 'matched aop'
                if rate != 1:
                    status = 'partially matched aop'
        else:
            status = 'unmatched aop'
        return status

    def is_acceptable_rate(self, rate, min_score):
        return rate if rate >= min_score else 0

    def similarity_rate(self, article, aop):
        r = 0
        if aop is not None:
            if article.article_type == 'correction':
                if article.body_words is not None and aop.body_words is not None:
                    r += utils.how_similar(article.body_words[0:300], aop.body_words[0:300])
                    r = r * 100
                else:
                    r = 1
            else:
                r += utils.how_similar(article.title, aop.title)
                article_authors = sorted([contrib.fullname for contrib in article.article_contrib_items])
                aop_authors = sorted([contrib.fullname for contrib in aop.article_contrib_items])
                r += utils.how_similar(', '.join(article_authors), ', '.join(aop_authors))
                r = (r * 100) / 2
        return r

    def check_aop_message(self, article, aop, status):
        label = 'body' if article.article_type == 'correction' else _('title/author')
        data = []
        msg_list = []

        msg_list.append(_('Checking if {label} was published ahead of print').format(label=article.xml_name))
        if article.article_id is not None:
            msg_list.append(_('Checking if {label} was published ahead of print').format(label=article.article_id))

        if status == 'regular article':
            msg_list.append(validation_status.STATUS_WARNING + ': ' + _('Not found an "aop version" of this document. '))
        else:
            msg_list.append(validation_status.STATUS_INFO + ': ' + _('Found: "aop version"'))
            if status == 'partially matched aop':
                msg_list.append(validation_status.STATUS_INFO + ': ' + _('the {data} of article and its "aop version" are similar. ').format(data=label))
            elif status == 'aop missing PID':
                msg_list.append(validation_status.STATUS_ERROR + ': ' + _('the "aop version" has no PID'))
            elif status == 'unmatched aop':
                status = 'unmatched aop'
                msg_list.append(validation_status.STATUS_FATAL_ERROR + ': ' + _('the {data} of article and "aop version" are different. ').format(data=label))

            if article.article_type == 'correction':
                t = '' if article.body_words is None else article.body_words[0:300]
                data.append(_('doc body') + ':' + html_reports.format_html_data(t))
                t = '' if aop.body_words is None else aop.body_words[0:300]
                data.append(_('aop body') + ':' + html_reports.format_html_data(t))
            else:
                t = '' if article.title is None else article.title
                data.append(_('doc title') + ':' + html_reports.format_html_data(t))
                t = '' if aop.title is None else aop.title
                data.append(_('aop title') + ':' + html_reports.format_html_data(t))

                article_authors = [contrib.fullname for contrib in article.article_contrib_items]
                aop_authors = [contrib.fullname for contrib in aop.article_contrib_items]
                if len(article_authors) > 0:
                    data.append(_('doc authors') + ':' + html_reports.format_html_data(article_authors))
                if len(aop_authors) > 0:
                    data.append(_('aop authors') + ':' + html_reports.format_html_data(aop_authors))
        msg = ''
        msg += html_reports.tag('h5', _('Checking existence of aop version'))
        msg += ''.join([html_reports.p_message(item, False) for item in msg_list])
        msg += ''.join([html_reports.p_message(item, False) for item in data])
        return msg

    def mark_aop_as_deleted(self, aop):
        """
        Mark as deleted
        """
        if aop.article_id is not None:
            del self.xmlname_indexed_by_article_id[aop.article_id]
        issue_folder = self.issueid_indexed_by_xmlname[aop.xml_name]
        del self.issueid_indexed_by_xmlname[aop.xml_name]
        del self.xmlname_indexed_by_issueid_and_order[issue_folder + '|' + aop.order]

    def manage_ex_aop(self, aop):
        aop_issue_folder_name = None
        if aop.pid is not None:
            aop_issueid = self.issueid_indexed_by_xmlname[aop.xml_name]
            aop_issue_folder_name = aop_issueid
            if aop_issueid.startswith('ex-'):
                done = True
                aop_issue_folder_name = aop_issue_folder_name[3:]
                msg = [html_reports.p_message(validation_status.STATUS_INFO + ': ' + _('{item} is ex-aop').format(item=aop.xml_name))]
            else:
                done, msg = self.journal_files.archive_ex_aop_files(aop, aop_issueid)
                if done:
                    self.mark_aop_as_deleted(aop)
                    if aop_issueid not in self.updated_issue_bases:
                        self.updated_issue_bases.append(aop_issueid)
                    if 'ex-' + aop_issueid not in self.updated_issue_bases:
                        self.updated_issue_bases.append('ex-' + aop_issueid)
        if aop_issue_folder_name is not None:
            if aop_issue_folder_name not in self.updated_issue_bases:
                self.updated_issue_bases.append(aop_issue_folder_name)
        return (done, msg, aop_issue_folder_name)

    #aop_pdf_replacements
    @property
    def scilista_items(self):
        return [self.journal_files.acron + ' ' + base for base in self.updated_issue_bases if 'ex-' not in base]

    def update_all_aop_db(self):
        if len(self.updated_issue_bases) > 0:
            for issueid in self.updated_issue_bases:
                if issueid in self.aop_db_items.keys():
                    self.aop_db_items[issueid].create_db()
                elif issueid in self.ex_aop_db_items.keys():
                    self.ex_aop_db_items[issueid].create_db()


def format_affiliations(affiliations):
    affs = []
    for aff_xml in affiliations:
        item = aff_xml.aff
        a = {}
        a['l'] = item.label
        a['i'] = item.id
        a['e'] = item.email
        a['3'] = item.orgdiv3
        a['2'] = item.orgdiv2
        a['1'] = item.orgdiv1
        a['p'] = item.country
        a['c'] = item.city
        a['s'] = item.state
        a['_'] = item.orgname
        affs.append(a)
    return affs


def format_normalized_affiliations(affiliations):
    affs = []
    for affiliation in affiliations:
        aff = affiliation.aff
        if aff is not None:
            if aff.id is not None and aff.i_country is not None:
                a = {}
                a['i'] = aff.id
                a['p'] = aff.i_country
                affs.append(a)
    return affs


class DBManager(object):

    def __init__(self, db_isis, title_db_filenames, issue_db_filenames, serial_path):
        self.src_title_db_filename = title_db_filenames[0]
        self.title_db_filename = title_db_filenames[1]
        self.title_fst_filename = title_db_filenames[2]

        self.src_issue_db_filename = issue_db_filenames[0]
        self.issue_db_filename = issue_db_filenames[1]
        self.issue_fst_filename = issue_db_filenames[2]

        self.db_isis = db_isis
        self.serial_path = serial_path

    def update_db_copy(self, isis_db, isis_db_copy, fst_file):
        d = os.path.dirname(isis_db_copy)
        if not os.path.isdir(d):
            os.makedirs(d)
        if not os.path.isfile(isis_db_copy + '.fst'):
            shutil.copyfile(fst_file, isis_db_copy + '.fst')
        if fs_utils.read_file(fst_file) != fs_utils.read_file(isis_db_copy + '.fst'):
            shutil.copyfile(fst_file, isis_db_copy + '.fst')
        shutil.copyfile(isis_db + '.mst', isis_db_copy + '.mst')
        shutil.copyfile(isis_db + '.xrf', isis_db_copy + '.xrf')
        self.db_isis.update_indexes(isis_db_copy, isis_db_copy + '.fst')

    def search_journal_expr(self, pissn, eissn, journal_title):
        _expr = []
        if pissn is not None and len(pissn) == 9:
            _expr.append(pissn)
        if eissn is not None and len(eissn) == 9:
            _expr.append(eissn)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search_issue_expr(self, issue_id, pissn, eissn, acron=None):
        _expr = []
        if pissn is not None:
            _expr.append(pissn + issue_id)
        if eissn is not None:
            _expr.append(eissn + issue_id)
        if acron is not None:
            _expr.append(acron)
        _expr = [item for item in _expr if item != '' and not None]

        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def update_and_search(self, db, expr, source_db, fst_filename):
        result = []
        updated = False
        if os.path.isfile(db + '.mst'):
            d_copy = fs_utils.last_modified_datetime(db + '.mst')
            d_source = fs_utils.last_modified_datetime(source_db + '.mst')
            diff = d_source - d_copy
            updated = not (diff.days > 0 or (diff.days == 0 and diff.seconds > 0))

        if updated:
            result = self.db_isis.get_records(db, expr)
        if len(result) == 0:
            self.update_db_copy(source_db, db, fst_filename)
            result = self.db_isis.get_records(db, expr)
        return result[0] if len(result) > 0 else None

    def get_registered_data(self, journal_title, issue_label, p_issn, e_issn):
        issue_models = None
        msg = None
        acron_issue_label = 'unidentified issue'
        j = None
        j_data = None
        if issue_label is None:
            msg = _('Unable to identify the article\'s issue')
        else:
            i_record = self.find_i_record(issue_label, p_issn, e_issn)
            if i_record is None:
                acron_issue_label = 'not_registered issue'
                msg = _('Issue ') + issue_label + _(' is not registered in ') + self.issue_db_filename + _(' using ISSN: ') + _(' or ').join([i for i in [p_issn, e_issn] if i is not None]) + '.'
            else:
                issue_models = IssueModels(i_record)
                acron_issue_label = issue_models.issue.acron + ' ' + issue_models.issue.issue_label
                j_record = self.find_journal_record(journal_title, p_issn, e_issn)
                if j_record is None:
                    msg = _('Unable to get journal data') + ' ' + journal_title
                else:
                    t = RegisteredTitle(j_record)
                    j = Journal()
                    j.frequency = t.frequency
                    j.acron = t.acron
                    j.p_issn = t.print_issn
                    j.e_issn = t.e_issn
                    j.abbrev_title = t.abbrev_title
                    j.nlm_title = t.journal_id_nlm_ta
                    j.publisher_name = t.publisher_name
                    j.license = t.license
                    j.collection_acron = None
                    j.journal_title = journal_title
                    j.issn_id = t.issn_id
                    j_data = Journal()
                    j_data.acron = [t.acron]
                    j_data.frequency = [t.frequency]
                    j_data.p_issn = [t.print_issn]
                    j_data.e_issn = [t.e_issn]
                    j_data.abbrev_title = [t.abbrev_title]
                    j_data.nlm_title = [t.journal_id_nlm_ta]
                    j_data.publisher_name = [t.publisher_name]
                    if isinstance(t.publisher_name, list):
                        j_data.publisher_name = t.publisher_name
                    j_data.license = [t.license]
                    j_data.collection_acron = [None]
                    j_data.journal_title = [journal_title]
                    j_data.issn_id = [t.issn_id]
                    if (issue_models.issue.print_issn is None and issue_models.issue.e_issn is None) or issue_models.issue.license is None or issue_models.issue.journal_id_nlm_ta is None:
                        issue_models.complete_issue_info(t)
        if msg is not None:
            msg = html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + msg, False)
        return (acron_issue_label, issue_models, msg, j, j_data)

    def get_issue_files(self, issue_models):
        if issue_models is not None:
            journal_files = serial.JournalFiles(self.serial_path, issue_models.issue.acron)
            return serial.IssueFiles(journal_files, issue_models.issue.issue_label)

    def find_journal_record(self, journal_title, print_issn, e_issn):
        records = None
        expr = self.search_journal_expr(print_issn, e_issn, journal_title)
        if expr is not None:
            records = self.update_and_search(self.title_db_filename, expr, self.src_title_db_filename, self.title_fst_filename)
        return records

    def find_i_record(self, issue_label, print_issn, e_issn):
        records = None
        expr = self.search_issue_expr(issue_label, print_issn, e_issn)
        if expr is not None:
            records = self.update_and_search(self.issue_db_filename, expr, self.src_issue_db_filename, self.issue_fst_filename)
        return records


class JournalsList(object):

    def __init__(self, downloaded_journals_filename):
        self._journals = {}
        for row in fs_utils.read_file_lines(downloaded_journals_filename)[1:]:
            cols = row.split("\t")
            if len(cols) >= 10:
                item = [col.strip() for col in cols]
                j = Journal()
                j.collection_acron = item[0]
                j.collection_name = item[4]
                j.issn_id = item[1]
                j.p_issn = item[2]
                j.e_issn = item[3]
                j.acron = item[5]
                j.abbrev_title = item[6]
                j.journal_title = item[7]
                j.nlm_title = item[8]
                j.publisher_name = item[9]
                if len(item) == 12:
                    j.license = item[11]
                for issn in list(set([j.issn_id, j.p_issn, j.e_issn])):
                    if issn not in self._journals.keys():
                        self._journals[issn] = []
                    self._journals[issn].append(j)

    def get_journal_instances(self, p_issn, e_issn, journal_title):
        journal_instances = []
        for issn in [p_issn, e_issn]:
            if issn is not None:
                for j in self._journals.get(issn, []):
                    journal_instances.append(j)
        return journal_instances

    def get_journal_data(self, p_issn, e_issn, journal_title):
        journal = Journal()
        for issn in [p_issn, e_issn]:
            if issn is not None:
                for j in self._journals.get(issn, []):
                    journal.acron = update_list(journal.acron, j.acron)
                    journal.p_issn = update_list(journal.p_issn, j.p_issn)
                    journal.e_issn = update_list(journal.e_issn, j.e_issn)
                    journal.abbrev_title = update_list(journal.abbrev_title, j.abbrev_title)
                    journal.nlm_title = update_list(journal.nlm_title, j.nlm_title)
                    journal.publisher_name = update_list(journal.publisher_name, j.publisher_name)
                    journal.license = update_list(journal.license, j.license)
                    journal.collection_acron = update_list(journal.collection_acron, j.collection_acron)
                    journal.journal_title = update_list(journal.journal_title, j.journal_title)
                    journal.issn_id = update_list(journal.issn_id, j.issn_id)
        return journal

    def get_journal(self, p_issn, e_issn, journal_title):
        journal = Journal()
        for issn in [p_issn, e_issn]:
            if issn is not None:
                for j in self._journals.get(issn, []):
                    journal = j
                    break
        return journal


def update_list(l, value):
    if l is None:
        l = []
    if value is not None and value not in l and len(value) > 0:
        l.append(value)
    return l


class RegisteredIssuesManager(object):

    def __init__(self, db_manager, journals_list):
        self.db_manager = db_manager
        self.journals_list = journals_list

    def get_registered_issue_data(self, pkgissuedata, registered_issue):
        if self.db_manager is None:
            journals_list = self.journals_list
            pkgissuedata.journal = self.journals_list.get_journal(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
            pkgissuedata.journal_data = self.journals_list.get_journal_data(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
        else:
            registered_issue.acron_issue_label, registered_issue.issue_models, registered_issue.issue_error_msg, pkgissuedata.journal, pkgissuedata.journal_data = self.db_manager.get_registered_data(pkgissuedata.pkg_journal_title, pkgissuedata.pkg_issue_label, pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn)
            ign, pkgissuedata._issue_label = registered_issue.acron_issue_label.split(' ')
            if registered_issue.issue_error_msg is None:
                registered_issue.issue_files = self.db_manager.get_issue_files(registered_issue.issue_models)
                registered_issue.articles_db_manager = ArticlesManager(self.db_manager.db_isis, registered_issue.issue_files)
        return pkgissuedata
