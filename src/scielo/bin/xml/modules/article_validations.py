# coding=utf-8

import os
from datetime import datetime

from __init__ import _
import validation_status
import attributes
import article_utils
import xml_utils
import utils
import article
import html_reports
import institutions_service
import fs_utils


MIN_IMG_DPI = 300
MIN_IMG_WIDTH = 789
MAX_IMG_WIDTH = 2250
MAX_IMG_HEIGHT = 2625


def update_pkg_files_report(d, k, status, message):
    if not k in d.keys():
        d[k] = {}
    if not status in d[k].keys():
        d[k][status] = []
    d[k][status].append(message)
    return d


def evaluate_tiff(img_filename, min_height=None, max_height=None):
    status_message = []
    tiff_im = utils.tiff_image(img_filename)
    if tiff_im is not None:
        errors = []
        info = []
        info.append('{dpi} dpi'.format(dpi=tiff_im.info.get('dpi')[0]))
        info.append(_('height: {height} pixels').format(height=tiff_im.size[1]))
        info.append(_('width: {width} pixels').format(width=tiff_im.size[0]))

        status = None
        if min_height is not None:
            if tiff_im.size[1] < min_height:
                status = validation_status.STATUS_WARNING
        if max_height is not None:
            if tiff_im.size[1] > max_height:
                status = validation_status.STATUS_WARNING
        if status is not None:
            errors.append(_('Be sure that {img} has valid height. Recommended: min={min} and max={max}. The images must be proportional among themselves.').format(img=os.path.basename(img_filename), min=min_height, max=max_height))
        if tiff_im.info.get('dpi') is not None:
            if tiff_im.info.get('dpi') < MIN_IMG_DPI:
                errors.append(_('Expected >= {value} dpi').format(value=MIN_IMG_DPI))
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
                result.append(value + _(' starts with') + _(' "space"'))
            if value.endswith(' '):
                result.append(value + _(' ends with') + _(' "space"'))
            if value.startswith('.'):
                status = validation_status.STATUS_WARNING
                result.append(value + _(' starts with') + ' "."')
            differ = value.replace(_value, '')
            if len(differ) > 0:
                result.append('<data>' + value + '</data> ' + _('contains invalid characteres:') + ' "' + differ + '"')
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
    return (label, status, message) if value is not None else (label, validation_status.STATUS_WARNING, _('Required, if exists.'))


def required_one(label, value):
    return (label, validation_status.STATUS_OK, display_attributes(value)) if value is not None else (label, validation_status.STATUS_ERROR, _('Required at least one ') + label + '.')


def required(label, value, default_status, validate_content=True):
    if value is None:
        result = (label, default_status, _('Required'))
    elif value == '':
        result = (label, default_status, _('Required'))
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
    return (label, validation_status.STATUS_OK, value) if value in expected else (label, status, format_value(value) + ' - ' + _('Invalid value for ') + label + '. ' + _('Expected values') + ': ' + ', '.join(expected))


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
        return (label, error_or_warning, _('Invalid character/word') + ' (' + invalid + ') ' + _('in') + ' ' + label + ': ' + value)
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
            r = (label, validation_status.STATUS_WARNING, _('Be sure that {item} is correct.').format(item='<' + label + '>' + value + '</' + label + '>'))
    return r


def validate_surname(label, value):
    r = []
    label, status, msg = required(label, value, validation_status.STATUS_ERROR)
    if status == validation_status.STATUS_OK:
        msg = value
        suffix_list = [item.upper() for item in [u'Nieto', u'Sobrino', u'Hijo', u'Neto', u'Sobrinho', u'Filho', u'Júnior', u'Junior', u'Senior']]

        parts = value.split(' ')
        if len(parts) > 1:
            rejected = [item for item in parts if item.upper() in suffix_list or item in ['Jr.', 'Jr', 'Sr']]
            suffix = ' '.join(rejected)

            if len(suffix) > 0:
                msg = _('Invalid terms') + ' (' + suffix + ') ' + _('in') + ' ' + value + '. '
                msg += suffix + ' ' + _('must be identified as') + ' <suffix>' + suffix + '</suffix>.'
                status = validation_status.STATUS_ERROR
                r.append((label, status, msg))
    _test_number = warn_unexpected_numbers(label, value)
    if _test_number is not None:
        r.append(_test_number)
    return r


def validate_contrib_names(author, aff_ids=[]):
    results = validate_surname('surname', author.surname) + validate_name('given-names', author.fname, ['_'])
    if len(aff_ids) > 0:
        if len(author.xref) == 0:
            results.append(('xref', validation_status.STATUS_ERROR, _('Author') + ' "' + author.fname + ' ' + author.surname + '" ' + _('has no') + ' xref' + '. ' + _('Expected values') + ': ' + '|'.join(aff_ids)))
        else:
            for xref in author.xref:
                if not xref in aff_ids:
                    results.append(('xref', validation_status.STATUS_FATAL_ERROR, xref + ' ' + _('of') + ' "' + author.fname + ' ' + author.surname + '" ' + ': ' + _('Invalid value of') + ' xref[@ref-type="aff"]/@rid' + '. ' + _('Valid values: ') + '|'.join(aff_ids)))
    return results


class ArticleContentValidation(object):

    def __init__(self, journal, _article, is_db_generation, check_url):
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
        if self.expiration_sps is not None:
            items.append(self.expiration_sps)
        items.append(self.language)
        items.append(self.languages)
        items.append(self.months_seasons)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_title)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.publisher_name)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_id_publisher_id)
        items.append(self.journal_id_nlm_ta)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.journal_issns)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.issue_label)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.article_type)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.article_date_types)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.toc_section)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.order)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.doi)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.pagination)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_pages)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_equations)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_tables)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_figures)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.total_of_references)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.refstats)
        items.append(self.refs_sources)

        items.append(self.ref_display_only_stats)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.contrib)
        items.append(self.contrib_names)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.contrib_collabs)
        #utils.debugging(datetime.now().isoformat() + ' validations affiliations')
        items.append(self.affiliations)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.funding)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.article_permissions)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.history)
        #utils.debugging(datetime.now().isoformat() + ' validations')
        items.append(self.titles_abstracts_keywords)
        items.append(self.validate_xref_reftype)
        #utils.debugging(datetime.now().isoformat() + ' validations')

        items.append(self.sections)
        items.append(self.paragraphs)
        #items.append(self.xref_rid_and_text)
        items.append(self.missing_xref_list)
        #items.append(self.missing_bibr_xref)

        items.append(self.elements_permissions)

        #utils.debugging(datetime.now().isoformat() + ' validations 2')
        r = self.normalize_validations(items)
        #utils.debugging(datetime.now().isoformat() + ' validations 3')
        return (r, performance)

    @property
    def dtd_version(self):
        return expected_values('@dtd-version', self.article.dtd_version, ['3.0', '1.0', 'j1.0'])

    @property
    def article_type(self):
        results = attributes.validate_article_type_and_section(self.article.article_type, self.article.toc_section, len(self.article.abstracts) > 0)
        return results

    @property
    def sps(self):
        label = 'article/@specific-use'
        status = validation_status.STATUS_INFO
        msg = str(self.article.sps)

        r = []

        article_dateiso = self.article.article_pub_dateiso
        if article_dateiso is None:
            article_dateiso = self.article.issue_pub_dateiso

        if article_dateiso is not None:
            if not str(self.article.sps) in attributes.sps_current_versions():
                expected_values = attributes.expected_sps_versions(article_dateiso)
                if not str(self.article.sps) in expected_values:
                    status = validation_status.STATUS_ERROR
                    msg = _('Invalid value for ') + ' ' + label + ': ' + str(self.article.sps) + '. ' + _('Expected values') + ': ' + _(' or ').join(expected_values)
        r.append((label, status, msg))
        return r

    @property
    def expiration_sps(self):
        days = attributes.sps_version_expiration_days(self.article.sps)
        if days > 0 and days < (365/2):
            return [('sps version', validation_status.STATUS_INFO, self.article.sps + _(' expires in ') + str(days) + _(' days.'))]

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
        MONTHS_ABBREV = '|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|'
        r = []
        for parent, parent_id, value in self.article.months:
            error = False
            if value.isdigit():
                if not int(value) in range(1, 13):
                    error = True
            else:
                error = True
            if error:
                r.append((parent + '(' + parent_id + ')', validation_status.STATUS_FATAL_ERROR, _('Invalid value for ') + '<month>: ' + value + '. ' + _('Expected values') + ': ' + ' | '.join([str(i) for i in range(1, 13)])))
        for parent, parent_id, value in self.article.seasons:
            error = False
            if '-' in value:
                months = value.split('-')
                month_names = MONTHS_ABBREV
                if len(months) == 2:
                    for m in months:
                        if '|' + m + '|' in month_names:
                            month_names = month_names[month_names.find(m) + len(m):]
                        else:
                            error = True
                else:
                    error = True
            elif '|' + value + '|' in MONTHS_ABBREV:
                error = True
            if error:
                r.append((parent + '(' + parent_id + ')', validation_status.STATUS_FATAL_ERROR, _('Invalid value for ') + '<season>: ' + value + '. ' + _('Expected value for season: initial month and final month separated by hyphen. E.g.: Jan-Feb. Expected values for the months: ' + MONTHS_ABBREV.replace('|', ' '))))
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
        return article_utils.display_values_with_attributes('related articles', self.article.related_articles)

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
                msg += '. ' + _('Check the value of') + ' element-citation/@publication-type.'
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
        if not self.article.journal_id_nlm_ta in self.journal.nlm_title:
            if self.journal.nlm_title is None or len(self.journal.nlm_title) == 0:
                return (('journal-id (nlm-ta)', validation_status.STATUS_FATAL_ERROR, _('Use journal-id (nlm-ta) only for NLM journals.')))
            else:
                return (('journal-id (nlm-ta)', validation_status.STATUS_FATAL_ERROR, _('Invalid value: {value}. Expected {expected}.').format(value=self.article.journal_id_nlm_ta, expected='|'.join(self.journal.nlm_title))))

    @property
    def journal_issns(self):
        _valid = []
        for k, v in self.article.journal_issns.items():
            valid = False
            if v[4:5] == '-':
                if len(v) == 9:
                    valid = True
            status = validation_status.STATUS_OK if valid else validation_status.STATUS_FATAL_ERROR
            _valid.append((k + ' ISSN', status, v))
        if len(_valid) == 0:
            _valid.append(('ISSN', validation_status.STATUS_FATAL_ERROR, _('Missing ISSN. Required at least one.')))
        return _valid

    @property
    def toc_section(self):
        return required('subject', self.article.toc_section, validation_status.STATUS_FATAL_ERROR)

    @property
    def contrib(self):
        r = []
        if self.article.article_type in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC:
            if len(self.article.contrib_names) == 0 and len(self.article.contrib_collabs) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR, self.article.article_type + _(' requires contrib names or collabs.')))
        for item in self.article.article_type_and_contrib_items:
            if item[0] in attributes.AUTHORS_REQUIRED_FOR_DOCTOPIC and len(item[1]) == 0:
                r.append(('contrib', validation_status.STATUS_FATAL_ERROR, item[0] + _(' requires contrib names or collabs.')))
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
        for affid in aff_ids:
            if not affid in author_xref_items:
                r.append(('aff/@id', validation_status.STATUS_FATAL_ERROR, _('Missing') + ' xref[@ref-type="aff"]/@rid="' + affid + '".'))
        return r

    @property
    def contrib_collabs(self):
        return [('collab', validation_status.STATUS_OK, collab.collab) for collab in self.article.contrib_collabs]

    @property
    def trans_languages(self):
        return article_utils.display_values('trans languages', self.article.trans_languages)

    @property
    def doi(self):
        r = []
        if self.article.is_ahead:
            r.append(required('doi', self.article.doi, validation_status.STATUS_FATAL_ERROR))
        else:
            r.append(required('doi', self.article.doi, validation_status.STATUS_WARNING))

        if self.article.doi is not None:
            if self.journal.doi_prefix is not None:
                if not self.article.doi.startswith(self.journal.doi_prefix):
                    r.append(('doi', validation_status.STATUS_FATAL_ERROR, _('Invalid DOI: {doi}. DOI must starts with: {expected}').format(doi=self.article.doi, expected=self.journal.doi_prefix)))

            if not self.article.doi_journal_titles is None:
                status = validation_status.STATUS_INFO
                if not self.article.journal_title in self.article.doi_journal_titles:
                    max_rate, items = utils.most_similar(utils.similarity(self.article.doi_journal_titles, self.article.journal_title))
                    if max_rate < 0.7:
                        status = validation_status.STATUS_FATAL_ERROR
                r.append(('doi', status, self.article.doi + ' ' + _('belongs to') + ' ' + '|'.join(self.article.doi_journal_titles)))

            if not self.article.doi_article_titles is None:
                status = validation_status.STATUS_INFO
                max_rate = 0
                selected = None
                for t in self.article.titles:
                    rate, items = utils.most_similar(utils.similarity(self.article.doi_article_titles, xml_utils.remove_tags(t.title)))
                    if rate > max_rate:
                        max_rate = rate
                if max_rate < 0.7:
                    status = validation_status.STATUS_FATAL_ERROR
                r.append(('doi', status, self.article.doi + ' ' + _('is already registered to') + ' ' + '|'.join(self.article.doi_article_titles)))

            if self.article.doi_journal_titles is None:
                found = False
                for issn in [self.article.print_issn, self.article.e_issn]:
                    if issn is not None:
                        if issn in self.article.doi:
                            found = True
                if not found:
                    r.append(('doi', validation_status.STATUS_ERROR, _('Be sure that {item} belongs to this journal.').format(item='DOI=' + self.article.doi)))
        return r

    @property
    def previous_article_pid(self):
        return display_value('article-id[@specific-use="previous-pid"]', self.article.previous_article_pid)

    @property
    def order(self):
        def valid(order, status):
            r = (validation_status.STATUS_OK, order)
            if order is None:
                r = (status, _('Missing order. Expected number 1 to 99999.'))
            else:
                if order.isdigit():
                    if int(order) < 1 or int(order) > 99999:
                        r = (status, order + ': ' + _('Invalid format of order. Expected number 1 to 99999.'))
                else:
                    r = (status, order + ': ' + _('Invalid format of order. Expected number 1 to 99999.'))
            return r
        if self.is_db_generation:
            status = validation_status.STATUS_FATAL_ERROR
        else:
            status = validation_status.STATUS_ERROR
        status, msg = valid(self.article.order, status)
        return ('order', status, msg)

    @property
    def article_id_other(self):
        r = ('article-id[@pub-id-type="other"]', validation_status.STATUS_OK, self.article.article_id_other)
        if self.article.fpage is not None:
            if self.article.fpage == '00' or not self.article.fpage.isdigit():
                r = ('article-id[@pub-id-type="other"]', validation_status.STATUS_FATAL_ERROR, 'article-id[@pub-id-type="other"] ' + _('is required if there is no fpage > 0 or fpage is not number.'))
        return r

    @property
    def issue_label(self):
        if not self.article.volume and not self.article.number:
            return ('issue label', validation_status.STATUS_WARNING, _('There is no volume and no issue. It will be considered ahead of print.'))
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
        if len(self.article.award_id) == 0:
            found = has_number(self.article.ack_xml)
            if found > 4:
                r.append(('award-id', validation_status.STATUS_ERROR, _('Found numbers in') + ' ack. ' + self.article.ack_xml))
            found = has_number(self.article.financial_disclosure)
            if found > 4:
                r.append(('award-id', validation_status.STATUS_ERROR, _('Found numbers in') + ' fn[@fn-type="financial-disclosure"]. ' + self.article.fn_financial_disclosure))
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
        labels.append('institution[@content-type="orgdiv3"]')
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
            resp = (resp[0], resp[1], resp[2] + _('. E.g.: Use {this} instead of {that}.').format(this='<country country="BR">Brasil</country>', that='<country country="BR"/>'))
            r.append(resp)
            r.append(required('aff/country', aff.country, validation_status.STATUS_FATAL_ERROR))
            r.append(required('aff/country/@country', aff.i_country, validation_status.STATUS_FATAL_ERROR))

            for i_country_validation in attributes.validate_iso_country_code(aff.i_country):
                r.append(i_country_validation)

            r.append(required('aff/institution/[@content-type="orgname"]', aff.orgname, validation_status.STATUS_FATAL_ERROR))
            for item in [aff.orgdiv1, aff.orgdiv2, aff.orgdiv3]:
                if item is not None:
                    status = ''
                    if 'univers' in item.lower():
                        status = validation_status.STATUS_FATAL_ERROR
                    elif not 'depart' in item.lower() and not 'divi' in item.lower():
                        status = validation_status.STATUS_WARNING
                    if len(status) > 0:
                        if aff.orgname is not None:
                            r.append(('aff/institution[@content-type="orgdiv?"]', status, _('Be sure that {value} is a division of {orgname}').format(value=item, orgname=aff.orgname)))
                        else:
                            r.append(('aff/institution[@content-type="orgdiv?"]', status, _('Be sure that {value} is a division of an organization.').format(value=item)))

            norm_aff, found_institutions = article_utils.normalized_institution(aff)
            r.append(('aff', validation_status.STATUS_INFO, join_not_None_items([aff.orgname, aff.city, aff.state, aff.country])))
            r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_INFO, aff.norgname))
            r.append(('aff/country/@country', validation_status.STATUS_INFO, aff.i_country))

            if aff.norgname is None or aff.norgname == '':
                r.append(('aff/institution/[@content-type="normalized"]', validation_status.STATUS_ERROR, _('Required') + '. ' + _('Use aff/institution/[@content-type="normalized"] only if the normalized name is known, otherwise use no element.')))

            if norm_aff is None:
                msg = _('Unable to confirm/find the normalized institution name for ') + join_not_None_items(list(set([aff.orgname, aff.norgname])), ' or ')
                if found_institutions is not None:
                    if len(found_institutions) > 0:
                        msg += _('. Check if any option of the list is the normalized name: ') + '<OPTIONS/>' + '|'.join([join_not_None_items(list(item)) for item in found_institutions])
                r.append((_('Suggestions:'), validation_status.STATUS_ERROR, msg))
            else:
                status = validation_status.STATUS_INFO
                r.append((_('normalized aff checked'), validation_status.STATUS_VALID, _('Valid: ') + join_not_None_items([norm_aff.norgname, norm_aff.city, norm_aff.state, norm_aff.i_country, norm_aff.country])))
                self.article.normalized_affiliations[aff.id] = norm_aff

            values = [aff.original, aff.norgname, aff.orgname, aff.orgdiv1, aff.orgdiv2, aff.orgdiv3, aff.city, aff.state, aff.i_country, aff.country]
            i = 0
            for label in labels:
                if values[i] is not None:
                    if '|' in values[i]:
                        r.append((label, validation_status.STATUS_FATAL_ERROR, _('only one occurrence of ') + label + _(' is allowed.')))
                i += 1

        return r

    @property
    def clinical_trial_url(self):
        return display_value('clinical trial url', self.article.clinical_trial_url)

    @property
    def clinical_trial_text(self):
        return display_value('clinical trial text', self.article.clinical_trial_text)

    def _total(self, total, count, label_total, label_count):
        if count is None and total == 0:
            r = (label_total, validation_status.STATUS_OK, str(total))
        else:
            r = (label_count + ' (' + str(count) + ') x ' + label_total + ' (' + str(total) + ')', validation_status.STATUS_WARNING, _('Unable to validate'))
            if count is not None:
                if count.isdigit():
                    count = int(count)
                    if total == count:
                        r = (label_total, validation_status.STATUS_OK, str(total))
                    else:
                        r = (label_count + ' (' + str(count) + ') x ' + label_total + ' (' + str(total) + ')', validation_status.STATUS_ERROR, _('They must have the same value'))
        return r

    @property
    def total_of_pages(self):
        if self.article.total_of_pages is not None:
            return self._total(self.article.total_of_pages, self.article.page_count, 'total of pages', 'page-count')
        elif self.article.elocation_id:
            return (_('total of pages of ') + self.article.elocation_id, validation_status.STATUS_WARNING, _('Unable to calculate'))
        else:
            pages = [self.article.fpage, self.article.lpage]
            pages = join_not_None_items(pages, '-')
            if pages != '':
                return (_('total of pages of ') + pages, validation_status.STATUS_WARNING, _('Unable to calculate'))

    @property
    def total_of_references(self):
        r = []
        r.append(self._total(self.article.total_of_references, self.article.ref_count, _('total of references'), 'ref-count'))
        if self.article.article_type in attributes.REFS_REQUIRED_FOR_DOCTOPIC:
            if self.article.total_of_references == 0:
                r.append((_('total of references'), validation_status.STATUS_FATAL_ERROR, self.article.article_type + ' ' + _('requires references')))
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
        if not sorted_by_lang is None:
            if len(sorted_by_lang) > 0:
                values = [item.title for item in sorted_by_lang]
        if all(values) is True:
            if lang is None:
                errors.append(('@xml:lang (title-group' + _(' or ') + 'trans-title-group)', err_level, _('Invalid value') + ': None' + ':' + '|'.join(values)))
            else:
                valid.append(('title-group' + _(' or ') + 'trans-title-group (@xml:lang="' + lang + '")', validation_status.STATUS_INFO, '|'.join(values)))
        else:
            label = 'title-group' + _(' or ') + 'trans-title-group (@xml:lang="' + lang + '")' if sorted_by_lang is None else 'article-title' + _(' or ') + 'trans-title (@xml:lang="' + lang + '")'
            errors.append((label, err_level, _('not found')))
        if len(values) > 1:
            errors.append(('article-title' + _(' or ') + 'trans-title (@xml:lang="' + lang + '")', validation_status.STATUS_FATAL_ERROR, _('Required only one {element} for each language. Values found for @xml:lang="{lang}": {values}').format(element='article-title' + _(' or ') + 'trans-title', values='|'.join(values), lang=lang)))
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
        if all(values) is True:
            if lang is None:
                errors.append((elem_name + '/@xml:lang', err_level, _('Invalid value') + ': None' + ':' + '|'.join(values)))
            else:
                valid.append((elem_name + ' (@xml:lang="' + lang + '")', validation_status.STATUS_INFO, '|'.join(values)))
                if mininum > 0:
                    if 1 < len(values) < mininum:
                        errors.append((elem_name + ' (@xml:lang="' + lang + '")', err_level, _('Required at least {number} items').format(number=mininum)))
        else:
            if sorted_by_lang is None:
                if elem_group_name is not None:
                    elem_name = elem_group_name
            errors.append((elem_name + ' (@xml:lang="' + lang + '")', err_level, _('not found')))
        if mininum == 0:
            if len(values) > 1:
                errors.append((elem_item_name + ' (@xml:lang="' + lang + '")', validation_status.STATUS_FATAL_ERROR, _('Required only one {element} for each language. Values found for @xml:lang="{lang}": {values}').format(lang=lang, element=elem_item_name, values='|'.join(values))))
        else:
            if len(values) != len(list(set(values))):
                duplicated = {}
                for value in values:
                    if not value in duplicated.keys():
                        duplicated[value] = 0
                    duplicated[value] += 1
                errors.append((elem_item_name, validation_status.STATUS_FATAL_ERROR, _('Required only unique values of {element} for each language. Duplicated values found for @xml:lang="{lang}": {values}').format(lang=lang, element=elem_item_name, values='|'.join([k for k, c in duplicated.items() if c > 1]))))
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
                    errors.append(('abstract + kwd-group', validation_status.STATUS_ERROR, _('Expected {unexpected} for {demander}. Be sure that "{demander}" is correct.').format(unexpected='abstract + kwd-group', demander=article_type)))
            else:
                if len(abstracts) > 0 or len(keywords) > 0:
                    errors.append(('abstract + kwd-group', validation_status.STATUS_ERROR, _('Unexpected {unexpected} for {demander}. Be sure that {demander} is correct.').format(unexpected='abstract + kwd-group', demander=article_type)))

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
        if received is not None and accepted is not None:
            dates = []
            if not received < accepted:
                dates.append(('"' + received + '" (received)', '"' + accepted + '" (accepted)'))
            if self.article.pub_date_year < received[0:4]:
                dates.append(('"' + received + '" (received)', '"' + self.article.pub_date_year + '" (pub-date)'))
            if self.article.pub_date_year < accepted[0:4]:
                dates.append(('"' + accepted + '" (accepted)', '"' + self.article.pub_date_year + '" (pub-date)'))

            if len(dates) > 0:
                for date in dates:
                    r.append(('history', validation_status.STATUS_FATAL_ERROR, _('{date1} must be a previous date than {date2}').format(date1=date[0], date2=date[1])))

        elif received is None and accepted is None:
            r = [('history', validation_status.STATUS_INFO, _('there is no history dates'))]
        else:
            if received is None:
                r.append(required('history: received', received, validation_status.STATUS_ERROR))
            if accepted is None:
                r.append(required('history: accepted', accepted, validation_status.STATUS_ERROR))

        return r

    @property
    def received(self):
        return display_attributes('received', self.article.received)

    @property
    def accepted(self):
        return display_attributes('accepted', self.article.accepted)

    @property
    def elements_permissions(self):
        r = []
        status = validation_status.STATUS_WARNING if self.article.sps_version_number >= 1.4 else validation_status.STATUS_INFO
        if len(self.article.permissions_required) > 0:
            for xml, missing_children in self.article.permissions_required:
                r.append((xml, status, _('It is highly recommended identifying {elem}').format(elem=', '.join(missing_children))))
        return r

    @property
    def article_permissions(self):
        r = []
        if self.article.sps_version_number >= 1.4:
            for cp_elem in ['statement', 'year', 'holder']:
                if self.article.article_copyright.get(cp_elem) is None:
                    r.append(('copyright-' + cp_elem, validation_status.STATUS_WARNING, _('It is highly recommended identifying {elem}').format(elem='copyright-' + cp_elem)))
        for lang, license in self.article.article_licenses.items():
            if lang is None:
                if self.article.sps_version_number >= 1.4:
                    r.append(('license/@xml:lang', validation_status.STATUS_ERROR, _('Identify @xml:lang of license')))
            else:
                r.append(('license/@xml:lang', validation_status.STATUS_INFO, lang))
            if license.get('href') is None:
                r.append(('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('Invalid value for ') + 'license/@href. ' + license.get('href')))
            elif not '://creativecommons.org/licenses/' in license.get('href'):
                r.append(('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('Invalid value for ') + 'license/@href. ' + license.get('href')))
            elif not article_utils.url_check(license.get('href')):
                r.append(('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('Invalid value for ') + 'license/@href. ' + license.get('href')))
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
            r.append(('article dates', validation_status.STATUS_ERROR, _('Invalid combination of date types: ') + c + '. ' + _('Expected values') + ': ' + ' | '.join(expected)))
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
                message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, _('Missing') + ' @rid in ' + xref['xml']))
            if xref['ref-type'] is None:
                message.append(('xref/@ref-type', validation_status.STATUS_ERROR, _('Missing') + ' @ref-type in ' + xref['xml']))
            if xref['rid'] is not None and xref['ref-type'] is not None:
                elements = attributes.REFTYPE_AND_TAG_ITEMS.get(xref['ref-type'])
                tag = id_and_elem_name.get(xref['rid'])
                if tag is None:
                    message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, xref['xml'] + ': ' + _('Missing') + ' ' + xref['ref-type'] + '[@id=' + xref['rid'] + ']'))
                elif elements is None:
                    # no need to validate
                    valid = True
                elif tag in elements:
                    valid = True
                elif not tag in elements:
                    reftypes = [reftype for reftype, _elements in attributes.REFTYPE_AND_TAG_ITEMS.items() if tag in _elements]
                    _msg = _('Unmatched')
                    _msg += ' @ref-type (' + xref['ref-type'] + ')'
                    _msg += _(' and ') + tag + ': '
                    _msg += 'xref[@ref-type="' + xref['ref-type'] + '"] '
                    _msg += _('is for') + ' ' + ' | '.join(elements)
                    _msg += _(' and ') + _('valid values of') + ' @ref-type ' + _('of') + ' '
                    _msg += tag + ' ' + _('are') + ' '
                    _msg += '|'.join(reftypes)

                    #_msg = _('Unmatched @ref-type (%s), and %s: xref[@ref-type="%s"] is for %s and valid values of  @ref-type of %s are %s') % (xref['ref-type'], tag, xref['ref-type'], attributes.REFTYPE_AND_TAG_ITEMS.get(xref['ref-type']), tag, '|'.join(reftypes))

                    message.append(('xref/@rid', validation_status.STATUS_FATAL_ERROR, _msg))
        return message

    @property
    def sections(self):
        expected_values = ['cases', 'conclusions', 'discussion', 'intro', 'materials', 'methods', 'results', 'supplementary-material']
        r = []
        for body in self.article.article_sections:
            for label, sections in body.items():
                for sectype, sectitle in sections:
                    if not sectype in expected_values:
                        invalid = None
                        if '|' in sectype:
                            invalid = [sec for sec in sectype.split('|') if not sec in expected_values]
                        else:
                            invalid = sectype
                        if invalid is not None:
                            if len(invalid) > 0:
                                r.append((label + '/sec/@sec-type', validation_status.STATUS_FATAL_ERROR, _('Invalid value: {value}. Expected {expected}.').format(value=sectype, expected=_(' and/or ').join(expected_values))))
        return r

    @property
    def paragraphs(self):
        return [('paragraphs', validation_status.STATUS_ERROR, {_('Do not start a paragraph with the colon character (:)'): self.article.paragraphs_startswith(':')})]

    @property
    def missing_xref_list(self):
        tag_and_xref_types = {'ref': 'bibr', 'fig-group': 'fig', 'table-wrap-group': 'table', 'fig': 'fig', 'table-wrap': 'table'}
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
                            message.append(('xref/@ref-type', validation_status.STATUS_FATAL_ERROR, 'xref[@rid="' + str(item['rid']) + '"]/@ref-type=' + str(item['ref-type']) + ': ' + _('Invalid value') + '. ' + _('Expected value:') + str(xref_type)))

        for xref_type, missing_xref_list in missing.items():
            if self.article.any_xref_ranges.get(xref_type) is None:
                print(xref_type + ' has no xref ranges???')
            else:
                missing_xref_list = confirm_missing_xref_items(missing_xref_list, self.article.any_xref_ranges.get(xref_type))

            if len(missing_xref_list) > 0:
                for xref in missing_xref_list:
                    message.append(('xref[@ref-type=' + xref_type + ']', validation_status.STATUS_ERROR, _('Missing') + ' xref[@ref-type=' + xref_type + ']: ' + xref))
            if self.article.any_xref_ranges.get(xref_type) is not None:
                for start, end, start_node, end_node in self.article.any_xref_ranges.get(xref_type):
                    if start > end:
                        message.append(('xref', validation_status.STATUS_ERROR, _('Invalid values for @rid={rid} or xref={xref} or @rid={rid2} or xref={xref2}').format(rid=start_node.attrib.get('rid'), xref=start_node.text, rid2=end_node.attrib.get('rid'), xref2=end_node.text)))
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
            message.append(('xref[@ref-type=bibr]', validation_status.STATUS_FATAL_ERROR, '@ref-type=' + item['ref-type'] + ': ' + _('Invalid value for') + ' @ref-type. ' + _('Expected value:') + ' bibr.'))

        if len(missing) > 0:
            missing = confirm_missing_xref_items(missing, self.article.bibr_xref_ranges)

            if len(missing) > 0:
                for xref in missing:
                    message.append(('xref[@ref-type=bibr]', validation_status.STATUS_ERROR, _('Missing') + ' xref[@ref-type=bibr]: ' + xref))

        if self.article.is_bibr_xref_number:
            for start, end, start_node, end_node in self.article.bibr_xref_ranges:
                if start > end:
                    message.append(('xref', validation_status.STATUS_ERROR, _('Invalid values for @rid={rid} or xref={xref} or @rid={rid2} or xref={xref2}').format(rid=start_node.attrib.get('rid'), xref=start_node.text, rid2=end_node.attrib.get('rid'), xref2=end_node.text)))
            for bibr_xref in self.article.bibr_xref_nodes:
                rid = bibr_xref.attrib.get('rid')
                if rid is not None and bibr_xref.text is not None:
                    if not rid[1:] in bibr_xref.text and not bibr_xref.text.replace('(', '').replace(')', '') in rid:
                        message.append(('xref/@rid', validation_status.STATUS_ERROR, _('Invalid values for @rid={rid} or xref={xref}').format(rid=rid, xref=bibr_xref.text)))
        return message

    @property
    def xref_rid_and_text(self):
        message = []
        for xref_node in self.article.xref_nodes:
            rid = xref_node['rid']
            if rid is not None and xref_node['xml'] is not None:
                if not rid[1:] in xref_node['xml']:
                    message.append(('xref/@rid', validation_status.STATUS_WARNING, _('Invalid values for @rid={rid} or xref={xref}').format(rid=rid, xref=xref_node['xml'])))
        return message

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
                        status_message.append((validation_status.STATUS_FATAL_ERROR, hrefitem.src + _(' not found in package')))
                    elif file_location.endswith('.jpg') and (hrefitem.src.endswith('.tif') or hrefitem.src.endswith('.tiff')):
                        status_message.append((validation_status.STATUS_FATAL_ERROR, os.path.basename(file_location) + _(' not found in package')))
                    elif file_location.endswith('.jpg') and not '.' in hrefitem.src:
                        status_message.append((validation_status.STATUS_WARNING, _('missing extension of ') + hrefitem.src + '.'))
                        status_message.append((validation_status.STATUS_FATAL_ERROR, os.path.basename(file_location) + _(' not found in package')))
                hreflocation = 'file:///' + file_location
                if hrefitem.is_image:
                    display = html_reports.image(hreflocation)
                if len(status_message) == 0:
                    status_message.append((validation_status.STATUS_INFO, ''))
                href_items[hrefitem.src] = {'display': display, 'elem': hrefitem, 'results': status_message}
            else:
                hreflocation = hrefitem.src
                if self.check_url or 'scielo' in hrefitem.src:
                    if not article_utils.url_check(hrefitem.src, 1):
                        message = _(' is not working')
                        if 'scielo' in hrefitem.src:
                            message += '. ' + _('Be sure that there is no missing character such as _.')
                        status_message.append((validation_status.STATUS_WARNING, hrefitem.src + message))
                        if hrefitem.is_image:
                            display = html_reports.image(hreflocation)
                        else:
                            display = html_reports.link(hreflocation, hrefitem.src)
                        if len(status_message) == 0:
                            status_message.append((validation_status.STATUS_INFO, ''))
                        href_items[hrefitem.src] = {'display': display, 'elem': hrefitem, 'results': status_message}
        return href_items

    def package_files(self, pkg_path):
        _pkg_files = {}
        #from XML, find files
        pdf_langs = [item[-6:-4] for item in self.article.package_files(pkg_path) if item.endswith('.pdf') and item[-7:-6] == '-']
        if self.article.language is not None:
            filename = self.article.new_prefix + '.pdf'
            _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_INFO, _('PDF ({lang})').format(lang=self.article.language))
            if not filename in self.article.package_files(pkg_path):
                _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_WARNING, _('not found in the package'))
        for lang in self.article.trans_languages:
            if not lang in pdf_langs:
                filename = self.article.new_prefix + '-' + lang + '.pdf'
                _pkg_files = update_pkg_files_report(_pkg_files, filename, validation_status.STATUS_WARNING, _('not found in the package'))

        #from files, find in XML
        inxml = [item.name_without_extension for item in self.article.href_files]
        inxml += [item.src for item in self.article.href_files]
        for item in self.article.package_files(pkg_path):
            status = validation_status.STATUS_INFO if item.startswith(self.article.new_prefix) else validation_status.STATUS_FATAL_ERROR
            message = _('found in the package') if status == validation_status.STATUS_INFO else _('file name must start with ') + self.article.prefix
            _pkg_files = update_pkg_files_report(_pkg_files, item, status, message)

            status = validation_status.STATUS_INFO
            message = None
            if item in inxml:
                message = _('found in XML')
            elif item == self.article.new_prefix + '.pdf':
                message = None
            elif item.endswith('.pdf'):
                lang = item[len(self.article.new_prefix):]
                if lang.startswith('-'):
                    lang = lang[1:3]
                    if lang in self.article.trans_languages:
                        message = _('found sub-article({lang}) in XML').format(lang=lang)
                    elif lang in self.article.language:
                        status = validation_status.STATUS_WARNING
                        message = _('PDF ({lang})').format(lang=lang) + _(' must not have -{lang} in PDF name').format(lang=lang)
                    else:
                        status = validation_status.STATUS_WARNING
                        message = _('not found sub-article({lang}) in XML').format(lang=lang)
            else:
                if '.' in item:
                    without_extension = item[0:item.rfind('.')]
                    if '"' + without_extension + '"' in inxml:
                        message = _('found in XML')
                    elif not item.endswith('.jpg'):
                        status = validation_status.STATUS_ERROR
                        message = _('not found in XML')
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
        for item in self.mixed_citation:
            r.append(item)
        r.append(self.publication_type)
        if self.publication_type_other is not None:
            r.append(self.publication_type_other)
        for item in self.publication_type_dependence:
            r.append(item)
        for item in self.authors_list:
            r.append(item)
        for item in self.year(article_year):
            r.append(item)
        for item in self.source:
            r.append(item)
        for item in self.ext_link:
            r.append(item)
        return r

    @property
    def id(self):
        return self.reference.id

    @property
    def source(self):
        r = []
        if self.reference.source is not None:
            _test_number = warn_unexpected_numbers('source', self.reference.source, 4)
            if _test_number is not None:
                r.append(_test_number)
            if self.reference.source[0:1] != self.reference.source[0:1].upper():
                r.append(('source', validation_status.STATUS_ERROR, self.reference.source + '-' + _('Invalid value for ') + 'source' + '. '))
            _source = self.reference.source.strip()
            if self.reference.source != _source:
                r.append(('source', validation_status.STATUS_ERROR, self.reference.source + '-' + _('Invalid value for ') + 'source, ' + _('it starts or ends with space characters.')))
            if _source.startswith('<') and _source.endswith('>'):
                r.append(('source', validation_status.STATUS_ERROR, self.reference.source + '-' + _('Invalid value for ') + 'source, ' + _('it must not have styles elements (italic, bold).')))
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
                r.append(('@publication-type', validation_status.STATUS_ERROR, '@publication-type=' + str(self.reference.publication_type) + '. ' + _('Be sure that {item} is correct.').format(item='@publication-type') + _('This reference looks like {publication_type}').format(publication_type=looks_like)))

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
                    r.append(('@publication-type', validation_status.STATUS_WARNING, '@publication-type=' + self.reference.publication_type + '. ' + _('Be sure that {item} is correct.').format(item='@publication-type') + ' ' + _('This reference looks like {publication_type}.').format(publication_type='confproc')))
            if self.is_look_like_thesis == 'thesis':
                r.append(('@publication-type', validation_status.STATUS_WARNING, '@publication-type=' + self.reference.publication_type + '. ' + _('Be sure that {item} is correct.').format(item='@publication-type') + ' ' + _('This reference looks like {publication_type}.').format(publication_type='thesis')))

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
                items.append((_('Incomplete Reference'), validation_status.STATUS_WARNING, _('Check if the elements of this reference is properly identified.')))
                items = []
                for label, status, message in r:
                    if status != validation_status.STATUS_OK:
                        items.append((label, validation_status.STATUS_WARNING + _(' ignored ') + status.lower(), message))
                r = items
        return r

    @property
    def ext_link(self):
        r = []
        if self.reference.ext_link is not None:
            ext_link = self.reference.ext_link
            if not isinstance(ext_link, list):
                ext_link = [self.reference.ext_link]
            for link in ext_link:
                if not link.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').strip() in self.reference.mixed_citation:
                    r += [('ext-link', validation_status.STATUS_ERROR, _('Be sure that the value of ext-link ({ext_link}) is found in <mixed-citation>{mixed}</mixed-citation>').format(ext_link=link, mixed=self.reference.mixed_citation))]
            if not '<ext-link' in self.reference.mixed_citation:
                r += [('ext-link', validation_status.STATUS_WARNING, _('Missing ext-link element in mixed-citation'))]
        return r

    @property
    def publication_type(self):
        return expected_values('@publication-type', self.reference.publication_type, attributes.PUBLICATION_TYPE, 'FATAL ')

    @property
    def publication_type_other(self):
        if self.reference.publication_type == 'other':
            return ('@publication-type', validation_status.STATUS_WARNING, '@publication-type=' + self.reference.publication_type + '. ' + _('Be sure that ') + _('this reference is not ') + _(' or ').join([v for v in attributes.PUBLICATION_TYPE if v != 'other']))

    @property
    def xml(self):
        return ('xml', validation_status.STATUS_INFO, self.reference.xml)

    @property
    def mixed_citation(self):
        r = []
        if self.reference.mixed_citation is not None:
            r.append(('mixed-citation', validation_status.STATUS_INFO, self.reference.mixed_citation))
            if self.reference.source is not None:
                if not xml_utils.remove_tags(self.reference.source) in xml_utils.remove_tags(self.reference.mixed_citation):
                    r.append(('source', validation_status.STATUS_ERROR, _('Be sure that the value of {element} ({value}) is found in <mixed-citation>{mixed}</mixed-citation>').format(element='source', value=self.reference.source, mixed=self.reference.mixed_citation)))
            if self.reference.year is not None:
                if not self.reference.year in self.reference.mixed_citation:
                    r.append(('year', validation_status.STATUS_ERROR, _('Be sure that the value of {element} ({value}) is found in <mixed-citation>{mixed}</mixed-citation>').format(element='year', value=self.reference.year, mixed=self.reference.mixed_citation)))
        else:
            r.append(required('mixed-citation', self.reference.mixed_citation, validation_status.STATUS_FATAL_ERROR, False))
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
                r.append((_('invalid author'), validation_status.STATUS_WARNING, str(type(person))))
        return r

    def year(self, article_year):
        r = []
        if article_year is None:
            article_year = datetime.now().isoformat()[0:4]
        _y = self.reference.formatted_year
        if _y is not None:
            if _y.isdigit():
                if int(_y) > article_year:
                    r.append(('year', validation_status.STATUS_FATAL_ERROR, _y + _(' must not be greater than ') + datetime.now().isoformat()[0:4]))
            elif 's.d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            elif 's/d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            elif 's/d' in _y:
                r.append(('year', validation_status.STATUS_INFO, _y))
            else:
                r.append(('year', validation_status.STATUS_FATAL_ERROR, _y + _(' is not a number nor in an expected format.')))
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
