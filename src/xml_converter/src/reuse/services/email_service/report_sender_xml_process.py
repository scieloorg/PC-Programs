
class ReportSenderConfiguration:
    def __init__(self, adm_email, flag_send_to_main_destinatary, alert_forward_msg, flag_attach_reports):
        self.adm_email = adm_email
        self.flag_send_to_main_destinatary = flag_send_to_main_destinatary
        self.alert_forward_msg = alert_forward_msg
        self.flag_attach_reports = flag_attach_reports

    def to(self, main_destinatary = ''):
        
        _to = main_destinatary
        bcc = self.adm_email
        forward_to = ''
        
        if (len(main_destinatary) == 0) or (self.flag_send_to_main_destinatary == False):
            _to = self.adm_email        

        if _to == self.adm_email:
            bcc = []
            if len(main_destinatary) > 0:
                forward_to = main_destinatary
            
        return (_to, bcc, forward_to)


class ReportSender:
    def __init__(self, email_service, config):
        self.email_service = email_service
        self.config = config 

    def log(self, to, cc, bcc, subject, msg, attached_files):
        report = [] 
        report.append('Email')
        report.append('subject:' + subject)
        report.append('to:' + ','.join(to))
        report.append('cc:' + ','.join(cc))
        report.append('bcc:' + ','.join(bcc))
        report.append('files:' + ','.join(attached_files))
        report.append('msg:' + msg)
        return '\n'.join(report)

    def package_eval_message_params(self, package_name, forward_to, report_location, report_content):
        parameters = {}
        parameters['REPLACE_PACKAGE'] = package_name
        parameters['REPLACE_REPORTS_CONTENTS'] = report_content
        parameters['REPLACE_FORWARD_TO'] = forward_to
        parameters['REPLACE_ATTACHED_OR_BELOW'] = report_location
        return parameters

    def adm_message_params(self, content):
        parameters = {}
        parameters['CONTENT'] = content        
        return parameters

    def send_to_adm(self, template, content):
        to = self.config.adm_email
        msg = template.msg(self.adm_message_params(content))
        if not content in msg:
            msg += content

        if self.email_service.is_available_email_service:
            self.email_service.send(to, [], [], template.subject, msg, [])
        return self.log(to, [], [], template.subject, msg, [])

    def send_package_evaluation_report(self, template, package_name, report_files, attaches = [], package_sender_email = ''):
        
        to, bcc, forward_to = self.config.to(package_sender_email)

        if forward_to != '':
            forward_to = self.config.alert_forward_msg +  '  ' + forward_to + '\n' + '-'*80 + '\n'

        if self.config.flag_attach_reports == 'yes':
            attached_files = report_files 
            report_location = 'em anexo' 
            report_content = ''
        else:
            attached_files = []
            report_location = 'abaixo'
            report_content = template.msg_from_files(report_files)

        msg = template.msg(self.package_eval_message_params(package_name, forward_to, report_location, report_content))
        
        attached_files += attaches

        if self.email_service.is_available_email_service:
            self.email_service.send(to, [], bcc, template.subject + ' ' + package_name, msg, attached_files)
        return self.log(to, [], bcc, template.subject + ' ' + package_name, msg, attached_files)
     
