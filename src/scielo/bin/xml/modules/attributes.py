# coding=utf-8

from datetime import datetime

from __init__ import _
import validation_status
import article_utils
import ws_requester


SPS_MIN_DATE = datetime(2012, 06, 01)
SPS_MIN_DATEISO = 20120601

SPS_versions_expiration_dates = {
                'sps-1.5': '20171001',
                'sps-1.4': '20170401',
                'sps-1.3': '20160901',
                'sps-1.2': '20160301',
                'sps-1.1': '20150901',
                'sps-1.0': '20150301',
                'pre-sps': '20140901',
}

# pre-sps: 2012-06 a 2014-09
# sps-1.0: 2014-03 a 2015-03
# sps-1.1: 2014-09 a 2015-09
# sps-1.2: 2015-03 a 2016-03
# sps-1.3: 2015-09 a 2016-09


SPS_expiration_dates_versions = {v: k for k, v in SPS_versions_expiration_dates.items()}

REFTYPE_AND_TAG_ITEMS = {'aff': ['aff'], 'app': ['app'], 'author-notes': ['fn'], 'bibr': ['ref'], 'boxed-text': ['boxed-text'], 'contrib': ['fn'], 'corresp': ['corresp'], 'disp-formula': ['disp-formula'], 
            'fig': ['fig', 'fig-group'], 
            'fn': ['fn'], 'list': ['list'], 'other': ['?'], 'supplementary-material': ['supplementary-material'], 
            'table': ['table-wrap', 'table-wrap-group']
            }

DOCTOPIC = {
                'research-article': 'oa',
                'editorial': 'ed',
                'abstract': 'zz',
                'announcement': 'zz',
                'article-commentary': 'co',
                'case-report': 'cr',
                'letter': 'le',
                'review-article': 'ra',
                'rapid-communication': 'sc',
                'addendum': 'zz',
                'book-review': 'rc',
                'books-received': 'zz',
                'brief-report': 'rn',
                'calendar': 'zz',
                'clinical-trial': 'oa',
                'collection': 'zz',
                'correction': 'er',
                'discussion': 'ed',
                'dissertation': 'ed',
                'editorial-material': 'ed',
                'in-brief': 'pr',
                'introduction': 'ed',
                'meeting-report': 'zz',
                'news': 'zz',
                'obituary': 'zz',
                'oration': 'zz',
                'partial-retraction': 'partial-retraction',
                'product-review': 'zz',
                'reply': 'reply',
                'reprint': 'zz',
                'retraction': 're',
                'translation': 'zz',
                'technical-report': 'oa',
                'other': 'zz',
}

DOCTOPIC_IN_USE = [
    'article-commentary', 
    'book-review', 
    'brief-report', 
    'case-report', 
    'correction', 
    'editorial', 
    'in-brief', 
    'letter', 
    'other', 
    'rapid-communication', 
    'research-article', 
    'partial-retraction', 
    'retraction', 
    'reply', 
    'review-article', 
    ]

AUTHORS_REQUIRED_FOR_DOCTOPIC = [
    'article-commentary', 
    'book-review', 
    'brief-report', 
    'case-report', 
    'editorial', 
    'letter', 
    'rapid-communication', 
    'research-article', 
    'reply', 
    'review-article', 
    ]

ABSTRACT_REQUIRED_FOR_DOCTOPIC = [
    'brief-report', 
    'case-report', 
    'research-article', 
    'review-article', 
    ]

ABSTRACT_UNEXPECTED_FOR_DOCTOPIC = [
    'editorial', 
    'in-brief', 
    'letter', 
    'other', 
    ]

REFS_REQUIRED_FOR_DOCTOPIC = [
    'brief-report', 
    'case-report', 
    'rapid-communication', 
    'research-article', 
    'review-article', 
    ]

TOC_SECTIONS = { 
    u'carta': u'letter', 
    u'revisão': u'review', 
    u'resenha': u'review', 
    u'reseña': u'review', 
    u'origin': u'research', 
    u'informe': u'report', 
    u'revisión': u'review', 
    u'relato': u'report', 
    u'artigo': u'article', 
    u'artículo': u'article', 
    u'errata': u'correction', 
    u'erratum': u'correction'
}


ROLE = {
    'author': 'ND',
    'editor': 'ED',
    'assignee': 'assignee',
    'compiler': 'compiler',
    'director': 'director',
    'guest-editor': 'guest-editor',
    'inventor': 'inventor',
    'transed': 'transed',
    'translator': 'TR',    
}


BIBLIOMETRICS_USE = ['journal', 'book', 'thesis', 'confproc']

scholars_level1 = ['journal', 'book']
scholars_level2 = ['thesis', 'confproc']

PUBLICATION_TYPE = []
PUBLICATION_TYPE.append('journal')
PUBLICATION_TYPE.append('book')
PUBLICATION_TYPE.append('thesis')
PUBLICATION_TYPE.append('patent')
PUBLICATION_TYPE.append('report')
PUBLICATION_TYPE.append('software')
PUBLICATION_TYPE.append('webpage')
PUBLICATION_TYPE.append('database')
PUBLICATION_TYPE.append('confproc')
PUBLICATION_TYPE.append('legal-doc')
PUBLICATION_TYPE.append('newspaper')
PUBLICATION_TYPE.append('other')


REFERENCE_REQUIRED_SUBELEMENTS = {}
REFERENCE_REQUIRED_SUBELEMENTS['journal'] = ['article-title', 'person-group', 'year', 'source']
REFERENCE_REQUIRED_SUBELEMENTS['book'] = ['year', 'source']
REFERENCE_REQUIRED_SUBELEMENTS['confproc'] = ['conf-name', 'source', 'year']
REFERENCE_REQUIRED_SUBELEMENTS['thesis'] = ['comment', 'source', 'year']
REFERENCE_REQUIRED_SUBELEMENTS['webpage'] = ['ext-link', 'date-in-citation[@content-type="access-date"]']


REFERENCE_NOT_ALLOWED_SUBELEMENTS = {}
REFERENCE_NOT_ALLOWED_SUBELEMENTS['journal'] = ['chapter-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['book'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['thesis'] = ['article-title', 'conf-date', 'conf-loc', 'conf-name', 'conf-num', 'conf-sponsor', 'conf-theme', 'conference', 'patent']
REFERENCE_NOT_ALLOWED_SUBELEMENTS['confproc'] = ['chapter-title', 'patent']

LANGUAGES = {
    'en': _('English'),
    'pt': _('Portuguese'),
    'es': _('Spanish'),
    'af': _('Afrikaans'),
    'ar': _('Arabic'),
    'bg': _('Bulgarian'),
    'zh': _('Chinese'),
    'cs': _('Czech'),
    'da': _('Danish'),
    'nl': _('Dutch'),
    'eo': _('Esperanto'),
    'fr': _('French'),
    'de': _('German'),
    'gr': _('Greek'),
    'he': _('Hebrew'),
    'hi': _('Hindi'),
    'hu': _('Hungarian'),
    'in': _('Indonesian'),
    'ia': _('Interlingua'),
    'ie': _('Interlingue'),
    'it': _('Italian'),
    'ja': _('Japanese'),
    'ko': _('Korean'),
    'la': _('Latin'),
    'no': _('Norwergian'),
    'pl': _('Polish'),
    'ro': _('Romanian'),
    'ru': _('Russian'),
    'sa': _('Sanskrit'),
    'sh': _('Serbo-Croat'),
    'sk': _('Slovak'),
    'sn': _('Slovenian'),
    'sv': _('Swedish'),
    'tr': _('Turkish'),
    'uk': _('Ukrainian'),
    'ur': _('Urdu'),
    'zz': _('Other'),
    'gl': _('Galician'),
    'eu': _('Basque'),
    'ca': _('Catalan'),
}


COUNTRY_CODES = [
 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 
 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 
 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 
 'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 
 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 
 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 
 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 
 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 
 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 
 'IS', 'IT', 'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 
 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 
 'KV',
 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 
 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 
 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 
 'NR', 'NU', 'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 
 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 
 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 
 'SN', 'SO', 'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 
 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 
 'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 
 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW',
 ]

PERMISSION_ELEMENTS = ['license', 'copyright-holder', 'copyright-year', 'copyright-statement']

related_articles_type = ['corrected-article', 'article-commentary', 'press-release', 'retracted-article']

CONTRIB_ID_URLS = {
    'lattes': 'http://lattes.cnpq.br/',
    'orcid': 'http://orcid.org/',
    'researchid': 'http://www.researcherid.com/rid/',
    'scopus': 'https://www.scopus.com/authid/detail.uri?authorId=',  
}

LICENSES = [
    'http://creativecommons.org/licenses/by/4.0/',
    'http://creativecommons.org/licenses/by/3.0/',
    'http://creativecommons.org/licenses/by-nc/4.0/',
    'http://creativecommons.org/licenses/by-nc/3.0/',
    'http://creativecommons.org/licenses/by-nc-nd/3.0/',
    'http://creativecommons.org/licenses/by-nc-nd/4.0/',
    'http://creativecommons.org/licenses/by/3.0/igo/',
    'http://creativecommons.org/licenses/by-nc/3.0/igo/',
    'http://creativecommons.org/licenses/by-nc-nd/3.0/igo/',
    'https://creativecommons.org/licenses/by/4.0/',
    'https://creativecommons.org/licenses/by/3.0/',
    'https://creativecommons.org/licenses/by-nc/4.0/',
    'https://creativecommons.org/licenses/by-nc/3.0/',
    'https://creativecommons.org/licenses/by-nc-nd/3.0/',
    'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'https://creativecommons.org/licenses/by/3.0/igo/',
    'https://creativecommons.org/licenses/by-nc/3.0/igo/',
    'https://creativecommons.org/licenses/by-nc-nd/3.0/igo/',
]

SPS_HELP_ELEMENTS = [
    'abbrev-journal-title',
    'abstract',
    'ack',
    'addr-line',
    'aff',
    'app',
    'article-categories',
    'article-id',
    'article-meta',
    'article-title',
    'article',
    'attrib',
    'author-notes',
    'award-group',
    'award-id',
    'back',
    'body',
    'boxed-text',
    'caption',
    'chapter-title',
    'collab',
    'comment',
    'conf-date',
    'conf-loc',
    'conf-name',
    'contrib-group',
    'contrib-id',
    'contrib',
    'copyright-holder',
    'copyright-statement',
    'copyright-year',
    'corresp',
    'country',
    'counts',
    'date-in-citation',
    'date',
    'day',
    'def-list',
    'disp-formula',
    'disp-quote',
    'edition',
    'element-citation',
    'elocation-id',
    'email',
    'etal',
    'ext-link',
    'fig',
    'fn-group',
    'fn',
    'fpage',
    'front-stub',
    'front',
    'funding-group',
    'funding-source',
    'funding-statement',
    'given-names',
    'glossary',
    'history',
    'inline-formula',
    'inline-graphic',
    'inline-supplementary-material',
    'institution',
    'isbn',
    'issn',
    'issue',
    'journal-id',
    'journal-meta',
    'journal-title-group',
    'journal-title',
    'kwd-group',
    'kwd',
    'label',
    'license',
    'list',
    'lpage',
    'media',
    'mixed-citation',
    'month',
    'name',
    'named-content',
    'on-behalf-of',
    'p',
    'page-range',
    'patent',
    'permissions',
    'person-group',
    'prefix',
    'product',
    'pub-date',
    'pub-id',
    'publisher-loc',
    'publisher-name',
    'publisher',
    'ref-list',
    'ref',
    'related-article',
    'response',
    'role',
    'season',
    'sec',
    'sig-block',
    'size',
    'source',
    'sub-article',
    'subj-group',
    'suffix',
    'supplementary-material',
    'surname',
    'table-wrap-foot',
    'table-wrap',
    'table',
    'title-group',
    'trans-abstract',
    'trans-title-group',
    'trans-title',
    'verse-group',
    'volume',
    'xref',
    'year',
]


def normalize_doctopic(_doctopic):
    r = DOCTOPIC.get(_doctopic)
    return _doctopic if r == '??' else r


def normalize_role(_role):
    r = ROLE.get(_role)
    if r == '??' or _role is None or r is None:
        r = 'ND'
    return r


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
    compl = ''
    items = []
    if value is None or value == '':
        if is_required(publication_type, label):
            problem = _('{requirer} requires {required}. ').format(requirer='@publication-type="' + publication_type + '"', required=label)
            compl = _('If the reference has no {label}, ignore this message. ').format(label=label)
            items = ['@publication-type', _('the elements of this reference')]
    else:
        if not is_allowed_element(publication_type, label):
            problem = _('{label} is not allowed for {item}. ').format(label=label, item='@publication-type=' + publication_type)
            items = ['@publication-type', label, value]
    if len(problem) > 0:
        problem += _('. Be sure that you have correctly identified: ') + ', '.join(items)
        problem += compl
    return problem


def doctopic_label(code):
    label = [k for k, v in DOCTOPIC.items() if v == code]
    if len(label) == 0:
        label = None
    else:
        label = label[0]
    return label


def suggestions_of_article_type_by_section_title(section_title):
    suggestions = []
    if section_title is not None:
        lower_section_title = section_title.lower().strip()
        if 'retra' in lower_section_title:
            suggestions.append('retraction')
        elif 'abstract' in lower_section_title or 'resum' in lower_section_title:
            suggestions.append('abstract')
        elif 'book' in lower_section_title or 'resenha' in lower_section_title or u'reseñ' in lower_section_title:
            suggestions.append('book-review')
        elif 'brief report' in lower_section_title or ('pesquisa' in lower_section_title and 'nota' in lower_section_title) or ('research' in lower_section_title and 'note' in lower_section_title):
            suggestions.append('brief-report')
        elif 'case' in lower_section_title or 'caso' in lower_section_title:
            suggestions.append('case-report')
        elif 'correction' in lower_section_title or 'errat' in lower_section_title:
            suggestions.append('correction')
        elif 'carta' in lower_section_title or 'letter' in lower_section_title or 'reply' in lower_section_title or 'correspond' in lower_section_title:
            suggestions.append('letter')
        elif 'editoria' in lower_section_title:
            suggestions.append('editorial')
        elif 'interview' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'entrevista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'point' in lower_section_title and 'view' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'ponto' in lower_section_title and 'vista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'punto' in lower_section_title and 'vista' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'opini' in lower_section_title:
            suggestions.append('editorial-material')
        elif 'communication' in lower_section_title or 'comunica' in lower_section_title:
            suggestions.append('rapid-communication')
        elif 'atualiza' in lower_section_title or 'actualiza' in lower_section_title or 'updat' in lower_section_title:
            suggestions.append('rapid-communication')
        elif 'art' in lower_section_title and 'origin' in lower_section_title:
            suggestions.append('research-article')
        elif 'review' in lower_section_title and 'article' in lower_section_title:
            suggestions.append('review-article')
        elif 'review' in lower_section_title and 'article' in lower_section_title:
            suggestions.append('review-article')
        elif 'revis' in lower_section_title and ('artigo' in lower_section_title or u'artículo' in lower_section_title):
            suggestions.append('review-article')
        elif ('tech' in lower_section_title and 'article' in lower_section_title) or (u'técnico' in lower_section_title and 'informe' in lower_section_title) or (u'técnico' in lower_section_title and u'relatório' in lower_section_title):
            suggestions.append('technical-report')
        elif 'comment' in lower_section_title or 'coment' in lower_section_title:
            suggestions.append('article-commentary')
        elif 'article' in lower_section_title or u'artículo' in lower_section_title or 'artigo' in lower_section_title:
            suggestions.append('research-article')
        elif 'original' in lower_section_title:
            suggestions.append('research-article')

    if 'editorial-material' in suggestions:
        suggestions = [item.replace('editorial-material', 'other') for item in suggestions]
    return suggestions


def normalize_section_title(text):
    if text is None:
        text = ''

    text = text.lower().replace('-', ' ')
    text = text.replace('update article', 'rapid communication')
    text = text.replace(u'artículo de actualización', 'rapid communication')
    text = text.replace(u'artigo de atualização', 'rapid communication')
    text = text.replace(u'comunicação breve', 'rapid communication')
    text = text.replace(u'comunicación breve', 'rapid communication')
    text = text.replace(u'nota técnica', 'brief report')
    text = text.replace(u'nota de pesquisa', 'brief report')
    text = text.replace(u'nota de investigación', 'brief report')
    text = text.replace(u'research note', 'brief report')
    text = text.replace(u'relato breve', 'brief report')
    text = text.replace(u'informe breve', 'brief report')

    text = ' '.join([item for item in text.split(' ') if len(item) > 2])

    text = ' '.join([item for item in sorted(text.split(' '))])
    if text is not None:
        for term, transl in TOC_SECTIONS.items():
            text = text.replace(term, transl)
    return text


def check_lang(lang):
    if lang in LANGUAGES.keys():
        return (True, LANGUAGES.get(lang))
    else:
        return (False, _('{value} is an invalid value for {label}. ').format(value=lang, label='@xml:lang') + _('Expected values: {expected}. ').format(expected=', '.join(sorted(LANGUAGES.keys())) + '. ' + '|'.join(sorted([k + '(' + v + ')' for k, v in LANGUAGES.items()]))))


def expected_sps_versions(article_dateiso):
    sps_dateiso_items = sorted(SPS_expiration_dates_versions.keys())
    sps_datetime_items = [article_utils.dateiso2datetime(item) for item in sps_dateiso_items]
    article_datetime = article_utils.dateiso2datetime(article_dateiso)
    min_version = str(None)
    max_version = SPS_expiration_dates_versions.get(sps_dateiso_items[len(sps_dateiso_items)-1])
    valid_versions = [min_version, max_version]

    if article_datetime is not None:
        diff = SPS_MIN_DATE - article_datetime
        if diff.days > 0:
            # data do artigo é antiga, anterior a 2012
            # permitido qualquer versão
            valid_versions = [item for item in SPS_expiration_dates_versions.values() if item != 'pre-sps']
        else:
            i = 0
            k = 0
            for sps_datetime in sps_datetime_items:
                diff = article_datetime - sps_datetime
                if diff.days < 0:
                    valid_versions = []
                    for k in range(i, len(sps_dateiso_items)):
                        _sps_value = SPS_expiration_dates_versions.get(sps_dateiso_items[k])
                        if _sps_value == 'pre-sps':
                            _sps_value = 'None'
                        valid_versions.append(_sps_value)
                    break
                i += 1
    return list(set(sorted(valid_versions)))


def sps_current_versions():
    sps_dateiso_items = sorted(SPS_expiration_dates_versions.keys())
    sps_dateiso_items.reverse()
    currents = []
    for item in sps_dateiso_items[:2]:
        currents.append(SPS_expiration_dates_versions.get(item))
    return list(set(sorted(currents)))


def sps_version_expiration_days(sps_version):
    days = None
    if sps_version is None:
        sps_version = 'pre-sps'
    sps_version_datetime = SPS_versions_expiration_dates.get(sps_version)
    if sps_version_datetime is not None:
        sps_version_datetime = article_utils.dateiso2datetime(sps_version_datetime)
        now = datetime.now()
        diff = sps_version_datetime - now
        days = diff.days
    return days


def validate_article_type_and_section(article_type, article_section, has_abstract):
    results = []
    if article_type is None:
        article_type = 'None'
    if article_section is None:
        article_section = 'None'

    status = ''
    suggestions = suggestions_of_article_type_by_section_title(article_section)
    if not article_type in suggestions:
        suggestions_msg = ''
        status = validation_status.STATUS_ERROR
        if len(suggestions) == 0:
            status = validation_status.STATUS_WARNING
            if has_abstract is True:
                suggestions = ABSTRACT_REQUIRED_FOR_DOCTOPIC
            else:
                suggestions = [item for item in DOCTOPIC_IN_USE if not item in ABSTRACT_REQUIRED_FOR_DOCTOPIC]
    if not article_type in suggestions:
        suggestions_msg = _('{value} is an invalid value for {label}. ').format(value=article_type, label='@article-type') + _('Expected values: {expected}. ').format(expected=_(' or ').join(suggestions))
        results.append(('@article-type', status, _('Be sure that the elements {elem1} and {elem2} are properly identified. ').format(elem1='@article-type', elem2=_('section title') + '(' + article_section + ')') + suggestions_msg))

    return results


def validate_iso_country_code(iso_country_code):
    r = []
    if iso_country_code is None:
        r.append(('aff/country/@country', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='aff/country/@country')))
    else:
        if not iso_country_code in COUNTRY_CODES:
            r.append(('aff/country/@country', validation_status.STATUS_FATAL_ERROR, 
                _('{value} is an invalid value for {label}. ').format(value=iso_country_code, label='aff/country/@country') + _('Expected values: {expected}. ').format(expected=' | '.join(COUNTRY_CODES))))
    return r


def validate_license_href(license_href):
    result = None
    if license_href is None:
        result = ('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('{label} is required. ').format(label='license/@href'))
    elif license_href in LICENSES or license_href + '/' in LICENSES:
        result = ('license/@xlink:href', validation_status.STATUS_VALID, license_href)
    else:
        result = ('license/@xlink:href', validation_status.STATUS_WARNING, _('{value} is an invalid value for {label}. ').format(value=license_href, label='license/@href') + _('Expected values: {expected}. ').format(expected=_('or').join(LICENSES)))
        #if not ws_requester.wsr.is_valid_url(license_href):
        #    result = ('license/@xlink:href', validation_status.STATUS_FATAL_ERROR, _('{value} is an invalid value for {label}. ').format(value=license_href, label='license/@href'))
    return result
