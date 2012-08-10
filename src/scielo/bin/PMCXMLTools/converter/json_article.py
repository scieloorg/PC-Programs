# -*- coding: utf-8 -*-

from journal_issue_article import Journal, JournalIssue, Article, Section

from table_ent_and_char import TableEntAndChar
from table_conversion import ConversionTables

class JSON_ArticleFixer:
    def __init__(self):
        self.conversion_tables = ConversionTables()
        self.table_entity_and_char = TableEntAndChar()
        self.sections = {}

    def fix_json_data(self, article_json_data):
        article_json_data = self.fix_f_record(article_json_data)
        article_json_data['doc']['h'] = self.format_for_indexing(article_json_data['doc']['f'])
        article_json_data['doc']['l'] = self.format_for_indexing(article_json_data['doc']['h'])
        
        for rec in article_json_data['doc']['c']:
            rec = self.format_for_indexing(rec)
            
        return article_json_data

    def get(self, doc, rec_name, tag):
        if tag in doc['doc'][rec_name].keys():
            v = doc['doc'][rec_name][tag]
        else:
            v = None
        return v

    def convert_value(self, doc, table_name, rec_name, tag):
        a = self.get(doc, rec_name, tag)
        if a != None:
            doc['doc'][rec_name][tag] = self.conversion_tables.return_fixed_value(table_name, a)
        return doc
                
    

    def fix_keywords(self, doc):
        kw_groups = self.get(doc, 'f', '85')
        keyword_groups = []
        if type(kw_groups) == type({}):
            keyword_groups.append(kw_groups)
        else:
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
            print(new)
            doc['doc']['f']['85'] = new    
        return doc
    
    

    def fix_f_record(self, doc):
        doc = self.fix_keywords(doc)
        doc = self.convert_value(doc, 'doctopic', 'f', '71')
        
        if '120' in doc['doc']['f'].keys():
            doc['doc']['f']['120'] = 'XML_' + doc['doc']['f']['120']

        doc['doc']['f']['42'] = '1'
        doc['doc']['f']['42'] = '1'

        if len(doc['doc']['f']['65']) == 4:
            m = '00'
            if '64' in doc['doc']['f'].keys():
                m = doc['doc']['f']['64']
                m = self.return_month_number(m)
            doc['doc']['f']['65'] = doc['doc']['f']['65'] + m + '00'
        doc = self.fix_38(doc)

        doc = self.fix_affiliations(doc)

        return doc
    
    def fix_affiliations(self, doc):
        aff_occs = self.get(doc, 'f', '70')
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

            
        if len(new_affiliations) > 0:
            doc['doc']['f']['70'] = new_affiliations
        return doc

    def fix_aff(self, aff):

        new_aff = aff 
        list = []
        unmatched = []

        if not 'p' in aff.keys():
            if ', ' in aff['_']:
                full_affiliation = aff['_']
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

                    
                loc = ''
                if len(state) > 0:
                    loc += ', ' + state
                if len(country) > 0:
                    loc += ', ' + country
                if len(loc) > 0:
                    p = full_affiliation.find(loc)
                    if full_affiliation[p:] == loc:
                        city = full_affiliation[0:p]
                        city = city[city.rfind(', ')+2:]
                        loc = ', ' + city + loc
                        aff['c'] = city
                        if len(state) > 0:
                            aff['s'] = state
                        if len(country) > 0:
                            aff['p'] = country
                unidentified = sep = ''
                for aff_part in aff_parts:
                    if not aff_part in aff.values():
                        unidentified += aff_part + sep
                        sep = ', '
                if aff['_'] == '':
                    aff['_'] = unidentified
                    aff['5'] = '?'
                else:
                    aff['1'] = unidentified
                
            
        return aff 



    
    def fix_38(self, doc):
        v38 = []
        fig_count = self.get(doc, 'f', '901')
        if fig_count != None:

            if int(fig_count)>0:
                v38.append('GRA')
            del doc['doc']['f']['901']
        tab_count = self.get(doc, 'f', '900')
        if tab_count != None:
            if int(tab_count)>0:
                v38.append('TAB')
            del doc['doc']['f']['900']
        if len(v38) > 0:
            doc['doc']['f']['38'] = v38
        return doc
    
    def return_month_number(self, month_range):
        m = month_range
        
        if m.isdigit():
            m = '00' + m
            m = m[-2:]
        else:
            if '-' in m:
                m = m[m.find('-')+1:]
            m = self.conversion_tables.return_fixed_value('month', m)

        return m 

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
    def __init__(self):
        pass
    
    

    def load_article(self, article_json_data, journal_list, xml_filename):
        article_json_data = JSON_ArticleFixer().fix_json_data(article_json_data)
        doc_f = article_json_data['doc']['f']
        
        journal = journal_list.find_journal(doc_f['100'])
        if journal == None:
            journal = Journal(doc_f['100'], doc_f['35'])
            
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
   
    

    