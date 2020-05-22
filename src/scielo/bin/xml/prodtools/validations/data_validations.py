# coding=utf-8

from prodtools import _
from prodtools.reports import validation_status
from prodtools.data import attributes


def label_equal_value(label, value):
    if value is None:
        value = str(value)
    return label + '="' + value + '"'


def invalid_labels_and_values(labels_and_values):
    return _(u'The items are not correct. Check: {values}. ').format(values='; '.join([label_equal_value(label, value) for label, value in labels_and_values]))


def check_lang(elem_name, lang):
    status, msg = attributes.check_lang(lang)
    if status is False:
        status = validation_status.STATUS_FATAL_ERROR
    else:
        status = validation_status.STATUS_OK
    return (elem_name + '/@xml:lang', status, msg)


def conditional_required(label, value, condition_msg=_('if applicable')):
    status, message = validate_value(value)
    return (label, status, message) if value is not None else (label, validation_status.STATUS_WARNING, _('{label} is required, {condition}. ').format(label=label, condition=condition_msg))


def required_one(label, value):
    return (label, validation_status.STATUS_OK, display_attributes(value)) if value is not None else (label, validation_status.STATUS_ERROR, _('It is required at least one {label}. ').format(label=label))


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
    for term in invalid_terms:
        if term.upper() in value.upper():
            r = False
            invalid = term
            break
    if not r:
        return (label, error_or_warning, _('{value} contains invalid {invalid_items_name}: {invalid_items}. ').format(value='<data>' + value + '</data> ', invalid_items_name=_('characters'), invalid_items=invalid))
    else:
        return (label, validation_status.STATUS_OK, value)


def warn_unexpected_numbers(label, value, max_number=0):
    r = None
    if value is not None:
        #value = xml_utils.htmlent2char(value)
        q_numbers = len([c for c in value if c.isdigit()])
        q_others = len(value) - q_numbers
        if q_numbers > q_others:
            r = (label, validation_status.STATUS_WARNING, _('Be sure that {item} is correct. ').format(item='<' + label + '>' + value + '</' + label + '>'))
    return r


def required_data(label, values, status=validation_status.STATUS_ERROR):
    if values is None or len(values) == 0:
        return [(label, status, _('{label} is required. ').format(label=label))]
    return [(label, validation_status.STATUS_OK, value) for value in values]


def invalid_value_message(label, value, expected=None):
    msg = ''
    if expected is not None:
        msg = expected_values_message(expected)
    return _('{value} is an invalid value for {label}. ').format(value=value, label=label) + msg


def expected_values_message(expected):
    return _('Expected values: {expected}. ').format(expected=expected)


def invalid_value_result(label, value, expected, status=validation_status.STATUS_ERROR):
    return (label, status, invalid_value_message(label, value, expected))


def is_required_only_one(label, status=validation_status.STATUS_FATAL_ERROR):
    return (label, status, _('only one occurrence of {label} is allowed. ').format(label=label))


def is_expected_value(label, value, expected_values, status=validation_status.STATUS_ERROR):
    if expected_values is None:
        return (label, validation_status.STATUS_OK, value)
    if value in expected_values:
        return (label, validation_status.STATUS_OK, value)
    else:
        return invalid_value_result(label, value, ' | '.join(expected_values), status)


def is_required_data(label, value, status=validation_status.STATUS_ERROR):
    if value is None or len(value) == 0:
        return (label, status, _('{label} is required. ').format(label=label))
    else:
        return (label, validation_status.STATUS_OK, value)


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
        message = str(value) if value is None else value
    else:
        message = ';\n'.join(result)
    return (status, message)


def is_valid_value(label, value):
    status, message = validate_value(value)
    return (label, status, message)
