
class Bar:
    def __init__(self):
        self.d = {}
        self.order = []
    def load_bars(self, file_name, lang):
        f = open(file_name, 'r')
        content = f.readlines()
        f.close()
        self.lang = lang
        for line in content:
            s = str(line)
            s = s.replace('\r\n','' )
            part = s.split(';')
            if len(part)>2:
                #traducoes
                item_name = part[0]
                k = group_name + ';' + item_name
                try:
                    self.d[k][lang] = part[1]
                except:
                    self.d[k] = {}
                    self.order.append(k)
                    self.d[k][lang] = part[1]
            else:
                if len(part)==0:
                    #termina grupo
                    group_name = '' 
                else:
                    if part[0]!='down':
                        group_name = part[0]
                    else:
                        pass
    def write(self):
        for i in self.order:
            v = self.d[i]
            print i
            
            try:
                print v['pt']
            except:
                print ''
            try:
                print v['es']
            except:
                print ''
            try:
                print v['en']
            except:
                print ''
            print ''
            
bar = Bar()

bar.load_bars('../pt_bars.mds','pt')

bar.load_bars('../es_bars.mds','es')

bar.load_bars('../en_bars.mds','en')

bar.write()
        