# coding=utf-8
import os
from datetime import datetime

import article_utils
import xml_utils
import attributes


IMG_EXTENSIONS = ['.tif', '.tiff', '.eps', '.gif', '.png', '.jpg', ]


def nodetext(node, sep='|'):
    if node is None:
        r = None
    elif isinstance(node, list):
        r = sep.join([item.text for item in node if item.text is not None])
    else:
        r = node.text
    if r == '':
        r = None
    return r


def format_author(author):
    r = author.surname
    if author.suffix:
        r += ' (' + author.suffix + ')'
    r += ', '
    if author.prefix:
        r += '(' + author.prefix + ') '
    r += author.fname
    if author.role:
        r += '(role: ' + author.role + ')'
    r += '(xref: ' + ','.join(author.xref) + ')'
    return r


class Table(object):

    def __init__(self, name, id, label, caption, graphic, table):
        self.table = table
        self.name = name
        self.id = id
        self.label = label if label is not None else ''
        self.caption = caption if caption is not None else ''
        self.graphic = graphic


class HRef(object):

    def __init__(self, src, element, parent, xml, xml_name):
        self.src = src
        self.element = element
        self.xml = xml

        ext = '.jpg' if not '.' in src else src[src.rfind('.'):]

        self.id = element.attrib.get('id', None)
        if self.id is None and parent is not None:
            self.id = parent.attrib.get('id', None)
        self.parent = parent
        self.is_internal_file = xml_name in src
        self.is_image = ext in IMG_EXTENSIONS

    def file_location(self, path):
        location = None
        if self.src is not None and self.src != '':
            if self.is_internal_file:
                location = path + '/' + self.src

                if self.is_image:
                    if location.endswith('.tiff'):
                        location = location.replace('.tiff', '.jpg')
                    elif location.endswith('.tif'):
                        location = location.replace('.tif', '.jpg')
                    else:
                        if location[-5:-4] != '.' and location[-4:-3] != '.':
                            location += '.jpg'
        return location


class PersonAuthor(object):

    def __init__(self):
        self.fname = ''
        self.surname = ''
        self.suffix = ''
        self.prefix = ''
        self.contrib_id = ''
        self.role = ''
        self.xref = []


class CorpAuthor(object):

    def __init__(self):
        self.role = ''
        self.collab = ''


class Affiliation(object):

    def __init__(self):
        self.xml = ''
        self.id = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.i_country = ''
        self.orgname = ''
        self.norgname = ''
        self.orgdiv1 = ''
        self.orgdiv2 = ''
        self.orgdiv3 = ''
        self.label = ''
        self.email = ''
        self.original = ''


class Title(object):

    def __init__(self):
        self.title = ''
        self.subtitle = ''
        self.language = ''


class Text(object):

    def __init__(self):
        self.text = ''
        self.language = ''


class ArticleXML(object):

    def __init__(self, tree, xml_name):
        self.xml_name = xml_name
        self.prefix = xml_name.replace('.xml', '')
        self._ahead_pid = None
        self.tree = tree
        self.journal_meta = None
        self.article_meta = None
        self.body = None
        self.back = None
        self.translations = []
        self.sub_articles = []
        self.responses = []
        self._title_abstract_kwd_languages = None
        self._language = None
        self._trans_languages = None
        self._titles_by_lang = None
        self._abstracts_by_lang = None
        self._keywords_by_lang = None
        self._collection_date = None
        self._epub_date = None
        self._epub_ppub_date = None
        self._received_date = None
        self._accepted_date = None

        if tree is not None:
            self.journal_meta = self.tree.find('./front/journal-meta')
            self.article_meta = self.tree.find('./front/article-meta')
            self.body = self.tree.find('./body')
            self.back = self.tree.find('./back')
            self.translations = self.tree.findall('./sub-article[@article-type="translation"]')
            for s in self.tree.findall('./sub-article'):
                if s.attrib.get('article-type') != 'translation':
                    self.sub_articles.append(s)
            self.responses = self.tree.findall('./response')

    def sections(self, node, scope):
        r = []
        if node is not None:
            for sec in node.findall('./sec'):
                r.append((scope + '/sec', sec.attrib.get('sec-type', ''), sec.findtext('title')))
                for subsec in sec.findall('sec'):
                    r.append((scope + '/sec/sec', subsec.attrib.get('sec-type', 'None'), subsec.findtext('title')))
                    for subsubsec in subsec.findall('sec'):
                        r.append((scope + '/sec/sec/sec', subsubsec.attrib.get('sec-type', 'None'), subsubsec.findtext('title')))
        return r

    @property
    def article_sections(self):
        r = self.sections(self.body, 'article')
        if self.translations is not None:
            for item in self.translations:
                for sec in self.sections(item.find('.//body'), 'sub-article/[@id="' + item.attrib.get('id', 'None') + '"]'):
                    r.append(sec)
        return r

    @property
    def article_type_and_contrib_items(self):
        r = []
        for subart in self.translations:
            r.append((subart.attrib.get('article-type'), subart.findall('.//contrib/collab') + subart.findall('.//contrib/name')))
        for subart in self.responses:
            r.append((subart.attrib.get('response-type'), subart.findall('.//contrib/collab') + subart.findall('.//contrib/name')))
        return r

    def fn_list(self, node, scope):
        r = []
        if node is not None:
            for fn in node.findall('.//fn'):
                r.append((scope, xml_utils.node_xml(fn)))
        return r

    @property
    def article_fn_list(self):
        r = self.fn_list(self.back, 'article')
        if self.translations is not None:
            for item in self.translations:
                scope = 'sub-article/[@id="' + item.attrib.get('id', 'None') + '"]'
                for fn in self.fn_list(item.find('.//back'), scope):
                    r.append(fn)
        return r

    @property
    def xref_nodes(self):
        _xref_list = []
        if self.tree is not None:
            for node in self.tree.findall('.//xref'):
                n = {}
                n['ref-type'] = node.attrib.get('ref-type')
                n['rid'] = node.attrib.get('rid')
                n['xml'] = xml_utils.node_xml(node)
                _xref_list.append(n)
        return _xref_list

    @property
    def dtd_version(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('dtd-version')

    @property
    def sps(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('specific-use')

    @property
    def article_type(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('article-type')

    @property
    def language(self):
        if self._language is None:
            if self.tree is not None:
                self._language = xml_utils.element_lang(self.tree.find('.'))
        return self._language

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
        r = []
        if self.article_meta is not None:
            related = self.article_meta.findall('related-article')
            for rel in related:
                item = {}
                item['href'] = rel.attrib.get('{http://www.w3.org/1999/xlink}href')
                item['related-article-type'] = rel.attrib.get('related-article-type')
                item['ext-link-type'] = rel.attrib.get('ext-link-type')
                item['id'] = rel.attrib.get('id')
                if not item['related-article-type'] in ['corrected-article', 'press-release']:
                    item['id'] = ''.join([c for c in item['id'] if c.isdigit()])
                r.append(item)
        return r

    @property
    def journal_title(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('.//journal-title')

    @property
    def abbrev_journal_title(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('abbrev-journal-title')

    @property
    def publisher_name(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('.//publisher-name')

    @property
    def journal_id(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('journal-id')

    @property
    def journal_id_nlm_ta(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('journal-id[@journal-id-type="nlm-ta"]')

    @property
    def journal_issns(self):
        if self.journal_meta is not None:
            return {item.attrib.get('pub-type', 'epub'):item.text for item in self.journal_meta.findall('issn')}

    @property
    def print_issn(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('issn[@pub-type="ppub"]')

    @property
    def e_issn(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('issn[@pub-type="epub"]')

    @property
    def toc_section(self):
        r = None
        if self.article_meta is not None:
            node = self.article_meta.find('.//subj-group[@subj-group-type="heading"]')
            if node is not None:
                r = node.findtext('subject')
        return r

    @property
    def normalized_toc_section(self):
        return attributes.normalized_toc_section(self.toc_section)

    @property
    def keywords_by_lang(self):
        if self._keywords_by_lang is None:
            k = {}
            if not self.article_meta is None:
                for node in self.article_meta.findall('kwd-group'):
                    language = xml_utils.element_lang(node)
                    if language is None:
                        language = self.language
                    kw_items = []
                    for kw in node.findall('kwd'):
                        t = Text()
                        t.language = language
                        t.text = xml_utils.node_text(kw)
                        kw_items.append(t)
                    k[language] = kw_items
            for subart in self.translations:
                for node in subart.findall('.//kwd-group'):
                    language = xml_utils.element_lang(node)
                    kw_items = []
                    for kw in node.findall('kwd'):
                        t = Text()
                        t.language = language
                        t.text = xml_utils.node_text(kw)
                        kw_items.append(t)
                    k[language] = kw_items
            self._keywords_by_lang = k
        return self._keywords_by_lang

    @property
    def keywords(self):
        k = []
        if not self.article_meta is None:
            for node in self.article_meta.findall('kwd-group'):
                language = xml_utils.element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': xml_utils.node_text(kw)})
        for subart in self.translations:
            for node in subart.findall('.//kwd-group'):
                language = xml_utils.element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': xml_utils.node_text(kw)})
        return k

    @property
    def contrib_names(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib'):
                if contrib.findall('name'):
                    p = PersonAuthor()
                    p.fname = contrib.findtext('name/given-names')
                    p.surname = contrib.findtext('name/surname')
                    p.suffix = contrib.findtext('name/suffix')
                    p.prefix = contrib.findtext('name/prefix')
                    p.contrib_id = contrib.findtext('contrib-id[@contrib-id-type="orcid"]')
                    p.role = contrib.attrib.get('contrib-type')
                    for xref_item in contrib.findall('xref[@ref-type="aff"]'):
                        p.xref.append(xref_item.attrib.get('rid'))
                    k.append(p)
        return k

    @property
    def authors_aff_xref_stats(self):
        with_aff = []
        no_aff = []
        mismatched_aff_id = []
        aff_ids = [aff.id for aff in self.affiliations if aff.id is not None]
        for contrib in self.contrib_names:
            if len(contrib.xref) == 0:
                no_aff.append(contrib)
            else:
                q = 0
                for xref in contrib.xref:
                    if xref in aff_ids:
                        q += 1
                if q != len(contrib.xref):
                    mismatched_aff_id.append(contrib)
                else:
                    with_aff.append(contrib)
        return (with_aff, no_aff, mismatched_aff_id)

    @property
    def authors_without_aff(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib'):
                if contrib.findall('name'):
                    p = PersonAuthor()
                    p.fname = contrib.findtext('name/given-names')
                    p.surname = contrib.findtext('name/surname')
                    p.suffix = contrib.findtext('name/suffix')
                    p.prefix = contrib.findtext('name/prefix')
                    p.contrib_id = contrib.findtext('contrib-id[@contrib-id-type="orcid"]')
                    p.role = contrib.attrib.get('contrib-type')
                    for xref_item in contrib.findall('xref[@ref-type="aff"]'):
                        p.xref.append(xref_item.attrib.get('rid'))
                    k.append(p)
        return k

    @property
    def first_author_surname(self):
        surname = None
        authors = self.contrib_names
        if len(authors) > 0:
            surname = authors[0].surname
        return surname

    @property
    def contrib_collabs(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib/collab'):
                collab = CorpAuthor()
                collab.collab = contrib.text
                k.append(collab)
        return k

    @property
    def title(self):
        return self.titles[0].title if len(self.titles) > 0 else None

    @property
    def titles(self):
        k = []
        if self.article_meta is not None:
            for node in self.article_meta.findall('.//title-group'):
                t = Title()
                t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
                t.language = self.language
                k.append(t)
            for node in self.article_meta.findall('.//trans-title-group'):
                t = Title()
                t.title = article_utils.remove_xref(xml_utils.node_text(node.find('trans-title')))
                t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('trans-subtitle')))
                t.language = xml_utils.element_lang(node)
                k.append(t)
        if self.translations is not None:
            for subart in self.translations:
                for node in subart.findall('.//title-group'):
                    t = Title()
                    t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                    t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
                    t.language = xml_utils.element_lang(subart)
                    k.append(t)
        return k

    @property
    def titles_by_lang(self):
        if self._titles_by_lang is None:
            k = {}
            if self.article_meta is not None:
                language = self.language
                for node in self.article_meta.findall('.//title-group'):
                    t = Title()
                    t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                    t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
                    t.language = language
                    k[language] = t
                for node in self.article_meta.findall('.//trans-title-group'):
                    language = xml_utils.element_lang(node)
                    t = Title()
                    t.title = article_utils.remove_xref(xml_utils.node_text(node.find('trans-title')))
                    t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('trans-subtitle')))
                    t.language = language
                    k[language] = t
            if self.translations is not None:
                for subart in self.translations:
                    for node in subart.findall('.//title-group'):
                        language = xml_utils.element_lang(subart)
                        t = Title()
                        t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                        t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
                        t.language = language
                        k[language] = t
            self._titles_by_lang = k
        return self._titles_by_lang

    @property
    def title_abstract_kwd_languages(self):
        if self._title_abstract_kwd_languages is None:
            self._title_abstract_kwd_languages = list(set(self.keywords_by_lang.keys() + self.abstracts_by_lang.keys() + self.titles_by_lang.keys()))
            self._title_abstract_kwd_languages = [item for item in self._title_abstract_kwd_languages if item is not None]
        return self._title_abstract_kwd_languages

    @property
    def trans_languages(self):
        if self._trans_languages is None:
            k = []
            if self.translations is not None:
                for node in self.translations:
                    k.append(xml_utils.element_lang(node))
            self._trans_languages = k
        return self._trans_languages

    @property
    def doi(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('article-id[@pub-id-type="doi"]')

    @property
    def article_previous_id(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('article-id[@specific-use="previous-pid"]')

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
        if self.article_meta is not None:
            return self.article_meta.findtext('article-id[@pub-id-type="other"]')

    @property
    def volume(self):
        v = None
        if self.article_meta is not None:
            v = self.article_meta.findtext('volume')
            v = article_utils.normalize_number(v)
            if v == '0':
                v = None
        return v

    @property
    def issue(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('issue')

    @property
    def supplement(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('supplement')

    @property
    def funding_source(self):
        return [xml_utils.node_text(item) for item in self.article_meta.findall('.//funding-source')]

    @property
    def principal_award_recipient(self):
        return [xml_utils.node_text(item) for item in self.article_meta.findall('.//principal-award-recipient')]

    @property
    def principal_investigator(self):
        return [xml_utils.node_text(item) for item in self.article_meta.findall('.//principal-investigator')]

    @property
    def award_id(self):
        return [xml_utils.node_text(item) for item in self.article_meta.findall('.//award-id')]

    @property
    def funding_statement(self):
        return [xml_utils.node_text(item) for item in self.article_meta.findall('.//funding-statement')]

    @property
    def ack_xml(self):
        #107
        if self.back is not None:
            return xml_utils.node_xml(self.back.find('.//ack'))

    @property
    def financial_disclosure(self):
        if self.tree is not None:
            return xml_utils.node_text(self.tree.find('.//fn[@fn-type="financial-disclosure"]'))

    @property
    def fn_financial_disclosure(self):
        if self.tree is not None:
            return xml_utils.node_xml(self.tree.find('.//fn[@fn-type="financial-disclosure"]'))

    @property
    def fpage(self):
        if self.article_meta is not None:
            return article_utils.normalize_number(self.article_meta.findtext('fpage'))

    @property
    def fpage_seq(self):
        if self.article_meta is not None:
            return self.article_meta.find('fpage').attrib.get('seq') if self.article_meta.find('fpage') is not None else None

    @property
    def lpage(self):
        if self.article_meta is not None:
            return article_utils.normalize_number(self.article_meta.findtext('lpage'))

    @property
    def elocation_id(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('elocation-id')

    @property
    def affiliations(self):
        affs = []
        if self.article_meta is not None:
            for aff in self.article_meta.findall('.//aff'):
                a = Affiliation()

                a.xml = xml_utils.node_xml(aff)
                a.id = aff.get('id')
                a.label = aff.findtext('label')
                country = aff.findall('country')
                a.country = nodetext(country)
                if not country is None:
                    if isinstance(country, list):
                        a.i_country = '|'.join([item.attrib.get('country') for item in country if item.attrib.get('country') is not None])
                        if a.i_country == '':
                            a.i_country = None

                a.email = nodetext(aff.findall('email'), ', ')
                a.original = nodetext(aff.findall('institution[@content-type="original"]'))
                a.norgname = nodetext(aff.findall('institution[@content-type="normalized"]'))
                a.orgname = nodetext(aff.findall('institution[@content-type="orgname"]'))
                a.orgdiv1 = nodetext(aff.findall('institution[@content-type="orgdiv1"]'))
                a.orgdiv2 = nodetext(aff.findall('institution[@content-type="orgdiv2"]'))
                a.orgdiv3 = nodetext(aff.findall('institution[@content-type="orgdiv3"]'))
                a.city = nodetext(aff.findall('addr-line/named-content[@content-type="city"]'))
                a.state = nodetext(aff.findall('addr-line/named-content[@content-type="state"]'))

                affs.append(a)

        return affs

    @property
    def uri_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="clinical-trial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.tree is not None:
            node = self.tree.find('.//uri[@content-type="clinical-trial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def uri_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="clinical-trial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.tree is not None:
            node = self.tree.find('.//uri[@content-type="clinical-trial"]')
            if node is not None:
                return xml_utils.node_text(node)

    @property
    def ext_link_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="clinical-trial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.tree is not None:
            node = self.tree.find('.//ext-link[@ext-link-type="clinical-trial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def ext_link_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="clinical-trial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.tree is not None:
            node = self.tree.find('.//ext-link[@ext-link-type="clinical-trial"]')
            if node is not None:
                return xml_utils.node_text(node)

    @property
    def page_count(self):
        if self.article_meta is not None:
            if self.article_meta.find('.//page-count') is not None:
                return self.article_meta.find('.//page-count').attrib.get('count')

    @property
    def ref_count(self):
        if self.article_meta is not None:
            if self.article_meta.find('.//ref-count') is not None:
                return self.article_meta.find('.//ref-count').attrib.get('count')

    @property
    def table_count(self):
        if self.article_meta is not None:
            if self.article_meta.find('.//table-count') is not None:
                return self.article_meta.find('.//table-count').attrib.get('count')

    @property
    def fig_count(self):
        if self.article_meta is not None:
            if self.article_meta.find('.//fig-count') is not None:
                return self.article_meta.find('.//fig-count').attrib.get('count')

    @property
    def equation_count(self):
        if self.article_meta is not None:
            if self.article_meta.find('.//equation-count') is not None:
                return self.article_meta.find('.//equation-count').attrib.get('count')

    @property
    def total_of_pages(self):
        if self.fpage is not None and self.lpage is not None:
            if self.fpage.isdigit() and self.lpage.isdigit():
                return int(self.lpage) - int(self.fpage) + 1

    def total(self, node, xpath):
        if node is not None:
            return len(node.findall(xpath))

    @property
    def total_of_references(self):
        return self.total(self.tree, './/ref')

    @property
    def total_of_tables(self):
        return self.total(self.tree, './/table-wrap')

    @property
    def total_of_equations(self):
        return self.total(self.tree, './/disp-formula')

    @property
    def total_of_figures(self):
        return self.total(self.tree, './/fig')

    @property
    def formulas(self):
        r = []
        if self.tree is not None:
            if self.tree.findall('.//disp-formula') is not None:
                for item in self.tree.findall('.//disp-formula'):
                    r.append(xml_utils.node_xml(item))
            if self.tree.findall('.//inline-formula') is not None:
                for item in self.tree.findall('.//inline-formula'):
                    r.append(xml_utils.node_xml(item))
        return r

    @property
    def abstracts_by_lang(self):
        if self._abstracts_by_lang is None:
            r = {}
            if self.article_meta is not None:
                language = self.language
                for a in self.article_meta.findall('.//abstract'):
                    _abstract = Text()
                    _abstract.language = language
                    _abstract.text = xml_utils.node_text(a)
                    r[language] = _abstract
                for a in self.article_meta.findall('.//trans-abstract'):
                    language = xml_utils.element_lang(a)
                    _abstract = Text()
                    _abstract.language = language
                    _abstract.text = xml_utils.node_text(a)
                    r[language] = _abstract
            for subart in self.translations:
                language = xml_utils.element_lang(subart)
                for a in subart.findall('.//abstract'):
                    _abstract = Text()
                    _abstract.language = language
                    _abstract.text = xml_utils.node_text(a)
                    r[language] = _abstract
            self._abstracts_by_lang = r
        return self._abstracts_by_lang

    @property
    def abstracts(self):
        r = []
        if self.article_meta is not None:
            for a in self.article_meta.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = self.language
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
            for a in self.article_meta.findall('.//trans-abstract'):
                _abstract = Text()
                _abstract.language = xml_utils.element_lang(a)
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
        for subart in self.translations:
            subart_lang = xml_utils.element_lang(subart)
            for a in subart.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = subart_lang
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
            for a in subart.findall('.//trans-abstract'):
                _abstract = Text()
                _abstract.language = xml_utils.element_lang(a)
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
        return r

    @property
    def references(self):
        refs = []
        if self.back is not None:
            for ref in self.back.findall('.//ref'):
                refs.append(ReferenceXML(ref))
        return refs

    @property
    def refstats(self):
        _refstats = {}
        for ref in self.references:
            if not ref.publication_type in _refstats.keys():
                _refstats[ref.publication_type] = 0
            _refstats[ref.publication_type] += 1
        return _refstats

    @property
    def display_only_stats(self):
        q = 0
        for ref in self.references:
            if not ref.ref_status is None:
                if ref.ref_status == 'display-only':
                    q += 1
        return q

    @property
    def press_release_id(self):
        _id = None
        for related in self.related_articles:
            if related.get('id') is not None:
                _id = related.get('id')
        return _id

    @property
    def received(self):
        if self._received_date is None:
            if self.article_meta is not None:
                self._received_date = xml_utils.date_element(self.article_meta.find('date[@pub-type="received"]'))
        return self._received_date

    @property
    def accepted(self):
        if self._accepted_date is None:
            if self.article_meta is not None:
                self._accepted_date = xml_utils.date_element(self.article_meta.find('date[@pub-type="accepted"]'))
        return self._accepted_date

    @property
    def collection_date(self):
        if self._collection_date is None:
            if self.article_meta is not None:
                self._collection_date = xml_utils.date_element(self.article_meta.find('pub-date[@pub-type="collection"]'))
        return self._collection_date

    @property
    def epub_ppub_date(self):
        if self._epub_ppub_date is None:
            if self.article_meta is not None:
                self._epub_ppub_date = xml_utils.date_element(self.article_meta.find('pub-date[@pub-type="epub-ppub"]'))
        return self._epub_ppub_date

    @property
    def epub_date(self):
        if self._epub_date is None:
            if self.article_meta is not None:
                date_node = self.article_meta.find('pub-date[@pub-type="epub"]')
                if date_node is None:
                    date_node = self.article_meta.find('pub-date[@date-type="preprint"]')
                self._epub_date = xml_utils.date_element(date_node)
        return self._epub_date

    @property
    def is_article_press_release(self):
        r = False
        types = [related.get('related-article-type') for related in self.related_articles if not related.get('related-article-type') in ['corrected-article', 'press-release']]
        return (len(types) > 0)

    @property
    def illustrative_materials(self):
        _illustrative_materials = []
        if self.tree is not None:
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
    def license_text(self):
        r = None
        if self.tree is not None:
            node = self.tree.find('.//license-p')
            if node is not None:
                r = xml_utils.node_text(node)
                if '>' in r:
                    r = r[r.rfind('>')+1:]
        return r

    @property
    def license_type(self):
        r = None
        if self.tree is not None:
            node = self.tree.find('.//license')
            if node is not None:
                r = node.attrib.get('license-type')
        return r

    @property
    def license_url(self):
        r = None
        if self.tree is not None:
            node = self.tree.find('.//license')
            if node is not None:
                r = node.attrib.get('{http://www.w3.org/1999/xlink}href')
                if r is not None:
                    if r.find('/deed.'):
                        r = r[0:r.find('/deed.')]
                    if r.endswith('/'):
                        r = r[:-1]
        return r

    @property
    def license_graphic(self):
        r = None
        if self.tree is not None:
            node = self.tree.find('.//license//graphic')
            if node is not None:
                r = node.attrib.get('{http://www.w3.org/1999/xlink}href')
        return r

    @property
    def hrefs(self):
        r = []
        if self.tree is not None:
            for parent in self.tree.findall('.//*[@{http://www.w3.org/1999/xlink}href]/..'):
                for elem in parent.findall('.//*[@{http://www.w3.org/1999/xlink}href]'):
                    href = elem.attrib.get('{http://www.w3.org/1999/xlink}href')
                    _href = HRef(href, elem, parent, xml_utils.node_xml(parent), self.prefix)
                    r.append(_href)
        return r

    @property
    def elements_which_has_id_attribute(self):
        if self.tree is not None:
            return self.tree.findall('.//*[@id]')

    @property
    def href_files(self):
        return [href for href in self.hrefs if href.is_internal_file] if self.hrefs is not None else []

    @property
    def tables(self):
        r = []
        if self.tree is not None:
            for t in self.tree.findall('.//*[table]'):
                graphic = t.find('./graphic')
                _href = None
                if graphic is not None:
                    src = graphic.attrib.get('{http://www.w3.org/1999/xlink}href')
                    xml = xml_utils.node_xml(graphic)

                    _href = HRef(src, graphic, t, xml, self.prefix)
                _table = Table(t.tag, t.attrib.get('id'), t.findtext('.//label'), xml_utils.node_text(t.find('.//caption')), _href, xml_utils.node_xml(t.find('./table')))
                r.append(_table)
        return r


class Article(ArticleXML):

    def __init__(self, tree, xml_name):
        ArticleXML.__init__(self, tree, xml_name)
        self.number = None
        self.number_suppl = None
        self.volume_suppl = None
        self.compl = None
        if self.tree is not None:
            self._issue_parts()
        self.pid = None
        self.creation_date_display = None
        self.creation_date = None
        self.last_update = None
        self._doi_query_result = None
        self._doi_pid = None
        self._doi_journal_and_article = None

    @property
    def clinical_trial_url(self):
        return self.ext_link_clinical_trial_href if self.ext_link_clinical_trial_href is not None else self.uri_clinical_trial_href

    @property
    def clinical_trial_text(self):
        return self.ext_link_clinical_trial_text if self.ext_link_clinical_trial_text is not None else self.uri_clinical_trial_text

    @property
    def page_range(self):
        _page_range = []
        if self.fpage is not None:
            _page_range.append(self.fpage)
        if self.lpage is not None:
            _page_range.append(self.lpage)
        _page_range = '-'.join(_page_range)
        return None if len(_page_range) == 0 else _page_range

    @property
    def pages(self):
        _pages = []
        if self.page_range is not None:
            _pages.append(self.page_range)
        if self.elocation_id is not None:
            _pages.append(self.elocation_id)
        return '; '.join(_pages)

    @property
    def doi_query_result(self):
        if self._doi_query_result is None:
            self._doi_query_result = article_utils.doi_query(self.doi)
        return self._doi_query_result

    @property
    def doi_pid(self):
        if self._doi_pid is None:
            self._doi_pid = article_utils.doi_pid(self.doi_query_result)
        return self._doi_pid

    @property
    def doi_journal_and_article(self):
        if self._doi_journal_and_article is None:
            self._doi_journal_and_article = article_utils.doi_journal_and_article(self.doi_query_result)
        return self._doi_journal_and_article

    def summary(self):
        data = {}
        data['journal-title'] = self.journal_title
        data['journal id NLM'] = self.journal_id_nlm_ta
        data['journal ISSN'] = ','.join([k + ':' + v for k, v in self.journal_issns.items() if v is not None]) if self.journal_issns is not None else None
        data['print ISSN'] = self.print_issn
        data['e-ISSN'] = self.e_issn
        data['publisher name'] = self.publisher_name
        data['issue label'] = self.issue_label
        data['issue pub date'] = self.issue_pub_dateiso[0:4] if self.issue_pub_dateiso is not None else None
        data['order'] = self.order
        data['doi'] = self.doi
        data['fpage-lpage-seq'] = '-'.join([str(item) for item in [self.fpage, self.lpage, self.fpage_seq]])
        data['lpage'] = self.lpage
        data['fpage'] = self.fpage
        data['elocation id'] = self.elocation_id

        return data

    @property
    def article_titles(self):
        titles = {}
        for title in self.titles:
            titles[title.language] = title.title
        return titles

    def _issue_parts(self):
        number_suppl = None
        volume_suppl = None

        number, suppl, compl = article_utils.get_number_suppl_compl(self.issue)
        number = article_utils.normalize_number(number)
        if number == '0':
            number = None
        if number is None and self.volume is None:
            number = 'ahead'

        suppl = article_utils.normalize_number(suppl)
        if suppl is not None:
            if number is None:
                volume_suppl = suppl
            else:
                number_suppl = suppl

        self.number = number
        self.number_suppl = number_suppl
        self.volume_suppl = volume_suppl
        self.compl = compl

    @property
    def is_issue_press_release(self):
        return self.compl == 'pr'

    @property
    def is_ahead(self):
        return (self.volume is None) and (self.number == 'ahead')

    @property
    def is_epub_only(self):
        r = False
        if self.epub_date is not None:
            if not self.is_ahead:
                if self.epub_ppub_date is None and self.collection_date is None:
                    r = True
        return r

    @property
    def ahpdate(self):
        return self.article_pub_date if self.is_ahead else None

    @property
    def ahpdate_dateiso(self):
        return article_utils.format_dateiso(self.ahpdate)

    @property
    def is_text(self):
        return len(self.keywords) == 0 and len(self.abstracts) == 0

    @property
    def previous_pid(self):
        def is_valid(pid):
            r = False
            if not d is None:
                r = (len(d) == 23) or (d.isdigit() and 0 < int(d) <= 99999)
            return r

        d = self.article_previous_id
        if not is_valid(d):
            if self.doi is not None:
                d = self.doi_pid
        if not is_valid(d):
            d = self._ahead_pid
        #if not is_valid(d):
        #    d = self.article_id_other
        if not is_valid(d):
            d = None
        return d

    @property
    def collection_dateiso(self):
        return article_utils.format_dateiso(self.collection_date)

    @property
    def epub_dateiso(self):
        return article_utils.format_dateiso(self.epub_date)

    @property
    def epub_ppub_dateiso(self):
        return article_utils.format_dateiso(self.epub_ppub_date)

    @property
    def issue_label(self):
        year = self.issue_pub_date.get('year', '') if self.issue_pub_date is not None else ''
        return article_utils.format_issue_label(year, self.volume, self.number, self.volume_suppl, self.number_suppl, self.compl)

    @property
    def issue_pub_dateiso(self):
        return article_utils.format_dateiso(self.issue_pub_date)

    @property
    def issue_pub_date(self):
        d = self.epub_ppub_date
        if d is None:
            d = self.collection_date
        if d is None:
            d = self.epub_date
        return d

    @property
    def article_pub_date(self):
        if self.epub_date is not None:
            if self.epub_date.get('day') is not None:
                if int(self.epub_date.get('day')) != 0:
                    return self.epub_date

    @property
    def article_pub_dateiso(self):
        return article_utils.format_dateiso(self.article_pub_date)

    @property
    def pub_date_year(self):
        pubdate = self.article_pub_date
        if pubdate is None:
            pubdate = self.issue_pub_date
        year = None
        if not pubdate is None:
            year = pubdate.get('year')
        return year

    @property
    def received_dateiso(self):
        return article_utils.format_dateiso(self.received)

    @property
    def accepted_dateiso(self):
        return article_utils.format_dateiso(self.accepted)

    @property
    def history_days(self):
        h = 0
        if self.received is not None and self.accepted is not None:
            h = (article_utils.dateiso2datetime(self.accepted_dateiso) - article_utils.dateiso2datetime(self.received_dateiso)).days
        return h

    @property
    def publication_days(self):
        d1 = self.accepted_dateiso
        d2 = self.article_pub_dateiso if self.article_pub_dateiso else self.issue_pub_dateiso
        if d1 is None or d2 is None:
            h = None
        else:
            h = (article_utils.dateiso2datetime(d2) - article_utils.dateiso2datetime(d1)).days
        return h

    @property
    def registration_days(self):
        h = None
        if self.accepted is not None:
            h = (datetime.now() - article_utils.dateiso2datetime(self.accepted_dateiso)).days
        return h


class ReferenceXML(object):

    def __init__(self, root):
        self.root = root
        self.element_citation = self.root.find('.//element-citation') if self.root is not None else None
        self._source = None

    @property
    def source(self):
        if self._source is None:
            if self.element_citation is not None:
                self._source = xml_utils.node_text(self.element_citation.find('.//source'))
        return self._source

    @property
    def id(self):
        return self.root.find('.').attrib.get('id')

    @property
    def language(self):
        lang = None
        for elem in ['.//source', './/article-title', './/chapter-title']:
            if self.root.find(elem) is not None:
                lang = xml_utils.element_lang(self.root.find(elem))
            if lang is not None:
                break
        return lang

    @property
    def article_title(self):
        if self.element_citation is not None:
            return xml_utils.node_text(self.element_citation.find('.//article-title'))

    @property
    def chapter_title(self):
        if self.element_citation is not None:
            return xml_utils.node_text(self.element_citation.find('.//chapter-title'))

    @property
    def trans_title(self):
        if self.element_citation is not None:
            return xml_utils.node_text(self.element_citation.find('.//trans-title'))

    @property
    def trans_title_language(self):
        if self.element_citation is not None:
            if self.element_citation.find('.//trans-title') is not None:
                return xml_utils.element_lang(self.element_citation.find('.//trans-title'))

    @property
    def publication_type(self):
        if self.element_citation is not None:
            return self.element_citation.attrib.get('publication-type')

    @property
    def ref_status(self):
        if self.element_citation is not None:
            return self.element_citation.attrib.get('specific-use')

    @property
    def xml(self):
        return xml_utils.node_xml(self.root)

    @property
    def mixed_citation(self):
        return xml_utils.node_text(self.root.find('.//mixed-citation'))

    @property
    def authors_list(self):
        r = []
        if self.element_citation is not None:
            for person_group in self.element_citation.findall('.//person-group'):
                person_group_id = person_group.attrib.get('person-group-type', 'author')
                for person in person_group.findall('.//name'):
                    p = PersonAuthor()
                    p.fname = person.findtext('given-names')
                    p.surname = person.findtext('surname')
                    p.suffix = person.findtext('suffix')
                    p.role = person_group_id
                    r.append(p)
                for collab in person_group.findall('.//collab'):
                    c = CorpAuthor()
                    c.collab = xml_utils.node_text(collab)
                    c.role = person_group_id
                    r.append(c)
        return r

    @property
    def authors_by_group(self):
        groups = []
        if self.element_citation is not None:
            for person_group in self.element_citation.findall('.//person-group'):
                role = person_group.attrib.get('person-group-type', 'author')
                authors = []
                for person in person_group.findall('.//name'):
                    p = PersonAuthor()
                    p.fname = person.findtext('given-names')
                    p.surname = person.findtext('surname')
                    p.suffix = person.findtext('suffix')
                    p.role = role
                    authors.append(p)
                for collab in person_group.findall('.//collab'):
                    c = CorpAuthor()
                    c.collab = xml_utils.node_text(collab)
                    c.role = role
                    authors.append(c)
                groups.append(authors)
        return groups

    @property
    def volume(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//volume')

    @property
    def issue(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//issue')

    @property
    def supplement(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//supplement')

    @property
    def edition(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//edition')

    @property
    def year(self):
        _year = None
        if self.element_citation is not None:
            _year = self.element_citation.findtext('.//year')
        if _year is None:
            if self.publication_type == 'confproc':
                _year = self.conference_date
        return _year

    @property
    def formatted_year(self):
        return article_utils.four_digits_year(self.year)

    @property
    def publisher_name(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//publisher-name')

    @property
    def publisher_loc(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//publisher-loc')

    @property
    def fpage(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//fpage')

    @property
    def lpage(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//lpage')

    @property
    def page_range(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//page-range')

    @property
    def elocation_id(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//elocation-id')

    @property
    def size(self):
        if self.element_citation is not None:
            node = self.element_citation.find('size')
            if node is not None:
                return {'size': node.text, 'units': node.attrib.get('units')} 

    @property
    def label(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//label')

    @property
    def etal(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//etal')

    @property
    def cited_date(self):
        _d = None
        if self.element_citation is not None:
            _d = self.element_citation.findtext('.//date-in-citation[@content-type="access-date"]')
            if _d is None:
                _d = self.element_citation.findtext('.//date-in-citation[@content-type="update"]')
        return _d

    @property
    def ext_link(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//ext-link')

    @property
    def _comments(self):
        if self.element_citation is not None:
            return self.element_citation.findall('.//comment')

    @property
    def degree(self):
        if self.element_citation is not None:
            if self.publication_type == 'thesis':
                return self.element_citation.findtext('.//comment')

    @property
    def comments(self):
        c = []
        if self.element_citation is not None:
            if self._comments is not None:
                c = [c.text for c in self._comments if c.text is not None]
        return '; '.join(c)

    @property
    def notes(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//notes')

    @property
    def contract_number(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//comment[@content-type="award-id"]')

    @property
    def doi(self):
        _doi = None
        if self.element_citation is not None:
            _doi = self.element_citation.findtext('.//pub-id[@pub-id-type="doi"]')
            if not _doi:
                for c in self.comments:
                    if 'doi:' in c:
                        _doi = c
        return _doi

    @property
    def pmid(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//pub-id[@pub-id-type="pmid"]')

    @property
    def pmcid(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//pub-id[@pub-id-type="pmcid"]')

    @property
    def conference_name(self):
        if self.element_citation is not None:
            return xml_utils.node_text(self.element_citation.find('.//conf-name'))

    @property
    def conference_location(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//conf-loc')

    @property
    def conference_date(self):
        if self.element_citation is not None:
            return self.element_citation.findtext('.//conf-date')


class Issue(object):

    def __init__(self, acron, volume, number, dateiso, volume_suppl, number_suppl, compl):
        self.volume = volume
        self.number = number
        self.dateiso = dateiso
        self.volume_suppl = volume_suppl
        self.number_suppl = number_suppl
        self.acron = acron
        self.year = dateiso[0:4]
        self.compl = compl

    @property
    def issue_label(self):
        return article_utils.format_issue_label(self.year, self.volume, self.number, self.volume_suppl, self.number_suppl, self.compl)
