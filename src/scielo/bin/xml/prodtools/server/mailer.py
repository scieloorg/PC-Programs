# coding=utf-8

from prodtools.utils import email_service


class Mailer(object):

    def __init__(self, config):
        self.config = config
        self.mailer = None
        if config.is_enabled_email_service:
            self.mailer = email_service.EmailService(config.email_sender_name, config.email_sender_email)

    def send_message(self, to, subject, text, attaches=[]):
        self.mailer.send_message(to, subject, text, attaches)

    def mail_invalid_packages(self, invalid_pkg_files):
        if self.config.is_enabled_email_service:
            self.send_message(self.config.email_to, self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n'.join(invalid_pkg_files))

    def mail_step1_failure(self, package_folder, e):
        if self.config.is_enabled_email_service:
            self.send_message(
                self.config.email_to_adm,
                '[Step 1]' + self.config.email_subject_invalid_packages,
                self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

    def mail_results(self, package_folder, results, report_location):
        if self.config.is_enabled_email_service:
            self.send_message(self.config.email_to, self.config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

    def mail_step2_failure(self, package_folder, e):
        if self.config.is_enabled_email_service:
            self.send_message(self.config.email_to_adm, '[Step 2]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))

    def mail_step3_failure(self, package_folder, e):
        if self.config.is_enabled_email_service:
            self.send_message(self.config.email_to_adm, '[Step 3]' + self.config.email_subject_invalid_packages, self.config.email_text_invalid_packages + '\n' + package_folder + '\n' + str(e))
