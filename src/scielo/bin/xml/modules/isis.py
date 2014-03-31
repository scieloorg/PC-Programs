# coding=utf-8


import os
from tempfile import mkdtemp

from xml_utils import normalize_space, convert_using_htmlparser


class IDFile(object):

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
        r = '!ID ' + i[-6:] + '\n'
        if record is not None:
            for tag_i in sorted([int(s) for s in record.keys()]):
                tag = str(tag_i)
                occs = record[tag]
                s = ''
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
            return '!v' + tag + '!' + convert_using_htmlparser(normalize_space(value)) + '\n'
        else:
            return ''

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

    def save(self, filename, records):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        f = open(filename, 'w')
        content = self._format_file(records)
        try:
            f.write(self._iso(content))
        except Exception as e:
            print(e)
            for line in content.split('\n'):
                try:
                    f.write(line + '\n')
                except:
                    r = ''
                    for c in line:
                        try:
                            f.write(self._iso(c))
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

    def _iso(self, content):
        if type(content) is unicode:
            try:
                iso = content.encode('iso-8859-1', 'replace')
            except:
                try:
                    iso = content.encode('iso-8859-1', 'xmlcharrefreplace')
                except:
                    iso = content.encode('iso-8859-1', 'ignore')
        else:
            iso = content
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
