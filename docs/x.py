f=open('source/titlemanager_title.rst')
c = f.readlines()
f.close()


s = ''
for l in c:
    a = l.replace('[[BR]]','\n').replace('a)','\n- ').replace('b)','\n- ').replace('c)','\n- ').replace('d)','\n- ').replace('e)','\n- ').replace('f)','\n- ')
    if '= ' in a:
        if ' =' in a:
            a = a.replace('=','').strip()
            x = ''
            for i in a:
                x = x + '-'
            a = a + '\n' + x
    if '....' in a:
    	test = a.replace('....', '')
        if not test == '\n':
	    a = test + '\n' 
            for i in test:
                a = a + '.'
      
    s = s + a + '\n'

s = s.replace('\n\n....','\n....').replace('\n\n==','\n==').replace('\n\n--','\n--').replace('\n\n\n','\n\n')
s = s.replace('\n\n\n','\n\n')
print s    
