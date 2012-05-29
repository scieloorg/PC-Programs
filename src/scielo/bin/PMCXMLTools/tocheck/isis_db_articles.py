from isis_record import ISISRecord
from ISODateTimeNow import ISODateTimeNow
from isis_record_article import Article_ISISRecord

now = ISODateTimeNow()
isis_record = ISISRecord()
tocheader = {}
tocheader['en'] = 'Table of Contents'
tocheader['es'] = 'Sumario'
tocheader['pt'] = 'Sumario'

label_vol = {}
label_vol['en'] = 'v.'
label_vol['es'] = 'v.'
label_vol['pt'] = 'vol.'

label_num = {}
label_num['en'] = 'n.'
label_num['es'] = 'n.'
label_num['pt'] = 'no.'

label_suppl = {}
label_suppl['en'] = 'suppl.'
label_suppl['es'] = 'sup.'
label_suppl['pt'] = 'sup.'

label_months = {}
label_months['en'] = ['Jan.','Feb.','Mar.','Apr.','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.', ]
label_months['es'] = ['ene.','feb.','mar.','abr.','mayo','jun.','jul.','ago.','set.','oct.','nov.','dic.',]
label_months['pt'] = ['jan.','fev.','mar.','abr.','maio','jun.','jul.','ago.','set.','out.','nov.','dez.',]


class Articles_ISISDB:
    def __init__(self, param_journal, param_issue, param_articles, control_info):
        self.journal = param_journal
        self.issue = param_issue
        self.articles = param_articles
        self.control_info = control_info
        
    def generate_i_record(self):
    	r = '!ID 000001' + "\n" 
    	l = []
    	
    	l.append(('991', '1'))
    	l.append(('700', '0'))
    	l.append(('706', 'i'))
    	l.append(('701', '1'))
    	l.append(('091', now.get_date()))
    	
    	l.append(('130', self.journal.get_title()))
    	l.append(('421', self.journal.get_title('medline')))
    	l.append(('151', self.journal.get_title('iso')))
    	l.append(('030', self.journal.get_title('abbrev')))
    	
    	l.append(('230', self.journal.get_parallel_titles()))
    	l.append(('035', self.journal.get_issn()))
    	l.append(('480', self.journal.get_publisher()))
    	
    	l.append(('031', self.issue.get_volume()))
    	l.append(('032', self.issue.get_number()))
    	l.append(('131', self.issue.get_volume_suppl()))
    	l.append(('132', self.issue.get_number_suppl()))
    	l.append(('036', self.issue.get_year_order()))
    	
    	
    	l.append(('930', self.control_info.get_acron().upper()))
    	l.append(('042', self.control_info.get_issue_status()))
    	l.append(('117', self.control_info.get_standard()))
    	l.append(('085', self.control_info.get_descriptor()))
    	l.append(('200', self.control_info.get_is_markup_done()))
    	l.append(('065', self.control_info.get_dateiso()))
    	l.append(('122', self.control_info.get_document_count()))
        
    	
    	for lang in ['en', 'es', 'pt']:
    	    l.append(('048','^l' + lang + '^h' +  tocheader[lang]))
    	    sections = self.issue.get_sections(lang)
    	    bibstrip = ''
    	    for section in sections:
    	        l.append(('049','^l' + lang + '^c' + section[0] +  '^t' + section[1]))
    	    
    	    value = self.issue.get_volume()
    	    if value != '':
    	        bibstrip = bibstrip +  '^v' + label_vol[lang] + value
    	    value = self.issue.get_number()
    	    if value != '':
    	        bibstrip = bibstrip +  '^n' + label_num[lang] + value
    	        
    	    value = self.issue.get_volume_suppl()
    	    if value != '':
    	        bibstrip = bibstrip +  '^w' + label_suppl[lang] + value
    	            
    	    value = self.issue.get_number_suppl()
    	    if value != '':
    	        bibstrip = bibstrip +  '^s' + label_suppl[lang] + value
    	            
    	    value = label_months[lang][0]
    	    if value != '':
    	        bibstrip = bibstrip +  '^m' + value
    	        #+ label_months[lang][str(int(self.control_info.get_dateiso()[4:8]))] + self.control_info.get_dateiso()[0:4]
    	            
    	    l.append(('043', '^l' + lang + '^t' + self.journal.get_title('abbrev') + bibstrip)) 
    	
    	r = r + isis_record.build_record(l)
        
    	return r
    	
    def generate_article_records(self):
        r = self.generate_i_record()
        id = 2
        for a in self.articles:
            record_a = Article_ISISRecord(self.journal, self.issue, a, self.control_info)
            records = record_a.generate_records()
            for rec in records:
    		    n = '000000' + str(id) 
    		    r = r + '!ID ' + n[-6:] + "\n"
    		    r = r + rec
    		    id += 1
        return r
        