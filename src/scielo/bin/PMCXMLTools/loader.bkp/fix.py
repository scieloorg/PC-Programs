f = open('temp', 'r')
content = f.readlines()
f.close()

for line in content:
    if '|' in line:
        c = line.replace("\n", "").split("|") 
        #print(c)
        # h|article|002||MANDATORY|||||||.//scielo//filename
        reg = c[0]
        index = c[1]
        tag = c[2]
        subf =  c[3]
        mandatory = c[4]
        xpath = c[11]
        default = c[9]
        attr = c[10]
        table = ''
        try: 
            table = c[12]
        except:
            pass
        x = ''
        elem = ''
        s = [ reg, index, tag, subf, x, x, x, mandatory, x, x, x, xpath, elem, attr, x, x, x, default, table, ]
        
        text = ''
        for a in s:
            text +=  a + '|'
        print(text)
        






