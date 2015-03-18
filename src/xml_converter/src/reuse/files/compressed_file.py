import os
import shutil

from files_extractor import extract_file, is_compressed_file


def delete_file_or_folder(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            delete_file_or_folder(path + '/' + item)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.unlink(path)


def copy_all_files_to(src, dest):
    if os.path.isdir(src):
        for item in os.listdir(src):
            copy_all_files_to(src + '/' + item, dest)
    elif os.path.isfile(src):
        shutil.copyfile(src, dest + '/' + os.path.basename(src))


class CompressedFile:
    def __init__(self, report):
        self.report = report

    def extract_files(self, compressed_file, destination_path, temp_dir=None):
        """
        Extract files to destination_path from compressed files that are in compressed_path
        """
        r = False

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        self.report.write('package file: ' + compressed_file, True, False, True)
        if os.path.isfile(compressed_file):
            if is_compressed_file(compressed_file):
                self.report.write('Extract ' + compressed_file + ' to ' + destination_path, True, False, True)
                if self.__extract__(compressed_file, destination_path, temp_dir):
                    r = True
        if not r:
            self.report.write(compressed_file + ' is not a valid file. It must be a compressed file.', True, True, True)

        return r

    def __extract__(self, compressed_file, destination_path, temp_dir=None):
        r = False
        # create destination path
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        # delete content of destination path
        if os.path.exists(destination_path):
            for i in os.listdir(destination_path):
                os.unlink(destination_path + '/' + i)
        # create tempdir
        if temp_dir is None:
            temp_dir = self.create_temp_dir()
        else:
            delete_file_or_folder(temp_dir)
            if not os.path.isdir(temp_dir):
                os.makedirs(temp_dir)

        # extract in tempdir
        if extract_file(compressed_file, temp_dir):
            copy_all_files_to(temp_dir, destination_path)
            r = True

        delete_file_or_folder(temp_dir)
        return r

    def create_temp_dir(self):
        import tempfile
        return tempfile.mkdtemp().replace('\\', '/')
