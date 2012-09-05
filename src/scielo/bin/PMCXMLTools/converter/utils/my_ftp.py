from ftplib import FTP

class MyFTP:

    def __init__(self, server, user, pswd):
        self.server = server
        self.user = user
        self.pswd = pswd

        self.ftp = FTP(server)

    def download(self, dirname):
    	
        self.ftp.login(self.user, self.pswd)
        self.ftp.cwd(dirname)
        folders = self.ftp.nlst()
        for folder in folders:
        	self.ftp.cwd(folder)


