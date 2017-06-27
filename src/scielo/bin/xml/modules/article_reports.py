# coding=utf-8
import os
from datetime import datetime

from __init__ import _
import validation_status
import xml_utils
import article_utils
import attributes
import html_reports
from article import PersonAuthor, CorpAuthor, format_author
import utils


log_items = []


def register_log(text):
    log_items.append(datetime.now().isoformat() + ' ' + text)


def display_author(author):
    text = ''
    if isinstance(author, PersonAuthor):
        if author.surname is not None:
            text += html_reports.tag('span', author.surname, 'surname')

        if author.suffix is not None:
            text += ' ' + html_reports.tag('span', author.suffix, 'suffix')

        if author.fname is not None:
            text += ', ' + html_reports.tag('span', author.fname, 'name')
    else:
        text += html_reports.tag('span', author.collab, 'collab')
    return text


def display_authors(authors_list, sep):
    return sep.join([display_author(item) for item in authors_list])


class ArticleDisplayReport(object):

    def __init__(self, article_validation, xml_path, xml_name):
        self.article = article_validation.article
        self.article_validation = article_validation
        self.xml_name = article_validation.article.prefix
        self.xml_path = xml_path

    @property
    def article_front(self):
        r = _('{xml_name} is an invalid XML file').format(xml_name=self.xml_name)
        if self.article.tree is not None:
            r = ''
            r += self.sps
            r += self.language
            r += self.toc_section
            r += self.article_type
            r += self.display_titles()
            r += self.article_id
            r += self.article_id_other
            r += self.previous_article_pid
            r += self.order
            r += self.fpage
            r += self.fpage_seq
            r += self.elocation_id
            r += self.article_dates
            r += self.contrib_names
            r += self.contrib_collabs
            r += self.affiliations
            r += self.abstracts
            r += self.keywords

        return html_reports.tag('h2', 'article/front') + html_reports.tag('div', r, 'article-data')

    @property
    def article_body(self):
        r = ''
        r += self.sections
        #r += self.formulas
        r += self.tables
        return html_reports.tag('h2', 'article/body') + html_reports.tag('div', r, 'article-data')

    @property
    def article_back(self):
        r = ''
        r += self.funding
        r += self.footnotes
        return html_reports.tag('h2', 'article/back') + html_reports.tag('div', r, 'article-data')

    @property
    def authors_sheet(self):
        labels, width, data = self.authors_sheet_data()
        return html_reports.tag('h2', _('Authors')) + html_reports.sheet(labels, data)

    @property
    def sources_sheet(self):
        labels, width, data = self.sources_sheet_data()
        return html_reports.tag('h2', _('Sources')) + html_reports.sheet(labels, data)

    def display_labeled_value(self, label, value, style=''):
        return html_reports.display_labeled_value(label, value, style)

    def display_titles(self):
        r = ''
        for title in self.article.titles:
            r += html_reports.display_labeled_value(title.language, title.title)
        return r

    def display_text(self, label, items):
        r = html_reports.tag('p', label, 'label')
        for item in items:
            r += self.display_labeled_value(item.language, item.text)
        return html_reports.tag('div', r)

    @property
    def language(self):
        return self.display_labeled_value('@xml:lang', self.article.language)

    @property
    def sps(self):
        return self.display_labeled_value('@specific-use', self.article.sps)

    @property
    def toc_section(self):
        return self.display_labeled_value('subject', self.article.toc_section, 'toc-section')

    @property
    def article_type(self):
        return self.display_labeled_value('@article-type', self.article.article_type, 'article-type')

    @property
    def article_dates(self):
        return self.display_labeled_value('date(epub-ppub)', article_utils.format_date(self.article.epub_ppub_date)) + self.display_labeled_value('date(epub)', article_utils.format_date(self.article.epub_date)) + self.display_labeled_value('date(collection)', article_utils.format_date(self.article.collection_date))

    @property
    def contrib_names(self):
        return html_reports.format_list('authors:', 'ol', [format_author(a) for a in self.article.contrib_names])

    @property
    def contrib_collabs(self):
        r = [a.collab for a in self.article.contrib_collabs]
        if len(r) > 0:
            r = html_reports.format_list('collabs', 'ul', r)
        else:
            r = self.display_labeled_value('collabs', 'None')
        return r

    @property
    def abstracts(self):
        return self.display_text('abstracts', self.article.abstracts)

    @property
    def keywords(self):
        return html_reports.format_list('keywords:', 'ol', ['(' + k['l'] + ') ' + k['k'] for k in self.article.keywords])

    @property
    def order(self):
        return self.display_labeled_value('order', self.article.order, 'order')

    @property
    def article_id(self):
        if self.article.doi is not None:
            return self.display_labeled_value('doi', self.article.doi, 'doi')
        if self.article.publisher_article_id is not None:
            return self.display_labeled_value('article-id (publisher)', self.article.publisher_article_id, 'doi')

    @property
    def fpage(self):
        r = self.display_labeled_value('fpage', self.article.fpage, 'fpage')
        r += self.display_labeled_value('lpage', self.article.lpage, 'lpage')
        return r

    @property
    def fpage_seq(self):
        return self.display_labeled_value('fpage/@seq', self.article.fpage_seq, 'fpage')

    @property
    def elocation_id(self):
        return self.display_labeled_value('elocation-id', self.article.elocation_id, 'fpage')

    @property
    def funding(self):
        r = self.display_labeled_value('ack', self.article.ack_xml)
        r += self.display_labeled_value('fn[@fn-type="financial-disclosure"]', self.article.financial_disclosure, 'fpage')
        return r

    @property
    def article_id_other(self):
        return self.display_labeled_value('article-id[@pub-id-type="other"]', self.article.article_id_other)

    @property
    def previous_article_pid(self):
        return self.display_labeled_value('previous article id', self.article.previous_article_pid)

    @property
    def sections(self):
        _sections = []
        for item in self.article.article_sections:
            for label, sections in item.items():
                type_and_title_items = [sectitle + ' (' + sectype + ')' for sectype, sectitle in sections]
            _sections.append([label, type_and_title_items])
        return html_reports.format_list('sections:', 'ul', _sections)

    @property
    def formulas(self):
        r = html_reports.tag('p', 'disp-formulas:', 'label')
        for item in self.article.formulas:
            r += html_reports.tag('p', item, 'code')
        return r

    @property
    def footnotes(self):
        r = ''
        for item in self.article.article_fn_list:
            scope, fn_xml = item
            r += html_reports.tag('p', scope, 'label')
            r += html_reports.tag('p', fn_xml)
        if len(r) > 0:
            r = html_reports.tag('p', 'foot notes:', 'label') + r
        return r

    @property
    def issue_header(self):
        if self.article.tree is not None:
            r = [self.article.journal_title, self.article.journal_id_nlm_ta, self.article.issue_label, article_utils.format_date(self.article.issue_pub_date)]
            return html_reports.tag('div', '\n'.join([html_reports.tag('h5', item) for item in r if item is not None]), 'issue-data')
        else:
            return ''

    @property
    def tables(self):
        r = '<!-- no tables -->'
        if len(self.article.tables) > 0:
            r = html_reports.tag('p', 'Tables:', 'label')

            for t in self.article.tables:
                #print(t)
                header = html_reports.tag('h3', t.id)
                table_data = ''
                table_data += html_reports.display_labeled_value('label', t.label, 'label')
                table_data += html_reports.display_labeled_value('caption',  t.caption, 'label')
                table_data += html_reports.tag('p', 'table-wrap/table (xml)', 'label')
                table_data += html_reports.tag('div', html_reports.format_html_data(t.table), 'xml')
                if t.table:
                    table_data += html_reports.tag('p', 'table-wrap/table', 'label')
                    table_data += html_reports.tag('div', t.table, 'element-table')
                if t.graphic:
                    #table_data += html_reports.display_labeled_value('table-wrap/graphic', t.graphic.display('file:///' + self.xml_path), 'value')
                    table_data += html_reports.display_labeled_value('table-wrap/graphic', html_reports.thumb_image('{IMG_PATH}'), 'value')
                r += header + html_reports.tag('div', table_data, 'block')
        return r

    @property
    def table_tables(self):
        r = '<!-- no tables -->'
        if len(self.article.tables) > 0:
            r = html_reports.tag('p', 'Tables:', 'label')
            for t in self.article.tables:
                if t.table:
                    table_data = ''
                    table_data += html_reports.display_labeled_value('label', t.label, 'label')
                    table_data += html_reports.tag('div', t.table, 'element-table')
                    r += html_reports.tag('div', table_data, 'block')
        return r

    @property
    def display_formulas(self):
        labels = ['id', 'code', 'graphic', 'xml']
        formulas_data = []
        for formula_data in self.article.formulas_data:
            if formula_data['graphic'] is not None:
                formula_data['graphic'] = html_reports.link('{IMG_PATH}/' + formula_data['graphic'], html_reports.thumb_image('{IMG_PATH}/' + formula_data['graphic']))
            if formula_data['code'] is not None:
                formula_data['code'] = formula_data['code'].replace('mml:', '')
            formulas_data.append(formula_data)
        return html_reports.tag('h1', _('Equations')) + html_reports.sheet(labels, formulas_data, html_cell_content=['code'])

    @property
    def affiliations(self):
        r = html_reports.tag('p', 'Affiliations:', 'label')
        for item in self.article.affiliations:
            r += html_reports.tag('p', html_reports.format_html_data(item.xml))
        th, w, data = self.affiliations_sheet_data()
        r += html_reports.sheet(th, data)
        return r

    @property
    def id_and_xml_list(self):
        sheet_data = []
        t_header = ['@id', 'xml']
        for item in self.article.elements_which_has_id_attribute:
            row = {}
            row['@id'] = item.attrib.get('id')
            row['xml'] = xml_utils.node_xml(item)
            if '>' in row['xml']:
                row['xml'] = row['xml'][0:row['xml'].find('>')+1]
            sheet_data.append(row)
        r = html_reports.tag('h2', 'elements and @id:')
        r += html_reports.sheet(t_header, sheet_data)
        return r

    @property
    def id_and_tag_list(self):
        sheet_data = []
        t_header = ['@id', 'tag']
        for item in self.article.elements_which_has_id_attribute:
            row = {}
            row['@id'] = item.attrib.get('id')
            row['tag'] = item.tag
            sheet_data.append(row)
        r = html_reports.tag('h2', 'elements and @id:')
        r += html_reports.sheet(t_header, sheet_data)
        return r

    @property
    def references_stats(self):
        r = html_reports.tag('h2', 'references')
        sheet_data = []
        for ref_type, q in self.article.refstats.items():
            row = {}
            row['element-citation/@publication-type'] = ref_type
            row['quantity'] = q
            sheet_data.append(row)
        r += html_reports.sheet(['element-citation/@publication-type', 'quantity'], sheet_data)
        return r

    def authors_sheet_data(self):
        r = []
        t_header = ['xref', 'publication-type', 'role', 'given-names', 'surname', 'suffix', 'prefix', 'collab']
        if not self.xml_name is None:
            t_header = ['filename', 'scope'] + t_header
        for a in self.article.contrib_names:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = self.xml_name
            row['xref'] = ' '.join(a.xref)
            row['role'] = a.role
            row['publication-type'] = self.article.article_type
            row['given-names'] = a.fname
            row['surname'] = a.surname
            row['suffix'] = a.suffix
            row['prefix'] = a.prefix
            r.append(row)

        for a in self.article.contrib_collabs:
            row = {}
            row['scope'] = 'article meta'
            row['filename'] = self.xml_name
            row['publication-type'] = self.article.article_type
            row['collab'] = a.collab
            row['role'] = a.role
            r.append(row)

        for ref in self.article.references:
            for item in ref.authors_list:
                row = {}
                row['scope'] = ref.id
                row['filename'] = self.xml_name
                row['publication-type'] = ref.publication_type

                if isinstance(item, PersonAuthor):
                    row['given-names'] = item.fname
                    row['surname'] = item.surname
                    row['suffix'] = item.suffix
                    row['prefix'] = item.prefix
                    row['role'] = item.role
                elif isinstance(item, CorpAuthor):
                    row['collab'] = item.collab
                    row['role'] = item.role
                else:
                    row['given-names'] = '?'
                    row['surname'] = '?'
                    row['suffix'] = '?'
                    row['prefix'] = '?'
                    row['role'] = '?'
                r.append(row)
        return (t_header, [], r)

    def sources_sheet_data(self):
        r = []
        t_header = ['ID', 'type', 'year', 'source', 'publisher name', 'location', ]
        if not self.xml_name is None:
            t_header = ['filename', 'scope'] + t_header

        for ref in self.article.references:
            row = {}
            row['scope'] = ref.id
            row['ID'] = ref.id
            row['filename'] = self.xml_name
            row['type'] = ref.publication_type
            row['year'] = ref.year
            row['source'] = ref.source
            row['publisher name'] = ref.publisher_name
            row['location'] = ref.publisher_loc
            r.append(row)
        return (t_header, [], r)

    def tables_sheet_data(self):
        t_header = ['ID', 'label/caption', 'table/graphic']
        r = []
        for t in self.article.tables:
            row = {}
            row['ID'] = t.graphic_parent.id
            row['label/caption'] = t.graphic_parent.label + '/' + t.graphic_parent.caption
            row['table/graphic'] = t.table + html_reports.thumb_image('{IMG_PATH}')
            r.append(row)
        return (t_header, ['label/caption', 'table/graphic'], r)

    def files_and_href(self):
        r = ''
        r += html_reports.tag('h4', _('Files in the package'))
        th, data = self.package_files()
        r += html_reports.sheet(th, data, table_style='validation_sheet')
        r += html_reports.tag('h4', '@href')
        th, data = self.hrefs_sheet_data()
        r += html_reports.sheet(th, data, table_style='validation_sheet')
        return r

    def hrefs_sheet_data(self):
        t_header = ['label', 'status', 'message', _('why it is not a valid message?'), 'display', 'xml']
        r = []
        href_items = self.article_validation.href_list(self.xml_path)
        for src in sorted(href_items.keys()):
            hrefitem = href_items.get(src)
            for result in hrefitem['results']:
                row = {}
                row['label'] = src
                row['xml'] = hrefitem['elem'].xml
                row['display'] = hrefitem['display']
                row['status'] = result[0]
                row['message'] = result[1]
                row[_('why it is not a valid message?')] = ''
                r.append(row)
        return (t_header, r)

    def package_files(self):
        r = []
        t_header = ['label', 'status', 'message', _('why it is not a valid message?')]
        items = self.article_validation.package_files(self.xml_path) + self.article_validation.svg(self.xml_path)

        if len(items) > 0:
            for filename, status, message in items:
                row = {}
                row['label'] = filename
                row['status'] = status
                row['message'] = message
                row[_('why it is not a valid message?')] = ''
                r.append(row)
        return (t_header, r)

    def affiliations_sheet_data(self):
        t_header = ['aff id', 'aff orgname', 'aff norgname', 'aff orgdiv1', 'aff orgdiv2', 'aff country', 'aff city', 'aff state', ]
        r = []
        for a in self.article.affiliations:
            row = {}
            row['aff id'] = a.id
            row['aff norgname'] = a.norgname
            row['aff orgname'] = a.orgname
            row['aff orgdiv1'] = a.orgdiv1
            row['aff orgdiv2'] = a.orgdiv2
            row['aff city'] = a.city
            row['aff state'] = a.state
            row['aff country'] = a.country
            r.append(row)
        return (t_header, ['aff xml'], r)

    @property
    def table_of_contents_data(self):
        return display_article_data_in_toc(self.article)

    @property
    def table_of_contents(self):
        r = ''
        r += '<div>'
        #r += html_reports.tag('h7', self.work_area.xml_name)
        r += self.table_of_contents_data
        r += self.link_to_pdf_and_xml_files()
        r += '</div>'
        return r

    @property
    def table_of_contents_detailed(self):
        r = ''
        r += '<div>'
        r += self.table_of_contents_data
        r += self.table_of_contents_data_with_lang
        r += self.link_to_pdf_and_xml_files()
        r += '</div>'
        return r

    @property
    def table_of_contents_data_with_lang(self):
        r = ''
        for lang in sorted(self.article.title_abstract_kwd_languages):
            label = html_reports.tag('smaller', attributes.LANGUAGES.get(lang, _('unknown')) + ' [' + lang + ']')
            r += '<h4>' + label + '</h4>'
            r += '<p>' + '; '.join([k.text for k in self.article.abstracts_by_lang.get(lang, [])]) + '</p>'
            r += html_reports.tag('h5', '; '.join([k.text for k in self.article.keywords_by_lang.get(lang, [])]))
        return r

    def embedded_pdf_items(self, page_id='', width='400px', height='400px'):
        items = []
        for item in self.article.related_files:
            items.append(html_reports.tag('p', html_reports.display_embedded_object(
                item,
                os.path.basename(item), page_id + item, width, height)))
        return ''.join(items)

    def link_to_pdf_and_xml_files(self):
        items = []
        for item in self.article.related_files + [self.article.filename]:
            location = '{PDF_PATH}' if item.endswith('.pdf') else '{XML_PATH}'
            items.append(html_reports.tag('p', html_reports.link(
                location + item,
                item, window=('1000', '400'))))
        return ''.join(items)


class ArticleValidationReport(object):

    def __init__(self, article_validation):
        self.article_validation = article_validation

    def display_items(self, items):
        r = ''
        for item in items:
            r += self.display_item(item)
        return r

    def display_item(self, item):
        return html_reports.p_message(item, False)

    def validations(self, display_all_message_types):
        items, performance = self.article_validation.validations
        items = [item for item in items if item is not None]
        new_items = []
        for item in items:
            xml = ''
            if len(item) == 3:
                label, status, msg = item
            elif len(item) == 4:
                label, status, msg, xml = item
            if display_all_message_types:
                new_items.append((label, status, msg, xml))
            elif status != validation_status.STATUS_OK:
                new_items.append((label, status, msg, xml))
        items = new_items

        r = validations_table(items)

        r += self.references(display_all_message_types)

        if len(r) > 0:
            r = html_reports.tag('div', r, 'article-messages')

        return r

    def references(self, display_all):
        rows = ''
        found_errors = []
        for ref, ref_result in self.article_validation.references:
            if not display_all:
                found_errors = [res[1] for res in ref_result if res[1] in [validation_status.STATUS_WARNING, validation_status.STATUS_ERROR, validation_status.STATUS_FATAL_ERROR]]
                ref_result = [res for res in ref_result if res[1] != validation_status.STATUS_OK]

            if len(found_errors) > 0:
                rows += html_reports.tag('h3', _('Reference {id}').format(id=ref.id))
                rows += validations_table(ref_result)
        return rows


def validations_table(results):
    r = ''
    if results is not None:
        rows = []
        for result in results:
            result = list(result)
            if len(result) == 3:
                result.append('')
            if len(result) == 4:
                label, status, msg, xml = result
                rows.append({'label': sps_help(label), 'status': status, 'message': msg, 'xml': xml, _('why it is not a valid message?'): ' '})
            else:
                print('validations_table: ', result)
        r = html_reports.tag('div', html_reports.sheet(['label', 'status', 'message', 'xml', _('why it is not a valid message?')], rows, table_style='validation_sheet'))
    return r


def sps_help(label):
    r = label
    if label in attributes.SPS_HELP_ELEMENTS:
        href = 'http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/latest/tagset/elemento-{label}.html'.format(label=label)
        r += ' ' + html_reports.link(href, '[?]')
    return r


def display_article_metadata(_article, sep='<br/>'):
    dates_labels = ['collection', 'aop', 'epub', 'epub-ppub']
    dates = [_article.collection_dateiso, _article.ahpdate_dateiso, _article.epub_dateiso, _article.epub_ppub_dateiso]

    r = ''
    r += html_reports.tag('p', html_reports.tag('strong', _article.xml_name), 'doi')
    r += html_reports.tag('p', _article.publisher_article_id, 'doi')
    r += html_reports.tag('p', html_reports.tag('strong', _article.order), 'fpage')
    for l, d in zip(dates_labels, dates):
        if d is not None:
            r += html_reports.display_label_value(_('date') + ' (' + l + ')', utils.display_datetime(d), 'p')
    r += html_reports.tag('p', html_reports.tag('strong', _article.title), 'article-title')
    r += html_reports.tag('p', display_authors(_article.article_contrib_items, sep))
    return r


def display_article_data_in_toc(_article):
    r = ''
    style = 'excluded' if _article.is_ex_aop else None
    #status = validation_status.STATUS_INFO + ': ' + _('This article is an ex-aop article. ') + _('Order of ex-aop is reserved, it is not allowed to reuse it for other article. ') if _article.is_ex_aop else ''

    #r += html_reports.p_message(status)
    r += html_reports.tag('p', _article.toc_section, 'toc-section')
    r += html_reports.tag('p', _article.article_type, 'article-type')

    r += display_article_metadata(_article, '; ')
    return html_reports.tag('div', r, style)


def display_article_data_to_compare(_article):
    r = ''
    style = 'excluded' if _article.is_ex_aop else None
    status = validation_status.STATUS_INFO + ': ' + _('This article is an ex-aop article. ') + _('Order of ex-aop is reserved, it is not allowed to reuse it for other article. ') if _article.is_ex_aop else ''
    r += html_reports.p_message(status)
    r += display_article_metadata(_article, '<br/>')
    return html_reports.tag('div', r, style)


def old_article_history(articles):
    r = []
    for status, article in articles:
        text = []
        text.append(html_reports.tag('h4', _(status)))
        text.append(html_reports.display_label_value(_('name'), article.xml_name, 'p'))
        if article.is_ex_aop:
            text.append(html_reports.display_label_value(_('status'), 'ex-aop', 'p'))
        text.append(html_reports.display_label_value('order', article.order, 'p'))
        if article.creation_date_display is not None:
            text.append(html_reports.display_label_value(_('creation date'), article.creation_date_display, 'p'))
            text.append(html_reports.display_label_value(_('last update date'), article.last_update_display, 'p'))
        r.append(html_reports.tag('div', ''.join(text), 'hist-' + status))
    return ''.join(r)


def article_history(articles):
    r = []
    for status, article in articles:
        text = []
        text.append(html_reports.tag('h4', _(status)))
        text.append(html_reports.display_label_value(_('name'), article.xml_name, 'p'))
        text.append(html_reports.display_label_value('order', article.order, 'p'))
        if article.is_ex_aop:
            text.append(html_reports.display_label_value(_('status'), 'ex-aop', 'p'))
        if status in [_('registered article'), 'registered article']:
            r.append(display_article_data_in_toc(article))
            if article.creation_date_display is not None:
                text.append('<hr/>' + html_reports.display_label_value(_('creation date'), article.creation_date_display, 'p'))
                text.append(html_reports.display_label_value(_('last update date'), article.last_update_display, 'p'))
        r.append(html_reports.tag('div', ''.join(text), 'hist-' + status))
    return '<hr/>'.join(r)
