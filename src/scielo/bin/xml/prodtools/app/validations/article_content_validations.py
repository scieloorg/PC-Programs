# coding=utf-8

import os
from datetime import datetime

from prodtools import _
from prodtools.utils import img_utils
from prodtools.utils import utils
from prodtools.utils import encoding
from prodtools.data import article_utils
from prodtools.reports import html_reports
from prodtools.reports import validation_status
from prodtools.data import attributes
from prodtools.validations import ref_validations
from prodtools.validations import data_validations
from prodtools.validations import orcid
from prodtools.validations import article_disp_formula
from prodtools.validations import article_tablewrap
from prodtools.processing import xml_versions


def join_not_None_items(items, sep=', '):
    return sep.join([item for item in items if item is not None])


def confirm_missing_xref_items(missing_xref_items, any_xref_ranges_items):
    confirmed_missing = missing_xref_items
    if len(any_xref_ranges_items) > 0:
        missing_numbers = [int(rid[1:]) for rid in missing_xref_items if rid[1:].isdigit()]
        not_missing = []
        i = 0
        for missing_number in missing_numbers:
            for start, end, start_node, end_node in any_xref_ranges_items:
                if start < missing_number < end:
                    not_missing.append(missing_xref_items[i])
            i += 1
        confirmed_missing = []
        for missing_xref in missing_xref_items:
            if missing_xref not in not_missing:
                confirmed_missing.append(missing_xref)
    return confirmed_missing


class AffValidator(object):

    def __init__(self, aff_xml, institutions_query_results, xref_items):
        self.aff_xml = aff_xml
        self.aff = aff_xml.aff
        self.xref_items = xref_items
        self.institutions_query_results = institutions_query_results
        self.norm_aff = None
        self._validations = None

    @property
    def xml(self):
        return ('aff xml', validation_status.STATUS_INFO, self.aff_xml.xml)

    @property
    def id(self):
        return data_validations.required_data('aff/@id', self.aff_xml.id)

    @property
    def original(self):
        return data_validations.required_data('aff/institution/[@content-type="original"]', self.aff_xml.original, validation_status.STATUS_ERROR)

    @property
    def orgname(self):
        return data_validations.required_data('aff/institution/[@content-type="orgname"]', self.aff_xml.orgname)

    @property
    def orgdivs(self):
        r = []
        for orgdiv in [self.aff_xml.orgdiv1, self.aff_xml.orgdiv2]:
            item = ', '.join(orgdiv)
            if len(item) > 0:
                status = ''
                if 'univers' in item.lower():
                    status = validation_status.STATUS_WARNING
                elif 'depart' not in item.lower() and 'divi' not in item.lower():
                    status = validation_status.STATUS_WARNING
                if len(status) > 0:
                    orgname = self.aff_xml.orgname[0] if len(self.aff_xml.orgname) > 0 else _('an organization')
                    r.append(('aff/institution[@content-type="orgdiv?"]', status, _('Be sure that {value} is a division of {orgname}. ').format(value=item, orgname=orgname)))
        return r

    @property
    def orgdiv3(self):
        if len(self.aff_xml.orgdiv3) > 0:
            return ('aff/institution/[@content-type="orgdiv3"]', validation_status.STATUS_ERROR, _('Remove this institution(orgdiv3). Use only one orgdiv1 and one orgdiv2. Other levels are not allowed. '))

    @property
    def country(self):
        r = []
        for code, text in self.aff_xml.country:
            r.extend(data_validations.required_data('aff/country', text, validation_status.STATUS_ERROR))
            r.extend(attributes.validate_iso_country_code(code))
        return r

    @property
    def normalized(self):
        return []
        r = []
        status_error = validation_status.STATUS_DISAGREED_WITH_COLLECTION_CRITERIA
        status_fatal_error = validation_status.STATUS_DISAGREED_WITH_COLLECTION_CRITERIA
        if self.aff.norgname is None:
            return r
        if self.institutions_query_results is not None:
            norm_aff, found_institutions = self.institutions_query_results
            if norm_aff is None:
                msg = _('Unable to confirm/find the normalized institution name for ') + join_not_None_items(list(set([self.aff.orgname, self.aff.norgname])), ' or ')
                if found_institutions is None or len(found_institutions) == 0:
                    r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_WARNING, msg))
                else:
                    msg += _('. Check if any option of the list is the normalized name: ') + '<OPTIONS/>' + '|'.join([join_not_None_items(list(item)) for item in found_institutions])
                    r.append((_('Suggestions:'), status_error, msg))
            else:
                status = status_fatal_error
                if self.aff.norgname is not None:
                    if self.aff.norgname == norm_aff.norgname:
                        status = validation_status.STATUS_VALID
                if status == validation_status.STATUS_VALID:
                    message = _('Valid: ') + join_not_None_items([norm_aff.norgname, norm_aff.city, norm_aff.state, norm_aff.i_country, norm_aff.country])
                else:
                    message = _('Use {right} instead of {wrong}. ').format(right=norm_aff.norgname, wrong=self.aff.norgname)
                r.append(('aff/institution/[@content-type="normalized"]', status, message))
            self.norm_aff = norm_aff
        return r

    @property
    def occurrences(self):
        labels = []
        labels.append('institution[@content-type="original"]')
        labels.append('institution[@content-type="normalized"]')
        labels.append('institution[@content-type="orgname"]')
        labels.append('institution[@content-type="orgdiv1"]')
        labels.append('institution[@content-type="orgdiv2"]')
        labels.append('addr-line/named-content[@content-type="city"]')
        labels.append('addr-line/named-content[@content-type="state"]')
        labels.append('country')
        items = [self.aff_xml.original, self.aff_xml.norgname, self.aff_xml.orgname, self.aff_xml.orgdiv1, self.aff_xml.orgdiv2, self.aff_xml.city, self.aff_xml.state, self.aff_xml.country]

        r = []
        for label, item in zip(labels, items):
            if len(item) > 1:
                r.append(data_validations.is_required_only_one(label, validation_status.STATUS_FATAL_ERROR))
        return r

    @property
    def xref(self):
        r = []
        if self.aff.id not in self.xref_items:
            r.append(('aff/@id', validation_status.STATUS_FATAL_ERROR, _('Not found: {label}. ').format(label='<xref ref-type="aff" rid="' + str(self.aff.id) + '"/>')))
        return r

    @property
    def validations(self):
        if self._validations is None:
            r = []
            r.append(self.xml)
            r.extend(self.id)
            r.extend(self.original)
            r.extend(self.country)
            r.extend(self.orgname)
            r.append(self.orgdiv3)
            r.append(self.normalized)
            r.append(self.occurrences)
            r.append(self.xref)
            self._validations = [item for item in r if item is not None]
        return self._validations


class ArticleContentValidation(object):

    def __init__(self, journal, _article, pkgfiles, is_db_generation, check_url, app_institutions_manager, doi_validator, config):
        self.doi_validator = doi_validator
        self.app_institutions_manager = app_institutions_manager
        self.journal = journal
        self.article = _article
        self.is_db_generation = is_db_generation
        self.check_url = check_url
        self.pkgfiles = pkgfiles
        self._validations = None
        self.config = config
        self.disp_formulas_validator = article_disp_formula.ArticleDispFormulasValidator(config)
        self.tablewrap_validator = article_tablewrap.ArticleTableWrapValidator(config)
        self.orcid_validator = orcid.ORCIDValidator(config.app_ws_requester)

    def normalize_validations(self, validations_result_list):
        r = []
        if isinstance(validations_result_list, list):
            for item in validations_result_list:
                r += self.normalize_validations(item)
        elif validations_result_list is None:
            pass
        else:
            r.append(validations_result_list)
        return r

    @property
    def validations(self):
        if self._validations is None:
            performance = []
            #encoding.debugging(datetime.now().isoformat() + ' validations 1')
            items = []
            items.append(self.sps)
            items.append(self.expiration_sps)
            items.append(self.language)
            items.append(self.languages)
            items.append(self.article_type)

            if self.article.article_meta is None:
                items.append(('journal-meta', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='journal-meta')))
            else:
                items.append(self.journal_title)
                items.append(self.publisher_name)
                items.append(self.journal_id_publisher_id)
                items.append(self.journal_id_nlm_ta)
                items.append(self.journal_issns)

            if self.article.article_meta is None:
                items.append(('article-meta', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='article-meta')))
            else:
                items.append(self.months_seasons)
                items.append(self.issue_label)
                items.append(self.article_date_types)
                items.append(self.toc_section)
                items.append(self.doi)
                items.append(self.doi_and_lang)
                items.append(self.article_id)
                items.append(self.pagination)
                if self.is_db_generation:
                    items.append(self.article_id_other)
                    items.append(self.order)
                items.append(self.total_of_pages)
                items.append(self.total_of_equations)
                items.append(self.total_of_tables)
                items.append(self.total_of_figures)
                items.append(self.total_of_references)
                items.append(self.ref_display_only_stats)
                items.append(self.contrib)
                items.append(self.contrib_id)
                items.append(self.contrib_names)
                items.append(self.contrib_collabs)
                items.append(self.affiliations)
                items.append(self.funding)
                items.append(self.article_permissions)
                items.append(self.history)
                items.append(self.titles_abstracts_keywords)

                items.append(self.related_articles)

            items.append(self.sections)
            items.append(self.paragraphs)
            items.append(self.disp_formulas_validator.validate(self.article))
            items.append(self.tablewrap_validator.validate(self.article))
            items.append(self.validate_xref_reftype)
            items.append(self.missing_xref_list)
            #items.append(self.innerbody_elements_permissions)

            items.append(self.refstats)
            items.append(self.refs_sources)

            r = self.normalize_validations(items)
            encoding.debugging('fim normalize_validations', '')
            self._validations = (r, performance)
        return self._validations

    @property
    def dtd_version(self):
        return data_validations.is_expected_value('@dtd-version', self.article.dtd_version, xml_versions.valid_dtd_items)

    @property
    def article_type(self):
        """
        com autoria e afiliação institucional dos autores,
        título próprio diferente do título da seção,
        citações,
        e referências bibliográficas
        """
        results = attributes.validate_article_type_and_section(self.article.article_type, self.article.toc_section, len(self.article.abstracts) > 0)
        msg = _('The documents used to generate the bibliometric indicators must have:\na) @article-type ({}); b) contributors and their affiliations; c) own title, not similar to the table of contents title; d) citations; e) and references. ').format(_(', ').join(attributes.INDEXABLE))
        level = validation_status.STATUS_FATAL_ERROR
        if self.config.BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA:
            level = validation_status.STATUS_BLOCKING_ERROR

        errors = []
        warnings = []
        if self.article.article_type in attributes.INDEXABLE:
            if self.article.article_type not in attributes.INDEXABLE_BUT_EXCEPTION \
                    and not self.article.is_provisional:
                check = attributes.INDEXABLE_EXCEPTIONS.get(
                    self.article.article_type,
                    ['contrib', 'aff', 'xref (bibr)', 'ref']
                )
                items = [
                    ('contrib', len(self.article.article_contrib_items)),
                    ('aff', len(self.article.article_affiliations)),
                    ('xref (bibr)', len(self.article.bibr_xref_nodes)),
                    ('ref', len(self.article.references_xml))]
                invalid = [label
                           for label, qtd in items
                           if label in check and qtd == 0]
                warning = [label
                           for label, qtd in items
                           if label not in check and qtd == 0]
                if len(warning) > 0:
                    warnings.append(
                        _('@article-type="{}" expects: {}. ').format(
                            self.article.article_type,
                            ' ; '.join(warning)))
                if len(invalid) > 0:
                    errors.append(
                        _('@article-type="{}" requires: {}. ').format(
                            self.article.article_type,
                            ' ; '.join(invalid)))
                titles = [t.title for t in self.article.titles]
                _titles = ' / '.join([u'"{}"'.format(t) for t in titles])
                if utils.is_similar(self.article.toc_section, titles):
                    errors.append(
                        _(u'{} must not be similar to the table of contents section "{}" '.format(
                            _titles, self.article.toc_section)))
        else:
            errors.append(
                _('@article-type="{}" is not used to generate bibliometric indicators').format(self.article.article_type))
        if len(errors) > 0:
            results.append(('@article-type', level, msg))
            results.append(
                (
                    '@article-type',
                    level,
                    _('This document will be rejected according to SciELO Collection\'s criteria. ') +
                    _('Check the criteria of the corresponding SciELO Collection. ')
                ))
            results.append(('@article-type', level, ''.join(errors)))
        if len(warnings) > 0:
            results.append(('@article-type', validation_status.STATUS_FATAL_ERROR, ''.join(warnings)))
        return results

    @property
    def sps(self):
        version = str(self.article.sps)
        label = 'article/@specific-use'
        status = validation_status.STATUS_INFO
        msg = version

        if version in attributes.sps_current_versions():
            return [(label, status, msg)]

        pub_dateiso = self.article.real_pubdate or self.article.expected_pubdate
        if pub_dateiso is None:
            return [(label, validation_status.STATUS_ERROR, _('Unable to validate sps version because article has no publication date. '))]
        pub_dateiso = article_utils.format_dateiso(pub_dateiso)

        expected_versions = list(set(attributes.expected_sps_versions(pub_dateiso) + attributes.sps_current_versions()))
        expected_versions.sort()

        if version in expected_versions:
            status = validation_status.STATUS_INFO
            msg = _('For articles published on {pubdate}, {sps_version} is valid. ').format(pubdate=utils.display_datetime(pub_dateiso, None), sps_version=version)
        else:
            status = validation_status.STATUS_ERROR
            msg = _('For articles published on {pubdate}, {sps_version} is not valid. ').format(pubdate=utils.display_datetime(pub_dateiso, None), sps_version=version) + _('Expected SPS versions for this article: {sps_versions}. ').format(sps_versions=_(' or ').join(expected_versions))
        return [(label, status, msg)]

    @property
    def expiration_sps(self):
        version = str(self.article.sps)
        days = attributes.sps_version_expiration_days(version)
        if days is None:
            return [(_('sps expiration date'), validation_status.STATUS_WARNING, _('Unable to identify expiration date of SPS version={version}. ').format(version=version))]
        if days < 0:
            return [(_('sps expiration date'), validation_status.STATUS_INFO, _('{version} has expired {days} days ago. ').format(version=version, days=-1 * days))]
        if days > 0:
            return [(_('sps expiration date'), validation_status.STATUS_INFO, _('{version} expires in {days} days. ').format(version=version, days=days))]

    @property
    def language(self):
        return data_validations.check_lang('article', self.article.language)

    @property
    def languages(self):
        msg = []
        for lang in self.article.trans_languages:
            msg.append(data_validations.check_lang('sub-article', lang))
        for lang in self.article.titles_by_lang.keys():
            msg.append(data_validations.check_lang('(title-group | trans-title-group)', lang))
        for lang in self.article.abstracts_by_lang.keys():
            msg.append(data_validations.check_lang('(abstract | trans-abstract)', lang))
        for lang in self.article.graphical_abstracts_by_lang.keys():
            msg.append(data_validations.check_lang('graphical abstract', lang))
        for lang in self.article.keywords_by_lang.keys():
            msg.append(data_validations.check_lang('kwd-group', lang))
        return msg

    @property
    def months_seasons(self):
        r = []
        for parent, parent_id, value in self.article.months:
            error = False
            if value.isdigit():
                if int(value) not in range(1, 13):
                    error = True
            else:
                error = True
            if error:
                msg = data_validations.invalid_value_message('month', value)
                msg += data_validations.expected_values_message(range(1, 13))
                r.append(('{parent} ({parent_id}'.format(parent=parent, parent_id=parent_id), validation_status.STATUS_FATAL_ERROR, msg))
        for parent, parent_id, value in self.article.seasons:
            error = False
            if '-' in value:
                months = value.split('-')
                month_names = article_utils.MONTHS_ABBREV
                if len(months) == 2:
                    for m in months:
                        if '|' + m + '|' in month_names:
                            month_names = month_names[month_names.find(m) + len(m):]
                        else:
                            error = True
                else:
                    error = True
            elif '|' + value + '|' in article_utils.MONTHS_ABBREV:
                error = True
            elif value.isdigit():
                error = True
            if error:
                expected = _('initial month and final month must be separated by hyphen. E.g.: Jan-Feb. Expected values for the months: {months}. ').format(months=article_utils.MONTHS_ABBREV.replace('|', ' '))
                msg = data_validations.invalid_value_message('season', value, expected)
                r.append(('{parent} ({parent_id}'.format(parent=parent, parent_id=parent_id), validation_status.STATUS_FATAL_ERROR, msg))
        return r

    @property
    def related_articles(self):
        """
        @id k
        @xlink:href i
        @ext-link-type n
        . t article
        @related-article-type
        @id k
        . t pr
        """
        r = []
        for related_article in self.article.related_articles:
            value = related_article.get('related-article-type')
            expected_values = attributes.related_articles_type
            msg = data_validations.is_expected_value('related-article/@related-article-type', value, expected_values, validation_status.STATUS_FATAL_ERROR)
            r.append(msg)
            if related_article.get('ext-link-type', '') == 'doi':
                _doi = related_article.get('href', '')
                if _doi != '':
                    valid = self.doi_validator.validate_format(_doi)
                    if not valid:
                        msg = data_validations.invalid_value_message('related-article/@xlink:href', related_article.get('href'))
                        r.append(('related-article/@xlink:href', validation_status.STATUS_FATAL_ERROR, msg + ('The content of {label} must be a DOI number. ').format(label='related-article/@xlink:href')))
        return r

    @property
    def refstats(self):
        r = []
        non_scholar_types = [k for k in self.article.refstats.keys() if k not in attributes.BIBLIOMETRICS_USE]
        sch1 = sum([t for k, t in self.article.refstats.items() if k in attributes.scholars_level1])
        sch2 = sum([t for k, t in self.article.refstats.items() if k in attributes.scholars_level2])
        total = sum(self.article.refstats.values())
        nonsch = total - sch1 - sch2
        stats = self.article.refstats
        msg = '; '.join([k + ': ' + str(stats[k]) for k in sorted(stats.keys())])
        status = validation_status.STATUS_INFO
        if total > 0:
            if (nonsch >= sch1 + sch2) or (sch1 < sch2):
                status = validation_status.STATUS_WARNING
                msg += '. ' + _('Check the value of {label}. ').format(label='element-citation/@publication-type')
        r.append((_('quantity of reference types'), status, msg))
        return r

    @property
    def refs_sources(self):
        refs = {}
        for ref_xml in self.article.references_xml:
            if ref_xml.reference.publication_type not in refs.keys():
                refs[ref_xml.reference.publication_type] = {}
            if ref_xml.reference.source not in refs[ref_xml.reference.publication_type].keys():
                refs[ref_xml.reference.publication_type][ref_xml.reference.source] = 0
            refs[ref_xml.reference.publication_type][ref_xml.reference.source] += 1
        return [(_('sources'), validation_status.STATUS_INFO, refs)]

    @property
    def ref_display_only_stats(self):
        r = []
        if self.article.display_only_stats > 0:
            r.append(('element-citation/@specific-use="display-only"', validation_status.STATUS_WARNING, self.article.display_only_stats))
        return r

    @property
    def journal_title(self):
        return data_validations.is_required_data('journal title', self.article.journal_title, validation_status.STATUS_FATAL_ERROR)

    @property
    def publisher_name(self):
        return data_validations.is_required_data('publisher name', self.article.publisher_name, validation_status.STATUS_FATAL_ERROR)

    def check_for_sps_version_number(self, number):
        if self.article.sps_version_number is not None:
            return number <= self.article.sps_version_number
        return False

    @property
    def journal_id_publisher_id(self):
        if self.check_for_sps_version_number(1.3):
            return data_validations.is_required_data('journal-id (publisher-id)', self.article.journal_id_publisher_id, validation_status.STATUS_FATAL_ERROR)

    @property
    def journal_id_nlm_ta(self):
        #FIXME
        if self.journal is not None:
            if self.journal.nlm_title is not None:
                if len(self.journal.nlm_title) > 0:
                    label = 'journal-id (nlm-ta)'
                    value = self.article.journal_id_nlm_ta
                    expected_values = [self.journal.nlm_title]
                    status = validation_status.STATUS_FATAL_ERROR
                    return data_validations.is_expected_value(label, value, expected_values, status)

    @property
    def journal_issns(self):
        _valid = []
        if self.article.journal_issns is not None:
            for k, v in self.article.journal_issns.items():
                valid = v is not None and len(v) == 9  and v[4:5] == '-'
                status = validation_status.STATUS_OK if valid else validation_status.STATUS_FATAL_ERROR
                _valid.append((k + ' ISSN', status, v))
            if len(_valid) == 0:
                _valid.append(('ISSN', validation_status.STATUS_FATAL_ERROR, _('It is required at least one {label}. ').format(label='ISSN')))
        return _valid

    @property
    def toc_section(self):
        return data_validations.is_required_data('subject', self.article.toc_section, validation_status.STATUS_FATAL_ERROR)

    @property
    def contrib(self):
        r = []
        if self.article.article_type in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC:
            if len(self.article.contrib_names) == 0 and len(self.article.contrib_collabs) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR,  _('{requirer} requires {required}. ').format(requirer=self.article.article_type, required=_('contrib names or collabs'))))
        elif self.article.article_type in attributes.AUTHORS_NOT_REQUIRED_FOR_DOCTOPIC:
            if len(self.article.contrib_names) + len(self.article.contrib_collabs) > 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR,  _('{} must not have {}. ').format(self.article.article_type, _('contrib names or collabs'))))
        for item in self.article.article_type_and_contrib_items:
            if item[0] in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC and len(item[1]) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR, _('{requirer} requires {required}. ').format(requirer=item[0], required=_('contrib names or collabs'))))
        return r

    @property
    def contrib_names(self):
        r = []
        aff_ids = [aff.id for aff in self.article.affiliations if aff.id is not None]
        for item in self.article.contrib_names:
            r.extend(ref_validations.PersonValidation(item, aff_ids).validate())
        return r

    @property
    def contrib_collabs(self):
        return [('collab', validation_status.STATUS_OK, collab.collab) for collab in self.article.contrib_collabs]

    @property
    def contrib_id(self):
        if len(self.article.contrib_names) > 0:
            return self.orcid_validator.validate_contrib_names(
                self.article.contrib_names)

    @property
    def trans_languages(self):
        return article_utils.display_values('trans languages', self.article.trans_languages)

    @property
    def article_id(self):
        if self.article.article_id is None:
            return ('article-id', validation_status.STATUS_ERROR, _('{label} is required. ').format(label=_(' or ').join(['article-id[@pub-id-type=\"doi\"]', 'article-id[@pub-id-type=\"publisher-id\"]'])))

    @property
    def doi(self):
        r = []
        level = validation_status.STATUS_WARNING
        if self.is_db_generation:
            if self.config.BLOCK_DISAGREEMENT_WITH_COLLECTION_CRITERIA:
                level = validation_status.STATUS_BLOCKING_ERROR
        if self.article.doi is None:
            r.append(('doi', level, _('article has no DOI. ')))
        else:
            r = self.doi_validator.validate(self.article)
        return r

    @property
    def doi_and_lang(self):
        r = []
        if not self.article.doi:
            return r
        doi_items = [doi for lang, doi in self.article.doi_and_lang
                     if doi != '']
        unique = set(doi_items)
        if len(unique) < len(doi_items):
            msg = '; '.join(['{}:&#160;{}'.format(lang, doi)
                            for lang, doi in self.article.doi_and_lang])
            r.append(
                ('doi',
                 validation_status.STATUS_FATAL_ERROR,
                 _('It is required a different DOI'
                   ' for each text language. ') + msg
                 ))
        return r

    @property
    def previous_article_pid(self):
        return data_validations.is_valid_value('article-id[@specific-use="previous-pid"]', self.article.previous_article_pid)

    @property
    def order(self):
        def valid(order, status):
            r = (validation_status.STATUS_OK, order)
            if order is None:
                r = (status, _('{label} is required. ').format(label='order') + data_validations.expected_values_message(_('number from 1 to 99999')))
            else:
                if order.isdigit():
                    if int(order) < 1 or int(order) > 99999:
                        r = (status, order + ': ' + _('Invalid format of {label}. ').format(label='order') + data_validations.expected_values_message(_('number from 1 to 99999')))
                else:
                    r = (status, order + ': ' + _('Invalid format of {label}. ').format(label='order') + data_validations.expected_values_message(_('number from 1 to 99999')))
            return r
        if self.is_db_generation:
            status = validation_status.STATUS_BLOCKING_ERROR
        else:
            status = validation_status.STATUS_ERROR
        status, msg = valid(self.article.order, status)
        if status != validation_status.STATUS_OK:
            return [('order', validation_status.STATUS_INFO, _('order is a 5-digits number generated from fpage or article-id (other) to compose the article PID. ')), ('order', status, msg)]

    @property
    def article_id_other(self):
        r = ('article-id[@pub-id-type="other"]', validation_status.STATUS_OK, self.article.article_id_other)
        conditions = [
                        self.article.fpage is None,
                        self.article.fpage_seq is not None,
                        self.article.fpage is not None and (
                            not self.article.fpage.isdigit() or
                            int(self.article.fpage) == 0
                            )
                        ]
        if any(conditions):
            if self.article.article_id_other is None:
                r = (
                        'article-id[@pub-id-type="other"]',
                        validation_status.STATUS_FATAL_ERROR,
                        _('{label} is required, {condition}. ').format(
                            label='article-id[@pub-id-type="other"]',
                            condition=_('if there is no first page or first page is not a number') + _(' or ') + _('more than one document starts at the same page. ')))
        return r

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return ('issue label', validation_status.STATUS_WARNING, _('Not found: {label}. ').format(label='volume, issue') + _('{item} will be considered ahead of print. ').format(item=_('issue')))
        else:
            return [self.volume, self.number]

    @property
    def volume(self):
        return data_validations.is_valid_value('volume', self.article.volume)

    @property
    def number(self):
        return data_validations.is_valid_value('number', self.article.number)

    @property
    def supplement(self):
        return data_validations.is_valid_value('supplement', self.article.supplement)

    @property
    def is_issue_press_release(self):
        return data_validations.is_valid_value('is_issue_press_release', self.article.is_issue_press_release)

    @property
    def funding_source(self):
        return article_utils.display_values('funding_source', self.article.funding_source)

    @property
    def principal_award_recipient(self):
        return article_utils.display_values('principal_award_recipient', self.article.principal_award_recipient)

    @property
    def principal_investigator(self):
        return article_utils.display_values('principal_investigator', self.article.principal_investigator)

    @property
    def funding(self):
        def has_number(content):
            numbers = 0
            if content is not None:
                content = content.replace('<', '=BREADK=<')
                content = content.replace('>', '>=BREADK=')
                content = content.replace('&#', '=BREADK=&#')
                content = content.replace('&#', ';=BREADK=')
                parts = content.split('=BREADK=')
                for part in parts:
                    if part.startswith('<') and part.endswith('>'):
                        pass
                    elif part.startswith('&#') and part.endswith(';'):
                        pass
                    else:
                        for c in part:
                            if c.isdigit():
                                numbers += 1
            return numbers

        r = []
        if self.article.award_id is None:
            found = has_number(self.article.ack_xml)
            if found > 4:
                r.append(('award-id', validation_status.STATUS_ERROR, _('Found {items} in {element}. ').format(items=_('numbers'), element='ack'), self.article.ack_xml))
            found = has_number(self.article.financial_disclosure)
            if found > 4:
                r.append(('award-id', validation_status.STATUS_ERROR, _('Found {items} in {element}. ').format(items=_('numbers'), element='fn[@fn-type="financial-disclosure"]'), self.article.fn_financial_disclosure))
        else:
            for item in self.article.award_id:
                r.append(('award-id', validation_status.STATUS_OK, item))
        return r

    @property
    def award_id(self):
        return article_utils.display_values('award-id', self.article.award_id)

    @property
    def funding_statement(self):
        return article_utils.display_values('funding statement', self.article.funding_statement)

    @property
    def ack_xml(self):
        return data_validations.is_valid_value('ack xml', self.article.ack_xml)

    @property
    def pagination(self):
        pages = [self.article.fpage, self.article.elocation_id]
        labels = ['fpage', 'elocation-id']
        status = validation_status.STATUS_OK
        label = 'fpage | elocation-id'
        msg = ' | '.join(['{}: {}'.format(l, p) for l, p in zip(labels, pages) if p is not None])
        if self.article.is_ahead:
            if any(pages):
                status = validation_status.STATUS_FATAL_ERROR
                msg = _('It is an ahead of print article and it must not have fpage neither elocation-id ({}). '.format(msg))
            return (label, status, msg)
        if all(pages) is True:
            status = validation_status.STATUS_ERROR
            msg = _('Remove elocation-id. Use only fpage and lpage ({}). '.format(msg))
            return (label, status, msg)
        elif any(pages) is False:
            status = validation_status.STATUS_FATAL_ERROR
            msg = _('Required fpage or elocation-id. ')
            return (label, status, msg)
        return (label, status, msg)

    @property
    def affiliations(self):
        r = []
        xref_items = []
        for item in self.article.contrib_names:
            xref_items.extend(item.xref)
        for aff_xml in self.article.affiliations:
            normalized = None
            if self.article.institutions_query_results is not None:
                normalized = self.article.institutions_query_results.get(aff_xml.id)
            aff_validator = AffValidator(aff_xml, normalized, xref_items)
            r.extend(aff_validator.validations)
        return r

    @property
    def clinical_trial_url(self):
        return data_validations.is_valid_value('clinical trial url', self.article.clinical_trial_url)

    @property
    def clinical_trial_text(self):
        return data_validations.is_valid_value('clinical trial text', self.article.clinical_trial_text)

    def _total(self, total, count, label_total, label_count):
        r = []
        if total is not None and count is not None:
            if total < 0:
                msg = data_validations.invalid_value_result(label_total, total, _('numbers greater or equal to 0'), validation_status.STATUS_FATAL_ERROR)
                r.append(msg)
            if count.isdigit():
                if total != int(count):
                    r.append((u'{} ({}) x {} ({})'.format(label_count, count, label_total, total), validation_status.STATUS_ERROR, _('{label1} and {label2} must have the same value. ').format(label1=label_count, label2=label_total)))
            else:
                msg = data_validations.invalid_value_result(label_count, count, _('numbers greater or equal to 0'), validation_status.STATUS_FATAL_ERROR)
                r.append(msg)
        elif total is None and count is not None:
            # total is None: unable to calculate
            pass
        elif total is None and count is None:
            # total is None: unable to calculate
            r.append((label_count, validation_status.STATUS_WARNING, _('{} is absent. ').format(label_count)))
        else:
            # count is None
            r.append((label_count, validation_status.STATUS_INFO, u'{}={} '.format(label_count, count)))
            r.append((label_total, validation_status.STATUS_INFO, u'{}={} '.format(label_total, total)))
        return r

    def old_total(self, total, count, label_total, label_count):
        r = []
        if total < 0:
            msg = data_validations.invalid_value_result(label_total, total, _('numbers greater or equal to 0'), validation_status.STATUS_FATAL_ERROR)
            r.append(msg)
        elif count is not None:
            if count.isdigit():
                if total != int(count):
                    r.append((u'{label_count} ({count}) x {label_total} ({total})'.format(label_count=label_count, count=count, label_total=label_total, total=total), validation_status.STATUS_ERROR, _('{label1} and {label2} must have the same value. ').format(label1=label_count, label2=label_total)))
            else:
                msg = data_validations.invalid_value_result(label_count, count, _('numbers greater or equal to 0'), validation_status.STATUS_FATAL_ERROR)
                r.append(msg)
        return r

    @property
    def total_of_pages(self):
        if self.article.elocation_id and self.article.page_count:
            return [(_('page-count'), validation_status.STATUS_ERROR, _('Electronic-only works do not traditionally have page counts. '))]
        if self.article.total_of_pages is None and self.article.page_count is None:
            pass
        else:
            return self._total(self.article.total_of_pages, self.article.page_count, _('total of pages'), 'page-count')

    @property
    def total_of_references(self):
        r = []
        r.append(self._total(self.article.total_of_references, self.article.ref_count, _('total of references'), 'ref-count'))
        if self.article.article_type in attributes.REFS_REQUIRED_FOR_DOCTOPIC:
            if self.article.total_of_references == 0:
                if self.article.is_provisional:
                    return r
                r.append((_('total of references'), validation_status.STATUS_FATAL_ERROR, _('{requirer} requires {required}. ').format(requirer=self.article.article_type, required=_('references'))))
        return r

    @property
    def total_of_tables(self):
        return self._total(self.article.total_of_tables, self.article.table_count, _('total of tables'), 'table-count')

    @property
    def total_of_equations(self):
        return self._total(self.article.total_of_equations, self.article.equation_count, _('total of equations'), 'equation-count')

    @property
    def total_of_figures(self):
        return self._total(self.article.total_of_figures, self.article.fig_count, _('total of figures'), 'fig-count')

    def titles_by_lang(self, lang, err_level):
        valid = []
        errors = []
        sorted_by_lang = self.article.titles_by_lang.get(lang)
        values = []

        label_title = _(' or ').join(['article-title', 'trans-title (@xml:lang="' + lang + '")'])
        label_xml_lang = _(' or ').join(['title-group/@xml:lang', 'trans-title-group/@xml:lang'])
        label_title_group = _(' or ').join(['title-group', 'trans-title-group[@xml:lang="' + lang + '"]'])
        if sorted_by_lang is not None:
            if len(sorted_by_lang) > 0:
                values = [item.title for item in sorted_by_lang]
        if all(values) is True:
            if lang is None:
                errors.append(data_validations.invalid_value_result(label_xml_lang, _('None'), _('None'), ' | '.join(values)))
            else:
                valid.append((label_xml_lang, validation_status.STATUS_INFO, ' | '.join(values)))
        else:
            label = label_title_group if sorted_by_lang is None else label_title
            errors.append((label, err_level, _('Not found: {label}. ').format(label=label)))
        if len(values) > 1:
            errors.append((label_title, validation_status.STATUS_FATAL_ERROR, _('Required only one {item} for each language. Values found for @xml:lang="{lang}": {values}. ').format(item='article-title' + _(' or ') + 'trans-title', values=' | '.join(values), lang=lang)))
        return (values, valid, errors)

    def texts_by_lang(self, lang, err_level, elem_group_name, elem_item_name, text_elements, mininum=0):
        valid = []
        errors = []
        sorted_by_lang = text_elements.get(lang)
        values = []
        if sorted_by_lang is not None:
            if len(sorted_by_lang) > 0:
                values = [item.text for item in sorted_by_lang]
        elem_name = elem_item_name if elem_group_name is None else elem_group_name

        label_lang = elem_name + '/@xml:lang'
        label_elem = elem_name + ' (@xml:lang="' + lang + '")'
        if all(values) is True:
            if lang is None:
                errors.append(
                    data_validations.invalid_value_result(label_lang, _('None'), ' | '.join(values), err_level))
            else:
                valid.append((label_elem, validation_status.STATUS_INFO, ' | '.join(values)))
                if mininum > 0:
                    if 1 < len(values) < mininum:
                        errors.append((label_elem, err_level, _('Required at least {quantity} items. ').format(quantity=mininum)))
        else:
            if sorted_by_lang is None:
                if elem_group_name is not None:
                    elem_name = elem_group_name
            res = [item for item in values if item is not None]
            if len(res) == 0:
                res = _('not found')
            else:
                res = {_('found'): res}
            errors.append((label_elem, err_level, res))
        if mininum == 0:
            if len(values) > 1:
                errors.append((elem_item_name + ' (@xml:lang="' + lang + '")', validation_status.STATUS_FATAL_ERROR, _('Required only one {item} for each language. Values found for @xml:lang="{lang}": {values}. ').format(lang=lang, item=elem_item_name, values=str(len(values)))))
        else:
            if len(values) != len(list(set(values))):
                duplicated = {}
                for value in values:
                    if value not in duplicated.keys():
                        duplicated[value] = 0
                    duplicated[value] += 1
                errors.append((elem_item_name, validation_status.STATUS_FATAL_ERROR, _('Required only unique values of {label} for each language. Found duplicated values for @xml:lang="{lang}": {values}. ').format(lang=lang, label=elem_item_name, values=' | '.join([k for k, c in duplicated.items() if c > 1]))))
        return (values, valid, errors)

    @property
    def titles_abstracts_keywords(self):
        r = []
        for lang in sorted(self.article.title_abstract_kwd_languages):
            err_level = validation_status.STATUS_ERROR if lang != self.article.language else validation_status.STATUS_FATAL_ERROR
            titles, valid, errors = self.titles_by_lang(lang, err_level)

            abstracts, _valid, _errors = self.texts_by_lang(lang, err_level, None, 'abstract', self.article.abstracts_by_lang)
            valid += _valid
            errors += _errors

            graphical_abstracts, _valid, _errors = self.texts_by_lang(lang, err_level, None, 'graphical abstract', self.article.graphical_abstracts_by_lang)
            valid += _valid
            errors += _errors

            keywords, _valid, _errors = self.texts_by_lang(lang, err_level, 'kwd-group', 'kwd', self.article.keywords_by_lang, mininum=2)
            valid += _valid
            errors += _errors

            article_type = '"@article-type=' + self.article.article_type + '"'
            if self.article.article_type in attributes.ABSTRACT_REQUIRED_FOR_DOCTOPIC:
                if len(abstracts) == 0 or len(keywords) == 0:
                    errors.append(('abstract + kwd-group', validation_status.STATUS_ERROR, _('Expected {expected} for {demander}. Be sure that "{demander}" is correct. ').format(expected='abstract + kwd-group', demander=article_type)))
            elif self.article.article_type in attributes.ABSTRACT_UNEXPECTED_FOR_DOCTOPIC:
                if len(abstracts) > 0 or len(keywords) > 0:
                    errors.append(('abstract + kwd-group', validation_status.STATUS_ERROR, _('Unexpected {unexpected} for {demander}. Be sure that {demander} is correct. ').format(unexpected='abstract + kwd-group', demander=article_type)))

            if len(errors) > 0:
                if len(valid) > 0:
                    for item in valid:
                        r.append(item)
                for item in errors:
                    r.append(item)
        return r

    @property
    def history(self):
        received = self.article.received_dateiso
        accepted = self.article.accepted_dateiso
        r = []
        error_level = validation_status.STATUS_FATAL_ERROR if self.article.article_type in attributes.HISTORY_REQUIRED_FOR_DOCTOPIC else validation_status.STATUS_INFO
        if received is not None and accepted is not None:
            errors = []
            errors.extend(article_utils.is_fulldate('received', received))
            errors.extend(article_utils.is_fulldate('accepted', accepted))
            if len(errors) > 0:
                r.append(('history', validation_status.STATUS_FATAL_ERROR, '\n'.join(errors)))
            else:
                dates = []
                if received > accepted:
                    dates.append(('received: {value}'.format(value=received),
                                  'accepted: {value}'.format(value=accepted)))
                if self.article.real_pubdate:
                    real_pubdate = article_utils.format_dateiso(
                        self.article.real_pubdate)
                    if real_pubdate < received:
                        dates.append(
                            ('received: {value}'.format(value=received),
                             'pub-date: {value}'.format(value=real_pubdate)))
                    if real_pubdate < accepted:
                        dates.append(
                            ('accepted: {value}'.format(value=accepted),
                             'pub-date: {value}'.format(value=real_pubdate)))

                if len(dates) > 0:
                    for date in dates:
                        r.append(('history', validation_status.STATUS_FATAL_ERROR, _('{date1} must be before {date2}. ').format(date1=date[0], date2=date[1])))

        elif received is None and accepted is None:
            r = [('history', error_level, _('Not found: {label}. ').format(label='history'))]
        else:
            if received is None:
                r.append(data_validations.is_required_data('history: received', received, error_level))
            if accepted is None:
                r.append(data_validations.is_required_data('history: accepted', accepted, error_level))

        return r

    @property
    def received(self):
        return data_validations.display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return data_validations.display_attributes('accepted', self.article.accepted)

    @property
    def innerbody_elements_permissions(self):
        r = []
        status = validation_status.STATUS_WARNING if self.check_for_sps_version_number(1.4) else validation_status.STATUS_INFO
        if len(self.article.permissions_required) > 0:
            l = [elem_id for elem_id, missing_children in self.article.permissions_required]
            if len(l) > 0:
                r.append(('permissions', status, {_('It is highly recommended identifying {elem}, if applicable. ').format(elem=', '.join(attributes.PERMISSION_ELEMENTS)): l}))
        return r

    @property
    def article_permissions(self):
        text_languages = sorted(list(set(self.article.trans_languages + [self.article.language] + ['en'])))
        r = []

        if  self.check_for_sps_version_number(1.4):
            for cp_elem in ['statement', 'year', 'holder']:
                if self.article.article_copyright.get(cp_elem) is None:
                    r.append(('copyright-' + cp_elem, validation_status.STATUS_WARNING, _('It is highly recommended identifying {elem}. ').format(elem='copyright-' + cp_elem)))
        for lang, license in self.article.article_licenses.items():

            if lang is None:
                if self.check_for_sps_version_number(1.4):
                    r.append(('license/@xml:lang', validation_status.STATUS_ERROR, _('{label} is required. ').format(label='license/@xml:lang')))
            elif lang not in text_languages:
                r.append(('license/@xml:lang', validation_status.STATUS_ERROR, _('{value} is an invalid value for {label}. ').format(value=lang, label='license/@xml:lang') + _('The license text must be written in {langs}. ').format(langs=_(' or ').join(attributes.translate_code_languages(text_languages))) + _('Expected values for {label}: {expected}. ').format(label='xml:lang', expected=_(' or ').join(text_languages)), license['xml']))
            result = attributes.validate_license_href(license.get('href'))
            if result is not None:
                r.append(result)
            r.append(data_validations.is_expected_value('license/@license-type', license.get('type'), ['open-access'], validation_status.STATUS_FATAL_ERROR))
            r.append(data_validations.is_required_data('license/license-p', license.get('text'), validation_status.STATUS_FATAL_ERROR))

            r.extend(self.check_license_text(license, lang))

        return [item for item in r if r is not None]

    def check_license_text(self, license, lang):
        r = []
        text = license.get('text', '')
        if text:
            code = license.get('code-and-version', '').split('/')
            if code:
                code = code[0]
                code_parts = code.split('-')
                expected = attributes.LICENSE_TEXTS.get(lang)
                if code == 'by' and 'mercial' in text:
                    r += [
                            ('license/license-p',
                             validation_status.STATUS_ERROR,
                             _('The license text ({}) and code ({}) are inconsistent. ').format(license['text'], code),
                             )
                        ]
                if (not utils.compare_text(text, expected) or
                        code_parts[0] != 'by' or 'nc' in code_parts):
                    r += [
                            ('license/license-p',
                             validation_status.STATUS_WARNING,
                             license,
                             )
                        ]
        return r

    @property
    def references(self):
        r = []
        article_year = (
            self.article.real_pubdate or self.article.expected_pubdate or {}).get(
                'year')
        year = ('published', article_year)
        if article_year is None:
            year = ('today', datetime.now().isoformat()[0:4])
        previous_refxml = None
        for ref_xml in self.article.references_xml:
            r.append((ref_xml.reference, ref_validations.ReferenceContentValidation(ref_xml, previous_refxml).evaluate(year)))
            previous_refxml = ref_xml
        return r

    @property
    def press_release_id(self):
        return data_validations.is_valid_value(_('press release id'), self.article.press_release_id)

    @property
    def article_date_types(self):
        r = []
        dt = []
        for fmt, date_type, pub_type, xml in self.article.raw_pubdate_items:
            if date_type in dt or pub_type in dt:
                r.append(
                    ('pub-date',
                     validation_status.STATUS_BLOCKING_ERROR,
                     _('"pub-date" ({}) is duplicated. ').format(
                        date_type or pub_type),
                     xml
                     )
                )
            if date_type is not None:
                dt.append(date_type)
            if pub_type is not None:
                dt.append(pub_type)

        if self.article.sps_version_number > 1.8:
            for fmt, date_type, pub_type, xml in self.article.raw_pubdate_items:
                if fmt is None:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@publication-format is required. '),
                         xml
                         )
                    )
                if pub_type:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@pub-type is invalid for this version of SPS. '),
                         xml)
                    )
                if date_type == 'pub':
                    if fmt != 'electronic':
                        r.append(
                            ('pub-date',
                             validation_status.STATUS_BLOCKING_ERROR,
                             _('@publication-format must be electronic. '),
                             xml)
                        )
                elif date_type == 'collection':
                    pass
                else:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@date-type must be pub or collection. '),
                         xml)
                    )
        elif self.article.sps_version_number == 1.8:
            for fmt, date_type, pub_type, xml in self.article.raw_pubdate_items:
                if date_type:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@date-type is invalid for this version of SPS. '),
                         xml)
                    )
                if fmt:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@publication-format is invalid for this version of SPS. '),
                         xml)
                    )
                if pub_type not in ['epub', 'collection']:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@pub-type must be epub or collection. '),
                         xml)
                    )
        else:
            for fmt, date_type, pub_type, xml in self.article.raw_pubdate_items:
                if date_type:
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('@date-type is invalid for this version of SPS. '),
                         xml)
                    )
        if self.article.sps_version_number > 1.8:
            if self.article.is_ahead:
                expected = [{'pub'}]
                expected_items = 'pub'
            else:
                expected = [{'pub', 'collection'}]
                expected_items = 'pub|collection'
        elif self.article.sps_version_number == 1.8:
            if self.article.is_ahead:
                expected = [{'epub'}]
                expected_items = 'epub'
            else:
                expected = [{'epub', 'collection'}]
                expected_items = 'epub|collection'
        else:
            expected = [{'epub-ppub'}, {'epub', 'collection'}, {'epub'}]
            expected_items = "'epub-ppub', 'epub', 'collection', 'epub'"
        date_types = {
              label
              for label, value in self.article.labeled_xml_dates
              if value
            }
        c = ' | '.join(list(date_types))
        if date_types in expected:
            r.append(('pub-date', validation_status.STATUS_OK, c))
        else:
            r.append(('pub-date', validation_status.STATUS_BLOCKING_ERROR,
                     _('Invalid combination of date types: ') + c + '. ' +
                     data_validations.expected_values_message(expected_items)))
        for label, value in self.article.labeled_xml_dates:
            if value:
                dateiso = article_utils.format_dateiso(value)
                if label in ['epub', 'pub']:
                    if value.get('year') is None or \
                       value.get('month') is None or \
                       value.get('day') is None or value.get('season'):
                        r.append(
                            ('pub-date',
                             validation_status.STATUS_BLOCKING_ERROR,
                             _('"{}" ({}) must have year, month and day').format(
                                label, dateiso))
                        )
                elif value.get('year') is None or value.get('day'):
                    r.append(
                        ('pub-date',
                         validation_status.STATUS_BLOCKING_ERROR,
                         _('"{}"  ({}) must have year; can have month or season,'
                           ' but no day').format(label, dateiso))
                    )
        return r

    @property
    def expected_pubdate(self):
        return data_validations.required_one(_('editorial pub-date'), self.article.expected_pubdate)

    @property
    def real_pubdate(self):
        return data_validations.display_attributes(_('SciELO pub-date'), self.article.real_pubdate)

    @property
    def is_ahead(self):
        return data_validations.is_valid_value(_('is aop'), self.article.is_ahead)

    @property
    def is_article_press_release(self):
        return data_validations.is_valid_value(_('is press_release'), self.article.is_article_press_release)

    @property
    def illustrative_materials(self):
        return article_utils.display_values(_('illustrative materials'), self.article.illustrative_materials)

    @property
    def is_text(self):
        return data_validations.is_valid_value(_('is text'), self.article.is_text)

    @property
    def previous_pid(self):
        return data_validations.is_valid_value(_('previous pid'), self.article.previous_pid)

    @property
    def validate_xref_reftype(self):
        message = []

        id_and_elem_name = {node.attrib.get('id'): node.tag for node in self.article.elements_which_has_id_attribute if node.attrib.get('id') is not None}

        for xref in self.article.xref_nodes:
            if xref['rid'] is None:
                message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='@rid'), xref['xml']))
            if xref['ref-type'] is None:
                message.append(('xref/@ref-type', validation_status.STATUS_ERROR, _('{label} is required. ').format(label='@ref-type'), xref['xml']))
            if xref['rid'] is not None and xref['ref-type'] is not None:
                elements = attributes.REFTYPE_AND_TAG_ITEMS.get(xref['ref-type'])
                tag = id_and_elem_name.get(xref['rid'])
                if tag is None:
                    message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label=xref['ref-type'] + '[@id=' + xref['rid'] + ']'), xref['xml']))
                elif elements is None:
                    # no need to validate
                    valid = True
                elif tag in elements:
                    valid = True
                elif tag not in elements:
                    reftypes = [reftype for reftype, _elements in attributes.REFTYPE_AND_TAG_ITEMS.items() if tag in _elements]

                    _msg = _('Unmatched {value} and {label}: {value1} is valid for {label1}, and {value2} is valid for {label2}').format(
                        value='@ref-type (' + xref['ref-type'] + ')',
                        label=tag,
                        value1='xref[@ref-type="' + xref['ref-type'] + '"]',
                        label1=' | '.join(elements),
                        value2='|'.join(reftypes),
                        label2=tag + '/@ref-type'
                        )
                    #_msg = _('Unmatched')
                    #_msg += ' @ref-type (' + xref['ref-type'] + ')'
                    #_msg += _(' and ') + tag + ': '
                    #_msg += 'xref[@ref-type="' + xref['ref-type'] + '"] '
                    #_msg += _('is for') + ' ' + ' | '.join(elements)
                    #_msg += _(' and ') + _('valid values of') + ' @ref-type ' + _('of') + ' '
                    #_msg += tag + ' ' + _('are') + ' '
                    #_msg += '|'.join(reftypes)

                    message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, _msg))
        return message

    @property
    def sections(self):
        expected_values = ['cases', 'conclusions', 'discussion', 'intro', 'materials', 'methods', 'results', 'supplementary-material']
        r = []
        for body in self.article.article_sections:
            for label, sections in body.items():
                for sectype, sectitle in sections:
                    if sectype == '':
                        msg = _('Not found: {label} for {item}. ').format(item=sectitle, label='@sec-type') + data_validations.expected_values_message(_(' and/or ').join(expected_values))
                        r.append((label + '/sec/@sec-type',
                                  validation_status.STATUS_WARNING,
                                  msg))
                    elif sectype not in expected_values:
                        invalid = None
                        if '|' in sectype:
                            invalid = [sec for sec in sectype.split('|') if sec not in expected_values]
                        else:
                            invalid = sectype
                        if invalid is not None:
                            if len(invalid) > 0:
                                msg = data_validations.invalid_value_result(label + '/sec/@sec-type', sectype, _(' and/or ').join(expected_values), validation_status.STATUS_FATAL_ERROR)
                                r.append(msg)
        return r

    @property
    def paragraphs(self):
        invalid_items = self.article.paragraphs_startswith(':')
        if len(invalid_items) > 0:
            return [('paragraph',
                validation_status.STATUS_ERROR,
                {_('{value} starts with invalid characters: {invalid_chars}. ').format(value=_('paragraphs'), invalid_chars=':'): invalid_items})]

    @property
    def missing_xref_list(self):
        tag_and_xref_types = {
            'fig-group': 'fig',
            'table-wrap-group': 'table',
            'fig': 'fig',
            'table-wrap': 'table'
            }
        if len(self.article.references_xml) > 0:
            tag_and_xref_types['ref'] = 'bibr'
        message = []
        missing = {}
        for node in self.article.elements_which_has_id_attribute:
            xref_type = tag_and_xref_types.get(node.tag)
            if xref_type is not None:
                _id = node.attrib.get('id')
                xref_nodes = [item for item in self.article.xref_nodes if item['rid'] == _id]
                if len(xref_nodes) == 0:
                    if xref_type not in missing.keys():
                        missing[xref_type] = []
                    missing[xref_type].append(_id)
                else:
                    for item in xref_nodes:
                        msg = data_validations.is_expected_value('xref[@rid="' + str(item['rid']) + '"]/@ref-type', str(item['ref-type']), [str(xref_type)],validation_status.STATUS_FATAL_ERROR)
                        message.append(msg)
        for xref_type, missing_xref_type_items in missing.items():
            if self.article.any_xref_ranges.get(xref_type) is None:
                encoding.debugging('missing_xref_list()', xref_type + ' has no xref ranges')
            else:
                missing_xref_type_items = confirm_missing_xref_items(missing_xref_type_items, self.article.any_xref_ranges.get(xref_type))

            if len(missing_xref_type_items) > 0:
                for xref in missing_xref_type_items:
                    message.append(('xref[@ref-type=' + xref_type + ']', validation_status.STATUS_ERROR, 
                        _('Not found: {label}. ').format(label='xref[@ref-type="{xreftype}" and rid="{rid}"]'.format(xreftype=xref_type, rid=xref))))
            if self.article.any_xref_ranges.get(xref_type) is not None:
                for start, end, start_node, end_node in self.article.any_xref_ranges.get(xref_type):
                    if start > end:
                        message.append(
                                (
                                _('xref range'),
                                validation_status.STATUS_ERROR,
                                _('Invalid range ')+
                                '{}-{} ({}-{})'.format(
                                    start_node.text,
                                    end_node.text,
                                    start_node.attrib.get('rid'),
                                    end_node.attrib.get('rid'))
                                )
                            )
        return message

    @property
    def missing_bibr_xref(self):
        missing = []
        invalid_reftype = []
        for ref_xml in self.article.references_xml:
            if ref_xml.reference.id is not None:
                found = [item for item in self.article.xref_nodes if item['rid'] == ref_xml.reference.id]
                for item in found:
                    if item['ref-type'] != 'bibr':
                        invalid_reftype.append(item)
                if len(found) == 0:
                    missing.append(ref_xml.reference.id)
        message = []
        if len(invalid_reftype) > 0:
            msg = data_validations.is_expected_value('xref[@ref-type=bibr]', item['ref-type'], ['bibr'], validation_status.STATUS_FATAL_ERROR)
            message.append(msg)

        if len(missing) > 0:
            missing = confirm_missing_xref_items(missing, self.article.bibr_xref_ranges)

            if len(missing) > 0:
                for xref in missing:
                    message.append(('xref[@ref-type=bibr]', validation_status.STATUS_ERROR, _('Not found {label} in the {item}. ').format(label='xref[@ref-type=bibr]', item=xref)))

        if self.article.is_bibr_xref_number:
            for start, end, start_node, end_node in self.article.bibr_xref_ranges:
                if start > end:
                    items = []
                    items.append(('@rid', start_node.attrib.get('rid')))
                    items.append(('xref', start_node.text))
                    items.append(('@rid', end_node.attrib.get('rid')))
                    items.append(('xref', end_node.text))
                    message.append(('xref', validation_status.STATUS_ERROR, data_validations.invalid_labels_and_values(items)))
            for bibr_xref in self.article.bibr_xref_nodes:
                rid = bibr_xref.attrib.get('rid')
                if rid is not None and bibr_xref.text is not None:
                    if rid[1:] not in bibr_xref.text and bibr_xref.text.replace('(', '').replace(')', '') not in rid:
                        items = []
                        items.append(('@rid', rid))
                        items.append(('xref', bibr_xref.text))
                        message.append(('xref', validation_status.STATUS_ERROR, data_validations.invalid_labels_and_values(items)))
        return message

    @property
    def xref_rid_and_text(self):
        message = []
        for xref_node in self.article.xref_nodes:
            rid = xref_node['rid']
            if rid is not None and xref_node['xml'] is not None:
                if rid[1:] not in xref_node['xml']:
                    items = []
                    items.append(('@rid', rid))
                    items.append(('xref', xref_node['xml']))
                    message.append(('xref', validation_status.STATUS_WARNING, data_validations.invalid_labels_and_values(items)))
        return message

    @property
    def svg(self):
        messages = []
        for href in self.article.hrefs:
            if href.is_internal_file and href.src.endswith('.svg'):
                try:
                    if '<image' in fs_utils.read_file(os.path.join(self.pkgfiles.path, href.src)):
                        messages.append(('svg', validation_status.STATUS_ERROR, _(u'Invalid SVG file: {} contains embedded images. ').format(href.src)))
                except:
                    pass
        return messages

    @property
    def graphics_min_and_max_height(self):
        min_inline, max_inline = utils.valid_formula_min_max_height(self.article.inline_graphics_heights(self.pkgfiles.path))
        min_disp, max_disp = utils.valid_formula_min_max_height(self.article.disp_formulas_heights(self.pkgfiles.path), 0.3)
        if min_disp < min_inline:
            min_disp = min_inline
        if max_disp < max_inline:
            max_disp = max_inline
        return min_disp, max_disp, min_inline, max_inline

    def graphic_min_and_max_height(self, hrefitem, min_disp, max_disp, min_inline, max_inline):
        min_height = None
        max_height = None
        if hrefitem in self.article.inline_graphics:
            min_height = min_inline
            max_height = max_inline
        elif hrefitem in self.article.disp_formulas:
            min_height = min_disp
            max_height = max_disp
        return min_height, max_height

    @property
    def href_list(self):
        href_items = {}
        min_disp, max_disp, min_inline, max_inline = self.graphics_min_and_max_height
        for hrefitem in self.article.hrefs:
            href_validations = HRefValidation(self.app_institutions_manager.ws.ws_requester, hrefitem, self.check_url, self.pkgfiles, min_disp, max_disp, min_inline, max_inline)
            href_items[hrefitem.src] = {
                'display': href_validations.display,
                'elem': hrefitem,
                'results': href_validations.validate()}
        return href_items

    @property
    def href_files(self):
        href_items = {}
        min_disp, max_disp, min_inline, max_inline = self.graphics_min_and_max_height
        for hrefitem in self.article.href_files:
            href_validations = HRefValidation(self.app_institutions_manager.ws.ws_requester, hrefitem, self.check_url, self.pkgfiles, min_disp, max_disp, min_inline, max_inline)
            href_items[hrefitem.src] = {
                'display': href_validations.display,
                'elem': hrefitem,
                'results': href_validations.validate()}
        return href_items

    @property
    def package_files(self):
        _pkg_files = {}
        for lang, f in self.article.expected_pdf_files.items():
            if f not in _pkg_files.keys():
                _pkg_files[f] = []
            msg = _('Expected PDF file which content in "{lang}". ').format(lang=_(attributes.LANGUAGES.get(lang)))
            if f not in self.pkgfiles.related_files:
                _pkg_files[f].append((validation_status.STATUS_ERROR, msg + _('Not found {label} in the {item}. ').format(label=f, item=_('package'))))

        #from files, find in XML
        href_items_in_xml = [item.name_without_extension for item in self.article.href_files]
        href_items_in_xml += [item.src for item in self.article.href_files]
        href_items_in_xml = list(set(href_items_in_xml))
        for f in self.pkgfiles.related_files:
            if f not in self.article.expected_pdf_files.values():
                name, ext = os.path.splitext(f)
                if f not in _pkg_files.keys():
                    _pkg_files[f] = []
                _pkg_files[f].append((validation_status.STATUS_INFO, _('Found {label} in the {item}. ').format(label=f, item=_('package'))))

                status = validation_status.STATUS_INFO
                message = None
                if f in href_items_in_xml or name in href_items_in_xml:
                    message = _('Found {label} in the {item}. ').format(label='xlink:href="{}"'.format(f), item=self.pkgfiles.basename)
                else:
                    message = _('Not found {label} in the {item}. ').format(label='xlink:href="{}"'.format(f), item=self.pkgfiles.basename)
                    status = validation_status.STATUS_ERROR

                if message is not None:
                    _pkg_files[f].append((status, message))
        items = []
        for name in sorted(_pkg_files.keys()):
            messages = {}
            for status, message_list in _pkg_files[name]:
                if status not in messages.keys():
                    messages[status] = []
                messages[status].append(message_list)
            for status, message_list in messages.items():
                items.append((name, status, message_list))
        return items


class HRefValidation(object):

    def __init__(self, ws_requester, hrefitem, check_url, pkgfiles, min_disp=None, max_disp=None, min_inline=None, max_inline=None):
        self.pkgfiles = pkgfiles
        self.hrefitem = hrefitem
        self.check_url = check_url
        self.name, self.ext = os.path.splitext(self.hrefitem.src)
        self.min_max_height(min_disp, max_disp, min_inline, max_inline)
        self.ws_requester = ws_requester

    def min_max_height(self, min_disp, max_disp, min_inline, max_inline):
        self.min_height = None
        self.max_height = None
        if self.hrefitem.is_inline:
            self.min_height = min_inline
            self.max_height = max_inline
        elif self.hrefitem.is_disp_formula:
            self.min_height = min_disp
            self.max_height = max_disp

    def validate(self):
        status_message = []
        if self.hrefitem.is_internal_file:
            status_message.extend(self.validate_href_file)
            if self.hrefitem.is_image:
                status_message.extend(self.validate_tiff_image)
            status_message = [item for item in status_message if item is not None]
        else:
            if self.check_url or 'scielo.php' in self.hrefitem.src:
                if self.ws_requester.is_valid_url(self.hrefitem.src) is False:
                    message = data_validations.invalid_value_message('URL', self.hrefitem.src)
                    if 'scielo.php' in self.hrefitem.src:
                        message += _('Be sure that there is no missing character such as _. ')
                    status_message.append((validation_status.STATUS_WARNING, self.hrefitem.src + message))        
        if len(status_message) == 0:
            status_message.append((validation_status.STATUS_INFO, ''))
        return status_message

    @property
    def validate_href_file(self):
        result = []
        name, ext = os.path.splitext(self.hrefitem.src)
        if self.hrefitem.src not in self.pkgfiles.related_files:
            if name not in self.pkgfiles.related_files_by_name.keys():
                result.append((validation_status.STATUS_BLOCKING_ERROR, _('Not found {label} in the {item}. ').format(label=self.hrefitem.src, item=_('package'))))
        if '.' not in self.hrefitem.src:
            result.append((validation_status.STATUS_WARNING, _('missing extension of ') + self.hrefitem.src + '.'))
        return result

    @property
    def validate_tiff_image(self):
        for name in [self.name+'.tif', self.name+'.tiff']:
            if name in self.pkgfiles.tiff_items:
                return img_utils.evaluate_tiff(
                    os.path.join(self.pkgfiles.path, name), self.min_height, self.max_height)
        return []

    @property
    def display(self):
        location = self.hrefitem.src
        if self.hrefitem.is_internal_file:
            location = self.hrefitem.file_location(self.pkgfiles.path)
        if self.hrefitem.is_image:
            return html_reports.thumb_image(
                location.replace(self.pkgfiles.path, '{IMG_PATH}/'))
        else:
            return html_reports.link(
                location.replace(
                    self.pkgfiles.path, '{PDF_PATH}/'), self.hrefitem.src)
