

class Reception:
    def __init__(self, config, report):
        self.config = config 
        self.report = report

    def download(self, my_ftp, subdir_in_ftp_server, download_path):
        self.report.write('Before downloading. Files in ' + download_path, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)
        self.report.write('Downloading...', True, False, True)

        my_ftp.download_files(download_path, subdir_in_ftp_server)

        self.report.write('After downloading. Files in ' + download_path, True, False, True)
        for f in os.listdir(download_path):
            self.report.write(f, True, False, True)

    def put_files_in_queue(self, download_path, queue_path):   
        uploaded_files_manager = UploadedFilesManager(self.report, download_path)
        uploaded_files_manager.transfer_files(queue_path)

        self.report.write('Downloaded files in ' + queue_path, True, False, True)
        for f in os.listdir(queue_path):
            self.report.write(f, True, False, True)
    
        self.report.write('Read '+ self.report.summary_filename, True, False, True)
        

    def open_packages(self, loader, email_service, email_data, package_path, work_path, report_path):
        for filename in os.listdir(package_path):
            package_file = package_path + '/' + filename

            package = Package(package_file, work_path, report_path)
            package.open_package()
            package.read_package_sender_email()

            # processa
            loader.load(package)

            self.send_report(email_service, email_data, package)

        
    def send_report(self, email_service, email_data, package):        
        emails = package.package_sender_email
        

        if email_data['FLAG_SEND_EMAIL_TO_XML_PROVIDER'] == 'yes':
            to = emails.split(',')
            text = ''
            bcc = email_data['BCC_EMAIL']
        else:

            to = email_data['BCC_EMAIL']
            if len(emails) > 0:
                foward_to = emails
            else:
                foward_to = '(e-mail ausente no pacote)'
            text = email_data['ALERT_FORWARD'] + ' ' +  foward_to + '\n'  + '-' * 80 + '\n\n'
            bcc = []

        if len(email_data['EMAIL_TEXT']) > 0:
            if os.path.isfile(email_data['EMAIL_TEXT']):
                f = open(email_data['EMAIL_TEXT'], 'r')
                text += f.read()
                f.close()

                text = text.replace('REPLACE_PACKAGE', package.package_name)

        attached_files = package.report_files_to_send
        if email_data['FLAG_ATTACH_REPORTS'] == 'yes':
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'em anexo')

        else:
            text = text.replace('REPLACE_ATTACHED_OR_BELOW', 'abaixo')
            
            for item in attached_files:
                f = open(item, 'r')
                text += '-'* 80 + '\n'+ f.read() + '-'* 80 + '\n' 
                f.close()
            attached_files = []

        self.report.write('Email data:' + package.package_name)
        self.report.write('to:' + ','.join(to))
        self.report.write('bcc:' + ','.join(bcc))
        self.report.write('files:' + ','.join(attached_files))
        self.report.write('text:' + text)

        if email_data['IS_AVAILABLE_EMAIL_SERVICE'] == 'yes':
            email_service.send(to, [], email_data['BCC_EMAIL'], email_data['EMAIL_SUBJECT_PREFIX'] + package.package_name, text, attached_files)

    


class Package:
    def __init__(self, package_file, work_path, report_path):
        self.package_sender_email = ''
        self.package_file = package_file 
        self.report_path = report_path
        self.package_path = os.path.dirname(package_file)
        self.package_filename = os.path.basename(package_file)

        self.package_name = self.package_filename
        self.package_name = self.package_name[0:self.package_name.rfind('.')]

        self.work_path = work_path + '/' + self.package_name
        
        files = ['detailed.log', 'error.log', 'summarized.txt'] 
        self.report_files = [ report_path + '/' +  self.package_name + '_' + f for f in files ]
        log_filename, err_filename, summary_filename = self.report_files
        self.report = Report(log_filename, err_filename, summary_filename, 0, False) 
        self.report_files_to_send = [ summary_filename, err_filename ]
        #self.files = os.listdir(self.work_path)

    def open_package(self):
        self.report.write('\n' +'=' * 80 + '\n' +  'Package: ' + self.package_filename, True, False, True )
        uploaded_files_manager = UploadedFilesManager(self.report, self.package_path)
        uploaded_files_manager.backup(self.package_file)
        uploaded_files_manager.extract_file(self.package_file, self.work_path)
        self.files = os.listdir(self.work_path)
        
    def read_package_sender_email(self):
        if os.path.exists(work_path + '/email.txt'):
            f = open(work_path + '/email.txt', 'r')
            self.package_sender_email = f.read()
            self.package_sender_email = self.package_sender_email.replace(';', ',')
            f.close()
        return self.package_sender_email

    def fix_xml_extension(self):
        xml_list = [ f for f in self.files if f.endswith('.XML') ]
        if len(xml_list)>0:
            self.report.write('Program will convert .XML to .xml', True, False, False)
            for f in xml_list:
                new_name = self.work_path +'/' + f.replace('.XML','.xml')
                shutil.copyfile(self.work_path+'/'+f, new_name)
                if os.path.exists(new_name):
                    self.report.write('Converted ' + new_name, False, False, False)
                    os.unlink(self.work_path+'/'+f)
                else:
                    self.report.write('Unable to convert ' + new_name, True, False, False)

    def convert_img_to_jpg(self):
        ImageConverter().img_to_jpeg(self.work_path, self.work_path)

    def return_xml_images(self, xml_name):
        img_files = [ img_file[0:img_file.rfind('.')] for img_file in self.files if img_file.startswith(xml_name.replace('.xml', '-'))  ]
        return list(set(img_files))