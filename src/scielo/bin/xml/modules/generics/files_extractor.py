# coding=utf-8
## {{{ http://code.activestate.com/recipes/576714/ (r2)
import os
import tarfile
import zipfile


def is_compressed_file(path):
    r = False
    if path.endswith('.zip'):
        r = True
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        r = True
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        r = True
    return r


def extract_file(path, to_directory='.'):
    r = False

    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError("Could not extract `%s` as no appropriate extractor is found" % path)
    cwd = os.getcwd()
    os.chdir(to_directory)
    try:
        file = opener(path, mode)
        try:
            file.extractall()
        finally:
            file.close()
        r = True
    except IOError:
        print('extract_file: Invalid file ' + path)
        r = False
    finally:
        os.chdir(cwd)
        return r
## end of http://code.activestate.com/recipes/576714/ }}}
