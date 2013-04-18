import os, shutil

java_path = ''
jar_transform = ''
jar_validate = ''

def wait_file_creation(filename, MAX_SPENT_TIME = 300):
    import time
    start = time.time()

    wait = True
    while wait:
        if os.path.exists(filename):
            wait = False
        else:
            spent_time = time.time() - start
            if spent_time > MAX_SPENT_TIME:
                wait = False

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
    f = open(xml_filename, 'r')
    content = f.read()
    f.close()

    if not dtd_path in content:

        old = content
        if not '<!DOCTYPE' in content:
            #print('none')
            start = content[1:]
            start = start[start.find('<')+1:]
            start = start[0:start.find('>')]
            
            if ' ' in start:
                start = start[0:start.find(' ')]
            #print('start:' + start)
            #content = content.replace('<' + start, '<!DOCTYPE ' + start + ' PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "journalpublishing3.dtd">' + '\n' + '<' + start) 
            content = content[0:content.find('<' + start)] + '<!DOCTYPE ' + start + ' PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "journalpublishing3.dtd">\n' + content[content.find('<' + start):] 

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
        os.unlink(temp)
    if os.path.exists(result_filename):
        os.unlink(result_filename)
    if os.path.exists(err_filename):
        os.unlink(err_filename)

    if dtd_path != '':
        import tempfile

        ign, temp_xml_filename = tempfile.mkstemp()
        shutil.copyfile(xml_filename, temp_xml_filename)
        replace_dtd_path(temp_xml_filename, dtd_path)
        xml = temp_xml_filename
        validation_type = '--validate'

    cmd = java_path + ' -cp ' +  jar_validate + ' br.bireme.XMLCheck.XMLCheck ' + xml + ' ' +  validation_type +  '>' + temp
    
    if os.path.exists(jar_validate):
        teste = os.system(cmd)



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

    if 'ERROR' in content.upper():
        shutil.move(temp, err_filename)
    else:
        valid = True
        os.unlink(temp)
    
    if temp_xml_filename != '':
        try:
            os.unlink(temp_xml_filename)
        except WindowsError:
            pass
        
    return valid


def transform(xml_filename, xsl_filename, result_filename, err_filename, parameters = {}):
    r = False
    temp_result = result_filename + '.tmp'

    if os.path.exists(temp_result):
       os.unlink(temp_result)
    if os.path.exists(result_filename):
        os.unlink(result_filename)
        
    if os.path.exists(err_filename):
        os.unlink(err_filename)
   
    cmd = java_path + ' -jar ' +  jar_transform + ' -novw -w0 -o "' + temp_result + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)
    
    
    if os.path.exists(jar_transform ):
        #print(cmd)
        teste = os.system(cmd)

    if not os.path.exists(temp_result):
        wait_file_creation(temp_result)


    if os.path.exists(temp_result):
        r = True

    else:
        f = open(temp_result, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        f.close()
        
    if r == True:
        shutil.copyfile(temp_result, result_filename)
        #print(result_filename)
    else:
        shutil.copyfile(temp_result, err_filename)
        #print(err_filename)

    os.unlink(temp_result)
    return r



def tranform_in_steps(xml, dtd, xsl_list, result, parameters={}):
    err = xml + '.err'
    inputfile = xml + '.in'

    shutil.copyfile(xml, inputfile)
    if os.path.exists(result):
        os.unlink(result)

    for xsl in xsl_list:
        replace_dtd_path(inputfile, dtd)
        transform(inputfile, xsl, result, err, parameters)
        
        if os.path.exists(err):
            break
        else:
            if os.path.exists(result):
                shutil.copyfile(result, inputfile)
                
    if os.path.exists(inputfile):
        os.unlink(inputfile) 
    if os.path.exists(err):
        shutil.copyfile(err, result)
        