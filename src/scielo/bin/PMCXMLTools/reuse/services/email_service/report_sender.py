class MessageType:
    def __init__(self, subject, message_header_filename, flag_send_to_package_provider, forward_alert, flag_attach_reports):
        self.flag_send_to_package_provider = flag_send_to_package_provider
        self.message_header_filename = message_header_filename
        self.forward_alert = forward_alert
        self.subject = subject
        self.flag_attach_reports = flag_attach_reports
    
    def message_header(self):
        fn = open(self.message_header_filename, 'r')
        content = fn.read()
        fn.close()
        return '\n' + content + '\n'


class ReportSender:
    def __init__(self, report, is_available_email_service, email_service, bcc, message_type):
        self.report = report
        self.is_available_email_service = is_available_email_service
        self.email_service = email_service
        self.bcc = bcc        
        self.message_type = message_type
        
    def configure_destinatary(self, xml_provider_email):
        to = []
        bcc = []
        forward_to = ''
        if self.message_type.flag_send_to_package_provider == 'yes':
            if xml_provider_email == '':
                to = self.bcc
            else:
                to = xml_provider_email
                bcc = self.bcc
        else:
            to = self.bcc
            if len(xml_provider_email) > 0:
                forward_to = xml_provider_email
            else:
                forward_to = 'the XML provider'
            bcc = [] 
        return (to, bcc, forward_to)

    
    def report_files_content(self, param_files):
        msg = ''
        for f in param_files:
            fn = open(f, 'r')
            content = fn.read()
            fn.close()
            msg += content + '\n'  + '='*80 + '\n'

        return msg

    
    def send_report(self,  package_name, package_sender_email, msg, report_files, attached_files):   
        #compressed, '', text, [], attached_files     
        to, bcc, forward_to = self.configure_destinatary(package_sender_email)
        text = self.message_type.forward_alert + '\n' + '='*80 + '\n'
        text += self.message_type.message_header()
        text += msg 
        text = text.replace('REPLACE_PACKAGE', package_name)

        
        if self.message_type.flag_attach_reports == 'yes':
            attached_files += report_files 
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'em anexo')
        else:
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'abaixo')
            text += self.report_files_content(report_files) 

   
        self.report.write('Email data:' + package_name)
        self.report.write('to:' + ','.join(to))
        self.report.write('bcc:' + ','.join(bcc))

        self.report.write('reports:' + ','.join(report_files))
        self.report.write('files:' + ','.join(attached_files))
        self.report.write('text:' + text)

        if self.is_available_email_service == 'yes':
            self.email_service.send(to, [], bcc, self.message_type.subject + package_name, text, attached_files)

