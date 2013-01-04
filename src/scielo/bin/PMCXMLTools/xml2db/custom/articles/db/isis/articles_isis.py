import os

import shutil

class ISISManager4Articles:
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

    def update(self, issues, package):
        #print(issues)
        for issue in issues:
            self.save_issue(issue, package)
        if len(issues) > 1:
            package.report.write(' ! ERROR: This package contains data of more than one issue:' + ','.join(issues.keys()), True, True, True)
    
    
    def save_issue(self, issue, package):
        package.report.write('Saving issue', True)
        issue_paths = IssuePath(self.paths, issue)

        package.report.write('Saving issue - add issue to scilista', True)
        self.add_issue_to_scilista(issue) 
        
        package.report.write('Saving issue record', True)
        self.save_issue_record(package, issue, issue_paths)

        package.report.write('Saving article records', True)
        for article in issue.documents:
            self.save_article_records(package, article, issue_paths)
        
        package.report.write('Generate issue db', True)
        self.generate_issue_db(issue, package, issue_paths)




        
    def generate_issue_db(self, issue, package, issue_paths):
        count_id = len(os.listdir(issue_paths.issue_id_path) ) - 1
        #print(type(issue.documents))
        package.report.write(' Total of xml files: ' + str(issue.documents.count), True, False, False )
        package.report.write(' Total of id files: ' + str(count_id) , True, False, False  )
        package.report.write(' Status of ' + issue.journal.acron +  ' ' + issue.name  + ': ' + issue.status, True, False, False  )

        if os.path.exists(issue_paths.issue_db_filename + '.mst'):
            os.unlink(issue_paths.issue_db_filename + '.mst')
            os.unlink(issue_paths.issue_db_filename + '.xrf')

        self.cisis.id2mst(issue_paths.issue_i_record_filename , issue_paths.issue_db_filename, False)
        for id_file in os.listdir(issue_paths.issue_id_path):
            if id_file != 'i.id':
                self.cisis.id2mst(issue_paths.issue_id_path + '/' + id_file, issue_paths.issue_db_filename, False)
        if issue.documents.count != count_id:
            package.report.write(' ! WARNING: Check total of xml files and id files', True, True, True )            

 
    def add_issue_to_scilista(self, issue):
        journal_acron = issue.journal.acron
        issue_label = issue.name
        c = []
        if os.path.exists(self.paths.scilista):
            f = open(self.paths.scilista, 'r')
            c = f.read()
            f.close()

        if not journal_acron + ' ' + issue_label + '\n' in c:
            f = open(self.paths.scilista, 'a+')
            f.write(journal_acron + ' ' + issue_label + '\n')
            f.close()

    def generate_issue_db_for_proc(self, table_name):
        proc_issue_db = self.filename(table_name)

        self.cisis.create('null count=0', proc_issue_db)
        src_path = self.paths.i_records_path
        for f in os.listdir(src_path):
            self.cisis.id2mst(src_path + '/' + f, proc_issue_db, False)        
    

                

    def save_issue_record(self, package, issue, issue_paths):

        #print(type(issue.documents))
        #print(type(issue.articles))

       
        package.report.write('\n' + '-' * 80 + '\n' + 'Generating db ' + issue.journal.acron +  issue.name, True, False, True )
            
        # generate id filename
        self.json2idfile.set_file_data(issue_paths.i_filename, package.report)
        issue.json_data['122'] = str(issue.documents.count)
        issue.json_data['49'] = issue.toc.return_json()
        self.json2idfile.format_and_save_document_data(issue.json_data)
        
        self.cisis.id2mst(issue_paths.i_filename, issue_paths.issue_db_filename, True)

        # copy id filename to processing path
        if os.path.exists(issue_paths.issue_i_record_filename):
            os.unlink(issue_paths.issue_i_record_filename)
        shutil.copyfile(issue_paths.i_filename, issue_paths.issue_i_record_filename)

    def save_article_records(self, package, article, issue_paths):
        
        # identify files and paths
        id_filename = issue_paths.article_filename(article.xml_filename)
        
        # generate id file for one article
        self.json2idfile_article.set_file_data(id_filename, package.report)
        self.json2idfile_article.format_and_save_document_data(article.json_data, self.records_order, issue_paths.issue_db_name, issue_paths.xml_filename(article.xml_filename))
        
        # archive files
        
        package.report.write(package.package_path)
        package.report.write(','.join(os.listdir(package.package_path)))
        package.report.write(article.xml_filename)
        package.report.write(','.join(package.return_matching_files(os.path.basename(article.xml_filename))))
        
        #if article.issue.status != 'not_registered':
        issue_paths.archive(package.return_matching_files(os.path.basename(article.xml_filename)), article.issue, package)
        #FIXME issue_files.archive(filename)

        
class Paths:
    def __init__(self, serial_path, web_pdf_path, web_xml_path, web_img_path, scilista):
        self.serial_path = serial_path
        self.web_pdf_path = web_pdf_path
        self.web_xml_path = web_xml_path
        self.web_img_path = web_img_path    
        self.web_outs_path = self.web_xml_path[0:-3] + 'outs'
        

        self.scilista = scilista
   
        self.extension_path = {}
        self.extension_path['xml'] = self.web_xml_path
        self.extension_path['xml~'] = self.web_xml_path
        self.extension_path['jpg'] = self.web_img_path
        self.extension_path['pdf'] = self.web_pdf_path
        self.extension_path['epub'] = self.web_outs_path
        self.extension_path['html'] = self.web_outs_path
        
        self.i_records_path = self.serial_path + '/i'

     
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

     
    def existing_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

     
    @property
    def issue_folder(self):
        return  self.issue.journal.acron + '/' + self.issue.name

    @property
    def issue_path(self):
        return self.existing_path(self.paths.serial_path + '/' + self.issue_folder )

     
    @property
    def issue_id_path(self):
        return self.existing_path(self.issue_path + '/id')

     
    @property
    def issue_db_path(self):
        return self.existing_path(self.issue_path + '/base')

     
    @property
    def i_filename(self):
        return self.issue_id_path + '/i.id'
     
    def article_filename(self, xml_filename):
        return self.issue_id_path + '/' + os.path.basename(xml_filename.replace('.xml', '.id')) 
    
    
     
    @property
    def issue_i_record_filename(self):
        return self.existing_path(self.paths.i_records_path) + '/' + self.issue.journal.acron + self.issue.name + '.id'
        
     
    @property
    def issue_db_filename(self):
        return self.issue_db_path + '/' + self.issue.name

     
    @property
    def issue_db_name(self):
        return  self.issue.name

     
    
    def xml_filename(self, xml_filename):
        return self.issue_folder + '/' + os.path.basename(xml_filename)

    def archive(self, files, issue, package):
        package.report.write( 'Archiving ' + self.issue.journal.acron + ' ' + self.issue.name)

        for f in files:

            ext = f[f.rfind('.')+1:]
            package.report.write('ext=' + ext)

            filename =  package.package_path + '/' +  f 
            if ext in self.paths.extension_path.keys():
                  
                
                package.report.write('file:' + f)
                package.report.write('package_path and file:' + filename)

                if os.path.exists(filename) and os.path.isfile(filename):
                    path = self.paths.extension_path[ext]

                    package.report.write( 'Archiving ' + filename + ' in ' + path + '/' + self.issue_folder)
                    
                    if not self.paths.move_file_to_path(filename, path + '/' + self.issue_folder):
                        package.report.write('Unable to archive ' + filename + ' in ' + path + '/' + self.issue_folder)
                

            else:
                os.unlink(filename)
                package.report.write(filename + ' was ignored/deleted.')



