# coding=utf-8
import smtplib, os

##from email.Utils import COMMASPACE, formatdate
from email import encoders
#from email.message import Message
#from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, send_from, server="localhost"):
        self.send_from = send_from
        self.server = server

    def send(self, send_to, cc, bcc, subject, text, files=[]):
        assert type(send_to)==list
        assert type(files)==list
        assert type(bcc)==list
        assert type(cc)==list
        
        if len(send_to) == 0:
            if len(cc) > 0:
                send_to = cc 
                cc = [] 
            else:
                send_to = bcc
                bcc = [] 

        if len(send_to) > 0:

            msg = MIMEMultipart()
            msg['From'] = self.send_from
            msg['To'] = ', '.join(send_to)
            msg['Subject'] = subject
            msg['BCC'] = ', '.join(bcc)
            msg.attach( MIMEText(text) )

            for f in files:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(f,"rb").read() )
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
                msg.attach(part)

            smtp = smtplib.SMTP(self.server)
            smtp.sendmail(send_from, send_to, msg.as_string())
            smtp.close()

if __name__ == '__main__':
    s = EmailSender('sender@email.com')
    send_to = ['dest@email.com']
    s.send(send_to, 'teste', 'isso eh um teste', [])
