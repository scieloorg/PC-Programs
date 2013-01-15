# coding=utf-8
import smtplib, os

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
    if type(s) == type(''):
        if ';' in s:
            l = s.split(';')
        elif ',' in s:
            l = s.split(',')
        else:
            l = [s]
    elif type(s) == type([]):
        l = s
    return l

class EmailMessageTemplate:
    def __init__(self, subject, message_template_filename):
        self.subject = subject
        self.message_template = ''
        if len(message_template_filename)>0 and os.path.isfile(message_template_filename):
            fn = open(message_template_filename, 'r')
            self.message_template = fn.read()
            fn.close()
        
    def msg(self, parameters={}):
        message = self.message_template
        for key, value in parameters.items():
            message = message.replace(key, value)
        return message

    def msg_from_files(self, param_files):
        msg = ''
        for f in param_files:
            fn = open(f, 'r')
            content = fn.read()
            fn.close()
            msg += content + '\n'  + '='*80 + '\n'
        return msg

class EmailService:
    def __init__(self, label_from, mail_from, server="localhost", is_available_email_service = True):
        self.mail_from = mail_from
        self.server = server
        self.label_from = label_from
        self.is_available_email_service = is_available_email_service

    def send(self, to, cc, bcc, subject, text, attaches=[]):
        to = strtolist(to)
        attaches = strtolist(attaches)
        bcc = strtolist(bcc)
        cc = strtolist(cc)

        assert type(to)==type([])
        assert type(attaches)==type([])
        assert type(bcc)==type([])
        assert type(cc)==type([])
        
        if len(to) == 0:
            if len(cc) > 0:
                to = cc 
                cc = [] 
            else:
                to = bcc
                bcc = [] 

        if len(to) > 0:

            msg = MIMEMultipart()
            msg['From'] = self.mail_from
            msg['To'] = ', '.join(to)
            msg['Subject'] = Header(subject, 'utf-8')
            msg['BCC'] = ', '.join(bcc)
            msg.attach( MIMEText(text, 'plain', 'utf-8') )

            for f in attaches:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(f,"rb").read() )
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)

            smtp = smtplib.SMTP(self.server)
            smtp.sendmail(self.label_from + '<' + self.mail_from + '>', to, msg.as_string())
            smtp.close()

if __name__ == '__main__':
    s = EmailService('Nome do remetente',  'sender@email.com')
    to = ['dest@email.com']
    s.send(to, 'teste', 'isso eh um teste', [])
