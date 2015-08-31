# coding=utf-8


import os
from tempfile import mkdtemp, NamedTemporaryFile

from article_utils import u_encode
import xml_utils
import utils


def format_value(content):
    try:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
    except Exception as e:
        utils.debbuging('format_value 1:')
        utils.debbuging(e)
        utils.debbuging(content)

    try:
        content = xml_utils.remove_break_lines_characters(content)
    except Exception as e:
        utils.debbuging('format_value: remove_break_lines_characters:')
        utils.debbuging(e)
        utils.debbuging(content)

    try:
        if '&' in content:
            content, replace = xml_utils.convert_entities_to_chars(content)
    except Exception as e:
        utils.debbuging('format_value:  convert_entities_to_chars:')
        utils.debbuging(e)
        utils.debbuging(content)

    try:
        if not isinstance(content, unicode):
            content = content.decode('utf-8')
    except Exception as e:
        utils.debbuging('format_value: 2:')
        utils.debbuging(e)
        utils.debbuging(content)

    return content


class IDFile(object):

    def __init__(self, content_formatter=None):
        self.content_formatter = content_formatter

    def _format_file(self, records):
        r = ''
        index = 0
        for item in records:
            index += 1
            r += self._format_id(index) + self._format_record(item)
        return r

    def _format_id(self, index):
        i = '000000' + str(index)
        return '!ID ' + i[-6:] + '\n'

    def _format_record(self, record):
        result = ''
        if record is not None:
            #utils.debbuging(record)
            r = []
            for tag_i in sorted([int(s) for s in record.keys() if s.isdigit()]):
                tag = str(tag_i)
                data = record.get(tag)
                r.append(self.tag_data(tag, data))
            result = ''.join(r)

            if self.content_formatter is not None:
                result = self.content_formatter(result)
        return result

    def tag_data(self, tag, data):
        occs = []
        if not isinstance(data, list):
            data = [data]
        for item in data:
            occs.append(self.tag_occ(tag, item))

        return ''.join(occs)

    def tag_occ(self, tag, data):
        if isinstance(data, tuple):
            utils.debbuging(tag)
            utils.debbuging(data)
            s = ''
        elif isinstance(data, dict):
            s = self.tag_content(tag, self.format_subfields(data))
        else:
            s = self.tag_content(tag, data)
        return s

    def format_subfields(self, subf_and_value_list):
        try:
            first = u''
            value = u''
            for k, v in subf_and_value_list.items():
                if v is not None and v != '' and len(k) == 1:
                    v = format_value(v)
                    if k in 'abcdefghijklmnopqrstuvwxyz123456789':
                        value += u'^' + k + v
                    elif k in '_':
                        first = v
        except Exception as e:
            utils.debbuging('format_subfields')
            utils.debbuging(e)
            utils.debbuging(subf_and_value_list)
            utils.debbuging(first + value)
        return first + value

    def tag_content(self, tag, value):
        r = ''
        s = value
        if int(tag) <= 999:
            if value is not None and value != '':
                try:
                    tag = '000' + tag
                    tag = tag[-3:]
                    r = '!v' + tag + '!' + format_value(value) + '\n'
                except Exception as e:
                    utils.debbuging('tag_content: ')
                    utils.debbuging(e)
                    utils.debbuging(s)
                    utils.debbuging(value)
                    utils.debbuging(type(s))
                    utils.debbuging(type(value))
        return r

    def read(self, filename):
        rec_list = []
        record = {}
        for line in open(filename, 'r').readlines():
            line = line.strip()
            if not isinstance(line, unicode):
                line = line.decode('iso-8859-1')
            if '!ID ' in line:
                if len(record) > 0:
                    rec_list.append(self.simplify_record(record))
                record = {}
            else:
                item = line.split('!')
                tag = None
                if len(item) == 3:
                    ign, tag, content = item
                elif len(item) > 3:
                    tag = item[1]
                    content = line[6:]
                if tag is not None and content != '':
                    tag = str(int(tag[1:]))
                    if not tag in record.keys():
                        record[tag] = []
                    content = content.replace('^', 'BREAKSUBF^')
                    subfields = content.split('BREAKSUBF')
                    content = {}
                    for subf in subfields:
                        if subf.startswith('^'):
                            c = subf[1]
                            v = subf[2:]
                        else:
                            if len(subfields) == 1:
                                c = ''
                                v = subf
                            else:
                                c = '_'
                                v = subf
                        if len(c) > 0:
                            content[c] = v
                        else:
                            content = v
                    record[tag].append(content)

        # last record
        if len(record) > 0:
            rec_list.append(self.simplify_record(record))

        return rec_list

    def simplify_record(self, record):
        for tag, content in record.items():
            if len(content) == 1:
                record[tag] = content[0]
        return record

    def save(self, filename, records):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        content = self._format_file(records)

        if isinstance(content, unicode):
            content = u_encode(content, 'iso-8859-1')
        try:
            open(filename, 'w').write(content)
        except Exception as e:
            utils.debbuging('saving...')
            utils.debbuging(e)


class CISIS(object):

    def __init__(self, cisis_path):
        cisis_path = cisis_path.replace('\\', '/')
        self.temp_dir = mkdtemp().replace('\\', '/')
        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path
        else:
            utils.debbuging('Invalid cisis path: ' + cisis_path)

    def crunchmf(self, mst_filename, wmst_filename):
        cmd = self.cisis_path + '/crunchmf ' + mst_filename + ' ' + wmst_filename
        os.system(cmd)

    def id2i(self, id_filename, mst_filename):
        cmd = self.cisis_path + '/id2i ' + id_filename + ' create=' + mst_filename
        os.system(cmd)

    def append(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  append=' + dest + ' now -all'
        os.system(cmd)

    def create(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + ' create=' + dest + ' now -all'
        os.system(cmd)

    def append_id_to_master(self, id_filename, mst_filename, reset):
        if reset:
            self.id2i(id_filename, mst_filename)
        else:
            temp = id_filename.replace('.id', '')
            self.id2i(id_filename, temp)
            self.append(temp, mst_filename)
            try:
                os.unlink(temp + '.mst')
                os.unlink(temp + '.xrf')
            except:
                pass

    def i2id(self, mst_filename, id_filename):
        cmd = self.cisis_path + '/i2id ' + mst_filename + ' > ' + id_filename
        os.system(cmd)

    def mst2iso(self, mst_filename, iso_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' iso=' + iso_filename + ' now -all'
        os.system(cmd)

    def iso2mst(self, iso_filename, mst_filename):
        cmd = self.cisis_path + '/mx iso=' + iso_filename + ' create=' + mst_filename + ' now -all'
        os.system(cmd)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        os.system(cmd)

    def modify_records(self, mst_filename, proc):
        temp = self.temp_dir + '/f'
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "proc=' + proc + '" append=' + temp + ' now -all'
        os.system(cmd)
        self.create(temp, mst_filename)

    def find_record(self, mst_filename, expression):
        r = mst_filename + expression
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "bool=' + expression + '"  lw=999 "pft=mfn/" now > ' + r
        os.system(cmd)
        return [l.strip().decode('utf-8') for l in open(r, 'r').readlines()]

    def new(self, mst_filename):
        cmd = self.cisis_path + '/mx null count=0 create="' + mst_filename + '" now -all'
        os.system(cmd)

    def search(self, mst_filename, expression, result_filename):
        if os.path.isfile(result_filename + '.mst'):
            os.unlink(result_filename + '.mst')
            os.unlink(result_filename + '.xrf')
        cmd = self.cisis_path + '/mx btell=0 ' + mst_filename + ' "bool=' + expression + '"  lw=999 append=' + result_filename + ' now -all'
        os.system(cmd)

    def generate_indexes(self, mst_filename, fst_filename, inverted_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' fst=@' + fst_filename + ' fullinv=' + inverted_filename
        os.system(cmd)

    def is_readable(self, mst_filename):
        s = ''
        if os.path.isfile(mst_filename + '.mst'):
            temp = self.temp_dir + '/readable'
            cmd = self.cisis_path + '/mx ' + mst_filename + ' +control now > ' + temp
            os.system(cmd)
            if os.path.isfile(temp):
                s = open(temp, 'r').read()
        return len(s) > 0


class UCISIS(object):

    def __init__(self, cisis1030, cisis1660):
        self.cisis1030 = cisis1030
        self.cisis1660 = cisis1660
        self.temp_dir = mkdtemp().replace('\\', '/')

    def cisis(self, mst_filename):
        if os.path.isfile(mst_filename + '.mst'):
            if self.cisis1030.is_readable(mst_filename):
                return self.cisis1030
            elif self.cisis1660.is_readable(mst_filename):
                return self.cisis1660
        else:
            return self.cisis1030

    def version(self, mst_filename):
        if self.cisis1030.is_readable(mst_filename):
            return '1030'
        elif self.cisis1660.is_readable(mst_filename):
            return '1660'

    def convert1660to1030(self, mst_filename):
        if os.path.isfile(mst_filename + '.mst'):
            name = self.temp_dir + '/' + os.path.basename(mst_filename)
            self.cisis1660.mst2iso(mst_filename, name)
            self.cisis1030.iso2mst(name, mst_filename)

    def crunchmf(self, mst_filename, wmst_filename):
        self.cisis(mst_filename).crunchmf(mst_filename, wmst_filename)

    def id2i(self, id_filename, mst_filename):
        self.cisis(mst_filename).id2i(id_filename, mst_filename)

    def append(self, src, dest):
        self.cisis(src).append(src, dest)

    def create(self, src, dest):
        self.cisis(src).append(src, dest)

    def append_id_to_master(self, id_filename, mst_filename, reset):
        self.cisis(mst_filename).append_id_to_master(id_filename, mst_filename, reset)

    def i2id(self, mst_filename, id_filename):
        self.cisis(mst_filename).i2id(mst_filename, id_filename)

    def mst2iso(self, mst_filename, iso_filename):
        self.cisis(mst_filename).mst2iso(mst_filename, iso_filename)

    def iso2mst(self, iso_filename, mst_filename):
        self.cisis(mst_filename).iso2mst(iso_filename, mst_filename)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        self.cisis(src_mst_filename).copy_record(src_mst_filename, mfn, dest_mst_filename)

    def modify_records(self, mst_filename, proc):
        self.cisis(mst_filename).modify_records(mst_filename, proc)

    def find_record(self, mst_filename, expression):
        return self.cisis(mst_filename).find_record(mst_filename, expression)

    def new(self, mst_filename):
        self.cisis1030.new(mst_filename)

    def search(self, mst_filename, expression, result_filename):
        self.cisis(mst_filename).search(mst_filename, expression, result_filename)

    def generate_indexes(self, mst_filename, fst_filename, inverted_filename):
        self.cisis(mst_filename).generate_indexes(mst_filename, fst_filename, inverted_filename)


class IsisDAO(object):

    def __init__(self, cisis):
        self.cisis = cisis

    def save_records(self, records, db_filename, fst_filename=None):
        id_file = mkdtemp().replace('\\', '/') + '/' + os.path.basename(db_filename) + '.id'
        IDFile().save(id_file, records)
        self.cisis.id2i(id_file, db_filename)
        os.unlink(id_file)
        self.update_indexes(db_filename, fst_filename)

    def update_indexes(self, db_filename, fst_filename):
        if fst_filename is not None:
            self.cisis.generate_indexes(db_filename, fst_filename, db_filename)

    def append_records(self, records, db_filename, fst_filename=None):
        path = os.path.dirname(db_filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        id_temp = mkdtemp().replace('\\', '/') + '/' + os.path.basename(db_filename) + '.id'
        IDFile().save(id_temp, records)
        self.cisis.append_id_to_master(id_temp, db_filename, False)
        os.unlink(id_temp)
        self.update_indexes(db_filename, fst_filename)

    def save_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.id2i(id_filename, db_filename)
        self.update_indexes(db_filename, fst_filename)

    def append_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.append_id_to_master(id_filename, db_filename, False)
        self.update_indexes(db_filename, fst_filename)

    def get_records(self, db_filename, expr=None):
        temp_file = None
        if expr is None:
            base = db_filename
        else:
            temp_file = NamedTemporaryFile(delete=False)
            base = temp_file.name
            self.cisis.search(db_filename, expr, base)

        id_filename = base + '.id'

        self.cisis.i2id(base, id_filename)
        r = IDFile().read(id_filename)
        if len(r) > 0:
            if temp_file is not None:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            try:
                os.unlink(id_filename)
            except:
                pass
        return r

    def get_id_records(self, id_filename):
        return IDFile().read(id_filename)

    def save_id(self, id_filename, records, content_formatter=None):
        IDFile(content_formatter).save(id_filename, records)
