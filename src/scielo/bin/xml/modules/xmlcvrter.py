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
import pkg_validations
import xml_utils
import xml_versions
import xpmaker
import xc
import xc_config


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

CONFIG_PATH = CURRENT_PATH + '/../config/'
converter_env = None


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


def normalized_package(src_path, report_path, wrk_path, pkg_path, version):
    xml_filenames = sorted([src_path + '/' + f for f in os.listdir(src_path) if f.endswith('.xml') and not 'incorrect' in f])
    articles, doc_file_info_items = xpmaker.make_package(xml_filenames, report_path, wrk_path, pkg_path, version, 'acron', is_db_generation=True)
    return (articles, doc_file_info_items)


class ArticlesConversion(object):

    def __init__(self, articles_set_validations, db, create_windows_base=False):
        self.articles_set_validations = articles_set_validations
        self.db = db
        self.create_windows_base = create_windows_base
        self.final_report_path = None
        self.final_result_path = None
        self.articles_merger = self.articles_set_validations.articles_merger
        self.conversion_status = {'rejected': self.articles_set_validations.pkg.pkg_articles.keys()}
        self.aop_status = {}
        self.articles_conversion_validations = pkg_validations.ValidationsResultItems()
        self.error_messages = []

    def convert(self):
        scilista_items = []
        self.acron_issue_label = 'not registered'

        self.conversion_status = {'rejected': self.articles_set_validations.pkg.pkg_articles.keys()}
        self.aop_status = {}

        self.registered_articles = self.db.registered_articles
        if self.articles_set_validations.blocking_errors == 0 and self.articles_merger.total_to_convert > 0:
            self.conversion_status = {}
            #FIXME
            self.error_messages = self.db.exclude_order_id_filenames(self.articles_merger.order_changes, self.articles_merger.excluded_orders)

            scilista_items = self.db.convert_articles(self.articles_set_validations.articles_data.acron_issue_label, self.articles_merger.xc_articles, self.articles_set_validations.articles_data.issue_models.record, self.create_windows_base)

            self.conversion_status.update(self.db.db_conversion_status)
            self.aop_status.update(self.db.db_aop_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = pkg_validations.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(scilista_items) > 0:
                self.db.issue_files.copy_files_to_local_web_app()
                self.db.issue_files.save_source_files(self.articles_set_validations.pkg.pkg_path)
                self.registered_articles = self.db.registered_articles
                self.acron_issue_label = self.articles_set_validations.articles_data.acron_issue_label

                self.final_report_path = self.articles_set_validations.articles_data.issue_files.base_reports_path
                self.final_result_path = self.articles_set_validations.articles_data.issue_files.issue_path
        return scilista_items

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
        elif self.articles_merger.total_to_convert == 0:
            result = 'ignored'
        elif self.articles_set_validations.fatal_errors > 0:
            result = 'accepted'
        else:
            result = 'approved'
        return result

    @property
    def conversion_status_report(self):
        return report_status(_('Conversion results'), self.conversion_status, 'conversion')

    @property
    def aop_status_report(self):
        r = report_status(_('AOP status'), self.aop_status, 'aop-block')
        if len(r) == 0:
            r = _('this journal has no aop.')
        return r

    @property
    def conclusion_message(self):
        text = ''.join(self.error_messages)
        app_site = converter_env.web_app_site if converter_env.web_app_site is not None else _('scielo web site')
        status = ''
        result = _('be updated/published on {app_site}').format(app_site=app_site)
        reason = ''
        update = True
        if self.xc_status == 'rejected':
            update = False
            status = validation_status.STATUS_BLOCKING_ERROR
            if self.articles_merger.total_to_convert > 0:
                if self.total_not_converted > 0:
                    reason = _('because it is not complete ({value} were not converted).').format(value=str(self.total_not_converted) + '/' + str(self.articles_merger.total_to_convert))
                else:
                    reason = _('unknown')
            else:
                reason = _('because there are blocking errors in the package.')
        elif self.xc_status == 'ignored':
            update = False
            reason = _('because no document was changed.')
        elif self.xc_status == 'accepted':
            status = validation_status.STATUS_WARNING
            reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services.')
        elif self.xc_status == 'approved':
            status = validation_status.STATUS_OK
            reason = ''
        else:
            status = validation_status.STATUS_FATAL_ERROR
            reason = _('because there are blocking errors in the package.')
        action = ' not'
        if update:
            action = ''
        text = _('{status}: {issueid} will{action} {result} {reason}.').format(status=status, issueid=self.acron_issue_label, result=result, reason=reason, action=action)
        text = html_reports.tag('h2', _('Summary report')) + html_reports.p_message(_('converted') + ': ' + str(self.total_converted) + '/' + str(self.articles_merger.total_to_convert), False) + html_reports.p_message(text, False)
        return text


def package_paths_preparation(src_path):
    result_path = src_path + '_xml_converter_result'
    wrk_path = result_path + '/work'
    pkg_path = result_path + '/scielo_package'
    report_path = result_path + '/errors'

    for path in [result_path, wrk_path, pkg_path, report_path]:
        if not os.path.isdir(path):
            os.makedirs(path)
    return (report_path, wrk_path, pkg_path, result_path)


def convert_package(src_path):
    xc_process_logger = fs_utils.ProcessLogger()

    scilista_items = []
    is_xml_generation = False

    scielo_dtd_files = xml_versions.DTDFiles('scielo', converter_env.version)

    pkg_name = os.path.basename(src_path)[:-4]

    if not os.path.isdir('./../log'):
        os.makedirs('./../log')
    log_package = './../log/' + datetime.now().isoformat().replace(':', '_') + os.path.basename(pkg_name)

    fs_utils.append_file(log_package, 'preparing')
    tmp_report_path, wrk_path, scielo_pkg_path, tmp_result_path = package_paths_preparation(src_path)
    final_result_path = tmp_result_path
    final_report_path = tmp_report_path

    fs_utils.append_file(log_package, 'normalized_package')
    articles, articles_work_area = normalized_package(src_path, tmp_report_path, wrk_path, scielo_pkg_path, converter_env.version)

    #, converter_env.is_windows
    doi_services = article_validations.DOI_Services()

    articles_pkg = pkg_validations.ArticlesPackage(scielo_pkg_path, articles, is_xml_generation)

    articles_data = pkg_validations.ArticlesData()
    articles_data.setup(articles_pkg, xc_models.JournalsManager(), db_manager=converter_env.db_manager)

    articles_set_validations = pkg_validations.ArticlesSetValidations(articles_pkg, articles_data, xc_process_logger)
    articles_set_validations.validate(doi_services, scielo_dtd_files, articles_work_area)

    conversion = ArticlesConversion(articles_set_validations, articles_data.articles_db_manager, not converter_env.is_windows)
    conversion.final_result_path = final_result_path
    conversion.final_report_path = final_report_path
    scilista_items = conversion.convert()

    reports = pkg_validations.ReportsMaker(articles_set_validations, None, conversion, display_report=converter_env.is_windows)

    reports.processing_result_location = conversion.final_result_path
    report_location = conversion.final_report_path + '/xml_converter.html'
    reports.save_report(conversion.final_report_path, 'xml_converter.html', _('XML Conversion (XML to Database)'))

    if not converter_env.is_windows:
        format_reports_for_web(conversion.final_report_path, scielo_pkg_path, conversion.acron_issue_label.replace(' ', '/'))
    if tmp_result_path != final_result_path:
        fs_utils.delete_file_or_folder(tmp_result_path)
    os.unlink(log_package)
    return (scilista_items, conversion.xc_status, reports.validations.statistics_display(), report_location)


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

            try:
                if len(scilista_items) == 0:
                    scilista_items.append('not registered')
                acron, issue_id = scilista_items[0].split(' ')

                if xc_status in ['accepted', 'approved']:
                    if config.collection_scilista is not None:
                        open(config.collection_scilista, 'a+').write('\n'.join(scilista_items) + '\n')

                    if config.is_enabled_transference:
                        transfer_website_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_servers, config.remote_web_app_path)

                if report_location is not None:
                    if config.is_windows:
                        pkg_validations.display_report(report_location)

                    if config.email_subject_package_evaluation is not None:
                        results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                        link = converter_env.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
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
    converter_env.db_manager = xc_models.DBManager(db_isis, [config.title_db, config.title_db_copy, CURRENT_PATH + '/title.fst'], [config.issue_db, config.issue_db_copy, CURRENT_PATH + '/issue.fst'], config.serial_path, config.local_web_app_path)

    converter_env.local_web_app_path = config.local_web_app_path
    converter_env.version = '1.0'
    converter_env.is_windows = config.is_windows
    converter_env.web_app_site = config.web_app_site
    converter_env.skip_identical_xml = config.skip_identical_xml
    converter_env.max_fatal_error = config.max_fatal_error
    converter_env.max_error = config.max_error
    converter_env.max_warning = config.max_warning
