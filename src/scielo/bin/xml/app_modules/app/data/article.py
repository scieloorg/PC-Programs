# coding=utf-8
import os
from datetime import datetime

from .. import article_utils
from ...generics import xml_utils
from ...generics import img_utils
from . import attributes


def first_item(l):
    if l is not None and len(l) > 0:
        return l[0]


def element_which_requires_permissions(node, node_graphic=None):
    missing_children = []
    missing_permissions = []
    for child in attributes.PERMISSION_ELEMENTS:
        if node.find('.//' + child) is None:
            missing_children.append(child)
    if len(missing_children) > 0:
        identif = node.tag
        if node.attrib.get('id') is None:
            identif = xml_utils.node_xml(node)
        else:
            identif = node.tag + '(' + node.attrib.get('id', '') + ')'
            if node_graphic is not None:
                identif += '/graphic'
        missing_permissions.append([identif, missing_children])
    return missing_permissions


class AffiliationXML(object):

    def __init__(self, node):
        self.node = node
        self.xml_node = xml_utils.XMLNode(node)
        self._aff = None
        self._institution_id = None

    @property
    def xml(self):
        return self.xml_node.xml

    @property
    def id(self):
        return self.node.attrib.get('id')

    @property
    def institution_id(self):
        if self._institution_id is None:
            r = []
            for node in self.xml_node.nodes_data(['.//institution-id']):
                if node is not None:
                    r.append((node[0], node[1].get('institution-id-type')))
            self._institution_id = r
        return self._institution_id

    @property
    def city(self):
        return self.xml_node.nodes_text(['.//city', './/named-content[@content-type="city"]'])

    @property
    def state(self):
        return self.xml_node.nodes_text(['.//state', './/named-content[@content-type="state"]'])

    @property
    def country(self):
        r = []
        for node in self.xml_node.nodes(['.//country']):
            r.append((node.attrib.get('country'), node.text))
        return r

    @property
    def orgname(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="orgname"]'])

    @property
    def norgname(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="normalized"]'])

    @property
    def orgdiv1(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="orgdiv1"]'])

    @property
    def orgdiv2(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="orgdiv2"]'])

    @property
    def orgdiv3(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="orgdiv3"]'])

    @property
    def label(self):
        return self.xml_node.nodes_text(['.//label'])

    @property
    def email(self):
        return self.xml_node.nodes_text(['.//email'])

    @property
    def original(self):
        return self.xml_node.nodes_text(['.//institution[@content-type="original"]'])

    @property
    def aff(self):
        if self._aff is None:
            self._aff = Affiliation()
            self._aff.xml = self.xml
            self._aff.id = self.id
            self._aff.city = first_item(self.city)
            self._aff.state = first_item(self.state)
            country = first_item(self.country)
            if country is not None:
                self._aff.i_country, self._aff.country = country
            self._aff.orgname = first_item(self.orgname)
            self._aff.norgname = first_item(self.norgname)
            self._aff.orgdiv1 = first_item(self.orgdiv1)
            self._aff.orgdiv2 = first_item(self.orgdiv2)
            self._aff.orgdiv3 = first_item(self.orgdiv3)
            self._aff.label = first_item(self.label)
            self._aff.email = first_item(self.email)
            self._aff.original = first_item(self.original)
        return self._aff


class Affiliation(object):

    def __init__(self):
        self.xml = None
        self.id = None
        self.city = None
        self.state = None
        self.country = None
        self.i_country = None
        self.orgname = None
        self.norgname = None
        self.orgdiv1 = None
        self.orgdiv2 = None
        self.orgdiv3 = None
        self.label = None
        self.email = None
        self.original = None


def items_by_lang(items):
    r = {}
    for item in items:
        if item is not None:
            if item.language not in r.keys():
                r[item.language] = []
            r[item.language].append(item)
    return r


class TableParentXML(object):

    def __init__(self, node):
        self.node = node
        self.xml_node = xml_utils.XMLNode(node)
        self._table_parent = None

    @property
    def name(self):
        return self.node.tag

    @property
    def id(self):
        return self.node.get('id')

    @property
    def label(self):
        return self.xml_node.nodes_text(['.//label'])

    @property
    def caption(self):
        return self.xml_node.nodes_text(['.//caption'])

    @property
    def table(self):
        return self.xml_node.nodes_xml(['.//table'])

    @property
    def table_parent(self):
        if self._table_parent is None:
            self._table_parent = TableParent()
            self._table_parent.name = self.name
            self._table_parent.id = self.id
            self._table_parent.label = first_item(self.label)
            self._table_parent.caption = first_item(self.caption)
            self._table_parent.table = first_item(self.table)
        return self._table_parent


class TableParent(object):

    def __init__(self):
        self.table = None
        self.name = None
        self.id = None
        self.label = None
        self.caption = None
        self.graphic = None


class HRef(object):

    def __init__(self, src, element, parent, xml, xml_name):
        self.src = src
        self.element = element
        self.xml = xml
        self.name_without_extension, self.ext = os.path.splitext(src)

        self.id = element.attrib.get('id', None)
        if self.id is None and parent is not None:
            self.id = parent.attrib.get('id', None)
        self.parent = parent
        self.is_internal_file = '/' not in src
        if element.tag in ['ext-link', 'uri', 'related-article']:
            self.is_internal_file = False
        self.is_image = self.ext in img_utils.IMG_EXTENSIONS

    @property
    def is_inline(self):
        return self.element.tag in ['inline-graphic', 'inline-formula']

    @property
    def is_disp_formula(self):
        return self.parent.tag == 'disp-formula'

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

    @property
    def href_attach_type(self):
        parent_tag, tag = self.parent.tag, self.element.tag
        if 'suppl' in tag or 'media' == tag:
            attach_type = 's'
        elif 'inline' in tag:
            attach_type = 'i'
        elif parent_tag in ['equation', 'disp-formula']:
            attach_type = 'e'
        else:
            attach_type = 'g'
        return attach_type


class ContribId(object):

    def __init__(self, node):
        self.attrib = node.attrib
        self.xml = xml_utils.node_xml(node)
        self.value = node.text


class ContribXML(object):

    def __init__(self, node):
        self.node = node
        self.xml_node = xml_utils.XMLNode(node)
        self._contrib = None
        self.fnames = self.xml_node.nodes_text(['.//given-names'])
        self.surnames = self.xml_node.nodes_text(['.//surname'])
        self.suffixes = self.xml_node.nodes_text(['.//suffix'])
        self.prefixes = self.xml_node.nodes_text(['.//prefix'])
        self.contrib_id_items = [ContribId(item) for item in node.findall('.//contrib-id')]
        self.xref_items = self.xml_node.nodes_data(['.//xref[@ref-type="aff"]'])

    @property
    def collabs(self):
        if self.node.tag == 'collab':
            return [xml_utils.node_text(self.node)]
        return self.xml_node.nodes_text(['.//collab'])

    @property
    def anonymous_author(self):
        if self.node.tag == 'anonymous':
            return AnonymousAuthor('anonymous')

    @property
    def person_author(self):
        if len(self.surnames) > 0:
            c = PersonAuthor()
            c.fname = first_item(self.fnames)
            c.surname = first_item(self.surnames)
            c.suffix = first_item(self.suffixes)
            c.prefix = first_item(self.prefixes)
            c.xref = []
            c.contrib_id = {}
            for contrib_id in self.contrib_id_items:
                c.contrib_id[contrib_id.attrib.get('contrib-id-type')] = contrib_id.value
            c.role = self.node.get('contrib-type')
            for xref in self.xref_items:
                if xref is not None:
                    text, attribs = xref
                    if attribs.get('ref-type') == 'aff':
                        c.xref.append(attribs.get('rid'))
            return c

    @property
    def corp_author(self):
        if len(self.collabs) > 0:
            c = CorpAuthor()
            c.role = self.node.attrib.get('contrib-type')
            c.collab = first_item(self.collabs)
            return c

    def contrib(self, role=None):
        if self._contrib is None:
            self._contrib = self.person_author
            if self._contrib is None:
                self._contrib = self.corp_author
            if self._contrib is None:
                self._contrib = self.anonymous_author
            if self._contrib is not None and role is not None:
                self._contrib.role = role
        return self._contrib


class AnonymousAuthor(object):

    def __init__(self, fullname):
        self.fullname = fullname


class PersonAuthor(object):

    def __init__(self):
        self.fname = None
        self.surname = None
        self.suffix = None
        self.prefix = None
        self.contrib_id = None
        self.role = None
        self.xref = None

    @property
    def fullname(self):
        return ' '.join([item for item in [self.fname, self.surname] if item is not None])


class CorpAuthor(object):

    def __init__(self):
        self.role = None
        self.collab = None

    @property
    def fullname(self):
        return self.collab


class TitleXML(object):

    def __init__(self, node, lang=None):
        self.node = node
        self.lang = lang
        self.xml_node = xml_utils.XMLNode(self.node)
        self._title = None

    @property
    def article_title(self):
        items = []
        for title in self.xml_node.nodes_text(['article-title', 'trans-title']):
            if title is not None:
                items.append(article_utils.remove_xref(title))
        return first_item(items)

    @property
    def subtitle(self):
        items = []
        for title in self.xml_node.nodes_text(['subtitle', 'trans-subtitle']):
            if title is not None:
                items.append(article_utils.remove_xref(title))
        return first_item(items)

    @property
    def language(self):
        lang = xml_utils.element_lang(self.node)
        return lang if lang is not None else self.lang

    @property
    def title(self):
        if self._title is None:
            self._title = Title()
            self._title.title = self.article_title
            self._title.subtitle = self.subtitle
            self._title.language = self.language
        return self._title


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

    def __init__(self, tree):
        self.tree = tree
        self.journal_meta = None
        self.article_meta = None
        self.body = None
        self.back = None
        self.translations = []
        self.sub_articles = []
        self.responses = []
        self._fpage_node = None
        self._fpage = None
        self.fpage_seq = None
        self._epub_ppub_date = None

        if tree is not None:
            self.journal_meta = self.tree.find('./front/journal-meta')
            self.article_meta = self.tree.find('./front/article-meta')
            self.body = self.tree.find('.//body')
            self.back = self.tree.find('.//back')
            self.translations = self.tree.findall('./sub-article[@article-type="translation"]')
            for s in self.tree.findall('./sub-article'):
                if s.attrib.get('article-type') != 'translation':
                    self.sub_articles.append(s)
            self.responses = self.tree.findall('./response')

    def paragraphs_startswith(self, character=':'):
        paragraphs = []
        if self.tree is not None:
            for node_p in self.tree.findall('.//p'):
                text = xml_utils.node_text(node_p)
                if text is not None:
                    if text.strip().startswith(character):
                        paragraphs.append(xml_utils.node_xml(node_p))
        return paragraphs

    @property
    def months(self):
        items = []
        nodes = self.tree.findall('.//pub-date[month]')
        for node in nodes:
            items.append((node.tag, node.attrib.get('pub-type'), node.findtext('month')))
        return items

    @property
    def seasons(self):
        items = []
        nodes = self.tree.findall('.//pub-date[season]')
        for node in nodes:
            items.append((node.tag, node.attrib.get('pub-type'), node.findtext('season')))
        return items

    def sections(self, node):
        _sections = []
        if node is not None:
            for node in node.findall('sec'):
                _sections.append((node.attrib.get('sec-type', ''), node.findtext('title')))
        return _sections

    @property
    def article_sections(self):
        r = []
        r.append({'article': self.sections(self.body)})
        if self.translations is not None:
            for item in self.translations:
                r.append({'sub-article/[@id="' + item.attrib.get('id', 'None') + '"]': self.sections(item.find('.//body'))})
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
    def any_xref_ranges(self):
        _any_xref_ranges = {}
        for xref_type, xref_type_nodes in self.any_xref_parent_nodes.items():
            if xref_type is not None:
                if xref_type not in _any_xref_ranges.keys():
                    _any_xref_ranges[xref_type] = []
                for xref_parent_node, xref_node_items in xref_type_nodes:
                    # nodes de um tipo de xref
                    xref_parent_xml = xml_utils.tostring(xref_parent_node)
                    parts = xref_parent_xml.replace('<xref', '~BREAK~<xref').split('~BREAK~')
                    parts = [item for item in parts if ' ref-type="' + xref_type + '"' in item]
                    k = 0
                    for item in parts:
                        text = ''
                        delimiter = ''
                        if '</xref>' in item:
                            delimiter = '</xref>'
                        elif '/>' in item:
                            delimiter = '/>'
                        if len(delimiter) > 0:
                            if delimiter in item:
                                text = item[item.find(delimiter)+len(delimiter):]
                        if text.replace('</sup>', '').replace('<sup>', '').startswith('-'):
                            start = None
                            end = None
                            n = xref_node_items[k].attrib.get('rid')
                            if n is not None:
                                n = n[1:]
                                if n.isdigit():
                                    start = int(n)
                            if k + 1 < len(xref_node_items):
                                n = xref_node_items[k+1].attrib.get('rid')
                                if n is not None:
                                    n = n[1:]
                                    if n.isdigit():
                                        end = int(n)
                                if all([start, end]):
                                    _any_xref_ranges[xref_type].append([start, end, xref_node_items[k], xref_node_items[k+1]])
                        k += 1
        return _any_xref_ranges

    @property
    def any_xref_parent_nodes(self):
        _any_xref_parent_nodes = {}
        if self.tree is not None:
            for xref_parent_node in self.tree.findall('.//*[xref]'):
                xref_nodes = {}
                for xref_node in xref_parent_node.findall('.//xref'):
                    xref_type = xref_node.attrib.get('ref-type')
                    if xref_type not in xref_nodes.keys():
                        xref_nodes[xref_type] = []
                    xref_nodes[xref_type].append(xref_node)

                    if xref_type not in _any_xref_parent_nodes.keys():
                        _any_xref_parent_nodes[xref_type] = []

                for xref_type, xref_type_nodes in xref_nodes.items():
                    if len(xref_type_nodes) > 1:
                        # considerar apenas quando há mais de 1 xref[@ref-type='<any>']
                        # pois range somente éh possível a partir de 2
                        _any_xref_parent_nodes[xref_type].append((xref_parent_node, xref_type_nodes))
        return _any_xref_parent_nodes

    @property
    def bibr_xref_ranges(self):
        _bibr_xref_ranges = []
        if self.is_bibr_xref_number:
            for xref_parent_node, bibr_xref_node_items in self.bibr_xref_parent_nodes:
                xref_parent_xml = xml_utils.tostring(xref_parent_node)
                parts = xref_parent_xml.replace('<xref', '~BREAK~<xref').split('~BREAK~')
                if len(bibr_xref_node_items) != len(parts) - 1:
                    parts = xref_parent_xml.replace('<xref ref-type="bibr', '~BREAK~<xref ref-type="bibr').split('~BREAK~')

                if len(bibr_xref_node_items) == len(parts) - 1:
                    if len(bibr_xref_node_items) > 1:
                        for k in range(1, len(bibr_xref_node_items)):
                            text = ''
                            delimiter = ''
                            if '</xref>' in parts[k]:
                                delimiter = '</xref>'
                            elif '/>' in parts[k]:
                                delimiter = '/>'
                            if len(delimiter) > 0:
                                if delimiter in parts[k]:
                                    text = parts[k][parts[k].find(delimiter)+len(delimiter):]
                            if text.replace('</sup>', '').replace('<sup>', '').startswith('-'):
                                start = None
                                end = None
                                n = bibr_xref_node_items[k-1].attrib.get('rid')
                                if n is not None:
                                    n = n[1:]
                                    if n.isdigit():
                                        start = int(n)
                                n = bibr_xref_node_items[k].attrib.get('rid')
                                if n is not None:
                                    n = n[1:]
                                    if n.isdigit():
                                        end = int(n)
                                if None not in [start, end]:
                                    _bibr_xref_ranges.append([start, end, bibr_xref_node_items[k-1], bibr_xref_node_items[k]])
        return _bibr_xref_ranges

    @property
    def is_bibr_xref_number(self):
        _is_bibr_xref_number = False
        if self.bibr_xref_nodes is not None:
            for bibr_xref in self.bibr_xref_nodes:
                if bibr_xref.text is not None:
                    if bibr_xref.text.replace('(', '')[0].isdigit():
                        _is_bibr_xref_number = True
                    else:
                        _is_bibr_xref_number = False
                    break
        return _is_bibr_xref_number

    @property
    def bibr_xref_parent_nodes(self):
        _bibr_xref_parent_nodes = []
        if self.tree is not None:
            for node in self.tree.findall('.//*[xref]'):
                bibr_xref = node.findall('xref[@ref-type="bibr"]')
                if len(bibr_xref) > 0:
                    _bibr_xref_parent_nodes.append((node, bibr_xref))
        return _bibr_xref_parent_nodes

    @property
    def bibr_xref_nodes(self):
        if self.tree is not None:
            return self.tree.findall('.//xref[@ref-type="bibr"]')

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
    def sps_version_number(self):
        version_number = self.sps
        if version_number is not None:
            if 'sps-' in version_number:
                version_number = version_number[4:]
            if version_number.replace('.', '').isdigit():
                return float(version_number)

    @property
    def article_type(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('article-type')

    @property
    def body_words(self):
        if self.body is not None:
            return xml_utils.remove_tags(' '.join(xml_utils.node_text(self.body).split()))

    @property
    def language(self):
        if self.tree is not None:
            return xml_utils.element_lang(self.tree.find('.'))

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
        #<related-article related-article-type="in-this-issue" id="pr01" xmlns:xlink="https://www.w3.org/1999/xlink" xlink:href="10.1590/S0102-311X2013000500014 " ext-link-type="doi"/>
        # ^i<doi>^tdoi^rfrom-press-release-to-article
        #
        #registro de errata, link para artigo
        #<related-article related-article-type="corrected-article" vol="29" page="970" id="RA1" xmlns:xlink="https://www.w3.org/1999/xlink" xlink:href="10.1590/S0102-311X2013000500014" ext-link-type="doi"/>
        # ^i<doi>^tdoi^rfrom-corrected-article-to-article
        r = []
        if self.article_meta is not None:
            related = self.article_meta.findall('related-article')
            for rel in related:
                item = {}
                item['href'] = rel.attrib.get('{http://www.w3.org/1999/xlink}href')
                item['related-article-type'] = rel.attrib.get('related-article-type')
                item['ext-link-type'] = rel.attrib.get('ext-link-type')
                if item['ext-link-type'] == 'scielo-pid':
                    item['ext-link-type'] = 'pid'
                item['id'] = rel.attrib.get('id')
                if item['related-article-type'] not in attributes.related_articles_type:
                    item['id'] = ''.join([c for c in item['id'] if c.isdigit()])
                item['xml'] = xml_utils.node_xml(rel)
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
    def journal_id_publisher_id(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('journal-id[@journal-id-type="publisher-id"]')

    @property
    def journal_id_nlm_ta(self):
        if self.journal_meta is not None:
            return self.journal_meta.findtext('journal-id[@journal-id-type="nlm-ta"]')

    @property
    def journal_issns(self):
        if self.journal_meta is not None:
            return {item.attrib.get('pub-type', 'epub'):item.text for item in self.journal_meta.findall('issn')}
        return {}

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
    def toc_sections(self):
        r = []
        if self.tree.find('.') is not None:
            r = xml_utils.XMLNode(self.tree.find('.')).nodes_text(['.//subj-group/subject'])
        return r

    @property
    def sorted_toc_sections(self):
        return sorted(self.toc_sections)

    @property
    def normalized_toc_section(self):
        return attributes.normalized_toc_section(self.toc_section)

    @property
    def keywords_by_lang(self):
        k = {}
        for item in self.keywords:
            if item['l'] not in k.keys():
                k[item['l']] = []

            t = Text()
            t.language = item['l']
            t.text = item['k']

            k[item['l']].append(t)
        return k

    @property
    def article_keywords(self):
        k = []
        if self.article_meta is not None:
            for node in self.article_meta.findall('kwd-group'):
                language = xml_utils.element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': xml_utils.node_text(kw)})
        return k

    @property
    def subarticle_keywords(self):
        k = []
        for subart in self.translations:
            for node in subart.findall('.//kwd-group'):
                language = xml_utils.element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': xml_utils.node_text(kw)})
        return k

    @property
    def keywords(self):
        return self.article_keywords + self.subarticle_keywords

    @property
    def contrib_names(self):
        items = []
        for item in self.article_contrib_items:
            if isinstance(item, PersonAuthor):
                items.append(item)
        for subartid, subarticle_contrib_items in self.subarticles_contrib_items.items():
            items.extend([subarticlecontrib for subarticlecontrib in subarticle_contrib_items if isinstance(subarticlecontrib, PersonAuthor)])
        return items

    @property
    def article_contrib_items(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib'):
                k.append(ContribXML(contrib).contrib())
            return [item for item in k if item is not None]
        return k

    @property
    def subarticles_contrib_items(self):
        contribs = {}
        if self.sub_articles is not None:
            for subart in self.sub_articles:
                if subart.attrib.get('article-type') != 'translation':
                    contribs[subart.attrib.get('id')] = []
                    for contrib in subart.findall('.//contrib'):
                        a = ContribXML(contrib).contrib()
                        if a is not None:
                            contribs[subart.attrib.get('id')].append(a)
        return contribs

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
    def first_author_surname(self):
        surname = None
        authors = self.contrib_names
        if len(authors) > 0:
            surname = authors[0].surname
            if authors[0].suffix is not None:
                surname += ' ' + authors[0].suffix
        return surname

    @property
    def contrib_collabs(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib[collab]'):
                a = ContribXML(contrib).contrib()
                if a is not None:
                    k.append(a)
        return k

    def short_article_title(self, size=None):
        if size is None:
            return self.title
        elif not size.isdigit():
            return self.title
        elif self.title is not None:
            if len(self.title) > size:
                return self.title[0:size] + '...'
            else:
                return self.title

    @property
    def title_group_title(self):
        k = []
        if self.article_meta is not None:
            return [TitleXML(node, self.language).title for node in self.article_meta.findall('.//title-group')]
        return k

    @property
    def trans_title_group_titles(self):
        k = []
        if self.article_meta is not None:
            return [TitleXML(node).title for node in self.article_meta.findall('.//trans-title-group')]
        return k

    @property
    def translations_title_group_titles(self):
        k = []
        if self.translations is not None:
            for subart in self.translations:
                for node in subart.findall('*/title-group'):
                    t = TitleXML(node).title
                    t.language = xml_utils.element_lang(subart)
                    k.append(t)
        return k

    @property
    def titles(self):
        return self.title_group_title + self.trans_title_group_titles + self.translations_title_group_titles

    @property
    def title(self):
        if len(self.titles) > 0:
            return self.titles[0].title

    @property
    def titles_by_lang(self):
        return items_by_lang(self.titles)

    @property
    def title_abstract_kwd_languages(self):
        items = []
        for item in [self.keywords_by_lang, self.abstracts_by_lang, self.titles_by_lang]:
            items.extend(list(item.keys()))
        return [item for item in list(set(items)) if item is not None]

    @property
    def trans_languages(self):
        k = []
        if self.translations is not None:
            for node in self.translations:
                k.append(xml_utils.element_lang(node))
        return k

    @property
    def article_id(self):
        if self.doi is not None:
            return self.doi
        elif self.publisher_article_id is not None:
            return self.publisher_article_id

    @property
    def doi(self):
        if self.article_meta is not None:
            _doi = self.article_meta.findtext('article-id[@pub-id-type="doi"]')
            if _doi is not None:
                return _doi.lower()

    @property
    def publisher_article_id(self):
        if self.article_meta is not None:
            _publisher_article_id = self.article_meta.findtext('article-id[@pub-id-type="publisher-id"]')
            if _publisher_article_id is not None:
                return _publisher_article_id.lower()

    @property
    def marked_to_delete(self):
        if self.article_meta is not None:
            return self.article_meta.find('article-id[@specific-use="delete"]') is not None
        return False

    @property
    def previous_article_pid(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('article-id[@specific-use="previous-pid"]')

    @property
    def order(self):
        _order = self.article_id_other
        if _order is None:
            _order = self.fpage
        if _order is None or not _order.isdigit():
            _order = '0'
        return _order.zfill(5)

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
        if self.article_meta is not None:
            return [xml_utils.node_text(item) for item in self.article_meta.findall('.//funding-source')]

    @property
    def principal_award_recipient(self):
        if self.article_meta is not None:
            return [xml_utils.node_text(item) for item in self.article_meta.findall('.//principal-award-recipient')]

    @property
    def principal_investigator(self):
        if self.article_meta is not None:
            return [xml_utils.node_text(item) for item in self.article_meta.findall('.//principal-investigator')]

    @property
    def award_id(self):
        if self.article_meta is not None:
            return [xml_utils.node_text(item) for item in self.article_meta.findall('.//award-id')]

    @property
    def funding_statement(self):
        if self.article_meta is not None:
            return [xml_utils.node_text(item) for item in self.article_meta.findall('.//funding-statement')]

    @property
    def ack_xml(self):
        #107
        if self.back is not None:
            return xml_utils.node_xml(self.back.find('.//ack'))

    @property
    def financial_disclosure(self):
        if self.tree is not None:
            return xml_utils.XMLNode(self.tree).nodes_text(['.//fn[@fn-type="financial-disclosure"]'])

    @property
    def fn_financial_disclosure(self):
        return self.financial_disclosure

    @property
    def fpage(self):
        if self._fpage is None:
            if self.article_meta is not None:
                self._fpage_node = self.article_meta.find('fpage')
                if self._fpage_node is not None:
                    self._fpage = article_utils.normalize_number(self._fpage_node.text)
                    self.fpage_seq = self._fpage_node.attrib.get('seq')
        return self._fpage

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
        return self.article_affiliations + self.subarticles_affiliations

    @property
    def article_affiliations(self):
        affs = []
        if self.article_meta is not None:
            for aff in self.article_meta.findall('.//aff'):
                affs.append(AffiliationXML(aff))
        return affs

    @property
    def subarticles_affiliations(self):
        affs = []
        if self.sub_articles is not None:
            for sub_art in self.sub_articles:
                if sub_art.attrib.get('article-type') != 'translation':
                    for aff in sub_art.findall('.//aff'):
                        affs.append(AffiliationXML(aff))
        return affs

    @property
    def uri_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="ClinicalTrial" xlink:href="https://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.article_meta is not None:
            node = self.article_meta.find('.//uri[@content-type="clinical-trial"]')
            if node is None:
                node = self.article_meta.find('.//uri[@content-type="ClinicalTrial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def uri_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="ClinicalTrial" xlink:href="https://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.article_meta is not None:
            node = self.article_meta.find('.//uri[@content-type="clinical-trial"]')
            if node is None:
                node = self.article_meta.find('.//uri[@content-type="ClinicalTrial"]')
            if node is not None:
                return xml_utils.node_text(node)

    @property
    def ext_link_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="ClinicalTrial" xlink:href="https://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.article_meta is not None:
            node = self.article_meta.find('.//ext-link[@ext-link-type="clinical-trial"]')
            if node is None:
                node = self.article_meta.find('.//ext-link[@ext-link-type="ClinicalTrial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def ext_link_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="ClinicalTrial" xlink:href="https://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.article_meta is not None:
            node = self.article_meta.find('.//ext-link[@ext-link-type="clinical-trial"]')
            if node is None:
                node = self.article_meta.find('.//ext-link[@ext-link-type="ClinicalTrial"]')
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
        q = 1
        if self.fpage is not None and self.lpage is not None:
            if self.fpage.isdigit() and self.lpage.isdigit():
                q = int(self.lpage) - int(self.fpage) + 1
        return q

    def total(self, node, xpath):
        q = 0
        if node is not None:
            q = len(node.findall(xpath))
        return q

    def total_group(self, element_name, element_parent):
        q = 0
        nodes = self.tree.findall('.//*[' + element_name + ']')
        if nodes is not None:
            for node in nodes:
                if node.tag == element_parent:
                    q += 1
                else:
                    q += len(node.findall(element_name))
        return q

    @property
    def total_of_references(self):
        return self.total(self.tree, './/ref')

    @property
    def total_of_tables(self):
        return self.total_group('table-wrap', 'table-wrap-group')

    @property
    def total_of_equations(self):
        return self.total(self.tree, './/disp-formula')

    @property
    def total_of_figures(self):
        return self.total_group('fig', 'fig-group')

    @property
    def formulas_nodes(self):
        r = []
        if self.tree is not None:
            if self.tree.findall('.//disp-formula') is not None:
                r.extend(self.tree.findall('.//disp-formula'))
            if self.tree.findall('.//inline-formula') is not None:
                r.extend(self.tree.findall('.//inline-formula'))
        return r

    @property
    def formulas(self):
        data = []
        for node in self.formulas_nodes:
            data.append(ArticleFormula(node))
        return data

    @property
    def disp_formulas(self):
        return [item for item in self.formulas if item.tag == 'disp-formula']

    @property
    def tablewraps(self):
        data = []
        nodes = self.tree.findall('.//table-wrap')
        if nodes is not None:
            for node in nodes:
                data.append(ArticleTableWrap(node))
        return data

    @property
    def abstract(self):
        r = []
        if self.article_meta is not None:
            for a in self.article_meta.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = self.language
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
        return r

    @property
    def trans_abstracts(self):
        r = []
        if self.article_meta is not None:
            for a in self.article_meta.findall('.//trans-abstract'):
                _abstract = Text()
                _abstract.language = xml_utils.element_lang(a)
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
        return r

    @property
    def subarticle_abstracts(self):
        r = []
        for subart in self.translations:
            language = xml_utils.element_lang(subart)
            for a in subart.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = language
                _abstract.text = xml_utils.node_text(a)
                r.append(_abstract)
        return r

    @property
    def abstracts_by_lang(self):
        return items_by_lang(self.abstracts)

    @property
    def abstracts(self):
        return self.abstract + self.trans_abstracts + self.subarticle_abstracts

    @property
    def references_xml(self):
        refs = []
        if self.back is not None:
            for ref in self.back.findall('.//ref'):
                refs.append(ReferenceXML(ref))
        return refs

    @property
    def refstats(self):
        _refstats = {}
        for ref_xml in self.references_xml:
            pubtype = ref_xml.reference.publication_type
            if ref_xml.reference.publication_type not in _refstats.keys():
                if pubtype is None:
                    pubtype = 'None'
                _refstats[pubtype] = 0
            _refstats[pubtype] += 1
        return _refstats

    @property
    def display_only_stats(self):
        q = 0
        for ref_xml in self.references_xml:
            if ref_xml.reference.ref_status is not None:
                if ref_xml.reference.ref_status == 'display-only':
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
        if self.article_meta is not None:
            return xml_utils.date_element(self.article_meta.find('history/date[@date-type="received"]'))

    @property
    def accepted(self):
        if self.article_meta is not None:
            return xml_utils.date_element(self.article_meta.find('history/date[@date-type="accepted"]'))

    @property
    def collection_date(self):
        if self.article_meta is not None:
            return xml_utils.date_element(self.article_meta.find('pub-date[@pub-type="collection"]'))

    @property
    def epub_ppub_date(self):
        if self._epub_ppub_date is None:
            if self.article_meta is not None:
                self._epub_ppub_date = xml_utils.date_element(self.article_meta.find('pub-date[@pub-type="epub-ppub"]'))
        return self._epub_ppub_date

    @property
    def epub_date(self):
        if self.article_meta is not None:
            date_node = self.article_meta.find('pub-date[@pub-type="epub"]')
            if date_node is None:
                date_node = self.article_meta.find('pub-date[@date-type="preprint"]')
            return xml_utils.date_element(date_node)

    @property
    def is_article_press_release(self):
        return self.article_type == 'in-brief' and len(self.related_articles) > 0

    @property
    def illustrative_materials(self):
        _illustrative_materials = []
        if self.tree is not None:
            if len(self.tree.findall('.//table-wrap')) > 0:
                _illustrative_materials.append('TAB')
            figs = len(self.tree.findall('.//fig'))
            if figs > 0:
                _illustrative_materials.append('GRA')

        if len(_illustrative_materials) > 0:
            return _illustrative_materials
        else:
            return 'ND'

    @property
    def article_copyright(self):
        _article_cpright = {}
        if self.article_meta is not None:
            _article_cpright['statement'] = self.article_meta.findtext('.//copyright-statement')
            _article_cpright['year'] = self.article_meta.findtext('.//copyright-year')
            _article_cpright['holder'] = self.article_meta.findtext('.//copyright-holder')
        return _article_cpright

    @property
    def article_licenses(self):
        _article_licenses = {}
        if self.article_meta is not None:
            for license_node in self.article_meta.findall('.//license'):
                lang = xml_utils.element_lang(license_node)
                href = license_node.attrib.get('{http://www.w3.org/1999/xlink}href')

                _article_licenses[lang] = {}
                _article_licenses[lang]['href'] = href
                if href is not None:
                    if 'creativecommons.org/licenses/' in href:
                        _article_licenses[lang]['code-and-version'] = href[href.find('creativecommons.org/licenses/')+len('creativecommons.org/licenses/'):].lower()
                        if 'igo' in _article_licenses[lang]['code-and-version']:
                            _article_licenses[lang]['code-and-version'] = _article_licenses[lang]['code-and-version'][0:_article_licenses[lang]['code-and-version'].find('igo')+len('igo')]
                        elif '/' in _article_licenses[lang]['code-and-version']:
                            items = _article_licenses[lang]['code-and-version'].split('/')
                            _article_licenses[lang]['code-and-version'] = items[0] + '/' + items[1]
                        else:
                            _article_licenses[lang]['code-and-version'] = None
                _article_licenses[lang]['type'] = license_node.attrib.get('license-type')
                _article_licenses[lang]['text'] = xml_utils.node_findtext(license_node, './/license-p')
                _article_licenses[lang]['xml'] = xml_utils.node_xml(license_node)
        return _article_licenses

    @property
    def article_license_code_and_version_lang(self):
        r = {}
        for lang, lic in self.article_licenses.items():
            if lic.get('code-and-version') is not None:
                r[lic.get('code-and-version')] = []
            r[lic.get('code-and-version')].append(lang)
        return r

    @property
    def article_license_code_and_versions(self):
        return self.article_license_code_and_version_lang.keys()

    @property
    def permissions_required(self):
        missing_permissions = []
        for tag in attributes.REQUIRES_PERMISSIONS:
            xpath = './/' + tag
            if tag == 'graphic':
                xpath = './/*[graphic]'

                for node in self.tree.findall(xpath):
                    if node.tag not in ['fig', 'table-wrap']:
                        for node_graphic in node.findall('graphic'):
                            for elem in element_which_requires_permissions(node, node_graphic):
                                missing_permissions.append(elem)
            else:
                for node in self.tree.findall(xpath):
                    for elem in element_which_requires_permissions(node):
                        missing_permissions.append(elem)
        return missing_permissions

    @property
    def elements_which_has_id_attribute(self):
        if self.tree is not None:
            return self.tree.findall('.//*[@id]')

    @property
    def href_files(self):
        return [href for href in self.hrefs if href.is_internal_file] if self.hrefs is not None else []

    @property
    def hrefs(self):
        items = []
        if self.tree is not None:
            for parent in self.tree.findall('.//*[@{http://www.w3.org/1999/xlink}href]/..'):
                for elem in parent.findall('*[@{http://www.w3.org/1999/xlink}href]'):
                    if elem.tag != 'related-article':
                        href = elem.attrib.get('{http://www.w3.org/1999/xlink}href')
                        _href = HRef(href, elem, parent, xml_utils.node_xml(parent), self.prefix)
                        items.append(_href)
        return items

    @property
    def inline_graphics(self):
        return [item for item in self.hrefs if item.is_inline]

    @property
    def disp_formulas(self):
        return [item for item in self.hrefs if item.is_disp_formula]

    def inline_graphics_heights(self, path):
        return article_utils.image_heights(path, self.inline_graphics)

    def disp_formulas_heights(self, path):
        return article_utils.image_heights(path, self.disp_formulas)

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
                r.append(TableParentXML(t).table_parent)
        return r


class Article(ArticleXML):

    def __init__(self, tree, xml_name):
        ArticleXML.__init__(self, tree)
        self.xml_name = xml_name
        self.prefix = xml_name.replace('.xml', '')
        self.new_prefix = self.prefix
        self.filename = xml_name if xml_name.endswith('.xml') else xml_name + '.xml'
        self.number = None
        self.number_suppl = None
        self.volume_suppl = None
        self.compl = None
        if self.tree is not None:
            self._issue_parts()
        self.pid = None
        self.creation_date_display = None
        self.creation_date = None
        self.last_update_date = None
        self.last_update_display = None
        self.registered_aop_pid = None
        self._previous_pid = None
        self.article_records = None
        self.is_ex_aop = False
        self.section_code = None
        self.normalized_affiliations = {}
        self.institutions_query_results = {}
        self._issue_pub_date = None
        self.xml = None if self.tree is None else xml_utils.node_xml(self.tree.find('.'))

    def count_words(self, word):
        return self.xml.count(word)

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
    def fpage_number(self):
        if self.fpage is not None:
            if self.fpage.isdigit():
                return int(self.fpage)

    @property
    def lpage_number(self):
        if self.lpage is not None:
            if self.lpage.isdigit():
                return int(self.lpage)

    @property
    def summary(self):
        data = {}
        data['journal-title'] = self.journal_title
        data['journal-id (publisher-id)'] = self.journal_id_publisher_id
        data['journal-id (nlm-ta)'] = self.journal_id_nlm_ta
        data['journal ISSN'] = ','.join([k + ':' + v for k, v in self.journal_issns.items() if v is not None]) if self.journal_issns is not None else None
        data['print ISSN'] = self.print_issn
        data['e-ISSN'] = self.e_issn
        data['publisher name'] = self.publisher_name
        data['issue label'] = self.issue_label
        data['issue pub date'] = self.issue_pub_dateiso[0:4] if self.issue_pub_dateiso is not None else None
        data['order'] = self.order
        data['doi'] = self.doi
        data['fpage-lpage-seq-elocation-id'] = '-'.join([str(item) for item in [self.fpage, self.lpage, self.fpage_seq, self.elocation_id]])
        data['lpage'] = self.lpage
        data['fpage'] = self.fpage
        data['elocation id'] = self.elocation_id
        data['license'] = None
        if len(self.article_licenses) > 0:
            data['license'] = list(self.article_licenses.values())[0]['href']
        return data

    @property
    def article_titles(self):
        titles = {}
        for title in self.titles:
            titles[title.language] = title.title
        return titles

    @property
    def textual_titles(self):
        return ' | '.join([self.article_titles.get(k) for k in sorted(self.article_titles.keys())])

    @property
    def textual_contrib_surnames(self):
        return ' | '.join([contrib.surname for contrib in self.contrib_names])

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
            if pid is not None:
                r = (len(pid) == 23) or (pid.isdigit() and 0 < int(pid) <= 99999)
            return r
        d = None
        if not self.is_ahead:
            if self.previous_article_pid is not None:
                if is_valid(self.previous_article_pid):
                    d = self.previous_article_pid
            if d is None:
                if self.registered_aop_pid is not None:
                    if is_valid(self.registered_aop_pid):
                        d = self.registered_aop_pid
            if d is None:
                d = ''
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
        if self._issue_pub_date is None:
            for d in [self.epub_ppub_date, self.collection_date, self.epub_date]:
                if d is not None:
                    self._issue_pub_date = d
                    break
        return self._issue_pub_date

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
    def pub_date(self):
        if self.epub_date is not None:
            return self.epub_date
        elif self.epub_ppub_date is not None:
            return self.epub_ppub_date
        elif self.collection_date is not None:
            return self.collection_date

    @property
    def pub_dateiso(self):
        return article_utils.format_dateiso(self.pub_date)

    @property
    def pub_date_year(self):
        pubdate = self.article_pub_date
        if pubdate is None:
            pubdate = self.issue_pub_date
        year = None
        if pubdate is not None:
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
        if self.received is not None and self.accepted is not None:
            return article_utils.days('received date', self.received_dateiso, 'accepted date', self.accepted_dateiso)

    @property
    def publication_days(self):
        d1 = self.accepted_dateiso
        d2 = self.article_pub_dateiso if self.article_pub_dateiso else self.issue_pub_dateiso
        if d1 is not None and d2 is not None:
            return article_utils.days('accepted date', d1, 'pub-date', d2)

    @property
    def registration_days(self):
        if self.accepted is not None:
            return article_utils.days('accepted date', self.accepted_dateiso, 'current date', datetime.now().isoformat())

    @property
    def expected_pdf_files(self):
        expected_files = {self.language: self.new_prefix + '.pdf'}
        expected_files.update(
            {lang: self.new_prefix + '-' + lang + '.pdf' for lang in self.trans_languages})
        return expected_files


class Reference(object):

    def __init__(self):
        self.source = None
        self.id = None
        self.language = None
        self.article_title = None
        self.chapter_title = None
        self.trans_title = None
        self.trans_title_language = None
        self.publication_type = None
        self.xml = None
        self.mixed_citation = None
        self.element_citation_texts = None
        self.contrib_xml_items = None
        self.person_group_xml_items = None
        self.volume = None
        self.issue = None
        self.supplement = None
        self.edition = None
        self.version = None
        self.year = None
        self.publisher_name = None
        self.publisher_loc = None
        self.fpage = None
        self.lpage = None
        self.page_range = None
        self.elocation_id = None
        self.size = None
        self.label = None
        self.cited_date = None
        self.ext_link = None
        self.degree = None
        self.comments = None
        self.notes = None
        self.contract_number = None
        self.doi = None
        self.pmid = None
        self.pmcid = None
        self.conference_name = None
        self.conference_location = None
        self.conference_date = None

    @property
    def formatted_year(self):
        return article_utils.four_digits_year(self.year)

    @property
    def fpage_number(self):
        if self.fpage is not None:
            if self.fpage.isdigit():
                return int(self.fpage)

    @property
    def lpage_number(self):
        if self.lpage is not None:
            if self.lpage.isdigit():
                return int(self.lpage)


class ReferenceXML(object):

    def __init__(self, root):
        self.root = root
        self.root_xml_node = xml_utils.XMLNode(root)
        self.elem_citation_nodes = self.root_xml_node.nodes(['.//element-citation'])
        self._pub_id_items = None
        self._doi = None
        self._ref = None
        self._person_group_xml_items = None
        self._contrib_xml_items = None
        self.source = self.root_xml_node.nodes_text(['.//source'])
        self.volume = self.root_xml_node.nodes_text(['.//volume'])
        self.issue = self.root_xml_node.nodes_text(['.//issue'])
        self.supplement = self.root_xml_node.nodes_text(['.//supplement'])
        self.edition = self.root_xml_node.nodes_text(['.//edition'])
        self.version = self.root_xml_node.nodes_text(['.//version'])
        self.year = self.root_xml_node.nodes_text(['.//year'])
        self.fpage = self.root_xml_node.nodes_text(['.//fpage'])
        self.lpage = self.root_xml_node.nodes_text(['.//lpage'])
        self.label = self.root_xml_node.nodes_text(['.//label'])
        self.article_title = self.root_xml_node.nodes_text(['.//article-title'])
        self.chapter_title = self.root_xml_node.nodes_text(['.//chapter-title'])
        self.trans_title = self.root_xml_node.nodes_text(['.//trans-title'])
        self.publisher_name = self.root_xml_node.nodes_text(['.//publisher-name'])
        self.publisher_loc = self.root_xml_node.nodes_text(['.//publisher-loc'])
        self.page_range = self.root_xml_node.nodes_text(['.//page-range'])
        self.elocation_id = self.root_xml_node.nodes_text(['.//elocation-id'])
        self.ext_link = self.root_xml_node.nodes_text(['.//ext-link'])
        self.comments = self.root_xml_node.nodes_text(['.//comment'])
        self.notes = self.root_xml_node.nodes_text(['.//notes'])
        self.contract_number = self.root_xml_node.nodes_text(['.//comment[@content-type="award-id"]'])
        self.conference_name = self.root_xml_node.nodes_text(['.//conf-name'])
        self.conference_location = self.root_xml_node.nodes_text(['.//conf-loc'])
        self.conference_date = self.root_xml_node.nodes_text(['.//conf-date'])

    @property
    def reference(self):
        if self._ref is None:
            self._ref = Reference()
            self._ref.xml = self.xml
            self._ref.id = self.id
            self._ref.language = self.language
            self._ref.trans_title_language = self.trans_title_language
            self._ref.contrib_xml_items = self.contrib_xml_items
            self._ref.person_group_xml_items = self.person_group_xml_items
            self._ref.page_range = self.page_range
            self._ref.doi = self.doi
            self._ref.pmid = self.pmid
            self._ref.pmcid = self.pmcid

            self._ref.source = first_item(self.source)
            self._ref.article_title = first_item(self.article_title)
            self._ref.chapter_title = first_item(self.chapter_title)
            self._ref.trans_title = first_item(self.trans_title)
            self._ref.publication_type = first_item(self.publication_type)
            self._ref.ref_status = first_item(self.ref_status)
            self._ref.mixed_citation = first_item(self.mixed_citation)
            self._ref.volume = first_item(self.volume)
            self._ref.issue = first_item(self.issue)
            self._ref.supplement = first_item(self.supplement)
            self._ref.edition = first_item(self.edition)
            self._ref.version = first_item(self.version)
            self._ref.year = first_item(self.year)
            self._ref.publisher_name = first_item(self.publisher_name)
            self._ref.publisher_loc = first_item(self.publisher_loc)
            self._ref.fpage = first_item(self.fpage)
            self._ref.lpage = first_item(self.lpage)
            self._ref.elocation_id = first_item(self.elocation_id)
            self._ref.size = first_item(self.size)
            self._ref.label = first_item(self.label)
            self._ref.cited_date = first_item(self.cited_date)
            self._ref.ext_link = first_item(self.ext_link)
            self._ref.degree = first_item(self.degree)
            self._ref.comments = first_item(self.comments)
            self._ref.notes = first_item(self.notes)
            self._ref.contract_number = first_item(self.contract_number)
            self._ref.conference_name = first_item(self.conference_name)
            self._ref.conference_location = first_item(self.conference_location)
            self._ref.conference_date = first_item(self.conference_date)
        return self._ref

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
    def trans_title_language(self):
        items = []
        for node in self.root_xml_node.nodes(['.//trans-title']):
            items.append(xml_utils.element_lang(node))
        return items

    @property
    def publication_type(self):
        if self.elem_citation_nodes is not None:
            return [item.get('publication-type') for item in self.elem_citation_nodes]

    @property
    def ref_status(self):
        if self.elem_citation_nodes is not None:
            return [item.get('specific-use') for item in self.elem_citation_nodes]

    @property
    def xml(self):
        return xml_utils.node_xml(self.root)

    @property
    def mixed_citation(self):
        return self.root_xml_node.nodes_text(['.//mixed-citation'])

    @property
    def element_citation(self):
        return self.root_xml_node.nodes_text(['.//element-citation'])

    @property
    def contrib_xml_items(self):
        if self._contrib_xml_items is None:
            r = []
            for items in self.person_group_xml_items:
                if items is not None:
                    r.extend(items[1])
            self._contrib_xml_items = r
        return self._contrib_xml_items

    @property
    def person_group_nodes(self):
        if not hasattr(self, '_person_group_nodes'):
            self._person_group_nodes = self.root_xml_node.nodes(['.//person-group'])
        return self._person_group_nodes

    @property
    def person_group_xml_items(self):
        if self._person_group_xml_items is None:
            groups = []
            if self.elem_citation_nodes is not None:
                for person_group in self.person_group_nodes:
                    role = person_group.attrib.get('person-group-type', 'author')
                    authors = []
                    etal = None
                    for contrib in person_group.findall('*'):
                        if contrib.tag == 'etal':
                            etal = 'et al'
                        else:
                            contrib_xml = ContribXML(contrib)
                            if contrib_xml.contrib() is not None:
                                authors.append(contrib_xml)
                    groups.append((role, authors, etal))
            self._person_group_xml_items = groups
        return self._person_group_xml_items

    @property
    def size(self):
        items = []
        for item in self.root_xml_node.nodes_data(['.//size']):
            if item is not None:
                text, attribs = item
                items.append({'size': text, 'units': attribs.get('units')})
        return items if len(items) > 0 else [None]

    @property
    def cited_date(self):
        return self.root_xml_node.nodes_text(
            [
                './/date-in-citation[@content-type="access-date"]',
                './/date-in-citation[@content-type="update"]'
            ])

    @property
    def degree(self):
        if self.publication_type == 'thesis':
            return self.comments

    @property
    def pub_id_items(self):
        if self._pub_id_items is None:
            data = self.root_xml_node.nodes_data(['.//pub-id'])
            if len(data) > 0:
                self._pub_id_items = {attribs.get('pub-id-type'): text for text, attribs in data}
        return self._pub_id_items

    @property
    def doi(self):
        if self._doi is None and self.pub_id_items is not None:
            self._doi = self.pub_id_items.get('doi')
            if self._doi is None:
                self._doi = [item for item in self.comments if 'doi' in item.lower()]
        return self._doi

    @property
    def pmid(self):
        if self.pub_id_items is not None:
            return self.pub_id_items.get('pmid')

    @property
    def pmcid(self):
        if self.pub_id_items is not None:
            return self.pub_id_items.get('pmcid')


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
        self.journal_issns = None

    @property
    def issue_label(self):
        return article_utils.format_issue_label(self.year, self.volume, self.number, self.volume_suppl, self.number_suppl, self.compl)

    @property
    def print_issn(self):
        if self.journal_issns is not None:
            return self.journal_issns.get('ppub')

    @property
    def e_issn(self):
        if self.journal_issns is not None:
            return self.journal_issns.get('epub')


class Journal(object):

    def __init__(self):
        self.collection_acron = None
        self.collection_name = None
        self.journal_title = None
        self.issn_id = None
        self.p_issn = None
        self.e_issn = None
        self.acron = None
        self.abbrev_title = None
        self.journal_title = None
        self.nlm_title = None
        self.publisher_name = None
        self.license = None


class ArticleXMLContent(object):

    def __init__(self, xml_content, name, new_name):
        self.xml_content = xml_content
        self.name = name
        self.new_name = new_name
        self.xml, self.xml_error = xml_utils.load_xml(self.xml_content)

    @property
    def doc(self):
        a = Article(self.xml, self.name)
        a.new_prefix = self.new_name
        return a


class ArticleFormula(object):

    def __init__(self, node):
        self.node = node
        self.tag = node.tag
        self.xml = xml_utils.node_xml(node)

    @property
    def id(self):
        if self.node is not None:
            return self.node.get('id')

    @property
    def codes(self):
        _codes = []
        if self.node is not None:
            _codes = codes(self.node)
        return _codes

    @property
    def graphics(self):
        _graphics = []
        if self.node is not None:
            _graphics = graphics(self.node)
        return _graphics


class ArticleTableWrap(object):

    def __init__(self, node):
        self.node = node
        self.tag = node.tag
        self.xml = xml_utils.node_xml(node)

    @property
    def id(self):
        if self.node is not None:
            return self.node.get('id')

    @property
    def codes(self):
        _codes = []
        if self.node is not None:
            for tag in ['table', 'alternative/table']:
                nodes = self.node.findall(tag)
                if nodes is not None:
                    _codes.extend([xml_utils.node_xml(item) for item in nodes])
        return _codes

    @property
    def graphics(self):
        _graphics = []
        if self.node is not None:
            for tag in ['alternative/graphic', 'graphic']:
                nodes = self.node.findall(tag)
                if nodes is not None:
                    for node in nodes:
                        href = node.get(
                                'href',
                                node.get('{http://www.w3.org/1999/xlink}href'))
                        _graphics.append(href)
        return _graphics


def codes(main_node):
    _codes = []
    if main_node is not None:
        for tag in ['alternatives']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                for item in nodes:
                    _codes.extend(codes(item))
        for tag in ['math', '{http://www.w3.org/1998/Math/MathML}math']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                _codes.extend([xml_utils.node_xml(item).replace('mml:', '') for item in nodes])
        for tag in ['tex-math']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                _codes.extend([xml_utils.node_text(item) for item in nodes])
    return _codes


def graphics(main_node):
    _graphics = []
    if main_node is not None:
        for tag in ['alternatives']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                for item in nodes:
                    _graphics.extend(graphics(item))
        for tag in ['inline-graphic', 'graphic']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                for node in nodes:
                    href = node.get(
                            'href',
                            node.get('{http://www.w3.org/1999/xlink}href'))
                    _graphics.append(href)
    return _graphics


def table(main_node):
    _table = []
    if main_node is not None:
        for tag in ['alternatives']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                for item in nodes:
                    _table.extend(table(item))
        for tag in ['table']:
            nodes = main_node.findall(tag)
            if nodes is not None:
                for node in nodes:
                    _table.append(xml_utils.node_xml(node))
    return _table
