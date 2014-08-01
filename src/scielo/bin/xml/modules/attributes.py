

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


def article_title_status():
    status = {}
    status['required'] = ['journal', ]
    status['allowed'] = ['confproc', 'conf-proc', 'newspaper', 'in-press', 'manuscript']
    status['not_allowed'] = ['book', 'book-part', 'thesis', 'software']
    return status


def chapter_title_status():
    status = {}
    status['required'] = ['book-part']
    status['not_allowed'] = ['journal', 'confproc', 'conf-proc', 'newspaper', 'in-press', 'manuscript', 'book']
    status['allowed'] = ['book-part']
    return status
