# coding=utf-8

import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as etree

from StringIO import StringIO


MONTHS = {'': '00', 'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }


def format_dateiso(self, adate):
    month = adate.get('season', adate.get('month', '00'))
    if not month.isdigit():
        if '-' in month:
            month = month[0:month.find('-')]
        month = MONTHS.get(month, '00')
    if month == '':
        month = '00'
    return adate.get('year', '0000') + month + adate.get('day', '00')


def xml_string(node):
    return etree.tostring(node) if node is not None else ''


def load_xml(content):
    def handle_mml_entities(content):
        if '<mml:' in content:
            temp = content.replace('<mml:math', 'BREAKBEGINCONSERTA<mml:math')
            temp = temp.replace('</mml:math>', '</mml:math>BREAKBEGINCONSERTA')
            replaces = [item for item in temp.split('BREAKBEGINCONSERTA') if '<mml:math' in item and '&' in item]
            for repl in replaces:
                content = content.replace(repl, repl.replace('&', 'MYMATHMLENT'))
        if '<math' in content:
            temp = content.replace('<math', 'BREAKBEGINCONSERTA<math')
            temp = temp.replace('</math>', '</math>BREAKBEGINCONSERTA')
            replaces = [item for item in temp.split('BREAKBEGINCONSERTA') if '<math' in item and '&' in item]
            for repl in replaces:
                content = content.replace(repl, repl.replace('&', 'MYMATHMLENT'))
        return content

    NAMESPACES = {'mml': 'http://www.w3.org/TR/MathML3/'}
    for prefix, uri in NAMESPACES.items():
        etree.register_namespace(prefix, uri)

    if not '<' in content:
        # is a file
        try:
            r = etree.parse(content)
        except Exception as e:
            content = open(content, 'r').read()

    if '<' in content:
        content = handle_mml_entities(content)

        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            print('XML is not well formed')
            print(e)
            r = None
    return r


class ArticleRecords(object):

    def __init__(self):
        self.records = {}

    def load(self, article):
        self.records['f'] = {}
        self.records['f']['120'] = article.dtd_version
        self.records['f']['71'] = article.article_type
        self.records['f']['40'] = article.language

        self.records['f']['241'] = []
        for item in article.related_objects:
            new = {}
            new['k'] = item['id']
            new['r'] = item.get('link-type')
            new['i'] = item.get('document-id', item.get('object-id', item.get('source-id')))
            new['n'] = item.get('document-id-type', item.get('object-id-type', item.get('source-id-type')))
            new['t'] = item.get('document-type', item.get('object-type', item.get('source-type')))
            self.records['f']['241'].append(new)

        for item in article.related_objects:
            new = {}
            new['k'] = item['id']
            new['i'] = item.get('{http://www.w3.org/1999/xlink}href')
            new['n'] = item.get('ext-link-type')
            new['t'] = 'pr' if item.get('related-article-type') == 'press-release' else 'article'
            self.records['f']['241'].append(new)

        #self.records['f']['100'] = article.journal_title
        self.records['f']['30'] = article.abbrev_journal_title
        #self.records['f']['62'] = article.publisher_name
        #self.records['f']['421'] = article.journal_id_nlm_ta
        #self.records['f']['930'] = article.journal_id_nlm_ta
        #self.records['f']['935'] = article.journal_issns

        self.records['f']['85'] = article.keywords
        self.records['f']['49'] = issue.section_code(article.toc_section)

        self.records['f']['10'] = []
        for item in article.contrib_names:
            new = {}
            new['n'] = item['given-names']
            new['s'] = item['surname']
            new['z'] = item['suffix']
            new['p'] = item['prefix']
            new['r'] = item['contrib-type']
            new['1'] = item['xref']
            new['k'] = item['contrib-id']
            self.records['f']['10'].append(new)

        self.records['f']['11'] = self.contrib_collab
        self.records['f']['12'] = []
        for item in article.title:
            new = {}
            new['_'] = item['article-title']
            new['s'] = item['subtitle']
            new['l'] = item['language']
            self.records['f']['12'].append(new)
        for item in article.trans_titles:
            new = {}
            new['_'] = item['trans-title']
            new['s'] = item['trans-subtitle']
            new['l'] = item['language']
            self.records['f']['12'].append(new)

        self.records['f']['601'] = article.trans_languages
        self.records['f']['237'] = article.doi

        self.records['f']['121'] = article.order if article.order is not None else article.fpage

        self.records['f']['31'] = article.volume
        self.records['f']['32'] = article.number
        self.records['f']['131'] = article.volume_suppl
        self.records['f']['132'] = article.number_suppl

        self.records['f']['58'] = article.funding_source
        self.records['f']['591'] = [{'_': item for item in article.principal_award_recipient}]
        self.records['f']['591'] = [{'n': item for item in article.principal_investigator}]
        self.records['f']['60'] = article.award_id
        self.records['f']['102'] = article.funding_statement

        self.records['f']['65'] = format_dateiso(article.issue_pub_date)
        self.records['f']['223'] = format_dateiso(article.article_pub_date)

        self.records['f']['14'] = {}
        self.records['f']['14']['f'] = article.fpage
        self.records['f']['14']['l'] = article.lpage
        self.records['f']['14']['e'] = article.elocation_id

        self.records['f']['70'] = []
        for item in article.affiliations:
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
            #self.records['f']['170'].append(item['xml'])
            self.records['f']['70'].append(item)
        #FIXME nao existe clinical trial
        self.records['f']['770'] = article.clinical_trial
        self.records['f']['72'] = article.total_of_references
        self.records['f']['901'] = article.total_of_tables
        self.records['f']['902'] = article.total_of_figures

        self.records['f']['83'] = []
        for item in article.abstracts:
            self.records['f']['83'].append({'l': item['language'], '_': item['text']})

        self.records['f']['111'] = format_dateiso(article.history['received'])
        self.records['f']['113'] = format_dateiso(article.history['accepted'])

        self.records['c'] = []
        for item in article.references:
            rec_c = {}
            rec_c['71'] = item.publication_type

            if item.article_title or item.chapter_title:
                rec_c['12'] = {'_': item.article_title if item.article_title else item.chapter_title, 'l': item.language}
            if item.article_title:
                rec_c['30'] = item.source
            else:
                rec_c['18'] = item.source
            rec_c['71'] = item.publication_type

            rec_c['10'] = []
            rec_c['11'] = []
            rec_c['16'] = []
            rec_c['17'] = []
            for person_group_id, person_group in item.person_groups.items():

                for person in person_group:
                    field = self.author_tag(person_group_id, 'given-names' in person)
                    if 'collab' in person:
                        a = person['collab']
                    else:
                        a = {}
                        a['n'] = person['given-names']
                        a['s'] = person['surname']
                        a['z'] = person['suffix']
                        a['r'] = self.author_role(person_group_id)

                    rec_c[field].append(a)
            rec_c['31'] = item.volume
            rec_c['32'] = {}
            rec_c['32']['_'] = item.issue
            rec_c['32']['s'] = item.supplement
            rec_c['63'] = item.edition
            rec_c['65'] = item.year + '0000'
            rec_c['66'] = item.publisher_loc
            rec_c['62'] = item.publisher_name
            rec_c['514'] = {'f': item.fpage, 'l': item.lpage, 'r': item.page_range}
            rec_c['14'] = item.fpage + '-' + item.lpage
            if item.size:
                rec_c['20']['_'] = item.size['size']
                rec_c['20']['u'] = item.size['units']
            rec_c['118'] = item.label
            rec_c['810'] = item.etal
            rec_c['109'] = item.cited_date
            rec_c['61'] = item.notes if item.notes else item.comment
            rec_c['237'] = item.doi
            rec_c['238'] = item.pmid
            rec_c['239'] = item.pmcid
            rec_c['53'] = item.conference_name
            rec_c['56'] = item.conference_location
            rec_c['54'] = item.conference_date
        self.records['c'].append(rec_c)

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

    def author_tag(self, person_group_id, is_person):
        other = ['transed', 'translator']
        monographic = ['compiler', 'director', 'editor', 'guest-editor', ]
        analytical = ['allauthors', 'assignee', 'author', 'inventor', ]
        if person_group_id in analytical:
            return '10' if is_person else '11'
        if person_group_id in monographic:
            return '16' if is_person else '17'
        return '10' if is_person else '11'

    @property
    def record_o(self, article):
        r = {}
        self.records['91'] = datetime.now().isoformat()[0:10].replace('-', '')
        self.records['92'] = datetime.now().isoformat()[11:19].replace(':', '')
        self.records['703'] = total_of_all_records
        return r

    def save_records(self):
        self.records['o'] = self.record_o
        self.records['h'] = self.records['f']
        self.records['l'] = self.records['f']

    def common(self, xml_filename, text_or_article, issue_label, id_filename):
        r = {}
        r['2'] = id_filename
        r['4'] = issue_label
        r['702'] = xml_filename
        r['705'] = 'S'
        r['709'] = text_or_article
        return r

    def record_info(self, record_name, record_index, record_name_index, record_name_total):
        r = {}
        r['706'] = record_name
        r['700'] = record_index # starts with 0
        r['701'] = record_name_index # starts with 1
        r['708'] = record_name_total
        # r.update(dict)
        return r


class Issue(object):

    def section_code(self, section_title):
        r = [section.get('code') for section in self.sections if section.get('title') == section_title]
        return r[0] if len(r) > 0 else None


class Article(object):

    def __init__(self, tree):
        self.tree = tree
        self.journal_meta = self.tree.find('./front/journal-meta')
        self.article_meta = self.tree.find('./front/article-meta')
        self.body = self.tree.find('./body')
        self.back = self.tree.find('./back')
        self.subarticles = self.tree.findall('./sub-article')
        self.responses = self.tree.findall('./response')

    @property
    def dtd_version(self):
        return self.tree.attrib.get('dtd-version')

    @property
    def article_type(self):
        return self.tree.attrib.get('article-type')

    @property
    def language(self):
        return self.tree.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

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
        r = []
        related = self.article_meta.findall('related-object')
        for rel in related:
            item = {k: v for k, v in rel.attrib.items()}
            r.append(item)
        return r

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
        r = []
        related = self.article_meta.findall('related-article')
        for rel in related:
            item = {k: v for k, v in rel.attrib.items()}
            r.append(item)
        return r

    @property
    def journal_title(self):
        return self.journal_meta.findtext('journal-title')

    @property
    def abbrev_journal_title(self):
        return self.journal_meta.findtext('abbrev-journal-title')

    @property
    def publisher_name(self):
        return self.journal_meta.findtext('publisher-name')

    @property
    def journal_id(self):
        return self.journal_meta.findtext('journal-id')

    @property
    def journal_id_nlm_ta(self):
        return self.journal_meta.findtext('journal-id[@journal-id-type="nlm-ta"]')

    @property
    def journal_issns(self):
        return {item.attrib.get('pub-type', 'epub'):item.text for item in self.journal_meta.findall('issn')}

    @property
    def toc_section(self):
        node = self.article_meta.find('subj-group[@subj-group-type="heading"]')    
        if node is not None:
            return node.findtext('subject')
        return None

    @property
    def keywords(self):
        if self._keywords is None:
            k = []
            for node in self.article_meta.findall('kwd-group'):
                language = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': kw.text})
        return self._keywords

    @property
    def contrib_names(self):
        k = []
        for contrib in self.article_meta.findall('.//contrib'):
            item = {}
            if contrib.findall('name'):
                item['given-names'] = contrib.find('name/given-names')
                item['surname'] = contrib.find('name/surname')
                item['suffix'] = contrib.find('name/suffix')
                item['prefix'] = contrib.find('name/prefix')
                item['contrib-id'] = contrib.contrib.findtext('contrib-id[@contrib-id-type="orcid"]')
                item['contrib-type'] = contrib.attrib.get('contrib-type')
                item['xref'] = []
                for xref_item in contrib.findall('xref[@ref-type="aff"]'):
                    item['xref'].append(xref_item.attrib.get('rid'))
                item['xref'] = ' '.join(item['xref'])
                k.append(item)
        return k

    @property
    def contrib_collab(self):
        k = []
        for contrib in self.article_meta.findall('.//contrib/collab'):
            k.append(contrib.text)
        return k

    @property
    def title(self):
        k = []
        for node in self.article_meta.findall('.//title-group'):
            item = {}
            item['article-title'] = node.findtext('article-title')
            item['subtitle'] = node.findtext('subtitle')
            if item['article-title'] is not None:
                item['language'] = item['article-title'].attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

            k.append(item)
        return k

    @property
    def trans_titles(self):
        k = []
        for node in self.article_meta.findall('.//trans-title-group'):
            item = {}
            item['trans-title'] = node.findtext('trans-title')
            item['trans-subtitle'] = node.findtext('trans-subtitle')
            if item['trans-title'] is not None:
                item['language'] = item['trans-title'].attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

            k.append(item)

        for subart in self.subarticles:
            if subart.get('article-type') == 'translation':
                for node in subart.find('.//title-group'):
                    item = {}
                    item['article-title'] = node.findtext('article-title')
                    item['subtitle'] = node.findtext('subtitle')
                    if item['article-title'] is not None:
                        item['language'] = item['article-title'].attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

                    k.append(item)
        return k

    @property
    def trans_languages(self):
        k = []
        for node in self.subarticles:
            k.append(node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
        return k

    @property
    def doi(self):
        return self.article_meta.findtext('article-id[@pub-id-type="doi"]')

    @property
    def order(self):
        return self.article_meta.findtext('article-id[@pub-id-type="other"]')

    @property
    def volume(self):
        return self.article_meta.findtext('volume')

    @property
    def issue(self):
        return self.article_meta.findtext('issue')

    @property
    def supplement(self):
        return self.article_meta.findtext('supplement')

    def _issue_parts(self):
        self.number = None
        self.number_suppl = None
        self.volume_suppl = None
        suppl = None
        parts = issue.split(' ')
        if len(parts) == 1:
            if 'sup' in parts[0].lower():
                suppl = parts[0]
            else:
                self.number = parts[0]
        elif len(parts) == 2:
            #n suppl or suppl s
            if 'sup' in parts[0].lower():
                suppl = parts[1]
            else:
                self.number, suppl = parts
        elif len(parts) == 3:
            # n suppl s
            self.number, ign, suppl = parts
        if suppl is not None:
            if self.number is None:
                self.number_suppl = suppl
            else:
                self.volume_suppl = suppl

    @property
    def funding_source(self):
        return [item.text for item in self.article_meta.findall('.//funding-source')]

    @property
    def principal_award_recipient(self):
        return [item.text for item in self.article_meta.findall('.//principal-award-recipient')]

    @property
    def principal_investigator(self):
        return [item.text for item in self.article_meta.findall('.//principal-investigator')]

    @property
    def award_id(self):
        return [item.text for item in self.article_meta.findall('.//award-id')]

    @property
    def funding_statement(self):
        return [item.text for item in self.article_meta.findall('.//funding-statement')]

    @property
    def ack_xml(self):
        #107
        return xml_string(self.back.find('.//ack'))

    @property
    def issue_pub_date(self):
        _issue_pub_date = None
        date = self.article_meta.find('pub-date[@date-type="pub"]')
        if date is None:
            date = self.article_meta.find('pub-date[@pub-type="epub-ppub"]')
        if date is None:
            date = self.article_meta.find('pub-date[@pub-type="ppub"]')
        if date is None:
            date = self.article_meta.find('pub-date[@pub-type="collection"]')
        if date is not None:
            _issue_pub_date = {}
            _issue_pub_date['season'] = date.findtext('season')
            _issue_pub_date['month'] = date.findtext('month')
            _issue_pub_date['year'] = date.findtext('year')
            _issue_pub_date['day'] = date.findtext('day')
        return _issue_pub_date

    @property
    def article_pub_date(self):
        _article_pub_date = None
        date = self.article_meta.find('pub-date[@date-type="preprint"]')
        if date is None:
            date = self.article_meta.find('pub-date[@pub-type="epub"]')
        if date is not None:
            _article_pub_date = {}
            _article_pub_date['season'] = date.findtext('season')
            _article_pub_date['month'] = date.findtext('month')
            _article_pub_date['year'] = date.findtext('year')
            _article_pub_date['day'] = date.findtext('day')
        return _article_pub_date

    @property
    def fpage(self):
        return self.article_meta.find('fpage')

    @property
    def fpage_seq(self):
        return self.article_meta.find('fpage').attrib.get('seq') if self.article_meta.find('fpage') is not None else None

    @property
    def lpage(self):
        return self.article_meta.find('lpage')

    @property
    def elocation_id(self):
        return self.article_meta.find('elocation-id')

    @property
    def affiliations(self):
        affs = []
        for aff in self.article_meta.findall('aff'):
            a = {}
            a['xml'] = xml_string(aff)
            a['id'] = aff.get('id')
            for tag in ['label', 'country', 'email']:
                a[tag] = aff.findtext(tag)
            for inst in aff.findall('institution'):
                # institution[@content-type='orgdiv3']
                tag = inst.get('content-type')
                if tag is not None:
                    a[tag] = inst.text
            for named_content in aff.findall('addr-line/named-content'):
                tag = named_content.get('content-type')
                if tag is not None:
                    a[tag] = named_content.text
            affs.append(a)
        return affs

    @property
    def clinical_trial(self):
        #FIXME nao existe clinical-trial 
        return xml_string(self.article_meta.find('clinical-trial'))

    @property
    def total_of_references(self):
        return self.article_meta.find('.//ref-count').attrib.get('count') if self.article_meta.find('.//ref-count') is not None else None

    @property
    def total_of_tables(self):
        return self.article_meta.find('.//table-count').attrib.get('count') if self.article_meta.find('.//table-count') is not None else None

    @property
    def total_of_figures(self):
        return self.article_meta.find('.//fig-count').attrib.get('count') if self.article_meta.find('.//fig-count') is not None else None

    @property
    def abstracts(self):
        r = []
        _abstract = {}
        for a in self.tree.findall('.//abstract'):
            _abstract['language'] = a.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            _abstract['text'] = xml_string(a) if a.find('.//*') else a.text
            r.append(_abstract)
        for a in self.tree.findall('.//trans-abstract'):
            _abstract['language'] = a.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            _abstract['text'] = xml_string(a) if a.find('.//*') else a.text
            r.append(_abstract)
        return r

    @property
    def history(self):
        _hist = {}
        for item in self.article_meta.findall('.//date'):
            _id = item.attrib.get('date-type')
            _hist[_id] = {}
            for tag in ['year', 'month', 'day', 'season']:
                _hist[_id][tag] = item.findtext(tag)
        return _hist

    @property
    def references(self):
        refs = []
        for ref in self.back.findall('.//ref'):
            refs.append(Reference(ref))
        return refs


class Reference(object):

    def __init__(self, root):
        self.root = root

    @property
    def source(self):
        return self.root.findtext('.//source')

    @property
    def language(self):
        lang = self.root.find('.//source').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//source') else None
        if lang is None:
            lang = self.root.find('.//article-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//article-title') else None
        if lang is None:
            lang = self.root.find('.//chapter-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//chapter-title') else None
        return lang

    @property
    def article_title(self):
        return self.root.findtext('.//article-title')

    @property
    def chapter_title(self):
        return self.root.findtext('.//chapter-title')

    @property
    def trans_title(self):
        return self.root.findtext('.//trans-title')

    @property
    def trans_title_language(self):
        return self.root.find('.//trans-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//trans-title') else None

    @property
    def publication_type(self):
        return self.root.find('.//element-citation').attrib.get('publication-type') if self.root.find('.//element-citation') else None

    @property
    def xml(self):
        return xml_string(self.root)

    @property
    def mixed_citation(self):
        return xml_string(self.root.find('.//mixed-citation'))

    @property
    def person_groups(self):
        r = {}
        k = 0
        for person_group in self.root.findall('.//person-group'):
            k += 1
            person_group_id = person_group.attrib.get('person-group-type', k)
            r[person_group_id] = []
            for person in person_group.findall('.//name'):
                p = {}
                for tag in ['given-names', 'surname', 'suffix']:
                    p[tag] = person.findtext(tag)

                r[person_group_id].append(p)
            for collab in person_group.findall('.//collab'):
                r[person_group_id].append(collab.text)
        return r

    @property
    def volume(self):
        return self.root.findtext('.//volume')

    @property
    def issue(self):
        return self.root.findtext('.//issue')

    @property
    def supplement(self):
        return self.root.findtext('.//supplement')

    @property
    def edition(self):
        return self.root.findtext('.//edition')

    @property
    def year(self):
        return self.root.findtext('.//year')

    @property
    def publisher_name(self):
        return self.root.findtext('.//publisher-name')

    @property
    def publisher_loc(self):
        return self.root.findtext('.//publisher-loc')

    @property
    def fpage(self):
        return self.root.findtext('.//fpage')

    @property
    def lpage(self):
        return self.root.findtext('.//lpage')

    @property
    def page_range(self):
        return self.root.findtext('.//page-range')

    @property
    def size(self):
        node = self.root.find('size')
        if node is not None:
            return {'size': node.text, 'units': node.attrib.get('units')} 

    @property
    def label(self):
        return self.root.findtext('.//label')

    @property
    def etal(self):
        return self.root.findtext('.//etal')

    @property
    def cited_date(self):
        return self.root.findtext('.//date-in-citation[@content-type="access-date"]')

    @property
    def ext_link(self):
        return self.root.findtext('.//ext-link')

    @property
    def comments(self):
        return self.root.findtext('.//comment')

    @property
    def notes(self):
        return self.root.findtext('.//notes')

    @property
    def contract_number(self):
        return self.root.findtext('.//comment[@content-type="award-id"]')

    @property
    def doi(self):
        return self.root.findtext('.//pub-id[@pub-id-type="doi"]')

    @property
    def pmid(self):
        return self.root.findtext('.//pub-id[@pub-id-type="pmid"]')

    @property
    def pmcid(self):
        return self.root.findtext('.//pub-id[@pub-id-type="pmcid"]')

    @property
    def conference_name(self):
        return self.root.findtext('.//conf-name')

    @property
    def conference_location(self):
        return self.root.findtext('.//conf-loc')

    @property
    def conference_date(self):
        return self.root.findtext('.//conf-date')


class XMLConverter(object):

    def __init__(self):
        pass

    def convert(self, xml_files_path):
        records = ''
        for xml_file in os.listdir(xml_files_path):
            records += self.format_records(xml_file)
        return records

    def format_records(self):
        return ''


class Record(object):

    def __init__(self, data):
        self.data = data

    def record(self):
        r = ''
        for tag, occs in self.data.items():
            if occs is str:
                r += self.tagged(tag, occs)
            elif occs is list:
                for occ in occs:
                    if occ is str:
                        r += self.format(tag, occ)
                    elif occ is dict:
                        value = ''
                        first = ''
                        for k, v in occ.items():
                            if v != '':
                                if k == '_':
                                    first = k + v
                                else:
                                    value += '^' + k + v
                        r += self.tagged(tag, first + value)
        return r

    def tagged(self, tag, value):
        if value is not None':
            tag = '000' + tag
            tag = tag[-3:]
            return '!v' + tag + '!' + value + '\n'
        return ''


class FilesLocation(object):

    def __init__(self, acron, issue_label):
        self.acron = acron
        self.issue_label = issue_label

    
