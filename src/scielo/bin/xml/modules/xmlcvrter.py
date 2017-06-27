# coding=utf-8

import os
import shutil
from datetime import datetime

from __init__ import _
import validation_status
import fs_utils
import utils
import html_reports
import dbm_isis
import xc_models
import article_validations
import article_reports
import pkg_validations
import serial_files
import xml_utils
import xpmaker
import xc
import xc_config


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None

ALTERNATIVE_WEB_PATH = os.path.dirname(os.path.dirname(CURRENT_PATH)) + '/web'


categories_messages = {
    'converted': _('converted'), 
    'rejected': _('rejected'), 
    'not converted': _('not converted'), 
    'skipped': _('skipped conversion'), 
    'excluded ex-aop': _('excluded ex-aop'), 
    'excluded incorrect order': _('excluded incorrect order'), 
    'not excluded incorrect order': _('not excluded incorrect order'), 
    'not excluded ex-aop': _('not excluded ex-aop'), 
    'new aop': _('aop version'), 
    'regular doc': _('doc has no aop'), 
    'ex aop': _('aop is published in an issue'), 
    'matched aop': _('doc has aop version'), 
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'), 
    'aop missing PID': _('doc has aop version which has no PID'), 
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'), 
}

CONVERSIONS_STATUS = ['converted', 'not converted', 'rejected', 'skipped', 'excluded incorrect order', 'not excluded incorrect order']

EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = ['', _('IGNORED')]
EMAIL_SUBJECT_STATUS_ICON['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
EMAIL_SUBJECT_STATUS_ICON['approved'] = [u"\u2705", _(' APPROVED ')]
EMAIL_SUBJECT_STATUS_ICON['not processed'] = ['', _(' NOT PROCESSED ')]


class ConverterEnv(object):

    def __init__(self):
        self.version = None
        self.local_web_app_path = None
        self.serial_path = None
        self.is_windows = None
        self.db_manager = None


class ArticlesConversion(object):

    def __init__(self, articles_set_validations, db, create_windows_base=False):
        self.articles_set_validations = articles_set_validations
        self.db = db
        self.create_windows_base = create_windows_base
        self.report_path = None
        self.results_path = None
        self.articles_merger = self.articles_set_validations.articles_merger
        self.conversion_status = {'rejected': self.articles_set_validations.pkg.pkg_articles.keys()}
        self.aop_status = {}
        self.articles_conversion_validations = pkg_validations.ValidationsResultItems()
        self.error_messages = []
        self.files_final_location = serial_files.FilesFinalLocation(self.articles_set_validations.pkg.pkg_path, self.articles_set_validations.articles_data.acron, self.articles_set_validations.articles_data.issue_label, None, converter_env.local_web_app_path, converter_env.web_app_site)
        self.statistics_display = ''

    def convert(self):
        scilista_items = [self.articles_set_validations.articles_data.acron_issue_label]
        if self.articles_set_validations.blocking_errors == 0 and self.total_to_convert > 0:
            self.conversion_status = {}
            self.error_messages = self.db.exclude_articles(self.articles_merger.order_changes, self.articles_merger.excluded_orders)

            _scilista_items = self.db.convert_articles(self.articles_set_validations.articles_data.acron_issue_label, self.articles_merger.xc_articles, self.articles_set_validations.articles_data.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = pkg_validations.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                self.files_final_location.serial_path = self.articles_set_validations.articles_data.serial_path

                self.db.issue_files.copy_files_to_local_web_app(self.articles_set_validations.pkg.pkg_path, converter_env.local_web_app_path)
                self.db.issue_files.save_source_files(self.articles_set_validations.pkg.pkg_path)
                self.replace_ex_aop_pdf_files()

            self.aop_status.update(self.db.db_aop_status)
        self.generate_report()
        return scilista_items

    def replace_ex_aop_pdf_files(self):
        print(self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = converter_env.local_web_app_path + '/bases/pdf/' + folder
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)
            issue_pdf_path = converter_env.local_web_app_path + '/bases/pdf/' + self.articles_set_validations.articles_data.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                print((issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf))
                shutil.copyfile(issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf)

    def xxreplace_ex_aop_pdf_files(self):
        print(self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            print(aop_location_data)
            folder, aop_name = aop_location_data

            aop_pdf_path = converter_env.local_web_app_path + '/bases/pdf/' + folder
            issue_pdf_path = converter_env.local_web_app_path + '/bases/pdf/' + self.articles_set_validations.articles_data.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]
            aop_pdf_files = [f for f in os.listdir(aop_pdf_path) if f.startswith(aop_name) or f[2:].startswith('_'+aop_name)]
            for aop_pdf in aop_pdf_files:
                article_pdf = aop_pdf.replace(aop_name, xml_name)
                print((issue_pdf_path + '/' + article_pdf, aop_pdf_path + '/' + aop_pdf))
                if not os.path.isdir(aop_pdf_path):
                    os.makedirs(aop_pdf_path)
                shutil.copyfile(issue_pdf_path + '/' + article_pdf, aop_pdf_path + '/' + aop_pdf)


    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20',  _('achieved results'): '20'}

        #print(self.articles_merger.history_items)
        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    article = self.articles_merger.xc_articles[name]
                    self.articles_merger.history_items[name].append((status, article))
        for status, names in self.conversion_status.items():
            for name in names:
                self.articles_merger.history_items[name].append((status, self.articles_merger.xc_articles[name]))

        history = sorted([(hist[0][1].order, xml_name) for xml_name, hist in self.articles_merger.history_items.items()])
        history = [(xml_name, self.articles_merger.history_items[xml_name]) for order, xml_name in history]

        items = []
        for xml_name, hist in history:
            values = []
            registered = [item for item in hist if item[0] == 'registered article']
            package = [item for item in hist if item[0] == 'package']
            diff = ''
            if len(registered) == 1 and len(package) == 1:
                diff = pkg_validations.display_articles_differences(registered[0][1], package[0][1], _('registered'), _('package')) + '<hr/>'
            values.append(article_reports.display_article_data_in_toc(hist[-1][1]))
            values.append(article_reports.article_history(registered))
            values.append(diff + article_reports.article_history(package))
            values.append(article_reports.article_history([item for item in hist if not item[0] in ['registered article', 'package', 'rejected', 'converted', 'not converted']]))
            values.append(article_reports.article_history([item for item in hist if item[0] in ['rejected', 'converted', 'not converted']]))

            items.append(pkg_validations.label_values(labels, values))

        return html_reports.tag('h3', _('Conversion steps')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')], widths=widths)

    @property
    def registered_articles(self):
        if self.db is not None:
            return self.db.registered_articles

    @property
    def acron_issue_label(self):
        return self.articles_set_validations.articles_data.acron_issue_label

    def generate_report(self, base_report_path=None):
        report_filename = 'xc-{}.html'.format(datetime.now().isoformat()[0:19].replace(':', '').replace('T', '_'))
        reports = pkg_validations.ReportsMaker([], self.articles_set_validations, self.files_final_location, None, self)
        if converter_env.is_windows:
            reports.processing_result_location = self.files_final_location.result_path
        self.report_location = self.files_final_location.report_path + '/' + report_filename
        reports.save_report(self.files_final_location.report_path, report_filename, _('XML Conversion (XML to Database)'))
        self.statistics_display = reports.validations.statistics_display(html_format=False)
        if converter_env.is_windows:
            html_reports.display_report(self.report_location)

    @property
    def total_to_convert(self):
        return self.articles_merger.total_to_convert

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.articles_set_validations.blocking_errors > 0:
            result = 'rejected'
        elif self.total_to_convert == 0:
            result = 'ignored'
        elif self.articles_conversion_validations.blocking_errors > 0:
            result = 'rejected'
        elif self.articles_conversion_validations.fatal_errors > 0:
            result = 'accepted'
        else:
            result = 'approved'
        return result

    @property
    def conversion_status_report(self):
        return report_status(_('Conversion results'), self.conversion_status, 'conversion')

    @property
    def aop_status_report(self):
        if len(self.aop_status) == 0:
            return _('this journal has no aop. ')
        r = ''
        for status in sorted(self.aop_status.keys()):
            if status != 'aop':
                r += self.aop_report(status, self.aop_status[status])
        r += self.aop_report('aop', self.aop_status.get('aop'))
        return r

    def aop_report(self, status, status_items):
        if status_items is None:
            return ''
        r = ''
        if len(status_items) > 0:
            labels = []
            widths = {}
            if status == 'aop':
                labels = [_('issue')]
                widths = {_('issue'): '5'}
            labels.extend([_('filename'), 'order', _('article')])
            widths.update({_('filename'): '5', 'order': '2', _('article'): '88'})

            report_items = []
            for item in status_items:
                issueid = None
                article = None
                if status == 'aop':
                    issueid, name, article = item
                else:
                    name = item
                    article = self.articles_merger.merged_articles.get(name)
                if article is not None:
                    if not article.is_ex_aop:
                        values = []
                        if issueid is not None:
                            values.append(issueid)
                        values.append(name)
                        values.append(article.order)
                        values.append(article.title)
                        report_items.append(pkg_validations.label_values(labels, values))
            r = html_reports.tag('h3', _(status)) + html_reports.sheet(labels, report_items, table_style='reports-sheet', html_cell_content=[_('article')], widths=widths)
        return r

    @property
    def conclusion_message(self):
        text = ''.join(self.error_messages)
        app_site = converter_env.web_app_site if converter_env.web_app_site is not None else _('scielo web site')
        status = ''
        result = _('updated/published on {app_site}').format(app_site=app_site)
        reason = ''
        update = True
        if self.xc_status == 'rejected':
            update = False
            status = validation_status.STATUS_BLOCKING_ERROR
            if self.total_to_convert > 0:
                if self.total_not_converted > 0:
                    reason = _('because it is not complete ({value} were not converted). ').format(value=str(self.total_not_converted) + '/' + str(self.total_to_convert))
                else:
                    reason = _('because there are blocking errors in the package. ')
            else:
                reason = _('because there are blocking errors in the package. ')
        elif self.xc_status == 'ignored':
            update = False
            reason = _('because no document has changed. ')
        elif self.xc_status == 'accepted':
            status = validation_status.STATUS_WARNING
            reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services. ')
        elif self.xc_status == 'approved':
            status = validation_status.STATUS_OK
            reason = ''
        else:
            status = validation_status.STATUS_FATAL_ERROR
            reason = _('because there are blocking errors in the package. ')
        action = _('will not be')
        if update:
            action = _('will be')
        text = u'{status}: {issueid} {action} {result} {reason}'.format(status=status, issueid=self.acron_issue_label, result=result, reason=reason, action=action)
        text = html_reports.p_message(_('converted') + ': ' + str(self.total_converted) + '/' + str(self.total_to_convert), False) + html_reports.p_message(text, False)
        return text


def convert_package(src_path):
    xc_process_logger = fs_utils.ProcessLogger()

    scilista_items = []
    is_xml_generation = False

    pkg_name = os.path.basename(src_path)[:-4]

    if not os.path.isdir('./../log'):
        os.makedirs('./../log')
    log_package = './../log/' + datetime.now().isoformat().replace(':', '_') + os.path.basename(pkg_name)

    fs_utils.append_file(log_package, 'preparing')
    tmp_result_path = src_path + '_xc'

    fs_utils.append_file(log_package, 'normalized_package')
    xml_files = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    pkg_maker = xpmaker.PackageMaker(xml_files, tmp_result_path, 'acron', converter_env.version, is_db_generation=True)
    pkg_maker.make_sps_package()

    #, converter_env.is_windows
    doi_services = article_validations.DOI_Services()

    articles_pkg = pkg_validations.ArticlesPackage(pkg_maker.scielo_pkg_path, pkg_maker.article_items, is_xml_generation)

    articles_data = pkg_validations.ArticlesData()
    articles_data.setup(articles_pkg, db_manager=converter_env.db_manager)

    articles_set_validations = pkg_validations.ArticlesSetValidations(articles_pkg, articles_data, xc_process_logger)
    articles_set_validations.validate(doi_services, pkg_maker.scielo_dtd_files, pkg_maker.article_work_area_items)

    conversion = ArticlesConversion(articles_set_validations, articles_data.articles_db_manager, not converter_env.is_windows)
    scilista_items = conversion.convert()

    #reports.validations.statistics_display()
    #conversion.statistics_display
    #report_location
    #conversion.report_location

    if tmp_result_path != conversion.results_path:
        fs_utils.delete_file_or_folder(tmp_result_path)
    os.unlink(log_package)
    return (scilista_items, conversion.xc_status, conversion.statistics_display, conversion.report_location)


def format_reports_for_web(report_path, pkg_path, issue_path):
    if not os.path.isdir(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path):
        os.makedirs(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path)

    #utils.debugging('format_reports_for_web')
    #utils.debugging('content of ' + report_path)
    #utils.debugging('\n'.join(os.listdir(report_path)))

    for f in os.listdir(report_path):
        if f.endswith('.zip') or f == 'xml_converter.txt':
            os.unlink(report_path + '/' + f)
        else:
            #utils.debugging(report_path + '/' + f)
            content = fs_utils.read_file(report_path + '/' + f)
            content = content.replace('file:///' + pkg_path, '/img/revistas/' + issue_path)
            content = content.replace('file:///' + report_path, '/reports/' + issue_path)
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            fs_utils.write_file(converter_env.local_web_app_path + '/htdocs/reports/' + issue_path + '/' + f, content)


def report_status(title, status, style=None):
    text = ''
    if status is not None:
        for category in sorted(status.keys()):
            _style = style
            if status.get(category) is None:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            elif len(status[category]) == 0:
                ltype = 'ul'
                list_items = ['None']
                _style = None
            else:
                ltype = 'ol'
                list_items = status[category]
            text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)
    if len(text) > 0:
        text = html_reports.tag('h3', title) + text
    return text


def transfer_website_files(acron, issue_id, local_web_app_path, user, servers, remote_web_app_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        for server in servers:
            xc.run_remote_mkdirs(user, server, dest_path)
            xc.run_rsync(source_path, user, server, dest_path)


def transfer_report_files(acron, issue_id, local_web_app_path, user, servers, remote_web_app_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/reports/']
    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        log_filename = './transfer_report_' + issue_id_path.replace('/', '-') + '.log'
        for server in servers:
            xc.run_remote_mkdirs(user, server, dest_path, log_filename)
            xc.run_rsync(source_path, user, server, dest_path, log_filename)


def queue_packages(download_path, temp_path, queue_path, archive_path):
    invalid_pkg_files = []
    proc_id = datetime.now().isoformat()[11:16].replace(':', '')
    temp_path = temp_path + '/' + proc_id
    queue_path = queue_path + '/' + proc_id
    pkg_paths = []

    if os.path.isdir(temp_path):
        fs_utils.delete_file_or_folder(temp_path)
    if os.path.isdir(queue_path):
        fs_utils.delete_file_or_folder(queue_path)

    if archive_path is not None:
        if not os.path.isdir(archive_path):
            os.makedirs(archive_path)

    if not os.path.isdir(temp_path):
        os.makedirs(temp_path)

    for pkg_name in os.listdir(download_path):
        if is_valid_pkg_file(download_path + '/' + pkg_name):
            shutil.copyfile(download_path + '/' + pkg_name, temp_path + '/' + pkg_name)
        else:
            pkg_paths.append(pkg_name)
        fs_utils.delete_file_or_folder(download_path + '/' + pkg_name)

    for pkg_name in os.listdir(temp_path):
        queued_pkg_path = queue_path + '/' + pkg_name
        if not os.path.isdir(queued_pkg_path):
            os.makedirs(queued_pkg_path)

        if fs_utils.extract_package(temp_path + '/' + pkg_name, queued_pkg_path):
            if archive_path is not None:
                if os.path.isdir(archive_path):
                    shutil.copyfile(temp_path + '/' + pkg_name, archive_path + '/' + pkg_name)
            pkg_paths.append(queued_pkg_path)
        else:
            invalid_pkg_files.append(pkg_name)
            fs_utils.delete_file_or_folder(queued_pkg_path)
        fs_utils.delete_file_or_folder(temp_path + '/' + pkg_name)
    fs_utils.delete_file_or_folder(temp_path)

    return (pkg_paths, invalid_pkg_files)


def xml_converter_read_configuration(filename):
    r = None
    if os.path.isfile(filename):
        r = xc_config.XMLConverterConfiguration(filename)
        if not r.valid:
            r = None
    return r


def xml_converter_get_inputs(args):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    package_path = None
    script = None
    collection_acron = None
    if len(args) == 2:
        script, param = args
        if os.path.isfile(param) or os.path.isdir(param):
            package_path = param
        else:
            collection_acron = param

    return (script, package_path, collection_acron)


def xml_converter_validate_inputs(package_path, collection_acron):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    errors = []
    if package_path is None:
        if collection_acron is None:
            errors.append(_('Missing collection acronym'))
    else:
        errors = xml_utils.is_valid_xml_path(package_path)
    return errors


def xml_config_filename(collection_acron):
    filename = CURRENT_PATH + '/../../scielo_paths.ini'

    if not os.path.isfile(filename):
        if not collection_acron is None:
            filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'
    return filename


def is_valid_configuration_file(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append(validation_status.STATUS_ERROR + ': ' + _('No configuration file was informed'))
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append(validation_status.STATUS_ERROR + ': ' + _('unable to read XML Converter configuration file: ') + configuration_filename)
    return messages


def is_valid_pkg_file(filename):
    return os.path.isfile(filename) and (filename.endswith('.zip') or filename.endswith('.tgz'))


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = xml_converter_get_inputs(args)
    if package_path is None and collection_acron is None:
        # GUI
        import xml_gui
        xml_gui.open_main_window(True, None)

    elif package_path is not None and collection_acron is not None:
        errors = xml_converter_validate_inputs(package_path, collection_acron)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
            messages.append(validation_status.STATUS_ERROR + ': ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python xml_converter.py <xml_folder> | <collection_acron>')
            messages.append(_('where') + ':')
            messages.append('  <xml_folder> = ' + _('path of folder which contains'))
            messages.append('  <collection_acron> = ' + _('collection acron'))
            messages.append('\n'.join(errors))
            utils.display_message('\n'.join(messages))
        else:
            execute_converter(package_path, collection_acron)
    elif collection_acron is not None:
        execute_converter(package_path, collection_acron)
    elif package_path is not None:
        execute_converter(package_path)


def send_message(mailer, to, subject, text, attaches=None):
    if mailer is not None:
        #utils.debugging('sending message ' + subject)
        mailer.send_message(to, subject, text, attaches)


def execute_converter(package_paths, collection_name=None):
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    if collection_acron is None:
        collection_acron = collection_name

    config = xc.get_configuration(collection_acron)
    if config is not None:
        prepare_env(config)
        invalid_pkg_files = []

        mailer = xc.get_mailer(config)

        if package_paths is None:
            package_paths, invalid_pkg_files = queue_packages(config.download_path, config.temp_path, config.queue_path, config.archive_path)
        if package_paths is None:
            package_paths = []
        if not isinstance(package_paths, list):
            package_paths = [package_paths]

        for package_path in package_paths:
            package_folder = os.path.basename(package_path)
            utils.display_message(package_path)
            scilista_items = []
            xc_status = 'interrupted'
            stats_msg = ''
            report_location = None

            try:
                scilista_items, xc_status, stats_msg, report_location = convert_package(package_path)
            except Exception as e:
                if config.queue_path is not None:
                    fs_utils.delete_file_or_folder(package_path)
                if config.email_subject_invalid_packages is not None:
                    send_message(mailer, config.email_to_adm, '[Step 1]' + config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))
                if len(package_paths) == 1:
                    raise
            print(scilista_items)
            try:
                acron, issue_id = scilista_items[0].split(' ')

                if xc_status in ['accepted', 'approved']:
                    if config.collection_scilista is not None:
                        open(config.collection_scilista, 'a+').write('\n'.join(scilista_items) + '\n')

                    if config.is_enabled_transference:
                        transfer_website_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_servers, config.remote_web_app_path)

                if report_location is not None:
                    if config.email_subject_package_evaluation is not None:
                        results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                        link = config.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                        report_location = '<html><body>' + html_reports.link(link, link) + '</body></html>'

                        transfer_report_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_servers, config.remote_web_app_path)
                        send_message(mailer, config.email_to, config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

            except Exception as e:
                if config.email_subject_invalid_packages is not None:
                    send_message(mailer, config.email_to_adm, '[Step 2]' + config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

                if len(package_paths) == 1:
                    print('exception as finishing')
                    raise

        if len(invalid_pkg_files) > 0:
            if config.email_subject_invalid_packages is not None:
                send_message(mailer, config.email_to, config.email_subject_invalid_packages, config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))

    utils.display_message(_('finished'))


def prepare_env(config):
    global converter_env

    if converter_env is None:
        converter_env = ConverterEnv()

    db_isis = dbm_isis.IsisDAO(dbm_isis.UCISIS(dbm_isis.CISIS(config.cisis1030), dbm_isis.CISIS(config.cisis1660)))
    converter_env.db_manager = xc_models.DBManager(db_isis, [config.title_db, config.title_db_copy, CURRENT_PATH + '/title.fst'], [config.issue_db, config.issue_db_copy, CURRENT_PATH + '/issue.fst'], config.serial_path)
    if config.local_web_app_path is None:
        config.local_web_app_path = ALTERNATIVE_WEB_PATH

    converter_env.local_web_app_path = config.local_web_app_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    converter_env.web_app_site = config.web_app_site
    converter_env.skip_identical_xml = config.skip_identical_xml
    converter_env.max_fatal_error = config.max_fatal_error
    converter_env.max_error = config.max_error
    converter_env.max_warning = config.max_warning
