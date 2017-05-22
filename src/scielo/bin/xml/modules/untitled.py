class PackageMaker(object):

    def __init__(self, source_path, original_files, original_name, destination_path, new_name):
        self.destination_path = destination_path
        self.new_name = new_name
        self.original_files = original_files
        self.original_name = original_name
        self.packed_files = []

    def pack_article_files(self):
        xpm_process_logger.register('pack_article_files: inicio')
        self.clean_folder()

    def clean_folder(self):
        for item in os.listdir(self.destination_path):
            if item.startswith(self.new_name + '-') or item.startswith(self.new_name + '.') or item.endswith('.sgm.xml'):
                eliminate = (item.endswith('incorrect.xml') or item.endswith('.sgm.xml'))
                if eliminate is False:
                    eliminate = not item.endswith('.xml')
                if eliminate:
                    try:
                        os.unlink(self.destination_path + '/' + item)
                    except:
                        pass

    def pack_article_href_files(self):
        for f in self.original_files:
            new_name = f.replace(original_name, new_name)
            self.packed_files.append(f, new_name)
            shutil.copyfile(self.source_path + '/' + f, self.destination_path + '/' + new_name)

    def generate_packed_files_report(self):
        #doc_files_info, dest_path, related_packed, href_packed, href_replacement_items, not_found

        def format(files_list):
            return ['   ' + c + ' => ' + n for c, n in files_list]

        def format2(files_list):
            return ['   ' + k + ' => ' + files_list[k] for k in sorted(files_list.keys())]

        xml_name = self.doc_files_info.xml_name
        new_name = self.new_name
        src_path = self.doc_files_info.xml_path
        dest_path = self.destination_path

        log = []

        log.append(_('Report of files') + '\n' + '-'*len(_('Report of files')) + '\n')

        if src_path != dest_path:
            log.append(_('Source path') + ':   ' + src_path)
        log.append(_('Package path') + ':  ' + dest_path)
        if src_path != dest_path:
            log.append(_('Source XML name') + ': ' + xml_name)
        log.append(_('Package XML name') + ': ' + new_name)

        log.append(message_file_list(_('Total of related files'), format2(self.replacements_related_files_items)))
        log.append(message_file_list(_('Total of files in package'), format2(self.replacements_href_files_items)))
        log.append(message_file_list(_('Total of @href in XML'), format(self.replacements_href_values)))
        log.append(message_file_list(_('Total of files not found in package'), format(self.missing_href_files)))

        return '\n'.join(log)

    def pack_article_xml_file(self):
        xpm_process_logger.register('pack_article_xml_file')
        original = self.version_info.local
        final = self.version_info.remote
        if self.is_db_generation:
            original = self.version_info.remote
            final = self.version_info.local
        self.content = self.content.replace('"' + original + '"', '"' + final + '"')
        fs_utils.write_file(self.doc_files_info.new_xml_filename, self.content)
        xpm_process_logger.register('pack_article_xml_file: fim')

