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


class ArticleISIS(object):

    def __init__(self, xml_filename, text_or_article, issue_label, id_filename, article, section_code):
        self.xml_filename = xml_filename
        self.text_or_article = text_or_article
        self.issue_label = issue_label
        self.id_filename = id_filename
        self.article = article
        self.section_code = section_code

    def metadata(self):
        rec_f = {}
        rec_f['120'] = self.article.dtd_version
        rec_f['71'] = self.article.article_type
        rec_f['40'] = self.article.language

        rec_f['241'] = []
        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['r'] = item.get('link-type')
            new['i'] = item.get('document-id', item.get('object-id', item.get('source-id')))
            new['n'] = item.get('document-id-type', item.get('object-id-type', item.get('source-id-type')))
            new['t'] = item.get('document-type', item.get('object-type', item.get('source-type')))
            rec_f['241'].append(new)

        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['i'] = item.get('{http://www.w3.org/1999/xlink}href')
            new['n'] = item.get('ext-link-type')
            new['t'] = 'pr' if item.get('related-article-type') == 'press-release' else 'article'
            rec_f['241'].append(new)

        #rec_f['100'] = self.article.journal_title
        rec_f['30'] = self.article.abbrev_journal_title
        #rec_f['62'] = self.article.publisher_name
        #rec_f['421'] = self.article.journal_id_nlm_ta
        #rec_f['930'] = self.article.journal_id_nlm_ta
        #rec_f['935'] = self.article.journal_issns

        rec_f['85'] = self.article.keywords
        #rec_f['49'] = issue.section_code(self.article.toc_section)
        rec_f['49'] = self.section_code

        rec_f['10'] = []
        for item in self.article.contrib_names:
            new = {}
            new['n'] = item['given-names']
            new['s'] = item['surname']
            new['z'] = item['suffix']
            new['p'] = item['prefix']
            new['r'] = item['contrib-type']
            new['1'] = item['xref']
            new['k'] = item['contrib-id']
            rec_f['10'].append(new)

        rec_f['11'] = self.contrib_collab
        rec_f['12'] = []
        for item in self.article.title:
            new = {}
            new['_'] = item['article-title']
            new['s'] = item['subtitle']
            new['l'] = item['language']
            rec_f['12'].append(new)
        for item in self.article.trans_titles:
            new = {}
            new['_'] = item['trans-title']
            new['s'] = item['trans-subtitle']
            new['l'] = item['language']
            rec_f['12'].append(new)

        rec_f['601'] = self.article.trans_languages
        rec_f['237'] = self.article.doi

        rec_f['121'] = self.article.order if self.article.order is not None else self.article.fpage

        rec_f['31'] = self.article.volume
        rec_f['32'] = self.article.number
        rec_f['131'] = self.article.volume_suppl
        rec_f['132'] = self.article.number_suppl

        rec_f['58'] = self.article.funding_source
        rec_f['591'] = [{'_': item for item in self.article.principal_award_recipient}]
        rec_f['591'] = [{'n': item for item in self.article.principal_investigator}]
        rec_f['60'] = self.article.award_id
        rec_f['102'] = self.article.funding_statement

        rec_f['65'] = format_dateiso(self.article.issue_pub_date)
        rec_f['223'] = format_dateiso(self.article.article_pub_date)

        rec_f['14'] = {}
        rec_f['14']['f'] = self.article.fpage
        rec_f['14']['l'] = self.article.lpage
        rec_f['14']['e'] = self.article.elocation_id

        rec_f['70'] = []
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
            #rec_f['170'].append(item['xml'])
            rec_f['70'].append(item)
        #FIXME nao existe clinical trial
        rec_f['770'] = self.article.clinical_trial
        rec_f['72'] = self.article.total_of_references
        rec_f['901'] = self.article.total_of_tables
        rec_f['902'] = self.article.total_of_figures

        rec_f['83'] = []
        for item in self.article.abstracts:
            rec_f['83'].append({'l': item['language'], '_': item['text']})

        _h = self.article.history
        rec_f['111'] = format_dateiso(_h['received'])
        rec_f['113'] = format_dateiso(_h['accepted'])

        return rec_f

    def references(self):

        records_c = []
        for item in self.article.references:
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

    def author_tag(self, person_group_id, is_person):
        other = ['transed', 'translator']
        monographic = ['compiler', 'director', 'editor', 'guest-editor', ]
        analytical = ['allauthors', 'assignee', 'author', 'inventor', ]
        if person_group_id in analytical:
            return '10' if is_person else '11'
        if person_group_id in monographic:
            return '16' if is_person else '17'
        return '10' if is_person else '11'

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

        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('2', 'h', '1', '1'))
        r.append(rec)

        #metadata = self.metadata(article)
        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('3', 'f', '1', '1'))
        r.append(rec)

        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('4', 'l', '1', '1'))
        r.append(rec)

        c_total = str(len(self.references))
        c_index = 0
        k = 4
        for rec in self.references:
            c_index += 1
            k += 1
            rec.update(self.common_data)
            rec.update(self.record_info(str(k), 'c', str(c_index), c_total))
            r.append(rec)
        return r

    @property
    def common_data(self):
        r = {}
        r['2'] = self.id_filename
        r['4'] = self.issue_label
        r['702'] = self.xml_filename
        r['705'] = 'S'
        r['709'] = self.text_or_article
        return r

    def record_info(self, record_index, record_name, record_name_index, record_name_total):
        r = {}
        r['706'] = record_name
        r['700'] = record_index # starts with 0
        r['701'] = record_name_index # starts with 1
        r['708'] = record_name_total
        # r.update(dict)
        return r


class Issue(object):

    def __init__(self, sections):
        self.sections = [{'title': 'nd'}]

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

    def __init__(self, cisis):
        self.cisis = cisis

    def create_id_files(self, xml_files_path, issue, id_path):
        records = ''
        for xml_file in os.listdir(xml_files_path):
            article = Article(load_xml(xml_files_path + '/' + xml_file))

            section_code = issue.section_code(article.toc_section)
            #FIXME
            xml_filename = 'xml/acron/' + issue_label + '/' + xml_file
            text_or_article = 'article'
            id_filename = '0'*5 + article.order
            id_filename = id_filename[-5:]

            isis = ArticleISIS(xml_filename, text_or_article, issue_label, id_filename, article, section_code)
            id_file = IDFile(isis.records)
            id_file.save(id_path + '/' + id_filename + '.id')

    def id2mst(self, id_path, base_path, base_name):
        base_filename = base_path + '/' + base_name
        if os.path.exists(base_filename + '.mst'):
            os.unlink(base_filename + '.mst')
            os.unlink(base_filename + '.xrf')
        #FIXME
        if os.path.isfile(id_path + '/i.id'):
            self.cisis.id2mst(id_path + '/i.id', base_filename, False)
        for id_file in os.listdir(id_path):
            if id_file != 'i.id' and id_file != '00000.id':
                self.cisis.id2mst(id_path + '/' + id_file, base_filename, False)


class IDFile(object):

    def __init__(self, records):
        self.records = records

    def save(self, id_filename):
        path = os.path.dirname(id_filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        f = open(id_filename, 'w')
        f.write(self.format_file())
        f.close()

    def format_file(self):
        r = ''
        index = 0
        for item in self.records:
            index += 1
            r += self.format_record(index, item)
        return r

    def format_record(self, index, record):
        i = '000000' + str(index)
        r = '!ID ' + i[-6:] + '\n'
        for tag, occs in record.items():
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


class CISIS:
    def __init__(self, cisis_path):
        cisis_path = cisis_path.replace('\\', '/')

        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path
        else:
            print('Invalid cisis path: ' + cisis_path)

    def crunchmf(self, mst_filename, wmst_filename):
        cmd = self.cisis_path + '/crunchmf ' + mst_filename + ' ' + wmst_filename
        os.system(cmd)

    def id2i(self, id_filename, mst_filename):
        cmd = self.cisis_path + '/id2i ' + id_filename + ' create=' + mst_filename
        os.system(cmd)

    def append(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  append=' + dest + ' now -all'
        os.system(cmd)

    def create(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  create=' + dest + ' now -all'
        os.system(cmd)

    def id2mst(self, id_filename, mst_filename, reset):
        from tempfile import mkstemp

        _, temp = mkstemp()
        self.id2i(id_filename, temp)

        if reset:
            self.create('null count=0', mst_filename)
        self.append(temp, mst_filename)
        os.remove(temp)

    def i2id(self, mst_filename, id_filename):
        cmd = self.cisis_path + '/i2id ' + mst_filename + ' > ' + id_filename 
        os.system(cmd)

    def mst2iso(self, mst_filename, iso_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' iso=' + iso_filename + ' now -all' 
        os.system(cmd)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        os.system(cmd)

    def find_record(self, mst_filename, expression):
        r = mst_filename + expression
        cmd = self.cisis_path + '/mx ' + mst_filename + ' bool="' + expression + '"  lw=999 "pft=mfn/" now > ' + r

        os.system(cmd)
        f = open(r, 'r')
        c = f.readlines()
        f.close()

        a = []
        for l in c:
            a.append(l.replace('\n', ''))

        return a


class FilesLocation(object):

    def __init__(self, acron, issue_label):
        self.acron = acron
        self.issue_label = issue_label

    
