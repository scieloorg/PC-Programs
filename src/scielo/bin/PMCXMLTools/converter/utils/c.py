f = open('pmcxml2isis.txt', 'r')
content = f.readlines()
f.close()

r = ''
a = []
for i in content:
    col = i.replace("\n", '').split("|")
    
    if len(col)>1:
        #print(col)
        r = '' 
    
        if col[0] == 'h':
            r += 'article|article-meta h|' 
        else:
            r += 'article|ref r|'
            
        r += col[11].replace('article-meta//', '') + ' ' 
        if col[4] != '':
            r += col[4]
        else:
            r += col[2]
        r += '|'
        
        if col[12] != '' and col[13]!= '':
            r += col[12] + '#' + col[13] 
        else:
            r += col[12]
            r += col[13]
        r += ' ' + col[3]
        r += '|' + col[17]
        a.append(r)  
        print(r)
    else:
        print('')
    

    