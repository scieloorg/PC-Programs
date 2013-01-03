# -*- coding: utf-8 -*-

import os
from xml2db.json_functions import return_multval, return_singleval

from reuse.items_and_id import id_generate, Items
from xml2db.box_folder_document import Section, TOC

from xml2db.custom.articles.models.journal_issue_article import Journal, JournalIssue, Article, JournalsList, JournalIssuesList 
#from models.json_functions import JSON_Values, JSON_Dates


def return_journals_list(json):
    #json = self.db2json(title_db_filename)
    journal_list = JournalsList()
    json_title = JSON_Journal()
    for json_item in json:
        
        json_title.load(json_item)

        
        j = Journal(json_title.journal_title, json_title.journal_issn_id, json_title.journal_acron)
        
        journal_list.insert(j, False)
    return journal_list

def return_issues_list(json_issues, journals):
    issues_list = JournalIssuesList()

    json_issue = JSON_Issue()
    for json in json_issues:
        json_issue.load(json)
        j = journals.find_journal(json_issue.journal_title)
        if j != None:
            json_issue.load(json)
            issue = json_issue.return_issue(j)
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
        return required, desirable

    def join_pages(self, citation, k):
        if '514' in citation.keys():
            citation['14'] = ''
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
        return citation

class JSON_Article:
    def __init__(self, aff_handler, json_citations):
        self.json_normalizer = json_citations.json_normalizer
        
        self.aff_handler = aff_handler
        self.json_citations = json_citations
        


    def load(self, json_data, article_report):
        self.json_data = json_data
        self.article_report = article_report

    def return_article(self):
        titles = return_multval(self.json_data['f'], '12')
        authors = return_multval(self.json_data['f'], '10')
        
        first_page = ''
        last_page = ''
        page = return_singleval(self.json_data['f'], '14')
        if type(page) == type({}):
            if 'f' in page:
                first_page =  page['f']
            if 'l' in page:
                last_page =  page['l']
        if first_page == '' or last_page == '':
            self.article_report.write('\n'+ ' ! ERROR: Missing first and last pages', True, True, False)
            
        
            
        article = Article(first_page, last_page)
        article.titles = self.format_titles(titles)
        article.authors = self.format_author_names(authors)
        article.section = self.section
        article.json_data = self.json_data


        return article

    


    def format_author_names(self, authors):
        new = []
        for a in authors:
            author = ''

            if 's' in a:
                author += a['s'] + ', '
            if 'n' in a:
                author += a['n']
            
            
            new.append(author)
        return new
    
    def format_titles(self, titles):
        new = []
        for a in titles:
            title = ''
            if 'l' in a:
                title += '[' + a['l'] + '] '
            if 't' in a:
                title += a['t'] 
            if '_' in a:
                title += a['_'] 
            
            if 's' in a:
                title += ': ' + a['s']


            new.append(title)
        return new

    def normalize(self, issn_id):
        self.json_data['f']['35'] = issn_id
        
        self.json_data['f']['120'] = 'XML_' + return_singleval(self.json_data['f'], '120')
        self.json_data['f']['42'] = '1'
        
        self.section = Section(return_singleval(self.json_data['f'], '49'))
        #self.json_data['f']['49'] = self.section.code
        
        self.normalize_metadata_authors()
        self.normalize_illustrative_materials()
        self.normalize_affiliations()
        self.normalize_keywords()
        
        self.json_data['f'] = self.json_normalizer.convert_value(self.json_data['f'], '71', 'doctopic')
        
        

        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '64', '65', '64')
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '112', '111', '112')
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '114', '113', '114')

        self.publication_dateiso = return_singleval(self.json_data['f'], '65')

        
        self.json_data['h'] = self.json_normalizer.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.json_normalizer.format_for_indexing(self.json_data['h'])

    def normalize_issue_data(self, issn_id):
        self.json_data['f']['35'] = issn_id
        
        #self.section = Section(return_singleval(self.json_data['f'], '49'))
        #self.json_data['f']['49'] = self.section.code
        
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '64', '65', '64')
        self.publication_dateiso = return_singleval(self.json_data['f'], '65')

        
    def normalize_document_data(self, issue):
        
        self.json_data['f']['120'] = 'XML_' + return_singleval(self.json_data['f'], '120')
        self.json_data['f']['42'] = '1'
        
        section = Section(return_singleval(self.json_data['f'], '49'))
        self.section = issue.toc.return_section(section)
        if self.section == None:
            self.section = section
        self.json_data['f']['49'] = self.section.code

        self.normalize_metadata_authors()
        self.normalize_illustrative_materials()
        self.normalize_affiliations()
        self.normalize_keywords()
        
        self.json_data['f'] = self.json_normalizer.convert_value(self.json_data['f'], '71', 'doctopic')
        
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '112', '111', '112')
        self.json_data['f'] = self.json_normalizer.normalize_dates(self.json_data['f'], '114', '113', '114')

        self.json_data['h'] = self.json_normalizer.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.json_normalizer.format_for_indexing(self.json_data['h'])                

    def normalize_metadata_authors(self):
        authors = return_multval(self.json_data['f'], '10')
        changed = False
        new_authors = []
        for author in authors:
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
        
    def normalize_illustrative_materials(self):
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
        affiliations = return_multval(self.json_data['f'], '70')

        new_affiliations = [ self.aff_handler.complete_affiliation(aff)  for aff in affiliations ]
        new_affiliations = self.aff_handler.complete_affiliations(new_affiliations)
        
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

    def report_messages(self, errors, warnings, header_errors, header_warnings):
        if len(warnings) > 0:
            #self.article_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' +  '\n' + '\n'.join(warnings), False, True, False)
            #self.general_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' + ', '.join(warnings), False, True, False)
            self.article_report.write('\n'+ ' ! WARNING: ' + header_warnings +  ':\n' + '\n'.join(warnings), False, True, False)
        
        if len(errors) > 0:
            #self.article_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' +  '\n' + '\n'.join(errors), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            self.article_report.write('\n'+ ' ! ERROR: ' + header_errors +  ':\n' + '\n'.join(errors), False, True, False)
    

    def validate(self, img_files):
        count_errors = 0
        count_warnings = 0
        errors = [] 
        warnings = [] 
        
        # validate metadatas
        errors, warnings = self.validate_pubdate(errors, warnings)
        errors, warnings = self.validate_pages(errors, warnings)
        errors, warnings = self.validate_affiliations(errors, warnings)
        count_warnings += len(warnings)
        count_errors += len(errors)
        
        self.report_messages(errors, warnings, 'Expected data in article front', 'Missing desirable data in article front')

        count_errors += self.validate_href(img_files)
        errors, warnings, refcount = self.normalize_and_validate_citations()
        count_warnings += warnings
        count_errors += errors

        return (count_errors, count_warnings, refcount)
        
    def normalize_and_validate_citations(self):
        k = 0
        refcount = 0
        errors = 0
        warnings = 0
        if 'c' in self.json_data.keys():
            refcount = len(self.json_data['c'])
            for citation in self.json_data['c']:
                # normalize
                citation = self.json_normalizer.format_for_indexing(citation)
                citation = self.json_citations.normalize_citation(citation, k, self.publication_dateiso)
                self.json_data['c'][k] = citation 

                # validate
                required_data, missing_data = self.json_citations.validate_citation_metadata(citation)
                if len(missing_data) > 0:
                    self.article_report.write('\n'+ ' ! WARNING: Missing data in citation ' + str(k + 1) +': ' + ', '.join(missing_data), False, True, False)
                    warnings += len(missing_data)
                if len(required_data) > 0:
                    self.article_report.write('\n'+ ' ! ERROR: Required data in citation ' + str(k + 1) +': ' + ', '.join(required_data), False, True, False)
                    errors += len(required_data)

                if len(missing_data) + len(required_data) > 0:
                    if '9704' in citation.keys():
                        self.article_report.write('\n'+citation['9704'], False, True, False)
                        del citation['9704']
                k += 1
        return (errors, warnings, refcount)

    def validate_href(self, img_files):

        missing_files = []
        missing_href = []
        href_list = []

        img_files = [ name[0:name.rfind('.')] for name in img_files ]

        if 'body' in self.json_data:
            href_list = list(set(return_multval(self.json_data['body'], 'file')))

        for href in href_list:
            if not href in img_files:
                missing_files.append(href)

        if len(missing_files) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Expected image files: '  +  '\n'+ '\n'.join(missing_files), False, True, False)
            
        for file in img_files:
            if not file in href_list:
                missing_href.append(file)

        if len(missing_href) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Expected graphic/@xlink:href: '  +  '\n' + '\n'.join(missing_href), False, True, False)
            
        return len(missing_files) + len(missing_href)
        


    def validate_pubdate(self, errors, warnings):
        if self.publication_dateiso == '':
            errors.append('Missing publication date')
        return (errors, warnings)

    def validate_pages(self, errors, warnings):
        pages = return_singleval(self.json_data['f'], '14')
        if not 'f' in pages:
            errors.append('Missing pages')
        
        return (errors, warnings)
     
    def validate_affiliations(self, errors, warnings):
        xml_affs    = return_multval(self.json_data['f'], '170')
        affiliations = return_multval(self.json_data['f'], '70')
        
        e, w = self.aff_handler.validate_affiliations(xml_affs, affiliations)

        return (errors + e, warnings + w)

    
   
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

        suppl = return_singleval(data, '131')
        suppl = return_singleval(data, '132')
        vol = return_singleval(data, '31')
        num = return_singleval(data, '32')
        date = return_singleval(data, '65')
        order = return_singleval(data, '36')
        compl = return_singleval(data, '41')
        
        if 'suppl' in num.lower():
            if ' ' in num:
                if '(' in num:
                    suppl = num[num.find('(')+1:]
                    suppl = suppl[0:suppl.find(')')]
                else:
                    suppl = num[num.rfind(' ')+1:]
                num = num[0:num.find(' ')]

        issue = JournalIssue(journal, vol, num, date, suppl, compl, order) 


        i_record = {}
        keep_list = [30, 31, 32, 132, 35, 42, 65, 100, 480, ]
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
        if issue.number != num:
            if '31' in i_record.keys():
                del i_record['31'] 
            i_record['32'] = issue.number

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
        self._aff_required_parts['9'] = 'full affiliation'
        self._aff_required_parts['p'] = 'country'
        self._aff_required_parts['c'] = 'city'
        self._aff_required_parts['_'] = 'organization name'
        #self._aff_required_parts['e'] = 'e-mail'

    def validate_affiliations(self, xml_affs, affiliations):
        warnings = []
        errors = []


        if len(affiliations) == 0:
            warnings.append('Missing affiliations')

        i = 0
        for aff in affiliations:
            missing_parts = []
            for required_key, required_label in self._aff_required_parts.items():
                if not required_key in aff:
                    missing_parts.append(required_label)
            if len(missing_parts) > 0:
                if 'i' in aff.keys():
                    warnings.append('Missing required data in affiliation ' +  aff['i'] +  ': ' + ', '.join(missing_parts) +  '\n' + xml_affs[i])
                else:
                    warnings.append('Missing required data in affiliation: ' + ', '.join(missing_parts) + '\n' + xml_affs[i])
            else:
                if '9' in aff:
                    parts = ''
                    for key, value in aff.items():
                        if key in self.aff_labels.keys():
                            parts += self.aff_labels[key] + ': ' + value +'\n'
                        
                    warnings.append('\nAffiliation: ' + aff['9'] + '\n Its parts were automatically identified: ' + '\n' + parts + '\nPlease, check if they were correctly identified.\n' )
            i += 1

        return (errors, warnings)

    def complete_affiliation(self, aff):
        return self.normalized_affiliations.complete_affiliation(aff)

    def complete_affiliations(self, affs):
        return self.normalized_affiliations.complete_affiliations(affs)



   
        
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
        suppl = return_singleval(data, '131')
        suppl = return_singleval(data, '132')
        vol = return_singleval(data, '31')
        num = return_singleval(data, '32')
        date = return_singleval(data, '65')
        order = return_singleval(data, '36')
        compl = return_singleval(data, '41')
        
        if 'suppl' in num.lower():
            if ' ' in num:
                if '(' in num:
                    suppl = num[num.find('(')+1:]
                    suppl = suppl[0:suppl.find(')')]
                else:
                    suppl = num[num.rfind(' ')+1:]
                num = num[0:num.find(' ')]

        issue = JournalIssue(journal, vol, num, date, suppl, compl, order) 


        i_record = {}
        keep_list = [30, 31, 32, 132, 35, 42, 65, 100, 480, ]
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
        if issue.number != num:
            if '31' in i_record.keys():
                del i_record['31'] 
            i_record['32'] = issue.number

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
            issue.toc.insert(section, False)

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
class JSON_Journal:
    def __init__(self):
        pass 

    def load(self, json_data):
        self.json_data = json_data

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
        
        # normalize
        self.json_article.normalize_issue_data(journal.issn_id)
        
        # issue
        return self.json_article.return_issue(journal)
    
    def return_doc(self, issue, img_files):
        # normalize
        self.json_article.normalize_document_data(issue)
        
        
        count_errors, count_warnings, refcount = self.json_article.validate(img_files)

        self.article_report.write(' References found:' + str(refcount), True, False, False)
        self.article_report.write(' Errors found: ' + str(count_errors), True, True, False)
        self.article_report.write(' Warnings found: ' + str(count_warnings), True, True, False)


        article = self.json_article.return_article()
        article.issue = issue
        article.issue.toc.insert(self.json_article.section, True)
        article.xml_filename = self.xml_filename


        return (article, count_errors, count_warnings, refcount)

    # sera eliminado
    def return_document(self, journal, img_files):
        
        # normalize
        self.json_article.normalize(journal.issn_id)
        
        # issue
        issue = self.json_article.return_issue(journal)
        

        count_errors, count_warnings, refcount = self.json_article.validate(img_files)

        self.article_report.write(' References found:' + str(refcount), True, False, False)
        self.article_report.write(' Errors found: ' + str(count_errors), True, True, False)
        self.article_report.write(' Warnings found: ' + str(count_warnings), True, True, False)


        article = self.json_article.return_article()
        article.issue = issue
        article.xml_filename = self.xml_filename


        return (article, count_errors, count_warnings, refcount)


