# coding=utf-8


import os
from tempfile import mkdtemp, NamedTemporaryFile

from utils import u_encode
from xml_utils import normalize_space, convert_entities_to_chars


class IDFile(object):

    def __init__(self):
        pass

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
        if record is not None:
            r = ''
            for tag_i in sorted([int(s) for s in record.keys()]):
                tag = str(tag_i)
                items = record[tag]
                r += self.tag_items(tag, items)
        return r

    def tag_items(self, tag, items):
        s = ''
        if type(items) is dict:
            s = self._tagged(tag, self._format_subfields(items))
        elif type(items) is list:
            for item in items:
                s += self.tag_items(tag, item)
        else:
            s = self._tagged(tag, items)
        return s

    def _format_subfields(self, subfields_and_values):
        first = ''
        value = ''
        for k, v in subfields_and_values.items():
            if v is not None:
                if k == '_':
                    first = v
                else:
                    if len(k) == 1 and k in 'abcdefghijklmnopqrstuvwxyz123456789':
                        value += '^' + k + v
        return first + value

    def _tagged(self, tag, value):
        if value is not None and value != '':
            tag = '000' + tag
            tag = tag[-3:]

            t1 = value
            t2 = convert_using_htmlparser(t1)

            return '!v' + tag + '!' + normalize_space(t2) + '\n'
        else:
            return ''

    def read(self, filename):
        rec_list = []
        record = {}
        for line in open(filename, 'r').readlines():
            s = line.replace('\n', '').replace('\r', '')
            if '!ID ' in s:
                if len(record) > 0:
                    rec_list.append(self.simplify_record(record))
                record = {}
            else:
                ign, tag, content = s.split('!')
                tag = str(int(tag[1:]))
                if not tag in record.keys():
                    record[tag] = []
                content = content.replace('^', 'BREAKSUBF^')
                subfields = content.split('BREAKSUBF')
                if len(subfields) == 1:
                    content = subfields[0]
                else:
                    content = {}
                    for subf in subfields:
                        if subf.startswith('^'):
                            c = subf[1:2]
                            v = subf[2:]
                        else:
                            c = '_'
                            v = subf
                        content[c] = v
                record[tag].append(content)

        # last record
        if len(record) > 0:
            rec_list.append(self.simplify_record(record))

        print('Loaded ' + str(len(rec_list))) + ' issue rec_list.'
        return rec_list

    def simplify_record(self, record):
        for tag, content in record.items():
            if len(content) == 1:
                record[tag] = content[0]
        return record

    def save(self, filename, records, data_encoding):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        content = self._format_file(records)
        if isinstance(content, unicode):
            unicode_content = content
        else:
            unicode_content = content.decode('utf-8')

        iso = u_encode(unicode_content, 'iso-8859-1')
        try:
            open(filename, 'w').write(iso)
        except Exception as e:
            print(e)


class OLDIDFile(object):

    def __init__(self):
        pass

    def _format_file(self, records):
        r = ''
        index = 0
        for item in records:
            index += 1
            r += self._format_record(index, item)
        return r

    def _format_record(self, index, record):
        i = '000000' + str(index)
        r = u'!ID ' + i[-6:] + '\n'

        if record is not None:
            for tag_i in sorted([int(s) for s in record.keys()]):
                tag = str(tag_i)
                occs = record[tag]

                s = u''
                if type(occs) is dict:
                    s = self._tagged(tag, self._format_subfields(occs))
                elif type(occs) is list:
                    for occ in occs:
                        if type(occ) is dict:
                            s += self._tagged(tag, self._format_subfields(occ))
                        else:
                            s += self._tagged(tag, occ)
                else:
                    s = self._tagged(tag, occs)

                r += s

        return r

    def _format_subfields(self, subfields_and_values):
        first = ''
        value = ''
        for k, v in subfields_and_values.items():
            if v is not None:
                if k == '_':
                    first = v
                else:
                    if len(k) == 1 and k in 'abcdefghijklmnopqrstuvwxyz123456789':
                        value += '^' + k + v
        return first + value

    def _tagged(self, tag, value):
        if value is not None and value != '':
            tag = '000' + tag
            tag = tag[-3:]

            t1 = value
            t2 = convert_using_htmlparser(t1)

            s = '!v' + tag + '!' + normalize_space(t2) + '\n'
            if type(s) is str:
                s = s.decode('utf-8')
            return s
        else:
            return u''

    def read(self, filename):
        f = open(filename, 'r')

        records = []
        record = {}
        for line in f.readlines():
            s = line.replace('\n', '').replace('\r', '')
            if type(s) is type(''):
                s = s.decode('iso-8859-1')

            if '!ID ' in s:
                if len(record) > 0:
                    records.append(self.simplify_record(record))

                record = {}
            else:
                ign, tag, content = s.split('!')
                tag = str(int(tag[1:]))
                if not tag in record.keys():
                    record[tag] = []
                content = content.replace('^', 'BREAKSUBF^')
                subfields = content.split('BREAKSUBF')
                if len(subfields) == 1:
                    content = subfields[0]
                else:
                    content = {}
                    for subf in subfields:
                        if subf.startswith('^'):
                            c = subf[1:2]
                            v = subf[2:]
                        else:
                            c = '_'
                            v = subf
                        content[c] = v
                record[tag].append(content)

        # last record
        if len(record) > 0:
            records.append(self.simplify_record(record))

        #print('Loaded ' + str(len(records))) + ' issue records.'
        f.close()
        return records

    def simplify_record(self, record):
        for tag, content in record.items():
            if len(content) == 1:
                record[tag] = content[0]
        return record

    def save(self, filename, records, data_encoding):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        f = open(filename, 'w')
        content = self._format_file(records)
        content = self._iso(content, data_encoding)
        try:
            f.write(content)
        except Exception as e:
            print(e)
            print(type(content))
            for line in content.split('\n'):
                try:
                    f.write(line + '\n')
                except:
                    r = ''
                    for c in line:
                        try:
                            f.write(c)
                        except Exception as e:
                            f.write('??')
                            print(type(c))

                            print('Unable to write ')
                            print(r)
                            print(e)
                            #print(content)
                        r += c
                    f.write('\n')
        f.close()

    def _iso(self, content, encoding):
        if type(content) is str:
            content = content.decode(encoding)
        iso = u_encode(content, 'iso-8859-1')

        return iso


class CISIS(object):

    def __init__(self, cisis_path):
        cisis_path = cisis_path.replace('\\', '/')
        self.temp_dir = mkdtemp().replace('\\', '/')
        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path
        else:
            print('Invalid cisis path: ' + cisis_path)

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

    def id2mst(self, id_filename, mst_filename, reset):
        if reset:
            self.new(mst_filename)
        
        temp = mkdtemp().replace('\\', '/') + '/f'
        self.id2i(id_filename, temp)
        self.append(temp, mst_filename)
        try:
            os.unlink(temp)
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
        f = open(r, 'r')
        c = f.readlines()
        f.close()

        a = []
        for l in c:
            a.append(l.replace('\n', ''))

        return a

    def new(self, mst_filename):
        cmd = self.cisis_path + '/mx null count=0 create="' + mst_filename + '" now -all'
        os.system(cmd)

    def search(self, mst_filename, expression, result_filename):
        if os.path.isfile(result_filename + '.mst'):
            os.unlink(result_filename + '.mst')
            os.unlink(result_filename + '.xrf')
        
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "bool=' + expression + '"  lw=999 append=' + result_filename + ' now -all'
        os.system(cmd)

    def generate_indexes(self, mst_filename, fst_filename, inverted_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' fst=@' + fst_filename + ' fullinv=' + inverted_filename
        print(cmd)
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

    def id2mst(self, id_filename, mst_filename, reset):
        if reset:
            self.cisis1030.id2mst(id_filename, mst_filename, reset)
        else:
            self.cisis(mst_filename).id2mst(id_filename, mst_filename, reset)

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
        IDFile().save(id_file, records, 'iso-8859-1')
        self.cisis.id2i(id_file, db_filename)
        os.unlink(id_file)
        self.update_indexes(db_filename, fst_filename)

    def update_indexes(self, db_filename, fst_filename):
        if fst_filename is not None:
            self.cisis.generate_indexes(db_filename, fst_filename, db_filename)

    def append_records(self, records, db_filename, fst_filename=None):
        id_temp = mkdtemp().replace('\\', '/') + '/' + os.path.basename(db_filename) + '.id'
        IDFile().save(id_temp, records, 'iso-8859-1')
        self.cisis.id2mst(id_temp, db_filename, False)
        os.unlink(id_temp)
        self.update_indexes(db_filename, fst_filename)

    def save_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.id2i(id_filename, db_filename)
        self.update_indexes(db_filename, fst_filename)

    def append_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.id2mst(id_filename, db_filename, False)
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
        if temp_file is not None:
            try:
                os.unlink(temp_file.name)
            except:
                print(temp_file.name)
        try:
            os.unlink(id_filename)
        except:
            print(id_filename)
        return r

    def save_id(self, id_filename, records):
        IDFile().save(id_filename, records)

