import os
import shutil
from reuse.db.isis.cisis import IDFile


class AheadManager:
    def __init__(self, cisis, journal_path):
        self.cisis = cisis
        self.journal_path = journal_path
        self.ahead_filenames = {}

        self.ahead_folders = [folder for folder in os.listdir(journal_path) if folder.endswith('ahead') and not folder.startswith('ex-')]

        for ahead_folder in self.ahead_folders:
            # 2013nahead
            id_path = journal_path + '/' + ahead_folder + '/base_xml/id'
            if not os.path.isdir(id_path):
                os.makedirs(id_path)
            old_id_path = journal_path + '/' + ahead_folder + '/id'
            if os.path.isdir(old_id_path):
                for id_filename in os.listdir(old_id_path):
                    if not os.path.isfile(id_path + '/' + id_filename):
                        shutil.copy(old_id_path + '/' + id_filename, id_path)
                try:
                    import fs_utils
                    fs_utils.delete_file_or_folder(old_id_path)
                except:
                    pass
            for id_filename in os.listdir(id_path):
                if id_filename != 'i.id':
                    filename = id_path + '/' + id_filename
                    j = IDFile().id2json(filename)
                    doi = self.doi(j)
                    if doi != '':
                        self.ahead_filenames[doi] = filename

    def doi(self, j):
        _doi = ''
        #print(j)
        if isinstance(j, list):
            if len(j) > 0:
                if '706' in j[1].keys():
                    if j[1]['706'] in 'hf':
                        if '237' in j[1].keys():
                            _doi = j[1]['237']
        elif isinstance(j, dict):
            if 'h' in j.keys():
                if '237' in j['h'].keys():
                    _doi = j['h']['237']
        return _doi

    def filename(self, doi):
        f = ''
        if doi in self.ahead_filenames.keys():
            f = self.ahead_filenames[doi]
        return f

    def exclude_filename(self, doi):
        excluded = False
        filename = self.filename(doi)
        print('exclude: ' + filename + '.')
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
                print('excluded ' + filename)

                shutil.move(filename, dest)
                excluded = True
        else:
            print('doi not found in ahead files')
            existing = []
            for doi, filename in self.ahead_filenames.items():
                existing.append(doi + ' ' + filename)
            print('\n'.join(sorted(existing)))
        return excluded

    def update_ahead_issue(self):
        for ahead_issue_folder in self.ahead_folders:
            id_path = self.journal_path + '/' + ahead_issue_folder + '/base_xml/id'
            db_path = self.journal_path + '/' + ahead_issue_folder + '/base'

            db_name = ahead_issue_folder

            mst_filename = db_path + '/' + db_name
            id_filename = id_path + '/i.id'
            self.cisis.id2mst(id_filename, mst_filename, True)

            for id_name in os.listdir(id_path):
                order = id_name.replace('.id', '')
                if order.isdigit():
                    if id_name != 'i.id' and id_name != '00000.id' and id_name.endswith('.id'):
                        print('update_ahead_issue:' + id_path + '/' + id_name)
                        self.cisis.id2mst(id_path + '/' + id_name, mst_filename, False)


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

    def filename(self, table_name, ext=''):
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
        if len(issues) == 1:
            for issue in issues:
                self.save_issue(issue, package)
        else:
            package.report.result += ' ! FATAL ERROR: This package does not contains one issue:'
            for issue in issues:
                package.report.result += issue.journal.acron + '  ' + issue.name + '\n'

    def return_validation_report_filenames(self, issues):
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
            if ahead_manager is not None:
                if article.doi != '':
                    if ahead_manager.exclude_filename(article.doi):
                        excluded += 1
        print('excluded=')
        print(excluded)
        if ahead_manager is not None:
            ahead_manager.update_ahead_issue()
            for folder in ahead_manager.ahead_folders:
                print('add to scilista')
                print(issue.journal.acron + ' ' + folder)
                self.add_issue_to_scilista(issue.journal.acron + ' ' + folder)

        package.report.write('Generate issue db')
        self.generate_issue_db(issue, package, issue_paths)

    def generate_issue_db(self, issue, package, issue_paths):
        count_id = len(os.listdir(issue_paths.issue_id_path)) - 1
        #print(type(issue.documents))
        package.report.write(' Total of xml files: ' + str(issue.documents.count), True, False, False)
        package.report.write(' Total of id files: ' + str(count_id), True, False, False)
        package.report.write(' Status of ' + issue.journal.acron + ' ' + issue.name + ': ' + issue.status, True, False, False)

        if os.path.exists(issue_paths.issue_db_filename + '.mst'):
            os.unlink(issue_paths.issue_db_filename + '.mst')
            os.unlink(issue_paths.issue_db_filename + '.xrf')

        for id_file in os.listdir(issue_paths.issue_id_path):
            order = id_file.replace('.id', '')
            if not order == 'i':
                if not order.isdigit():
                    os.unlink(issue_paths.issue_id_path + '/' + id_file)
        self.cisis.id2mst(issue_paths.issue_i_record_filename, issue_paths.issue_db_filename, False)
        id_files = [f for f in os.listdir(issue_paths.issue_id_path) if f.endswith('.id') and f.replace('.id', '').isdigit()]
        for id_file in id_files:
            #order = id_file.replace('.id', '')
            #if order.isdigit():
            package.report.write(id_file, True, False, False)
            self.cisis.id2mst(issue_paths.issue_id_path + '/' + id_file, issue_paths.issue_db_filename, False)

        if issue.documents.count > count_id:
            package.report.result += ' ! FATAL ERROR: Some articles are not published.'

        package.report.result += 'Published/updated articles: ' + str(len(id_files)) + '\n' + '\n'.join(sorted([f.replace('.id', '.xml') for f in id_files]))

        self.cisis.mst2iso(issue_paths.issue_db_filename, issue_paths.issue_db_filename + '.iso')

        win_path = os.path.dirname(issue_paths.issue_db_filename)
        win_path = os.path.dirname(win_path)
        win_path += '/windows'
        if not os.path.exists(win_path):
            os.makedirs(win_path)
        if os.path.exists(win_path):
            self.cisis.crunchmf(issue_paths.issue_db_filename, win_path + '/' + os.path.basename(issue_paths.issue_db_filename))

    def add_issue_to_scilista(self, scilista_item):
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
        package.report.write('\n' + '-' * 80 + '\n' + 'Generating db ' + issue.journal.acron + issue.name, True, False, True)

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
        creation_date = None

        id_filename = issue_paths.article_filename(article)
        if os.path.isfile(id_filename):
            j = IDFile().id2json(id_filename)
            if len(j) > 0:
                if j[0].get('91') is not None and j[0].get('92') is not None:
                    creation_date = (j[0].get('91'), j[0].get('92'))

        if os.path.exists(id_filename):
            os.unlink(id_filename)

        # generate id file for one article
        self.json2idfile_article.set_file_data(id_filename, package.report, creation_date)

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
        self.extension_path['pdf'] = self.web_pdf_path

        self.i_records_path = self.serial_path + '/i'

    def get_destination_path(self, filename):
        ext = filename[filename.rfind('.')+1:]
        return self.extension_path.get(ext, self.web_img_path)

    def move_file_to_path(self, filename, issue_folder):
        r = False
        dest_path = self.get_destination_path(filename) + '/' + issue_folder
        f = os.path.basename(filename)
        if os.path.exists(filename):
            if os.path.exists(dest_path + '/' + f):
                os.unlink(dest_path + '/' + f)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            if not filename.endswith('.tif') and not filename.endswith('.tiff'):
                shutil.move(filename, dest_path)
                r = os.path.exists(dest_path + '/' + f)
            else:
                r = True
        return r


class IssuePath:
    def __init__(self, paths, issue):
        self.issue = issue
        self.paths = paths
        self.move_old_id_folder()

    def existing_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def return_validation_report_filenames(self, startswith):
        files = []
        path = self.paths.web_outs_path + '/' + self.issue_folder
        for f in os.listdir(path):
            if f.endswith('.rep.html'):
                test = f[0:-len('.rep.html')].replace('.pmc', '')
                if test in startswith:
                    files.append(path + '/' + f)
        return sorted(files)

    @property
    def issue_folder(self):
        return self.issue.journal.acron + '/' + self.issue.name

    @property
    def journal_path(self):
        return self.existing_path(self.paths.serial_path + '/' + self.issue.journal.acron)

    @property
    def issue_path(self):
        return self.existing_path(self.paths.serial_path + '/' + self.issue_folder)

    @property
    def issue_id_path(self):
        return self.existing_path(self.issue_path + '/base_xml/id')

    @property
    def issue_base_source_path(self):
        return self.existing_path(self.issue_path + '/base_xml/base_source')

    @property
    def issue_old_id_path(self):
        return self.existing_path(self.issue_path + '/id')

    @property
    def issue_db_path(self):
        return self.existing_path(self.issue_path + '/base')

    @property
    def i_filename(self):
        return self.issue_id_path + '/i.id'

    def article_filename(self, article):
        id_filename = self.issue_id_path + '/' + os.path.basename(article.xml_filename.replace('.xml', '.id'))
        #if os.path.exists(id_filename):
        #    os.unlink(id_filename)

        order = '00000' + article.order

        new_id_filename = self.issue_id_path + '/' + order[-5:] + '.id'
        return new_id_filename

    @property
    def issue_i_record_filename(self):
        return self.existing_path(self.paths.i_records_path) + '/' + self.issue.journal.acron + self.issue.name + '.id'

    @property
    def issue_db_filename(self):
        return self.issue_db_path + '/' + self.issue.name

    @property
    def issue_db_name(self):
        return self.issue.name

    def xml_filename(self, _xml_filename):
        return self.issue_folder + '/' + os.path.basename(_xml_filename)

    def archive_article_files(self, xml_filename, issue, package):
        package.report.write('Archiving ' + self.issue.journal.acron + ' ' + self.issue.name)
        xml_content = open(xml_filename).read() if os.path.isfile(xml_filename) else ''
        if not os.path.isdir(self.issue_base_source_path):
            os.makedirs(self.issue_base_source_path)
        if len(xml_content) > 0:
            if not isinstance(xml_content, unicode):
                xml_content = xml_content.decode('utf-8')
            dirname = os.path.dirname(xml_filename)
            fname = os.path.basename(xml_filename).replace('.xml', '')
            if os.path.isdir(dirname):
                for f in os.listdir(dirname):
                    if f.startswith(fname + '-') or f.startswith(fname + '.'):
                        src_filename = dirname + '/' + f
                        shutil.copy(src_filename, self.issue_base_source_path)
                        if src_filename.endswith('.pdf') and f.startswith(fname + '-'):
                            if not '="' + f + '"' in xml_content:
                                # ajusta o nome do arquivo pdf de traducao
                                rename_to = f[-6:-4] + '_' + fname + '.pdf'
                                shutil.copyfile(src_filename, dirname + '/' + rename_to)
                                os.unlink(src_filename)
                                src_filename = dirname + '/' + rename_to

                        self.paths.move_file_to_path(src_filename, self.issue_folder)
        print('fim archive_article_files.')

    def move_old_id_folder(self):
        if os.path.isdir(self.issue_old_id_path):
            if not os.path.isdir(self.issue_id_path):
                os.makedirs(self.issue_id_path)
            for item in os.listdir(self.issue_old_id_path):
                if not os.path.isfile(self.issue_id_path + '/' + item):
                    shutil.copyfile(self.issue_old_id_path + '/' + item, self.issue_id_path + '/' + item)
            try:
                import fs_utils
                fs_utils.delete_file_or_folder(self.issue_old_id_path)
            except:
                pass
