# coding=utf-8

import os
from datetime import datetime
import re

from __init__ import _
import validation_status
import attributes
import article_utils
import xml_utils
import utils
import article
import html_reports
from serial_files import filename_language_suffix
import ws_requester


MIN_IMG_DPI = 300
MIN_IMG_WIDTH = 789
MAX_IMG_WIDTH = 2250
MAX_IMG_HEIGHT = 2625


class DOI_Services(object):

    def __init__(self):
        self.doi_data_items = {}
        self.doi_journal_prefixes = {}

    def get_doi_data(self, doi):
        doi_data = self.doi_data_items.get(doi)
        if doi_data is None:
            url = ws_requester.wsr.article_doi_checker_url(doi)
            article_json = ws_requester.wsr.json_result_request(url)
            if article_json is not None:
                data = article_json.get('message')
                if data is not None:
                    doi_data = DOI_Data(doi)
                    doi_data.journal_titles = data.get('container-title')
                    doi_data.article_titles = data.get('title')
                    doi_data.pid = data.get('alternative-id')
                    if doi_data.pid is not None:
                        doi_data.pid = doi_data.pid[0]
        if doi_data is not None:
            self.doi_data_items[doi] = doi_data
        return doi_data

    def doi_journal_prefix(self, issn, year):
        prefix = self.doi_journal_prefixes.get(issn)
        if prefix is None:
            url = ws_requester.wsr.journal_doi_prefix_url(issn, year)
            json_results = ws_requester.wsr.json_result_request(url)
            if json_results is not None:
                items = json_results.get('message', {}).get('items')
                if items is not None:
                    if len(items) > 0:
                        prefix = items[0].get('prefix')
                        if prefix is not None:
                            if '/prefix/' in prefix:
                                prefix = prefix[prefix.find('/prefix/')+len('/prefix/'):]
        if prefix is not None:
            self.doi_journal_prefixes[issn] = prefix
        return prefix


class ArticleDOIValidator(object):

    def __init__(self, doi_services, article):
        self.article = article
        self.doi_data = doi_services.get_doi_data(article.doi)
        if self.doi_data is None and article.doi is not None:
            self.doi_data = DOI_Data(article.doi)
        self.journal_doi_prefix_items = [doi_services.doi_journal_prefix(issn, article.pub_date_year) for issn in [article.e_issn, article.print_issn] if issn is not None]
        self.journal_doi_prefix_items = [item for item in self.journal_doi_prefix_items if item is not None]
        if len(self.journal_doi_prefix_items) == 0:
            self.journal_doi_prefix_items = None
        self.messages = []

    def validate(self):
        self.messages = []
        self.validate_format()
        self.validate_doi_prefix()
        self.validate_journal_title()
        self.validate_article_title()
        self.validate_issn()

    def validate_format(self):
        invalid_chars = self.doi_data.validate_doi_format()
        if len(invalid_chars) > 0:
            self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} has {q} invalid characteres ({invalid}). Valid characters are: {valid_characters}. ').format(value=self.doi_data.doi, valid_characters=_('numbers, letters no diacritics, and -._;()/'), invalid=' '.join(invalid_chars), q=str(len(invalid_chars)))))

    def validate_doi_prefix(self):
        valid_prefix = False
        if self.journal_doi_prefix_items is not None:
            for prefix in self.journal_doi_prefix_items:
                if self.doi_data.doi.startswith(prefix):
                    valid_prefix = True
            if not valid_prefix:
                prefix = ''
                if '/' in self.doi_data.doi:
                    prefix = self.doi_data.doi[:self.doi_data.doi.find('/')]
                self.messages.append(('doi', validation_status.STATUS_FATAL_ERROR, _('{value} is an invalid value for {label}. ').format(value=prefix, label=_('doi prefix')) + _('{label} must starts with: {expected}. ').format(label='doi', expected=_(' or ').join(self.journal_doi_prefix_items))))

    def validate_journal_title(self):
        if not self.doi_data.journal_titles is None:
            status = validation_status.STATUS_INFO
            if not self.article.journal_title in self.doi_data.journal_titles:
                max_rate, items = utils.most_similar(utils.similarity(self.doi_data.journal_titles, self.article.journal_title))
                if max_rate < 0.7:
                    status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=self.doi_data.doi, owner='|'.join(self.doi_data.journal_titles))))

    def validate_article_title(self):
        if not self.doi_data.article_titles is None:
            status = validation_status.STATUS_INFO
            max_rate = 0
            selected = None
            for t in self.article.titles:
                rate, items = utils.most_similar(utils.similarity(self.doi_data.article_titles, xml_utils.remove_tags(t.title)))
                if rate > max_rate:
                    max_rate = rate
            if max_rate < 0.7:
                status = validation_status.STATUS_FATAL_ERROR
            self.messages.append(('doi', status, _('{item} is registered as belonging to {owner}. ').format(item=self.doi_data.doi, owner='|'.join(self.doi_data.article_titles))))

    def validate_issn(self):
        if self.doi_data.journal_titles is None:
            found = False
            for issn in [self.article.print_issn, self.article.e_issn]:
                if issn is not None:
                    if issn.upper() in self.doi_data.doi.upper():
                        found = True
            if not found:
                self.messages.append(('doi', validation_status.STATUS_ERROR, _('Be sure that {item} belongs to this journal. ').format(item='DOI=' + self.doi_data.doi)))


class DOI_Data(object):

    def __init__(self, doi):
        self.doi = doi
        self.journal_titles = None
        self.article_titles = None
        self.pid = None

    def validate_doi_format(self):
        errors = []
        if self.doi is not None:
            for item in self.doi:
                if item.isdigit():
                    pass
                elif item in '-.-;()/':
                    pass
                elif item in 'abcdefghijklmnopqrstuvwxyz' or item in 'abcdefghijklmnopqrstuvwxyz'.upper():
                    pass
                else:
                    errors.append(item)
        return errors


def invalid_labels_and_values(labels_and_values):
    return _(u'The items are not correct. Check: {values}. ').format(values='; '.join([label + '="' + value + '"' for label, value in labels_and_values]))


def invalid_value_message(invalid_value, label, expected_values=None):
    msg = _('{value} is an invalid value for {label}. ').format(value=invalid_value, label=label)
    if expected_values is not None:
        msg += _('Expected values: {expected}. ').format(expected=expected_values)
    return msg


def validate_element_is_found_in_mixed_citation(element_name, element_content, mixed_citation):
    r = []
    if element_content is not None:
        _mixed = xml_utils.remove_tags(mixed_citation).replace('  ', ' ')
        if not isinstance(element_content, list):
            element_content = [element_content]

        for item in element_content:
            _element_content = xml_utils.remove_tags(item).replace('  ', ' ')

            if not _element_content in _mixed:
                diff1, s1 = utils.diff(_element_content, _mixed)
                r.append(
                    (
                        element_name,
                        validation_status.STATUS_ERROR,
                         {_('Be sure that the elements {elem1} and {elem2} are properly identified. ').format(elem1=element_name, elem2='mixed-citation'):

                            {element_name: s1,
                             _('Words found in {elem1}, but not found in {elem2}. ').format(elem1=element_name, elem2='mixed-citation'): diff1
                            },
                        }
                    )
                )
    return r


def update_pkg_files_report(d, k, status, message):
    if not k in d.keys():
        d[k] = {}
    if not status in d[k].keys():
        d[k][status] = []
    if not message in d[k][status]:
        d[k][status].append(message)
    return d


def evaluate_tiff(img_filename, min_height=None, max_height=None):
    status_message = []
    tiff_im = utils.tiff_image(img_filename)
    if tiff_im is not None:
        errors = []
        dpi = None if tiff_im.info is None else tiff_im.info.get('dpi', [_('unknown')])[0]

        info = []
        info.append(u'{dpi} dpi'.format(dpi=dpi))
        info.append(_('height: {height} pixels. ').format(height=tiff_im.size[1]))
        info.append(_('width: {width} pixels. ').format(width=tiff_im.size[0]))

        status = None
        if min_height is not None:
            if tiff_im.size[1] < min_height:
                status = validation_status.STATUS_WARNING
        if max_height is not None:
            if tiff_im.size[1] > max_height:
                status = validation_status.STATUS_WARNING
        if status is not None:
            errors.append(_('Be sure that {img} has valid height. Recommended: min={min} and max={max}. The images must be proportional among themselves. ').format(img=os.path.basename(img_filename), min=min_height, max=max_height))
        if dpi is not None:
            if dpi < MIN_IMG_DPI:
                errors.append(_('Expected values: {expected}. ').format(expected=_('equal or greater than {value} dpi').format(value=MIN_IMG_DPI)))
                status = validation_status.STATUS_ERROR
        if len(errors) > 0:
            status_message.append((status, '; '.join(info) + ' | ' + '. '.join(errors)))
        else:
            status_message.append((validation_status.STATUS_INFO, '; '.join(info)))

    return status_message


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
            if not missing_xref in not_missing:
                confirmed_missing.append(missing_xref)
    return confirmed_missing


def check_lang(elem_name, lang):
    label, status, msg = required(elem_name + '/@xml:lang', lang, validation_status.STATUS_FATAL_ERROR)
    if status == validation_status.STATUS_OK:
        status, msg = attributes.check_lang(lang)
        status = validation_status.STATUS_OK if status else validation_status.STATUS_FATAL_ERROR
    return (label, status, msg)


def format_value(value):
    if value is None:
        value = 'None'
    return value


def validate_value(value):
    result = []
    status = validation_status.STATUS_OK
    if value is not None:
        _value = value.strip()
        if _value == value:
            pass
        elif _value.startswith('<') and _value.endswith('>'):
            pass
        else:
            status = validation_status.STATUS_ERROR
            if value.startswith(' '):
                result.append(_('{value} starts with invalid characters: {invalid_chars}. ').format(value=value, invalid_chars=_('space')))
            if value.endswith(' '):
                result.append(_('{value} ends with invalid characters: {invalid_chars}. ').format(value=value, invalid_chars=_('space')))
            if value.startswith('.'):
                status = validation_status.STATUS_WARNING
                result.append(_('{value} starts with invalid characters: {invalid_chars}. ').format(value=value, invalid_chars=_('dot')))
            differ = value.replace(_value, '')
            if len(differ) > 0:
                result.append(_('{value} contains invalid {invalid_items_name}: {invalid_items}. ').format(value='<data>' + value + '</data> ', invalid_items_name=_('characters'), invalid_items=differ))
    if status == validation_status.STATUS_OK:
        message = format_value(value)
    else:
        message = ';\n'.join(result)
    return (status, message)


def display_value(label, value):
    status, message = validate_value(value)
    return (label, status, message)


def conditional_required(label, value):
    status, message = validate_value(value)
    return (label, status, message) if value is not None else (label, validation_status.STATUS_WARNING, _('{label} is required, {condition}. ').format(label=label, condition=_('if applicable')))


def required_one(label, value):
    return (label, validation_status.STATUS_OK, display_attributes(value)) if value is not None else (label, validation_status.STATUS_ERROR, _('It is required at least one {label}. ').format(label=label))


def required(label, value, default_status, validate_content=True):
    if value is None:
        result = (label, default_status, _('{label} is required. ').format(label=label))
    elif value == '':
        result = (label, default_status, _('{label} is required. ').format(label=label))
    else:
        if validate_content:
            status, message = validate_value(value)
            result = (label, status, message)
        else:
            result = (label, validation_status.STATUS_OK, value)
    return result


def expected_values(label, value, expected, fatal=''):
    status = validation_status.STATUS_ERROR
    if fatal != '':
        status = validation_status.STATUS_FATAL_ERROR
    return (label, validation_status.STATUS_OK, value) if value in expected else (label, status, invalid_value_message(format_value(value), label, expected))


def display_attributes(attributes):
    r = []
    for key, value in attributes.items():
        if value is list:
            value = '; '.join(value)
        status, message = validate_value(value)
        r.append(key + ' (' + status + '): ' + message)
    return '; '.join(r)


def invalid_terms_in_value(label, value, invalid_terms, error_or_warning):
    r = True
    invalid = ''
    b = value.decode('utf-8') if not isinstance(value, unicode) else value

    for term in invalid_terms:
        a = term.decode('utf-8') if not isinstance(term, unicode) else term

        if term.upper() in value.upper() or term in value or a in b:
            r = False
            invalid = term
            break
    if not r:
        return (label, error_or_warning, _('{value} contains invalid {invalid_items_name}: {invalid_items}. ').format(value='<data>' + value + '</data> ', invalid_items_name=_('characters'), invalid_items=invalid))
    else:
        return (label, validation_status.STATUS_OK, value)


def validate_name(label, value, invalid_terms):
    r = []
    result = required(label, value, validation_status.STATUS_WARNING)
    label, status, msg = result
    if status == validation_status.STATUS_OK:
        result = invalid_terms_in_value(label, value, invalid_terms, validation_status.STATUS_ERROR)
    r.append(result)
    _test_number = warn_unexpected_numbers(label, value)
    if _test_number is not None:
        r.append(_test_number)
    return r


def warn_unexpected_numbers(label, value, max_number=0):
    r = None
    if value is not None:
        value = xml_utils.htmlent2char(value)
        q_numbers = len([c for c in value if c.isdigit()])
        q_others = len(value) - q_numbers
        if q_numbers > q_others:
            r = (label, validation_status.STATUS_WARNING, _('Be sure that {item} is correct. ').format(item='<' + label + '>' + value + '</' + label + '>'))
    return r


def validate_surname(label, value):
    r = []
    label, status, msg = required(label, value, validation_status.STATUS_ERROR)
    if status == validation_status.STATUS_OK:
        msg = value
        parts = value.split(' ')
        if parts[-1] in attributes.identified_suffixes():
            msg = _('{label} contains invalid {invalid_items_name}: {invalid_items}. ').format(label=u'<surname>{v}</surname>'.format(v=value), invalid_items_name=_('terms'), invalid_items=parts[-1])
            msg += _(u'{value} should be identified as {label}, if {term} is the surname, ignore this message. ').format(value=parts[-1], label=u' <suffix>' + parts[-1] + '</suffix>', term=parts[-1])
            status = validation_status.STATUS_ERROR
            r.append((label, status, msg))
    _test_number = warn_unexpected_numbers(label, value)
    if _test_number is not None:
        r.append(_test_number)
    return r


def validate_contrib_names(author, aff_ids=[]):
    #FIXME
    results = validate_surname('surname', author.surname) + validate_name('given-names', author.fname, ['_'])
    if len(aff_ids) > 0:
        if len(author.xref) == 0:
            msg = _('{item} has no {missing_item}. ').format(item=author.fullname, missing_item='xref[@ref-type="aff"]/@rid') + _('Expected values: {expected}. ').format(expected='|'.join(aff_ids))
            results.append(('xref', validation_status.STATUS_WARNING, msg))
        else:
            for xref in author.xref:
                if not xref in aff_ids:
                    msg = invalid_value_message(xref, '{label} ({value})'.format(label='xref[@ref-type="aff"]/@rid', value=author.fullname), ', '.join(aff_ids))
                    results.append(('xref', validation_status.STATUS_FATAL_ERROR, msg))
    if author.contrib_id.get('orcid'):
        if not validate_orcid(author.contrib_id.get('orcid')):
            results.append(
                ('orcid',
                 validation_status.STATUS_FATAL_ERROR,
                 _('{value} is a invalid value for {label}. ').format(
                    value=author.contrib_id.get('orcid'),
                    label='')))
    return results


class ArticleContentValidation(object):

    def __init__(self, doi_services, journal, _article, is_db_generation, check_url):
        #FIXME ArticleDOIValidator
        self.doi_validator = ArticleDOIValidator(doi_services, _article)
        self.journal = journal
        self.article = _article
        self.is_db_generation = is_db_generation
        self.check_url = check_url

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
        performance = []
        #utils.debugging(datetime.now().isoformat() + ' validations 1')
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
            items.append(self.order)
            items.append(self.doi)
            items.append(self.article_id)
            items.append(self.pagination)
            items.append(self.total_of_pages)
            items.append(self.total_of_equations)
            items.append(self.total_of_tables)
            items.append(self.total_of_figures)
            items.append(self.total_of_references)
            items.append(self.ref_display_only_stats)
            items.append(self.contrib)
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
        items.append(self.disp_formulas)
        items.append(self.validate_xref_reftype)
        items.append(self.missing_xref_list)
        #items.append(self.innerbody_elements_permissions)

        items.append(self.refstats)
        items.append(self.refs_sources)

        r = self.normalize_validations(items)
        return (r, performance)

    def is_not_empty_element(self, node):
        if node is not None:
            return len(xml_utils.remove_tags(xml_utils.node_text(node))) > 0

    def is_not_empty_attribute(self, node, attr_name):
        if node is not None:
            return node.attrib.get(attr_name) != ''

    @property
    def disp_formulas(self):
        results = []
        required_at_least_one_child = ['graphic', '{http://www.w3.org/1998/Math/MathML}math', 'math', 'tex-math', 'alternatives']
        for disp_formula_node in self.article.disp_formula_elements:
            found = False
            for child in disp_formula_node.findall('*'):
                if child.tag in required_at_least_one_child:
                    if child.tag == 'graphic':
                        found = self.is_not_empty_attribute(child, '{http://www.w3.org/1999/xlink}href')
                    elif child.tag in ['{http://www.w3.org/1998/Math/MathML}math', 'math', 'tex-math']:
                        found = self.is_not_empty_element(child)
                    elif child.tag in ['alternatives']:
                        if self.is_not_empty_attribute(child, '{http://www.w3.org/1999/xlink}href'):
                            found = any([self.is_not_empty_element(child.find('math')),
                                self.is_not_empty_element(child.find('{http://www.w3.org/1998/Math/MathML}math')),
                                self.is_not_empty_element(child.find('tex-math')),
                                ])                    
                if found: 
                    break
            if not found:
                results.append(('disp-formula', validation_status.STATUS_FATAL_ERROR, _('{element} is not complete, it requires {children} with valid structure. ').format(children=_(' or ').join(required_at_least_one_child), element='disp-formula'), xml_utils.node_xml(disp_formula_node)))
        return results

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        results = attributes.validate_article_type_and_section(self.article.article_type, self.article.toc_section, len(self.article.abstracts) > 0)
        return results

    @property
    def sps(self):
        version = str(self.article.sps)
        label = 'article/@specific-use'
        status = validation_status.STATUS_INFO
        msg = version

        if version in attributes.sps_current_versions():
            return [(label, status, msg)]

        article_dateiso = self.article.article_pub_dateiso
        if article_dateiso is None:
            article_dateiso = self.article.issue_pub_dateiso
        if article_dateiso is None:
            return [(label, validation_status.STATUS_ERROR, _('Unable to validate sps version because article has no publication date. '))]

        expected_versions = list(set(attributes.expected_sps_versions(article_dateiso) + attributes.sps_current_versions()))
        expected_versions.sort()

        if version in expected_versions:
            status = validation_status.STATUS_INFO
            msg = _('For articles published on {pubdate}, {sps_version} is valid. ').format(pubdate=utils.display_datetime(article_dateiso, None), sps_version=version)
        else:
            status = validation_status.STATUS_ERROR
            msg = _('For articles published on {pubdate}, {sps_version} is not valid. ').format(pubdate=utils.display_datetime(article_dateiso, None), sps_version=version) + _('Expected SPS versions for this article: {sps_versions}. ').format(sps_versions=_(' or ').join(expected_versions))
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
        return check_lang('article', self.article.language)

    @property
    def languages(self):
        msg = []
        for lang in self.article.trans_languages:
            msg.append(check_lang('sub-article', lang))
        for lang in self.article.titles_by_lang.keys():
            msg.append(check_lang('(title-group | trans-title-group)', lang))
        for lang in self.article.abstracts_by_lang.keys():
            msg.append(check_lang('(abstract | trans-abstract)', lang))
        for lang in self.article.keywords_by_lang.keys():
            msg.append(check_lang('kwd-group', lang))
        return msg

    @property
    def months_seasons(self):
        r = []
        for parent, parent_id, value in self.article.months:
            error = False
            if value.isdigit():
                if not int(value) in range(1, 13):
                    error = True
            else:
                error = True
            if error:
                r.append(('{parent} ({parent_id}'.format(parent=parent, parent_id=parent_id), validation_status.STATUS_FATAL_ERROR, invalid_value_message(value, 'month', ' | '.join([str(i) for i in range(1, 13)]))))
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
            if error:
                expected = _('initial month and final month must be separated by hyphen. E.g.: Jan-Feb. Expected values for the months: {months}. ').format(months=article_utils.MONTHS_ABBREV.replace('|', ' '))
                msg = invalid_value_message(value, 'season', expected)
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
            if not related_article.get('related-article-type') in attributes.related_articles_type:
                r.append(('related-article/@related-article-type', validation_status.STATUS_FATAL_ERROR,
                    invalid_value_message(related_article.get('related-article-type', _('None')), 'related-article/@related-article-type')))
            if related_article.get('ext-link-type', '') == 'doi':
                _doi = related_article.get('href', '')
                if _doi != '':
                    doi_data = DOI_Data(_doi)
                    errors = doi_data.validate_doi_format()
                    if len(errors) > 0:
                        msg = invalid_value_message(related_article.get('href'), 'related-article/@xlink:href')
                        r.append(('related-article/@xlink:href', validation_status.STATUS_FATAL_ERROR, msg + ('The content of {label} must be a DOI number. ').format(label='related-article/@xlink:href')))
        return r

    @property
    def refstats(self):
        r = []
        non_scholar_types = [k for k in self.article.refstats.keys() if not k in attributes.BIBLIOMETRICS_USE]
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
        for ref in self.article.references:
            if not ref.publication_type in refs.keys():
                refs[ref.publication_type] = {}
            if not ref.source in refs[ref.publication_type].keys():
                refs[ref.publication_type][ref.source] = 0
            refs[ref.publication_type][ref.source] += 1
        return [(_('sources'), validation_status.STATUS_INFO, refs)]

    @property
    def ref_display_only_stats(self):
        r = []
        if self.article.display_only_stats > 0:
            r.append(('element-citation/@specific-use="display-only"', validation_status.STATUS_WARNING, self.article.display_only_stats))
        return r

    @property
    def journal_title(self):
        return required('journal title', self.article.journal_title, validation_status.STATUS_FATAL_ERROR)

    @property
    def publisher_name(self):
        return required('publisher name', self.article.publisher_name, validation_status.STATUS_FATAL_ERROR)

    @property
    def journal_id_publisher_id(self):
        if self.article.sps_version_number is not None:
            if self.article.sps_version_number >= 1.3:
                return required('journal-id (publisher-id)', self.article.journal_id_publisher_id, validation_status.STATUS_FATAL_ERROR)

    @property
    def journal_id_nlm_ta(self):
        if self.journal is not None:
            if self.journal.nlm_title is not None:
                if len(self.journal.nlm_title) > 0:
                    if self.article.journal_id_nlm_ta is not None:
                        if not self.article.journal_id_nlm_ta in self.journal.nlm_title:
                            msg = invalid_value_message(self.article.journal_id_nlm_ta, 'journal-id (nlm-ta)', '|'.join(self.journal.nlm_title))
                            return (('journal-id (nlm-ta)', validation_status.STATUS_FATAL_ERROR, msg))

    @property
    def journal_issns(self):
        _valid = []
        if self.article.journal_issns is not None:
            for k, v in self.article.journal_issns.items():
                valid = False
                if v[4:5] == '-':
                    if len(v) == 9:
                        valid = True
                status = validation_status.STATUS_OK if valid else validation_status.STATUS_FATAL_ERROR
                _valid.append((k + ' ISSN', status, v))
            if len(_valid) == 0:
                _valid.append(('ISSN', validation_status.STATUS_FATAL_ERROR, _('It is required at least one {label}. ').format(label='ISSN')))
        return _valid

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section, validation_status.STATUS_FATAL_ERROR)

    @property
    def contrib(self):
        r = []
        if self.article.article_type in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC:
            if len(self.article.contrib_names) == 0 and len(self.article.contrib_collabs) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR,  _('{requirer} requires {required}. ').format(requirer=self.article.article_type, required=_('contrib names or collabs'))))
        for item in self.article.article_type_and_contrib_items:
            if item[0] in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC and len(item[1]) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR, _('{requirer} requires {required}. ').format(requirer=item[0], required=_('contrib names or collabs'))))
        return r

    @property
    def contrib_names(self):
        r = []
        author_xref_items = []
        aff_ids = [aff.id for aff in self.article.affiliations if aff.id is not None]
        for item in self.article.contrib_names:
            for xref in item.xref:
                author_xref_items.append(xref)
            for result in validate_contrib_names(item, aff_ids):
                r.append(result)
            for contrib_id_type, contrib_id in item.contrib_id.items():
                if contrib_id_type in attributes.CONTRIB_ID_URLS.keys():
                    if attributes.CONTRIB_ID_URLS.get(contrib_id_type) in contrib_id or contrib_id.startswith('http'):
                        label = 'contrib-id[@contrib-id-type="' + contrib_id_type + '"]'
                        msg = invalid_value_message(contrib_id, label)
                        r.append((label, validation_status.STATUS_ERROR, msg + _('Use only the ID')))
                else:
                    msg = invalid_value_message(contrib_id_type, 'contrib-id/@contrib-id-type', ', '.join(attributes.CONTRIB_ID_URLS.keys()))
                    r.append(('contrib-id/@contrib-id-type', validation_status.STATUS_ERROR, msg))
        for affid in aff_ids:
            if not affid in author_xref_items:
                r.append(('aff/@id', validation_status.STATUS_FATAL_ERROR, _('Not found: {label}. ').format(label='<xref ref-type="aff" rid="' + affid + '"/>')))
        return r

    @property
    def contrib_collabs(self):
        return [('collab', validation_status.STATUS_OK, collab.collab) for collab in self.article.contrib_collabs]

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
        if self.article.doi is not None:
            self.doi_validator.validate()
            r = self.doi_validator.messages
        return r

    @property
    def previous_article_pid(self):
        return display_value('article-id[@specific-use="previous-pid"]', self.article.previous_article_pid)

    @property
    def order(self):
        def valid(order, status):
            r = (validation_status.STATUS_OK, order)
            if order is None:
                r = (status, _('{label} is required. ').format(label='order') + _('Expected values: {expected}. ').format(expected=_('number from 1 to 99999')))
            else:
                if order.isdigit():
                    if int(order) < 1 or int(order) > 99999:
                        r = (status,  _('Invalid format of {label}. ').format(label='order') + _('Expected values: {expected}. ').format(expected=_('number from 1 to 99999')))
                else:
                    r = (status,  _('Invalid format of {label}. ').format(label='order') + _('Expected values: {expected}. ').format(expected=_('number from 1 to 99999')))
            return r
        if self.is_db_generation:
            status = validation_status.STATUS_BLOCKING_ERROR
        else:
            status = validation_status.STATUS_ERROR
        status, msg = valid(self.article.order, status)
        return [('order', validation_status.STATUS_INFO, _('order is a 5-digits number generated from fpage or article-id (other) to compose the article PID. ')), ('order', status, msg)]

    @property
    def article_id_other(self):
        r = ('article-id[@pub-id-type="other"]', validation_status.STATUS_OK, self.article.article_id_other)
        if self.article.fpage is not None:
            if self.article.fpage == '00' or not self.article.fpage.isdigit():
                r = ('article-id[@pub-id-type="other"]', validation_status.STATUS_FATAL_ERROR, _('{label} is required, {condition}. ').format(label='article-id[@pub-id-type="other"]', condition=_('if there is no first page or first page is not a number')))
        return r

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return ('issue label', validation_status.STATUS_WARNING, _('Not found: {label}. ').format(label='volume, issue') + _('{item} will be considered ahead of print. ').format(item=_('issue')))
        else:
            return [self.volume, self.number]

    @property
    def volume(self):
        return display_value('volume', self.article.volume)

    @property
    def number(self):
        return display_value('number', self.article.number)

    @property
    def supplement(self):
        return display_value('supplement', self.article.supplement)

    @property
    def is_issue_press_release(self):
        return display_value('is_issue_press_release', self.article.is_issue_press_release)

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
        return display_value('ack xml', self.article.ack_xml)

    @property
    def pagination(self):
        if all([self.article.fpage, self.article.elocation_id]) is True:
            return (('fpage', validation_status.STATUS_ERROR, _('Use only fpage and lpage. ')))
        r = ('fpage', validation_status.STATUS_OK, self.article.fpage)
        if self.article.fpage is None:
            r = required('elocation-id', self.article.elocation_id, validation_status.STATUS_ERROR)
        return r

    @property
    def affiliations(self):
        r = []

        labels = []
        labels.append('institution[@content-type="original"]')
        labels.append('institution[@content-type="normalized"]')
        labels.append('institution[@content-type="orgname"]')
        labels.append('institution[@content-type="orgdiv1"]')
        labels.append('institution[@content-type="orgdiv2"]')
        #labels.append('institution[@content-type="orgdiv3"]')
        labels.append('addr-line/named-content[@content-type="city"]')
        labels.append('addr-line/named-content[@content-type="state"]')
        labels.append('country')
        labels.append('country/@country')

        self.article.normalized_affiliations = {}
        for aff in self.article.affiliations:
            text = aff.original if aff.original is not None else aff.xml
            r.append(('aff xml', validation_status.STATUS_INFO, aff.xml))
            r.append(required('aff/@id', aff.id, validation_status.STATUS_FATAL_ERROR))

            r.append(required('aff/institution/[@content-type="original"]', aff.original, validation_status.STATUS_ERROR, False))
            resp = required('aff/country', aff.country, validation_status.STATUS_FATAL_ERROR)
            resp = (resp[0], resp[1], resp[2] + _('E.g.: Use {this} instead of {that}. ').format(this='<country country="BR">Brasil</country>', that='<country country="BR"/>'))
            r.append(resp)

            for i_country_validation in attributes.validate_iso_country_code(aff.i_country):
                r.append(i_country_validation)

            r.append(required('aff/institution/[@content-type="orgname"]', aff.orgname, validation_status.STATUS_FATAL_ERROR))

            if aff.orgdiv3 is not None:
                r.append(('aff/institution/[@content-type="orgdiv3"]', validation_status.STATUS_ERROR, _('Remove this institution(orgdiv3). Use only one orgdiv1 and one orgdiv2. Other levels are not allowed. ')))
            for item in [aff.orgdiv1, aff.orgdiv2]:
                if item is not None:
                    status = ''
                    if 'univers' in item.lower():
                        status = validation_status.STATUS_WARNING
                    elif not 'depart' in item.lower() and not 'divi' in item.lower():
                        status = validation_status.STATUS_WARNING
                    if len(status) > 0:
                        if aff.orgname is not None:
                            r.append(('aff/institution[@content-type="orgdiv?"]', status, _('Be sure that {value} is a division of {orgname}. ').format(value=item, orgname=aff.orgname)))
                        else:
                            r.append(('aff/institution[@content-type="orgdiv?"]', status, _('Be sure that {value} is a division of {orgname}. ').format(value=item, orgname=_('an organization'))))

            norm_aff, found_institutions = article_utils.normalized_institution(aff)

            #if aff.norgname is None or aff.norgname == '':
            #    r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_ERROR, _('Required') + '. ' + _('Use aff/institution/[@content-type="normalized"] only if the normalized name is known, otherwise use no element. ')))

            if norm_aff is None:
                msg = _('Unable to confirm/find the normalized institution name for ') + join_not_None_items(list(set([aff.orgname, aff.norgname])), ' or ')
                if found_institutions is None:
                    r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_WARNING, msg))
                elif len(found_institutions) == 0:
                    r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_WARNING, msg))
                else:
                    msg += _('. Check if any option of the list is the normalized name: ') + '<OPTIONS/>' + '|'.join([join_not_None_items(list(item)) for item in found_institutions])
                    r.append((_('Suggestions:'), validation_status.STATUS_ERROR, msg))
            else:
                self.article.normalized_affiliations[aff.id] = norm_aff
                status = validation_status.STATUS_VALID
                if aff.norgname is not None:
                    if aff.norgname != norm_aff.norgname:
                        status = validation_status.STATUS_FATAL_ERROR
                if status == validation_status.STATUS_VALID:
                    message = _('Valid: ') + join_not_None_items([norm_aff.norgname, norm_aff.city, norm_aff.state, norm_aff.i_country, norm_aff.country])
                else:
                    message = _('Use {right} instead of {wrong}. ').format(right=norm_aff.norgname, wrong=aff.norgname)
                r.append(('aff/institution/[@content-type="normalized"]', status, message))

            values = [aff.original, aff.norgname, aff.orgname, aff.orgdiv1, aff.orgdiv2, aff.city, aff.state, aff.i_country, aff.country]
            i = 0
            for label in labels:
                if values[i] is not None:
                    if '|' in values[i]:
                        r.append((label, validation_status.STATUS_FATAL_ERROR, _('only one occurrence of {label} is allowed. ').format(label=label)))
                i += 1

        return r

    @property
    def clinical_trial_url(self):
        return display_value('clinical trial url', self.article.clinical_trial_url)

    @property
    def clinical_trial_text(self):
        return display_value('clinical trial text', self.article.clinical_trial_text)

    def _total(self, total, count, label_total, label_count):
        r = []
        if total < 0:
            msg = invalid_value_message(str(total), label_total, _('numbers greater or equal to 0'))
            r.append((label_total, validation_status.STATUS_FATAL_ERROR, msg))
        elif count is not None:
            if count.isdigit():
                if total != int(count):
                    r.append((u'{label_count} ({count}) x {label_total} ({total})'.format(label_count=label_count, count=count, label_total=label_total, total=total), validation_status.STATUS_ERROR, _('{label1} and {label2} must have the same value. ').format(label1=label_count, label2=label_total)))
            else:
                msg = invalid_value_message(count, label_count, _('numbers greater or equal to 0'))
                r.append((label_count, validation_status.STATUS_FATAL_ERROR, msg))
        return r

    @property
    def total_of_pages(self):
        return self._total(self.article.total_of_pages, self.article.page_count, _('total of pages'), 'page-count')

    @property
    def total_of_references(self):
        r = []
        r.append(self._total(self.article.total_of_references, self.article.ref_count, _('total of references'), 'ref-count'))
        if self.article.article_type in attributes.REFS_REQUIRED_FOR_DOCTOPIC:
            if self.article.total_of_references == 0:
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
        if not sorted_by_lang is None:
            if len(sorted_by_lang) > 0:
                values = [item.title for item in sorted_by_lang]
        if all(values) is True:
            if lang is None:
                errors.append(invalid_value_message(_('None'), label_xml_lang, ' | '.join(values)))
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
        if not sorted_by_lang is None:
            if len(sorted_by_lang) > 0:
                values = [item.text for item in sorted_by_lang]
        elem_name = elem_item_name if elem_group_name is None else elem_group_name

        label_lang = elem_name + '/@xml:lang'
        label_elem = elem_name + ' (@xml:lang="' + lang + '")'
        if all(values) is True:
            if lang is None:
                errors.append((label_lang, err_level,
                    invalid_value_message(_('None'), label_lang, ' | '.join(values))))
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
                errors.append((elem_item_name + ' (@xml:lang="' + lang + '")', validation_status.STATUS_FATAL_ERROR, _('Required only one {item} for each language. Values found for @xml:lang="{lang}": {values}. ').format(lang=lang, item=elem_item_name, values=' | '.join(values))))
        else:
            if len(values) != len(list(set(values))):
                duplicated = {}
                for value in values:
                    if not value in duplicated.keys():
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
                if not received < accepted:
                    dates.append(('received: {value}'.format(value=received), 'accepted: {value}'.format(value=accepted)))
                if self.article.pub_date_year is not None:
                    if self.article.pub_date_year < received[0:4]:
                        dates.append(('received: {value}'.format(value=received), 'pub-date: {value}'.format(value=self.article.pub_date_year)))
                    if self.article.pub_date_year < accepted[0:4]:
                        dates.append(('accepted: {value}'.format(value=accepted), 'pub-date: {value}'.format(value=self.article.pub_date_year)))

                if len(dates) > 0:
                    for date in dates:
                        r.append(('history', validation_status.STATUS_FATAL_ERROR, _('{date1} must be before {date2}. ').format(date1=date[0], date2=date[1])))

        elif received is None and accepted is None:
            r = [('history', error_level, _('Not found: {label}. ').format(label='history'))]
        else:
            if received is None:
                r.append(required('history: received', received, error_level))
            if accepted is None:
                r.append(required('history: accepted', accepted, error_level))

        return r

    @property
    def received(self):
        return display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return display_attributes('accepted', self.article.accepted)

    @property
    def innerbody_elements_permissions(self):
        r = []
        status = validation_status.STATUS_WARNING if self.article.sps_version_number >= 1.4 else validation_status.STATUS_INFO
        if len(self.article.permissions_required) > 0:
            l = [elem_id for elem_id, missing_children in self.article.permissions_required]
            if len(l) > 0:
                r.append(('permissions', status, {_('It is highly recommended identifying {elem}, if applicable. ').format(elem=', '.join(attributes.PERMISSION_ELEMENTS)): l}))
        return r

    @property
    def article_permissions(self):
        text_languages = sorted(list(set(self.article.trans_languages + [self.article.language] + ['en'])))
        r = []
        if self.article.sps_version_number >= 1.4:
            for cp_elem in ['statement', 'year', 'holder']:
                if self.article.article_copyright.get(cp_elem) is None:
                    r.append(('copyright-' + cp_elem, validation_status.STATUS_WARNING, _('It is highly recommended identifying {elem}. ').format(elem='copyright-' + cp_elem)))
        for lang, license in self.article.article_licenses.items():
            if lang is None:
                if self.article.sps_version_number >= 1.4:
                    r.append(('license/@xml:lang', validation_status.STATUS_ERROR, _('{label} is required. ').format(label='license/@xml:lang')))
            elif not lang in text_languages:
                r.append(('license/@xml:lang', validation_status.STATUS_ERROR, _('{value} is an invalid value for {label}. ').format(value=lang, label='license/@xml:lang') + _('The license text must be written in {langs}. ').format(langs=_(' or ').join(attributes.translate_code_languages(text_languages))) + _('Expected values for {label}: {expected}. ').format(label='xml:lang', expected=_(' or ').join(text_languages)), license['xml']))
            result = attributes.validate_license_href(license.get('href'))
            if result is not None:
                r.append(result)
            r.append(expected_values('license/@license-type', license.get('type'), ['open-access'], 'FATAL '))
            r.append(required('license/license-p', license.get('text'), validation_status.STATUS_FATAL_ERROR, False))
        return [item for item in r if r is not None]

    @property
    def references(self):
        r = []
        year = self.article.received.get('year') if self.article.received is not None else None
        if year is None:
            year = self.article.accepted.get('year') if self.article.accepted is not None else None
        if year is None:
            year = self.article.pub_date_year
        if year is None:
            year = datetime.now().isoformat()[0:4]
        for ref in self.article.references:
            r.append((ref, ReferenceContentValidation(ref).evaluate(year)))
        return r

    @property
    def press_release_id(self):
        return display_value(_('press release id'), self.article.press_release_id)

    @property
    def article_date_types(self):
        r = []
        date_types = []
        expected = ['epub-ppub', 'epub' + _(' and ') + 'collection', 'epub']
        if self.article.epub_date is not None:
            date_types.append('epub')
        if self.article.collection_date is not None:
            date_types.append('collection')
        if self.article.epub_ppub_date is not None:
            date_types.append('epub-ppub')
        c = _(' and ').join(date_types)
        if c in expected:
            r.append(('article dates', validation_status.STATUS_OK, c))
        else:
            r.append(('article dates', validation_status.STATUS_ERROR, _('Invalid combination of date types: ') + c + '. ' + _('Expected values: {expected}. ').format(expected=' | '.join(expected))))
        return r

    @property
    def issue_pub_date(self):
        return required_one(_('issue pub-date'), self.article.issue_pub_date)

    @property
    def article_pub_date(self):
        return display_attributes(_('article pub-date'), self.article.article_pub_date)

    @property
    def is_ahead(self):
        return display_value(_('is aop'), self.article.is_ahead)

    @property
    def ahpdate(self):
        return display_value(_('aop'), self.article.ahpdate)

    @property
    def is_article_press_release(self):
        return display_value(_('is press_release'), self.article.is_article_press_release)

    @property
    def illustrative_materials(self):
        return article_utils.display_values(_('illustrative materials'), self.article.illustrative_materials)

    @property
    def is_text(self):
        return display_value(_('is text'), self.article.is_text)

    @property
    def previous_pid(self):
        return display_value(_('previous pid'), self.article.previous_pid)

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
                elif not tag in elements:
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
                        msg = _('Not found: {label} for {item}. ').format(item=sectitle, label='@sec-type') + _('Expected values: {expected}. ').format(expected=_(' and/or ').join(expected_values))
                        r.append((label + '/sec/@sec-type',
                                  validation_status.STATUS_WARNING,
                                  msg))
                    elif not sectype in expected_values:
                        invalid = None
                        if '|' in sectype:
                            invalid = [sec for sec in sectype.split('|') if not sec in expected_values]
                        else:
                            invalid = sectype
                        if invalid is not None:
                            if len(invalid) > 0:
                                msg = invalid_value_message(sectype, label + '/sec/@sec-type', _(' and/or ').join(expected_values))
                                r.append((label + '/sec/@sec-type', validation_status.STATUS_FATAL_ERROR, msg))
        return r

    @property
    def paragraphs(self):
        invalid_items = self.article.paragraphs_startswith(':')
        if len(invalid_items) > 0:
            return [('paragraph', validation_status.STATUS_ERROR, 
                {_('{value} starts with invalid characters: {invalid_chars}. ').format(value=_('paragraphs'), invalid_chars=':'): invalid_items})]

    @property
    def missing_xref_list(self):
        tag_and_xref_types = {'fig-group': 'fig', 'table-wrap-group': 'table', 'fig': 'fig', 'table-wrap': 'table'}
        if len(self.article.bibr_xref_ranges) > 0:
            tag_and_xref_types['ref'] = 'bibr'
        message = []
        missing = {}
        tags_id_list = {k: [] for k in tag_and_xref_types.keys()}
        for node in self.article.elements_which_has_id_attribute:
            if node.tag in tag_and_xref_types.keys():
                xref_type = tag_and_xref_types[node.tag]
                _id = node.attrib.get('id')
                xref_nodes = [item for item in self.article.xref_nodes if item['rid'] == _id]
                if len(xref_nodes) == 0:
                    if not xref_type in missing.keys():
                        missing[xref_type] = []
                    missing[xref_type].append(_id)
                else:
                    for item in xref_nodes:
                        if item['ref-type'] != xref_type:
                            msg = invalid_value_message(str(item['ref-type']), 'xref[@rid="' + str(item['rid']) + '"]/@ref-type', [str(xref_type)])
                            message.append(('xref/@ref-type', validation_status.STATUS_FATAL_ERROR, msg))

        for xref_type, missing_xref_type_items in missing.items():
            if self.article.any_xref_ranges.get(xref_type) is None:
                print(xref_type + ' has no xref ranges')
            else:
                missing_xref_type_items = confirm_missing_xref_items(missing_xref_type_items, self.article.any_xref_ranges.get(xref_type))

            if len(missing_xref_type_items) > 0:
                for xref in missing_xref_type_items:
                    message.append(('xref[@ref-type=' + xref_type + ']', validation_status.STATUS_ERROR, 
                        _('Not found: {label}. ').format(label='xref[@ref-type="{xreftype}" and rid="{rid}"]'.format(xreftype=xref_type, rid=xref))))
            if self.article.any_xref_ranges.get(xref_type) is not None:
                for start, end, start_node, end_node in self.article.any_xref_ranges.get(xref_type):
                    if start > end:
                        items = []
                        items.append(('@rid', start_node.attrib.get('rid')))
                        items.append(('xref', start_node.text))
                        items.append(('@rid', end_node.attrib.get('rid')))
                        items.append(('xref', end_node.text))
                        message.append(('xref', validation_status.STATUS_ERROR, invalid_labels_and_values(items)))
        return message

    @property
    def missing_bibr_xref(self):
        missing = []
        invalid_reftype = []
        for ref in self.article.references:
            if ref.id is not None:
                found = [item for item in self.article.xref_nodes if item['rid'] == ref.id]
                for item in found:
                    if item['ref-type'] != 'bibr':
                        invalid_reftype.append(item)
                if len(found) == 0:
                    missing.append(ref.id)
        message = []
        if len(invalid_reftype) > 0:
            msg = invalid_value_message(item['ref-type'], '@ref-type', ['bibr'])
            message.append(('xref[@ref-type=bibr]', validation_status.STATUS_FATAL_ERROR, msg))

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
                    message.append(('xref', validation_status.STATUS_ERROR, invalid_labels_and_values(items)))
            for bibr_xref in self.article.bibr_xref_nodes:
                rid = bibr_xref.attrib.get('rid')
                if rid is not None and bibr_xref.text is not None:
                    if not rid[1:] in bibr_xref.text and not bibr_xref.text.replace('(', '').replace(')', '') in rid:
                        items = []
                        items.append(('@rid', rid))
                        items.append(('xref', bibr_xref.text))
                        message.append(('xref', validation_status.STATUS_ERROR, invalid_labels_and_values(items)))
        return message

    @property
    def xref_rid_and_text(self):
        message = []
        for xref_node in self.article.xref_nodes:
            rid = xref_node['rid']
            if rid is not None and xref_node['xml'] is not None:
                if not rid[1:] in xref_node['xml']:
                    items = []
                    items.append(('@rid', rid))
                    items.append(('xref', xref_node['xml']))
                    message.append(('xref', validation_status.STATUS_WARNING, invalid_labels_and_values(items)))
        return message

    def svg(self, path):
        messages = []
        for href in self.article.hrefs:
            if href.is_internal_file and href.src.endswith('.svg'):
                try:
                    if '<image' in open(os.path.join(path, href.src)).read():
                        messages.append(('svg', validation_status.STATUS_ERROR, _(u'Invalid SVG file: {} contains embedded images. ').format(href.src)))
                except:
                    pass
        return messages
                
    def href_list(self, path):
        href_items = {}
        min_inline, max_inline = utils.valid_formula_min_max_height(self.article.inline_graphics_heights(path))
        min_disp, max_disp = utils.valid_formula_min_max_height(self.article.disp_formulas_heights(path), 0.3)
        if min_disp < min_inline:
            min_disp = min_inline
        if max_disp < max_inline:
            max_disp = max_inline
        for hrefitem in self.article.hrefs:
            status_message = []

            if hrefitem.is_internal_file:
                min_height = None
                max_height = None
                file_location = hrefitem.file_location(path)
                if hrefitem in self.article.inline_graphics:
                    min_height = min_inline
                    max_height = max_inline
                elif hrefitem in self.article.disp_formulas:
                    min_height = min_disp
                    max_height = max_disp
                status_message = evaluate_tiff(path + '/' + hrefitem.src, min_height, max_height)

                if os.path.isfile(file_location):
                    if not '.' in hrefitem.src:
                        status_message.append((validation_status.STATUS_WARNING, _('missing extension of ') + hrefitem.src + '.'))
                else:
                    if file_location.endswith(hrefitem.src):
                        status_message.append((validation_status.STATUS_FATAL_ERROR, _('Not found {label} in the {item}. ').format(label=hrefitem.src, item=_('package'))))
                    elif file_location.endswith('.jpg') and (hrefitem.src.endswith('.tif') or hrefitem.src.endswith('.tiff')):
                        status_message.append((validation_status.STATUS_FATAL_ERROR, _('Not found {label} in the {item}. ').format(label=os.path.basename(file_location), item=_('package'))))
                    elif file_location.endswith('.jpg') and not '.' in hrefitem.src:
                        status_message.append((validation_status.STATUS_WARNING, _('Not found {label} in the {item}. ').format(label=_('extension'), item=hrefitem.src)))
                        status_message.append((validation_status.STATUS_FATAL_ERROR, _('Not found {label} in the {item}. ').format(label=os.path.basename(file_location), item=_('package'))))
                hreflocation = file_location
                if hrefitem.is_image:
                    display = html_reports.thumb_image(hreflocation.replace(path, '{IMG_PATH}'))
                else:
                    display = html_reports.link(hreflocation.replace(path, '{PDF_PATH}'), hrefitem.src)
                if len(status_message) == 0:
                    status_message.append((validation_status.STATUS_INFO, ''))
                href_items[hrefitem.src] = {'display': display, 'elem': hrefitem, 'results': status_message}
            else:
                hreflocation = hrefitem.src
                if self.check_url or ('scielo' in hrefitem.src and not hrefitem.src.endswith('.pdf')):
                    if not ws_requester.wsr.is_valid_url(hrefitem.src, 30):
                        message = invalid_value_message(hrefitem.src, 'URL')
                        if ('scielo' in hrefitem.src and not hrefitem.src.endswith('.pdf')):
                            message += _('Be sure that there is no missing character such as _. ')
                        status_message.append((validation_status.STATUS_WARNING, hrefitem.src + message))
                        if hrefitem.is_image:
                            display = html_reports.thumb_image(hreflocation)
                        else:
                            display = html_reports.link(hreflocation, hrefitem.src)
                        if len(status_message) == 0:
                            status_message.append((validation_status.STATUS_INFO, ''))
                        href_items[hrefitem.src] = {'display': display, 'elem': hrefitem, 'results': status_message}
        return href_items

    def package_files(self, pkg_path):
        _pkg_files = {}
        #from XML, find files
        pdf_langs = [item[-6:-4] for item in self.article.package_files if item.endswith('.pdf') and item[-7:-6] == '-']
        if self.article.language is not None:
            filename = self.article.new_prefix + '.pdf'
            _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_INFO, 'PDF ({lang}). '.format(lang=self.article.language))
            if not filename in self.article.package_files:
                _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_ERROR, _('Not found {label} in the {item}. ').format(label=_('file'), item=_('package')))
        for lang in self.article.trans_languages:
            if not lang in pdf_langs:
                filename = self.article.new_prefix + '-' + lang + '.pdf'
                _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_ERROR, _('Not found {label} in the {item}. ').format(label=_('file'), item=_('package')))

        #from files, find in XML
        href_items_in_xml = [item.name_without_extension for item in self.article.href_files]
        href_items_in_xml += [item.src for item in self.article.href_files]
        for item in self.article.package_files:
            fname, ext = os.path.splitext(item)

            if item.startswith(self.article.new_prefix):
                status = validation_status.STATUS_INFO
                message = _('Found {label} in the {item}. ').format(label=_('file'), item=_('package'))
            else:
                status = validation_status.STATUS_FATAL_ERROR
                message = _('{label} must start with {prefix}. ').format(label=_('file'), prefix=self.article.new_prefix)

            _pkg_files = update_pkg_files_report(_pkg_files, item, status, message)

            status = validation_status.STATUS_INFO
            message = None
            if item in href_items_in_xml:
                message = _('Found {label} in the {item}. ').format(label=_('file'), item='XML')
            elif item == self.article.new_prefix + '.pdf':
                message = None
            elif ext == '.pdf':
                suffix = filename_language_suffix(fname)
                if suffix is None:
                    message = _('Not found {label} in the {item}. ').format(label=_('file'), item='XML')
                    status = validation_status.STATUS_ERROR
                else:
                    if suffix in self.article.trans_languages:
                        message = _('Found {label} in {item}. ').format(label='sub-article({lang})'.format(lang=suffix), item='XML')
                    elif suffix == self.article.language:
                        status = validation_status.STATUS_ERROR
                        message = _('PDF ({lang}). ').format(lang=suffix) + _(' must not have -{lang} in PDF name. ').format(lang=suffix)
                    else:
                        status = validation_status.STATUS_WARNING
                        message = _('Not found {label} in {item}. ').format(label='sub-article({lang})'.format(lang=suffix), item='XML')
            elif fname in href_items_in_xml:
                message = _('Found {label} in the {item}. ').format(label=_('file'), item='XML')
            elif not ext == '.jpg':
                status = validation_status.STATUS_ERROR
                message = _('Not found {label} in the {item}. ').format(label=_('file'), item='XML')

            if message is not None:
                _pkg_files = update_pkg_files_report(_pkg_files, item, status, message)
        items = []
        for filename in sorted(_pkg_files.keys()):
            for status, message_list in _pkg_files[filename].items():
                items.append((filename, status, message_list))
        return items


class ReferenceContentValidation(object):

    def __init__(self, reference):
        self.reference = reference

    def evaluate(self, article_year):
        r = []
        r.append(self.xml)
        r.extend(self.mixed_citation)
        r.append(self.publication_type)
        if self.publication_type_other is not None:
            r.append(self.publication_type_other)
        r.extend(self.publication_type_dependence)
        r.extend(self.authors_list)
        r.extend(self.year(article_year))
        r.extend(self.source)
        r.extend(self.ext_link)
        return r

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        r = []

        if self.reference.source is not None:
            msg = invalid_value_message(self.reference.source, 'source')
            _test_number = warn_unexpected_numbers('source', self.reference.source, 4)
            if _test_number is not None:
                r.append(_test_number)
            if self.reference.source[0:1] != self.reference.source[0:1].upper():
                if not self.reference.source[0:2] != 'e-':
                    r.append(('source', validation_status.STATUS_ERROR, msg))

            _source = self.reference.source.strip()
            if self.reference.source != _source:
                r.append(('source', validation_status.STATUS_ERROR, msg + _('"{value}" starts or ends with space characters. ').format(value=self.reference.source)))
        return r

    def validate_element(self, label, value, error_level=validation_status.STATUS_FATAL_ERROR):
        if not self.reference.publication_type is None:
            res = attributes.validate_element(self.reference.publication_type, label, value)
            if res != '':
                return (label, error_level, res)
            else:
                if not value is None and value != '':
                    return (label, validation_status.STATUS_OK, value)

    @property
    def is_look_like_thesis(self):
        looks_like = None
        if self.reference.publication_type != 'thesis':
            _mixed = self.reference.mixed_citation.lower() if self.reference.mixed_citation is not None else ''
            _mixed = _mixed.replace('[', ' ').replace(']', ' ').replace(',', ' ').replace(';', ' ').replace('.', ' ')
            _mixed = _mixed.split()
            for item in _mixed:
                for word in ['thesis', 'dissert', 'master', 'doctor', 'mestrado', 'doutorado', 'maestr', 'tese']:
                    if item.startswith(word):
                        looks_like = 'thesis'
                        break
        return looks_like

    @property
    def publication_type_dependence(self):
        r = []
        if not self.reference.publication_type is None:
            authors = None
            if len(self.reference.authors_list) > 0:
                _authors = []
                for item in self.reference.authors_list:
                    if isinstance(item, article.PersonAuthor):
                        a = ' '.join([name for name in [item.fname, item.surname] if name is not None])
                        if len(a) > 0:
                            _authors.append(a)
                    elif isinstance(item, article.CorpAuthor):
                        if item.collab is not None:
                            _authors.append(item.collab)
                if len(_authors) > 0:
                    authors = ', '.join(_authors)
            items = [
                    self.validate_element('person-group', authors), 
                    self.validate_element('article-title', self.reference.article_title), 
                    self.validate_element('chapter-title', self.reference.chapter_title), 
                    self.validate_element('publisher-name', self.reference.publisher_name), 
                    self.validate_element('publisher-loc', self.reference.publisher_loc), 
                    self.validate_element('comment[@content-type="degree"]', self.reference.degree), 
                    self.validate_element('conf-name', self.reference.conference_name), 
                    self.validate_element('date-in-citation[@content-type="access-date"] ' + _(' or ') + ' date-in-citation[@content-type="update"]', self.reference.cited_date), 
                    self.validate_element('ext-link', self.reference.ext_link), 
                    self.validate_element('volume', self.reference.volume), 
                    self.validate_element('issue', self.reference.issue), 
                    self.validate_element('fpage', self.reference.fpage), 
                    self.validate_element('source', self.reference.source), 
                    self.validate_element('year', self.reference.year), 
                ]

            looks_like = None
            _mixed = self.reference.mixed_citation.lower() if self.reference.mixed_citation is not None else ''
            _source = self.reference.source.lower() if self.reference.source is not None else ''
            if self.reference.publication_type != 'journal':
                if self.reference.source is not None:
                    if 'journal' in _source or 'revista' in _source or 'J ' in self.reference.source or self.reference.source.endswith('J') or 'J. ' in self.reference.source or self.reference.source.endswith('J.'):
                        looks_like = 'journal'
            if self.reference.issue is None and self.reference.volume is None:
                if self.reference.fpage is None:
                    looks_like = self.is_look_like_thesis
                if not 'legal' in self.reference.publication_type:
                    if self.reference.source is not None:
                        if 'Lei ' in self.reference.source or ('Di' in self.reference.source and 'Oficial' in self.reference.source):
                            looks_like = 'legal-doc'
                        if 'portaria ' in _source:
                            looks_like = 'legal-doc'
                        if 'decreto ' in _source:
                            looks_like = 'legal-doc'
                if 'conference' in _mixed or 'proceeding' in _mixed or 'meeting' in _mixed:
                    if self.reference.publication_type != 'confproc':
                        looks_like = 'confproc'
            if looks_like is not None:
                r.append(('@publication-type', validation_status.STATUS_ERROR, _('Be sure that {item} is correct. ').format(item='@publication-type=' + str(self.reference.publication_type)) + _('This reference looks like {publication_type}. ').format(publication_type=looks_like)))
            
            for item in items:
                if item is not None:
                    r.append(item)
        return r

    @property
    def ignore_publication_type_dependence(self):
        r = []
        authors = None
        if len(self.reference.authors_list) > 0:
            for item in self.reference.authors_list:
                if isinstance(item, article.PersonAuthor):
                    authors = item.surname + ' ...'
                elif isinstance(item, article.CorpAuthor):
                    authors = item.collab

        items = [
                self.validate_element('person-group', authors), 
                self.validate_element('article-title', self.reference.article_title), 
                self.validate_element('chapter-title', self.reference.chapter_title), 
                self.validate_element('publisher-name', self.reference.publisher_name), 
                self.validate_element('publisher-loc', self.reference.publisher_loc), 
                self.validate_element('comment[@content-type="degree"]', self.reference.degree), 
                self.validate_element('conf-name', self.reference.conference_name), 
                self.validate_element('date-in-citation[@content-type="access-date"] ' + _(' or ') + ' date-in-citation[@content-type="update"]', self.reference.cited_date), 
                self.validate_element('ext-link', self.reference.ext_link), 
                self.validate_element('volume', self.reference.volume), 
                self.validate_element('issue', self.reference.issue), 
                self.validate_element('fpage', self.reference.fpage), 
                self.validate_element('source', self.reference.source), 
                self.validate_element('year', self.reference.year), 
            ]

        if self.reference.issue is None and self.reference.volume is None:
            _mixed = self.reference.mixed_citation.lower()
            if 'conference' in _mixed or 'proceeding' in _mixed:
                if self.reference.publication_type != 'confproc':
                    r.append(('@publication-type', validation_status.STATUS_WARNING, _('Be sure that {item} is correct. ').format(item='@publication-type=' + self.reference.publication_type) + _('This reference looks like {publication_type}. ').format(publication_type='confproc')))
            if self.is_look_like_thesis == 'thesis':
                r.append(('@publication-type', validation_status.STATUS_WARNING, _('Be sure that {item} is correct. ').format(item='@publication-type=' + self.reference.publication_type) + _('This reference looks like {publication_type}. ').format(publication_type='thesis')))

        for item in items:
            if item is not None:
                r.append(item)

        any_error_level = list(set([status for label, status, message in r if status in [validation_status.STATUS_FATAL_ERROR]]))
        if len(any_error_level) == 0:
            if self.reference.ref_status == 'display-only':
                minimum_required_elements = attributes.REFERENCE_REQUIRED_SUBELEMENTS.get(self.reference.publication_type)
                if minimum_required_elements is None:
                    r.append(('@specific-use', validation_status.STATUS_ERROR, _('Remove @specific-use="display-only". It is required to identify incomplete references which @publication-type is equal to ') + ' | '.join(attributes.REFERENCE_REQUIRED_SUBELEMENTS.keys())))
                else:
                    r.append(('@specific-use', validation_status.STATUS_FATAL_ERROR, _('Remove @specific-use="display-only". It is required to identify incomplete references which @publication-type is equal to ') + ' | '.join(attributes.REFERENCE_REQUIRED_SUBELEMENTS.keys()) + '. ' + _('Expected at least the elements: ') + ' | '.join(minimum_required_elements)))

        else:
            if self.reference.ref_status == 'display-only':
                items.append((_('Incomplete Reference'), validation_status.STATUS_WARNING, _('Check if the elements of this reference are properly identified. ')))
                items = []
                for label, status, message in r:
                    if status != validation_status.STATUS_OK:
                        items.append((label, validation_status.STATUS_WARNING + _(' ignored ') + status.lower(), message))
                r = items
        return r

    @property
    def ext_link(self):
        r = []
        #if len(self.reference.ext_link) > 0 and self.reference.mixed_citation is not None:
        #    if not '<ext-link' in self.reference.mixed_citation:
        #        r.append(('ext-link', validation_status.STATUS_WARNING, _('Identify the links in mixed-citation with the ext-link element.')))
        return r

    @property
    def publication_type(self):
        return expected_values('@publication-type', self.reference.publication_type, attributes.PUBLICATION_TYPE, 'FATAL ')

    @property
    def publication_type_other(self):
        if self.reference.publication_type == 'other':
            return ('@publication-type', validation_status.STATUS_WARNING, '@publication-type=' + self.reference.publication_type + '. ' + _('Expected values: {expected}. ').format(expected=_(' or ').join([v for v in attributes.PUBLICATION_TYPE if v != 'other'])))

    @property
    def xml(self):
        return ('xml', validation_status.STATUS_INFO, self.reference.xml)

    @property
    def mixed_citation(self):
        r = []
        if self.reference.mixed_citation is None:
            r.append(required('mixed-citation', self.reference.mixed_citation, validation_status.STATUS_FATAL_ERROR, False))
        else:
            for label, data in [('source', self.reference.source), ('year', self.reference.year), ('ext-link', self.reference.ext_link)]:
                for item in validate_element_is_found_in_mixed_citation(label, data, self.reference.mixed_citation):
                    if item is not None:
                        r.append(item)
            if '_'*6 in self.reference.mixed_citation:
                if len(self.reference.authors_list) == 0:
                    r.append(('person-group', validation_status.STATUS_FATAL_ERROR, _('This reference contains {}, which means the authors of this reference are the same of the previous reference. You must copy the corresponding person-group of previous reference to this reference. '.format('_'*6))))
        return r
    
    @property
    def person_group_type(self):
        r = []
        groups_type = [item[0] for item in self.reference.authors_by_group]
        if ' In: ' in self.reference.mixed_citation and len(groups_type) < 2:
            r.append(('@person-group-type', validation_status.STATUS_FATAL_ERROR, _(u'It is expected more than one person-group. ')))
        if len(groups_type) > 1:
            no_repetition = list(set(groups_type))
            if not len(groups_type) == len(no_repetition):
                r.append(('@person-group-type', validation_status.STATUS_FATAL_ERROR, _(u'Use @person-group-type to identify the person role. You have identified {} groups. @person-group must have different value for each one. '.format(len(groups_type)))))
        return r

    @property
    def authors_list(self):
        r = []
        for person in self.reference.authors_list:
            if isinstance(person, article.PersonAuthor):
                for item in validate_contrib_names(person):
                    r.append(item)
            elif isinstance(person, article.CorpAuthor):
                r.append(('collab', validation_status.STATUS_OK, person.collab))
            else:
                r.append((invalid_value_message(_('None'), _('authors')), validation_status.STATUS_WARNING, str(type(person))))
        return r

    def year(self, article_year):
        r = []
        if article_year is None:
            article_year = datetime.now().isoformat()[0:4]
        _y = self.reference.formatted_year
        if _y is not None:
            if _y.isdigit():
                if int(_y) > article_year:
                    r.append(('year', validation_status.STATUS_FATAL_ERROR, _('{value} must not be greater than {year}. ').format(value=_y, year=datetime.now().isoformat()[0:4])))
            elif 's.d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            elif 's/d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            elif 's/d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            else:
                r.append(('year', validation_status.STATUS_FATAL_ERROR, _('{value} is not a number nor is in an expected format. ').format(value=_y)))
        return r

    @property
    def publisher_name(self):
        return display_value('publisher-name', self.reference.publisher_name)

    @property
    def publisher_loc(self):
        return display_value('publisher-loc', self.reference.publisher_loc)

    @property
    def fpage(self):
        return conditional_required('fpage', self.reference.fpage)


def validate_orcid(orcid):
    # [0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]{1}
    if len(orcid) != 19:
        return False
    pattern = re.compile("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]{1}")
    return pattern.match(orcid) is not None
