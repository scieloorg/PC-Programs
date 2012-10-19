#<!ENTITY lsaquo  CDATA "&#8249;"  -- single left-pointing angle quotation mark, u+2039 ISO proposed -->
#caracter|&#192;|&Agrave;|capital a, grave accent|a
f = open('entity.seq', 'r')
c = f.readlines()
f.close()


for line in c:
	if line.startswith('<!ENTITY'):
		cleaned = line[0:line.rfind('-->')]
		while '  ' in cleaned:
			cleaned = cleaned.replace('  ', ' ')
		parts = cleaned.split(' ')
		print(parts[1] + '|' + parts[3].replace('"','') + '|&' + parts[1]  + ';|' + cleaned[cleaned.find('--')+2:] + '|' + parts[1])