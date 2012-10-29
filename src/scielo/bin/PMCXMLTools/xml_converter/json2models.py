# -*- coding: utf-8 -*-

import os

from journal_issue_article import Journal, JournalIssue, Article, Section, JournalList, JournalIssues

from table_ent_and_char import TableEntAndChar
from table_conversion import ConversionTables
from utils.aff_table import AffiliationTable
from utils.table_issn import ISSN_Table

class Generic:
    def __init__(self, conversion_tables = ConversionTables(), table_entity_and_char= TableEntAndChar()):
        #self.general_report = general_report
        self.conversion_tables = conversion_tables
        self.table_entity_and_char = table_entity_and_char

    def format_for_indexing(self, json_record):
        # FIXME
        if type(json_record) == type({}):
            json_record_dest = {}
            for key, json_data in json_record.items():
                json_record_dest[key] = self.format_for_indexing(json_data)
        else:
            if type(json_record) == type(''):
                json_record_dest = self.table_entity_and_char.remove_accent(self.conversion_tables.remove_formatting(json_record))
            else:
                if type(json_record) == type([]):
                    a = []
                    for json_data in json_record:
                        r = self.format_for_indexing(json_data)
                        a.append(r)
                    json_record_dest = a
        
        return json_record_dest

    def return_value(self, json_data, tag):
        r = []
        
        if tag in json_data.keys():
            r = json_data[tag]

        if type(r) != type([]):
            r = [r]
        return r 

    def return_singleval(self, json_data, tag = ''):
        r = ''
        if tag != '':
            if tag in json_data.keys():
                r = json_data[tag]
        else:
            r = json_data
        if type(r) == type([]):
            r = r[0]
        return r 
    
    def fill_number_with_zeros(self, number, quantity):
        if not number.isdigit():
            number = ''
        number = '0' * quantity + number
        number = number[-quantity:]

        return number

    def convert_value(self, json_data, tag, table_name):
        a = self.return_singleval(json_data, tag)
        if len(a)>0:
            json_data[tag] = self.conversion_tables.return_fixed_value(table_name, a)
    
        return json_data

    def fix_dates(self, json_data, tag, tag_iso, tag_not_iso):
        #print(json_data)
        

        publication_dates = self.return_value(json_data, tag)
        #print(publication_dates)

        r = ''
        s = ''
        display = ''
        
        for d in publication_dates:
            pdate = ''

            if 'y' in d.keys():
                s = d['y']
                pdate = self.fill_number_with_zeros(d['y'], 4)
            else:
                pdate = '0000'
            if 'm' in d.keys():
                s = d['m'] + ' ' + s
                pdate += self.return_month_number(d['m'])
            elif 's' in d.keys():
                s = d['s'] + ' ' + s
                pdate += self.return_month_number(d['s'])
            else:
                pdate += '00'
            if 'd' in d.keys():
                s = d['d'] + ' ' + s
                pdate = self.fill_number_with_zeros(d['d'], 2)
            else:
                pdate += '00'
            
            if r == '':
                r = pdate
                display = s
            else:
                if pdate > r:
                    r = pdate
                    display = s
        if len(r)>0:
            json_data[tag_iso] = r
            json_data[tag_not_iso] = display

        return json_data     

    def fix_citation_dates(self, json_data, tag, tag_iso, tag_not_iso):
        #print(json_data)
        day = self.return_singleval(json_data, tag + 'd')
        month = self.return_singleval(json_data, tag + 'm')
        season = self.return_singleval(json_data, tag + 's')
        year = self.return_singleval(json_data, tag )
        
        if len(year)>0:
            isodate = year
            if len(month)>0:
                isodate += self.return_month_number(month)
            elif len(season) >0:
                isodate += self.return_month_number(season)
            else:
                isodate += '00'
            if len(day)>0:
                isodate += self.fill_number_with_zeros(day, 2)
            else:
                isodate += '00'
            del json_data[tag]
            json_data[tag_iso] = isodate
        
        if len(month)>0:
            del json_data[tag + 'm']
        if len(season)>0:
            del json_data[tag + 's']
        if len(day)>0:
            del json_data[tag + 'd']

        return json_data     

    def return_month_number(self, number_or_text_month):
        r = '00'
        if number_or_text_month.isdigit():
            m = '00' + number_or_text_month
            m = m[-2:]
            if 0 <= m <=12:
                r = m
        else:
            r = self.conversion_tables.return_month_number(number_or_text_month)
        return r

    
    

class JSONArticle:
    def __init__(self, generic, table_aff = AffiliationTable()):
        #self.issn_table = ISSN_Table()
        self.table_aff = table_aff
        self.generic = generic 
        self.json_data = {}
        self.publication_dateiso = ''
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
        self._doctopics['web'] = ['65','37', '109']
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
        

        self._aff_required_parts = {}
        self._aff_required_parts['1'] = 'organization division'
        self._aff_required_parts['9'] = 'full affiliation'
        self._aff_required_parts['p'] = 'country'
        self._aff_required_parts['c'] = 'city'
        self._aff_required_parts['_'] = 'organization name'
        #self._aff_required_parts['e'] = 'e-mail'
        self.aff_labels = {}
        self.aff_labels['p'] = 'country'
        self.aff_labels['c'] = 'city'
        self.aff_labels['s'] = 'state'
        self.aff_labels['_'] = 'organization name'
        self.aff_labels['e'] = 'e-mail'
        self.aff_labels['1'] = 'organization division'


    def load_json(self, json_data, filename, report):
        self.json_data = json_data
        self.article_report = report
        self.filename = filename
        
    def format_author_names(self, authors):
        new = []
        for a in authors:
            author = ''

            if 'n' in a:
                author += a['n'] + ' '
            
            if 's' in a:
                author += a['s']

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

    def return_article(self, issue, xml_filename):   
        doc_f = self.json_data['f']
        titles = self.generic.return_value(doc_f, '12')

        authors = self.generic.return_value(doc_f, '10')
        
        first_page = ''
        last_page = ''
        page = self.generic.return_singleval(doc_f, '14')
        if type(page) == type({}):

            if 'f' in page:
                first_page =  page['f']
            if 'l' in page:
                last_page =  page['l']
            
        
        self.json_data['35'] = issue.journal.issn_id
        if first_page == '' or last_page == '':
            self.article_report.write('\n'+ ' ! ERROR: Missing first and last pages', True, True, False)
            
        article = Article(issue, first_page, last_page, xml_filename)
        article.titles = self.format_titles(titles)
        article.authors = self.format_author_names(authors)

        return article

    def return_section_title(self):
        return self.generic.return_singleval(self.json_data['f'], '49')


    def fix_and_validate(self, img_files):
        count_errors = 0
        
        self.fix_metadata()


        self.json_data['h'] = self.generic.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.generic.format_for_indexing(self.json_data['h'])
        
        #self.article_report.write(self.filename, True, False, False)
        ##self.general_report.write(self.filename, True, False, False)


        errors, warnings = self.validate_article_metadata()
        if len(warnings) > 0:
            self.article_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' +  '\n' + '\n'.join(warnings), False, True, False)
            #self.general_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' + ', '.join(warnings), False, True, False)
            count_errors += len(warnings)
        if len(errors) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' +  '\n' + '\n'.join(errors), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            count_errors += len(errors)

        #####
        missing_files = []
        missing_href = []
        href_list = []
        if 'body' in self.json_data:
            href_list = list(set(self.generic.return_value(self.json_data['body'], 'file')))
        for href in href_list:
            if not href in img_files:
                missing_files.append(href)
        if len(missing_files) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing image files: '  +  '\n'+ '\n'.join(missing_files), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing image files: ' + ', '.join(missing_files), False, True, False)
            count_errors += len(missing_files)
        for file in img_files:
            if not file in href_list:
                missing_href.append(file)

        if len(missing_href) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing graphic/@xlink:href: '  +  '\n' + '\n'.join(missing_href), False, True, False)
            #self.general_report.write('\n'+ ' ! ERROR: Missing graphic/@xlink:href: ' + ', '.join(missing_href), False, True, False)
            count_errors += len(missing_href)

        if len(missing_href) + len(missing_files)  > 0:
            print('VERIFICAR')
            print(href_list)
            print(img_files)
        ###     

        k = 0
        refcount = 0
        if 'c' in self.json_data.keys():
            refcount = len(self.json_data['c'])
            for citation in self.json_data['c']:
                citation = self.generic.format_for_indexing(citation)
                citation = self.fix_citation(citation, k)
                missing_data = self.validate_citation_metadata(citation)
                if len(missing_data) > 0:
                    self.article_report.write('\n'+ ' ! WARNING: Missing data in citation ' + str(k + 1) +': ' + ', '.join(missing_data), False, True, False)
                    #self.general_report.write('\n'+ ' ! WARNING: Missing data in citation ' + str(k + 1) +': ' + ', '.join(missing_data), False, True, False)
                    if '9704' in citation.keys():
                        self.article_report.write('\n'+citation['9704'], False, True, False)
                        del citation['9704']

                    count_errors += len(missing_data)
            
                self.json_data['c'][k] = citation 
                k += 1
        self.article_report.write(' References found:' + str(refcount), True, False, False)
        #self.general_report.write('  References:' + str(k), True, False, False)
        

        self.article_report.write(' Errors found: ' + str(count_errors), True, True, False)
        #self.general_report.write('Errors found: ' + str(count_errors), True, True, False)
    
    def fix_keywords(self):
        keyword_groups = self.generic.return_value(self.json_data['f'], '85')
        
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

    
    def return_journal_title(self):
        return self.json_data['f']['100']

    def return_issn_id(self):
        return self.json_data['f']['35']
     
    
    
    def set_section_code(self, section_code):
        self.json_data['f']['49'] = section_code
        self.json_data['h']['49'] = section_code
        self.json_data['l']['49'] = section_code

    

    #def return_issn_and_norm_title(self, citation):
    #    if '30' in citation.keys() and not '35' in citation.keys():
    #        issn, journal_title = self.issn_table.return_issn_and_normalized_title(citation['30'])
    
    #        if len(issn) > 0:
    #            citation['35'] = issn
    #            if len(journal_title) > 0:
    #                citation['801'] = journal_title
    #    return citation

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

    

    def fix_citation_title_language(self, citation):
        if '40' in citation.keys() and '18' in citation.keys():
            monog_title = citation['18']
            citation['18'] = { 'l': citation['40'], '_': monog_title}
            if '12' in citation.keys():
                if type(citation['12']) == type([]):
                    for title in citation['12']:
                        if not 'l' in title.keys():
                            title['l'] = citation['40']

                elif type(citation['12']) == type({}):
                    if not 'l' in citation['12']:
                        citation['12']['l'] = citation['40']
                else:
                    citation['12'] = { 'l': citation['40'], '_':citation['12']}

        return citation 

    def fix_citation_issue_number(self, citation):
        if '132' in citation:
            if '32' in citation:
                citation['132'].update({'_':citation['32']})
                citation['32'] = citation['132']

            else:
                citation['32'] = citation['132']
            del citation['132']
            
        return citation
    
    def fix_citation_monographic_or_analytic_data(self, citation):
        # if '30' then is a journal, delete 18
        if '30' in citation.keys():
            del citation['18']

        # roles
        roles = self.generic.return_value(citation, 'roles')
        roles = [ self.generic.conversion_tables.return_fixed_value('role', r)  for r in roles ]
        #print(roles)
        if len(roles) > 0:
            del citation['roles']

        authors_monog = self.generic.return_value(citation, '16')
        #print(authors_monog)
        if len(roles) > 0:
            for a in authors_monog:
                a['r'] = roles[len(roles)-1]
                #print(a)
            if len(authors_monog) > 0:
                citation['16'] = authors_monog
        #print(authors_monog)
        

        authors_analyt = self.generic.return_value(citation, '10')
        #print(authors_analyt)
        if len(roles) > 0:
            for a in authors_analyt:
                a['r'] = roles[0]
                #print(a)
            if len(authors_analyt) > 0:
                citation['10'] = authors_analyt
        #print(authors_analyt)
        analytic_title = self.generic.return_value(citation, '12')
        
        if len(analytic_title) == 0:
            # monographic
            if len(authors_analyt) > 0:
                citation['16'] = citation['10']
                del citation['10']
            if '11' in citation.keys():
                citation['17'] = citation['11']
                del citation['11']
        

        return citation


    def fix_citation(self, citation, k):
        citation = self.fix_citation_monographic_or_analytic_data(citation)
        citation = self.fix_citation_title_language(citation)
        citation = self.generic.fix_citation_dates(citation, '964', '65', '64')
        citation = self.fix_citation_issue_number(citation)
        #citation = self.fix_citation_doctopic(citation)
        #citation = self.return_issn_and_norm_title(citation)
        citation['865'] = self.publication_dateiso
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



    
    def fix_metadata_authors(self):
        authors = self.generic.return_value(self.json_data['f'], '10')
        changed = False
        new_authors = []
        for author in  authors:
            if '1' in author.keys():
                if type(author['1']) == type([]):
                    #print(self.json_json_data['f']['10'])
                    author['1'] = ' '.join(author['1'])
                    #print(self.json_json_data['f']['10'])
                    changed = True
            if 'r' in author.keys():
                author['r'] = self.generic.conversion_tables.return_fixed_value('role', author['r'])
            new_authors.append(author)
        if changed:
            if len(new_authors) == 1:
                self.json_data['f']['10'] = new_authors[0]
            else:
                self.json_data['f']['10'] = new_authors
        

    def fix_metadata(self):
        self.fix_keywords()
        self.json_data['f'] = self.generic.convert_value(self.json_data['f'], '71', 'doctopic')
        self.fix_metadata_authors()
        self.json_data['f'] = self.generic.fix_dates(self.json_data['f'], '112', '111', '112')
        self.json_data['f'] = self.generic.fix_dates(self.json_data['f'], '114', '113', '114')

        if '120' in self.json_data['f'].keys():
            self.json_data['f']['120'] = 'XML_' + self.json_data['f']['120']
        self.json_data['f']['42'] = '1'
        
        self.json_data['f'] = self.generic.fix_dates(self.json_data['f'], '64', '65', '64')
        
        if '65' in self.json_data['f']:
            self.publication_dateiso = self.json_data['f']['65']

        self.fix_illustrative_materials()
        self.fix_affiliations()
        

    def fix_affiliations(self):
        affiliations = self.generic.return_value(self.json_data['f'], '70')

        new_affiliations = [ self.table_aff.complete_affiliation(aff)  for aff in affiliations ]
        new_affiliations = self.table_aff.complete_affiliations(new_affiliations)
        
        id = ''
        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
            if 'i' in new_affiliations[0].keys():
                id = new_affiliations[0]['i']
    
        if id != '':
            authors = self.generic.return_value(self.json_data['f'], '10')
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
        
    
    def fix_illustrative_materials(self):
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
        
        
    def validate_article_metadata(self):
        errors = [] 
        warnings = [] 
        xml_affs    = self.generic.return_value(self.json_data['f'], '170')
        affiliations = self.generic.return_value(self.json_data['f'], '70')
        pages = self.generic.return_singleval(self.json_data['f'], '14')
        if not 'f' in pages:
            errors.append('Missing pages')
        if self.publication_dateiso == '':
            errors.append('Missing publication date')
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
 

class JSONIssue:
    def __init__(self, generic):
        self.generic = generic

    def load_json(self, json_data):
        self.json_data = json_data
        
    def return_issue(self, journal):
        suppl = ''
        order = ''
        vol = ''
        num = ''
        date = ''

        data = self.json_data
        suppl = self.generic.return_singleval(data, '131')
        suppl = self.generic.return_singleval(data, '132')
        vol = self.generic.return_singleval(data, '31')
        num = self.generic.return_singleval(data, '32')
        date = self.generic.return_singleval(data, '65')
        order = self.generic.return_singleval(data, '36')

        
        if 'suppl' in num.lower():
            if ' ' in num:
                if '(' in num:
                    suppl = num[num.find('(')+1:]
                    suppl = suppl[0:suppl.find(')')]
                else:
                    suppl = num[num.rfind(' ')+1:]
                num = num[0:num.find(' ')]
        return JournalIssue(journal, vol, num, date, suppl, order) 
        
    def return_issue_json_data(self, issue):
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
        return  i_record    


class JSONJournal:
    def __init__(self, json):
        self.json = json

    
    def journal_title(self):
        test = ''
        if '130' in self.json.keys():
            test = self.json['130']
        elif '100' in self.json.keys():
            test = self.json['100']

        return test

    def journal_issn_id(self):
        return self.json['400']

    def journal_acron(self):
        return self.json['68']

class JSON2Models:
    def __init__(self, report):
        self.report = report


        #self.general_report = general_report
        self.generic = Generic()
        self.json_article = JSONArticle(self.generic, AffiliationTable())
        self.json_issue = JSONIssue(self.generic)


    
    def return_journals_list(self, json):
        #json = self.db2json(title_db_filename)
        journal_list = JournalList()
        for json_item in json:
            json_journal = JSONJournal(json_item)
            j = Journal(json_journal.journal_title(), json_journal.journal_issn_id(), json_journal.journal_acron())
            
            journal_list.insert(j, False)
        return journal_list

    def return_issues_list(self, json_issues, journals):
        issues_list = JournalIssues()
        for json_issue in json_issues:
            title = self.return_journal_title(json_issue)
            j = journals.find_journal(title)
            if j != None:
                issue = self.return_issue(json_issue, j)
                issue.json_data = json_issue
                issues_list.insert(issue, False)
        return issues_list
    
    

    def return_journal_title(self, title_json_data):
        return JSONJournal(title_json_data).journal_title()
   
    def return_article_journal_title(self, article_json_data):
        return JSONJournal(article_json_data['doc']['f']).journal_title()
   
    

    def return_article(self, article_json_data, journal, img_files,  xml_filename, article_report):
        article = None
        
        
        self.json_article.load_json(article_json_data['doc'], xml_filename, article_report)
        
        self.json_article.fix_and_validate(img_files)

        ###
        self.json_issue.load_json(article_json_data['doc']['h'])
        issue = self.json_issue.return_issue(journal)
        issue.json_data = self.json_issue.return_issue_json_data(issue)

        article = self.json_article.return_article(issue, xml_filename)
        
        section_title = self.json_article.return_section_title()
        if len(section_title) > 0:
            section = article.issue.toc.insert(Section(section_title), False)
            self.json_article.set_section_code(section.code)
            article.section_title = section_title
    

        article.issue.articles.insert(article, True)
        article.json_data = self.json_article.json_data

        return article

    def return_issue(self, json_data, journal):
        self.json_issue.load_json(json_data)
        return self.json_issue.return_issue(journal)

