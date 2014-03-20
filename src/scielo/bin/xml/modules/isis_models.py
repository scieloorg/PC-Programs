# coding=utf-8

from datetime import datetime

from modules.utils import doi_pid, display_pages, format_dateiso


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


class ArticleISIS(object):

    def __init__(self, article_files, article, i_record, section_code, text_or_article):
        self.text_or_article = text_or_article
        self.article = article
        self.section_code = section_code
        self.article_files = article_files
        self.i_record = i_record
        self._metadata = {}
        self.metadata = {}

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = {}

        for k in ['30', '42', '62', '100', '35', '935', '421']:
            if k in self.i_record.keys():
                self._metadata[k] = self.i_record[k]
        self._metadata['120'] = 'XML_' + self.article.dtd_version
        self._metadata['71'] = normalize_doctopic(self.article.article_type)
        self._metadata['40'] = self.article.language
        self._metadata['38'] = self.article.illustrative_materials

        self._metadata['709'] = 'text' if self.article.is_text else 'article'

        self._metadata['241'] = []
        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['r'] = item.get('link-type')
            new['i'] = item.get('document-id', item.get('object-id', item.get('source-id')))
            new['n'] = item.get('document-id-type', item.get('object-id-type', item.get('source-id-type')))
            new['t'] = item.get('document-type', item.get('object-type', item.get('source-type')))
            self._metadata['241'].append(new)

        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['i'] = item.get('{http://www.w3.org/1999/xlink}href')
            new['n'] = item.get('ext-link-type')
            new['t'] = 'pr' if item.get('related-article-type') == 'press-release' else 'article'
            self._metadata['241'].append(new)
        if self.article.is_article_press_release or self.article.is_issue_press_release:
            self._metadata['41'] = 'pr'

        if self.article.is_article_press_release or self.article.is_issue_press_release:
            self._metadata['241'] = 'pr'

        self._metadata['85'] = self.article.keywords
        self._metadata['49'] = self.section_code

        self._metadata['10'] = []
        for item in self.article.contrib_names:
            new = {}
            new['n'] = item['given-names']
            new['s'] = item['surname']
            new['z'] = item['suffix']
            new['p'] = item['prefix']
            new['r'] = normalize_role(item['contrib-type'])
            new['1'] = item['xref']
            new['k'] = item['contrib-id']
            self._metadata['10'].append(new)

        self._metadata['11'] = self.article.contrib_collab
        self._metadata['12'] = []
        for item in self.article.title:
            new = {}
            new['_'] = item['article-title']
            new['s'] = item['subtitle']
            new['l'] = item['language']
            self._metadata['12'].append(new)
        for item in self.article.trans_titles:
            new = {}
            new['_'] = item['trans-title']
            new['s'] = item['trans-subtitle']
            new['l'] = item['language']
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
            a['l'] = item['label']
            a['i'] = item['id']
            a['p'] = item['country']
            a['e'] = item['email']
            a['c'] = item['city']
            a['s'] = item['state']
            a['3'] = item['orgdiv3']
            a['2'] = item['orgdiv2']
            a['1'] = item['orgdiv1']
            a['_'] = item['orgname']
            #a['9'] = item['original']
            #self._metadata['170'].append(item['xml'])
            self._metadata['70'].append(a)
        #FIXME nao existe clinical trial
        self._metadata['770'] = self.article.clinical_trial
        self._metadata['72'] = self.article.total_of_references
        self._metadata['901'] = self.article.total_of_tables
        self._metadata['902'] = self.article.total_of_figures

        self._metadata['83'] = []
        for item in self.article.abstracts:
            self._metadata['83'].append({'l': item['language'], '_': item['text']})

        _h = self.article.history
        self._metadata['111'] = format_dateiso(_h.get('received'))
        self._metadata['113'] = format_dateiso(_h.get('accepted'))

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
            for person_group_id, person_group in item.person_groups.items():
                for person in person_group:
                    field = self.author_tag(person_group_id, 'given-names' in person, item.article_title or item.chapter_title)
                    if 'collab' in person:
                        a = person['collab']
                    else:
                        a = {}
                        a['n'] = person['given-names']
                        a['s'] = person['surname']
                        a['z'] = person['suffix']
                        a['r'] = normalize_role(self.author_role(person_group_id))
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

    def author_role(self, person_group_id):
        if person_group_id == 'editor':
            return 'ed'
        if person_group_id == 'author':
            return 'nd'
        if person_group_id == 'translator':
            return 'tr'
        if person_group_id == 'compiler':
            return 'org'
        return person_group_id

    def author_tag(self, person_group_id, is_person, has_part_title):
        other = ['transed', 'translator']
        monographic = ['compiler', 'director', 'editor', 'guest-editor', ]
        analytical = ['allauthors', 'assignee', 'author', 'inventor', ]
        if person_group_id in analytical:
            return '10' if is_person else '11'
        if person_group_id in monographic:
            return '16' if is_person else '17'

        if has_part_title:
            return '10' if is_person else '11'
        else:
            return '16' if is_person else '17'

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

    @property
    def common_data(self):
        r = {}
        r['2'] = self.article_files.xml_name
        r['4'] = self.article_files.issue_folder
        r['702'] = self.article_files.relative_xml_filename
        r['705'] = 'S'
        return r

    def record_info(self, record_index, record_name, record_name_index, record_name_total):
        r = {}
        r['706'] = record_name
        r['700'] = record_index # starts with 0
        r['701'] = record_name_index # starts with 1
        r['708'] = record_name_total
        # r.update(dict)
        return r


class IssueISIS(object):
    def __init__(self, record):
        self.record = record

    def section_code(self, section_title):
        seccode = None

        for sec in self.record.get('49', []):
            if sec.get('t').lower() == section_title.lower():
                seccode = sec.get('c')
                break
        if seccode is None:
            print(section_title.lower())
            print(self.record.get('49', []))
        return seccode
