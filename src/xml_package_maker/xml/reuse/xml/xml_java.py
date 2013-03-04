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
    

def validate(xml_filename, dtd_path, validation_result_file, err_filename):
    valid = False
    validation_type = ''
    bkp = ''
    dtd_path = dtd(dtd_path)
    

    
    if os.path.exists(validation_result_file):
        os.unlink(validation_result_file)
    if os.path.exists(err_filename):
        os.unlink(err_filename)

    if dtd_path != '':
        import tempfile

        ign, bkp = tempfile.mkstemp()
        shutil.copyfile(xml_filename, bkp)

        replace_dtd_path(xml_filename, dtd_path)
        
        validation_type = '--validate'

    
    cmd = java + ' -cp ' +  jar_validate + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' +  validation_type +  '>' + validation_result_file
    
    if os.path.exists(jar_validate):
        os.system(cmd)
    else:
        print('wrong command: ' + cmd)
        #time.sleep(3)

    error = False
    if os.path.exists(validation_result_file):
        f = open(validation_result_file, 'r')
        content = f.read()
        f.close() 

        if 'ERROR' in content.upper():
            f = open(xml_filename, 'r')
            xml = f.read()
            f.close() 

            f = open(validation_result_file, 'w')
            if '<?xml ' in xml:
                xml = xml[xml.find('?>')+2:]
            n = 0
            a = []

            lines = xml.split('\n')
            xml = ''
            for line in lines:
                n += 1
                xml += str(n) + ':' + line + '\n'
                
            f.write(content + '\n' + xml)
            f.close() 
            error = True

    else:
        content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd
        f = open(validation_result_file, 'w')
        f.write(content)
        f.close()
        error = True

    if error:
        shutil.copyfile(validation_result_file, err_filename)
    
    
    if bkp != '':
        shutil.copyfile(bkp, xml_filename)
        try:
            os.unlink(bkp)
        except WindowsError:
            pass
    return not error


def transform(xml_filename, xsl_filename, result_filename, err_filename, parameters = {}):
    r = False
    temp_result = result_filename + '.tmp'

    if os.path.exists(temp_result):
       os.unlink(temp_result)
    if os.path.exists(result_filename):
        os.unlink(result_filename)
        
    if os.path.exists(err_filename):
        os.unlink(err_filename)
   
    cmd = java + ' -jar ' +  jar_transform + ' -novw -w0 -o "' + temp_result + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)
            
    if os.path.exists(jar_transform ):
        os.system(cmd)
        #time.sleep(3)
    
    
    if os.path.exists(temp_result):
        r = True
        #print(temp_result)
    else:
        f = open(temp_result, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        f.close()
        
    if r == True:
        shutil.copyfile(temp_result, result_filename)
        
    else:
        shutil.copyfile(temp_result, err_filename)
        

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
        