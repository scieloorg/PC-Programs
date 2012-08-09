# -*- coding: utf-8 -*-

from journal_issue_article import Journal
from journal_issue_article import JournalIssue
from journal_issue_article import Article
from journal_issue_article import Section

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

    def replace_value(self, doc, table_name, rec_name, tag):
        a = self.get(doc, rec_name, tag)
        if a != None:
            doc['doc'][rec_name][tag] = self.conversion_tables.return_fixed_value(table_name, a)
        return doc
                
    

    def fix_keywords(self, doc):
        list = self.get(doc, 'f', '85')
        
        #print(list)
        lang = ''
        new = [{}]
        if list != None:
            
            for item in list:
                if type(item) == type({}):

                    if 'l' in item.keys():
                        lang = item['l']
                    for kw in item['k']:
                        new.append({'k': kw, 'l': lang})
                elif type(item) == type(''):
                
                    new.append({'k' : item, 'l': 'en'})

            doc['doc']['f']['85'] = new    
        return doc
    
    

    def fix_f_record(self, doc):
        doc = self.fix_keywords(doc)
        doc = self.replace_value(doc, 'doctopic', 'f', '71')
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
        aff = self.get(doc, 'f', '70')
        if aff != None:
            if type(aff) == type([]):
                new_aff = []
                for a in aff:
                    r = self.fix_aff(a)
                    new_aff.append(r)

            else:
                new_aff = self.fix_aff(aff)
            if len(new_aff) > 0:
                doc['doc']['f']['70'] = new_aff
        return doc

    def fix_aff(self, aff):

        new_aff = aff 
        list = []
        unmatched = []
        if ',' in aff['_']:
            new_aff['4'] = aff['_']
            new_aff['_'] = ''

            aff_parts = aff['_'].split(', ')
            for key, s in self.conversion_tables.tables['aff'].items():
                for part in aff_parts:
                    if key in part:
                        new_aff[s] = part.strip() 
                        list.append(part)
            for part in aff_parts:
                if not part in list:
                    unmatched.append(part)
            if len(unmatched) > 0:
                new_aff['2'] = ', '.join(unmatched)
            aff = new_aff
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
        doc_f = article_json_data['doc']['f']
        
        journal = journal_list.find_journal(doc_f['100'])
        if journal == None:
            journal = Journal(doc_f['100'], doc_f['35'])
            
        issue = self.return_issue(doc_f, journal)
        issue.json_data = self.return_issue_json_data(doc_f, issue)

        article = self.return_article(article_json_data, issue)
        article.xml_filename = xml_filename
        article = self.update_toc(article)

        return article

    

    
    def update_toc(self, article):
        
        section_title = ''
        if '49' in article.json_data['f'].keys():
            section_title = article.json_data['f']['49']

        section = article.issue.toc.insert(Section(section_title), False)

        article.json_data['f']['49'] = section.code
        article.section_title = section_title
        article_json_data = {}
        article_json_data['doc'] = article.json_data
        article_json_data = JSON_ArticleFixer().fix_json_data(article_json_data)
        article.json_data = article_json_data['doc']

        article.issue.articles.insert(article, True)
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
   
    

    