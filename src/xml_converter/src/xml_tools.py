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

        if 'ERROR' in result_content.upper():
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

    cmd = java_path + ' -jar ' + jar_transform + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)

    os.system(cmd)

    if not os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'w')
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



class ValidationsParameters:

    def __init__(self, src_xml_filename, work_path, dtd_validation_report, style_checker_report, html_preview, img_path, new_name=''):
        self.src_xml_filename = src_xml_filename
        self.work_path = work_path
        self.dtd_validation_report = dtd_validation_report
        self.html_report = style_checker_report
        self.html_preview = html_preview

        self.img_path = 'file:///' + img_path if ':' in img_path else img_path
        self.new_name = new_name

        basename = os.path.basename(self.src_xml_filename)
        filename = self.basename.replace('.xml', '')

        self.work_path += '/' + filename
        self.xml_filename = self.work_path + '/' + basename

        if os.path.exists(self.work_path):
            for f in os.listdir(self.work_path):
                os.unlink(self.work_path + '/' + f)
        else:
            os.makedirs(self.work_path)
        shutil.copyfile(self.src_xml_filename, self.xml_filename)

        self.result_filenames = [dtd_validation_report, style_checker_report, html_preview]
        for f in self.result_filenames:
            if os.path.exists(f):
                os.unlink(f)


class XMLFixer:
    _doctypes = {
        #'2.3': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v2.3 20070202//EN" "{DTD_PATH}journalpublishing.dtd">',
        #'3.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_PATH}journalpublishing3.dtd">',
        #'1.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_PATH}JATS-journalpublishing1.dtd">'
        '2.3': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v2.3 20070202//EN" "{DTD_FILENAME}">',
        '3.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">',
        '1.0': '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'}

    def __init__(self, dtd_version, xml_filename):
        self.xml_filename = xml_filename
        f = open(xml_filename, 'r')
        self.content = f.read()
        f.close()
        self.dtd_version = dtd_version

    def _fix_dtd_location(self, dtd_filename):
        if not dtd_filename in self.content:
            if not '<?xml ' in self.content:
                self.content = '<?xml version="1.0" encoding="utf-8"?>\n' + self.content

            if ' dtd-version="' in self.content:
                dtd_version = self.content[self.content.find(' dtd-version="')+len(' dtd-version="'):]
                dtd_version = dtd_version[0:dtd_version.find('"')]
            else:
                dtd_version = self.dtd_version

            if '<!DOCTYPE' in self.content:
                doctype = self.content[self.content.find('<!DOCTYPE'):]
                doctype = self.content[0:doctype.find('>')+1]
                self.content = self.content.replace(doctype, '')

            if not '<!DOCTYPE' in self.content:
                self.content = self.content.replace('<article ', self._doctypes[dtd_version].replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')

    def _fix_entities(self):
        pass

    def _fix_tags(self):
        pass


class XMLValidations:
    def __init__(self, dtd_filename, xsl_prep_report, xsl_report, xsl_preview, css_filename):
        self.xsl_report = xsl_report
        self.xsl_prep_report = xsl_prep_report
        self.xsl_preview = xsl_preview
        self.dtd_filename = dtd_filename
        self.css_filename = css_filename
        self._report = []

    def log(self, content):
        print(content)

    def report(self, content):
        print(content)
        self._report.append(content)

    def _style_checker_report(self, xml_filename, html_report):
        # STYLE CHECKER REPORT
        report_ok = False
        xml_report = html_report.replace('.html', '.xml')
        if xml_transform(xml_filename, self.xsl_prep_report, xml_report):
            # Generate self.report.html
            #self.log('transform ' + xml_report + ' ' + self.xsl_report + ' ' + html_report)
            if xml_transform(xml_report, self.xsl_report, html_report):
                os.unlink(xml_report)

                f = open(html_report, 'r')
                c = f.read()
                f.close()

                report_ok = ('Total of errors = 0' in c)

                if report_ok:
                    self.report('Validation report. No errors found. Read ' + html_report)
                else:
                    self.report('Validation report. Some errors were found. Read ' + html_report)
            else:
                self.report('Unable to create validation report: ' + html_report)
        else:
            self.report('Unable to generate xml for report: ' + xml_report)
        return report_ok

    def _preview(self, xml_filename, html_preview, img_path, new_name=''):
        preview_ok = False
        if type(self.xsl_preview) == type([]):
            preview_ok = tranform_in_steps(xml_filename, self.xsl_preview, html_preview, {'path_img': img_path + '/', 'css':  self.css_filename, 'new_name': new_name})
        else:
            #self.log('transform ' + xml_filename + ' ' + self.xsl_preview + ' ' + html_preview)
            preview_ok = xml_transform(xml_filename, self.xsl_preview, html_preview, {'path_img': img_path + '/', 'css':  self.css_filename, 'new_name': new_name})

        if preview_ok:
            self.report('Preview ' + html_preview)
        else:
            self.report('Unable to create preview: ' + html_preview)
        return preview_ok

    def check_list(self, data):
        self.xsl_report = []
        well_formed, is_dtd_valid, report_ok, preview_ok = (False, False, False, False)

        errors = []

        self.report('\nValidating:' + data.xml_filename)

        if xml_is_well_formed(data.xml_filename):
            well_formed = True

            # VALIDATION
            is_dtd_valid = xml_validate(data.xml_filename, data.dtd_validation_report, (self.dtd_filename != ''))
            if not is_dtd_valid:
                self.report('Validation errors. Read ' + data.dtd_validation_report)

            # STYLE CHECKER REPORT
            report_ok = self._style_checker_report(data.xml_filename, data.html_report)

            # PREVIEW
            preview_ok = self._preview(data.xml_filename, data.html_preview)

        else:
            # not well formed
            self.report('Not well formed.')

        for f in data.result_filenames:
            if os.path.exists(f):
                print('Check ' + f)

        return (well_formed, is_dtd_valid, report_ok, preview_ok)

