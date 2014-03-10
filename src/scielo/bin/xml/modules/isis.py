# coding=utf-8


import os


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
            for tag, occs in record.items():
                print(tag)
                print(occs)
                s = ''
                if type(occs) is str:
                    s = self._tagged(tag, occs)
                elif type(occs) is list:
                        
                    s = ''
                    for occ in occs:
                        value = ''
                        first = ''
                        if type(occ) is str:
                            s += self._tagged(tag, occ)
                        elif type(occ) is dict:
                            
                            for k, v in occ.items():
                                if v is not None:
                                    if k == '_':
                                        first = v
                                    else:
                                        value += '^' + k + v
                            s += self._tagged(tag, first + value)
                print('s:')
                print(s)
                r += s
        return r

    def _tagged(self, tag, value):
        if value is not None:
            tag = '000' + tag
            tag = tag[-3:]
            return '!v' + tag + '!' + value + '\n'
        return ''

    def read(self, filename):
        f = open(filename, 'r')

        records = []
        record = {}
        for line in f.readlines():
            s = line.replace('\n', '').replace('\r', '')
            if '!ID ' in s:
                print(s)
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

        print('Loaded ' + str(len(records))) + ' issue records.'
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
                    for c in line:
                        try:
                            f.write(self._iso(c))
                        except:
                            f.write(' ')
                            print('Unable to write ' + c + ' of ' + line)
                    f.write('\n')
        f.close()

    def _iso(self, content):
        try:
            u = content.decode('utf-8', 'ignore')
            iso = u.encode('iso-8859-1')
        except:
            try:
                u = content.decode('ascii', 'ignore')
                iso = u.encode('iso-8859-1')
            except:
                iso = content
        return iso
        return iso


class CISIS(object):
    def __init__(self, cisis_path):
        cisis_path = cisis_path.replace('\\', '/')

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
        cmd = self.cisis_path + '/mx ' + src + '  create=' + dest + ' now -all'
        os.system(cmd)

    def id2mst(self, id_filename, mst_filename, reset):
        if reset:
            self.new(mst_filename)
        from tempfile import mkdtemp
        temp = mkdtemp() + '/f'
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

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        os.system(cmd)

    def modify_records(self, mst_filename, proc):
        import tempfile
        temp = tempfile.mkdtemp() + '/f'
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
        self.new(result_filename)
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "bool=' + expression + '"  lw=999 append=' + result_filename + ' now -all'
        os.system(cmd)

    def generate_index(self, mst_filename, fst_filename, inverted_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' fst=@' + fst_filename + '" fullinv=' + inverted_filename
        os.system(cmd)
