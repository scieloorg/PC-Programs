# coding=utf-8

import os
import shutil
from datetime import datetime
import csv

from __init__ import _
import validation_status
import utils
import xml_utils
import fs_utils
from utils import how_similar
from article import Issue, PersonAuthor, Article, Journal
import attributes
from dbm_isis import IDFile
import article_utils
import serial_files
import pkg_reports
import institutions_service
import html_reports
import article_reports
import ws_requester


ISSN_TYPE_CONVERSION = {
    'ONLIN': 'epub',
    'PRINT': 'ppub',
    'epub': 'ONLIN',
    'ppub': 'PRINT',
}


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
        if not '130' in self._metadata.keys():
            self._metadata['130'] = self.article.journal_title
        if not '62' in self._metadata.keys():
            self._metadata['62'] = self.article.publisher_name
        if not '421' in self._metadata.keys():
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

        self._metadata['121'] = self.article.order
        self._metadata['881'] = self.article.previous_pid

        if self.article.is_ahead:
            self._metadata['32'] = 'ahead'
            self._metadata['223'] = self.article.ahpdate_dateiso
        else:
            self._metadata['31'] = self.article.volume
            self._metadata['32'] = self.article.number
            self._metadata['131'] = self.article.volume_suppl
            self._metadata['132'] = self.article.number_suppl
            self._metadata['223'] = self.article.article_pub_dateiso

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
        self._metadata['240'] = format_normalized_affiliations(self.article.normalized_affiliations)
        #CT^uhttp://www.clinicaltrials.gov/ct2/show/NCT01358773^aNCT01358773
        self._metadata['770'] = {'u': self.article.clinical_trial_url}
        self._metadata['72'] = str(0 if self.article.total_of_references is None else self.article.total_of_references)
        #self._metadata['901'] = str(0 if self.article.total_of_tables is None else self.article.total_of_tables)
        #self._metadata['902'] = str(0 if self.article.total_of_figures is None else self.article.total_of_figures)

        self._metadata['83'] = []
        for item in self.article.abstracts:
            self._metadata['83'].append({'l': item.language, 'a': item.text})

        self._metadata['112'] = article_utils.format_dateiso(self.article.received)
        self._metadata['114'] = article_utils.format_dateiso(self.article.accepted)

    @property
    def references(self):

        records_c = []
        for item in self.article.references:
            rec_c = {}
            rec_c['865'] = self._metadata.get('65')
            rec_c['71'] = item.publication_type

            if item.article_title is not None or item.chapter_title is not None:
                rec_c['12'] = {'_': item.article_title if item.article_title is not None else item.chapter_title, 'l': item.language}
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
            for grp in item.authors_by_group:
                is_analytic = (len(item.authors_by_group) > 1) and (grp_idx == 0) and (item.article_title is not None or item.chapter_title is not None)
                grp_idx += 1

                for author in grp:
                    field = author_tag(isinstance(author, PersonAuthor), is_analytic)
                    if isinstance(author, PersonAuthor):
                        a = {}
                        a['n'] = author.fname
                        a['s'] = author.surname
                        if author.suffix is not None:
                            if author.suffix != '':
                                a['s'] += ' ' + author.suffix
                        #a['z'] = author.suffix
                        a['r'] = attributes.normalize_role(author.role)
                    else:
                        # collab
                        a = author.collab
                    rec_c[field].append(a)
            rec_c['31'] = item.volume
            rec_c['32'] = {}
            rec_c['32']['_'] = item.issue
            rec_c['32']['s'] = item.supplement
            rec_c['63'] = item.edition
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
            rec_c['810'] = item.etal
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
        rec_o['93'] = d if self.article.creation_date is None else self.article.creation_date
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


class IssueModels(object):

    def __init__(self, record):
        self.record = record
        self._issue = None

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
            a_year = article.issue_pub_dateiso[0:4] if article.issue_pub_dateiso is not None else ''
            i_year = self.issue.dateiso[0:4] if self.issue.dateiso is not None else ''

            validations = []
            validations.append((_('journal title'), article.journal_title, self.issue.journal_title, validation_status.STATUS_BLOCKING_ERROR))
            validations.append((_('issue label'), article.issue_label, self.issue.issue_label, validation_status.STATUS_BLOCKING_ERROR))

            labels = [_('journal-id (nlm-ta)'), _('journal e-ISSN'), _('journal print ISSN'), _('issue year')]
            article_items = [article.journal_id_nlm_ta, article.e_issn, article.print_issn, a_year]
            issue_items = [self.issue.journal_id_nlm_ta, self.issue.e_issn, self.issue.print_issn, i_year]

            for label, article_data, issue_data in zip(labels, article_items, issue_items):
                if article_data is not None:
                    validations.append((label, article_data, issue_data, validation_status.STATUS_BLOCKING_ERROR))

            # check issue data
            for label, article_data, issue_data, status in validations:
                error = False
                if not article_data == issue_data:
                    error = True
                    if issue_data is None:
                        status = validation_status.STATUS_WARNING
                    _msg = _('{label}: {value1} ({label1}) and {value2} ({label2}) do not match. ').format(label=label, value1=article_data, label1=_('article'), value2=issue_data, label2=_('issue'))
                    results.append((label, status, _msg))

            validations = []
            validations.append(('publisher', article.publisher_name, self.issue.publisher_name, validation_status.STATUS_ERROR))
            for label, article_data, issue_data, status in validations:
                if utils.how_similar(article_data, issue_data) < 0.8:
                    _msg = _('{label}: {value1} ({label1}) and {value2} ({label2}) do not match. ').format(label=label, value1=article_data, label1=_('article'), value2=issue_data, label2=_('issue'))
                    results.append((label, status, _msg))

            # license
            article_license_code_and_versions = ' | '.join(article.article_license_code_and_versions)
            if self.issue.license is None:
                results.append(('license', validation_status.STATUS_WARNING, _('Unable to identify {item}').format(item=_('issue license'))))
            elif article_license_code_and_versions is not None:
                if not self.issue.license.lower() in article_license_code_and_versions:
                    _msg = _('{label}: {value1} ({label1}) and {value2} ({label2}) do not match. ').format(label=label, value1=article_license_code_and_versions, label1=_('article'), value2=self.issue.license, label2=_('issue'))
                    results.append(('license', validation_status.STATUS_ERROR, _msg))

            # section
            fixed_sectitle = None
            if len(self.section_titles) == 0:
                if article.toc_section is not None:
                    results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('Issue has no table of contents sections. ')))
            else:
                if article.toc_section is None:
                    results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('Article has no subject. ') + _('Expected values: {expected}. ').format(expected=_(' or ').join(self.section_titles))))
                else:
                    found = False
                    for article_section in article.toc_sections:
                        if article_section in self.section_titles:
                            found = True
                            break
                    if not found:
                        fixed_sectitle = None
                        for article_section in article.toc_sections:
                            section_code, matched_rate, fixed_sectitle = self.most_similar_section_code(article_section)
                            if matched_rate != 1:
                                if section_code is None:
                                    results.append((_('table of contents section'), validation_status.STATUS_ERROR, _('{value} is a invalid value for {label}. ').format(value=article_section, label=_(_('table of contents section')))))
                                else:
                                    results.append((_('table of contents section'), validation_status.STATUS_WARNING, _('{incorrect} was changed to {fixed}. ').format(incorrect=article_section, fixed=fixed_sectitle)))
                                    break
                            else:
                                break
                        results.append((_('table of contents section'), validation_status.STATUS_INFO, _('Expected values: {expected}. ').format(expected=' | '.join(self.section_titles))))

            # @article-type
            _sectitle = article_section if fixed_sectitle is None else fixed_sectitle
            if _sectitle is not None:
                for item in attributes.validate_article_type_and_section(article.article_type, _sectitle, len(article.abstracts) > 0):
                    results.append(item)
                article.section_code = section_code
        return (html_reports.tag('div', article_reports.validations_table(results)))


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
                if not 'o' in record_types:
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


class ArticlesDBManager(object):

    def __init__(self, db_isis, issue_files):
        self.db_isis = db_isis
        self.issue_files = issue_files
        self.aop_db_manager = None
        if self.issue_files.is_regular:
            self.aop_db_manager = AopDBManager(db_isis, self.issue_files.journal_files)
        self.articles_by_doi = {}

    def restore_missing_id_file(self):
        if self.registered_articles.items() is not None:
            for name, registered_article in self.registered_articles.items():
                article_files = serial_files.ArticleFiles(self.issue_files, registered_article.order, registered_article.xml_name)
                if not os.path.isfile(article_files.id_filename):
                    self.db_isis.save_id(article_files.id_filename, registered_article.article_records)

    def registered_records(self):
        records = self.db_isis.get_records(self.issue_files.base)
        self.registered_i_record, self.registered_articles_records = IssueArticlesRecords(records).articles()

    @property
    def registered_articles(self):
        print('*' * 100)
        print(utils.now()[0])
        print('=' * 100)
        
        _registered_articles = {}
        self.registered_records()
        for xml_name, registered_article in self.registered_articles_records.items():
            f = self.issue_files.base_source_path + '/' + xml_name + '.xml'
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
            if doc.doi is not None:
                self.articles_by_doi[doc.doi] = xml_name
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
            content = content.replace('<italic>', '')
            content = content.replace('</italic>', '')
            content = content.replace('<bold>', '')
            content = content.replace('</bold>', '')
            content = xml_utils.remove_tags(content)
        if len(content) > 10000:
            content = reduce_content(content)
        return content

    def create_db(self):
        if os.path.isfile(self.issue_files.id_filename):
            self.db_isis.save_id_records(self.issue_files.id_filename, self.issue_files.base)
            for f in os.listdir(self.issue_files.id_path):
                if f == '00000.id':
                    os.unlink(self.issue_files.id_path + '/' + f)
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
                    os.unlink(article_files.id_filename)
                except:
                    print(_('Unable to exclude {item}. ').format(item=article_files.id_filename))
            previous = os.path.isfile(article_files.id_filename)

            self.db_isis.save_id(article_files.id_filename, article_records.records, self.content_formatter)
            saved = os.path.isfile(article_files.id_filename)
        return saved and not previous

    def convert_article(self, article, i_record):
        xc_messages = []
        article_converted = True
        excluded_aop = None
        valid_aop = None
        aop_status = None
        if self.aop_db_manager is not None:
            valid_aop, aop_status, messages = self.aop_db_manager.get_validated_aop(article)
            xc_messages.extend(messages)
            if valid_aop is not None:
                article.registered_aop_pid = valid_aop.pid
        if article_converted is True:
            article_files = serial_files.ArticleFiles(self.issue_files, article.order, article.xml_name)
            article_records = self.article_records(i_record, article, article_files)
            id_created = self.create_article_id_file(article_records, article_files)
            if id_created is True:
                if valid_aop is not None:
                    excluded_aop, messages = self.aop_db_manager.manage_ex_aop(valid_aop)
                    if excluded_aop is True:
                        xc_messages.append(validation_status.STATUS_INFO + ': ' + _('Excluded {item}').format(item='ex aop: ' + valid_aop.order))
                    else:
                        xc_messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to exclude {item}. ').format(item='ex aop: ' + valid_aop.order))
                        if messages is not None:
                            xc_messages.extend(messages)
                    article_converted = id_created and excluded_aop
            else:
                xc_messages.append(validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to create/update {order}.id').format(order=article.order))
                article_converted = False
        if article_converted is True:
            xc_messages.append(validation_status.STATUS_INFO + ': ' + _('created/updated {order}.id').format(order=article.order))
        return (article_converted, excluded_aop, ''.join([html_reports.p_message(item) for item in xc_messages]), aop_status)

    def sort_articles_by_status(self):
        self.db_aop_status = {}
        self.db_conversion_status = {}
        self.db_conversion_status['converted'] = [xml_name for xml_name, result in self.articles_conversion_status.items() if result is True]
        self.db_conversion_status['not converted'] = [xml_name for xml_name, result in self.articles_conversion_status.items() if result is False]

        for name, status in self.articles_aop_exclusion_status.items():
            if status is not None:
                status = 'excluded ex-aop' if status is True else 'not excluded ex-aop'
                if not status in self.db_aop_status.keys():
                    self.db_aop_status[status] = []
                self.db_aop_status[status].append(name)
        for name, status in self.articles_aop_status.items():
            if status is not None:
                if not status in self.db_aop_status.keys():
                    self.db_aop_status[status] = []
                self.db_aop_status[status].append(name)
        self.db_aop_status['still aop'] = self.aop_db_manager.still_aop_items()

    def convert_articles(self, acron_issue_label, articles, i_record, create_windows_base):
        self.articles_conversion_status = {}
        self.articles_aop_status = {}
        self.articles_aop_exclusion_status = {}
        self.articles_conversion_messages = {}

        scilista_items = []

        error = False

        for xml_name, article in articles.items():
            article_converted, excluded_aop, messages, aop_status = self.convert_article(article, i_record)
            self.articles_conversion_status[xml_name] = article_converted
            self.articles_aop_exclusion_status[xml_name] = excluded_aop
            self.articles_aop_status[xml_name] = aop_status
            self.articles_conversion_messages[xml_name] = messages
            if article_converted is False:
                error = True

        self.sort_articles_by_status()

        if not error:
            q_registered = self.finish_conversion(i_record)
            converted = q_registered == len(articles)
            if converted:
                if create_windows_base:
                    self.generate_windows_version()

                if self.aop_db_manager is not None:
                    scilista_items.extend(self.aop_db_manager.changed_issues)
                scilista_items.append(acron_issue_label)

        return scilista_items

    def exclude_order_id_filenames(self, changed_orders, excluded_orders):
        messages = []
        x = [item[0] for item in changed_orders.values()] + excluded_orders.values()
        not_excluded_items = self.issue_files.delete_id_files(x)
        if len(not_excluded_items) > 0:
            if len(excluded_orders) > 0:
                messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + html_reports.format_html_data(excluded_orders)))
            if len(changed_orders) > 0:
                messages.append(html_reports.p_message(validation_status.STATUS_INFO + ': ' + html_reports.format_html_data(changed_orders)))
            messages.append(html_reports.p_message(validation_status.STATUS_ERROR + ': ' + _('Unable to exclude {item}. ').format(item=', '.join(not_excluded_items))))
        return ''.join(messages)

    def finish_conversion(self, i_record):
        self.create_issue_id_file(i_record)
        self.create_db()
        if self.aop_db_manager is not None:
            self.aop_db_manager.update_all_aop_db()
        return len(self.registered_articles)

    def generate_windows_version(self):
        if not os.path.isdir(self.issue_files.windows_base_path):
            os.makedirs(self.issue_files.windows_base_path)
        self.db_isis.cisis.mst2iso(self.issue_files.base, self.issue_files.windows_base + '.iso')
        self.db_isis.cisis.crunchmf(self.issue_files.base, self.issue_files.windows_base)


class AopDBManager(object):

    def __init__(self, db_isis, journal_files):
        self.db_isis = db_isis
        self.journal_files = journal_files

        self.xmlname_indexed_by_issueid_and_order = {}
        self.xmlname_indexed_by_doi = {}
        self.issueid_indexed_by_xmlname = {}

        self._aop_db_items = None
        self.changed_issues = []
        self.setup()

    def journal_has_aop(self):
        return len(self.xmlname_indexed_by_issueid_and_order) > 0

    def journal_publishes_aop(self):
        return self.journal_files.publishes_aop()

    def setup(self):
        self._aop_db_items = {}
        for name, aop_issue_files in self.journal_files.aop_issue_files.items():
            self._aop_db_items[aop_issue_files.issue_folder] = ArticlesDBManager(self.db_isis, aop_issue_files)

            for xml_name, registered_aop in self._aop_db_items[aop_issue_files.issue_folder].registered_articles.items():
                if registered_aop.doi is not None:
                    self.xmlname_indexed_by_doi[registered_aop.doi] = registered_aop.xml_name
                self.xmlname_indexed_by_issueid_and_order[aop_issue_files.issue_folder + '|' + registered_aop.order] = registered_aop.xml_name
                self.issueid_indexed_by_xmlname[xml_name] = aop_issue_files.issue_folder

    @property
    def aop_db_items(self):
        return self._aop_db_items

    def get_aop_by_doi(self, doi):
        xml_name = self.xmlname_indexed_by_doi[doi.lower()]
        issueid = self.issueid_indexed_by_xmlname[xml_name]
        return self._aop_db_items[issueid].registered_articles.get(xml_name)

    def get_aop_by_xmlname(self, xml_name):
        issueid = self.issueid_indexed_by_xmlname[xml_name]
        return self._aop_db_items[issueid].registered_articles.get(xml_name)

    def still_aop_items(self):
        r = []
        for k in sorted(self.xmlname_indexed_by_issueid_and_order.keys()):
            xml_name = self.xmlname_indexed_by_issueid_and_order[k]
            aop = self.get_aop_by_xmlname(xml_name)
            parts = [k, aop.order, aop.filename, aop.short_article_title()]
            r.append(' | '.join([item for item in parts if item is not None]))
        return sorted(r)

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def find_aop(self, doi, xml_name):
        aop = None
        if doi is not None:
            aop = self.get_aop_by_doi(doi)
        if aop is None:
            aop = self.get_aop_by_xmlname(xml_name)
        return aop

    def get_validated_aop(self, article):
        found_aop = None
        status = 'regular doc'
        messages = []
        if self.journal_has_aop():
            found_aop = self.find_aop(article.doi, article.xml_name)
            if found_aop is not None:
                status = self.compare_article_and_aop(article, found_aop)
                messages = self.check_aop_message(article, found_aop, status)
                if not status in ['matched aop', 'partially matched aop']:
                    found_aop = None
        #status = (status in ['matched aop', 'partially matched aop', 'regular doc'])
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
        if not aop is None:
            if article.article_type == 'correction':
                if article.body_words is not None and aop.body_words is not None:
                    r += how_similar(article.body_words[0:300], aop.body_words[0:300])
                    r = r * 100
                else:
                    r = 1
            else:
                r += how_similar(article.title, aop.title)
                r += how_similar(article.first_author_surname, aop.first_author_surname)
                r = (r * 100) / 2
        return r

    def check_aop_message(self, article, aop, status):
        label = 'body' if article.article_type == 'correction' else _('title/author')
        data = []
        msg_list = []

        msg_list.append(_('Checking if {label} has an "aop version"').format(label=article.xml))
        if article.doi is not None:
            msg_list.append(_('Checking if {label} has an "aop version"').format(label=article.doi))

        if status == 'regular doc':
            msg_list.append(validation_status.STATUS_WARNING + ': ' + _('Not found an "aop version" of this document.'))
        else:
            msg_list.append(validation_status.STATUS_INFO + ': ' + _('Found: "aop version"'))
            if status == 'partially matched aop':
                msg_list.append(validation_status.STATUS_INFO + ': ' + _('the {data} of article and its "aop version" are similar.').format(data=label))
            elif status == 'aop missing PID':
                msg_list.append(validation_status.STATUS_ERROR + ': ' + _('the "aop version" has no PID'))
            elif status == 'unmatched aop':
                status = 'unmatched aop'
                msg_list.append(validation_status.STATUS_FATAL_ERROR + ': ' + _('the {data} of article and "aop version" are different.').format(data=label))

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
                t = '' if article.first_author_surname is None else article.first_author_surname
                data.append(_('doc first author') + ':' + html_reports.format_html_data(t))
                t = '' if aop.first_author_surname is None else aop.first_author_surname
                data.append(_('aop first author') + ':' + html_reports.format_html_data(t))
        msg = ''
        msg += html_reports.tag('h5', _('Checking existence of aop version'))
        msg += ''.join([html_reports.p_message(item, False) for item in msg_list])
        msg += ''.join([html_reports.p_message(item, False) for item in data])
        return msg

    def mark_aop_as_deleted(self, aop):
        """
        Mark as deleted
        """
        if aop.doi is not None:
            del self.xmlname_indexed_by_doi[registered_aop.doi]
        issue_folder = self.issueid_indexed_by_xmlname[aop.xml_name]
        del self.issueid_indexed_by_xmlname[aop.xml_name]
        del self.xmlname_indexed_by_issueid_and_order[issue_folder + '|' + aop.order]

    def manage_ex_aop(self, aop):
        if aop.pid is not None:
            issueid = self.issueid_indexed_by_xmlname[aop.xml_name]
            done, msg = self.journal_files.archive_ex_aop_files(aop, issueid)
            if done:
                self.mark_aop_as_deleted(aop)
                if not issueid in self.changed_issues:
                    self.changed_issues.append(issueid)
        return (done, msg)

    def update_all_aop_db(self):
        if len(self.changed_issues) > 0:
            for issueid in self.changed_issues:
                self._aop_db_items[issueid].create_db()


def format_affiliations(affiliations):
    affs = []
    for item in affiliations:
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
    for aff in affiliations.values():
        if aff.id is not None and aff.i_country is not None and aff.norgname is not None:
            a = {}
            a['i'] = aff.id
            a['p'] = aff.i_country
            a['_'] = aff.norgname
            a['c'] = aff.city
            a['s'] = aff.state
            affs.append(a)
    return affs


class DBManager(object):

    def __init__(self, db_isis, title_db_filenames, issue_db_filenames, serial_path, local_web_app_path):
        self.src_title_db_filename = title_db_filenames[0]
        self.title_db_filename = title_db_filenames[1]
        self.title_fst_filename = title_db_filenames[2]

        self.src_issue_db_filename = issue_db_filenames[0]
        self.issue_db_filename = issue_db_filenames[1]
        self.issue_fst_filename = issue_db_filenames[2]

        self.db_isis = db_isis
        self.local_web_app_path = local_web_app_path
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
        if pissn is not None:
            _expr.append(pissn)
        if eissn is not None:
            _expr.append(eissn)
        if journal_title is not None:
            _expr.append(journal_title.replace('(', '').replace(')', ''))
            #utils.display_message(journal_title)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search_issue_expr(self, issue_id, pissn, eissn, acron=None):
        _expr = []
        if pissn is not None:
            _expr.append(pissn + issue_id)
        if eissn is not None:
            _expr.append(eissn + issue_id)
        if acron is not None:
            _expr.append(acron)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def update_and_search(self, db, expr, source_db, fst_filename):
        updated = False
        if os.path.isfile(db + '.mst'):
            result = self.db_isis.get_records(db, expr)
            if len(result) == 0:
                d_copy = fs_utils.last_modified_datetime(db + '.mst')
                d_source = fs_utils.last_modified_datetime(source_db + '.mst')
                diff = d_source - d_copy
                updated = not (diff.days > 0 or (diff.days == 0 and diff.seconds > 0))
        if not updated:
            self.update_db_copy(source_db, db, fst_filename)
        result = self.db_isis.get_records(db, expr)
        if len(result) > 0:
            result = result[0]
        else:
            result = None
        return result

    def get_issue_models(self, journal_title, issue_label, p_issn, e_issn):
        issue_models = None
        msg = None
        acron_issue_label = 'unidentified issue'
        if issue_label is None:
            msg = html_reports.p_message(validation_status.STATUS_FATAL_ERROR + ': ' + _('Unable to identify the article\'s issue'), False)
        else:
            i_record = self.find_i_record(issue_label, p_issn, e_issn)
            if i_record is None:
                acron_issue_label = 'not_registered issue'
                msg = html_reports.p_message(validation_status.STATUS_FATAL_ERROR + ': ' + _('Issue ') + issue_label + _(' is not registered in ') + self.issue_db_filename + _(' using ISSN: ') + _(' or ').join([i for i in [p_issn, e_issn] if i is not None]) + '.', False)
            else:
                issue_models = IssueModels(i_record)
                acron_issue_label = issue_models.issue.acron + ' ' + issue_models.issue.issue_label
                if (issue_models.issue.print_issn is None and issue_models.issue.e_issn is None) or issue_models.issue.license is None or issue_models.issue.journal_id_nlm_ta is None:
                    j_record = self.find_journal_record(journal_title, p_issn, e_issn)
                    if j_record is None:
                        msg = html_reports.p_message(validation_status.STATUS_ERROR + ': ' + _('Unable to get journal data') + ' ' + journal_title, False)
                    else:
                        t = RegisteredTitle(j_record)
                        issue_models.complete_issue_info(t)

        return (acron_issue_label, issue_models, msg)

    def get_issue_files(self, issue_models, pkg_path):
        if issue_models is not None:
            journal_files = serial_files.JournalFiles(self.serial_path, issue_models.issue.acron)
            return serial_files.IssueFiles(journal_files, issue_models.issue.issue_label, pkg_path, self.local_web_app_path)

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

    def __init__(self):
        ws_requester.wsr.update_journals_file()
        self._journals = {}

        with open(ws_requester.wsr.downloaded_journals_filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t')
            for item in spamreader:
                if len(item) >= 10:
                    item = [elem.decode('utf-8').strip() for elem in item]
                    if item[1] != 'ISSN':
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
                            if not issn in self._journals.keys():
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
        #journal.doi_prefix = journal_doi_prefix([journal.e_issn, journal.p_issn])

    def get_journal(self, p_issn, e_issn, journal_title):
        journal = Journal()
        for issn in [p_issn, e_issn]:
            if issn is not None:
                for j in self._journals.get(issn, []):
                    journal = j
                    #journal.doi_prefix = journal_doi_prefix([journal.e_issn, journal.p_issn])
        return journal


def update_list(l, value):
    if l is None:
        l = []
    if value is not None:
        if len(value) > 0:
            l.append(value)
    return list(set(l))


class JournalsManager(object):

    def __init__(self, journals_db=None):
        self.journals_list = JournalsList()
        self.journals_db = journals_db

    def journal(self, p_issn, e_issn, journal_title):
        j = None
        j_data = None
        if self.journals_db is None:
            j = self.journals_list.get_journal(p_issn, e_issn, journal_title)
            j_data = self.journals_list.get_journal_data(p_issn, e_issn, journal_title)
        return (j, j_data)
