# coding=utf-8
import os
import smtplib

##mail_from email.Utils import COMMASPACE, formatdate
from email import encoders
#from email.message import Message
#from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def strtolist(s):
    l = []
    if s is not None:
        if not isinstance(s, list):
            if ';' in s:
                l = s.split(';')
            elif ',' in s:
                l = s.split(',')
            else:
                l = [s]
    return l


class EmailMessageTemplate(object):

    def __init__(self, subject, message_template_filename):
        self.subject = subject
        self.message_template = ''
        if len(message_template_filename) > 0 and os.path.isfile(message_template_filename):
            self.message_template = open(message_template_filename, 'r').read()
            if not isinstance(self.message_template, unicode):
                self.message_template = self.message_template.decode('utf-8')

    def msg(self, parameters={}):
        message = self.message_template
        for key, value in parameters.items():
            message = message.replace(key, value)
        return message

    def msg_from_files(self, param_files):
        msg = ''
        for f in param_files:
            content = open(f, 'r').read()
            if not isinstance(content, unicode):
                content = content.decode('utf-8')
            msg += content + '\n' + '='*80 + '\n'
        return msg


class EmailService(object):

    def __init__(self, label_from, mail_from, server="localhost"):
        self.mail_from = mail_from
        self.server = server
        self.label_from = label_from

    def send_message(self, to, subject, text, attaches=[], cc=[], bcc=[]):
        to = strtolist(to)
        attaches = strtolist(attaches)
        bcc = strtolist(bcc)
        cc = strtolist(cc)

        if len(to) > 0:
            msg = MIMEMultipart()
            msg['From'] = self.mail_from
            msg['To'] = ', '.join(to)
            msg['Subject'] = Header(subject, 'utf-8')
            msg['BCC'] = ', '.join(bcc)
            plain_or_html = 'html' if text.lower().startswith('<html') else 'plain'

            msg.attach(MIMEText(text, plain_or_html, 'utf-8'))

            for f in attaches:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(f, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)

            smtp = smtplib.SMTP(self.server)
            try:
                smtp.sendmail(self.label_from + '<' + self.mail_from + '>', to, msg.as_string())
            except Exception as e:

                try:

                    msg = MIMEMultipart()
                    msg['From'] = self.mail_from
                    msg['To'] = ', '.join(to)
                    msg['Subject'] = Header(subject, 'utf-8')
                    msg['BCC'] = ', '.join(bcc)
                    msg.attach(MIMEText(text, plain_or_html, 'utf-8'))
                    smtp.sendmail(self.label_from + '<' + self.mail_from + '>', to, msg.as_string())

                except Exception as e:
                    print(e)
            #except Exception as inst:
            #    msg = MIMEMultipart()
            #    msg['From'] = self.mail_from
            #    msg['To'] = ', '.join(to)
            #    msg['Subject'] = Header(subject, 'utf-8')
            #    msg['BCC'] = ', '.join(bcc)
            #    msg.attach( MIMEText('Problem in mail service ' +  subject, 'plain', 'utf-8') )
            #    smtp.sendmail(self.label_from + '<' + self.mail_from + '>', to, msg.as_string())
            smtp.close()


#if __name__ == '__main__':
#    s = EmailService('Nome do remetente',  'sender@email.com')
#    to = ['dest@email.com']
#    s.send(to, 'teste', 'isso eh um teste', [])
