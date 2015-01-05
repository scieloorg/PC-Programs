# coding=utf-8

from datetime import datetime

from article_utils import doi_pid, display_pages, format_dateiso
from article import Issue, PersonAuthor


DOCTOPIC = {
                'research-article': 'oa',
                'editorial': 'ed',
                'abstract': 'ab',
                'announcement': 'an',
                'article-commentary': 'co',
                'case-report': 'cr',
                'letter': 'le',
                'review-article': 'ra',
                'rapid-communication': 'sc',
                'addendum': 'ax',
                'book-review': 'rc',
                'books-received': '??',
                'brief-report': 'rn',
                'calendar': '??',
                'collection': '??',
                'correction': 'er',
                'discussion': '??',
                'dissertation': '??',
                'in-brief': 'pr',
                'introduction': '??',
                'meeting-report': '??',
                'news': '??',
                'obituary': '??',
                'oration': '??',
                'partial-retraction': '??',
                'product-review': '??',
                'reply': '??',
                'reprint': '??',
                'retraction': '??',
                'translation': '??',
}

ROLE = {
    'author': 'ND',
    'editor': 'ED',
    'assignee': 'assignee',
    'compiler': 'compiler',
    'director': 'director',
    'guest-editor': 'guest-editor',
    'inventor': 'inventor',
    'transed': 'transed',
    'translator': 'TR',    
}


def normalize_role(_role):
    r = ROLE.get(_role)
    return _role if r == '??' else r


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


class ArticleRecords(object):

    def __init__(self, article, i_record, article_files):
        self.article = article
        self.article_files = article_files
        self.i_record = i_record
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

        self._metadata['70'] = []
        for item in self.article.affiliations:
            a = {}
            a['l'] = item.label
            a['i'] = item.id
            a['p'] = item.country
            a['e'] = item.email
            a['c'] = item.city
            a['s'] = item.state
            a['4'] = item.norgname
            a['3'] = item.orgdiv3
            a['2'] = item.orgdiv2
            a['1'] = item.orgdiv1
            a['_'] = item.orgname
            #a['9'] = item['original']
            #self._metadata['170'].append(item['xml'])
            self._metadata['70'].append(a)
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
        rec_o['91'] = datetime.now().isoformat()[0:10].replace('-', '')
        rec_o['92'] = datetime.now().isoformat()[11:19].replace(':', '')
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


class IssueRecord(object):

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

    def most_similar_section_code(self, section_title, acceptable_result=0.80):
        best_result = 0
        seccode = None
        similar = None
        if section_title is not None:
            for sec in self.sections:
                if sec.get('t').lower() == section_title.lower():
                    best_result = 1
                    seccode = sec.get('c')
                    similar = sec.get('t')
                    break
            if seccode is None:
                import difflib
                for sec in self.sections:
                    sec_words = sec.get('t', '').lower().split(' ')
                    section_title_words = section_title.lower().split(' ')
                    for sec_word in sec_words:
                        for section_title_word in section_title_words:
                            r = difflib.SequenceMatcher(None, section_title_word, sec_word).ratio()
                            if r > best_result:
                                best_result = r
                                seccode = sec.get('c')
                                similar = sec.get('t')
        return (seccode, best_result, similar)

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
