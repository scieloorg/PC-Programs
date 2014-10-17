# coding=utf-8

import xml.etree.ElementTree as etree

from article_utils import doi_pid, format_date
from xml_utils import node_text, node_xml, element_lang


def format_issue_label(year, volume, number, volume_suppl, number_suppl):
    year = year if number == 'ahead' else ''
    v = 'v' + volume if volume is not None else None
    vs = 's' + volume_suppl if volume_suppl is not None else None
    n = 'n' + number if number is not None else None
    ns = 's' + number_suppl if number_suppl is not None else None
    return ''.join([i for i in [year, v, vs, n, ns] if i is not None])


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

    def __init__(self, src, element, parent, xml):
        self.src = src
        self.element = element
        self.xml = xml

        self.id = element.attrib.get('id', None)
        if self.id is None and parent is not None:
            self.id = parent.attrib.get('id', None)

        self.parent = parent
        self.isfile = (not element.tag == 'ext-link') and (not ':' in src) and (not '/' in src)

    def display(self, path):
        if self.src is not None and self.src != '':
            if ':' in self.src:
                return '<a href="' + self.src + '">' + self.src + '</a>'
            elif self.element.tag == 'graphic':
                return '<img src="' + path + '/' + self.src + '"/>'
            else:
                return '<a href="' + path + '/' + self.src + '">' + self.src + '</a>'
        else:
            return 'None'


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
        self._ahead_pid = None
        self.tree = tree
        self.journal_meta = None
        self.article_meta = None
        self.body = None
        self.back = None
        self.subarticles = []
        self.responses = []
        if tree is not None:
            self.journal_meta = self.tree.find('./front/journal-meta')
            self.article_meta = self.tree.find('./front/article-meta')
            self.body = self.tree.find('./body')
            self.back = self.tree.find('./back')
            self.subarticles = self.tree.findall('./sub-article')
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
        if self.subarticles is not None:
            for item in self.subarticles:
                for sec in self.sections(item.find('.//body'), 'sub-article/[@id="' + item.attrib.get('id', 'None') + '"]'):
                    r.append(sec)
        return r

    def fn_list(self, node, scope):
        r = []
        if node is not None:
            for fn in node.findall('.//fn'):
                r.append((scope, node_xml(fn)))
        return r

    @property
    def article_fn_list(self):
        r = self.fn_list(self.back, 'article')
        if self.subarticles is not None:
            for item in self.subarticles:
                scope = 'sub-article/[@id="' + item.attrib.get('id', 'None') + '"]'
                for fn in self.fn_list(item.find('.//back'), scope):
                    r.append(fn)
        return r

    @property
    def xref_list(self):
        _xref_list = {}
        if self.tree is not None:
            for xref in self.tree.findall('.//xref'):
                rid = xref.attrib.get('rid')
                if not rid in _xref_list.keys():
                    _xref_list[rid] = []
                _xref_list[rid].append(node_xml(xref))
        return _xref_list

    @property
    def dtd_version(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('dtd-version')

    @property
    def article_type(self):
        if self.tree is not None:
            if self.tree.find('.') is not None:
                return self.tree.find('.').attrib.get('article-type')

    @property
    def language(self):
        if self.tree is not None:
            return element_lang(self.tree.find('.'))

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
        if self.article_meta is not None:
            related = self.article_meta.findall('related-article')
            for rel in related:
                item = {}
                item['href'] = item.attrib.get('{http://www.w3.org/1999/xlink}href')
                item['ext-link-type'] = item.attrib.get('ext-link-type')
                if not item['ext-link-type'] == 'doi':
                    item['id'] = ''.join([c for c in item['href'] if c.isdigit()])
                item['related-article-type'] = item.attrib.get('related-article-type')
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
        node = self.article_meta.find('.//subj-group[@subj-group-type="heading"]')
        if node is not None:
            r = node.findtext('subject')
        return r

    @property
    def keywords(self):
        k = []
        if not self.article_meta is None:
            for node in self.article_meta.findall('kwd-group'):
                language = element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': node_text(kw)})
        for subart in self.subarticles:
            for node in subart.findall('kwd-group'):
                language = element_lang(node)
                for kw in node.findall('kwd'):
                    k.append({'l': language, 'k': node_text(kw)})
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
                t.title = node_text(node.find('article-title'))
                t.subtitle = node_text(node.find('subtitle'))
                t.language = self.language
                k.append(t)
            for node in self.article_meta.findall('.//trans-title-group'):
                t = Title()
                t.title = node_text(node.find('trans-title'))
                t.subtitle = node_text(node.find('trans-subtitle'))
                t.language = element_lang(node)
                k.append(t)
        if self.subarticles is not None:
            for subart in self.subarticles:
                if subart.attrib.get('article-type') == 'translation':
                    for node in subart.findall('.//title-group'):
                        t = Title()
                        t.title = node_text(node.find('article-title'))
                        t.subtitle = node_text(node.find('subtitle'))
                        t.language = element_lang(subart)
                        k.append(t)
        return k

    @property
    def trans_languages(self):
        k = []
        if self.subarticles is not None:
            for node in self.subarticles:
                k.append(element_lang(node))
        return k

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
        v = self.article_meta.findtext('volume')
        if v is not None:
            v = str(int(v))
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
            return node_xml(self.back.find('.//ack'))

    @property
    def financial_disclosure(self):
        if self.tree is not None:
            return node_text(self.tree.find('.//fn[@fn-type="financial-disclosure"]'))

    @property
    def fn_financial_disclosure(self):
        if self.tree is not None:
            return node_xml(self.tree.find('.//fn[@fn-type="financial-disclosure"]'))

    @property
    def fpage(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('fpage')

    @property
    def fpage_seq(self):
        if self.article_meta is not None:
            return self.article_meta.find('fpage').attrib.get('seq') if self.article_meta.find('fpage') is not None else None

    @property
    def lpage(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('lpage')

    @property
    def elocation_id(self):
        if self.article_meta is not None:
            return self.article_meta.findtext('elocation-id')

    @property
    def affiliations(self):
        affs = []
        for aff in self.article_meta.findall('.//aff'):
            a = Affiliation()

            a.xml = node_xml(aff)
            a.id = aff.get('id')
            a.label = aff.findtext('label')
            a.country = aff.findtext('country')
            a.email = aff.findtext('email')
            a.original = aff.findtext('institution[@content-type="original"]')
            a.norgname = aff.findtext('institution[@content-type="normalized"]')
            a.orgname = aff.findtext('institution[@content-type="orgname"]')
            a.orgdiv1 = aff.findtext('institution[@content-type="orgdiv1"]')
            a.orgdiv2 = aff.findtext('institution[@content-type="orgdiv2"]')
            a.orgdiv3 = aff.findtext('institution[@content-type="orgdiv3"]')
            a.city = aff.findtext('addr-line/named-content[@content-type="city"]')
            a.state = aff.findtext('addr-line/named-content[@content-type="state"]')

            affs.append(a)

        return affs

    @property
    def clinical_trial_url(self):
        #FIXME nao existe clinical-trial 
        #<uri content-type="clinical-trial" xlink:href="http://www.ensaiosclinicos.gov.br/rg/RBR-7bqxm2/">The study was registered in the Brazilian Clinical Trials Registry (RBR-7bqxm2)</uri>
        if self.tree is not None:
            node = self.tree.find('.//uri[@content-type="clinical-trial"]')
            if node is not None:
                return node.attrib.get('{http://www.w3.org/1999/xlink}href')

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
        if self.tree.findall('.//disp-formula') is not None:
            for item in self.tree.findall('.//disp-formula'):
                r.append(node_xml(item))
        if self.tree.findall('.//inline-formula') is not None:
            for item in self.tree.findall('.//inline-formula'):
                r.append(node_xml(item))
        return r

    @property
    def abstracts(self):
        r = []
        if self.article_meta is not None:
            for a in self.article_meta.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = self.language
                _abstract.text = node_text(a)
                r.append(_abstract)
            for a in self.article_meta.findall('.//trans-abstract'):
                _abstract = Text()
                _abstract.language = element_lang(a)
                _abstract.text = node_text(a)
                r.append(_abstract)
        for subart in self.subarticles:
            subart_lang = element_lang(subart)
            for a in subart.findall('.//abstract'):
                _abstract = Text()
                _abstract.language = subart_lang
                _abstract.text = node_text(a)
                r.append(_abstract)
            for a in subart.findall('.//trans-abstract'):
                _abstract = Text()
                _abstract.language = element_lang(a)
                _abstract.text = node_text(a)
                r.append(_abstract)
        return r

    @property
    def received(self):
        item = self.article_meta.find('.//date[@date-type="received"]')
        _hist = None
        if item is not None:
            _hist = {}
            for tag in ['year', 'month', 'day', 'season']:
                _hist[tag] = item.findtext(tag)
        return _hist

    @property
    def accepted(self):
        item = self.article_meta.find('.//date[@date-type="accepted"]')
        _hist = None
        if item is not None:
            _hist = {}
            for tag in ['year', 'month', 'day', 'season']:
                _hist[tag] = item.findtext(tag)
        return _hist

    @property
    def references(self):
        refs = []
        if self.back is not None:
            for ref in self.back.findall('.//ref'):
                refs.append(ReferenceXML(ref))
        return refs

    @property
    def press_release_id(self):
        for related in self.related_articles:


    @property
    def issue_pub_date(self):
        _issue_pub_date = None
        if self.article_meta is not None:
            date = self.article_meta.find('pub-date[@date-type="pub"]')
            if date is None:
                date = self.article_meta.find('pub-date[@pub-type="epub-ppub"]')
            if date is None:
                date = self.article_meta.find('pub-date[@pub-type="ppub"]')
            if date is None:
                date = self.article_meta.find('pub-date[@pub-type="collection"]')
            if date is None:
                date = self.article_meta.find('pub-date[@pub-type="epub"]')
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
        date = None
        if self.article_meta is not None:
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
    def is_article_press_release(self):
        r = False
        for related in self.related_articles:
            if related['related-article-type'] == 'article-reference':
                r = True
                break
            if related['related-article-type'] == 'article':
                r = True
                break
        return r

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
                r = node_text(node)
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
                    _href = HRef(href, elem, parent, node_xml(parent))
                    r.append(_href)
        return r

    @property
    def elements_which_has_id_attribute(self):
        return self.tree.findall('.//*[@id]')

    @property
    def href_files(self):
        return [href for href in self.hrefs if href.isfile]

    @property
    def tables(self):
        r = []
        if self.tree is not None:
            for t in self.tree.findall('.//*[table]'):
                graphic = t.find('./graphic')
                _href = None
                if graphic is not None:
                    src = graphic.attrib.get('{http://www.w3.org/1999/xlink}href')
                    xml = node_xml(graphic)

                    _href = HRef(src, graphic, t, xml)
                _table = Table(t.tag, t.attrib.get('id'), t.findtext('.//label'), node_text(t.find('.//caption')), _href, node_xml(t.find('./table')))
                r.append(_table)
        return r


class Article(ArticleXML):

    def __init__(self, tree):
        ArticleXML.__init__(self, tree)
        if self.tree is not None:
            self._issue_parts()

    def summary(self):
        data = {}
        data['journal-title'] = self.journal_title
        data['journal id NLM'] = self.journal_id_nlm_ta
        data['journal ISSN'] = ' '.join(self.journal_issns.values()) if self.journal_issns is not None else None
        data['publisher name'] = self.publisher_name
        data['issue label'] = self.issue_label
        data['issue pub date'] = format_date(self.issue_pub_date)
        data['order'] = self.order
        data['doi'] = self.doi
        seq = '' if self.fpage_seq is None else self.fpage_seq
        fpage = '' if self.fpage is None else self.fpage
        data['fpage-and-seq'] = fpage + seq
        data['elocation id'] = self.elocation_id
        return data

    @property
    def article_titles(self):
        titles = {}
        for title in self.titles:
            titles[title.language] = title.title
        return titles

    def _issue_parts(self):
        self.number = None
        self.number_suppl = None
        self.volume_suppl = None
        self.compl = None
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
                elif 'sup' in parts[1].lower():
                    self.number, suppl = parts
                else:
                    self.number, self.compl = parts
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
            if self.number == '0':
                self.number = None

        if self.volume is None and self.number is None:
            self.number = 'ahead'

    @property
    def is_issue_press_release(self):
        return self.compl == 'pr'

    @property
    def is_ahead(self):
        return (self.volume is None) and (self.number == 'ahead')

    @property
    def ahpdate(self):
        return self.article_pub_date if self.is_ahead else None

    @property
    def is_text(self):
        return len(self.keywords) == 0

    @property
    def previous_pid(self):
        def is_valid(pid):
            r = False
            if not d is None:
                r = (len(d) == 23)
            return r

        d = self.article_previous_id
        if not is_valid(d):
            if self.doi is not None:
                d = doi_pid(self.doi)
        if not is_valid(d):
            d = self._ahead_pid
        if not is_valid(d):
            d = self.article_id_other
        if not is_valid(d):
            d = None
        return d

    @property
    def issue_label(self):
        return format_issue_label(self.issue_pub_date.get('year', ''), self.volume, self.number, self.volume_suppl, self.number_suppl)


class ReferenceXML(object):

    def __init__(self, root):
        self.root = root

    @property
    def element_citation(self):
        return self.root.find('.//element-citation')

    @property
    def source(self):
        return node_text(self.root.find('.//source'))

    @property
    def id(self):
        return self.root.find('.').attrib.get('id')

    @property
    def language(self):
        lang = None
        for elem in ['.//source', './/article-title', './/chapter-title']:
            if self.root.find(elem) is not None:
                lang = element_lang(self.root.find(elem))
            if lang is not None:
                break
        return lang

    @property
    def article_title(self):
        if self.root is not None:
            return node_text(self.root.find('.//article-title'))

    @property
    def chapter_title(self):
        if self.root is not None:
            return node_text(self.root.find('.//chapter-title'))

    @property
    def trans_title(self):
        if self.root is not None:
            return node_text(self.root.find('.//trans-title'))

    @property
    def trans_title_language(self):
        if self.root is not None:
            if self.root.find('.//trans-title') is not None:
                return element_lang(self.root.find('.//trans-title'))

    @property
    def publication_type(self):
        if self.root.find('.//element-citation') is not None:
            return self.root.find('.//element-citation').attrib.get('publication-type')

    @property
    def xml(self):
        return node_xml(self.root)

    @property
    def mixed_citation(self):
        return node_text(self.root.find('.//mixed-citation'))

    @property
    def authors_list(self):
        r = []

        for person_group in self.root.findall('.//person-group'):
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
                c.collab = node_text(collab)
                c.role = person_group_id
                r.append(c)
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
    def _comments(self):
        return self.root.findall('.//comment')

    @property
    def comments(self):
        c = [c.text for c in self._comments]
        return '; '.join(c)

    @property
    def notes(self):
        return self.root.findtext('.//notes')

    @property
    def contract_number(self):
        return self.root.findtext('.//comment[@content-type="award-id"]')

    @property
    def doi(self):
        _doi = self.root.findtext('.//pub-id[@pub-id-type="doi"]')
        if not _doi:
            for c in self._comments:
                if 'doi:' in c.text:
                    _doi = c.text
        return _doi

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


class Issue(object):

    def __init__(self, acron, volume, number, year, volume_suppl, number_suppl):
        self.volume = volume
        self.number = number
        self.year = year
        self.volume_suppl = volume_suppl
        self.number_suppl = number_suppl
        self.acron = acron

    @property
    def issue_label(self):
        return format_issue_label(self.year, self.volume, self.number, self.volume_suppl, self.number_suppl)
