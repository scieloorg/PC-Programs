class ArticlesDataReports(object):

    def __init__(self, articles):
        self.articles = articles
        self.compile_references()

    @property
    def articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.articles.items()])
        l = [(xml_name, articles[xml_name]) for order, xml_name in l]
        return l

    def compile_references(self):
        self.sources_and_reftypes = {}
        self.reftype_and_sources = {}
        self.missing_source = []
        self.missing_year = []
        self.unusual_sources = []
        self.unusual_years = []
        self.years = {}
        for xml_name, doc in self.merged_articles.items():
            for ref in doc.references:
                if ref.source is not None:
                    if not ref.source in self.sources_and_reftypes.keys():
                        self.sources_and_reftypes[ref.source] = {}
                    if not ref.publication_type in self.sources_and_reftypes[ref.source].keys():
                        self.sources_and_reftypes[ref.source][ref.publication_type] = []
                    self.sources_and_reftypes[ref.source][ref.publication_type].append(xml_name + ': ' + str(ref.id))

                if not ref.publication_type in self.reftype_and_sources.keys():
                    self.reftype_and_sources[ref.publication_type] = {}
                if not ref.source in self.reftype_and_sources[ref.publication_type].keys():
                    self.reftype_and_sources[ref.publication_type][ref.source] = []
                self.reftype_and_sources[ref.publication_type][ref.source].append(xml_name + ': ' + str(ref.id))

                # year
                if ref.publication_type in attributes.BIBLIOMETRICS_USE:
                    if not ref.year in self.years.keys():
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

        for xml_name, doc in self.articles.items():
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
            for aff in doc.affiliations:
                if None in [aff.id, aff.i_country, aff.norgname, aff.orgname, aff.city, aff.state, aff.country]:
                    evaluation[_('incomplete affiliations')].append(xml_name)
        return evaluation

    @property
    def articles_dates_report(self):
        labels = ['name', '@article-type',
        'received', 'accepted', 'receive to accepted (days)', 'article date', 'issue date', 'accepted to publication (days)', 'accepted to today (days)']
        items = []
        for xml_name, doc in self.articles:
            values = []
            values.append(xml_name)
            values.append(doc.article_type)
            values.append(utils.display_datetime(doc.received_dateiso))
            values.append(utils.display_datetime(doc.accepted_dateiso))
            values.append(str(doc.history_days))
            values.append(utils.display_datetime(doc.article_pub_dateiso))
            values.append(utils.display_datetime(doc.issue_pub_dateiso))
            values.append(str(doc.publication_days))
            values.append(str(doc.registration_days))
            items.append(label_values(labels, values))
        article_dates = html_reports.sheet(labels, items, 'dbstatus')

        labels = [_('year'), _('location')]
        items = []
        for year in sorted(self.years.keys()):
            values = []
            values.append(year)
            values.append(self.years[year])
            items.append(label_values(labels, values))
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

    @property
    def references_overview_report(self):
        labels = ['label', 'status', 'message', _('why it is not a valid message?')]
        items = []
        values = []
        values.append(_('references by type'))
        values.append(validation_status.STATUS_INFO)
        values.append({reftype: str(sum([len(occ) for occ in sources.values()])) for reftype, sources in self.reftype_and_sources.items()})
        values.append('')
        items.append(label_values(labels, values))

        if len(self.bad_sources_and_reftypes) > 0:
            values = []
            values.append(_('same sources as different types references'))
            values.append(validation_status.STATUS_ERROR)
            values.append(self.bad_sources_and_reftypes)
            values.append('')
            items.append(label_values(labels, values))

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


class MergedArticlesData(object):

    def __init__(self, merged_articles, is_db_generation):
        self.merged_articles = merged_articles
        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_BLOCKING_ERROR, 'doi': validation_status.STATUS_BLOCKING_ERROR, 'elocation id': validation_status.STATUS_BLOCKING_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING
        self.IGNORE_NONE = ['journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', ]
        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

    @property
    def sorted_articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.merged_articles.items()])
        l = [(xml_name, articles[xml_name]) for order, xml_name in l]
        return l

    @property
    def is_processed_in_batches(self):
        return any([self.is_aop_issue, self.is_rolling_pass])

    @property
    def is_aop_issue(self):
        return any([a.is_ahead for a in self.merged_articles.values()])

    @property
    def is_rolling_pass(self):
        return all([a for a in self.merged_articles.values() if a.is_epub_only])

    @property
    def common_data(self):
        data = {}
        for label in self.EXPECTED_COMMON_VALUES_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if label in self.IGNORE_NONE and value is None:
                    pass
                else:
                    if not value in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def missing_required_data(self):
        required_items = {}
        for label in self.REQUIRED_DATA:
            if label in self.common_data.keys():
                if None in self.common_data[label].keys():
                    required_items[label] = self.common_data[label][None]
        return required_items

    @property
    def conflicting_values(self):
        data = {}
        for label, values in self.common_data.items():
            if len(values) > 1:
                data[label] = values
        return data

    @property
    def duplicated_values(self):
        duplicated_labels = {}
        for label, values in self.unique_values.items():
            if len(values) > 0 and len(values) != len(self.articles):
                duplicated = {value: xml_files for value, xml_files in values.items() if len(xml_files) > 1}
                if len(duplicated) > 0:
                    duplicated_labels[label] = duplicated
        return duplicated_labels

    @property
    def unique_values(self):
        data = {}
        for label in self.EXPECTED_UNIQUE_VALUE_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if value is not None:
                    if value not in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data


class MergedArticlesValidationsReports(object):

    def __init__(self, merged_articles_data):
        self.merged_articles_data = merged_articles_data

    @property
    def report_data_consistency(self):
        text = []
        text += self.report_missing_required_data
        text += self.report_conflicting_values
        text += self.report_duplicated_values
        text = html_reports.tag('div', ''.join(text), 'issue-messages')
        text += self.report_page_values
        return html_reports.tag('h2', _('Checking issue data consistency')) + text

    @property
    def report_missing_required_data(self):
        r = ''
        for label, items in self.merged_articles_data.missing_required_data.items():
            r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
            r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
        return r

    @property
    def report_conflicting_values(self):
        parts = []
        for label, values in self.merged_articles_data.conflicting_values.items():
            compl = ''
            _status = validation_status.STATUS_BLOCKING_ERROR
            if label == 'issue pub date':
                if self.is_rolling_pass:
                    _status = validation_status.STATUS_WARNING
            elif label == 'license':
                _status = validation_status.STATUS_WARNING
            _m = _('{status}: same value for {label} is required for all the documents in the package. ').format(status=_status, label=label)
            parts.append(html_reports.p_message(_m))
            parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
        return ''.join(parts)

    @property
    def report_duplicated_values(self):
        parts = []
        for label, values in self.merged_articles_data.duplicated_values.items():
            status = self.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
            _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
            parts.append(html_reports.p_message(status + ': ' + _m))
            for value, xml_files in values.items():
                parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
        return ''.join(parts)

    @property
    def report_page_values(self):
        # FIXME separar validacao e relatório
        results = []
        previous_lpage = None
        previous_xmlname = None
        int_previous_lpage = None

        error_level = validation_status.STATUS_BLOCKING_ERROR
        fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.merged_articles_data.sorted_articles]
        if all(fpage_and_article_id_other_status):
            error_level = validation_status.STATUS_ERROR

        for xml_name, article in self.merged_articles_data.sorted_articles:
            fpage = article.fpage
            lpage = article.lpage
            msg = []
            status = ''
            if article.pages == '':
                msg.append(_('no pagination was found. '))
                if not article.is_ahead:
                    status = validation_status.STATUS_ERROR
            if fpage is not None and lpage is not None:
                if fpage.isdigit() and lpage.isdigit():
                    int_fpage = int(fpage)
                    int_lpage = int(lpage)

                    #if not article.is_rolling_pass and not article.is_ahead:
                    if int_previous_lpage is not None:
                        if int_previous_lpage > int_fpage:
                            status = error_level if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid value for fpage and lpage. Check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage == int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}) are the same. ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                        elif int_previous_lpage + 1 < int_fpage:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('There is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous_xmlname, xml_name=xml_name, lpage=previous_lpage, fpage=fpage))
                    if int_fpage > int_lpage:
                        status = error_level
                        msg.append(_('Invalid page range: {fpage} (fpage) > {lpage} (lpage). '.format(fpage=int_fpage, lpage=int_lpage)))
                    int_previous_lpage = int_lpage
                    previous_lpage = lpage
                    previous_xmlname = xml_name
            #dates = '|'.join([item if item is not None else 'none' for item in [article.epub_ppub_dateiso, article.collection_dateiso, article.epub_dateiso]])
            msg = '\n'.join(msg)
            results.append({'label': xml_name, 'status': status, 'pages': article.pages, 'message': msg, _('why it is not a valid message?'): ''})
        return html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'pages', 'message', _('why it is not a valid message?')], results, table_style='validation_sheet', widths={'label': '10', 'status': '10', 'pages': '5', 'message': '75'}))


class MergingResult(object):

    def __init__(self):
        self.exclusions = []
        self.conflicts = {}
        self.actions = {}
        self.name_changes = {}
        self.order_changes = {}

        ###
    def registered_data_conflicts_report(self):
        merging_errors = []
        if len(self.conflicts) > 0:
            merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]
            for name, conflicts in self.conflicts.items():
                labels = ['package']
                values = [name]
                for k, articles in conflicts.items():
                    labels.append(k)
                    if isinstance(articles, dict):
                        data = []
                        for article in articles.values():
                            data.append(article_reports.display_article_data_to_compare(article))
                        values.append(''.join(data))
                    else:
                        values.append(article_reports.display_article_data_to_compare(articles))
                merging_errors.append(html_reports.sheet(labels, [label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
        return ''.join(merging_errors)

    @property
    def validations(self):
        v = ValidationsResult()
        v.message = ''.join([display_order_conflicts(self.orders_conflicts(self.merged_articles)) + self.registered_data_conflicts_report()])
        return v

    @property
    def names_change_report(self):
        r = []
        if len(self.name_changes) > 0:
            r.append(html_reports.tag('h3', _('Names changes')))
            for old, new in self.name_changes.items():
                r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
        return ''.join(r)

    @property
    def orders_change_report(self):
        r = []
        if len(self.order_changes) > 0:
            r.append(html_reports.tag('h3', _('Orders changes')))
            for name, changes in self.order_changes.items():
                for change in changes:
                    r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=change[0], new=change[1]), 'info'))
        if len(self.excluded_orders) > 0:
            r.append(html_reports.tag('h3', _('Orders exclusions')))
            for name, order in self.excluded_orders.items():
                r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
        return ''.join(r)

    @property
    def changes_report(self):
        r = ''
        r += self.orders_change_report
        r += self.names_change_report
        if len(r) > 0:
            r = html_reports.tag('h2', _('Changes Report')) + r
        return r


class ArticlesMerger(object):

    def __init__(self, registered_articles, articles):
        self._merged_articles = registered_articles.copy()
        self.registered_articles = RegisteredArticles(registered_articles)
        self.articles = articles
        self.merging_result = MergingResult()

    @property
    def total_to_convert(self):
        return len(self.articles)

    @property
    def xc_articles(self):
        return self.articles

    @property
    def merged_articles(self):
        return self._merged_articles

    def merge(self):
        self.analyze_pkg()
        self.update_articles()

    def analyze_pkg(self):
        for name, article in self.articles.items():
            action, old_name, conflicts = self.analyze_pkg_article(name, article)
            if conflicts is not None:
                self.merging_result.conflicts[name] = conflicts
            if action is not None:
                self.merging_result.actions[name] = action
            if action == 'update' and article.marked_to_delete:
                self.merging_result.exclusions.append(name)
            if old_name is not None:
                self.merging_result.name_changes[old_name] = name
            if name in self.registered_articles.keys():
                if article.order != self.registered_articles[name].order:
                    self.order_changes[name] = (self.registered_articles[name].order, article.order)

    def analyze_pkg_article(self, name, pkg_article):
        registered_titaut, registered_name, registered_order = self.registered_articles.search_articles(name, pkg_article)
        action, old_name, conflicts = self.registered_articles.analyze_registered_articles(name, registered_titaut, registered_name, registered_order)
        return (action, old_name, conflicts)

    def update_articles(self):
        self.history_items = {}
        # starts history with registered articles data
        self.history_items = {name: [('registered article', article)] for name, article in self.registered_articles.items()}

        # exclude registered items
        for name in self.merging_result.exclusions:
            self.history_items[name].append(('excluded article', self._merged_articles[name]))
            del self._merged_articles[name]

        # indicates package articles reception
        for name, article in self.articles.items():
            if not name in self.history_items.keys():
                self.history_items[name] = []
            self.history_items[name].append(('package', article))

        # indicates names changes, and exclude old names
        for previous_name, name in self.merging_result.name_changes.items():
            self.history_items[previous_name].append(('replaced by', self.articles[name]))

            self.history_items[name].append(('replaces', self._merged_articles[previous_name]))
            del self._merged_articles[previous_name]

        # merge pkg and registered, considering some of them are rejected
        orders_to_check = []
        for name, article in self.articles.items():
            if not article.marked_to_delete:
                action = self.merging_result.actions.get(name)

                if name in self.merging_result.conflicts.keys():
                    action = 'reject'
                if not action in ['reject', None]:
                    self._merged_articles[name] = self.articles[name]

    def orders_conflicts(self):
        orders = {}
        for name, article in self._merged_articles.items():
            if not article.order in orders.keys():
                orders[article.order] = []
            orders[article.order].append(name)
        return {order: names for order, names in orders.items() if len(names) > 1}

    @property
    def excluded_orders(self):
        #excluded_orders
        items = {}
        orders = [article.order for article in self.merged_articles.values()]
        for name, article in self.registered_articles.items():
            if not article.order in orders:
                items[name] = article.order
        return {name: article.order for name, article in self.registered_articles.items() if not article.order in orders}


class ArticlesSetValidations(object):

    def __init__(self, articles, outputs, registered_issue_data, package_path, is_xml_generation):
        self.articles = articles
        self.outputs = outputs
        self.registered_issue_data = registered_issue_data
        self.package_path = package_path
        self.is_xml_generation = is_xml_generation

        self.is_db_generation = self.registered_issue_data.db_manager is not None

        self.articles_merger = ArticlesMerger(self.registered_issue_data.registered_articles, self.articles)
        self.articles_merger.merge()
        self.merged_articles = self.articles_merger.merged_articles

        self.articles_validations = None

    def validate(self, doi_services, dtd_files):
        utils.display_message(_('Validate package ({n} files)').format(n=len(self.articles)))
        if len(self.registered_issue_data.registered_articles) > 0:
            utils.display_message(_('Previously registered: ({n} files)').format(n=len(self.registered_issue_data.registered_articles)))

        self.logger.register('pkg_journal_validations')
        self.pkg_journal_validations = ValidationsResultItems()
        self.pkg_journal_validations.title = self.pkg_journal_validations_report_title

        self.logger.register('pkg_issue_validations')
        self.pkg_issue_validations = ValidationsResultItems()
        self.pkg_issue_validations.title = html_reports.tag('h2', _('Checking issue data: XML files and registered data'))

        self.logger.register('articles validations - prep')

        xml_journal_data_validator = XMLJournalDataValidator(self.pkgissuedata.journal_data)
        xml_issue_data_validator = XMLIssueDataValidator(self.registered_issue_data)
        xml_structure_validator = XMLStructureValidator(dtd_files)
        xml_structure_validator.logger = self.logger
        xml_content_validator = XMLContentValidator(doi_services, self.pkgissuedata, self.registered_issue_data, self.package_path, self.is_xml_generation)
        xml_article_validator = ArticleValidator(xml_structure_validator, xml_content_validator)

        self.logger.register('articles validations')
        self.articles_validations = {}

        for name, article in self.articles.items():
            utils.display_message(_('Validate {name}').format(name=name))
            self.logger.register(' '.join(['validate', name]))

            self.pkg_journal_validations[name] = ValidationsResult()
            self.pkg_journal_validations[name].message = xml_journal_data_validator.validate(article)

            self.pkg_issue_validations[name] = ValidationsResult()
            self.pkg_issue_validations[name].message = xml_issue_data_validator.validate(article)

            self.articles_validations[name] = xml_article_validator.validate(article, self.outputs[name], self.pkg_issue_validations[name])

            self.logger.register(' '.join([name, 'fim']))

        self.logger.register('consistency validations')
        self.consistency_validations = ValidationsResult()

        issue_message = self.report_data_consistency
        if self.registered_issue_data.issue_error_msg is not None:
            issue_message = self.registered_issue_data.issue_error_msg + issue_message

        self.consistency_validations.message = issue_message

        self.logger.register('xc pre validations - fim')

    @property
    def pkg_journal_validations_report_title(self):
        #FIXME
        signal = ''
        msg = ''
        if not self.is_db_generation:
            signal = '<sup>*</sup>'
            msg = html_reports.tag('h5', '<a name="note"><sup>*</sup></a>' + _('Journal data in the XML files must be consistent with {link}').format(link=html_reports.link('http://static.scielo.org/sps/titles-tab-v2-utf-8.csv', 'http://static.scielo.org/sps/titles-tab-v2-utf-8.csv')), 'note')
        return html_reports.tag('h2', _('Journal data: XML files and registered data') + signal) + msg

    @property
    def detailed_report(self):
        labels = [_('filename'), 'order', _('article'), 'aop pid/related', _('reports')]
        widths = {}
        widths[_('filename')] = '10'
        widths['order'] = '5'
        widths[_('article')] = '60'
        widths['aop pid/related'] = '10'
        widths[_('reports')] = '10'
        pdf_items = []
        items = []
        for new_name, article in self.articles:
            hide_and_show_block_items = self.articles_validations[new_name].hide_and_show_block('view-reports-', new_name)
            values = []
            values.append(new_name)
            values.append(article.order)
            if self.articles_validations[new_name].article_display_report is None:
                values.append('')
            else:
                values.append(self.articles_validations[new_name].article_display_report.table_of_contents)
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
    def journal_issue_header_report(self):
        common_data = ''
        for label, values in self.merged_articles.common_data.items():
            if len(values.keys()) == 1:
                common_data += html_reports.tag('p', html_reports.display_label_value(label, values.keys()[0]))
            else:
                common_data += html_reports.format_list(label + ':', 'ol', values.keys())
        return html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', common_data, 'issue-data')


    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.journal_issue_header_report)
        report.append(self.pkg_journal_validations.report(errors_only=not self.pkg.is_xml_generation))
        report.append(self.pkg_issue_validations.report(errors_only=not self.pkg.is_xml_generation))
        if self.consistency_validations.total() > 0:
            report.append(self.consistency_validations.message)

        if self.articles_merger.validations.total() > 0:
            report.append(html_reports.tag('h2', _('Data Conflicts Report')))
            report.append(self.articles_merger.validations.message)
        return ''.join(report)

    @property
    def blocking_errors(self):
        return sum([self.consistency_validations.blocking_errors, self.pkg_issue_validations.blocking_errors, self.articles_merger.validations.blocking_errors])

    @property
    def fatal_errors(self):
        return sum([v.fatal_errors for v in self.articles_validations.values()])


"""
ArticlesDataReports(articles)

MergedArticlesData( merged_articles, is_db_generation)

MergedArticlesValidationsReports(merged_articles_data)


MergingResult()

ArticlesMerger(registered_articles, articles)

ArticlesSetValidations()
"""