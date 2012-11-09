

class Downloader:
    def __init__(self, report):
        
        self.report = report

    def download(self, ftp_service, ftp_folder, download_path):
        self.report.write('Before downloading. Files in ' + download_path, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)
        self.report.write('Downloading...', True, False, True)

        ftp_service.download_files(download_path, ftp_folder)

        self.report.write('After downloading. Files in ' + download_path, True, False, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)

    def extract_files(self, compressed_file_manager, download_path, extracted_path, backup_path, report_sender):   
        for compressed in os.listdir(download_path):
            self.report.write('Extract files from ' + download_path + ' to ' + extracted_path+ '/' + compressed, True, False, True)


            compressed_file_manager.extract_files(download_path + '/' + compressed, extracted_path + '/' + compressed)

            self.report.write('Do backup ' + backup_path, True, False, True)
            compressed_file_manager.backup(download_path + '/' + compressed, backup_path)
            attached_files = []

            text =  'Files in the package\n' + '\n'.join(os.listdir(extracted_path + '/' + compressed))


            report_sender.send_report( compressed, text, attached_files)

