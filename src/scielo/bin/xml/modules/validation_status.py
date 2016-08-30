

from __init__ import _


STATUS_OK = '[OK]'
STATUS_VALID = '[VALID]'
STATUS_INFO = '[INFO]'
STATUS_ERROR = '[ERROR]'
STATUS_FATAL_ERROR = '[FATAL ERROR]'
STATUS_WARNING = '[WARNING]'
STATUS_BLOCKING_ERROR = '[BLOCKING ERROR]'

STATUS_LABELS = {
                 STATUS_BLOCKING_ERROR: _('blocking errors'),
                 STATUS_FATAL_ERROR: _('fatal errors'),
                 STATUS_ERROR: _('errors'),
                 STATUS_WARNING: _('warnings'),}

STATUS_LEVEL_ORDER = [STATUS_BLOCKING_ERROR, STATUS_FATAL_ERROR, STATUS_ERROR, STATUS_WARNING]
STYLE_CHECKER_ERROR_TYPES = ['', 'Total of fatal errors = ', 'Total of errors = ', 'Total of warnings = ']


def message_style(label_and_number_items):
    s = 'ok'
    for label, number in label_and_number_items:
        if int(number) > 0:
            s = label
            break
    return s.replace(' ', '')[:-1]


def style(value):
    r = None
    if STATUS_BLOCKING_ERROR in value:
        r = 'blockingerror'
    elif STATUS_FATAL_ERROR in value:
        r = 'fatalerror'
    elif STATUS_ERROR in value:
        r = 'error'
    elif STATUS_WARNING in value:
        r = 'warning'
    elif STATUS_OK in value:
        r = 'ok'
    elif STATUS_INFO in value:
        r = 'info'
    elif STATUS_VALID in value:
        r = 'valid'
    return r
