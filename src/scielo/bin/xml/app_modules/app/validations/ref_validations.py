# coding=utf-8
import re
from datetime import datetime

from ...__init__ import _
from ...generics.reports import validation_status
from ..data import attributes
from . import data_validations
from ...generics import xml_utils
from ...generics import utils
from ...generics import encoding
from ...generics.reports import html_reports


def validate_publication_type(publication_type):
    if len(publication_type) == 1:
        if publication_type[0] not in attributes.PUBLICATION_TYPE:
            return data_validations.invalid_value_result(
                'publication-type',
                publication_type[0],
                ' | '.join(attributes.PUBLICATION_TYPE),
                validation_status.STATUS_FATAL_ERROR)
    else:
        return data_validations.is_required_only_one('publication-type')


def is_valid_publication_type(publication_type):
    if publication_type is not None and len(publication_type) == 1:
        if publication_type[0] in attributes.PUBLICATION_TYPE:
            return True
    return False


def validate_pubtype_and_ref_data(publication_type, label, values):
    problem = None
    compl = ''
    items = []

    required = label in attributes.REFERENCE_REQUIRED_SUBELEMENTS.get(publication_type, [])
    not_allowed = label in attributes.REFERENCE_NOT_ALLOWED_SUBELEMENTS.get(publication_type, [])

    if required and len(values) == 0:
        problem = _('{requirer} requires {required}. ').format(requirer='@publication-type="' + publication_type + '"', required=label)
        compl = _('If the reference has no {label}, ignore this message. ').format(label=label)
        items = ['@publication-type', _('the elements of this reference')]
    elif not_allowed and len(values) > 0:
        problem = _('{label} is not allowed for {item}. ').format(label=label, item='@publication-type=' + publication_type)
        items = ['@publication-type', label, ', '.join(values)]
    if problem is not None:
        problem += _('Be sure that you have correctly identified: ') + ' and/or '.join(items) + '. ' + compl
    return problem


def validate_ref_data_presence(publication_type, label, values, qtd_max=None, error_level=validation_status.STATUS_FATAL_ERROR):
    error_msg = validate_pubtype_and_ref_data(publication_type, label, values)
    if error_msg is not None:
        return (label, error_level, error_msg)
    elif qtd_max is not None:
        return validate_ref_data_quantity(label, values, 0, qtd_max, error_level)


def validate_ref_data_quantity(label, values, qtd_min=0, qtd_max=1, error_level=validation_status.STATUS_FATAL_ERROR):
    q = 0
    if values is not None:
        q = len(values)
    if not qtd_min <= q <= qtd_max:
        if qtd_min == qtd_max:
            msg = _('Expected quantity of {label} is {qtd}. ').format(label=label, qtd=qtd_max)            
        if qtd_min < qtd_max and qtd_min == 0:
            msg = _('Max quantity of {label} allowed is {qtd}. ').format(label=label, qtd=qtd_max)
        msg += _('Found {}. '.format(q))
        return (label, error_level, msg)


def element_in_mixed_citation(element_name, element_content, mixed_citation):
    r = []
    if element_content is not None:
        _mixed = xml_utils.remove_tags(mixed_citation).replace('  ', ' ')
        if not isinstance(element_content, list):
            element_content = [element_content]

        for item in element_content:
            _element_content = xml_utils.remove_tags(item).replace('  ', ' ')

            if _element_content not in _mixed:
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


class PersonValidation(object):

    def __init__(self, contrib, aff_ids):
        self.aff_ids = aff_ids
        self.contrib = contrib

    @property
    def name_validation_result(self):
        r = []
        label = 'given-names'
        result = data_validations.is_required_data(label, self.contrib.fname, validation_status.STATUS_WARNING)
        label, status, msg = result
        if status == validation_status.STATUS_OK:
            result = data_validations.invalid_terms_in_value(label, self.contrib.fname, ['_'], validation_status.STATUS_ERROR)
        r.append(result)
        _test_number = data_validations.warn_unexpected_numbers(label, self.contrib.fname)
        if _test_number is not None:
            r.append(_test_number)
        return r

    @property
    def surname_validation_result(self):
        r = []
        label = 'surname'
        label, status, msg = data_validations.is_required_data(label, self.contrib.surname)
        if status == validation_status.STATUS_OK:
            msg = self.contrib.surname
            parts = self.contrib.surname.split(' ')
            if parts[-1] in attributes.identified_suffixes():
                msg = _('{label} contains invalid {invalid_items_name}: {invalid_items}. ').format(label=u'<surname>{v}</surname>'.format(v=self.contrib.surname), invalid_items_name=_('terms'), invalid_items=parts[-1])
                msg += _(u'{value} should be identified as {label}, if {term} is the surname, ignore this message. ').format(value=parts[-1], label=u' <suffix>' + parts[-1] + '</suffix>', term=parts[-1])
                status = validation_status.STATUS_ERROR
                r.append((label, status, msg))
        _test_number = data_validations.warn_unexpected_numbers(label, self.contrib.surname)
        if _test_number is not None:
            r.append(_test_number)
        return r

    @property
    def xref_validation_result(self):
        results = []
        if len(self.aff_ids) > 0:
            if len(self.contrib.xref) == 0:
                msg = _('{item} has no {missing_item}. ').format(item=self.contrib.fullname, missing_item='xref[@ref-type="aff"]/@rid') + data_validations.expected_values_message('|'.join(self.aff_ids))
                results.append(('xref', validation_status.STATUS_WARNING, msg))
            else:
                for xref in self.contrib.xref:
                    label = u'{label} ({value})'.format(label='xref[@ref-type="aff"]/@rid', value=self.contrib.fullname)
                    results.append(data_validations.is_expected_value(label, xref, self.aff_ids, validation_status.STATUS_FATAL_ERROR))

        return results

    @property
    def contrib_id_validation_result(self):
        r = []
        for contrib_id_type, contrib_id in self.contrib.contrib_id.items():
            if contrib_id_type in attributes.CONTRIB_ID_URLS.keys():
                if attributes.CONTRIB_ID_URLS.get(contrib_id_type) in contrib_id or contrib_id.startswith('http'):
                    label = 'contrib-id[@contrib-id-type="' + contrib_id_type + '"]'
                    msg = data_validations.invalid_value_message(label, contrib_id)
                    r.append((label, validation_status.STATUS_ERROR, msg + _('Use only the ID')))
            else:
                msg = data_validations.invalid_value_result('contrib-id/@contrib-id-type', contrib_id_type, ', '.join(attributes.CONTRIB_ID_URLS.keys()))
                r.append(msg)

            if contrib_id_type == 'orcid':
                if not validate_orcid(contrib_id):
                    r.append(
                        ('orcid',
                         validation_status.STATUS_FATAL_ERROR,
                         _('{value} is a invalid value for {label}. ').format(
                            value=contrib_id,
                            label=contrib_id_type)))
        return r

    def validate(self):
        results = []
        results.extend(self.surname_validation_result)
        results.extend(self.name_validation_result)
        results.extend(self.xref_validation_result)
        results.extend(self.contrib_id_validation_result)
        return results


class ReferenceContentValidation(object):

    def __init__(self, reference_xml, previous_refxml):
        self.refxml = reference_xml
        self._mixed = None
        self._source = None
        self._elements_validations = None
        self.previous_refxml = previous_refxml

    def evaluate(self, article_year):
        self.is_valid_publication_type = is_valid_publication_type(
            self.refxml.reference.publication_type)
        self.contrib_names = ', '.join([item.contrib().fullname for item in self.refxml.contrib_xml_items if item is not None])
        r = []
        r.append(self.xml)
        r.append(self.element_citation)
        r.extend(self.mixed_citation)
        r.append(self.publication_type)
        if self.is_valid_publication_type:
            r.extend(self.publication_type_dependence)

        if self.publication_type_other is not None:
            r.append(self.publication_type_other)
        r.extend([item for item in self.elements_validations if item is not None])
        r.extend(self.contrib_xml_items)
        r.extend(self.previous_authors)
        r.extend(self.year(article_year))
        r.extend(self.source)
        return [item for item in r if item is not None]

    @property
    def elements_validations(self):
        if self._elements_validations is None:
            pubtype = self.refxml.reference.publication_type
            self._elements_validations = [
                validate_ref_data_presence(pubtype, 'person-group', self.refxml.contrib_xml_items),
                validate_ref_data_presence(pubtype, 'article-title', self.refxml.article_title, 1),
                validate_ref_data_presence(pubtype, 'chapter-title', self.refxml.chapter_title, 1), 
                validate_ref_data_presence(pubtype, 'publisher-name', self.refxml.publisher_name), 
                validate_ref_data_presence(pubtype, 'publisher-loc', self.refxml.publisher_loc), 
                validate_ref_data_presence(pubtype, 'comment[@content-type="degree"]', self.refxml.degree, 1), 
                validate_ref_data_presence(pubtype, 'conf-name', self.refxml.conference_name, 1), 
                validate_ref_data_presence(pubtype, 'date-in-citation[@content-type="access-date"] ' + _(' or ') + ' date-in-citation[@content-type="update"]', self.refxml.cited_date, 1), 
                validate_ref_data_presence(pubtype, 'ext-link', self.refxml.ext_link),
                validate_ref_data_presence(pubtype, 'volume', self.refxml.volume, 1),
                validate_ref_data_presence(pubtype, 'issue', self.refxml.issue, 1),
                validate_ref_data_presence(pubtype, 'fpage', self.refxml.fpage, 1),
                validate_ref_data_presence(pubtype, 'source', self.refxml.source, 1),
                validate_ref_data_presence(pubtype, 'year', self.refxml.year, 1),
                ]
        return self._elements_validations

    @property
    def normalized_mixed_citation(self):
        if self._mixed is None:
            _mixed = self.refxml.reference.mixed_citation.lower() if self.refxml.reference.mixed_citation is not None else ''
            _mixed = _mixed.replace('[', ' ').replace(']', ' ').replace(',', ' ').replace(';', ' ').replace('.', ' ')
            self._mixed = _mixed
        return self._mixed

    @property
    def normalized_source(self):
        if self._source is None:
            _source = self.refxml.reference.source.lower() if self.refxml.reference.source is not None else ''
            _source = _source.replace('[', ' ').replace(']', ' ').replace(',', ' ').replace(';', ' ').replace('.', ' ')
            self._source = _source
        return self._source

    @property
    def id(self):
        return self.refxml.id

    @property
    def element_citation(self):
        if len(self.refxml.element_citation) > 1:
            return data_validations.is_required_only_one('element-citation')

    @property
    def source(self):
        r = []
        ref_source = self.refxml.reference.source
        r.append(data_validations.is_valid_value('source', ref_source))
        return r

    @property
    def looks_like_thesis(self):
        looks_like = None
        if self.refxml.reference.publication_type != 'thesis':
            for item in self.normalized_mixed_citation.split():
                for word in ['thesis', 'dissert', 'master', 'doctor', 'mestrado', 'doutorado', 'maestr', 'tese']:
                    if item.startswith(word):
                        looks_like = 'thesis'
                        break
        return looks_like

    @property
    def looks_like_journal(self):
        if self.normalized_source is not None:
            if 'journal' in self.normalized_source or 'revista' in self.normalized_source or 'J ' in self.normalized_source or self.normalized_source.endswith('J') or 'J. ' in self.normalized_source or self.normalized_source.endswith('J.'):
                return 'journal'

    @property
    def looks_like_legal_doc(self):
        looks_like = None
        if self.normalized_source is not None:
            if 'Lei ' in self.normalized_source or ('Di' in self.normalized_source and 'Oficial' in self.refxml.reference.source):
                looks_like = 'legal-doc'
            if 'portaria ' in self.normalized_source:
                looks_like = 'legal-doc'
            if 'decreto ' in self.normalized_source:
                looks_like = 'legal-doc'
        return looks_like

    @property
    def looks_like_confproc(self):
        if self.refxml.reference.publication_type != 'confproc':
            if 'conference' in self.normalized_mixed_citation or 'proceeding' in self.normalized_mixed_citation or 'meeting' in self.normalized_mixed_citation:
                return 'confproc'

    @property
    def publication_type(self):
        return data_validations.is_expected_value('@publication-type', self.refxml.reference.publication_type, attributes.PUBLICATION_TYPE, validation_status.STATUS_FATAL_ERROR)

    @property
    def publication_type_dependence(self):
        r = []
        if self.is_valid_publication_type:
            pubtype = self.refxml.reference.publication_type

            looks_like = None
            if pubtype != 'journal':
                looks_like = self.looks_like_journal
            if self.refxml.issue is None and self.refxml.volume is None:
                if self.refxml.fpage is None:
                    looks_like = self.looks_like_thesis
                if 'legal' not in pubtype:
                    looks_like = self.looks_like_legal_doc
                if looks_like is False:
                    looks_like = self.looks_like_confproc
            if looks_like is not None:
                r.append(('@publication-type', validation_status.STATUS_ERROR, _('Be sure that {item} is correct. ').format(item='@publication-type=' + str(pubtype)) + _('This reference looks like {publication_type}. ').format(publication_type=looks_like)))
        return r

    @property
    def publication_type_other(self):
        if self.refxml.reference.publication_type == 'other':
            return ('@publication-type', validation_status.STATUS_WARNING, '@publication-type=' + self.refxml.reference.publication_type + '. ' + data_validations.expected_values_message(_(' or ').join([v for v in attributes.PUBLICATION_TYPE if v != 'other'])))

    @property
    def xml(self):
        return ('xml', validation_status.STATUS_INFO, self.refxml.xml)

    @property
    def mixed_citation(self):
        r = []
        ref_mixed_citation = self.refxml.reference.mixed_citation
        if len(self.refxml.mixed_citation) > 1:
            r.append(data_validations.is_required_only_one('mixed_citation'))
        elif ref_mixed_citation is None:
            r.append(data_validations.is_required_data('mixed_citation', ref_mixed_citation))
        else:
            for label, data in [('source', self.refxml.reference.source), ('year', self.refxml.reference.year), ('ext-link', self.refxml.reference.ext_link)]:
                r.extend(element_in_mixed_citation(label, data, self.refxml.reference.mixed_citation))
        return r

    @property
    def person_group_type(self):
        r = []
        groups_type = [item[0] for item in self.refxml.person_group_xml_items]
        if ' In: ' in self.refxml.reference.mixed_citation and len(groups_type) < 2:
            r.append(('@person-group-type', validation_status.STATUS_FATAL_ERROR, _(u'It is expected more than one person-group. ')))
        if len(groups_type) > 1:
            no_repetition = list(set(groups_type))
            if not len(groups_type) == len(no_repetition):
                r.append(('@person-group-type', validation_status.STATUS_FATAL_ERROR, _(u'Use @person-group-type to identify the person role. You have identified {} groups. @person-group must have different value for each one. '.format(len(groups_type)))))
        return r

    @property
    def previous_authors(self):
        r = []
        q_previous = self.refxml.xml.count('_'*6)
        if q_previous > 0:
            # (role, authors, etal)
            found = False
            previous = []
            if self.previous_refxml is not None:
                previous = [xml_utils.node_text(item) for item in self.previous_refxml.person_group_nodes]
            curr = [xml_utils.node_text(item) for item in self.refxml.person_group_nodes]
            for item in curr:
                if item in previous:
                    found = True
                    break
            if found is False:
                found_text = _('Found {}. ').format(
                    html_reports.format_text_as_xml(''.join(curr)))
                expected_text = _('Expected {}. ').format(
                    html_reports.format_text_as_xml(''.join(previous)))
                r.append(
                    (
                        'person-group',
                        validation_status.STATUS_FATAL_ERROR,
                        _('{} indicates the authors of this reference must be the same as the authors of the previous reference. ').format('_'*6) + found_text + expected_text
                        , self.previous_refxml.xml if self.previous_refxml is not None else '')
                    )
        return r

    @property
    def contrib_xml_items(self):
        result = []
        for contrib_xml in self.refxml.contrib_xml_items:
            if len(contrib_xml.surnames + contrib_xml.fnames) > 0:
                result.extend(PersonValidation(contrib_xml.contrib(), []).validate())
        return result

    def year(self, article_year):
        r = []
        label_year, value_year = article_year
        _y = self.refxml.reference.formatted_year
        if len(self.refxml.year) > 1:
            r.append(('year', validation_status.STATUS_FATAL_ERROR, _('Identify as "year" the more recent publication date. ')))
        if _y is not None:
            if _y.isdigit():
                if _y > value_year:
                    ref_year_label = 'ref/year ({})'.format(_y)
                    art_year_label = '{}/year ({})'.format(label_year, value_year)
                    r.append(('year', validation_status.STATUS_FATAL_ERROR, _('{} should not be greater than {}. ').format(ref_year_label, art_year_label)))
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
        return data_validations.display_value('publisher-name', self.refxml.publisher_name)

    @property
    def publisher_loc(self):
        return data_validations.display_value('publisher-loc', self.refxml.publisher_loc)

    @property
    def fpage(self):
        return data_validations.conditional_required('fpage', self.refxml.fpage)


def validate_orcid(orcid):
    # [0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]{1}
    if len(orcid) != 19:
        return False
    pattern = re.compile("[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[X0-9]{1}")
    return pattern.match(orcid) is not None
