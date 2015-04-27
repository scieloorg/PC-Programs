# coding=utf-8

import os
from datetime import datetime

import utils
from article_utils import doi_pid, display_pages, format_dateiso
from article_utils import how_similar
from article import Issue, PersonAuthor
from attributes import ROLE, DOCTOPIC, doctopic_label

from dbm_isis import IDFile

import institutions_service


def normalize_role(_role):
    r = ROLE.get(_role)
    return _role if r == '??' else r


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


class RegisteredArticle(object):
    def __init__(self, article_records):
        self.article_records = article_records

    @property
    def article_type(self):
        return doctopic_label(self.article_records[0]['71'])

    @property
    def xml_name(self):
        return os.path.basename(self.filename).replace('.xml', '')

    @property
    def filename(self):
        return self.article_records[0]['702']

    @property
    def titles(self):
        return self.article_records[1]['12']

    @property
    def first_title(self):
        return self.titles[0]['_']

    @property
    def title(self):
        return self.first_title

    @property
    def doi(self):
        return self.article_records[1]['237']

    @property
    def pid(self):
        return self.article_records[1]['880']

    @property
    def old_pid(self):
        return self.article_records[1]['881']

    @property
    def creation_date(self):
        return (self.article_records[0]['91'], self.article_records[0]['92'])

    @property
    def last_update(self):
        #2015-03-26T14:43:50.272660
        last = self.article_records[0].get('93')
        if last is not None:
            last = last.replace('-', '').replace('T', '')[0:8]
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
        self.add_issue_data()
        self.add_article_data()
        self.set_common_data(article_files.xml_name, article_files.issue_files.issue_folder, article_files.relative_xml_filename)

    def add_issue_data(self):
        self._metadata = {}
        for k in ['30', '42', '62', '100', '35', '935', '421']:
            if k in self.i_record.keys():
                self._metadata[k] = self.i_record[k]

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
            new['i'] = item['href'] if item['ext-link-type'] == 'doi' else item['id']
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
            new['z'] = item.suffix
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
            self._metadata['223'] = self.article.ahpdate
        else:
            self._metadata['31'] = self.article.volume
            self._metadata['32'] = self.article.number
            self._metadata['131'] = self.article.volume_suppl
            self._metadata['132'] = self.article.number_suppl
            self._metadata['223'] = self.article.article_pub_date

        self._metadata['58'] = self.article.funding_source
        self._metadata['591'] = [{'_': item for item in self.article.principal_award_recipient}]
        self._metadata['591'] += [{'n': item for item in self.article.principal_investigator}]
        self._metadata['60'] = self.article.award_id
        self._metadata['102'] = self.article.funding_statement

        self._metadata['62'] = self.article.publisher_name
        self._metadata['65'] = format_dateiso(self.article.issue_pub_date)
        self._metadata['223'] = format_dateiso(self.article.article_pub_date)

        self._metadata['14'] = {}
        self._metadata['14']['f'] = self.article.fpage
        self._metadata['14']['l'] = self.article.lpage
        self._metadata['14']['e'] = self.article.elocation_id

        self._metadata['70'] = format_affiliations(self.article.affiliations)
        self._metadata['240'] = normalized_affiliations(self.org_manager, self.article.affiliations)
        #CT^uhttp://www.clinicaltrials.gov/ct2/show/NCT01358773^aNCT01358773
        self._metadata['770'] = {'u': self.article.clinical_trial_url}
        self._metadata['72'] = str(0 if self.article.total_of_references is None else self.article.total_of_references)
        self._metadata['901'] = str(0 if self.article.total_of_tables is None else self.article.total_of_tables)
        self._metadata['902'] = str(0 if self.article.total_of_figures is None else self.article.total_of_figures)

        self._metadata['83'] = []
        for item in self.article.abstracts:
            self._metadata['83'].append({'l': item.language, '_': item.text})

        self._metadata['111'] = format_dateiso(self.article.received)
        self._metadata['113'] = format_dateiso(self.article.accepted)

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
            rec_c['40'] = item.language
            rec_c['10'] = []
            rec_c['11'] = []
            rec_c['16'] = []
            rec_c['17'] = []
            for person in item.authors_list:
                is_analytic = False
                if item.article_title is not None or item.chapter_title is not None:
                    is_analytic = True
                field = self.author_tag(person.role, isinstance(person, PersonAuthor), is_analytic)
                if isinstance(person, PersonAuthor):
                    a = {}
                    a['n'] = person.fname
                    a['s'] = person.surname
                    a['z'] = person.suffix
                    a['r'] = normalize_role(self.author_role(person.role))
                else:
                    # collab
                    a = person.collab
                rec_c[field].append(a)
            rec_c['31'] = item.volume
            rec_c['32'] = {}
            rec_c['32']['_'] = item.issue
            rec_c['32']['s'] = item.supplement
            rec_c['63'] = item.edition
            rec_c['65'] = item.year + '0000' if item.year is not None else None
            rec_c['66'] = item.publisher_loc
            rec_c['62'] = item.publisher_name
            rec_c['514'] = {'f': item.fpage, 'l': item.lpage, 'r': item.page_range}
            rec_c['14'] = display_pages(item.fpage, item.lpage)
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
            records_c.append(rec_c)
        return records_c

    def author_role(self, role):
        if role == 'editor':
            return 'ed'
        if role == 'author':
            return 'nd'
        if role == 'translator':
            return 'tr'
        if role == 'compiler':
            return 'org'
        return role

    def author_tag(self, role, is_person, is_analytic_author):
        other = ['transed', 'translator']
        monographic = ['compiler', 'director', 'editor', 'guest-editor', ]
        analytical = ['allauthors', 'assignee', 'author', 'inventor', ]
        r = {}
        r[True] = {True: '10', False: '16'}
        r[False] = {True: '11', False: '17'}
        if role in analytical:
            is_analytic = True
        elif role in monographic:
            is_analytic = False
        else:
            is_analytic = is_analytic_author
        return r[is_analytic][is_person]

    def outline(self, total_of_records):
        rec_o = {}
        if self.creation_date is None:
            rec_o['91'] = datetime.now().isoformat()[0:10].replace('-', '')
            rec_o['92'] = datetime.now().isoformat()[11:19].replace(':', '')
        else:
            rec_o['91'] = self.creation_date[0]
            rec_o['92'] = self.creation_date[1]
            rec_o['93'] = datetime.now().isoformat()
        rec_o['703'] = total_of_records
        return rec_o

    @property
    def records(self):
        r = []

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


class IssueModels(object):

    def __init__(self, record):
        self.record = record

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
        acron = self.record.get('930').lower()
        dateiso = self.record.get('65', '')
        volume = self.record.get('31')
        volume_suppl = self.record.get('131')
        number = self.record.get('32')
        number_suppl = self.record.get('132')
        i = Issue(acron, volume, number, dateiso, volume_suppl, number_suppl)

        i.issn_id = self.record.get('35')
        return i


class IssueArticlesRecords(object):

    def __init__(self, records):
        self.records = records

    def articles(self):
        items = []
        article_records = None
        i_record = None
        record_types = list(set([record.get('702') for record in self.records]))

        for record in self.records:
            if record.get('702') == 'i':
                i_record = record
            elif record.get('702') == 'o':
                # new article
                if article_records is not None:
                    items.append(RegisteredArticle(article_records))
                article_records = [record]
            elif record.get('702') == 'h':
                if not 'o' in record_types:
                    if article_records is not None:
                        items.append(RegisteredArticle(article_records))
                    if article_records is None:
                        article_records = []
                article_records.append(record)

        if article_records is not None:
            items.append(article_records)
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
        r = ' OR '.join(_expr) if len(_expr) > 0 else None
        return r

    def search(self, issue_label, pissn, eissn):
        expr = self.expr(issue_label, pissn, eissn)
        print('debug: expr=')
        print(expr)
        search_result = self.dao.get_records(self.db_filename, expr) if expr is not None else None
        if 'ahead' in issue_label:
            print('search_result')
            print(search_result)
        return search_result


class ArticleDAO(object):

    def __init__(self, dao, org_manager):
        self.org_manager = org_manager
        self.dao = dao

    def create_id_file(self, i_record, article, article_files, creation_date=None):
        saved = False
        if not os.path.isdir(article_files.issue_files.id_path):
            os.makedirs(article_files.issue_files.id_path)
        if not os.path.isdir(os.path.dirname(article_files.issue_files.base)):
            os.makedirs(os.path.dirname(article_files.issue_files.base))

        if article.order != '00000':
            article_records = ArticleRecords(self.org_manager, article, i_record, article_files, creation_date)
            self.dao.save_id(article_files.id_filename, article_records.records)
            if os.path.isfile(article_files.id_filename):
                saved_records = self.dao.get_id_records(article_files.id_filename)
                saved = (len(saved_records) == len(article_records.records))
        return saved

    def finish_conversion(self, issue_record, issue_files):
        loaded = []
        self.dao.save_records([issue_record], issue_files.base)
        for f in os.listdir(issue_files.id_path):
            if f == '00000.id':
                os.unlink(issue_files.id_path + '/' + f)
            if f.endswith('.id') and f != '00000.id' and f != 'i.id':
                self.dao.append_id_records(issue_files.id_path + '/' + f, issue_files.base)
                loaded.append(f)
        return loaded

    def registered_items(self, issue_files):
        records = self.dao.get_records(issue_files.base)
        print('records of ')
        print(issue_files.base)
        print(records)
        i, article_records_items = IssueArticlesRecords(records).articles()
        print(i)
        print(article_records_items)
        return (IssueModels(i), [RegisteredArticle(item) for item in article_records_items])

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
        self.create_ahead_id_files(i_ahead_records)

    def journal_has_aop(self):
        total = 0
        for dbname, items in self.still_ahead.items():
            total += len(items)
        return total > 0

    def create_ahead_id_files(self, i_ahead_records):
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
                self.indexed_by_xml_name[ahead.filename] = ahead
                self.still_ahead[dbname][ahead.order] = ahead

    def still_ahead_items(self):
        items = []
        for dbname in sorted(self.still_ahead.keys()):
            for order in sorted(self.still_ahead[dbname].keys()):
                items.append(dbname + '/' + self.still_ahead[dbname][order].filename + ' [' + order + ']: ' + self.still_ahead[dbname][order].article_title[0:50] + '...')
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
        return r

    def find_ahead(self, doi, filename):
        data = None
        i = None
        if doi is not None:
            i = self.indexed_by_doi.get(doi)
        if i is None:
            i = self.indexed_by_xml_name.get(filename)
        if i is not None:
            data = self.still_ahead[i]
        return data

    def get_valid_ahead(self, article):
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
                    matched_rate = self.score(article, ahead, 90)
                    if matched_rate > 0:
                        if ahead.ahead_pid is None:
                            status = 'aop missing PID'
                        else:
                            status = 'matched aop'
                            if matched_rate != 100:
                                status = 'partially matched aop'
                    else:
                        status = 'unmatched aop'
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
        msg.append('Exclude aop files of ' + ahead.filename)
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
