# -*- coding: iso-8859-1 -*-
class Bar:
    def __init__(self):
        self.elements = {}
        self.elements_order = []
        self.names = {}
        self.texts = {}
        
        
    def load_words(self, translations_file):
        f = open(translations_file, 'r')
        content = f.readlines()
        f.close()
        self.tr = {}
        self.tr_order = []
        for line in content:
            s = str(line)
            s = s.replace("\r", "" ).replace("\n", "")
            part = s.split('|')
            self.tr[ part[0] ] = part
            self.tr_order.append(part[0])
        
    def load_bars(self, file_name, lang):
        f = open(file_name, 'r')
        content = f.readlines()
        f.close()
        
        self.lang = lang
        for line in content:
            s = str(line)
            s = s.replace('\r\n', '' )
            part = s.split(';')
            
            if len(part)>2:
                # botoes de tag
                texto_em_pt = part[1]
                item_name = part[0]
                group_and_item = group_name + ';' + item_name
                
                self.elements_order.append(group_and_item)
                self.elements[group_and_item] = texto_em_pt
                
                try:
                    self.texts[texto_em_pt].append(group_and_item)
                except:
                    self.texts[texto_em_pt] = []
                    self.texts[texto_em_pt].append(group_and_item)
            else:
                if len(part)==0:
                    #termina grupo
                    group_name = '' 
                else:
                    if part[0]!='down':
                        group_name = part[0]
                    else:
                        pass
    
    def return_translated_texts(self):
         r =''
         for k,item in self.texts.items():
    	    r +=  k + "\r\n"
    	    r +=  self.translate_text(k, 'en')+ "\r\n"
    	    r +=  self.translate_text(k, 'es')+ "\r\n"
    	    r +=  "\r\n"
         return r
    
    def print_file(self, filename, content):    
    	f = open(filename, 'wb')
        f.write(content)
        f.close()
    	    
    def translate_text(self, text, lang):
    	index = 0
    	if lang == 'en':
    	    index = 1
    	if lang == 'es':
    	    index = 2
    	t = text
    	for order in self.tr_order:
    	    t = t.replace(self.tr[ order ][0], self.tr[ order ][index])
        
        return t	
    def return_bars_tr(self, lang):
        r = ''
        for group_and_item in self.elements_order:
            r += group_and_item + "\r\n"
            if lang == 'pt':
                r += self.elements[group_and_item]+ "\r\n"
            else:
                r += self.translate_text(self.elements[group_and_item], lang) + "\r\n"
            r += "\r\n"
        return r       
      
bar = Bar()
bar.load_words('words.txt')
bar.load_bars('../pt_bars.mds','pt')
bar.print_file('translated_texts.txt' , bar.return_translated_texts())
bar.print_file('pt_bars.tr', bar.return_bars_tr('pt'))
bar.print_file('es_bars.tr', bar.return_bars_tr('es'))
bar.print_file('en_bars.tr', bar.return_bars_tr('en'))

