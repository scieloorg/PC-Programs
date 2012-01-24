
class GroupItem:
	def __init__(self):
		self.item_name = ''
		self.tr = {}
		self.tr = ''
	def translate(self,lang,term):
		self.tr = term
	def display(self):
		print "item: " +self.item_name
		print self.tr
    def translated():
        return self.tr
        
class GroupItems:
	def __init__(self):
		self.dict = {}
	def append(self, item):
		self.dict[item.item_name] = item
	def display(self):
		for k,v in self.dict.items():
			v.display()
			
class Group:
	def __init__(self):
		self.group_name = ''
		self.items = GroupItems()
	def append(self,item):
		self.items.append(item)
	def display(self):
		print "-----"
		print self.group_name
		self.items.display()
		print "....."
		print ''

class Bar:
	def __init__(self):
		self.list = []
		
	def display(self):
		for i in self.list:
			i.display()
		
	def atualiza_grupo(self, grupo, part):
		if grupo.group_name == '':
			grupo.group_name = part[0]
		else:
			item = GroupItem()
			item.item_name = part[0]
			item.translate(self.lang, part[1])
			grupo.append(item)
		return grupo

	def get_translations():
	    d = {}
	    for g in self.list:
	        for item in g: 
	            d[ id ][ self.lang ] = item.translated()
	    return d
	     
	def load_bars(self, file_name, lang):
	    f = open(file_name, 'r')
	    content = f.readlines()
	    f.close()
	    
	    self.lang = lang
	    grupo = Group()
	    for line in content:
	    	s = str(line)
	    	s = s.replace('\r\n','' )
	        part = s.split(';')
	        #print part
	        if part[0] == 'down':
	        	pass
	        else:
	        	if part[0] != '':
	        		grupo = self.atualiza_grupo(grupo, part)
	        		
	        	else:
					if grupo.group_name != '':
						self.list.append(grupo)
					else:
						pass
					grupo = Group()	
	    return self.list   
    
bar = Bar()
pt = bar.load_bars('../pt_bars.mds','pt')
es = bar.load_bars('../es_bars.mds','es')
en = bar.load_bars('../en_bars.mds','en')

bar.display()
        