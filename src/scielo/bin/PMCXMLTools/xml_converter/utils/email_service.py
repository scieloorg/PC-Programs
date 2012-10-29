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

class EmailService:
    def __init__(self, label_from, mail_from, server="localhost"):
        self.mail_from = mail_from
        self.server = server
        self.label_from = label_from
        

    def send(self, to, cc, bcc, subject, text, files=[]):
        assert type(to)==list
        assert type(files)==list
        assert type(bcc)==list
        assert type(cc)==list
        
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

            for f in files:
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
