import os
import shutil

java_path = ''
jar_validate = ''
jar_transform = ''


def xml_validate(xml_filename, result_filename, dtd_validation=False):
    validation_type = ''

    if dtd_validation:
        validation_type = '--validate'

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)

    cmd = java_path + ' -cp ' + jar_validate + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' + validation_type + '>' + temp_result_filename

    os.system(cmd)

    if os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'r')
        result_content = f.read().replace(xml_filename, os.path.basename(xml_filename))
        f.close()

        if 'ERROR' in content.upper():
            f = open(xml_filename, 'r')

            n = 0
            s = ''
            for line in f.readlines():
                if n > 0:
                    s += str(n) + ':' + line + '\n'
                n += 1
            result_content += '\n' + s
    else:
        result_content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd

    if 'ERROR' in result_content.upper():
        f = open(temp_result_filename, 'w')
        f.write(result_content)
        f.close()
        valid = False
    else:
        valid = True

    shutil.move(temp_result_filename, result_filename)

    return valid


def xml_is_well_formed(xml_filename):
    import xml.etree.ElementTree as etree

    return (not etree.parse(xml_filename) is None)


def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if ' ' in v:
            r += k + '=' + '"' + v + '" '
        else:
            r += k + '=' + v + ' '
    return r


def xml_transform(xml_filename, xsl_filename, result_filename, parameters={}):
    error = False

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)

    cmd = java + ' -jar ' + jar_transform + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)

    os.system(cmd)

    if not s.path.exists(temp_result_filename):
        f = open(temp_result, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(cmd)
        error = True

    shutil.move(temp_result_filename, result_filename)

    return (not error)


def tranform_in_steps(xml_filename, xsl_list, result_filename, parameters={}):
    input_filename = xml_filename + '.in'
    output_filename = xml_filename + '.out'
    error = False

    shutil.copyfile(xml_filename, input_filename)
    if os.path.exists(result_filename):
        os.unlink(result_filename)

    for xsl in xsl_list:
        r = xml_transform(input_filename, xsl, output_filename, parameters)
        if r:
            shutil.copyfile(output_filename, input_filename)
        else:
            error = True
            break

    if os.path.exists(input_filename):
        os.unlink(input_filename)
    shutil.move(output_filename, result_filename)
    return not error


class StyleCheckerIO:

    _doctypes = {
        #'2.3': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v2.3 20070202//EN" "{DTD_PATH}journalpublishing.dtd">',
        #'3.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_PATH}journalpublishing3.dtd">',
        #'1.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_PATH}JATS-journalpublishing1.dtd">'
        '2.3': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v2.3 20070202//EN" "{DTD_FILENAME}">',
        '3.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">',
        '1.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'}

    def __init__(self, src_xml_filename, work_path, validation_report_filename, preview_filename, output_filename, image_path, new_name=''):
        self.src_xml_filename = src_xml_filename

        self.img_path = 'file:///' + img_path  if ':' in img_path else img_path
        self.new_name = new_name

        self.work_path = work_path

        self.output_path = os.path.dirname(output_filename)

        self.xml_path = os.path.dirname(self.src_xml_filename)
        self.basename = os.path.basename(self.src_xml_filename)
        self.filename = self.basename.replace('.xml', '')

        self.xml_filename = self.work_path + '/' + self.basename

        for p in [self.work_path, os.path.dirname(validation_report_filename), os.path.dirname(preview_filename), self.output_path]:
            if os.path.exists(p):
                for f in os.listdir(p):
                    os.unlink(p + '/' + f)
                    #if filename_matches(f, self.filename) and not self.basename == f:
                    #    os.unlink(p + '/' + f)
            else:
                os.makedirs(p)

        f = open(self.src_xml_filename, 'r')
        xml_content = f.read()
        f.close()

        f = open(self.xml_filename, 'w')
        f.write(xml_content)
        f.close()

        self.ouput_filename = output_filename
        self.html_report = validation_report_filename
        self.html_preview = preview_filename

        self.xml_report = self.work_path + '/' + self.filename + '.rep.xml'
        self.result_filename = self.work_path + '/' + self.filename + '.val.txt'
        self.err_filename = self.work_path + '/' + self.filename + '.err.tmp'

        self.result_filenames = [self.result_filename, self.html_report, self.html_preview, self.ouput_filename]

    def _fix_dtd_location(self, content, dtd_filename):
        if not dtd_filename in content:
            if not '<?xml ' in content:
                content = '<?xml version="1.0" encoding="utf-8"?>\n' + content

            dtd_version = content[content.find(' dtd-version="')+len(' dtd-version="'):]
            dtd_version = dtd_version[0:dtd_version.find('"')]

            if '<!DOCTYPE' in content:
                doctype = content[content.find('<!DOCTYPE'):]
                doctype = content[0:doctype.find('>')+1]
                content = content.replace(doctype, '')

            if not '<!DOCTYPE' in content:
                content = content.replace('<article ', self._doctypes[dtd_version].replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')
        return content


class StyleChecker:
    def __init__(self, dtd_filename, xsl_output, xsl_prep_report, xsl_report, xsl_preview, css_filename):
        self.xsl_report = xsl_report
        self.xsl_prep_report = xsl_prep_report
        self.xsl_preview = xsl_preview
        self.xsl_output = xsl_output
        self.dtd_filename = dtd_filename
        self.css_filename = css_filename
        self._report = []

    def log(self, content):
        print(content)

    def report(self, content):
        print(content)
        self._report.append(content)

    
    def validate(self, style_checker_io):
        well_formed, valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)

        errors = []

        self.report('\nValidating:' + style_checker_io.xml_filename)

        if xml_is_well_formed(style_checker_io.xml_filename):
            well_formed = True

            # VALIDATION
            valid = xml_validate(style_checker_io.xml_filename, style_checker_io.result_filename, (self.dtd_filename != ''))
            if not valid:
                self.report('Validation errors. Read ' + style_checker_io.result_filename)

            # STYLE CHECKER REPORT
            if xml_transform(style_checker_io.xml_filename, self.xsl_prep_report, style_checker_io.xml_report):
                # Generate self.report.html
                #self.log('transform ' + style_checker_io.xml_report + ' ' + self.xsl_report + ' ' + style_checker_io.html_report)
                if xml_transform(style_checker_io.xml_report, self.xsl_report, style_checker_io.html_report):
                    os.unlink(style_checker_io.xml_report)
                    self.report('Validation report. Read ' + style_checker_io.html_report)
                    report_ok = True
                else:
                    self.report('Unable to create validation report: ' + style_checker_io.html_report)
            else:
                self.report('Unable to generate xml for report: ' + style_checker_io.xml_report)

            # PREVIEW
            if type(self.xsl_preview) == type([]):
                preview_ok = tranform_in_steps(style_checker_io.xml_filename, self.xsl_preview, style_checker_io.html_preview, {'path_img': style_checker_io.img_path + '/', 'css':  self.css_filename, 'new_name': style_checker_io.new_name})
            else:
                #self.log('transform ' + style_checker_io.xml_filename + ' ' + self.xsl_preview + ' ' + style_checker_io.html_preview)
                preview_ok = xml_transform(style_checker_io.xml_filename, self.xsl_preview, style_checker_io.html_preview, {'path_img': style_checker_io.img_path + '/', 'css':  self.css_filename, 'new_name': style_checker_io.new_name})

            if preview_ok:
                self.report('Preview ' + style_checker_io.html_preview)
            else:
                self.report('Unable to create preview: ' + style_checker_io.html_preview)

            # OUTPUT
            if xml_transform(self.xml_filename, self.xsl_output, style_checker_io.ouput_filename):
                self.report('Result ' + style_checker_io.ouput_filename)
                output_ok = True
            else:
                self.report('Unable to create result: ' + style_checker_io.ouput_filename)
        else:
            # not well formed
            self.report('Not well formed.')

        for f in style_checker_io.result_filenames:
            if os.path.exists(f):
                print('Check ' + f)

        return (well_formed, valid, report_ok, preview_ok, output_ok)

    def validate_xml_and_style(self, report):
        is_valid_xml = False
        
        import time

        xml_java.replace_dtd_path(self.xml_filename, self.dtd)        
        if xml_java.validate(self.xml_filename, self.dtd, self.result_filename):  
            is_valid_xml = True    

            #self.log('Transform ' + self.xml_filename + ' + ' + self.xsl_prep_report +  ' => ' + style_checker_io.xml_report + ' ' + self.err_filename)        
            t = time.time()
            #self.log(str(os.path.exists(self.xml_filename)))        
            #self.log(str(os.path.exists(self.xsl_prep_report))   )     
            
            if xml_transform(self.xml_filename, self.xsl_prep_report, style_checker_io.xml_report):
                t1 = time.time()
                #self.log(str(t1 - t))
                #self.log('Transform ' + style_checker_io.xml_report + ' + ' + self.xsl_report +  ' => ' + style_checker_io.html_report + ' ' + self.err_filename)        
                
                #self.log(str(os.path.exists(self.xml_report)))        
                #self.log(str(os.path.exists(self.xsl_report)))        
                if xml_transform(self.xml_report, self.xsl_report, style_checker_io.html_report):
                    t2 = time.time()
                    #self.log(str(t2 - t1))
                else:
                    t2 = time.time()
                    #self.log('Unable to generate ' + style_checker_io.html_report )
                    #self.log(str(t2 - t1))
            else:
                t1 = time.time()
                #self.log('Unable to generate ' + self.xml_report)
                #self.log(str(t1 - t))
        
        if os.path.isfile(self.result_filename):
            os.unlink(self.result_filename)

        c = ''
        if os.path.exists(style_checker_io.html_report):
            f = open(style_checker_io.html_report, 'r')
            c = f.read()
            f.close()
            

        return (is_valid_xml, ('Total of errors = 0' in c))