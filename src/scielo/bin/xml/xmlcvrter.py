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

        self.records['f']['601'] = article.trans_languages
        self.records['f']['237'] = article.doi

        self.records['f']['121'] = article.order if article.order is not None else article.first_page

        self.records['f']['31'] = article.volume
        self.records['f']['32'] = article.number
        self.records['f']['131'] = article.volume_suppl
        self.records['f']['132'] = article.number_suppl

        self.records['f']['58'] = article.funding_source
        self.records['f']['591'] = [{'_': item for item in article.principal_award_recipient}]
        self.records['f']['591'] = [{'n': item for item in article.principal_investigator}]
        self.records['f']['60'] = article.award_id
        self.records['f']['102'] = article.funding_statement

        self.records['f']['64'] = {}
        self.records['f']['64']['s'] = article.issue_pub_date['season']
        self.records['f']['64']['d'] = article.issue_pub_date['day']
        self.records['f']['64']['m'] = article.issue_pub_date['month']
        self.records['f']['64']['y'] = article.issue_pub_date['year']

        self.records['f']['64'] = {}
        self.records['f']['64']['s'] = article.issue_pub_date['season']
        self.records['f']['64']['d'] = article.issue_pub_date['day']
        self.records['f']['64']['m'] = article.issue_pub_date['month']
        self.records['f']['64']['y'] = article.issue_pub_date['year']
        # FIXME
        
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
    def trans_title(self):
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
        return [item.text for item in self.article_meta.find('.//funding-source')]

    @property
    def principal_award_recipient(self):
        return [item.text for item in self.article_meta.find('.//principal-award-recipient')]

    @property
    def principal_investigator(self):
        return [item.text for item in self.article_meta.find('.//principal-investigator')]

    @property
    def award_id(self):
        return [item.text for item in self.article_meta.find('.//award-id')]

    @property
    def funding_statement(self):
        return [item.text for item in self.article_meta.find('.//funding-statement')]

    @property
    def ack_xml(self):
        #107
        return etree.tostring(self.back.find('.//ack'))

    @property
    def issue_pub_date(self):
        _issue_pub_date = None
        date = self.article_meta.find('[@date-type="pub"]')
        if date is None:
            date = self.article_meta.find('[@pub-type="epub-ppub"]')
        if date is None:
            date = self.article_meta.find('[@pub-type="ppub"]')
        if date is None:
            date = self.article_meta.find('[@pub-type="collection"]')
        
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
        date = self.article_meta.find('[@date-type="preprint"]')
        if date is None:
            date = self.article_meta.find('[@pub-type="epub"]')
        
        if date is not None:
            _article_pub_date = {}
            _article_pub_date['season'] = date.findtext('season')
            _article_pub_date['month'] = date.findtext('month')
            _article_pub_date['year'] = date.findtext('year')
            _article_pub_date['day'] = date.findtext('day')
        return _article_pub_date
        

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

    
