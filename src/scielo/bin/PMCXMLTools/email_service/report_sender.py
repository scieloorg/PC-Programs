class ReportSender:
    def __init__(self, report, email_service, email_data):
        self.report = report
        self.email_service = email_service
        self.email_data = email_data

    def send_report(self,  compressed_filename, msg_text, attached_files):        
        xml_provider_email = self.email_data['EMAIL_PROVIDER']
        text = ''
        to = ''
        if self.email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] == 'yes':
            to = xml_provider_email.split(',')
            text = ''
            bcc = self.email_data['BCC_EMAIL']
        

        if len(to) == '':
            to = self.email_data['BCC_EMAIL']
            if len(xml_provider_email) > 0:
                foward_to = xml_provider_email
            else:
                foward_to = '(e-mail ausente no pacote)'
            text += self.email_data['ALERT_FORWARD'] + ' ' +  foward_to + '\n'  + '-' * 80 + '\n\n'
            bcc = []

        if len(self.email_data['EMAIL_TEXT']) > 0:
            if os.path.isfile(self.email_data['EMAIL_TEXT']):
                f = open(self.email_data['EMAIL_TEXT'], 'r')
                text += f.read()
                f.close()

                text = text.replace('REPLACE_PACKAGE', compressed_filename)

        if len(msg_text)>0:
            text += msg_text + '\n'
        if len(attached_files) > 0:
            if self.email_data['FLAG_ATTACH_REPORTS'] == 'yes':
                text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'em anexo')

            else:
                text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'abaixo')
            
                for item in attached_files:
                    f = open(item, 'r')
                    text += '-'* 80 + '\n'+ f.read() + '-'* 80 + '\n' 
                    f.close()
                attached_files = []

        self.report.write('Email data:' + compressed_filename)
        self.report.write('to:' + ','.join(to))
        self.report.write('bcc:' + ','.join(bcc))
        self.report.write('files:' + ','.join(attached_files))
        self.report.write('text:' + text)

        if self.email_data['IS_AVAILABLE_EMAIL_SERVICE'] == 'yes':
            self.email_service.send(to, [], self.email_data['BCC_EMAIL'], self.email_data['EMAIL_SUBJECT_PREFIX'] + compressed_filename, text, attached_files)

