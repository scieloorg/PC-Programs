# coding=utf-8

import os
import shutil

import xml.etree.ElementTree as etree

from StringIO import StringIO


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
        for item in article.trans_title:
            new = {}
            new['_'] = item['trans-title']
            new['s'] = item['trans-subtitle']
            new['l'] = item['language']
            self.records['f']['12'].append(new)

        self.records['f']['601'] = self.trans_languages

        self.records['f']['70'] = []

        for item in article.affiliations:
            self.records['f']['70'].append({'o': item.get('orgname', ''), 'd': item.get('orgdiv', ''), 'c': item.get('country', ''), })
        for item in article.authors:
            self.records['f']['10'].append({'n': item.get('given-names', ''), 's': item.get('surname', ''), 'c': item.get('country', ''), })


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
        if self._dtd_version is None:
            self._dtd_version = self.tree.attrib.get('dtd-version')
        return self._dtd_version

    @property
    def article_type(self):
        if self._article_type is None:
            self._article_type = self.tree.attrib.get('article-type')
        return self._article_type

    @property
    def language(self):
        if self._language is None:
            self._language = self.tree.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
        return self._language

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
        if self._related_objects is None:
            r = []
            related = self.article_meta.findall('related-object')
            for rel in related:
                item = {k: v for k, v in rel.attrib.items()}
                r.append(item)
            self._related_objects = r
        return self._related_objects

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
        if self._related_articles is None:
            r = []
            related = self.article_meta.findall('related-article')
            for rel in related:
                item = {k: v for k, v in rel.attrib.items()}
                r.append(item)
            self._related_articles = r
        return self._related_articles

    @property
    def journal_title(self):
        if self._journal_title is None:
            self._journal_title = self.journal_meta.findtext('journal-title')
        return self._journal_title

    @property
    def abbrev_journal_title(self):
        if self._abbrev_journal_title is None:
            self._abbrev_journal_title = self.journal_meta.findtext('abbrev-journal-title')
        return self._abbrev_journal_title

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
        if self._toc_section is None:
            node = self.article_meta.find('subj-group[@subj-group-type="heading"]')    
            if node is not None:
                self._toc_section = node.findtext('subject')
        return self._toc_section

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
        if self._contrib_names is None:
            k = []
            for contrib in self.article_meta.findall('.//contrib'):
                item = {}
                if contrib.find('name'):
                    item['given-names'] = contrib.find('name/given-names')
                    item['surname'] = contrib.find('name/surname')
                    item['suffix'] = contrib.find('name/suffix')
                    item['prefix'] = contrib.find('name/prefix')
                    item['contrib-id'] = contrib.contrib.findtext('contrib-id[@contrib-id-type="orcid"]')
                    item['contrib-type'] = contrib.attrib.get('contrib-type')
                    item['xref'] = contrib.find('xref[@ref-type="aff"]')
                    if item['xref'] is not None:
                        item['xref'] = item['xref'].attrib.get('rid')
                    k.append(item)
            self._contrib_names = k            
        return self._contrib_names

    @property
    def contrib_collab(self):
        if self._contrib_collab is None:
            k = []
            for contrib in self.article_meta.findall('.//contrib/collab'):
                k.append(contrib.text)
            self._contrib_collab = k
        return self._contrib_collab

    @property
    def title(self):
        if self._title is None:
            k = []
            for node in self.article_meta.findall('.//title-group'):
                item = {}
                item['article-title'] = node.findtext('article-title')
                item['subtitle'] = node.findtext('subtitle')
                if item['article-title'] is not None:
                    item['language'] = item['article-title'].attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

                k.append(item)
            self._title = k
        return self._title

    @property
    def trans_title(self):
        if self._trans_title is None:
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
            self._trans_title = k
        return self._trans_title

    @property
    def trans_languages(self):
        if self._trans_languages is None:
            k = []
            for node in self.subarticles:
                k.append(node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'))
            self._trans_languages = k
        return self._trans_languages


    .//article-meta//article-id[@pub-id-type='doi'] 237
    .//article-meta//article-id[@pub-id-type='other'] 8121
    .//article-meta/volume 31    
    .//article-meta/issue 32    
    .//article-meta/supplement 132    
    .//article-meta//funding-source 58    
    .//article-meta//principal-award-recipient 591    
      . _
    .//article-meta//principal-investigator 591    
      . n
    .//article-meta//award-id 60    
    .//article-meta//funding-statement 102
    .//back//ack 102 XML
    .//article-meta/pub-date 64
      season s
      month m
      year y
      day d
    .//article-meta/pub-date[@pub-type='epub'] epub
      season s
      month m
      year y
      day d  
    .//article-meta/pub-date[@pub-type='collection'] 64
      season s
      month m
      year y
      day d  
    .//article-meta/pub-date[@pub-type='ppub'] 64
      season s
      month m
      year y
      day d  
    .//article-meta/pub-date[@pub-type='epub-ppub'] 64
      season s
      month m
      year y
      day d  
    .//article-meta/pub-date[@date-type='preprint'] epub
      season s
      month m
      year y
      day d  
    .//article-meta/pub-date[@date-type='pub'] 64
      season s
      month m
      year y
      day d  
    .//article-meta/publisher-loc 66    
    .//article-meta 14
      fpage f
      lpage l
      elocation-id f
      elocation-id e
    .//article-meta/fpage 121
    .//article-meta/fpage/@seq 9121
    .//article-meta//aff 70
      label l
      @id i
      . 9
      country p
      email e
      addr-line/named-content[@content-type='city'] c
      addr-line/named-content[@content-type='state'] s
      institution[@content-type='orgdiv3'] 3
      institution[@content-type='orgdiv2'] 2
      institution[@content-type='orgdiv1'] 1
      institution[@content-type='orgname'] _
    .//clinical-trial 770 XML
    .//article-meta//aff 170 XML
    .//ref-count/@count 72    
    .//table-count/@count 900
    .//fig-count/@count 901
    .//article-meta/abstract 83
      . a
      @xml:lang l 
    .//article-meta/trans-abstract[1] 83
      . a
      @xml:lang l
    .//article-meta/trans-abstract[2] 83
      . a
      @xml:lang l
    .//sub-article[@article-type='translation']//front-stub//abstract 83
      . a
      @xml:lang l 
    .//article-meta//date[@date-type='received'] 111    
      year y
      month m
      day d
      season s   
    .//article-meta//date[@date-type='accepted'] 113    
      year y
      month m
      day d
      season s      
  .//body body
    .//graphic/@xlink:href file
  .//ref c
    .//source/@xml:lang 40
    .//element-citation/@publication-type 71
    .//mixed-citation/@publication-type 71
    .//citation/@citation-type 71
    .//article-title 12
      . _
      @xml:lang l en
    .//trans-title 12
      . _
      @xml:lang l
    .//chapter-title 12
      . _
      @xml:lang l en
    .//source 18    
    . 9704 XML
    .//mixed-citation 704 XML
    .//citation[@citation-type='journal']//source 30 
    .//element-citation[@publication-type='journal']//source 30    
    .//mixed-citation[@publication-type='journal']//source 30    
    .//person-group/@person-group-type roles
    .//person-group[1]/name 10
      given-names n
      surname s
      suffix z
    name 10
      given-names n
      surname s
      suffix z
    .//person-group[2]/name 16
      given-names n
      surname s
      suffix z
    .//collab[1] 11
    .//collab[2] 17
    .//person-group[1]/collab 11
    .//person-group[2]/collab 17
    .//volume 31    
    .//issue 32  
    .//supplement 132
      . s
    .//edition 63    
    .//year 964    
    .//month 964m
    .//day 964d
    .//season 964s
    .//publisher-loc 66
    .//publisher-name 62
    .//element-citation 514
      fpage f
      lpage l
      page-range r
    .//mixed-citation 514
      fpage f
      lpage l
      page-range r
    .//size 20
      . _
      @units u
    .//label 118    
    .//et-al 810    
    .//ext-link 37    
    .//date-in-citation[@content-type='access-date'] 109
    .//comment 61    
    .//comment[@content-type='award-id'] 60   
    .//element-citation[@publication-type='report']//comment 60    
    .//notes 61    
    .//pub-id[@pub-id-type='doi'] 237    
    .//pub-id[@pub-id-type='pmid'] 238    
    .//pub-id[@pub-id-type='pmcid'] 239    
    .//element-citation[@publication-type='report']//pub-id[@pub-id-type='other'] 592    
    .//conf-name 53
    .//conf-loc 56
    .//conf-date 54


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

    
