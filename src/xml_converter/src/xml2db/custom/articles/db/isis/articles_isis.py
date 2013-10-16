import os
import shutil
from reuse.db.isis.cisis import IDFile

class AheadManager:
    def __init__(self, cisis, journal_path):
        self.cisis = cisis
        self.journal_path = journal_path
        self.ahead_filenames = {}

        self.ahead_folders = [ folder for folder in os.listdir(journal_path) if 'ahead' in folder and not 'ex-' in folder ]

        for ahead_folder in self.ahead_folders:
            # 2013nahead
            for id_filename in os.listdir(journal_path + '/' + ahead_folder + '/id'):
                if id_filename != 'i.id':
                    filename = journal_path + '/' + ahead_folder + '/id/' + id_filename
                    print(filename)
                    j = IDFile().id2json(filename)
                    print(j)
                    doi = self.doi(j)
                    if doi != '':
                        self.ahead_filenames[doi] = filename  

    def doi(self, j):
        doi = ''
        #print(j)
        if type(j) == type([]):
            if len(j) > 0:
                if '706' in j[1].keys():
                    if j[1]['706'] in 'hf':
                        if '237' in j[1].keys():
                            doi = j[1]['237']
        elif type(j) == type({}):
            if 'h' in j.keys():
                if '237' in j['h'].keys():
                    doi = j['h']['237']

        return doi
        
    def filename(self, doi):
        f = ''
        if doi in self.ahead_filenames.keys():
            f = self.ahead_filenames[doi]
        return f 

    def exclude_filename(self, doi):

        excluded = False
        filename = self.filename(doi)

        if len(filename) > 0:
            if os.path.exists(filename):

                from datetime import date

                today = date.today().isoformat()

                # <journal>/<ano>nahead/id
                id_path = os.path.dirname(filename) + '_' + today
                
                
                if not os.path.exists(id_path):
                    os.makedirs(id_path)

                dest = id_path + '/' + os.path.basename(filename)
                if os.path.exists(dest):
                    os.unlink(dest)


                shutil.move(filename, dest)
                excluded = True
        return excluded

    def update_ahead_issue(self):
        for ahead_issue_folder in self.ahead_folders:
            id_path = self.journal_path + '/' + ahead_issue_folder + '/id'
            db_path = self.journal_path + '/' + ahead_issue_folder + '/base'

            db_name = ahead_issue_folder

            mst_filename = db_path + '/' + db_name

            
            id_filename = id_path + '/i.id'
            self.cisis.id2mst(id_filename, mst_filename, True)

            for id_name in os.listdir(id_path):
                if id_name != 'i.id' and id_name.endswith('.id') :
                    id_filename = id_path + '/' + id_name 
                    self.cisis.id2mst(id_filename, mst_filename, False)
        


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
            package.report.write(' ! ERROR: This package contains data of more than one issue:' , True, True, True)
            for issue in issues:
                package.report.write(issue.journal.acron + '  ' + issue.name, True, True, True)
            
    def return_validation_report_filenames(self, issues):
        print('2')
        f = []
        for issue in issues:
            issue_paths = IssuePath(self.paths, issue)
            xml_filenames = []
            for d in issue.documents:
                xml_filenames.append(os.path.basename(d.xml_filename).replace('.xml', ''))
            f += issue_paths.return_validation_report_filenames(xml_filenames)
        return f
    
    def save_issue(self, issue, package):

        ahead_manager = None

        package.report.write('Saving issue')
        issue_paths = IssuePath(self.paths, issue)

        package.report.write('Saving issue - add issue to scilista')

        self.add_issue_to_scilista(issue.journal.acron + ' ' + issue.name)  
        
        if not 'ahead' in issue_paths.issue_id_path:
            # package.report.write('Deleting')
            # for f in os.listdir(issue_paths.issue_id_path):
            #     os.unlink(issue_paths.issue_id_path + '/' + f)

            ahead_manager = AheadManager(self.cisis, issue_paths.journal_path)



        package.report.write('Saving issue record')
        self.save_issue_record(package, issue, issue_paths)

        
        package.report.write('Saving article records')
        excluded = 0
        for article in issue.documents:
            self.save_article_records(package, article, issue_paths)
            if ahead_manager != None:
                if article.doi != '':
                    if ahead_manager.exclude_filename(article.doi):
                        excluded += 1
        if excluded > 0:
            ahead_manager.update_ahead_issue()
            for folder in ahead_manager.ahead_folders:
                self.add_issue_to_scilista(issue.journal.acron + ' ' + folder)


        
        package.report.write('Generate issue db')
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
        self.cisis.mst2iso(issue_paths.issue_db_filename, issue_paths.issue_db_filename + '.iso')

        win_path = os.path.dirname(issue_paths.issue_db_filename)
        win_path = os.path.dirname(win_path)
        win_path += '/windows'
        
        
        if not os.path.exists(win_path):
            os.makedirs(win_path)
        if os.path.exists(win_path):
            self.cisis.crunchmf(issue_paths.issue_db_filename, win_path + '/' + os.path.basename(issue_paths.issue_db_filename))

 
    def add_issue_to_scilista(self, scilista_item):
        
        c = []
        if os.path.exists(self.paths.scilista):
            f = open(self.paths.scilista, 'r')
            c = f.read()
            f.close()

        if not scilista_item + '\n' in c:
            f = open(self.paths.scilista, 'a+')
            f.write(scilista_item + '\n')
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
        id_filename = issue_paths.article_filename(article)
        if os.path.exists(id_filename):
            os.unlink(id_filename)
        
        # generate id file for one article
        self.json2idfile_article.set_file_data(id_filename, package.report)
        
        self.json2idfile_article.format_and_save_document_data(article.json_data, self.records_order, issue_paths.issue_db_name, issue_paths.xml_filename(article.xml_filename))
        
        if not os.path.exists(id_filename):
            package.report.write('Unable to create ' + id_filename, True, True)
            package.report.write(article.json_data, True, True)
        # archive files
        
         
        #if article.issue.status != 'not_registered':
        issue_paths.archive_article_files(article.xml_filename, article.issue, package)
        #FIXME issue_files.archive_article_files(filename)

        
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
               
        if os.path.exists(filename):            
            if os.path.exists(dest_path + '/' + f):
                os.unlink(dest_path + '/' + f)

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

    def return_validation_report_filenames(self, startswith):
        print('3')
        files = []
        path = self.paths.web_outs_path + '/' + self.issue_folder
        print(path)
        print(startswith)
        for f in os.listdir(path):
            if f.endswith('.rep.html') :
                test = f[0:-len('.rep.html')].replace('.pmc', '')
                
                if test in startswith:
                    files.append(path + '/' + f)
        return sorted(files)
     
    @property
    def issue_folder(self):
        return  self.issue.journal.acron + '/' + self.issue.name

    @property
    def journal_path(self):
        return self.existing_path(self.paths.serial_path + '/' + self.issue.journal.acron )

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
     
    def article_filename(self, article):
        name = article.xml_filename
        id_filename = self.issue_id_path + '/' + os.path.basename(article.xml_filename.replace('.xml', '.id')) 
        order = '00000' + article.order

        new_id_filename = self.issue_id_path + '/' + order[-5:] + '.id'
        if os.path.exists(id_filename):
            os.unlink(id_filename)

        return new_id_filename
    
    
     
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

    def archive_article_files(self, xml_filename, issue, package):
        package.report.write( 'Archiving ' + self.issue.journal.acron + ' ' + self.issue.name)
        
        dirname = os.path.dirname(xml_filename)
        fname = os.path.basename(xml_filename).replace('.xml', '')

        if os.path.isdir(dirname):
            for f in os.listdir(dirname):
                if f.startswith(fname + '-') or f.startswith(fname + '.'):

                    ext = f[f.rfind('.')+1:]
                    
                    filename = dirname + '/' +  f 
                    if ext in self.paths.extension_path.keys():
                        
                        if ext == 'pdf' and f.startswith(fname + '-'):
                            # lang (pt, es, etc)
                            rename_to = f[-6:-4] + '_' + fname + '.' + ext

                            shutil.copyfile(filename, dirname + '/' +  rename_to)
                            filename = dirname + '/' +  rename_to
                        
                        if os.path.isfile(filename):
                            package.report.write( 'Archiving ' + filename + ' in ' + self.paths.extension_path[ext] + '/' + self.issue_folder)
                        
                        if not self.paths.move_file_to_path(filename, self.paths.extension_path[ext] + '/' + self.issue_folder):
                            package.report.write('Unable to archive ' + filename + ' in ' + self.paths.extension_path[ext] + '/' + self.issue_folder, False, True, True)
                    

                    else:
                        os.unlink(filename)
                        package.report.write(filename + ' was ignored/deleted.', False, True, True)



