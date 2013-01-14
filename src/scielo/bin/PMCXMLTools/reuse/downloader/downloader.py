import os,  shutil
from datetime import datetime

class Downloader:
    def __init__(self, report, tracker, report_sender, template_message, download_path):
        self.tracker = tracker
        self.report = report
        self.download_path = download_path
        self.report_sender = report_sender
        self.template_message = template_message
        

    def download(self, ftp_service, ftp_folder, rename = False):
        
        existing = os.listdir(self.download_path)
        if len(existing)>0:
            self.report.write('Before downloading. Files in ' + self.download_path + '\n' + '\n'.join(existing), True, False, True)

        self.report.write('Downloading...', True, False, True)

        new_files = ftp_service.download_files(self.download_path, ftp_folder)

        all_files = os.listdir(self.download_path)
        #new_files = [ f for f in all_files if not f in existing ]

        if len(new_files)>0:
            self.report.write('Recently downloaded in ' + self.download_path  + '\n'  + '\n'.join(new_files), True, False, True)
        
          
            self.report.write('After downloading. Files in ' + self.download_path + '\n'  + '\n'.join(os.listdir(self.download_path)), True, False, True)
            content = self.report.read(self.report.summary_filename)
            self.report_sender.send_to_adm(self.template_message, content)
        
            
