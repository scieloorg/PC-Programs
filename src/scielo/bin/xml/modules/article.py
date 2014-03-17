# coding=utf-8

import xml.etree.ElementTree as etree

from modules.utils import node_text


class ArticleXML(object):

    def __init__(self, tree):
        self.tree = tree
        self.journal_meta = None
        self.article_meta = None
        self.body = None
        self.back = None
        self.subarticles = None
        self.responses = None
        if tree is not None:
            self.journal_meta = self.tree.find('./front/journal-meta')
            self.article_meta = self.tree.find('./front/article-meta')
            self.body = self.tree.find('./body')
            self.back = self.tree.find('./back')
            self.subarticles = self.tree.findall('./sub-article')
            self.responses = self.tree.findall('./response')

    @property
    def dtd_version(self):
        return self.tree.find('.').attrib.get('dtd-version')

    @property
    def article_type(self):
        return self.tree.find('.').attrib.get('article-type')

    @property
    def language(self):
        return self.tree.find('.').attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

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
        return self.journal_meta.findtext('.//publisher-name')

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
        node = self.article_meta.find('.//subj-group[@subj-group-type="heading"]')
        if node is not None:
            return node.findtext('subject')
        return None

    @property
    def keywords(self):
        k = []
        for node in self.article_meta.findall('kwd-group'):
            language = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            for kw in node.findall('kwd'):
                k.append({'l': language, 'k': node_text(kw)})
        return k

    @property
    def contrib_names(self):
        k = []
        for contrib in self.article_meta.findall('.//contrib'):
            item = {}
            if contrib.findall('name'):
                item['given-names'] = contrib.findtext('name/given-names')
                item['surname'] = contrib.findtext('name/surname')
                item['suffix'] = contrib.findtext('name/suffix')
                item['prefix'] = contrib.findtext('name/prefix')
                item['contrib-id'] = contrib.findtext('contrib-id[@contrib-id-type="orcid"]')
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
            item['article-title'] = node_text(node.find('article-title'))
            item['subtitle'] = node_text(node.find('subtitle'))
            item['language'] = self.tree.find('.').attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

            if item['article-title'] is not None:
                item['language'] = node.find('article-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

            k.append(item)
        return k

    @property
    def trans_titles(self):
        k = []
        for node in self.article_meta.findall('.//trans-title-group'):
            item = {}
            item['trans-title'] = node_text(node.find('trans-title'))
            item['trans-subtitle'] = node_text(node.find('trans-subtitle'))
            item['language'] = self.tree.find('.').attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            if item['trans-title'] is not None:
                item['language'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')

            k.append(item)

        for subart in self.subarticles:
            if subart.attrib.get('article-type') == 'translation':
                for node in subart.findall('.//title-group'):
                    item = {}
                    item['trans-title'] = node_text(node.find('article-title'))
                    item['trans-subtitle'] = node_text(node.find('subtitle'))
                    item['language'] = subart.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                    if item['trans-title'] is not None:
                        item['language'] = node.find('article-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
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
        _order = self.article_id_other
        if _order is None:
            _order = self.fpage
        if _order is None:
            _order = '00000'
        else:
            _order = '00000' + _order
        return _order[-5:]

    @property
    def article_id_other(self):
        return self.article_meta.findtext('article-id[@pub-id-type="other"]')

    @property
    def volume(self):
        v = self.article_meta.findtext('volume')
        return str(int(v)) if v is not None else None

    @property
    def issue(self):
        return self.article_meta.findtext('issue')

    @property
    def supplement(self):
        return self.article_meta.findtext('supplement')

    @property
    def is_issue_press_release(self):
        if self.tree.find('.').attrib.get('article-type') == 'press-release':
            return not self.is_article_press_release
        return False

    @property
    def funding_source(self):
        return [node_text(item) for item in self.article_meta.findall('.//funding-source')]

    @property
    def principal_award_recipient(self):
        return [node_text(item) for item in self.article_meta.findall('.//principal-award-recipient')]

    @property
    def principal_investigator(self):
        return [node_text(item) for item in self.article_meta.findall('.//principal-investigator')]

    @property
    def award_id(self):
        return [node_text(item) for item in self.article_meta.findall('.//award-id')]

    @property
    def funding_statement(self):
        return [node_text(item) for item in self.article_meta.findall('.//funding-statement')]

    @property
    def ack_xml(self):
        #107
        if self.back is not None:
            return node_text(self.back.find('.//ack'), False)

    @property
    def fpage(self):
        return self.article_meta.findtext('fpage')

    @property
    def fpage_seq(self):
        return self.article_meta.find('fpage').attrib.get('seq') if self.article_meta.find('fpage') is not None else None

    @property
    def lpage(self):
        return self.article_meta.findtext('lpage')

    @property
    def elocation_id(self):
        return self.article_meta.findtext('elocation-id')

    @property
    def affiliations(self):
        affs = []
        for aff in self.article_meta.findall('aff'):
            a = {}
            a['xml'] = node_text(aff, False)
            a['id'] = aff.get('id')

            for tag in ['city', 'state', 'orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3']:
                a[tag] = None

            for tag in ['label', 'country', 'email']:
                a[tag] = aff.findtext(tag)
            for inst in aff.findall('institution'):
                # institution[@content-type='orgdiv3']
                tag = inst.get('content-type')
                if tag is not None:
                    a[tag] = node_text(inst)
            for named_content in aff.findall('addr-line/named-content'):
                tag = named_content.get('content-type')
                if tag is not None:
                    a[tag] = node_text(named_content)
            affs.append(a)
        return affs

    @property
    def clinical_trial(self):
        #FIXME nao existe clinical-trial 
        return node_text(self.article_meta.find('clinical-trial'))

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
        for a in self.tree.findall('.//abstract'):
            _abstract = {}
            _abstract['language'] = a.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            _abstract['text'] = node_text(a)
            r.append(_abstract)
        for a in self.tree.findall('.//trans-abstract'):
            _abstract = {}
            _abstract['language'] = a.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            _abstract['text'] = node_text(a)
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
        if self.back is not None:
            for ref in self.back.findall('.//ref'):
                refs.append(ReferenceXML(ref))
        return refs


class Article(ArticleXML):

    def __init__(self, tree):
        ArticleXML.__init__(self, tree)
        if self.tree is not None:
            self._issue_parts()

    def _issue_parts(self):
        self.number = None
        self.number_suppl = None
        self.volume_suppl = None
        suppl = None
        if self.issue is not None:
            parts = self.issue.split(' ')
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
            if self.number is not None:
                if self.number.isdigit():
                    self.number = str(int(self.number))
            if suppl is not None:
                if self.number is None:
                    self.number_suppl = suppl
                    if self.number_suppl.isdigit():
                        self.number_suppl = str(int(self.number_suppl))
                else:
                    self.volume_suppl = suppl
                    if self.volume_suppl.isdigit():
                        self.volume_suppl = str(int(self.volume_suppl))

    @property
    def press_release_id(self):
        related = self.article_meta.find('related-object[@document-type="pr"]')
        if related is not None:
            return related.attrib.get('document-id')

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
    def is_ahead(self):
        if self.volume.replace('0', '') == '' and self.number.replace('0', '') == '':
            return True
        return False

    @property
    def ahpdate(self):
        return self.article_pub_date if self.is_ahead else None

    @property
    def is_article_press_release(self):
        return (self.article_meta.find('.//related-document[@link-type="article-has-press-release"]') is not None)

    @property
    def illustrative_materials(self):
        _illustrative_materials = []
        if len(self.tree.findall('.//table-wrap')) > 0:
            _illustrative_materials.append('TAB')
        figs = len(self.tree.findall('.//fig'))
        if figs > 0:

            maps = len(self.tree.findall('.//fig[@fig-type="map"]'))
            gras = len(self.tree.findall('.//fig[@fig-type="graphic"]'))
            if maps > 0:
                _illustrative_materials.append('MAP')
            if gras > 0:
                _illustrative_materials.append('GRA')
            if figs - gras - maps > 0:
                _illustrative_materials.append('ILUS')

        if len(_illustrative_materials) > 0:
            return _illustrative_materials
        else:
            return 'ND'

    @property
    def is_text(self):
        return self.tree.findall('.//kwd') is None


class ReferenceXML(object):

    def __init__(self, root):
        self.root = root

    @property
    def source(self):
        return node_text(self.root.find('.//source'))

    @property
    def language(self):
        lang = self.root.find('.//source').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//source') is not None else None
        if lang is None:
            lang = self.root.find('.//article-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//article-title') is not None else None
        if lang is None:
            lang = self.root.find('.//chapter-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//chapter-title') is not None else None
        return lang

    @property
    def article_title(self):
        return node_text(self.root.find('.//article-title'))

    @property
    def chapter_title(self):
        return node_text(self.root.find('.//chapter-title'))

    @property
    def trans_title(self):
        return node_text(self.root.find('.//trans-title'))

    @property
    def trans_title_language(self):
        return self.root.find('.//trans-title').attrib.get('{http://www.w3.org/XML/1998/namespace}lang') if self.root.find('.//trans-title') is not None else None

    @property
    def publication_type(self):
        return self.root.find('.//element-citation').attrib.get('publication-type') if self.root.find('.//element-citation') is not None else None

    @property
    def xml(self):
        return node_text(self.root, False)

    @property
    def mixed_citation(self):
        return node_text(self.root.find('.//mixed-citation'))

    @property
    def person_groups(self):
        r = {}
        k = 0
        for person_group in self.root.findall('.//person-group'):
            k += 1
            person_group_id = person_group.attrib.get('person-group-type', 'author')
            r[person_group_id] = []
            for person in person_group.findall('.//name'):
                p = {}
                for tag in ['given-names', 'surname', 'suffix']:
                    p[tag] = person.findtext(tag)

                r[person_group_id].append(p)
            for collab in person_group.findall('.//collab'):
                r[person_group_id].append({'collab': node_text(collab)})
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
        return node_text(self.root.find('.//conf-name'))

    @property
    def conference_location(self):
        return self.root.findtext('.//conf-loc')

    @property
    def conference_date(self):
        return self.root.findtext('.//conf-date')
