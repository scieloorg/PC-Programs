import os,  shutil
from datetime import datetime

class Downloader:
    def __init__(self, report, tracker, report_sender, download_path):
        self.tracker = tracker
        self.report = report
        self.download_path = download_path
        self.report_sender = report_sender
        

    def download(self, ftp_service, ftp_folder, rename = False):
        self.report.write('Before downloading. Files in ' + self.download_path, True)
        for f in os.listdir(self.download_path):
            self.report.write(f, True, False, True)
        self.report.write('Downloading...', True, False, True)

        ftp_service.download_files(self.download_path, ftp_folder)

        self.report.write('After downloading. Files in ' + self.download_path, True, False, True)
        for f in os.listdir(self.download_path):
            self.report.write(f, True, False, True)
            if rename:
                dot_position = f.rfind('.')
                ext = f[dot_position:]
                
                now = datetime.now().isoformat().replace(':', '')
                filename = self.download_path + '/' + f[0:dot_position] + '.' + now + ext
                os.rename(self.download_path + '/' + f, filename)
            else:
                filename = self.download_path + '/' + f
            
        self.report_sender.send_report('', '', '\n'.join(os.listdir(self.download_path)), [], [] )
