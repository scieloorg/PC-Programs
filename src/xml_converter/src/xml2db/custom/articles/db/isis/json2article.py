# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

from xml2db.json_functions import return_multval, return_singleval

from reuse.items_and_id import id_generate, Items
from xml2db.box_folder_document import Section, TOC

from xml2db.custom.articles.models.journal_issue_article import Journal, JournalIssue, Article, JournalsList, JournalIssuesList 
#from models.json_functions import JSON_Values, JSON_Dates


def normalized_issue_id(json):
    def format(json, key):
        value = json.get(key, '')
        if value.replace('0', '') == '':
            r = ''
        elif value.startswith('0'):
            r = value[1:]
        else:
            r = value
        return r

    vol = format(json, '31')
    num = format(json, '32')
    suppl = format(json, '132')
    compl = format(json, '41')

    if ' pr' == num:
        _i = num.split(' ')
        num = _i[0]
        compl = _i[1]
    n = num.lower().replace('(', '').replace(')', '').split('suppl')
    if len(n) == 2:
        # suppl
        num = n[0].strip()
        suppl = n[1].strip()
        if suppl == '':
            suppl = '0'
    if num == '':
        supplvol = suppl
        supplnum = ''
    else:
        supplvol = ''
        supplnum = suppl
    if num == '' and vol == '':
        num = 'ahead'
    return (vol, supplvol, num, supplnum, compl)


def reset_issue_id(json_data):
    vol, supplvol, num, supplnum, compl = normalized_issue_id(json_data)
    if supplvol != '':
        json_data['132'] = supplvol
    if supplnum != '':
        json_data['132'] = supplnum
    if num != '':
        json_data['32'] = num
    else:
        if '32' in json_data.keys():
            del json_data['32']
    if compl != '':
        json_data['41'] = compl
    return json_data


def return_journals_list(json):
    #json = self.db2json(title_db_filename)
    journal_list = JournalsList()
    json_title = JSON_Journal()
    for json_item in json:
        json_title.load(json_item)
        #print(json_title.journal_title+ '.')
        j = Journal(json_title.journal_title, json_title.journal_issn_id, json_title.journal_acron)
        j.publishers = json_title.publishers
        j.abbrev_title = json_title.journal_abbrev_title

        journal_list.insert(j, False)
    return journal_list


def return_issues_list(json_issues, journals):
    issues_list = JournalIssuesList()

    json_issue = JSON_Issue()
    for json in json_issues:
        json_issue.load(json)
        j = Journal(json_issue.journal_title)
        j = journals.find(j)
        if not j is None:
            json_issue.load(json)
            issue = json_issue.return_issue(j)
            #print(json_issue.journal_title + '.')
            #print(issue.name + '.')
            issues_list.insert(issue, False)
    return issues_list

class JSON_Citations:
    def __init__(self, json_normalizer):
        #self.publication_dateiso = publication_date
        self.json_normalizer = json_normalizer
        # book, conf-proc, journal, patent, thesis, report, 
        # communication, letter, review, list, discussion, standard, and working-paper
        self.doctopic_required_data = {}
        self.doctopic_required_data['journal'] = ['65', '30', '12']
        self.doctopic_required_data['book'] = [ '65', '62', '18',  ]
        self.doctopic_required_data['book-part'] = [ '65', '62', '18',  '12',]
        self.doctopic_required_data['conf-proc'] = ['65', '53', ]
        self.doctopic_required_data['thesis'] = ['65',  '51' ]
        self.doctopic_required_data['patent'] = ['65', '150', ]
        self.doctopic_required_data['report'] = ['65', '58', '60', ]
        self.doctopic_required_data['software'] = ['95', ]
        self.doctopic_required_data['web'] = ['37', '109']
        self.doctopic_required_data['unidentified'] = ['65', ]

        self.doctopic_desirable_data = {}
        self.doctopic_desirable_data['journal'] = []
        self.doctopic_desirable_data['book'] = [ ]
        self.doctopic_desirable_data['book-part'] = [ ]
        self.doctopic_desirable_data['conf-proc'] = [ ]
        self.doctopic_desirable_data['thesis'] = [ ]
        self.doctopic_desirable_data['patent'] = []
        self.doctopic_desirable_data['report'] = [ ]
        self.doctopic_desirable_data['software'] = [ ]
        self.doctopic_desirable_data['web'] = []
        self.doctopic_desirable_data['unidentified'] = []

        self.suggested_doctopic_order = [30, 18, 51, 53, 37, 150, 58, 95]
        self.suggested_doctopic_order = [ str(i) for i in self.suggested_doctopic_order ]
        
        self.suggested_doctopic = {}
        self.suggested_doctopic['30'] = 'journal'
        self.suggested_doctopic['18'] = 'book'
        self.suggested_doctopic['51'] = 'thesis'
        self.suggested_doctopic['53'] = 'conf-proc'
        self.suggested_doctopic['150'] = 'patent'
        self.suggested_doctopic['58'] = 'report'
        self.suggested_doctopic['95'] = 'software'
        self.suggested_doctopic['37'] = 'web'
        
        self._labels = {}
        self._labels['10'] = 'analytic authors'
        self._labels['11'] = 'corporative analytic authors'
        
        self._labels['16'] = 'monographic authors'
        self._labels['17'] = 'corporative monographic authors'

        self._labels['12'] = 'chapter or article title'
        self._labels['14'] = 'pages'
        self._labels['30'] = 'journal title'
        self._labels['18'] = 'book title'
        self._labels['65'] = 'publication date'
        self._labels['62'] = 'publisher'
        self._labels['63'] = 'edition'
        self._labels['66'] = 'city'
        self._labels['67'] = 'country'
        self._labels['53'] = 'conference name'
        self._labels['50'] = 'institution of the thesis'
        self._labels['51'] = 'thesis degree'
        self._labels['150'] = 'patent'
        self._labels['58'] = 'sponsor'
        self._labels['60'] = 'contract number'
        self._labels['95'] = 'software version'
        self._labels['109'] = 'cited date'
        self._labels['37'] = 'URL'
        self._labels['authors'] = 'authors'
        


    def return_doctopic(self, citation):
        doctopic = 'unidentified'
        if '71' in citation.keys(): 
            doctopic = citation['71'] 
        if not doctopic in self.doctopic_required_data.keys():
            doctopic = 'unidentified'    
        if doctopic == 'unidentified':
            for tag in self.suggested_doctopic_order:
                if tag in citation.keys():
                    doctopic = self.suggested_doctopic[tag]
                    if doctopic == 'book':
                        if '12' in citation.keys():
                            doctopic = 'book-part'
                        break
        
        return doctopic 

    

    def normalize_citation_title_language(self, citation):
        lang = return_singleval(citation, '40')
        if len(lang) == 0:
            lang = 'en'
        if '18' in citation.keys():
            monog_title = citation['18']
            citation['18'] = { 'l': lang, '_': monog_title}

            if '12' in citation.keys():
                if type(citation['12']) == type([]):
                    for title in citation['12']:
                        if not 'l' in title.keys():
                            title['l'] = lang

                elif type(citation['12']) == type({}):
                    if not 'l' in citation['12']:
                        citation['12']['l'] = lang
                else:
                    citation['12'] = { 'l': lang, '_':citation['12']}

        return citation 

    def normalize_citation_issue_number(self, citation):
        if '132' in citation:
            if '32' in citation:
                citation['132'].update({'_':citation['32']})
                citation['32'] = citation['132']

            else:
                citation['32'] = citation['132']
            del citation['132']
        return citation

    def normalize_citation_authors(self, citation):
        # if '30' then is a journal, delete 18
        if '30' in citation.keys():
            del citation['18']

        # roles
        roles = return_multval(citation, 'roles')
        roles = [ self.json_normalizer.normalize_role(r)  for r in roles ]
        #print(roles)
        if len(roles) > 0:
            del citation['roles']

        authors_monog = return_multval(citation, '16')
        #print(authors_monog)
        if len(roles) > 0:
            for a in authors_monog:
                a['r'] = roles[len(roles)-1]
                #print(a)
            if len(authors_monog) > 0:
                citation['16'] = authors_monog
        #print(authors_monog)
        

        authors_analyt = return_multval(citation, '10')
        #print(authors_analyt)
        if len(roles) > 0:
            for a in authors_analyt:
                a['r'] = roles[0]
                #print(a)
            if len(authors_analyt) > 0:
                citation['10'] = authors_analyt
        #print(authors_analyt)
        analytic_title = return_multval(citation, '12')
        
        if len(analytic_title) == 0:
            # monographic
            if len(authors_analyt) > 0:
                citation['16'] = citation['10']
                del citation['10']
            if '11' in citation.keys():
                citation['17'] = citation['11']
                del citation['11']
        

        return citation


    def normalize_citation(self, citation, k, publication_dateiso):
        citation = self.normalize_citation_authors(citation)
        citation = self.normalize_citation_title_language(citation)
        citation = self.json_normalizer.normalize_citation_dates(citation, '964', '65', '64')
        citation = self.normalize_citation_issue_number(citation)

        #citation = self.normalize_citation_doctopic(citation)
        #citation = self.return_issn_and_norm_title(citation)
        citation['865'] = publication_dateiso
        citation = self.join_pages(citation, k)
        
        return citation
    
    def validate_citation_metadata(self, citation):
        required = []
        desirable = []
        
        doctopic = self.return_doctopic(citation)

        if doctopic == 'software' and '63' in citation.keys():
            citation['95'] = citation['63']
            del citation['63']

        for tag in self.doctopic_required_data[doctopic]:
            if not tag in citation.keys():
                if tag in self._labels.keys():
                    required.append(self._labels[tag])
                else:
                    required.append(tag)


        for tag in self.doctopic_desirable_data[doctopic]:
            if not tag in citation.keys():
                if tag in self._labels.keys():
                    desirable.append(self._labels[tag])
                else:
                    desirable.append(tag)

        valid_authors = False

        #print(citation.keys())
        for tag in ['10','11','16','17',]:
            if tag in citation.keys():
                valid_authors = True
                break
        if not valid_authors:
            desirable.append('authors')
        return doctopic, required, desirable

    def join_pages(self, citation, k):
        if '514' in citation.keys():
            citation['14'] = ''
            if type(citation['514']) is dict:
                if 'r' in citation['514'].keys():
                    citation['14'] = citation['514']['r']
                else:
                    if 'f' in citation['514'].keys():
                        citation['14'] = citation['514']['f']
                        if 'l' in citation['514'].keys():
                            if type(citation['514']['l']) == type('') and type(citation['14']) == type(''):
                                if citation['14'].isdigit() and citation['514']['l'].isdigit():
                                    if len(citation['14']) != len(citation['514']['l']):
                                        citation['14'] += '-' + citation['514']['l']
                                    else:
                                        i = 0
                                        citation['14'] += '-'
                                        for c in citation['514']['l']:
                                            if not citation['14'][i:1] == c:
                                                citation['14'] += c
                                            i += 1
                                else:
                                    citation['14'] += '-' + citation['514']['l']
            else:
                print(type(citation['514']))
                print(citation['514'])
        return citation

class JSON_Article:
    def __init__(self, aff_handler, json_citations):
        self.json_normalizer = json_citations.json_normalizer        
        self.aff_handler = aff_handler
        self.json_citations = json_citations
        
    def load(self, json_data, article_report):
        self.json_data = json_data
        self.article_report = article_report

    def return_pagination(self):
        first_page = ''
        last_page = ''
        elocation = ''
        page = return_singleval(self.json_data['f'], '14')
        if type(page) == type({}):
            if 'f' in page.keys():
                first_page =  page['f']
            if 'l' in page.keys():
                last_page =  page['l']
            if 'e' in page.keys():
                elocation = page['e']

        return first_page, last_page, elocation           

    def return_article(self):
        
        doi = return_singleval(self.json_data['f'], '237')
        titles = return_multval(self.json_data['f'], '12')
        authors = return_multval(self.json_data['f'], '10')
        
        first_page, last_page, elocation = self.return_pagination()
        
        if first_page == '':
            first_page = elocation   
        
        
        #article = Article(doi, first_page, last_page)
        article = Article(doi, return_singleval(self.json_data['f'], '121'), first_page, last_page)

        titles = return_multval(self.json_data['f'], '12')
        norm_titles = []
        for t in titles:
            if type(t) == type({}):
                norm_titles.append(t)
            elif type(t) == type([]):
                for t1 in t:
                    if type(t) == type({}):
                        norm_titles.append(t1)

        article.titles = []
        for t in norm_titles:
            if '_' in t.keys():
                article.titles.append(t['_'])


        
        #article.authors = self.format_author_names(authors)
        
        article.section = self.section
        article.json_data = self.json_data
        article.display_data = self.set_display()
        article.display_order =  ['nlm-ta', 'print issn',  'online issn', 'publishers', 'issue label', '@article-type', 'doi', 'pages', 'order', 'received date', 'accepted date', 'publication date (epub)', 'publication date (ppub)', 'titles', 'authors', 'corporative authors', 'abstracts', 'keywords',  ]
        return article

    def _d(self, r, tag, label):
        d = return_singleval(self.json_data['f'], tag)
        if len(d) >0:
            r.append((label, int(d)))
        return r

    def validate_dates(self):
        e = []
        dates = []

        issue_date = return_singleval(self.json_data['f'], '65')

        dates = self._d(dates, '112', 'received date')
        dates = self._d(dates, '114', 'accepted date')
        dates = self._d(dates, '223', 'epub date')

        if not issue_date.endswith('0000'):
            dates = self._d(dates, '65', 'ppub date')

        prev = 0
        prev_label = ''
        if len(dates) > 0:
            print(dates)
            for label, test_date in dates:
                c = test_date
                if prev > c:
                    msg = str(prev) + '(' + prev_label + ') must be a date before ' + str(c) + ' (' + label + ')'
                    e.append(msg)
                else:
                    prev = c
                    prev_label = label
        return e

    def issuelabel(self):
        issue_id = (self.json_data['f'].get('31', ''), self.json_data['f'].get('32', ''), self.json_data['f'].get('131', self.json_data['f'].get('132', '')), self.json_data['f'].get('41', ''))
        prefix = ['v', 'n', 's', '']
        r = ''
        for i in range(0, 4):
            if issue_id[i] != '':
                r += prefix[i] + issue_id[i]
        return r

    def set_display(self):
        r = {}

        fpage, lpage, eloc = self.return_pagination()
        if len(fpage) > 0:
            r['pages'] = fpage
            if len(lpage) > 0:
                r['pages'] += '-' + lpage
        if len(eloc) > 0:
            r['pages'] = eloc + ' (e-location)'

        r['issue label'] = self.issuelabel()
        r['order'] = self.json_data['f'].get('121')

        r['nlm-ta'] = return_singleval(self.json_data['f'], '421')

        r['print issn'] = self.issns('ppub')
        r['online issn'] = self.issns('epub')
        r['@article-type'] = return_singleval(self.json_data['f'], '71')
        r['doi'] = return_singleval(self.json_data['f'], '237')
        r['received date'] = return_singleval(self.json_data['f'], '112')
        r['accepted date'] = return_singleval(self.json_data['f'], '114')
        r['publication date (epub)'] = return_singleval(self.json_data['f'], '223')
        r['publication date (ppub)'] = return_singleval(self.json_data['f'], '65')
        r['publishers'] = return_multval(self.json_data['f'], '62')
        if type(r['publishers']) == type([]):
            r['publishers'] = '\n'.join(r['publishers'])

        authors = return_multval(self.json_data['f'], '10')
        s = ''
        for a in authors:
            s += self.format_author(a)
        r['authors'] = s
        collab = return_multval(self.json_data['f'], '11')
        r['corporative authors'] = '\n'.join(collab)
        titles = return_multval(self.json_data['f'], '12')
        s = ''
        for t in titles:
            s += self.format_title(t)
        r['titles'] = s

        abstracts = return_multval(self.json_data['f'], '83')
        s = ''
        for a in abstracts:
            s += self.format_abstract(a)
        r['abstracts'] = s
        
        
        kwg = return_multval(self.json_data['f'], '85')
        s = ''
        for a in kwg:
            s += self.format_kwd(a)
        r['keywords'] = s
        
       
        return r

        

    def format_author(self, a):
        r = ''
        additional = {}
        if 's' in a.keys():
            r += a['s']
        if 'n' in a.keys():
            r += ', ' + a['n']

        if 'r' in a.keys():
            additional['role'] =  a['r'] 
        if 'z' in a.keys():
            additional['suffix'] = a['z']         
        if 'p' in a.keys():
            additional['prefix'] = a['p'] 
 

        if '1' in a.keys():
            if type(a['1']) == type(''):
                additional['aff'] = a['1']
            elif type(a['1']) == type([]):
                additional['aff'] = ', '.join(a['1']) 
        else:
            additional['aff'] = ' [ WARNING: Missing aff rid ] '

        if len(additional) >0:
            sep = ''
            r += ' ('
            for label, value in additional.items():
                r += sep + label +': ' + value 
                sep = '; '
            r += ')'
        r += '\n'
        return r

    def format_title(self, a):
        r = ''
        if 'l' in a.keys():
            r += '[' + a['l'] + '] '
        if '_' in a.keys():
            r += a['_']
        if 's' in a.keys():
            r += ': ' + a['s']
        
        r += '\n'
        return r

    def format_abstract(self, a):
        r = ''
        if 'l' in a.keys():
            r += '[' + a['l'] + '] '
        if 'a' in a.keys():
            r += a['a']
        
        
        r += '\n'
        return r

    def format_kwd(self, a):
        r = ''
        if 'l' in a.keys():
            r += '[' + a['l'] + '] '
        if 'k' in a.keys():
            r += a['k']
        r += '\n'
        return r

    def validate_issn(self):
        issns = self.issns()
        errors = []
        if not self.json_data['f']['35'] in issns.values():
            errors.append('ISSN in issue: ' + self.json_data['f']['35'] + '. ISSN in article:' + ' and '.join([k + ': ' + v for k, v in issns.items()]))
        val = issns.values()
        if len(val) == 2:
            if val[0] == val[1]:
                errors.append('Print ISSN and E-ISSN must be different:' + ' x '.join(val))
        return errors

    def issns(self, issn_type=None):
        issns = return_multval(self.json_data['f'], '435')
        issns = {issn.get('t'): issn.get('_') for issn in issns}
        if issn_type is None:
            return issns
        else:
            return issns.get(issn_type, '')

    def normalize_issue_data(self, issn_id):
        """
        Normalize the json structure for issue record
        """
        if self.json_data['f']['32'][-2:] == 'pr':
            self.json_data['f']['32'] = self.json_data['f']['32'][0:-2]
            self.json_data['f']['41'] = 'pr'

        self.json_data['f']['35'] = issn_id

        self.json_data['f'] = reset_issue_id(self.json_data['f'])
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '64', '65', '64')
        self.publication_dateiso = return_singleval(self.json_data['f'], '65')

    def set_article_pid(self, alternative_id):
        issueno = return_singleval(self.json_data['f'], '32')
        f = self.json_data['f']

        if issueno == 'ahead':
            article_id_pid = f.get('8121', None)
        else:
            # 8121 = article-id[@pub-id-type='other']
            #  121 = fpage
            # 9121 = fpage/@seq
            #article_id_pid = f.get('8121', f.get('121', alternative_id))
            article_id_pid = f.get('8121', None)
            if article_id_pid is None:
                article_id_pid = f.get('9121', None)
            if article_id_pid is None:
                article_id_pid = f.get('121', None)
        if article_id_pid is None:
            article_id_pid = '0'

        self.json_data['f']['121'] = article_id_pid[-5:]

        if '8121' in self.json_data['f'].keys():
            del self.json_data['f']['8121']
        if '881' in self.json_data['f'].keys():
            if not len(self.json_data['f']['881']) == 23:
                del self.json_data['f']['881']

    def remove_xref_from_article_title(self, text):
        new_value = text
        if '<xref' in text and '</xref>' in text:
            text = text.replace('<xref', '-BREAK-<xref')
            text = text.replace('</xref>', '</xref>-BREAK-')
            parts = text.split('-BREAK-')
            new_value = ''
            for part in parts:
                if '<xref' in part and '</xref>' in part:
                    pass
                else:
                    new_value += part
        return new_value

    def normalize_article_titles(self):
        langs = []
        langs.append(self.json_data['f']['40'])
        trans_langs = self.json_data.get('f', {}).get('601', [])

        if len(trans_langs) > 0:
            if type(trans_langs) is not list:
                trans_langs = [trans_langs]
            for lang in trans_langs:
                langs.append(lang['_'])

        titles = self.json_data.get('f', {}).get('12', [])
        if type(titles) is dict:
            titles = [titles]
        new_titles = []
        for title in titles:
            print(title)
            if type(title) is dict:
                new_titles.append(title)
            elif type(title) is list:
                for t in title:
                    new_titles.append(t)

        print(langs)
        print(new_titles)
        i = 0
        k = 0
        for title in new_titles:
            if title.get('_') is not None:
                new_titles[i]['_'] = self.remove_xref_from_article_title(title.get('_'))
            if title.get('t') is not None:
                if len(langs) > k:
                    new_titles[i]['l'] = langs[k]
                    del new_titles[i]['t']
                    k += 1
            if title.get('s'):
                sep = ': ' if not ':' in new_titles[i]['_'] else ' '
                new_titles[i]['_'] += sep + title.get('s')
                del new_titles[i]['s']
            i += 1
        print('=========normalized=======')
        print(new_titles)
        self.json_data['f']['12'] = new_titles

    def normalize_document_data(self, issue, alternative_id):
        """
        Normalize the json structure of the whole document
        """
        self.json_data['f']['120'] = 'XML_' + return_singleval(self.json_data['f'], '120')
        self.json_data['f']['42'] = '1'
        
        self.normalize_article_titles()
        #seq = self.json_data.get('f', {}).get('9121', None)
        #if not seq is None:

        self.set_article_pid(alternative_id)
        #if 'epub' in self.json_data['f'].keys():
        #    self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], 'epub', '223', 'epub')
        #if 'epub' in self.json_data['f'].keys():
        #    del self.json_data['f']['epub']

        section = Section(return_singleval(self.json_data['f'], '49'))
        print(section.title)
        print(issue.name)
        self.section = issue.toc.return_section(section)
        if self.section is None:
            if 'Article' in section.title and '' == issue.toc.return_sections() and 'ahead' in issue.name:
                section.code = 'nd'
            else:
                section.code = section.title + ' (INVALID) ' + 'The sections of ' + issue.name + ': ' + issue.toc.return_sections()
            self.section = section
        self.json_data['f']['49'] = self.section.code

        self.normalize_metadata_abstracts()
        #self.normalize_metadata_subtitles()
        self.normalize_metadata_authors()
        self.normalize_illustrative_materials()
        self.normalize_affiliations()
        self.normalize_keywords()

        self.json_data['f'] = self.json_normalizer.convert_value(self.json_data['f'], '71', 'doctopic')
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '111', '112', '111')
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '113', '114', '113')

        if 'epub' in self.json_data['f'].keys():
            self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], 'epub', '223', 'epub')
            del self.json_data['f']['epub']
        # ja esta normalizada self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '64', '65', '64')
        if self.json_data['f'].get('65') != issue.json_data.get('65'):
            self.json_data['f']['65'] = issue.json_data.get('65')

        self.json_data['h'] = self.json_normalizer.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.json_normalizer.format_for_indexing(self.json_data['h'])
        #self.json_data['h'] = self.json_data['f']
        #self.json_data['l'] = self.json_data['f']
    
    def normalize_metadata_authors(self):
        """
        Normalize the json structure for authors: 10
        """
        
        authors = return_multval(self.json_data['f'], '10')
        changed = False
        new_authors = []
        for author in authors:
            if 'z' in author.keys():
                author['s'] += ' ' + author['z']
            if '1' in author.keys():
                if type(author['1']) == type([]):
                    #print(self.json_json_data['f']['10'])
                    author['1'] = ' '.join(author['1'])
                    #print(self.json_json_data['f']['10'])
                    changed = True
            if 'r' in author.keys():
                author['r'] = self.json_normalizer.normalize_role(author['r'])
            new_authors.append(author)
        if changed:
            if len(new_authors) == 1:
                self.json_data['f']['10'] = new_authors[0]
            else:
                self.json_data['f']['10'] = new_authors
        
    def normalize_metadata_subtitles(self):
        """
        Normalize the json structure for article-titles: 12
        """
        
        titles = return_multval(self.json_data['f'], '12')
        norm_titles = []
        for t in titles:
            if type(t) == type({}):
                norm_titles.append(t)
            elif type(t) == type([]):
                for t1 in t:
                    if type(t1) == type({}):
                        norm_titles.append(t1)


        new_titles = []
        
        for t in norm_titles:

            if 'x' in t.keys():
                t['_'] = t['_'][0:t['_'].find('<xref')]
                print(t['_'])
            if 's' in t.keys():
                #print(t)
                if ':' in t['_']:
                    t['_'] += ' '
                else:
                    t['_'] += ': ' 
                t['_'] += t['s']
                del t['s']
                #print(t)
            new_titles.append(t)

        if len(new_titles) == 1:
            self.json_data['f']['12'] = new_titles[0]
        elif len(new_titles) > 1:
            self.json_data['f']['12'] = new_titles

    def normalize_metadata_abstracts(self):
        """
        Normalize the json structure for abstracts: 83
        """
        
        abstracts = return_multval(self.json_data['f'], '83')
        norm_abstracts = []
        for t in abstracts:
            if type(t) == type({}):
                norm_abstracts.append(t)
            elif type(t) == type([]):
                for t1 in t:
                    if type(t1) == type({}):
                        norm_abstracts.append(t1)


        if len(norm_abstracts) == 1:
            self.json_data['f']['83'] = norm_abstracts[0]
        elif len(norm_abstracts) > 1:
            self.json_data['f']['83'] = norm_abstracts

    def normalize_illustrative_materials(self):
        """
        Normalize the json structure for illustrative_materials: 38
        """
        types = {'900': 'TAB', '901': 'GRA'}
        illustrative_materials = []

        for tag, type in types.items():
            count = return_singleval(self.json_data['f'], tag)
            if len(count)>0:
                if int(count)>0:
                    illustrative_materials.append(type)
                del self.json_data['f'][tag]
        
        if len(illustrative_materials) > 0:
            self.json_data['f']['38'] = illustrative_materials
        else:
            self.json_data['f']['38'] = 'ND'
        
    def normalize_affiliations(self):
        """
        Normalize the json structure for affiliations: 70
        """
        
        affiliations = return_multval(self.json_data['f'], '70')

        new_affiliations = self.aff_handler.normalize_affiliations(affiliations)

        
        id = ''
        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
            if 'i' in new_affiliations[0].keys():
                id = new_affiliations[0]['i']
    
        if id != '':
            authors = return_multval(self.json_data['f'], '10')
            new_authors = []
            for author in authors:
                if author != None:
                    if not '1' in author:
                        author['1'] = id
                new_authors.append(author)
            if len(new_authors) > 1:
                self.json_data['f']['10'] = new_authors
            elif len(new_authors) > 0:
                self.json_data['f']['10'] = author
            
    def normalize_keywords(self):
        """
        Normalize the json structure for affiliations: 85
        """
        
        keyword_groups = return_multval(self.json_data['f'], '85')
        
        new = []
        for keyword_group in keyword_groups:
            lang = 'en'
            if type(keyword_group) == type({}):

                if 'l' in keyword_group.keys():
                    lang = keyword_group['l']

                for kw in keyword_group['k']:
                    new.append({'k': kw, 'l': lang})

            elif type(keyword_group) == type([]):
                for kw in keyword_group:
                    new.append({'k': kw, 'l': lang})

                
            elif type(keyword_group) == type(''):
                new.append({'k' : keyword_group, 'l': 'en'})
            
        if len(new) > 0:
            self.json_data['f']['85'] = new   

    def report_messages(self, errors, warnings, header_errors, header_warnings, fatal_errors, header_fatal_errors):
        
        if len(fatal_errors) > 0:
            #self.article_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' +  '\n' + '\n'.join(errors), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            self.article_report.write('\n'+ ' ! FATAL ERROR: ' + header_fatal_errors +  ':\n' + '\n'.join(fatal_errors), True, True, False)
        if len(errors) > 0:
            #self.article_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' +  '\n' + '\n'.join(errors), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            self.article_report.write('\n'+ ' ! ERROR: ' + header_errors +  ':\n' + '\n'.join(errors), True, True, False)
        if len(warnings) > 0:
            #self.article_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' +  '\n' + '\n'.join(warnings), False, True, False)
            #self.general_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' + ', '.join(warnings), False, True, False)
            self.article_report.write('\n'+ ' ! WARNING: ' + header_warnings +  ':\n' + '\n'.join(warnings), True, True, False)
    
    def validate_required(self):
        """
        Validate the required data of front
        """
        required = { 'doi': [237], 'publisher-name': [62], }
        errors = []
        for label, tags in required.items():
            value = ''
            values = [] 
            for t in tags:
                val = return_singleval(self.json_data['f'], str(t))
                values.append(val)
                if value == '':
                    value = val
            if len(values) == 2:
                if values[0] == values[1]:
                    errors.append('The value for ' + label + ' can not be the same: ' + ' x '.join(values))
            if value == '':
                errors.append( 'Missing ' + label)
        return errors

    def validate_pages(self):
        """
        Validate the pages of front
        """
        errors = []
        p = ''
        page = return_singleval(self.json_data['f'], '14')
        if type(page) == type({}):
            if 'f' in page.keys():
                p = page['f']
        else:
            errors.append('Missing pagination')
        num = return_singleval(self.json_data['f'], '32')
        num.replace('0', '')
        if p.replace('0', '') == '':
            if num != '' and num != 'ahead':
                errors.append('Missing pagination')
        return errors

    def validate_section(self):
        """
        Validate the pages of front
        """
        
        errors = []
        
        section_title = return_singleval(self.json_data['f'], '49')
        if 'INVALID' in section_title:
            errors.append( 'This section title is not registered: ' + section_title )
        
        return errors

    def validate_doctopic(self):
        """
        Validate the doctopic
        """
        errors = []
        doctopic = return_singleval(self.json_data['f'], '71')
        if not doctopic in self.json_normalizer.conversion_tables.table('doctopic').values():
            errors.append('Invalid value for doctopic: ' + doctopic)
        return errors

    def validate_ack_or_funding(self):
        """
        Validate the funding x ack
        """
        
        warnings = []
        project_number = return_multval(self.json_data['f'], '60')
        if len(project_number) == 0:
            ack = return_multval(self.json_data['f'], '102')
            if len(ack) > 0:
                warnings.append('WARNING: Check if there is funding data in ack \n ' + ack[0] + '\nIf yes, it must be in funding-group tag.')
        else:
            if self.json_data['f'].get('102', None):
                del self.json_data['f']['102']
        
        return warnings

    def validate(self, img_files):
        """
        Validate the data of front
        """

        count_errors = 0
        count_warnings = 0

        fatal_errors = []
        errors = [] 
        warnings = [] 
        
        # validate metadatas
        # aff, authors (prefix and suffix), pub-dates, funding (58,60) x ack
        #conditional = { 'page': (14, 32), }
        
        warnings += self.validate_issn()
        warnings += self.validate_required()
        fatal_errors += self.validate_section()
        warnings += self.validate_pages()
        errors += self.validate_dates()
        fatal_errors += self.validate_doctopic()
        e, w = self.validate_affiliations()
        errors += e 
        warnings += w
        warnings += self.validate_ack_or_funding()
        
        count_warnings += len(warnings)
        count_errors += len(errors)

        self.report_messages(errors, warnings, 'Required data in article front', 'Desirable data in article front', fatal_errors, '')

        e, w = self.validate_href(img_files)
        self.report_messages(e, w, 'Checking image files and their references inside of XML file', '', [], '')
        count_errors += len(e)
        count_warnings += len(w)

        e_count, w_count, refcount = self.normalize_and_validate_citations()
        count_warnings += w_count
        count_errors += e_count

        return (fatal_errors, count_errors, count_warnings, refcount)
        
    def normalize_and_validate_citations(self):
        k = 0
        refcount = 0
        errors = 0
        warnings = 0
        if 'c' in self.json_data.keys():
            if type(self.json_data['c']) == type({}):
                self.json_data['c'] = [self.json_data['c']]

            refcount = len(self.json_data['c'])
            for citation in self.json_data['c']:
                # normalize
                #citation = self.json_normalizer.format_for_indexing(citation)
                citation = self.json_citations.normalize_citation(citation, k, self.publication_dateiso)
                self.json_data['c'][k] = citation 

                # validate
                cittype, required_data, missing_data = self.json_citations.validate_citation_metadata(citation)
                if len(missing_data) + len(required_data) > 0:
                    self.article_report.write('\n'+ ' ! WARNING: citation ' + str(k + 1) + ' was identified as ' + cittype, True, True, False)
                    
                    if len(missing_data) > 0:
                        self.article_report.write('\n'+ ' ! WARNING: Missing data: ' + ', '.join(missing_data), True, True, False)
                        warnings += len(missing_data)
                    if len(required_data) > 0:
                        self.article_report.write('\n'+ ' ! ERROR: Required data: ' + ', '.join(required_data), True, True, False)
                        errors += len(required_data)

                    if '9704' in citation.keys():
                        self.article_report.write('\n'+citation['9704'], True, True, False)
                        

                if '9704' in citation.keys():
                    del citation['9704']
                k += 1
        else:
            self.article_report.write('\n'+ ' ! WARNING: No citation was found',  True, True, False)
            warnings += 1
        return (errors, warnings, refcount)

    def validate_href(self, img_files):

        missing_files = []
        missing_href = []
        href_list = []
        w = []
        e = []
        img_files = [ name[0:name.rfind('.')] for name in img_files ]

        if 'body' in self.json_data.keys():
            if type(self.json_data['body']) == type({}):
                href_list = list(set(return_multval(self.json_data['body'], 'file')))

            elif type(self.json_data['body']) == type([]):
                for occ in self.json_data['body']:
                    href_list += return_multval(occ, 'file')
                href_list = list(set(href_list))

        for href in href_list:
            if not href in img_files:
                missing_files.append(href)

            
        for file in img_files:
            if not file in href_list:
                missing_href.append(file)

        if len(missing_files) > 0:
            e.append('\nRequired image files: \n' + '\n'.join(missing_files))
        if len(missing_href) > 0:
            e.append( '\nRequired graphic/@xlink:href : \n' + '\n'.join(missing_href))

        return (e, w)
        




    def validate_affiliations(self):
        xml_affs    = return_multval(self.json_data['f'], '170')
        affiliations = return_multval(self.json_data['f'], '70')
        e, w = self.aff_handler.validate_affiliations(xml_affs, affiliations)

        return (e, w)

    def return_issue(self, journal):
        order = ''
        date = ''

        if 'f' in self.json_data.keys():
            data = self.json_data['f']
            
        else:
            data = self.json_data
           
        date = return_singleval(data, '65')
        order = return_singleval(data, '36')

        issue = JournalIssue(journal, data.get('31', ''), data.get('32', ''), date, data.get('132', data.get('131', '')), data.get('41', ''), order)

        issue.journal.publishers = ''
        publishers = return_multval(data, '62')
        if type(publishers) == type([]):
            issue.journal.publishers = ', '.join(publishers)
        elif type(publishers) == type(''):
            issue.journal.publishers = publishers

        i_record = {}
        keep_list = [30, 31, 32, 41, 131, 132, 35, 42, 65, 100, 480, ]
        for key, item in data.items():
            if key.isdigit():
                if int(key) in keep_list:
                    i_record[key] = item

        i_record['706'] = 'i'
        i_record['700'] = '0'
        i_record['701'] = '1'
        i_record['48'] = []
        i_record['48'].append({'l': 'en', 'h': 'Table of Contents'})
        i_record['48'].append({'l': 'pt', 'h': 'Sumário'})
        i_record['48'].append({'l': 'es', 'h': 'Sumario'})
        i_record['36'] = issue.order
        i_record['35'] = issue.journal.issn_id
        i_record['2'] = 'br1.1'        
        i_record['930'] = issue.journal.acron.upper()
        
        issue.json_data = i_record
        return  issue

    @property   
    def journal_title(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        r = return_singleval(json_data, '100')
        if r == '':
            r = return_singleval(json_data, '130')
        return r
   
    @property
    def journal_acron(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        return return_singleval(json_data, '68')
   
    @property 
    def journal_issn_id(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        return return_singleval(json_data, '400')        


class AffiliationsHandler:
    def __init__(self, normalized_affiliations):

        self.normalized_affiliations = normalized_affiliations

        self.aff_labels = {}
        self.aff_labels['p'] = 'country'
        self.aff_labels['c'] = 'city'
        self.aff_labels['s'] = 'state'
        self.aff_labels['_'] = 'organization name'
        self.aff_labels['e'] = 'e-mail'
        self.aff_labels['1'] = 'organization division'

        self._aff_required_parts = {}
        self._aff_required_parts['1'] = 'organization division'
        #self._aff_required_parts['9'] = 'full affiliation'
        self._aff_required_parts['p'] = 'country'
        #self._aff_required_parts['s'] = 'state'
        self._aff_required_parts['c'] = 'city'
        self._aff_required_parts['_'] = 'organization name'
        #self._aff_required_parts['e'] = 'e-mail'

    def validate_affiliations(self, xml_affs, affiliations):
        warnings = []
        errors = []
        fixed =''
        
        if len(affiliations) == 0:
            if len(xml_affs) > 0:
                warnings.append('No affiliation was found.\n' + '\n'.join(xml_affs))
        i = 0
        for aff in affiliations:
            identification = '\n'
            if 'i' in aff.keys():
                identification += 'affiliation: ' + aff['i']
            identification += '\n' + xml_affs[i] + '\n'
            if '8' in aff.keys():
                fixed = aff['8']

            
            missing_parts = []
            present = []
            for required_key, required_label in self._aff_required_parts.items():
                if required_key in aff.keys():
                    status = ''
                    if required_key in fixed:
                        status = '(automatically identified)'
                    if type(aff[required_key]) == type(''):
                        present.append(required_label +': ' + aff[required_key] + status)
                    else:
                        try:
                            present.append(required_label+': ' + str(aff[required_key]) + status)
                        except:
                            present.append(required_label+': ' + required_key + status)
                            print(aff[required_key])
                    
                else:
                    missing_parts.append(required_label)
            
            if len(missing_parts) > 0 or fixed != '':

                warnings.append(identification + '\n'.join(present))
                if len(missing_parts) > 0:
                    warnings.append('Missing required data in affiliation: ' + ', '.join(missing_parts))
            i += 1
        
        return (errors, warnings)

    
    
        
    def normalize_affiliations(self, affs):
        new = []
        for aff in affs:
            aff = self.normalized_affiliations.complete_affiliation(aff)
            new.append(aff)
    
        return new




   
        
class JSON_Issue:
    def __init__(self):
        pass 

    def load(self, json_data):
        self.json_data = json_data
        
    def return_issue(self, journal):
        suppl = ''
        order = ''
        vol = ''
        num = ''
        date = ''
        
        if 'f' in self.json_data.keys():
            data = self.json_data['f']
        else:
            data = self.json_data
        
        
        date = return_singleval(data, '65')
        order = return_singleval(data, '36')

        issue = JournalIssue(journal, data.get('31', ''), data.get('32', ''), date, data.get('132', data.get('131', '')), data.get('41', ''), order)

        i_record = {}
        keep_list = [30, 31, 32, 41, 131, 132, 35, 42, 65, 100, 480, ]
        for key, item in data.items():
            if int(key) in keep_list:
                i_record[key] = item

        i_record['706'] = 'i'
        i_record['700'] = '0'
        i_record['701'] = '1' 
        i_record['48'] = []
        i_record['48'].append({'l': 'en', 'h': 'Table of Contents'})
        i_record['48'].append({'l': 'pt', 'h': 'Sumário'})
        i_record['48'].append({'l': 'es', 'h': 'Sumario'})
        i_record['36'] = issue.order
        i_record['35'] = issue.journal.issn_id
        i_record['2'] = 'br1.1'        
        i_record['930'] = issue.journal.acron.upper()
        
        toc = return_multval(data, '49')
        for item in toc:
            lang = 'en'
            title = ''
            if 't' in item:
                title = item['t']
            if 'l' in item:
                lang = item['l']
            if 'c' in item:
                code = item['c']

            section = Section(title, code, lang)
            issue.toc.insert(section, True)

            #issue.toc.display()

        issue.json_data = i_record
        return issue

    @property   
    def journal_title(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        r = return_singleval(json_data, '100')
        if r == '':
            r = return_singleval(json_data, '130')
        return r

    @property   
    def journal_abbrev_title(self):
        return return_singleval(json_data.get('f', json_data), '421')

class JSON_Journal:
    def __init__(self):
        pass 

    def load(self, json_data):
        self.json_data = json_data
    @property   
    def publishers(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        r = return_singleval(json_data, '62')
        if type(r) == type([]):
            r = ', '.join(r)
        return r
    @property   
    def journal_title(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        r = return_singleval(json_data, '100')
        if r == '':
            r = return_singleval(json_data, '130')
        return r
   
    @property   
    def journal_abbrev_title(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        r = return_singleval(json_data, '421')
        return r

    @property
    def journal_acron(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        return return_singleval(json_data, '68')
   
    @property 
    def journal_issn_id(self):
        if 'f' in self.json_data.keys():
            json_data = self.json_data['f']
        else:
            json_data = self.json_data
        return return_singleval(json_data, '400')


class JSON2Article:
    def __init__(self, aff_handler, json_normalizer):
        self.json_data = {}
        self.json_article = JSON_Article(aff_handler, JSON_Citations(json_normalizer))

        

    def set_data(self, json_data, xml_filename, article_report):
        
        self.xml_filename = xml_filename
        self.article_report = article_report

        self.json_article.load(json_data['doc'], article_report)
        
    @property
    def publication_title(self):
        return self.json_article.journal_title
   
    def return_folder(self, journal):
        """
        Return an issue instance
        """
        
        # normalize
        self.json_article.normalize_issue_data(journal.issn_id)
        
        # issue
        return self.json_article.return_issue(journal)


    def evaluate_data(self, img_files):
        return self.json_article.validate(img_files)

        #self.article_report.write(' References found:' + str(refcount), True, False, False)
        #self.article_report.write(' Errors found: ' + str(count_errors), True, True, False)
        #self.article_report.write(' Warnings found: ' + str(count_warnings), True, True, False)

        #return (count_errors, count_warnings, refcount)

    def return_doc(self, issue):
        """
        Return an article instance
        """

        alternative_id = self.return_alternative_id()

        self.json_article.normalize_document_data(issue, alternative_id)
        
        article = self.json_article.return_article()
        article.issue = issue
        article.xml_filename = self.xml_filename
        

        return article
    
    def return_alternative_id(self):
        """
        Generate an alternative_id from filename 
        """

        alternative_id = os.path.basename(self.xml_filename)
        if '.' in alternative_id:
            alternative_id = alternative_id[0:alternative_id.rfind('.')]
            if '-' in alternative_id:
                alternative_id = alternative_id[alternative_id.rfind('-'):]

        new = ''
        for n in alternative_id:
            if n in '0123456789':
                new += n
        if new != alternative_id and new != '': 
            alternative_id = new
            alternative_id = alternative_id[-5:]
        return alternative_id


