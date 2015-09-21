# coding=utf-8

import os
from datetime import datetime

from __init__ import _
import utils
import xml_utils

from article_utils import display_pages, format_dateiso, format_issue_label
from utils import how_similar
from article import Issue, PersonAuthor, Article
from attributes import ROLE, DOCTOPIC, doctopic_label

from dbm_isis import IDFile
import pkg_reports
import institutions_service
import html_reports


ISSN_CONVERSION = {
    'ONLIN': 'epub',
    'PRINT': 'ppub',
    }


def author_tag(is_person, is_analytic_author):
    r = {}
    r[True] = {True: '10', False: '16'}
    r[False] = {True: '11', False: '17'}
    return r[is_person][is_analytic_author]


def read_issn_fields(fields):
    _issns = None
    if fields is not None:
        if not isinstance(fields, list):
            fields = [fields]
        _issns = {}
        for item in fields:
            if isinstance(item, dict):
                if 't' in item.keys() and '_' in item.keys():
                    _issns[ISSN_CONVERSION.get(item.get('t'), item.get('t'))] = item.get('_')
                elif 'epub' in item.keys() or 'ppub' in item.keys():
                    for k, v in item.items():
                        _issns[k] = v
            elif isinstance(item, tuple):
                _issns[item[0]] = item[1]
    return _issns


def format_issn_fields(issns):
    fields = []
    if issns is not None:
        if not isinstance(issns, list):
            issns = [issns]
        for issn in issns:
            if isinstance(issn, dict):
                for k, v in issn.items():
                    issn = {}
                    issn['t'] = k
                    issn['_'] = v
                    fields.append(issn)
    return fields


def normalize_role(_role):
    r = ROLE.get(_role)
    if r == '??' or _role is None or r is None:
        r = 'ND'
    return r


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


class RegisteredArticle(object):
    def __init__(self, article_records, i_record):
        self._issue = None
        self.i_record = i_record
        self.article_records = article_records

    def summary(self):
        data = {}
        data['journal-title'] = self.journal_title
        data['journal id NLM'] = self.journal_id_nlm_ta
        data['journal ISSN'] = ','.join([k + ':' + v for k, v in self.journal_issns.items() if v is not None]) if self.journal_issns is not None else None
        data['publisher name'] = self.publisher_name
        data['issue label'] = self.issue_models.issue.issue_label
        data['issue pub date'] = self.issue_models.issue.dateiso[0:4]
        data['order'] = self.order
        data['doi'] = self.doi
        data['fpage-and-seq'] = self.fpage
        data['elocation id'] = self.elocation_id
        return data

    @property
    def issue(self):
        if self._issue is None:
            issue_models = IssueModels(self.i_record)
            self._issue = issue_models.issue
        return self._issue

    @property
    def journal_title(self):
        return self.issue.journal_title if self.issue.journal_title else self.article_records[1].get('130')

    @property
    def journal_id_nlm_ta(self):
        return self.issue.journal_id_nlm_ta if self.issue.journal_id_nlm_ta else self.article_records[1].get('421')

    @property
    def journal_issns(self):
        if self.issue is not None:
            return self.issue.journal_issns

    @property
    def print_issn(self):
        if self.issue is not None:
            return self.issue.print_issn

    @property
    def e_issn(self):
        if self.issue is not None:
            return self.issue.e_issn

    @property
    def publisher_name(self):
        return self.issue.publisher_name if self.issue.publisher_name else self.article_records[1].get('62', self.article_records[1].get('480'))

    @property
    def tree(self):
        return True

    @property
    def elocation_id(self):
        return self.article_records[1]['14'].get('e')

    @property
    def fpage(self):
        return self.article_records[1]['14'].get('f')

    @property
    def article_type(self):
        return doctopic_label(self.article_records[1]['71'])

    @property
    def xml_name(self):
        return self.filename.replace('.xml', '')

    @property
    def filename(self):
        return self.article_records[0]['2']

    @property
    def rel_path(self):
        return self.article_records[0]['702']

    @property
    def titles(self):
        _titles = self.article_records[1].get('12')
        if _titles is None:
            _t = [{'_': None}]
        elif not isinstance(_titles, list):
            _t = [_titles]
        else:
            _t = _titles
        return _t

    @property
    def first_title(self):
        return self.titles[0].get('_')

    @property
    def title(self):
        return self.first_title

    @property
    def doi(self):
        return self.article_records[1].get('237')

    @property
    def pid(self):
        return self.article_records[1].get('880')

    @property
    def previous_pid(self):
        return self.article_records[1].get('881')

    @property
    def creation_date_display(self):
        return utils.display_datetime(self.article_records[0]['91'], self.article_records[0]['92'])

    @property
    def creation_date(self):
        return (self.article_records[0]['91'], self.article_records[0]['92'])

    @property
    def last_update(self):
        #2015-03-26T14:43:50.272660
        last = self.article_records[0].get('93')
        if last is not None:
            if '-' in last:
                last = last.replace('T', ' ')[0:16]
            if ' ' in last:
                last = last.split(' ')
                last = utils.display_datetime(last[0], last[1])
            else:
                last = utils.display_datetime(last, '')
        return last

    @property
    def order(self):
        _order = '0'*5 + self.article_records[1]['121']
        return _order[-5:]

    @property
    def toc_section(self):
        return self.article_records[1]['49']


class ArticleRecords(object):

    def __init__(self, institution_normalizer, article, i_record, article_files):
        self.institution_normalizer = institution_normalizer
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
        if not '435' in self._metadata.keys():
            self._metadata['435'] = self.article.journal_issns

    def fix_issue_data(self):
        if '130' in self._metadata.keys():
            self._metadata['100'] = self._metadata['130']
            del self._metadata['130']
        if '435' in self._metadata.keys():
            self._metadata['435'] = format_issn_fields(read_issn_fields(self.article.journal_issns))
        if '480' in self._metadata.keys():
            del self._metadata['480']

    @property
    def metadata(self):
        return self._metadata

    def add_article_data(self):
        self._metadata['120'] = 'XML_' + self.article.dtd_version
        self._metadata['71'] = normalize_doctopic(self.article.article_type)
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
        for item in self.article.contrib_names:
            new = {}
            new['n'] = item.fname
            new['s'] = item.surname
            if item.suffix is not None:
                if item.suffix != '':
                    new['s'] += ' ' + item.suffix
            new['p'] = item.prefix
            new['r'] = normalize_role(item.role)
            #if len(item.xref) == 0 and len(self.article.affiliations) > 0 and len(self.article.contrib_names) == 1:
            #    new['1'] = ' '.join([aff.id for aff in self.article.affiliations if aff.id is not None])
            #else:
            #    new['1'] = ' '.join(item.xref)
            new['1'] = ' '.join(item.xref)
            new['k'] = item.contrib_id
            self._metadata['10'].append(new)

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

        #self._metadata['65'] = format_dateiso(self.article.issue_pub_date)

        self._metadata['14'] = {}
        self._metadata['14']['f'] = self.article.fpage
        self._metadata['14']['s'] = self.article.fpage_seq
        self._metadata['14']['l'] = self.article.lpage
        self._metadata['14']['e'] = self.article.elocation_id

        self._metadata['70'] = format_affiliations(self.article.affiliations)

        self._metadata['240'] = normalize_affiliations(self.institution_normalizer, self.article.found_institutions(self.institution_normalizer))
        #CT^uhttp://www.clinicaltrials.gov/ct2/show/NCT01358773^aNCT01358773
        self._metadata['770'] = {'u': self.article.clinical_trial_url}
        self._metadata['72'] = str(0 if self.article.total_of_references is None else self.article.total_of_references)
        #self._metadata['901'] = str(0 if self.article.total_of_tables is None else self.article.total_of_tables)
        #self._metadata['902'] = str(0 if self.article.total_of_figures is None else self.article.total_of_figures)

        self._metadata['83'] = []
        for item in self.article.abstracts:
            self._metadata['83'].append({'l': item.language, 'a': item.text})

        self._metadata['112'] = format_dateiso(self.article.received)
        self._metadata['114'] = format_dateiso(self.article.accepted)

    @property
    def references(self):

        records_c = []
        for item in self.article.references:
            rec_c = {}
            rec_c['865'] = self.i_record.get('65')
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
                        a['r'] = normalize_role(author.role)
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
                y = item.formatted_year[0:4]
                if y.isdigit():
                    rec_c['65'] = y + '0000'
            rec_c['66'] = item.publisher_loc
            rec_c['62'] = item.publisher_name
            rec_c['514'] = {'f': item.fpage, 'l': item.lpage, 'r': item.page_range, 'e': item.elocation_id}

            if item.fpage is not None or item.lpage is not None:
                rec_c['14'] = display_pages(item.fpage, item.lpage)
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
        if self.article.creation_date is None:
            rec_o['91'] = datetime.now().isoformat().replace('-', '').replace(':', '').replace('T', ' ')[0:13]
            rec_o['93'] = rec_o['91']
            rec_o['91'], rec_o['92'] = rec_o['91'].split(' ')
        else:
            rec_o['91'] = self.article.creation_date[0]
            rec_o['92'] = self.article.creation_date[1]
            rec_o['93'] = datetime.now().isoformat().replace('-', '').replace('T', ' ').replace(':', '')[0:13]
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

    def license(self):
        if self.record is not None:
            return self.record.get('541')


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
        issns = record.get('435')
        # 0011-5258^tPRINT
        # 1678-4588^tONLIN
        # [{'_': 1234-567, 't': PRINT}, {'_': 1678-4588, 't': ONLIN}]
        i.journal_issns = read_issn_fields(record.get('435'))
        if i.journal_issns is None:
            i.e_issn = None
            i.print_issn = None
        else:
            i.e_issn = i.journal_issns.get('epub')
            i.print_issn = i.journal_issns.get('ppub')
        i.publisher_name = record.get('62', record.get('480'))
        i.license = record.get('541')
        return i


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


class RegisteredAhead(object):

    def __init__(self, record, ahead_db_name):
        self.record = record
        self.ahead_db_name = ahead_db_name

    @property
    def doi(self):
        return self.record.get('237')

    @property
    def filename(self):
        return self.record.get('2')

    @property
    def xml_name(self):
        return self.record.get('2', '').replace('.xml', '')

    @property
    def order(self):
        _order = '0'*5 + self.record.get('121', '00000')
        return _order[-5:]

    @property
    def ahead_pid(self):
        _order = '00000' + self.order
        r = 'S' + self.record.get('35') + self.ahead_db_name[0:4] + '0050' + _order[-5:]
        return r if len(r) == 23 else None

    @property
    def article_title(self):
        title = self.record.get('12')
        if isinstance(title, dict):
            t = title.get('_')
        elif isinstance(title, list):
            t = title[0].get('_')
        else:
            t = 'None'
        return t

    @property
    def first_author_surname(self):
        author = self.record.get('10')
        if isinstance(author, dict):
            a = author.get('s')
        elif isinstance(author, list):
            a = author[0].get('s')
        else:
            a = 'None'
        return a


class ArticleDB(object):

    def __init__(self, db_isis, issue_files, aop_manager):
        self.issue_files = issue_files
        self.db_isis = db_isis
        self.aop_manager = aop_manager
        self._registered_articles = None
        self._issue_models = None
        self._registered_articles_records = None
        self._registered_i_record = None

    def restore_missing_id_files(self):
        self._registered_i_record, self._registered_articles_records = self.registered_records
        if self._registered_articles_records is not None:
            for name, registered_article in self._registered_articles.items():
                article_files = ArticleFiles(self.issue_files, registered_article.order, registered_article.xml_name)
                if not os.path.isfile(article_files.id_filename):
                    self.db_isis.save_id(article_files.id_filename, registered_article.article_records)

    def reset_registered_records(self):
        self._registered_articles_records = None
        self._registered_articles = None

    @property
    def registered_records(self):
        if self._registered_i_record is None or self._registered_articles_records is None:
            records = self.db_isis.get_records(self.issue_files.base)
            self._registered_i_record, self._registered_articles_records = IssueArticlesRecords(records).articles()
        return (self._registered_i_record, self._registered_articles_records)

    @property
    def registered_articles(self):
        if self._registered_articles is None:
            self._registered_articles = {}
            self._registered_i_record, self._registered_articles_records = self.registered_records

            for xml_name, registered_article in self._registered_articles_records.items():
                f = issue_files.base_source_path + '/' + xml_name + '.xml'
                if os.path.isfile(f):

                    xml, e = xml_utils.load_xml(f)
                    doc = Article(xml, xml_name)

                    doc.pid = registered_article.pid
                    doc.creation_date_display = registered_article.creation_date_display
                    doc.creation_date = registered_article.creation_date
                    doc.last_update = registered_article.last_update
                    doc.order = registered_article.order
                    doc.previous_pid = registered_article.previous_pid
                else:
                    doc = None
                self._registered_articles[xml_name] = doc
        return self._registered_articles

    @property
    def registered_issue_models(self):
        if self._issue_models is None:
            self._issue_models = IssueModels(self._registered_i_record) if self._registered_i_record is not None else None
        return self._issue_models

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
        self.reset_registered_records()

    def article_records(self, institution_normalizer, i_record, article, article_files):
        _article_records = None
        if article.order != '00000':
            _article_records = ArticleRecords(institution_normalizer, article, i_record, article_files)
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
                    print('Unable to delete ' + article_files.id_filename)
            previous = os.path.isfile(article_files.id_filename)

            self.db_isis.save_id(article_files.id_filename, article_records.records, self.content_formatter)
            saved = os.path.isfile(article_files.id_filename)
        return saved and not previous

    def insert_article(self, institution_normalizer, i_record, article, valid_aop, incorrect_order):
        msg = ''
        is_excluded_incorrect_order = None
        is_excluded_aop = None
        if valid_aop is not None:
            article.registered_aop_pid = valid_aop.ahead_pid

        article_files = serial_files.ArticleFiles(self.issue_files, article.order, article.xml_name)
        article_records = self.article_records(institution_normalizer, i_record, article, article_files)
        saved = self.create_article_id_file(article_records, article_files)
        if saved:
            if incorrect_order is not None:
                incorrect_article_files = serial_files.ArticleFiles(self.issue_files, incorrect_order, article.xml_name)
                if os.path.isfile(incorrect_article_files.id_filename):
                    os.unlink(incorrect_article_files.id_filename)
                is_excluded_incorrect_order = not os.path.isfile(incorrect_article_files.id_filename)

            if valid_aop is not None:
                is_excluded_aop, excluded_aop_msg = self.aop_manager.manage_ex_aop(valid_aop)

        return (saved, is_excluded_incorrect_order, is_excluded_aop)

    def finish_conversion(self, pkg_path):
        self.create_db()
        self.issue_files.save_source_files(pkg_path)

    def generate_windows_version(self):
        if not os.path.isdir(self.issue_files.windows_base_path):
            os.makedirs(self.issue_files.windows_base_path)
        self.db_isis.cisis.mst2iso(self.issue_files.base, self.issue_files.windows_base + '.iso')
        self.db_isis.cisis.crunchmf(self.issue_files.base, self.issue_files.windows_base)


class AopManager(object):

    def __init__(self, db_isis, journal_files):
        self.db_isis = db_isis
        self.journal_files = journal_files
        self.still_aop = {}
        self.indexed_by_doi = {}
        self.indexed_by_xml_name = {}
        self._aop_db_items = None
        self.setup()
        self.aop_sorted_by_status = {'deleted ex-aop': [], 'not deleted ex-aop': []}
        self.aop_info = {}
        self.aop_validations = pkg_reports.PackageValidationsResults()

    def journal_has_aop(self):
        return len(self.indexed_by_xml_name[registered_aop.xml_name]) > 0

    def journal_publishes_aop(self):
        return self.journal_files.publishes_aop()

    def setup(self):
        self._aop_db_items = {}
        for name, aop_issue_files in self.journal_files.aop_issue_files.items():
            self._aop_db[aop_issue_files.issue_folder] = ArticleDB(self.db_isis, aop_issue_files)
            self._aop_db[aop_issue_files.issue_folder].restore_missing_id_files()

            registered_i_record, registered_articles = self._aop_db[aop_issue_files.issue_folder].registered_records

            if registered_articles is not None:
                for xml_name, registered_article in registered_articles.items():
                    registered_aop = RegisteredAhead(registered_article.article_records[1], aop_issue_files.issue_folder)
                    self.indexed_by_doi[registered_aop.doi] = registered_aop.xml_name
                    self.indexed_by_xml_name[registered_aop.xml_name] = registered_aop
                    if self.still_aop[aop_issue_files.issue_folder] is None:
                        self.still_aop[aop_issue_files.issue_folder] = {}
                    self.still_aop[aop_issue_files.issue_folder][registered_aop.order] = registered_aop.xml_name

    @property
    def aop_db_items(self):
        return self._aop_db_items

    def still_aop_items(self):
        if self.aop_sorted_by_status is None:
            self.aop_sorted_by_status = {}
        self.aop_sorted_by_status['still aop'] = []

        for dbname in sorted(self.still_aop.keys()):
            for order in sorted(self.still_aop[dbname].keys()):
                xml_name = self.still_aop[dbname][order]
                aop = self.indexed_by_xml_name[xml_name]
                self.aop_sorted_by_status['still aop'].append(dbname + '|' + order + '|' + aop.filename + '|' + aop.article_title[0:50] + '...')

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def find_aop(self, doi, filename):
        data = None
        aop = None
        if doi is not None:
            xml_name = self.indexed_by_doi.get(doi)
            if xml_name is not None:
                aop = self.indexed_by_xml_name.get(xml_name)
        if aop is None:
            aop = self.indexed_by_xml_name.get(filename)
        return aop

    @property
    def aop_article(self, xml_name):
        return self.aop_info.get(xml_name, [None, None])[0]

    @property
    def aop_status(self, xml_name):
        return self.aop_info.get(xml_name, [None, None])[1]

    @property
    def aop_items_status(self):
        return self.aop_sorted_by_status

    def check_aop(self, article):
        aop = None
        status = None
        if self.journal_has_aop():
            aop, status = self.get_aop_and_status(article)
            if not status in self.aop_sorted_by_status.keys():
                self.aop_sorted_by_status[status] = []
            self.aop_sorted_by_status[status].append(xml_name)
            msg = self.aop_message(article, doc_aop, status)
            self.aop_validations.add(article.xml_name, pkg_reports.ValidationsResults(msg))
            if aop is not None:
                if status in ['unmatched aop', 'aop missing PID']:
                    aop = None
            self.aop_info[article.xml_name] = (aop, status)

    def get_aop_and_status(self, article):
        aop = None
        status = None
        if article.number == 'ahead':
            status = 'new aop'
        else:
            if len(self.still_aop) == 0:
                status = 'new doc'
            else:
                aop = self.find_aop(article.doi, article.xml_name)
                if aop is None:
                    status = 'new doc'
                else:
                    rate = self.score(article, aop)
                    rate = self.is_acceptable_rate(rate, 80)
                    if rate > 0:
                        if aop.ahead_pid is None:
                            status = 'aop missing PID'
                        else:
                            status = 'matched aop'
                            if rate != 1:
                                status = 'partially matched aop'
                    else:
                        status = 'unmatched aop'
        return (aop, status)

    def is_acceptable_rate(self, rate, min_score):
        return rate if rate >= min_score else 0

    def similarity_rate(self, article, aop):
        r = 0
        if not aop is None:
            r += how_similar(article.title, aop.article_title)
            r += how_similar(article.first_author_surname, aop.first_author_surname)
            r = (r * 100) / 2
        return r

    def aop_message(self, article, aop, status):
        data = []
        msg_list = []
        if status == 'new aop':
            msg_list.append('INFO: ' + _('This document is an "aop".'))
        else:
            msg_list.append(_('Checking if ') + article.xml_name + _(' has an "aop version"'))
            if article.doi is not None:
                msg_list.append(_('Checking if ') + article.doi + _(' has an "aop version"'))

            if status == 'new doc':
                msg_list.append('WARNING: ' + _('Not found an "aop version" of this document.'))
            else:
                msg_list.append('WARNING: ' + _('Found: "aop version"'))
                if status == 'partially matched aop':
                    msg_list.append('WARNING: ' + _('the title/author of article and its "aop version" are similar.'))
                elif status == 'aop missing PID':
                    msg_list.append('ERROR: ' + _('the "aop version" has no PID'))
                elif status == 'unmatched aop':
                    status = 'unmatched aop'
                    msg_list.append('FATAL ERROR: ' + _('the title/author of article and "aop version" are different.'))

                t = '' if article.title is None else article.title
                data.append(_('doc title') + ':' + t)
                t = '' if aop.article_title is None else aop.article_title
                data.append(_('aop title') + ':' + t)
                t = '' if article.first_author_surname is None else article.first_author_surname
                data.append(_('doc first author') + ':' + t)
                t = '' if aop.first_author_surname is None else aop.first_author_surname
                data.append(_('aop first author') + ':' + t)
        msg = ''
        msg += html_reports.tag('h5', _('Checking existence of aop version'))
        msg += ''.join([html_reports.p_message(item) for item in msg_list])
        msg += ''.join([html_reports.display_xml(item, html_reports.XML_WIDTH*0.9) for item in data])
        return msg

    def mark_aop_as_deleted(self, aop):
        """
        Mark as deleted
        """
        if aop.ahead_db_name in self.still_aop.keys():
            if aop.order in self.still_aop[aop.ahead_db_name].keys():
                del self.still_aop[aop.ahead_db_name][aop.order]
        if aop.doi in self.indexed_by_doi.keys():
            del self.indexed_by_doi[aop.doi]
        if aop.filename in self.indexed_by_xml_name.keys():
            del self.indexed_by_xml_name[aop.filename]

    def archive_ex_aop_files(self, aop, db_name):
        aop_issue_files = None
        ex_aop_issue_files = None
        done = False
        msg = None
        if self.journal_files.ex_aop_issue_files is not None:
            ex_aop_issue_files = self.journal_files.ex_aop_issue_files.get(db_name)
        if self.journal_files.aop_issue_files is not None:
            aop_issue_files = self.journal_files.aop_issue_files.get('ex-' + db_name)
        if aop_issue_files is not None and ex_aop_issue_files is not None:
            fs_utils.move_file(aop_issue_files.markup_path + '/' + aop.filename, ex_aop_issue_files.markup_path + '/' + aop.filename)
            fs_utils.move_file(aop_issue_files.body_path + '/' + aop.filename, ex_aop_issue_files.body_path + '/' + aop.filename)
            fs_utils.move_file(aop_issue_files.base_source_path + '/' + aop.filename, ex_aop_issue_files.base_source_path + '/' + aop.filename)
            msg = fs_utils.move_file(aop_issue_files.id_path + '/' + aop.filename, ex_aop_issue_files.id_path + '/' + aop.filename)
            done = (not os.path.isfile(aop_issue_files.id_path + '/' + aop.filename))
        return (done, msg)

    def __manage_ex_aop(self, aop):
        done = False
        msg = []
        if aop is not None:
            if aop.ahead_pid is not None:
                done, msg = self.archive_ex_aop_files(aop)
                if done:
                    self.mark_aop_as_deleted(aop)
        return (done, msg)

    def manage_ex_aop(self, aop):
        if self.aop_status(aop.xml_name) in ['matched aop', 'partially matched aop']:
            is_excluded_aop, aop_msg = aop_manager.__manage_ex_aop(aop)
            msg += ''.join([item for item in aop_msg])
            if is_excluded_aop is True:
                self.aop_sorted_by_status['deleted ex-aop'].append(aop.xml_name)
            else:
                self.aop_sorted_by_status['not deleted ex-aop'].append(aop.xml_name)
        return (saved, msg)

    def update_all_aop_db(self):
        if self.aop_sorted_by_status is None:
            self.aop_sorted_by_status = {}
        self.aop_sorted_by_status['aop scilista item to update'] = []
        if self._aop_db_items is not None:
            for dbname, aop_db in self._aop_db_items.items():
                aop_db.create_db()
                self.aop_sorted_by_status['aop scilista item to update'].append(self.journal_files.acron + ' ' + dbname)


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
        a['p'] = item.country if item.i_country is None else item.i_country
        a['q'] = item.country if item.i_country is not None else None
        a['c'] = item.city
        a['s'] = item.state
        a['_'] = item.orgname
        affs.append(a)
    return affs


def normalize_affiliations(institution_normalizer, found_institutions):
    aff = []
    for aff_id, results in found_institutions:
        aff = institution_normalizer.normalized_institution(results)
        if aff is not None:
            norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name = aff
            a = {}
            a['i'] = item.id
            a['p'] = norm_country_code
            a['_'] = norm_orgname
            a['c'] = norm_city
            a['s'] = norm_state
            affs.append(a)
    return affs


class DBManager(object):

    def __init__(self, db_isis, title_filename, issue_filename, serial_path, local_web_app_path):
        self.title_db_filename = title_filename
        self.issue_db_filename = issue_filename
        self.db_isis = db_isis
        self.local_web_app_path = local_web_app_path
        self.serial_path = serial_path

    def search_journal_expr(self, pissn, eissn, journal_title):
        _expr = []
        if pissn is not None:
            _expr.append(pissn)
        if eissn is not None:
            _expr.append(eissn)
        if journal_title is not None:
            _expr.append("'" + journal_title + "'")
            utils.display_message(journal_title)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search_journal(self, pissn, eissn, journal_title):
        expr = self.search_journal_expr(pissn, eissn, journal_title)
        return self.db_isis.get_records(self.title_db_filename, expr) if expr is not None else None

    def search_issue_expr(self, issue_id, pissn, eissn, acron=None):
        _expr = []
        if pissn is not None:
            _expr.append(pissn + issue_id)
        if eissn is not None:
            _expr.append(eissn + issue_id)
        if acron is not None:
            _expr.append(acron)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search_issue(self, issue_label, pissn, eissn):
        expr = self.search_issue_expr(issue_label, pissn, eissn)
        return self.db_isis.get_records(self.issue_db_filename, expr) if expr is not None else None

    def get_issue_models(self, journal_title, issue_label, p_issn, e_issn):
        issue_models = None
        msg = None

        if issue_label is None:
            msg = html_reports.p_message('FATAL ERROR: ' + _('Unable to identify the article\'s issue'))
        else:
            i_record = self.find_i_record(issue_label, p_issn, e_issn)
            if i_record is None:
                msg = html_reports.p_message('FATAL ERROR: ' + _('Issue ') + issue_label + _(' is not registered in ') + self.db_issue.db_filename + _(' using ISSN: ') + _(' or ').join([i for i in [p_issn, e_issn] if i is not None]) + '.')
            else:
                issue_models = IssueModels(i_record)
                if issue_models.issue.license is None:
                    j_record = self.find_journal_record(journal_title, p_issn, e_issn)
                    if j_record is None:
                        msg = html_reports.p_message('ERROR: ' + _('Unable to get the license of') + ' ' + journal_title)
                    else:
                        t = RegisteredTitle(j_record)
                        issue_models.issue.license = t.license()
        return (issue_models, msg)

    def get_issue_files(self, issue_models, pkg_path):
        journal_files = serial_files.JournalFiles(self.serial_path, issue_models.issue.acron)
        return serial_files.IssueFiles(journal_files, issue_models.issue.issue_label, pkg_path, self.local_web_app_path)

    def find_journal_record(self, journal_title, print_issn, e_issn):
        record = None
        records = self.search_journal(print_issn, e_issn, journal_title)

        if len(records) > 0:
            record = records[0]
        return record

    def find_i_record(self, issue_label, print_issn, e_issn):
        i_record = None
        issues_records = self.search_issue(issue_label, print_issn, e_issn)
        if len(issues_records) > 0:
            i_record = issues_records[0]
        return i_record

