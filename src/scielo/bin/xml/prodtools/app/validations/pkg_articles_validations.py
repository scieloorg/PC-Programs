# coding=utf-8

from ...__init__ import _
from ...generics import utils
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from . import validations as validations_module
from ..data import attributes


class PkgArticlesValidationsReports(object):

    def __init__(self, pkg_articles_validations, is_db_generation=False):
        self.consistency_validations = None
        self.pkg_articles_validations = pkg_articles_validations
        self.is_db_generation = is_db_generation
        self.merged_articles_reports = None

    @property
    def pkg_journal_validations(self):
        items = validations_module.ValidationsResultItems()
        for name, validation in self.pkg_articles_validations.items():
            items[name] = validation.journal_validations
        signal = ''
        msg = ''
        if not self.is_db_generation:
            signal = '<sup>*</sup>'
            msg = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        items.title = html_reports.tag('h2', _('Journal data: XML files and registered data') + signal) + msg
        return items

    @property
    def pkg_issue_validations(self):
        items = validations_module.ValidationsResultItems()
        for name, validation in self.pkg_articles_validations.items():
            items[name] = validation.issue_validations
        items.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))
        return items

    @property
    def detailed_report(self):
        labels = [_('filename'), 'order', _('article'), 'aop pid/related', _('reports')]
        widths = {}
        widths[_('filename')] = '10'
        widths['order'] = '5'
        widths[_('article')] = '60'
        widths['aop pid/related'] = '10'
        widths[_('reports')] = '10'
        items = []
        for new_name, a_validations in sorted(self.pkg_articles_validations.items()):
            hide_and_show_block_items = a_validations.hide_and_show_block('view-reports-', new_name)
            values = []
            values.append(new_name)
            if a_validations.article_display_report is None:
                values.append('')
                values.append('')
                values.append('')
            else:
                article = a_validations.article_display_report.article
                values.append(article.order)
                values.append(a_validations.article_display_report.table_of_contents)
                related = {}
                for k, v in {'article-id(previous-pid)': article.previous_pid, 'related': [item.get('xml', '') for item in article.related_articles]}.items():
                    if v is not None:
                        if len(v) > 0:
                            related[k] = v
                values.append(related)
            items.append((values, hide_and_show_block_items))
        report = html_reports.HideAndShowBlocksReport(labels, items, html_cell_content=[_('article')], widths=widths)
        return report.content

    @property
    def validations(self):
        _validations = list(self.pkg_articles_validations.values())
        _validations.append(self.pkg_issue_validations)
        _validations.append(self.pkg_journal_validations)
        return _validations

    @property
    def fatal_errors(self):
        return sum([v.fatal_errors for v in self.validations])

    @property
    def blocking_errors(self):
        return sum([v.blocking_errors for v in self.validations])


class PackageReports(object):

    def __init__(self, package_folder):
        self.package_folder = package_folder

    @property
    def xml_list(self):
        r = ''
        r += u'<p>{}: {}</p>'.format(_('XML path'), self.package_folder.path)
        r += u'<p>{}: {}</p>'.format(_('Total of XML files'), len(self.package_folder.pkgfiles_items))

        files = ''
        for name, pkgfiles in self.package_folder.pkgfiles_items.items():
            files += '<li>{}</li>'.format(html_reports.format_list(name, 'ol', pkgfiles.files))
        r += '<ol>{}</ol>'.format(files)
        return u'<div class="xmllist">{}</div>'.format(r)

    @property
    def orphan_files_report(self):
        if len(self.package_folder.orphans) > 0:
            return '<div class="xmllist"><p>{}</p>{}</div>'.format(_('Invalid files names'), html_reports.format_list('', 'ol', self.package_folder.orphans))
        return ''


class PkgArticlesDataReports(object):

    def __init__(self, pkg_articles):
        self.pkg_articles = pkg_articles
        self.compile_references()

    @property
    def articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.pkg_articles.items()])
        l = [(xml_name, self.pkg_articles[xml_name]) for order, xml_name in l]
        return l

    @property
    def invalid_xml_name_items(self):
        return sorted([xml_name for xml_name, doc in self.pkg_articles.items() if doc.tree is None])

    @property
    def invalid_xml_report(self):
        r = ''
        if len(self.invalid_xml_name_items) > 0:
            r += html_reports.tag('div', html_reports.p_message(_('{status}: invalid XML files. ').format(status=validation_status.STATUS_BLOCKING_ERROR)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', self.invalid_xml_name_items, 'issue-problem'))
        return r

    @property
    def compiled_affiliations(self):
        evaluation = {}
        keys = [
            _('authors without aff'),
            _('authors with more than 1 affs'),
            _('authors with invalid xref[@ref-type=aff]'),
            _('incomplete affiliations')
            ]
        for k in keys:
            evaluation[k] = []

        for xml_name, doc in self.pkg_articles.items():
            aff_ids = [aff.id for aff in doc.affiliations]
            for contrib in doc.contrib_names:
                if len(contrib.xref) == 0:
                    evaluation[_('authors without aff')].append(xml_name)
                elif len(contrib.xref) > 1:
                    valid_xref = [xref for xref in contrib.xref if xref in aff_ids]
                    if len(valid_xref) != len(contrib.xref):
                        evaluation[_('authors with invalid xref[@ref-type=aff]')].append(xml_name)
                    elif len(valid_xref) > 1:
                        evaluation[_('authors with more than 1 affs')].append(xml_name)
                    elif len(valid_xref) == 0:
                        evaluation[_('authors without aff')].append(xml_name)
            for aff_xml in doc.affiliations:
                aff = aff_xml.aff
                if None in [aff.id, aff.i_country, aff.norgname, aff.orgname, aff.city, aff.state, aff.country]:
                    evaluation[_('incomplete affiliations')].append(xml_name)
        return evaluation

    @property
    def articles_dates_report(self):
        labels = ['name', '@article-type',
        'received', 'accepted', 'receive to accepted (days)', 'SciELO date', 'editorial date', 'accepted to SciELO (days)', 'accepted to nowadays (days)']
        items = []
        for xml_name, doc in self.articles:
            values = []
            values.append(xml_name)
            values.append(doc.article_type)
            values.append(utils.display_datetime(doc.received_dateiso))
            values.append(utils.display_datetime(doc.accepted_dateiso))
            values.append(str(doc.history_days))
            values.append(utils.display_datetime(doc.isoformat(doc.real_pubdate)))
            values.append(utils.display_datetime(doc.isoformat(doc.expected_pubdate)))
            values.append(str(doc.accepted_to_real_in_days))
            values.append(str(doc.accepted_to_nowadays_in_days))
            items.append(html_reports.label_values(labels, values))
        article_dates = html_reports.sheet(labels, items, 'dbstatus')

        labels = [_('year'), _('location')]
        items = []
        for year in sorted(self.years.keys()):
            values = []
            values.append(year)
            values.append(self.years[year])
            items.append(html_reports.label_values(labels, values))
        reference_dates = html_reports.sheet(labels, items, 'dbstatus')

        return html_reports.tag('h4', _('Articles Dates Report')) + article_dates + reference_dates

    @property
    def articles_affiliations_report(self):
        r = html_reports.tag('h4', _('Affiliations Report'))
        items = []
        for label, occs in self.compiled_affiliations.items():
            items.append({'label': label, 'quantity': str(len(occs)), _('files'): sorted(list(set(occs)))})
        r += html_reports.sheet(['label', 'quantity', _('files')], items, 'dbstatus')
        return r

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        self.years = {}
        for xml_name, doc in self.pkg_articles.items():
            for ref_xml in doc.references_xml:
                ref = ref_xml.reference
                if ref.source is not None:
                    if ref.source not in self.sources_and_reftypes.keys():
                        self.sources_and_reftypes[ref.source] = {}
                    if ref.publication_type not in self.sources_and_reftypes[ref.source].keys():
                        self.sources_and_reftypes[ref.source][ref.publication_type] = []
                    self.sources_and_reftypes[ref.source][ref.publication_type].append(xml_name + ': ' + str(ref.id))

                if ref.publication_type not in self.reftype_and_sources.keys():
                    self.reftype_and_sources[ref.publication_type] = {}
                if ref.source not in self.reftype_and_sources[ref.publication_type].keys():
                    if ref.source is None:
                        ref.source = ''
                    self.reftype_and_sources[ref.publication_type][ref.source] = []
                self.reftype_and_sources[ref.publication_type][ref.source].append(xml_name + ': ' + str(ref.id))

                # year
                if ref.publication_type in attributes.BIBLIOMETRICS_USE:
                    if ref.year not in self.years.keys():
                        if ref.year is None:
                            ref.year = ''
                        self.years[ref.year] = []
                    self.years[ref.year].append(xml_name + ': ' + str(ref.id))
                    if ref.year is None:
                        self.missing_year.append([xml_name, ref.id])
                    else:
                        if not ref.year.isdigit():
                            self.unusual_years.append([xml_name, ref.id, ref.year])

                    if ref.source is None:
                        self.missing_source.append([xml_name, ref.id])
                    else:
                        if ref.source.isdigit():
                            self.unusual_sources.append([xml_name, ref.id, ref.source])
        self.bad_sources_and_reftypes = {source: reftypes for source, reftypes in self.sources_and_reftypes.items() if len(reftypes) > 1}

    @property
    def references_overview_report(self):
        labels = ['label', 'status', 'message', _('why it is not a valid message?')]
        items = []
        values = []
        values.append(_('references by type'))
        values.append(validation_status.STATUS_INFO)
        values.append({reftype: str(sum([len(occ) for occ in sources.values()])) for reftype, sources in self.reftype_and_sources.items()})
        values.append('')
        items.append(html_reports.label_values(labels, values))

        if len(self.bad_sources_and_reftypes) > 0:
            values = []
            values.append(_('same sources as different types references'))
            values.append(validation_status.STATUS_ERROR)
            values.append(self.bad_sources_and_reftypes)
            values.append('')
            items.append(html_reports.label_values(labels, values))

        if len(self.missing_source) > 0:
            items.append({'label': _('references missing source'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.missing_source], _('why it is not a valid message?'): ''})
        if len(self.missing_year) > 0:
            items.append({'label': _('references missing year'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.missing_year], _('why it is not a valid message?'): ''})
        if len(self.unusual_sources) > 0:
            items.append({'label': _('references with unusual value for source'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.unusual_sources], _('why it is not a valid message?'): ''})
        if len(self.unusual_years) > 0:
            items.append({'label': _('references with unusual value for year'), 'status': validation_status.STATUS_ERROR, 'message': [' - '.join(item) for item in self.unusual_years], _('why it is not a valid message?'): ''})

        return html_reports.tag('h4', _('Package references overview')) + html_reports.sheet(labels, items, table_style='dbstatus')

    @property
    def sources_overview_report(self):
        labels = ['source', _('location')]
        h = ''
        if len(self.reftype_and_sources) > 0:
            for reftype, sources in self.reftype_and_sources.items():
                items = []
                h += html_reports.tag('h4', reftype)
                for source in sorted(sources.keys()):
                    items.append({'source': source, _('location'): sources[source]})
                h += html_reports.sheet(labels, items, 'dbstatus')
        return h
