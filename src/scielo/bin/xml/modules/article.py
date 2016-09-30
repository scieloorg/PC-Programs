# coding=utf-8
import os
from datetime import datetime

from __init__ import _

import article_utils
import xml_utils
import attributes
import utils
import ws_requester


IMG_EXTENSIONS = ['.tif', '.tiff', '.eps', '.gif', '.png', '.jpg', ]
REQUIRES_PERMISSIONS = [
        'boxed-text', 
        'disp-quote', 
        'fig', 
        'graphic', 
        'media', 
        'supplementary-material', 
        'table-wrap', 
        'verse-group', 
    ]


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
    r += '(xref: ' + ','.join([xref for xref in author.xref if xref is not None]) + ')'
    return r


def authors_list(authors):
    items = []
    for item in authors:
        if isinstance(item, PersonAuthor):
            if item.surname is not None and item.fname is not None:
                items.append(item.surname + ', ' + item.fname)
            elif item.surname is not None:
                items.append(item.surname + ', ')
            elif item.fname is not None:
                items.append(', ' + item.fname)
        else:
            items.append(item.collab)
    return items


def get_affiliation(aff):
    a = Affiliation()

    a.xml = xml_utils.node_xml(aff)
    a.id = aff.get('id')
    if aff.find('label') is not None:
        a.label = ' '.join(aff.find('label').itertext())
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
    return a


def get_author(contrib, role=None):
    c = None
    if contrib.find('name') is not None:
        c = PersonAuthor()
        c.fname = contrib.findtext('name/given-names')
        c.surname = contrib.findtext('name/surname')
        c.suffix = contrib.findtext('name/suffix')
        c.prefix = contrib.findtext('name/prefix')
        for contrib_id in contrib.findall('contrib-id[@contrib-id-type]'):
            c.contrib_id[contrib_id.attrib.get('contrib-id-type')] = contrib_id.text
        c.role = contrib.attrib.get('contrib-type')
        for xref_item in contrib.findall('xref[@ref-type="aff"]'):
            c.xref.append(xref_item.attrib.get('rid'))
    elif contrib.tag == 'name':
        c = PersonAuthor()
        c.fname = contrib.findtext('given-names')
        c.surname = contrib.findtext('surname')
        c.suffix = contrib.findtext('suffix')
        c.prefix = contrib.findtext('prefix')
        c.role = role
    elif contrib.find('collab') is not None:
        c = CorpAuthor()
        c.role = contrib.attrib.get('contrib-type')
        c.collab = contrib.findtext('collab')
    elif contrib.tag == 'collab':
        c = CorpAuthor()
        c.collab = contrib.text
    return c


def get_title(node, lang):
    t = Title()
    content = node.find('article-title')
    if content is None:
        content = node.find('trans-title')
    t.title = article_utils.remove_xref(xml_utils.node_text(content))

    content = node.find('article-subtitle')
    if content is None:
        content = node.find('trans-subtitle')
    t.subtitle = article_utils.remove_xref(xml_utils.node_text(content))
    t.language = lang
    return t


def items_by_lang(items):
    r = {}
    for item in items:
        if item is not None:
            if not item.language in r.keys():
                r[item.language] = []
            r[item.language].append(item)
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
        self.is_internal_file = (not '/' in src)
        if element.tag in ['ext-link', 'uri']:
            self.is_internal_file = False
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

    @property
    def name_without_extension(self):
        return self.src[0:self.src.rfind('.')] if '.' in self.src else self.src


class PersonAuthor(object):

    def __init__(self):
        self.fname = ''
        self.surname = ''
        self.suffix = ''
        self.prefix = ''
        self.contrib_id = {}
        self.role = ''
        self.xref = []

    @property
    def fullname(self):
        a = self.fname if self.fname is not None else ''
        a += ' ' + self.surname if self.surname is not None else ''
        return a


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

    def __init__(self, tree):
        self.tree = tree
        self.journal_meta = None
        self.article_meta = None
        self.body = None
        self.back = None
        self.translations = []
        self.sub_articles = []
        self.responses = []

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
                text = node_p.text
                if text is None:
                    text = xml_utils.node_text(node_p)
                if character in text:
                    text = text.split(character)[0]
                    if text.strip() == '':
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
            for sec in node.findall('sec'):
                _sections.append((sec.attrib.get('sec-type', ''), sec.findtext('title')))
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
                if not xref_type in _any_xref_ranges.keys():
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
                                if not None in [start, end]:
                                    _any_xref_ranges[xref_type].append([start, end, xref_node_items[k], xref_node_items[k+1]])
                        #else:
                        #    print(text)
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
                    if not xref_type in xref_nodes.keys():
                        xref_nodes[xref_type] = []
                    xref_nodes[xref_type].append(xref_node)

                    if not xref_type in _any_xref_parent_nodes.keys():
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
                            if not None in [start, end]:
                                _bibr_xref_ranges.append([start, end, bibr_xref_node_items[k-1], bibr_xref_node_items[k]])
                        #elif '-' in text:
                        #    print(text)
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
                if item['ext-link-type'] == 'scielo-pid':
                    item['ext-link-type'] = 'pid'
                item['id'] = rel.attrib.get('id')
                if not item['related-article-type'] in attributes.related_articles_type:
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
        r.append(self.toc_section)
        if self.translations is not None:
            for node in self.translations:
                nodes = node.findall('.//subj-group/subject')
                if nodes is not None:
                    for s in nodes:
                        r.append(s.text)
        return r

    @property
    def sorted_toc_sections(self):
        r = []
        r.append(self.toc_section)
        if self.translations is not None:
            for node in self.translations:
                nodes = node.findall('.//subj-group/subject')
                if nodes is not None:
                    for s in nodes:
                        r.append(s.text)
        return sorted(r)

    @property
    def normalized_toc_section(self):
        return attributes.normalized_toc_section(self.toc_section)

    @property
    def keywords_by_lang(self):
        k = {}
        for item in self.keywords:
            if not item['l'] in k.keys():
                k[item['l']] = []

            t = Text()
            t.language = item['l']
            t.text = item['k']

            k[item['l']].append(t)
        return k

    @property
    def article_keywords(self):
        k = []
        if not self.article_meta is None:
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
        for subartid, subarticlecontrib in self.subarticles_contrib_items.items():
            if isinstance(subarticlecontrib, PersonAuthor):
                items.append(subarticlecontrib)
        return items

    @property
    def article_contrib_items(self):
        k = []
        if self.article_meta is not None:
            for contrib in self.article_meta.findall('.//contrib'):
                a = get_author(contrib)
                if a is not None:
                    k.append(a)
        k = [item for item in k if item is not None]
        return k

    @property
    def subarticles_contrib_items(self):
        contribs = {}
        if self.sub_articles is not None:
            for subart in self.sub_articles:
                if subart.attrib.get('article-type') != 'translation':
                    contribs[subart.attrib.get('id')] = []
                    for contrib in subart.findall('.//contrib'):
                        a = get_author(contrib)
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
                a = get_author(contrib)
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
            for node in self.article_meta.findall('.//title-group'):
                t = Title()
                t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
                t.language = self.language
                k.append(t)
        return k

    @property
    def trans_title_group_titles(self):
        k = []
        if self.article_meta is not None:
            for node in self.article_meta.findall('.//trans-title-group'):
                t = Title()
                t.title = article_utils.remove_xref(xml_utils.node_text(node.find('trans-title')))
                t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('trans-subtitle')))
                t.language = xml_utils.element_lang(node)
                k.append(t)
        return k

    @property
    def translations_title_group_titles(self):
        k = []
        if self.translations is not None:
            for subart in self.translations:
                for node in subart.findall('*/title-group'):
                    t = Title()
                    t.title = article_utils.remove_xref(xml_utils.node_text(node.find('article-title')))
                    t.subtitle = article_utils.remove_xref(xml_utils.node_text(node.find('subtitle')))
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
        r = list(set(self.keywords_by_lang.keys() + self.abstracts_by_lang.keys() + self.titles_by_lang.keys()))
        return [item for item in r if item is not None]

    @property
    def trans_languages(self):
        k = []
        if self.translations is not None:
            for node in self.translations:
                k.append(xml_utils.element_lang(node))
        return k

    @property
    def doi(self):
        if self.article_meta is not None:
            _doi = self.article_meta.findtext('article-id[@pub-id-type="doi"]')
            if _doi is not None:
                return _doi.lower()

    @property
    def marked_to_delete(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('article-id[@specific-use="delete"]')

    @property
    def previous_article_pid(self):
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
                affs.append(get_affiliation(aff))
        if self.sub_articles is not None:
            for sub_art in self.sub_articles:
                if sub_art.attrib.get('article-type') != 'translation':
                    for aff in sub_art.findall('.//aff'):
                        affs.append(get_affiliation(aff))
        return affs

    @property
    def uri_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="ClinicalTrial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.article_meta is not None:
            node = self.article_meta.find('.//uri[@content-type="ClinicalTrial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def uri_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="ClinicalTrial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.article_meta is not None:
            node = self.article_meta.find('.//uri[@content-type="ClinicalTrial"]')
            if node is not None:
                return xml_utils.node_text(node)

    @property
    def ext_link_clinical_trial_href(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="ClinicalTrial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.article_meta is not None:
            node = self.article_meta.find('.//ext-link[@ext-link-type="ClinicalTrial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

    @property
    def ext_link_clinical_trial_text(self):
        #FIXME nao existe clinical-trial 
        #<ext-link ext-link-type="ClinicalTrial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</ext-link>
        if self.article_meta is not None:
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
    def disp_formula_elements(self):
        r = []
        if self.tree is not None:
            if self.tree.findall('.//disp-formula') is not None:
                r = self.tree.findall('.//disp-formula')
        return r

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
            pubtype = ref.publication_type
            if not ref.publication_type in _refstats.keys():
                if pubtype is None:
                    pubtype = 'None'
                _refstats[pubtype] = 0
            _refstats[pubtype] += 1
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
        if self.article_meta is not None:
            return xml_utils.date_element(self.article_meta.find('pub-date[@pub-type="epub-ppub"]'))

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
            _article_cpright['statement'] = xml_utils.node_text(self.article_meta.find('.//copyright-statement'))
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
                _article_licenses[lang]['text'] = xml_utils.node_text(license_node.find('.//license-p'))
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
        for tag in REQUIRES_PERMISSIONS:
            xpath = './/' + tag
            if tag == 'graphic':
                xpath = './/*[graphic]'

                for node in self.tree.findall(xpath):
                    if not node.tag in ['fig', 'table-wrap']:
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
                    href = elem.attrib.get('{http://www.w3.org/1999/xlink}href')
                    _href = HRef(href, elem, parent, xml_utils.node_xml(parent), self.prefix)
                    items.append(_href)
        return items

    @property
    def inline_graphics(self):
        return [item for item in self.hrefs if item.element.tag in ['inline-graphic', 'inline-formula']]

    @property
    def disp_formulas(self):
        return [item for item in self.hrefs if item.parent.tag == 'disp-formula']

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
                _table = Table(t.tag, t.attrib.get('id'), t.findtext('.//label'), xml_utils.node_text(t.find('.//caption')), _href, xml_utils.node_xml(t.find('./table')))
                r.append(_table)
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
        self.normalized_affiliations = None
        self.article_records = None
        self.related_files = []

    def package_files(self, pkg_path):
        files = [item for item in os.listdir(pkg_path) if item.startswith(self.new_prefix) and not item.endswith('.xml')]
        for hrefitem in self.href_files:
            file_location = hrefitem.file_location(pkg_path)
            if os.path.isfile(file_location):
                files.append(hrefitem.src)
        return list(set(files))

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
    def doi_data(self):
        return doi_data(self.doi)

    @property
    def doi_journal_titles(self):
        return self.doi_data.get('journal-titles')

    @property
    def doi_article_titles(self):
        return self.doi_data.get('article-titles')

    @property
    def doi_pid(self):
        return self.doi_data.get('pid')

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
            data['license'] = self.article_licenses.values()[0]['href']
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
            if not pid is None:
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

    @property
    def source(self):
        if self.element_citation is not None:
            return xml_utils.node_text(self.element_citation.find('.//source'))

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
        for grp in self.authors_by_group:
            for contrib in grp:
                r.append(contrib)

        return r

    @property
    def authors_by_group(self):
        groups = []
        if self.element_citation is not None:
            for person_group in self.element_citation.findall('.//person-group'):
                role = person_group.attrib.get('person-group-type', 'author')
                authors = [get_author(contrib, role) for contrib in person_group.findall('*')]
                authors = [a for a in authors if a is not None]

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
            items = []
            for item in self.element_citation.findall('.//ext-link'):
                if item is not None:
                    items.append(xml_utils.node_text(item).strip())
            return items

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


#FIXME
def doi_data(doi):
    results = {}
    url = ws_requester.wsr.article_doi_checker_url(doi)
    article_json = ws_requester.wsr.json_result_request(url)
    if article_json is not None:
        data = article_json.get('message')
        if data is not None:
            results = []
            for label in ['container-title', 'title', 'alternative-id']:
                result = data.get(label)
                if not result is None:
                    if not isinstance(result, list):
                        result = [result]
                results.append(result)
            if len(results) > 0:
                results = {'journal-titles': results[0], 'article-titles': results[1], 'pid': results[2][0] if results[2] is not None else None}
    return results
