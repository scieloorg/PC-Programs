# -*- coding: utf-8 -*-

import os

from journal_issue_article import Journal, JournalIssue, Article, Section, JournalList, JournalIssues
#from models.json_functions import JSON_Values, JSON_Dates


    

class JSON_Citations:
    def __init__(self, json_normalizer, json_dates):
        #self.publication_dateiso = publication_date
        self.json_normalizer = json_normalizer
        
        self.json_dates = json_dates
        # book, conf-proc, journal, patent, thesis, report, 
        # communication, letter, review, list, discussion, standard, and working-paper
        self._doctopics = {}
        self._doctopics['journal'] = ['65', '30', '12']
        self._doctopics['book'] = [ '65', '62', '18',  ]
        self._doctopics['book-part'] = [ '65', '62', '18',  '12',]
        self._doctopics['conf-proc'] = ['65', '53', ]
        self._doctopics['thesis'] = ['65',  '51' ]
        self._doctopics['patent'] = ['65', '150', ]
        self._doctopics['report'] = ['65', '58', '60', ]
        self._doctopics['software'] = ['65', '95', ]
        self._doctopics['web'] = ['65', '37', '109']
        self._doctopics['unidentified'] = ['65', ]

        self._evidences = {}
        self._evidences_order = [30, 18, 51, 53]
        self._evidences_order = [ str(i) for i in self._evidences_order ]
        self._evidences['30'] = 'journal'
        self._evidences['18'] = 'book'
        self._evidences['51'] = 'thesis'
        self._evidences['53'] = 'conf-proc'
        self._evidences['150'] = 'patent'
        self._evidences['58'] = 'report'
        self._evidences['95'] = 'software'
        self._evidences['37'] = 'web'
        
        self._labels = {}
        self._labels['10'] = 'analytic authors'
        self._labels['16'] = 'monographic authors'
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
            if not doctopic in self._doctopics.keys():
                doctopic = 'unidentified'    
        if doctopic == 'unidentified':
            for tag in self._evidences_order:
                if tag in citation.keys():
                    doctopic = self._evidences[tag]
                    if doctopic == 'book':
                        if '12' in citation.keys():
                            doctopic = 'book-part'
                        break
        
        return doctopic 

    

    def normalize_citation_title_language(self, citation):
        lang = self.json_normalizer.json_values.return_singleval(citation, '40')
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
    
    def normalize_citation_publication_data(self, citation):
        # if '30' then is a journal, delete 18
        if '30' in citation.keys():
            del citation['18']

        # roles
        roles = self.json_normalizer.json_values.return_value(citation, 'roles')
        roles = [ self.json_normalizer.normalize_role(r)  for r in roles ]
        #print(roles)
        if len(roles) > 0:
            del citation['roles']

        authors_monog = self.json_normalizer.json_values.return_value(citation, '16')
        #print(authors_monog)
        if len(roles) > 0:
            for a in authors_monog:
                a['r'] = roles[len(roles)-1]
                #print(a)
            if len(authors_monog) > 0:
                citation['16'] = authors_monog
        #print(authors_monog)
        

        authors_analyt = self.json_normalizer.json_values.return_value(citation, '10')
        #print(authors_analyt)
        if len(roles) > 0:
            for a in authors_analyt:
                a['r'] = roles[0]
                #print(a)
            if len(authors_analyt) > 0:
                citation['10'] = authors_analyt
        #print(authors_analyt)
        analytic_title = self.json_values.return_value(citation, '12')
        
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
        citation = self.normalize_citation_publication_data(citation)
        citation = self.normalize_citation_title_language(citation)
        citation = self.json_dates.normalize_citation_dates(citation, '964', '65', '64')
        citation = self.normalize_citation_issue_number(citation)
        #citation = self.normalize_citation_doctopic(citation)
        #citation = self.return_issn_and_norm_title(citation)
        citation['865'] = publication_dateiso
        citation = self.join_pages(citation, k)
        
        return citation
    
    def validate_citation_metadata(self, citation):
        missing = []
        doctopic = self.return_doctopic(citation)

        for tag in self._doctopics[doctopic]:
            if not tag in citation.keys():
                if tag in self._labels.keys():
                    missing.append(self._labels[tag])
                else:
                    missing.append(tag)

        valid_authors = False
        for tag in ['10', '11', '16', '17']:
            if tag in citation.keys():
                valid_authors = True
                break
        if not valid_authors:
            missing.append('authors')
        return missing

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




    

class JSON_Journal:
    def __init__(self, json_values):
        self.json_values = json_values
        self.json_data = {}

    def load(json_data):
        self.json_data = json_data

    @property 
    def title(self):
        r = self.json_values.return_singleval(self.json_data, '100')
        if r == '':
            r = self.json_values.return_singleval(self.json_data, '130')
        return r
   
    @property 
    def acron(self):
        return self.json_values.return_singleval(self.json_data, '68')
   
    @property 
    def issn_id(self):
        return self.json_values.return_singleval(self.json_data, '400')
   
        

class JSON_Issue:
    def __init__(self, json_values):
        self.json_values = json_values
        self.json_data = {}
    def load(json_data):
        self.json_data = json_data   

    def return_issue(self, journal):
        suppl = ''
        order = ''
        vol = ''
        num = ''
        date = ''

        data = self.json_data
        suppl = self.json_values.return_singleval(data, '131')
        suppl = self.json_values.return_singleval(data, '132')
        vol = self.json_values.return_singleval(data, '31')
        num = self.json_values.return_singleval(data, '32')
        date = self.json_values.return_singleval(data, '65')
        order = self.json_values.return_singleval(data, '36')

        
        if 'suppl' in num.lower():
            if ' ' in num:
                if '(' in num:
                    suppl = num[num.find('(')+1:]
                    suppl = suppl[0:suppl.find(')')]
                else:
                    suppl = num[num.rfind(' ')+1:]
                num = num[0:num.find(' ')]

        issue = JournalIssue(journal, vol, num, date, suppl, order) 


        i_record = {}
        keep_list = [30, 31, 32, 132, 35, 42, 65, 100, 480, ]
        for key, item in self.json_data.items():
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


class JSON_Article:
    def __init__(self, aff_handler, json_citations):
        self.json_normalizer = json_citations.json_normalizer
        self.json_values = self.json_normalizer.json_values
        
        self.aff_handler = aff_handler
        self.json_citations = json_citations

    def load(self, json_data):
        self.json_data = json_data

    def return_article(self):
        titles = self.json_values.return_value(self.json_data['f'], '12')
        authors = self.json_values.return_value(self.json_data['f'], '10')
        
        first_page = ''
        last_page = ''
        page = self.json_values.return_singleval(self.json_data['f'], '14')
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
        article.section = Section(self.json_values.return_singleval(self.json_data['f'], '49'))
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

    def normalize(self, issue):
        self.json_data['f']['35'] = issue.journal.issn_id
        
        self.json_data['f']['120'] = 'XML_' + self.json_values.return_singleval(self.json_data['f'], '120')
        self.json_data['f']['42'] = '1'
        
        section = Section(self.json_values.return_singleval(self.json_data['f'], '49'))
        self.json_data['f']['49'] = section.code
        
        self.normalize_metadata_authors()
        self.normalize_illustrative_materials()
        self.normalize_affiliations()
        self.normalize_keywords()
        
        self.json_data['f'] = self.json_normalizer.convert_value(self.json_data['f'], '71', 'doctopic')
        
        

        self.json_data['f'] = self.json_dates.normalize_dates(self.json_data['f'], '64', '65', '64')
        self.json_data['f'] = self.json_dates.normalize_dates(self.json_data['f'], '112', '111', '112')
        self.json_data['f'] = self.json_dates.normalize_dates(self.json_data['f'], '114', '113', '114')

        self.publication_dateiso = self.json_values.return_singleval(self.json_data['f'], '65')

        
        self.json_data['h'] = self.json_normalizer.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.json_normalizer.format_for_indexing(self.json_data['h'])
        

    def normalize_metadata_authors(self):
        authors = self.json_values.return_value(self.json_data['f'], '10')
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
            count = self.generic.return_singleval(self.json_data['f'], tag)
            if len(count)>0:
                if int(count)>0:
                    illustrative_materials.append(type)
                del self.json_data['f'][tag]
        
        if len(illustrative_materials) > 0:
            self.json_data['f']['38'] = illustrative_materials
        else:
            self.json_data['f']['38'] = 'ND'
        
    def normalize_affiliations(self):
        affiliations = self.json_values.return_value(self.json_data['f'], '70')

        new_affiliations = [ self.aff_handler.complete_affiliation(aff)  for aff in affiliations ]
        new_affiliations = self.aff_handler.complete_affiliations(new_affiliations)
        
        id = ''
        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
            if 'i' in new_affiliations[0].keys():
                id = new_affiliations[0]['i']
    
        if id != '':
            authors = self.json_values.return_value(self.json_data['f'], '10')
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
        keyword_groups = self.json_values.return_value(self.json_data['f'], '85')
        
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

    def report_messsages(self, errors, warnings, header_errors, header_warnings):
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

        count_errors += self.validate_href()
        errors, warnings = self.normalize_and_validate_citations()
        count_warnings += len(warnings)
        count_errors += len(errors)

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

    def validate_href(self):

        missing_files = []
        missing_href = []
        href_list = []

        if 'body' in self.json_data:
            href_list = list(set(self.json_values.return_value(self.json_data['body'], 'file')))

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
        pages = self.generic.return_singleval(self.json_data['f'], '14')
        if not 'f' in pages:
            errors.append('Missing pages')
        
        return (errors, warnings)
     
    def validate_affiliations(self, errors, warnings):
        xml_affs    = self.json_values.return_value(self.json_data['f'], '170')
        affiliations = self.json_values.return_value(self.json_data['f'], '70')
        
        e, w = self.aff_handler.validate_affiliations(xml_affs, affiliations)

        return (errors + e, warnings + w)

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

    def complete_affiliations(self, aff):
        return self.normalized_affiliations.complete_affiliation(affs)


class JSON_Articles_Models:
    def __init__(self, aff_handler, json_normalizer, json_dates):
        self.json_data = {}
        self.json_article = JSON_Article(aff_handler, JSON_Citations(json_normalizer, json_dates))
        self.json_journal = JSON_Journal(json_normalizer.json_values)
        self.json_issue = JSON_Issue(json_normalizer.json_values)
        

    def set_data(json_data, xml_filename, article_report):
        
        self.xml_filename = xml_filename
        self.article_report = article_report

        self.json_article.load(json_data['doc'])
        self.json_issue.load(json_data['doc']['f'])
        self.json_journal.load(json_data['doc']['f'])

    @property
    def publication_title(self):
        return self.json_journal.title
   
    def normalize_document(self, issue):
        self.json_article.normalize(issue)

    def validate_document(self, img_files):
        return self.json_article.validate(img_files)

    def return_document(self, journal, img_files):
        # issue
        issue = self.json_issue.return_issue(journal)
        
        # normalize
        self.json_article.normalize(issue)
        count_errors, count_warnings, refcount = self.json_article.validate(img_files)

        self.article_report.write(' References found:' + str(refcount), True, False, False)
        self.article_report.write(' Errors found: ' + str(count_errors), True, True, False)
        self.article_report.write(' Warnings found: ' + str(count_warnings), True, True, False)


        article = self.json_article.return_article()
        article.issue = issue
        article.xml_filename = self.xml_filename


        return (article, errors, warnings, refcount)

    def return_publication_item(self, json_data, journal):
        self.json_issue.load(json_data)
        return self.json_issue.return_issue(journal)

    def return_publications_list(self, json):
        #json = self.db2json(title_db_filename)
        journal_list = JournalList()
        for json_item in json:
            
            self.json_journal.load(json_item)
            j = Journal(self.json_journal.title, self.json_journal.issn_id, self.json_journal.acron)
            
            journal_list.insert(j, False)
        return journal_list

    def return_publication_items(self, json_issues, journals):
        issues_list = JournalIssues()
        for json_issue in json_issues:
            self.json_journal.load(json_issue)
            j = journals.find_journal(self.json_journal.title)
            if j != None:
                issue = self.return_issue(json_issue, j)
                issues_list.insert(issue, False)
        return issues_list
    
    