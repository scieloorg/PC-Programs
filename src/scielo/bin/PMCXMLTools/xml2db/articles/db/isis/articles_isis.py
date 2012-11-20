import os


class ISISArticle:
    def __init__(self, cisis, idfile, paths, records_order, json2idfile, json2idfile_article):
        self.cisis = cisis
        self.idfile = idfile
        self.tables = {}
        self.records_order = records_order
        self.paths = paths
        self.json2idfile = json2idfile
        self.json2idfile_article = json2idfile_article


    def create_table(self, table_name, filename):
    	self.tables[table_name] = filename

    @property 
    def filename(self, table_name, ext = ''):
        return self.tables[table_name] + ext 

    def db2json(self, table_name):
        from tempfile import mkstemp
        import os
        r = []
        if os.path.exists(self.filename(table_name, '.mst')):
            _, f = mkstemp()
            self.cisis.i2id(self.filename(table_name), f)
            r = self.idfile.id2json(f)
            os.remove(f)
        return r

    def save_issue(self, issues, package):
        for issue in issues:
            issue_paths = IssuePath(self.paths, issue)
            self.add_issue_to_scilista(issue) 
            self.save_issue_record(package, issue, issue_path)
            for article in issue.articles:
                self.save_article_records(package, article, issue_paths)
            
            self.generate_issue_db(issue, package, issue_paths)
            for f in os.listdir(package.package_path):
                os.unlink(package.package_path + '/' + f)


        if len(issues) > 1:
            package.report.write(' ! ERROR: This package contains data of more than one issue:' + ','.join(issues.keys()), True, True, True)
    
    
    def generate_issue_db(self, issue, package, issue_paths):
            count_id = len(os.listdir(issues_path.issue_id_path) ) - 1
            package.report.write(' Total of xml files: ' + str(len(issue.articles.elements)), True, False, False )
            package.report.write(' Total of id files: ' + str(count_id) , True, False, False  )
            package.report.write(' Status of ' + issue.journal.acron +  ' ' + issue.name  + ': ' + issue.status, True, False, False  )

            if os.path.exists(issue_paths.issue_db_filename + '.mst'):
                os.unlink(issue_paths.issue_db_filename + '.mst')
                os.unlink(issue_paths.issue_db_filename + '.xrf')

            self.cisis.id2mst(issues_path.issue_i_record_filename , issue_paths.issue_db_filename, False)
            for idfile in os.listdir(issues_path.issue_id_path):
                if id_file != 'i.id':
                    self.cisis.id2mst(issues_path.issue_id_path + '/' + id_file, issue_paths.issue_db_filename, False)
            if len(issue.articles.elements) != count_id:
                package.report.write(' ! WARNING: Check total of xml files and id files', True, True, True )            

 
    def add_to_scilista(self, journal_acron, issue_label):
        c = []
        if os.path.exists(self.paths.scilista):
            f = open(self.paths.scilista, 'r')
            c = f.read()
            f.close()

        if not journal_acron + ' ' + issue_label + '\n' in c:
            f = open(self.paths.scilista, 'a+')
            f.write(journal_acron + ' ' + issue_label + '\n')
            f.close()


    def save_issue_record(self, package, issue, issue_paths):
       
        package.report.write('\n' + '-' * 80 + '\n' + 'Generating db ' + issue.name, True, False, True )
            
        # generate id filename
        id_file = self.json2idfile.set_file_data(issue_paths.i_filename, package.report)
        issue.json_data['122'] = str(len(issue.articles.elements))
        issue.json_data['49'] = issue.toc.return_json()
        id_file.format_and_save_document_data(issue.json_data)

        self.cisis.id2mst(issue_paths.i_filename, issue_paths.issue_db_filename, True)

        # copy id filename to processing path
        if os.path.exists(self.issue_i_record_filename(issue)):
            os.unlink(self.issue_i_record_filename(issue))
        shutil.copyfile(issue_paths.i_filename, issue_paths.issue_i_record_filename)

    def save_article_records(self, package, article, issue_paths):
        
        # identify files and paths
        id_filename = issue_paths.article_filename(article.xml_filename)
        
        # generate id file for one article
        id_file = self.json2idfile_article.set_file_data(id_filename, package.report)
        id_file.format_and_save_document_data(article.json_data, self.records_order, issue_paths.issue_db_name, issue_paths.xml_filename(article.xml_filename))
        
        # archive files
        

        issue_paths.archive(package.return_matching_files(os.path.basename(article.xml_filename)), issue, package)
        #FIXME issue_files.archive(filename)

        
class Paths:
    def __init__(self, serial_path, web_pdf_path, web_xml_path, web_img_path, scilista):
        self.serial_path = serial_path
        self.web_pdf_path = web_pdf_path
        self.web_xml_path = web_xml_path
        self.web_img_path = web_img_path    
        
        self.scilista = scilista
   
        self.extension_path = {}
        self.extension_path['xml'] = self.web_xml_path
        self.extension_path['jpg'] = self.web_img_path
        self.extension_path['pdf'] = self.web_pdf_path
        
        self.i_records_path = self.serial_path + '/i'

    @property 
    def extension_path(self, ext):
        r = ''
        if ext in self.extension_path.keys():
            r = self.extension_path[ext]
        return r

    def move_file_to_path(self, filename, dest_path):
        f = os.path.basename(filename)
        if os.path.exists(dest_path + '/' + f):
            os.unlink(dest_path + '/' + f)
        if os.path.exists(filename):
            
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
    
            shutil.move(filename, dest_path)
        return os.path.exists(dest_path + '/' + f)

class IssuePath:
    def __init__(self, paths, issue):
        self.issue = issue
        self.paths = paths 

    @property 
    def existing_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @property 
    def issue_path(self):
        return self.existing_path(self.paths.serial_path + '/' + self.issue.journal.acron + '/' + self.issue.name )

    @property 
    def issue_id_path(self):
        return self.existing_path(self.issue_path + '/id')

    @property 
    def issue_db_path(self):
        return self.existing_path(self.issue_path + '/base')

    @property 
    def i_filename(self):
        return self.issue_id_path + '/i.id'
    @property 
    def article_filename(self, xml_filename):
        return self.issue_id_path + '/' + os.path.basename(xml_filename.replace('.xml', '.id')) 
    
    
    @property 
    def issue_i_record_filename(self):
        return self.paths.i_records_path + '/' + self.issue.journal.acron + self.issue.name + '.id'
        
    @property 
    def issue_db_filename(self):
        return self.issue_db_path + '/' + self.issue.name

    @property 
    def issue_db_name(self):
        return  self.issue.name

    @property 
    def xml_filename(self, xml_filename):
        return self.issue.journal.acron + '/' +  self.issue.name + '/' + os.path.basename(xml_filename)

    def archive(self, files, issue, package):
        for f in files:
            ext = f[-3:]
            path = self.paths.extension_path(ext)
            if path != '':
                self.paths.move_file_to_path(package.package_path + '/' + f, path + '/' + self.issue.journal.acron + '/' + self.issue.name)
            else:
                os.unlink(package.package_path + '/' +  f)

