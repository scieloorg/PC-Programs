# coding=utf-8

PUBLICATION_TYPE = []
PUBLICATION_TYPE.append('journal')
PUBLICATION_TYPE.append('book')
PUBLICATION_TYPE.append('book-part')
PUBLICATION_TYPE.append('conf-proc')
PUBLICATION_TYPE.append('thesis')
PUBLICATION_TYPE.append('patent')
PUBLICATION_TYPE.append('report')
PUBLICATION_TYPE.append('software')
PUBLICATION_TYPE.append('web')
PUBLICATION_TYPE.append('unidentified')
PUBLICATION_TYPE.append('confproc')
PUBLICATION_TYPE.append('scientific-technical-report')
PUBLICATION_TYPE.append('newspaper')
PUBLICATION_TYPE.append('legal-doc')
PUBLICATION_TYPE.append('in-press')
PUBLICATION_TYPE.append('poster')
PUBLICATION_TYPE.append('manuscript')
PUBLICATION_TYPE.append('database')
PUBLICATION_TYPE.append('web-site')
PUBLICATION_TYPE.append('standard')
PUBLICATION_TYPE.append('guidelines')
PUBLICATION_TYPE.append('letter')
PUBLICATION_TYPE.append('email')
PUBLICATION_TYPE.append('forum')
PUBLICATION_TYPE.append('other')


REFERENCE_REQUIRED_SUBELEMENTS = {}
REFERENCE_REQUIRED_SUBELEMENTS['journal'] = ['article-title']
REFERENCE_REQUIRED_SUBELEMENTS['book-part'] = ['chapter-title']
REFERENCE_REQUIRED_SUBELEMENTS['confproc'] = ['conf-name']
REFERENCE_REQUIRED_SUBELEMENTS['conf-proc'] = ['conf-name']
REFERENCE_REQUIRED_SUBELEMENTS['web'] = ['ext-link', 'date-in-citation[@content-type="access-date"]']
REFERENCE_REQUIRED_SUBELEMENTS['web-site'] = ['ext-link', 'date-in-citation[@content-type="access-date"]']


REFERENCE_NOT_ALLOWED_SUBELEMENTS = {}
REFERENCE_NOT_ALLOWED_SUBELEMENTS['journal'] = ['chapter-title']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['book'] = ['article-title']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['book-part'] = ['article-title']


def is_required(publication_type, label):
    return label in REFERENCE_REQUIRED_SUBELEMENTS.get(publication_type, [])


def is_allowed_element(publication_type, label):
    if is_required(publication_type, label):
        r = True
    else:
        r = not label in REFERENCE_NOT_ALLOWED_SUBELEMENTS.get(publication_type, [])
    return r


def validate_element(publication_type, label, value):
    problem = ''
    if value is None or value == '':
        if is_required(publication_type, label):
            problem = label + ' is required for @publication-type=' + publication_type
    else:
        if not is_allowed_element(publication_type, label):
            problem = label + ' is not allowed for @publication-type=' + publication_type
    return problem
