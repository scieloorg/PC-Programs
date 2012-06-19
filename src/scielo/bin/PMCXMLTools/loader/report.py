class Report:

    def __init__(self, filename, debug = 0):
        f = open(filename, 'w')
        f.close()
        
        self.debug = debug
        self.filename = filename
        
    def register(self, action, label):
        print( "")
        print(label)
        print(action)
        print( "")
        
    def debugging(self, action, label, level=0):
        display = False
        if level >0:
            if self.debug == level: 
                display = True
        else:
            display = (self.debug>0)
            
        if display:
            print("\n"  + '[DEBUG]')
            print(label)
            print(action)
            print('[/DEBUG]' + "\n" )
            
    def display_data(self, message, data):
        
        print('==> ' +  message ) 
        
        
        try: 
            print(data)
        except:
            print('unabled to print data')
        print('------------------------------------') 
            