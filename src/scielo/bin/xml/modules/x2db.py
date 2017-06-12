# coding=utf-8

import os
import shutil
from datetime import datetime

from __init__ import _
from . import validation_status
from . import fs_utils
from . import utils
from . import html_reports
from . import dbm_isis
from . import xc_models
from . import article_reports
from validations import package_validations
from . import xml_utils
from . import xc
from . import xc_config
from pkgmakers import pkgmaker


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


def call_converter(args, version='1.0'):
    script, package_path, collection_acron = read_inputs(args)
    if package_path is None and collection_acron is None:
        # FIXME
        # GUI
        import xml_gui
        xml_gui.open_main_window(True, None)

    elif package_path is not None and collection_acron is not None:
        errors = validate_inputs(package_path, collection_acron)
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


def read_inputs(args):
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


def validate_inputs(package_path, collection_acron):
    # python xml_converter.py <xml_src>
    # python xml_converter.py <collection_acron>
    errors = []
    if package_path is None:
        if collection_acron is None:
            errors.append(_('Missing collection acronym'))
    else:
        errors = xml_utils.is_valid_xml_path(package_path)
    return errors


def get_config(collection_name):
    collection_names = {}
    collection_acron = collection_names.get(collection_name)
    if collection_acron is None:
        collection_acron = collection_name
    #FIXME
    return xc.get_configuration(collection_acron)


def organize_packages_locations(pkg_path, config, mailer):
    if pkg_path is None:
        pkg_path, invalid_pkg_files = queue_packages(config.download_path, config.temp_path, config.queue_path, config.archive_path)
    if pkg_path is None:
        pkg_path = []
    if not isinstance(pkg_path, list):
        pkg_path = [pkg_path]
    if len(invalid_pkg_files) > 0:
        mailer.mail_invalid_packages(invalid_pkg_files)


def execute_converter(package_paths, collection_name):

    config = get_config(collection_name)
    mailer = Mailer(config)
    transfer = FilesTransfer(config)
    organize_packages_locations(package_paths, config, mailer)

    xc = XC(config, version, DISPLAY_REPORT, GENERATE_PMC, stage)

    for package_path in package_paths:

        pkgfolder = workarea.PackageFolder(os.path.dirname(xml_list[0]))
        pkgfiles = package.normalize_xml_packages(pkgfolder.xml_list, 'xc')

        xc.convert([f.filename for f in pkgfiles])

        package_name = os.path.basename(package_path)
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
                mailer.mail_step1_failure(package_name, e)
            if len(package_paths) == 1:
                raise
        print(scilista_items)
        try:
            acron, issue_id = scilista_items[0].split(' ')

            if xc_status in ['accepted', 'approved']:
                if config.collection_scilista is not None:
                    open(config.collection_scilista, 'a+').write('\n'.join(scilista_items) + '\n')

                if config.is_enabled_transference:
                    transfer.transfer_website_files(acron, issue_id)

            if report_location is not None:
                if config.email_subject_package_evaluation is not None:
                    results = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + stats_msg
                    link = config.web_app_site + '/reports/' + acron + '/' + issue_id + '/' + os.path.basename(report_location)
                    report_location = '<html><body>' + html_reports.link(link, link) + '</body></html>'

                    transfer.transfer_report_files(acron, issue_id)
                    mailer.mail_results(package_name, results, report_location)

        except Exception as e:
            if config.email_subject_invalid_packages is not None:
                mailer.mail_step2_failure(package_folder, e)

            if len(package_paths) == 1:
                print('exception as finishing')
                raise

    ###
    if tmp_result_path != conversion.results_path:
        fs_utils.delete_file_or_folder(tmp_result_path)
    os.unlink(log_package)
    ###

    utils.display_message(_('finished'))


class XC(pkgmaker.XPM):

    def __init__(self, config, version, DISPLAY_REPORT, GENERATE_PMC, stage='xpm'):
        pkgmakers.XPM.__init__(self, config, version, DISPLAY_REPORT, GENERATE_PMC, stage)
        db_isis = dbm_isis.IsisDAO(
                    dbm_isis.UCISIS(
                        dbm_isis.CISIS(config.cisis1030),
                        dbm_isis.CISIS(config.cisis1660)))
        self.db_manager = xc_models.DBManager(db_isis, [config.title_db, config.title_db_copy, CURRENT_PATH + '/title.fst'], [config.issue_db, config.issue_db_copy, CURRENT_PATH + '/issue.fst'], config.serial_path)
        if self.config.local_web_app_path is None:
            self.config.local_web_app_path = ALTERNATIVE_WEB_PATH
        self.mailer = None
        if config.is_enabled_email_service:
            self.mailer = email_service.EmailService(config.email_sender_name, config.email_sender_email)

    def convert(self, input_xml_list):
        pkg = self.package(input_xml_list)
        registered_issue_data = registered.RegisteredIssueData(self.db_manager)
        registered_issue_data.get_data(pkg.pkgissuedata)
        pkg_validations = self.validate_package(pkg, registered_issue_data)

        conversion = ArticlesConversion(registered_issue_data, pkg, not self.config.interative_mode, not self.config.local_web_app_path, not self.config.web_app_site)

        statistics_display = self.report(pkg, pkg_validations, conversion)
        utils.display_message(_('Result of the processing:'))
        utils.display_message(pkg.wk.output_path)
        scilista_items = conversion.convert()

        return (scilista_items, conversion.xc_status, statistics_display, conversion.report_location)


class Mailer(object):

    def __init__(self, config):
        self.config = config
        self.mailer = email_service.EmailService(config.email_sender_name, config.email_sender_email)

    def send_message(self, to, subject, text, attaches):
        if self.mailer is not None:
            self.mailer.send_message(to, subject, text, attaches)

    def mail_invalid_packages(self, invalid_pkg_files):
        self.send_message(self.config.email_to, self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))

    def mail_step1_failure(self, package_folder, e):
        self.send_message(self.config.email_to_adm, '[Step 1]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

    def mail_results(self, package_folder, results, report_location):
        self.send_message(self.config.email_to, self.config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

    def mail_step2_failure(self, package_folder, e):
        self.send_message(self.config.email_to_adm, '[Step 2]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))


class FilesTransfer(object):

    def __init__(self, config):
        self.config = config

    def transfer_website_files(self, acron, issue_id):
        #, config.local_web_app_path, config.transference_user, config.transference_servers, config.remote_web_app_path
        # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
        issue_id_path = acron + '/' + issue_id

        folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

        for folder in folders:
            dest_path = self.config.remote_web_app_path + folder + issue_id_path
            source_path = self.config.local_web_app_path + folder + issue_id_path
            for server in self.config.transference_servers:
                xc.run_remote_mkdirs(self.config.user, server, dest_path)
                xc.run_rsync(source_path, self.config.user, server, dest_path)

    def transfer_report_files(self, acron, issue_id):
        # 'rsync -CrvK img/* self.config.user@server:/var/www/...../revistas'
        issue_id_path = acron + '/' + issue_id

        folders = ['/htdocs/reports/']
        for folder in folders:
            dest_path = self.config.remote_web_app_path + folder + issue_id_path
            source_path = self.config.local_web_app_path + folder + issue_id_path
            log_filename = './transfer_report_' + issue_id_path.replace('/', '-') + '.log'
            for server in self.config.transference_servers:
                xc.run_remote_mkdirs(self.config.user, server, dest_path, log_filename)
                xc.run_rsync(source_path, self.config.user, server, dest_path, log_filename)


class ArticlesConversion(object):

    def __init__(self, registered_issue_data, pkg, create_windows_base, web_app_path, web_app_site):
        self.create_windows_base = create_windows_base
        self.registered_issue_data = registered_issue_data
        self.db = self.registered_issue_data.articles_db_manager
        self.local_web_app_path = web_app_path
        self.pkg = pkg
        self.merging_result = self.articles_validations_reports.merged_articles_reports.merging_result
        self.merged_articles = self.articles_validations_reports.merged_articles_reports.merged_articles_data.merged_articles

    def convert(self):
        self.articles_conversion_validations = {}
        scilista_items = [self.pkg.pkgissuedata.acron_issue_label]
        if self.articles_validations_reports.blocking_errors == 0 and self.total_to_convert > 0:
            self.conversion_status = {}
            self.error_messages = self.db.exclude_articles(self.merging_result.order_changes, self.merging_result.excluded_orders)

            _scilista_items = self.db.convert_articles(self.pkg.pkgissuedata.acron_issue_label, self.merging_result.articles_to_convert, self.registered_issue_data.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = package_validations.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                self.db.issue_files.copy_files_to_local_web_app(self.pkg.package_folder.path, self.local_web_app_path)
                self.db.issue_files.save_source_files(self.pkg.package_folder.path)
                self.replace_ex_aop_pdf_files()

            self.aop_status.update(self.db.db_aop_status)
        return scilista_items

    def replace_ex_aop_pdf_files(self):
        # FIXME
        print(self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = self.local_web_app_path + '/bases/pdf/' + folder
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)
            issue_pdf_path = self.local_web_app_path + '/bases/pdf/' + self.pkg.pkgissuedata.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                print((issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf))
                shutil.copyfile(issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf)

    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20',  _('achieved results'): '20'}

        #print(self.merging_result.history_items)
        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    article = self.merging_result.articles_to_convert[name]
                    self.merging_result.history_items[name].append((status, article))
        for status, names in self.conversion_status.items():
            for name in names:
                self.merging_result.history_items[name].append((status, self.merging_result.articles_to_convert[name]))

        history = sorted([(hist[0][1].order, xml_name) for xml_name, hist in self.merging_result.history_items.items()])
        history = [(xml_name, self.merging_result.history_items[xml_name]) for order, xml_name in history]

        items = []
        for xml_name, hist in history:
            values = []
            values.append(article_reports.display_article_data_in_toc(hist[-1][1]))
            values.append(article_reports.article_history([item for item in hist if item[0] == 'registered article']))
            values.append(article_reports.article_history([item for item in hist if item[0] == 'package']))
            values.append(article_reports.article_history([item for item in hist if not item[0] in ['registered article', 'package', 'rejected', 'converted', 'not converted']]))
            values.append(article_reports.article_history([item for item in hist if item[0] in ['rejected', 'converted', 'not converted']]))

            items.append(html_reports.label_values(labels, values))
        return html_reports.tag('h3', _('Conversion steps')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('achieved results')], widths=widths)

    @property
    def registered_articles(self):
        if self.db is not None:
            return self.db.registered_articles

    @property
    def acron_issue_label(self):
        return self.pkg.pkgissuedata.acron_issue_label

    @property
    def total_to_convert(self):
        return self.merging_result.total_to_convert

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.articles_validations_reports.blocking_errors > 0:
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
                        report_items.append(html_reports.label_values(labels, values))
            r = html_reports.tag('h3', _(status)) + html_reports.sheet(labels, report_items, table_style='reports-sheet', html_cell_content=[_('article')], widths=widths)
        return r

    @property
    def conclusion_message(self):
        text = ''.join(self.error_messages)
        app_site = self.web_app_site if self.web_app_site is not None else _('scielo web site')
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


def send_message(mailer, to, subject, text, attaches=None):
    if mailer is not None:
        #utils.debugging('sending message ' + subject)
        mailer.send_message(to, subject, text, attaches)

