# -*- coding: utf-8 -*-

from journal_issue_article import Journal, JournalIssue, Article, Section

from table_ent_and_char import TableEntAndChar
from table_conversion import ConversionTables

class JSON_ArticleFixer:
    def __init__(self, report, json_data):
        self.conversion_tables = ConversionTables()
        self.table_entity_and_char = TableEntAndChar()
        self.sections = {}
        self.report = report
        self.json_data = json_data

        doctopics = {}
        doctopics['journal'] = ['12', '30', '10', '65', '14']
        doctopics['book'] = [ '18', '10', '65', '62', '66', '67']
        doctopics['conf-proc'] = ['53', '65']
        doctopics['thesis'] = ['50', '51', '65']
        doctopics['patent'] = ['150', '65']
        doctopics['report'] = ['58', '60', '65']
        doctopics['software'] = ['95', '65']
        doctopics['web'] = ['110']
        doctopics['unidentified'] = ['65', '10']

        self._labels = {}
        self._labels['10'] = 'authors'
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
        self._labels['110'] = 'cited date'
        
        self._doctopics = doctopics

    def fix(self):
        self.fix_metadata()
        self.json_data['h'] = self.format_for_indexing(self.json_data['f'])
        self.json_data['l'] = self.format_for_indexing(self.json_data['h'])

        k = 0
        for citation in self.json_data['c']:
            citation = self.format_for_indexing(citation)
            citation = self.fix_dates(citation, '65', '64')
            citation['865'] = self.json_data['f']['65']
            citation = self.join_pages(citation)
            missing = self.validate_citation(citation) 
            if len(missing) > 0:
                self.report.log_error('Missing data in reference ' + str(k + 1) + ': ' + missing )
                self.report.log_summary(' ! Missing data in reference ' + str(k + 1) + ': ' + missing)
            self.json_data['c'][k] = citation
            k += 1
        return self.json_data
    
    def join_pages(self, citation):
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
                        else:
                            self.report.log_summary(' ! Warning: Check fpage, lpage, page-range of reference ' + str(k + 1))
                            self.report.log_error('Check fpage, lpage, page-range of reference ' + str(k + 1), rec['514'], True)
        return citation

    def validate_citation(self, citation):
        missing = []
        doctopic = ''
        if '71' in citation.keys(): 
            doctopic = citation['71'] 
            if not doctopic in self._doctopics.keys():
                doctopic = 'unidentified'

            for tag in self._doctopics[doctopic]:
                if not tag in citation.keys():
                    if tag in self._labels.keys():
                        missing.append(self._labels[tag])
                    else:
                        missing.append(tag)

        return ', '.join(missing)
         

    def get(self, group_name, tag):
        # group_name = h, f, l, c, etc
        if tag in self.json_data[group_name].keys():
            v = self.json_data[group_name][tag]
        else:
            v = None
        return v

    def convert_value(self, table_name, group_name, tag):
        a = self.get(group_name, tag)
        if a != None:
            self.json_data[group_name][tag] = self.conversion_tables.return_fixed_value(table_name, a)
        
                
    

    def fix_keywords(self):
        kw_groups = self.get('f', '85')
        keyword_groups = []
        if type(kw_groups) == type({}):
            keyword_groups.append(kw_groups)
        else:
            if kw_groups != None:
                keyword_groups = kw_groups
        
        if len(keyword_groups) > 0:
            new = [{}]
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
            #print(new)
            self.json_data['f']['85'] = new    
        
    
    def fix_dates(self, doc, tag_iso, tag_noiso):
        if tag_iso in doc.keys():
            m = '00'
            if tag_noiso in doc.keys():
                m = self.return_month_number(doc[tag_noiso])
                
            if len(doc[tag_iso]) == 4:
                doc[tag_iso] += m
                if len(m) == 2:
                    doc[tag_iso] += '00'
            
        return doc

    

    def fix_metadata(self):
        self.fix_keywords()
        self.convert_value('doctopic', 'f', '71')
        
        if '120' in self.json_data['f'].keys():
            self.json_data['f']['120'] = 'XML_' + self.json_data['f']['120']

        self.json_data['f']['42'] = '1'
        
        self.json_data['f'] = self.fix_dates(self.json_data['f'], '65', '64')
        
        
        self.fix_illustrative_materials()

        self.fix_affiliations()

        
    
    def fix_affiliations(self):
        aff_occs = self.get( 'f', '70')
        affiliations = []

        if type(aff_occs) == type({}):
            affiliations.append(aff_occs)
        else:
            if aff_occs != None:
                affiliations = aff_occs
        new_affiliations = []

        for a in affiliations:
            r = self.fix_aff(a)

            new_affiliations.append(r)
        
        print(new_affiliations)
        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
        

        new_affiliations = self.fix_affiliations_location(new_affiliations)
        print(new_affiliations)

        if len(new_affiliations) > 0:
            self.json_data['f']['70'] = new_affiliations
        

    def fix_aff(self, aff):

        new_aff = aff 
        list = []
        unmatched = []

        if not 'p' in aff.keys():
            if ', ' in aff['_']:
                full_affiliation = aff['_']
                if '</label>' in full_affiliation:
                    full_affiliation = full_affiliation[full_affiliation.find('</label>')+len('</label>'):]
                aff['_'] = ''
                aff['9'] = full_affiliation
                aff_parts = full_affiliation.split(', ')
                

                institution = country = state = ''
                for aff_part in aff_parts:

                    if 'Univ' == aff_part[0:4]:
                        institution = aff_part
                        aff['_'] = institution
                    elif 'U' == aff_part[0:1]:
                        institution = aff_part
                        aff['_'] = institution
                    elif aff_part in self.conversion_tables.tables['country'].keys():
                        country = aff_part

                    elif aff_part in self.conversion_tables.tables['state'].keys():
                        state = aff_part
                    elif aff_part in self.conversion_tables.tables['state'].values():
                        state = aff_part

                    
                loc = ''
                if len(state) > 0:
                    loc += ', ' + state
                if len(country) > 0:
                    loc += ', ' + country
                if len(loc) > 0:
                    p = full_affiliation.find(loc)
                    if full_affiliation[p:] == loc:
                        might_be_city = full_affiliation[0:p]
                        p = might_be_city.rfind(', ')
                        if p > 0:
                            might_be_city = might_be_city[p:]
                        if 
                            loc = might_be_city + loc
                            aff['c'] = might_be_city
                        if len(state) > 0:
                            aff['s'] = state
                        if len(country) > 0:
                            aff['p'] = country
                unidentified = [ aff_part for aff_part in aff_parts if not aff_part in aff.values() ]

                if aff['_'] == '':
                    aff['_'] = ', '.join(unidentified)
                    aff['5'] = '?'
                else:
                    aff['1'] = ', '.join(unidentified)
                
            
        return aff 
    
    def fix_affiliations_location(self, affiliations):
        r = []
        loc = {}
        for aff in affiliations:
            if 'p' in aff.keys():
                l = {}
                l['p'] = aff['p']
                
                if 's' in aff.keys():
                    l['s'] = aff['s']
                if 'c' in aff.keys():
                    l['c'] = aff['c']
                loc[', '.join(l.values())] = l
        location = ''

        if len(loc) > 1:
            print('')
            print('location:')
            print(loc)

        if len(loc) == 1:
            location = loc.values()[0]
            
            for aff in affiliations:
                print(aff)
                if not 'p' in aff.keys():
                    aff['p'] = location['p']
                if not 's' in aff.keys() and 's' in location.keys():
                    aff['s'] = location['s']
                if not 'c' in aff.keys() and 'c' in location.keys():
                    aff['c'] = location['c']
                print(aff)
                r.append(aff)
        return r

    
    def fix_illustrative_materials(self):
        illustrative_materials = []
        fig_count = self.get('f', '901')
        if fig_count != None:

            if int(fig_count)>0:
                illustrative_materials.append('GRA')
            del self.json_data['f']['901']
        tab_count = self.get('f', '900')
        if tab_count != None:
            if int(tab_count)>0:
                illustrative_materials.append('TAB')
            del self.json_data['f']['900']
        if len(illustrative_materials) > 0:
            self.json_data['f']['38'] = illustrative_materials
        else:
            self.json_data['f']['38'] = 'ND'
        
    
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

    def format_for_indexing(self, json_record):
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

    
class JSON_Article:
    def __init__(self, report):
        self.report = report
    
    

    def load_article(self, article_json_data, journal_list, xml_filename):
        doc_f = article_json_data['doc']['f']

        journal = journal_list.find_journal(doc_f['100'])
        if journal == None:
            journal = Journal(doc_f['100'], doc_f['35'])
        
        if '35' in doc_f.keys():
            if doc_f['35'] != journal.issn_id:
                doc_f['35'] = journal.issn_id
        else:
            doc_f['35'] = journal.issn_id

        json_fixer = JSON_ArticleFixer(self.report, article_json_data['doc'])
        article_json_data['doc'] = json_fixer.fix()
        
        
        


        issue = self.return_issue(doc_f, journal)
        issue.json_data = self.return_issue_json_data(doc_f, issue)

        article = self.return_article(article_json_data, issue)
        article.xml_filename = xml_filename
        article = self.update_toc(article)

        
        article.issue.articles.insert(article, True)
        
        return article

    

    
    def update_toc(self, article):
        
        section_title = ''
        if '49' in article.json_data['f'].keys():
            section_title = article.json_data['f']['49']

        section = article.issue.toc.insert(Section(section_title), False)

        article.json_data['f']['49'] = section.code
        article.json_data['h']['49'] = section.code
        article.json_data['l']['49'] = section.code
        article.section_title = section_title
        
        return article

    def return_issue(self, doc_f, journal):
        suppl = ''
        order = vol = num = date = suppl

        if '131' in doc_f.keys():
            suppl = doc_f['131']
            
        if '132' in doc_f.keys():
            suppl = doc_f['132']
        if '31' in doc_f.keys():
            vol = doc_f['31']
        if '32' in doc_f.keys():
            num = doc_f['32'].strip()
        if '65' in doc_f.keys():
            date = doc_f['65']
        if '36' in doc_f.keys():
            order = doc_f['36']
        if 'suppl' in num:
            if ' ' in num:
                if '(' in num:
                    suppl = num[num.find('(')+1:]
                    suppl = suppl[0:suppl.find(')')]
                else:
                    suppl = num[num.rfind(' ')+1:]
                num = num[0:num.find(' ')]
        issue = JournalIssue(journal, vol, num, date, suppl, order) 

        return  issue     

    def return_issue_json_data(self, doc_f, issue):

        i_record = issue.json_data
        keep_list = [30, 31, 32, 132, 35, 42, 65, 100, 480, ]
        for key, item in doc_f.items():
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
        
    def return_article(self, article_json_data, issue):   
        doc_f = article_json_data['doc']['f']
        
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
        article = Article(issue, page, surname)
        article.json_data = article_json_data['doc']

        return article
   
    

    