import os, shutil

java = 'java'
jar_transform = ''
jar_validate = ''

def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if  ' ' in v:
            r += k + '=' + '"' + v + '" '
        else:
            r += k + '=' +  v + ' '
    return r

def insert_doctype(xml_filename, doctype):
    f = open(xml_filename)
    c = f.read()
    f.close()
    if not doctype in c:
        if '<!DOCTYPE' in c:

            s = c[0:c.find('<!DOCTYPE')]
            c = c[c.find('<!DOCTYPE'):]
            c = c[c.find('>')+1:]
        else:
            a = doctype.replace('  ', ' ').split(' ')
            start = '<' + a[1]
            s = c[0:c.find(start)]
            c = '\n' + c[c.find(start):]
        c = s + doctype + c
        f = open(xml_filename , 'w')
        f.write(c)
        f.close()

def replace_dtd_path(xml_filename, dtd_path):
    f = open(xml_filename)
    content = f.read()
    f.close()

    if not dtd_path in content:

        old = content
        if not '<!DOCTYPE' in content:
            #print('none')
            start = content[1:]
            start = start[0:start.find('>')]
            if ' ' in start:
                start = start[0:start.find(' ')]
            #print('start:' + start)
            content = content.replace('<' + start, '<!DOCTYPE ' + start + ' PUBLIC "" "">' + '\n' + '<' + start) 
            #print('content:' + content)

        if '<!DOCTYPE' in content:
            doctype = content[content.find('<!DOCTYPE'):]
            doctype = doctype[0:doctype.find('>')+1]
            
            dtd = doctype[0:doctype.rfind('"')]
            dtd = dtd[dtd.rfind('"')+1:]
            

            new_doctype = doctype.replace(dtd, dtd_path)
            
            content = content.replace(doctype, new_doctype)
            
        if old != content:
            f = open(xml_filename, 'w')
            f.write(content)
            f.close()
            
        

def dtd(DTD_path):
    #if not DTD_path.endswith('.xsd') and not DTD_path.endswith('.dtd'):
    #    DTD_path = ''
    #if DTD_path != '':
    #    if not os.path.exists(DTD_path):
    #        DTD_path = ''
    return DTD_path
    

def validate(xml_filename, dtd_path, result_filename, err_filename):
    valid = False
    validation_type = ''
    temp_xml_filename = ''
    dtd_path = dtd(dtd_path)
    xml = xml_filename

    temp = xml_filename + '.validation.tmp'        
    if os.path.exists(temp):
        os.remove(temp)
    if os.path.exists(result_filename):
        os.remove(result_filename)
    if os.path.exists(err_filename):
        os.remove(err_filename)

    if dtd_path != '':
        import tempfile

        ign, temp_xml_filename = tempfile.mkstemp()
        shutil.copyfile(xml_filename, temp_xml_filename)
        replace_dtd_path(temp_xml_filename, dtd_path)
        xml = temp_xml_filename
        validation_type = '--validate'

    cmd = java + ' -cp ' +  jar_validate + ' br.bireme.XMLCheck.XMLCheck ' + xml + ' ' +  validation_type +  '>' + temp
    
    if os.path.exists(jar_validate):
        os.system(cmd)

    if os.path.exists(temp):
        f = open(temp, 'r')
        content = f.read().replace(xml, xml_filename)
        f.close()
        f = open(temp, 'w')
        f.write(content)
        f.close()

    else:
        content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd
        f = open(temp, 'w')
        f.write(content)
        f.close()

    shutil.copyfile(temp, result_filename)

    if 'ERROR' in content.upper():
        shutil.copyfile(temp, err_filename)
    else:
        valid = True
    os.unlink(temp)
    if temp_xml_filename != '':
        #print(open(temp_xml_filename).read()[0:500])
        os.unlink(temp_xml_filename)
    return valid


def transform(xml_filename, xsl_filename, result_filename, err_filename, parameters = {}):
    r = False
    temp_result = result_filename + '.tmp'

    if os.path.exists(temp_result):
       os.remove(temp_result)
    if os.path.exists(result_filename):
        os.remove(result_filename)
    if os.path.exists(err_filename):
        os.remove(err_filename)
   
    cmd = java + ' -jar ' +  jar_transform + ' -novw -w0 -o "' + temp_result + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)
            
    if os.path.exists(jar_transform ):
        #print(cmd)
        os.system(cmd)
    
    
    if os.path.exists(temp_result):
        r = True

    else:
        f = open(temp_result, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        f.close()
        
    if r == True:
        os.rename(temp_result, result_filename)
        #print(result_filename)
    else:
        os.rename(temp_result, err_filename)
        #print(err_filename)

        
    return r