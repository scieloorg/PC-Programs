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

import institutions_service


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
        return self.article_records[1]['121']

    @property
    def toc_section(self):
        return self.article_records[1]['49']


class ArticleRecords(object):

    def __init__(self, org_manager, article, i_record, article_files, creation_date=None):
        self.org_manager = org_manager
        self.article = article
        self.article_files = article_files
        self.i_record = i_record
        self.creation_date = creation_date
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
        self._metadata['240'] = normalized_affiliations(self.org_manager, self.article.affiliations)
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
        if self.creation_date is None:
            rec_o['91'] = datetime.now().isoformat().replace('-', '').replace(':', '').replace('T', ' ')[0:13]
            rec_o['93'] = rec_o['91']
            rec_o['91'], rec_o['92'] = rec_o['91'].split(' ')
        else:
            rec_o['91'] = self.creation_date[0]
            rec_o['92'] = self.creation_date[1]
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
        return self.record.get('121', '00000')

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


class TitleDAO(object):

    def __init__(self, dao, db_filename):
        self.dao = dao
        self.db_filename = db_filename

    def expr(self, pissn, eissn, journal_title):
        _expr = []
        if pissn is not None:
            _expr.append(pissn)
        if eissn is not None:
            _expr.append(eissn)
        if journal_title is not None:
            _expr.append("'" + journal_title + "'")
            utils.display_message(journal_title)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search(self, pissn, eissn, journal_title):
        expr = self.expr(pissn, eissn, journal_title)
        return self.dao.get_records(self.db_filename, expr) if expr is not None else None


class IssueDAO(object):

    def __init__(self, dao, db_filename):
        self.dao = dao
        self.db_filename = db_filename

    def expr(self, issue_id, pissn, eissn, acron=None):
        _expr = []
        if pissn is not None:
            _expr.append(pissn + issue_id)
        if eissn is not None:
            _expr.append(eissn + issue_id)
        if acron is not None:
            _expr.append(acron)
        return ' OR '.join(_expr) if len(_expr) > 0 else None

    def search(self, issue_label, pissn, eissn):
        expr = self.expr(issue_label, pissn, eissn)
        return self.dao.get_records(self.db_filename, expr) if expr is not None else None


class ArticleDAO(object):

    def __init__(self, dao, org_manager):
        self.org_manager = org_manager
        self.dao = dao

    def create_id_file(self, i_record, article, article_files, creation_date=None):
        saved = False
        found = False
        if not os.path.isdir(article_files.issue_files.id_path):
            os.makedirs(article_files.issue_files.id_path)
        if not os.path.isdir(os.path.dirname(article_files.issue_files.base)):
            os.makedirs(os.path.dirname(article_files.issue_files.base))

        if article.order != '00000':
            article_records = ArticleRecords(self.org_manager, article, i_record, article_files, creation_date)
            if os.path.isfile(article_files.id_filename):
                try:
                    os.unlink(article_files.id_filename)
                except:
                    print('Unable to delete ' + article_files.id_filename)
            found = os.path.isfile(article_files.id_filename)

            self.dao.save_id(article_files.id_filename, article_records.records, self.content_formatter)
            saved = os.path.isfile(article_files.id_filename)
        return (not found and saved)

    def content_formatter(self, content):
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
        return content

    def finish_conversion(self, issue_record, issue_files, pkg_path):
        loaded = []
        self.dao.save_records([issue_record], issue_files.base)
        for f in os.listdir(issue_files.id_path):
            if f == '00000.id':
                os.unlink(issue_files.id_path + '/' + f)
            if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                self.dao.append_id_records(issue_files.id_path + '/' + f, issue_files.base)
                loaded.append(f)
        issue_files.save_source_files(pkg_path)
        return loaded

    def registered_items(self, issue_files):
        articles = {}
        records = self.dao.get_records(issue_files.base)
        i, registered_articles = IssueArticlesRecords(records).articles()

        for xml_name, registered_doc in registered_articles.items():
            f = issue_files.base_source_path + '/' + xml_name + '.xml'
            if os.path.isfile(f):

                xml, e = xml_utils.load_xml(f)
                doc = Article(xml, xml_name)

                doc.pid = registered_doc.pid
                doc.creation_date_display = registered_doc.creation_date_display
                doc.creation_date = registered_doc.creation_date
                doc.last_update = registered_doc.last_update
                articles[xml_name] = doc

        issue_models = IssueModels(i) if i is not None else None
        return (issue_models, articles)

    def generate_windows_version(self, issue_files):
        if not os.path.isdir(issue_files.windows_base_path):
            os.makedirs(issue_files.windows_base_path)
        self.dao.cisis.mst2iso(issue_files.base, issue_files.windows_base + '.iso')
        self.dao.cisis.crunchmf(issue_files.base, issue_files.windows_base)


class AheadManager(object):

    def __init__(self, dao, journal_files, i_ahead_records):
        self.journal_files = journal_files
        self.dao = dao

        self.still_ahead = {}
        self.ahead_to_delete = {}

        self.indexed_by_doi = {}
        self.indexed_by_xml_name = {}
        self.load()
        self.extract_id_files_from_master(i_ahead_records)

    def journal_has_aop(self):
        total = 0
        for dbname, items in self.still_ahead.items():
            total += len(items)
        return total > 0

    def journal_publishes_aop(self):
        return self.journal_files.publishes_aop()

    def extract_id_files_from_master(self, i_ahead_records):
        for db_filename in self.journal_files.ahead_bases:

            year = os.path.basename(db_filename)[0:4]
            id_path = self.journal_files.ahead_id_path(year)
            i_id_filename = self.journal_files.ahead_i_id_filename(year)
            if not os.path.isdir(id_path):
                os.makedirs(id_path)
            if not os.path.isfile(i_id_filename):
                if year in i_ahead_records.keys():
                    self.dao.save_id(i_id_filename, [i_ahead_records[year]])
            records = self.dao.get_records(db_filename, expr=None)
            if len(records) > 0:
                previous = ''
                order = None
                r = []
                for rec in records:
                    if rec.get('706') == 'i':
                        if not os.path.isfile(id_path + '/i.id'):
                            self.dao.save_id(id_path + '/i.id', [rec])
                    else:
                        current = rec.get('2')
                        if rec.get('706') == 'h':
                            order = '00000' + rec.get('121')
                            order = order[-5:]
                        if previous != current:
                            if order is not None and len(r) > 0:
                                if not os.path.isfile(id_path + '/' + order + '.id'):
                                    self.dao.save_id(id_path + '/' + order + '.id', r)

                                r = []
                            previous = current
                        r.append(rec)
                if order is not None and len(r) > 0:
                    if not os.path.isfile(id_path + '/' + order + '.id'):
                        self.dao.save_id(id_path + '/' + order + '.id', r)

    def load(self):
        for db_filename in self.journal_files.ahead_bases:
            dbname = os.path.basename(db_filename)
            self.still_ahead[dbname] = {}
            for h_record in self.h_records(db_filename):
                ahead = RegisteredAhead(h_record, dbname)
                self.indexed_by_doi[ahead.doi] = ahead
                self.indexed_by_xml_name[ahead.xml_name] = ahead
                self.still_ahead[dbname][ahead.order] = ahead
        utils.debugging('~'*20)
        utils.debugging('\n'.join(self.indexed_by_doi.keys()))
        utils.debugging('\n'.join(self.indexed_by_xml_name.keys()))
        utils.debugging('~'*20)

    def still_ahead_items(self):
        items = []
        for dbname in sorted(self.still_ahead.keys()):
            for order in sorted(self.still_ahead[dbname].keys()):
                items.append(dbname + '/' + order + ' (' + self.still_ahead[dbname][order].filename + '): ' + self.still_ahead[dbname][order].article_title[0:50] + '...')
        return items

    def h_records(self, db_filename):
        return self._select_h(self.dao.get_records(db_filename))

    def _select_h(self, records):
        return [rec for rec in records if rec.get('706') == 'h']

    def name(self, db_filename):
        return os.path.basename(db_filename)

    def is_valid(self, ahead):
        r = False
        if ahead is not None:
            r = (ahead.ahead_pid is not None)
        return r

    def score(self, article, ahead, min_score):
        rate = self.matched_rate(article, ahead)
        if rate >= min_score:
            r = rate
        else:
            r = 0
        return r

    def matched_rate(self, article, ahead):
        r = 0
        if not ahead is None:
            r += how_similar(article.title, ahead.article_title)
            r += how_similar(article.first_author_surname, ahead.first_author_surname)
            r = (r * 100) / 2
            if r < 80:
                print((article.title, ahead.article_title))
                print((article.first_author_surname, ahead.first_author_surname))
        return r

    def find_ahead(self, doi, filename):
        data = None
        aop = None
        if doi is not None:
            aop = self.indexed_by_doi.get(doi)
        if aop is None:
            aop = self.indexed_by_xml_name.get(filename)
        return aop

    def get_valid_ahead(self, article):
        utils.debugging('get_valid_ahead - inicio')
        ahead = None
        status = None
        if article.number == 'ahead':
            status = 'new aop'
        else:
            if len(self.still_ahead) == 0:
                status = 'new doc'
            else:
                ahead = self.find_ahead(article.doi, article.xml_name)
                if ahead is None:
                    status = 'new doc'
                else:
                    matched_rate = self.score(article, ahead, 80)
                    if matched_rate > 0:
                        if ahead.ahead_pid is None:
                            status = 'aop missing PID'
                        else:
                            status = 'matched aop'
                            if matched_rate != 1:
                                status = 'partially matched aop'
                    else:
                        status = 'unmatched aop'
        utils.debugging('get_valid_ahead - fim')

        return (ahead, status)

    def mark_ahead_as_deleted(self, ahead):
        """
        Mark as deleted
        """
        if not ahead.ahead_db_name in self.ahead_to_delete.keys():
            self.ahead_to_delete[ahead.ahead_db_name] = []
        self.ahead_to_delete[ahead.ahead_db_name].append(ahead)
        if ahead.ahead_db_name in self.still_ahead.keys():
            if ahead.order in self.still_ahead[ahead.ahead_db_name].keys():
                del self.still_ahead[ahead.ahead_db_name][ahead.order]

    def manage_ex_ahead_files(self, ahead):
        msg = []
        msg.append(_('Exclude aop files of ') + ahead.filename)
        year = ahead.ahead_db_name[0:4]

        ex_ahead_markup_path, ex_ahead_body_path, ex_ahead_base_path = self.journal_files.ex_ahead_paths(year)

        # move files to ex-ahead folder
        xml_file, markup_file, body_file = self.journal_files.ahead_xml_markup_body(year, ahead.filename)
        if os.path.isfile(markup_file):
            if not os.path.isdir(ex_ahead_markup_path):
                os.makedirs(ex_ahead_markup_path)
            shutil.move(markup_file, ex_ahead_markup_path)
            msg.append('moved ' + markup_file + '\n    to ' + ex_ahead_markup_path)
        if os.path.isfile(body_file):
            if not os.path.isdir(ex_ahead_body_path):
                os.makedirs(ex_ahead_body_path)
            shutil.move(body_file, ex_ahead_body_path)
            msg.append('moved ' + body_file + '\n    to ' + ex_ahead_body_path)

        ahead_order = ahead.order
        ahead_id_filename = self.journal_files.ahead_id_filename(year, ahead_order)
        if os.path.isfile(ahead_id_filename):
            os.unlink(ahead_id_filename)
            msg.append('deleted ' + ahead_id_filename)
        return (not os.path.isfile(ahead_id_filename), msg)

    def save_ex_ahead_record(self, ahead):
        self.dao.append_records([ahead.record], self.journal_files.ahead_base('ex-' + ahead.ahead_db_name[0:4]))

    def manage_ex_ahead(self, ahead):
        done = False
        msg = []
        if ahead is not None:
            if ahead.ahead_pid is not None:
                self.mark_ahead_as_deleted(ahead)
                deleted, msg = self.manage_ex_ahead_files(ahead)
                if deleted:
                    self.save_ex_ahead_record(ahead)
                    done = True
                    if ahead.doi in self.indexed_by_doi.keys():
                        del self.indexed_by_doi[ahead.doi]
                    if ahead.filename in self.indexed_by_xml_name.keys():
                        del self.indexed_by_xml_name[ahead.filename]
        return (done, msg)

    def finish_manage_ex_ahead(self):
        updated = []
        for ahead_db_name, still_ahead in self.ahead_to_delete.items():
            year = ahead_db_name[0:4]
            id_path = self.journal_files.ahead_id_path(year)
            base = self.journal_files.ahead_base(year)
            if os.path.isfile(id_path + '/i.id'):
                self.dao.save_id_records(id_path + '/i.id', base)
                for f in os.listdir(id_path):
                    if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                        self.dao.append_id_records(id_path + '/' + f, base)
                updated.append(ahead_db_name)
        return updated

    def update_all_ahead_db(self):
        updated = []
        if self.journal_files.publishes_aop():
            for issue_label, issue_files in self.journal_files.aop_issue_files.items():
                id_path = issue_files.id_path
                if os.path.isfile(issue_files.id_filename):
                    self.dao.save_id_records(issue_files.id_filename, issue_files.base)
                    for f in os.listdir(issue_files.id_path):
                        if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                            self.dao.append_id_records(issue_files.id_path + '/' + f, issue_files.base)
                    updated.append(issue_label)
        return updated


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


def normalized_affiliations(org_manager, affiliations):
    affs = []
    for item in affiliations:
        if item.id is not None and (item.orgname is not None or item.norgname is not None):
            result_items = institutions_service.validate_organization(org_manager, item.orgname, item.norgname, item.country, item.i_country, item.state, item.city)
            if len(result_items) > 1:
                result_items = list(set([(norm_orgname, norm_country_code) for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in result_items]))
            if len(result_items) == 1:
                norm_city = None
                norm_state = None
                if len(result_items[0]) > 2:
                    norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name = result_items[0]
                else:
                    norm_orgname, norm_country_code = result_items[0]
                a = {}
                a['i'] = item.id
                a['p'] = norm_country_code
                a['_'] = norm_orgname
                a['c'] = norm_city
                a['s'] = norm_state
                affs.append(a)

    return affs
