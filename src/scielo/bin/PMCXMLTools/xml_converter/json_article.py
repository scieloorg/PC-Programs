# -*- coding: utf-8 -*-

from journal_issue_article import Journal, JournalIssue, Article, Section

from table_ent_and_char import TableEntAndChar
from table_conversion import ConversionTables
from utils.aff_table import AffiliationTable
from utils.table_issn import ISSN_Table

class Generic:
    def __init__(self, general_report):
        self.general_report = general_report
        self.conversion_tables = ConversionTables()
        self.table_entity_and_char = TableEntAndChar()

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

    def return_json_data_multi_values(self, json_data, tag):
        # group_name = h, f, l, c, etc
        r = []
        if tag in json_data.keys():
            r = json_data[tag]
            if type(r) != type([]):
                r = [r]  
        return r

    def return_json_data_single_value(self, json_data, tag):
        # group_name = h, f, l, c, etc
        r = ''
        if tag in json_data.keys():
            r = json_data[tag]
            if type(r) == type([]):
                r = r[0] 
        return r

    def convert_value(self, json_data, tag, table_name):
        a = self.return_json_data_single_value(json_data, tag)
        if len(a)>0:
            json_data[tag] = self.conversion_tables.return_fixed_value(table_name, a)
    
        return json_data

    def fix_dates(self, json_data, tag_iso, tag_noiso):

        if tag_iso in json_data.keys():
            d_iso = json_data[tag_iso]
            if type(d_iso) == type([]):
                d_iso = json_data[tag_iso][0]
            m = '00'
            d = '00'
            y = '0000'
            if len(d_iso) >= 4:
                y = d_iso[0:4]
            if len(d_iso) >= 6:
                m = d_iso[4:6]
            if len(d_iso) >= 8:
                d = d_iso[6:8]
            res = {'m': m, 'd': d}
            for item in res.keys():
                if res[item] == '00':
                    if tag_iso + item in json_data.keys():
                        r = '00' + json_data[tag_iso + item]
                        r = r[-2:]
                        del json_data[tag_iso + item]
                        res[item] = r
            
            if res['m'] == '00': 
                if tag_noiso in json_data.keys():
                    m = self.return_month_number(json_data[tag_noiso])
                    if len(m)>2:
                        d = m[2:4]
                    m = m[0:2]
            json_data[tag_iso] = y + m + d
        return json_data     

    def return_month_number(self, textual_date):
        d = '00'

        if type(textual_date) == type(''):
            m = textual_date
        elif type(textual_date) == type([]):
            m = textual_date[0]
        if m.isdigit():
            if len(m) == 4:
                # is year
                m = '00'
            elif len(m) <= 2:
                # is month
                m = '00' + m
                m = m[-2:]
        else:
            
            date_parts = []
            if ' ' in m:
                date_parts = m.split(' ')
            else:
                date_parts.append(m)

            m = '00'
            for part in date_parts:
                if part.isdigit() and len(part) <= 2:

                    d = '00' + part
                    d = d[-2:]
                else:
                    if '-' in part:
                        part = part[part.find('-')+1:]
                    
                    r = self.conversion_tables.return_month_number(part)
                    if r != '00':
                        m = r
            
        return m + d

    def fix_history(self, json_data, tag_date, tag_dateiso):
        if tag_dateiso in json_data.keys():
            json_data[tag_date] = self.fix_history_date_display(json_data[tag_dateiso])
            json_data[tag_dateiso] = self.fix_history_date(json_data[tag_dateiso])
        return json_data

    def fix_history_date(self, json_data_date):
        k = 'ymd'
        r = ''
        for key  in k:
            if key in json_data_date:
                r += json_data_date[key]
            else:
                r += '00'
                if key == 'y':
                    r += '00'
        return r

    def fix_history_date_display(self, json_data_date):
        k = 'dmy'
        r = []
        for key  in k:
            if key in json_data_date:
                r.append(json_data_date[key])

        return '/'.join(r)

    
   


class TaggedData:

    def __init__(self, general_report):
        self.general_report = general_report
        self.generic = Generic(general_report)
        self.issn_table = ISSN_Table()
        self.table_aff = AffiliationTable()

        # book, conf-proc, journal, patent, thesis, report, 
        # communication, letter, review, list, discussion, standard, and working-paper
        doctopics = {}
        doctopics['journal'] = ['65', '12', '30']
        doctopics['book'] = [ '65', '62', '18',  ]
        doctopics['book-part'] = [ '65', '62', '18',  '12',]

        doctopics['conf-proc'] = ['65', '53', ]
        doctopics['thesis'] = ['65',  '51' ]
        doctopics['patent'] = ['65', '150', ]
        doctopics['report'] = ['65', '58', '60', ]
        doctopics['software'] = ['65', '95', ]
        doctopics['web'] = ['37', '109']
        doctopics['unidentified'] = ['65', ]

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
        self._doctopics = doctopics

    def load(self, json_data, filename, article_report):
        self.json_data = json_data
        self.article_report = article_report
        self.filename = filename


    def return_journal_title(self):
        return self.json_data['f']['100']

    def return_issn_id(self):
        return self.json_data['f']['35']
     
    def return_issue(self, journal, data = None):

        suppl = ''
        order = ''
        vol = ''
        num = ''
        date = ''

        
        if data == None:
            data = self.json_data['f']

        suppl = self.generic.return_json_data_single_value(data, '131')
        suppl = self.generic.return_json_data_single_value(data, '132')
        vol = self.generic.return_json_data_single_value(data, '31')
        num = self.generic.return_json_data_single_value(data, '32')
        date = self.generic.return_json_data_single_value(data, '65')
        order = self.generic.return_json_data_single_value(data, '36')

        
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
        for key, item in self.json_data['f'].items():
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

    def return_article(self, issue):   
        doc_f = self.json_data['f']
        
        #print([ k  for k in doc_f.keys() ])
        surname = ''
        if '10' in  doc_f.keys():            
            if type(doc_f['10']) == type([]):
                surname =  doc_f['10'][0]['s']
            else:
                surname =  doc_f['10']['s']
        if type(doc_f['14']['f']) == type(''):
            page = doc_f['14']['f']
        else:
            page = doc_f['14']['f'][0]
        self.json_data['35'] = issue.journal.issn_id
        return Article(issue, page, surname)

    def return_section_title(self):
        return self.generic.return_json_data_single_value(self.json_data['f'], '49')

    def set_section_code(self, section_code):
        self.json_data['f']['49'] = section_code
        self.json_data['h']['49'] = section_code
        self.json_data['l']['49'] = section_code

    

    def return_issn_and_norm_title(self, citation):
        if '30' in citation.keys() and not '35' in citation.keys():
            issn, journal_title = self.issn_table.return_issn_and_normalized_title(citation['30'])
    
            if len(issn) > 0:
                citation['35'] = issn
                if len(journal_title) > 0:
                    citation['801'] = journal_title
        return citation

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
        roles = self.generic.return_json_data_multi_values(citation, 'roles')
        roles = [ self.generic.conversion_tables.return_fixed_value('role', r)  for r in roles ]
        #print(roles)
        if len(roles) > 0:
            del citation['roles']

        authors_monog = self.generic.return_json_data_multi_values(citation, '16')
        #print(authors_monog)
        if len(roles) > 0:
            for a in authors_monog:
                a['r'] = roles[len(roles)-1]
                #print(a)
            if len(authors_monog) > 0:
                citation['16'] = authors_monog
        #print(authors_monog)
        

        authors_analyt = self.generic.return_json_data_multi_values(citation, '10')
        #print(authors_analyt)
        if len(roles) > 0:
            for a in authors_analyt:
                a['r'] = roles[0]
                #print(a)
            if len(authors_analyt) > 0:
                citation['10'] = authors_analyt
        #print(authors_analyt)
        analytic_title = self.generic.return_json_data_multi_values(citation, '12')
        
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
        citation = self.generic.fix_dates(citation, '65', '64')
        citation = self.fix_citation_issue_number(citation)
        #citation = self.fix_citation_doctopic(citation)
        #citation = self.return_issn_and_norm_title(citation)
        citation['865'] = self.json_data['f']['65']
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



    def fix_keywords(self):
        keyword_groups = self.generic.return_json_data_multi_values(self.json_data['f'], '85')
        
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
            
    
    

    def fix_metadata_authors(self):
        authors = self.generic.return_json_data_multi_values(self.json_data['f'], '10')
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
        self.json_data['f'] = self.generic.fix_history(self.json_data['f'], '111', '112')
        self.json_data['f'] = self.generic.fix_history(self.json_data['f'], '113', '114')

        if '120' in self.json_data['f'].keys():
            self.json_data['f']['120'] = 'XML_' + self.json_data['f']['120']
        self.json_data['f']['42'] = '1'
        
        self.json_data['f'] = self.generic.fix_dates(self.json_data['f'], '65', '64')
        
        self.fix_illustrative_materials()
        self.fix_affiliations()
        

    def fix_affiliations(self):
        affiliations = self.generic.return_json_data_multi_values(self.json_data['f'], '70')

        new_affiliations = [ self.table_aff.complete_affiliation(aff)  for aff in affiliations ]
        new_affiliations = self.table_aff.complete_affiliations(new_affiliations)
        
        id = ''
        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
            if 'i' in new_affiliations[0].keys():
                id = new_affiliations[0]['i']
    
        if id != '':
            authors = self.generic.return_json_data_multi_values(self.json_data['f'], '10')
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
            count = self.generic.return_json_data_single_value(self.json_data['f'], tag)
            if len(count)>0:
                if int(count)>0:
                    illustrative_materials.append(type)
                del self.json_data['f'][tag]
        
        if len(illustrative_materials) > 0:
            self.json_data['f']['38'] = illustrative_materials
        else:
            self.json_data['f']['38'] = 'ND'
        


    def fix_and_validate(self, img_files):
        count_errors = 0
        self.fix_metadata()
        self.json_data['h'] = self.generic.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.generic.format_for_indexing(self.json_data['h'])
        
        #self.article_report.write(self.filename, True, False, False)
        #self.general_report.write(self.filename, True, False, False)


        errors, warnings = self.validate_article_metadata()
        if len(warnings) > 0:
            self.article_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' + ', '.join(warnings), False, True, False)
            self.general_report.write('\n'+ ' ! WARNING: Missing desirable data in article front : ' + ', '.join(warnings), False, True, False)
            count_errors += len(warnings)
        if len(errors) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            self.general_report.write('\n'+ ' ! ERROR: Missing required data in article front : ' + ', '.join(errors), False, True, False)
            count_errors += len(errors)

        #####
        missing_files = []
        missing_href = []
        href_list = []
        if 'body' in self.json_data:
            href_list = list(set(self.generic.return_json_data_multi_values(self.json_data['body'], 'file')))
        for href in href_list:
            if not href in img_files:
                missing_files.append(href)
        if len(missing_files) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing image files: ' + ', '.join(missing_files), False, True, False)
            self.general_report.write('\n'+ ' ! ERROR: Missing image files: ' + ', '.join(missing_files), False, True, False)
            count_errors += len(missing_files)
        for file in img_files:
            if not file in href_list:
                missing_href.append(file)

        if len(missing_href) > 0:
            self.article_report.write('\n'+ ' ! ERROR: Missing graphic/@xlink:href: ' + ', '.join(missing_href), False, True, False)
            self.general_report.write('\n'+ ' ! ERROR: Missing graphic/@xlink:href: ' + ', '.join(missing_href), False, True, False)
            count_errors += len(missing_href)

        if len(missing_href) + len(missing_files)  > 0:
            print('VERIFICAR')
            print(href_list)
            print(img_files)
        ###     

        k = 0
        for citation in self.json_data['c']:
            citation = self.generic.format_for_indexing(citation)
            citation = self.fix_citation(citation, k)
            missing_data = self.validate_citation_metadata(citation)
            if len(missing_data) > 0:
                self.article_report.write('\n'+ ' ! WARNING: Missing data in citation ' + str(k + 1) +': ' + ', '.join(missing_data), False, True, False)
                self.general_report.write('\n'+ ' ! WARNING: Missing data in citation ' + str(k + 1) +': ' + ', '.join(missing_data), False, True, False)
                if '704' in citation.keys():
                    self.article_report.write('\n'+citation['704'], False, True, False)
                    self.general_report.write('\n'+citation['704'], False, True, False)
                count_errors += len(missing_data)
            
            self.json_data['c'][k] = citation 
            k += 1
        self.article_report.write('  References:' + str(k), True, False, False)
        self.general_report.write('  References:' + str(k), True, False, False)
        

        self.article_report.write('Errors found: ' + str(count_errors), True, True, False)
        self.general_report.write('Errors found: ' + str(count_errors), True, True, False)
        
    def validate_article_metadata(self):
        errors = [] 
        warnings = [] 
        xml_error = self.generic.return_json_data_multi_values(self.json_data['f'], '770')
        list = self.generic.return_json_data_multi_values(self.json_data['f'], '70')
        i = 0
        for aff in list:
            if not 'p' in aff:
                xml = ''
                if len(list) == len(xml_error):
                    xml = '\n' + xml_error[i] + '\n'
                if 'i' in aff.keys():
                    warnings.append('Incomplete affiliation ' + aff['i'] + xml)
                else:
                    warnings.append('Incomplete affiliation ' + xml)
            i += 1
        return (errors, warnings)

    
class JSON_Article:
    def __init__(self, debug_report, general_report ):
        self.debug_report = debug_report
        self.general_report = general_report
        self.tagged_data = TaggedData(general_report)
    

    def return_article(self, article_json_data, img_files, journal_list, xml_filename, article_report):
        article = None

        self.tagged_data.load(article_json_data['doc'], xml_filename, article_report)
        
        journal = journal_list.find_journal(self.tagged_data.return_journal_title())
        if journal == None:

            #journal = Journal(self.tagged_data.return_journal_title(), self.tagged_data.return_issn_id())
            article_report.write(self.tagged_data.return_journal_title() + ' was not found in title database. The processing will use ' + self.tagged_data.return_issn_id() +  ' as its ISSN.', True, True)
        else:
            self.tagged_data.fix_and_validate(img_files)

            issue = self.tagged_data.return_issue(journal)
            issue.json_data = self.tagged_data.return_issue_json_data(issue)

            article = self.tagged_data.return_article(issue)
            article.xml_filename = xml_filename

            section_title = self.tagged_data.return_section_title()
            if len(section_title) > 0:
                section = article.issue.toc.insert(Section(section_title), False)
                self.tagged_data.set_section_code(section.code)
                article.section_title = section_title
        

            article.issue.articles.insert(article, True)
            article.json_data = self.tagged_data.json_data

        return article

    def return_issue(self, json_data, journal):
        return self.tagged_data.return_issue(journal, json_data)

