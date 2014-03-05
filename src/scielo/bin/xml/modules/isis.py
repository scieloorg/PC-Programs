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

                if occs is str:
                    r += self.tagged(tag, occs)
                elif occs is list:
                    for occ in occs:
                        if occ is str:
                            r += self.format(tag, occ)
                        elif occ is dict:
                            value = ''
                            first = ''
                            for k, v in occ.items():
                                if v != '':
                                    if k == '_':
                                        first = k + v
                                    else:
                                        value += '^' + k + v
                            r += self._tagged(tag, first + value)
        return r

    def _tagged(self, tag, value):
        if value is not None:
            tag = '000' + tag
            tag = tag[-3:]
            return '!v' + tag + '!' + value + '\n'
        return ''

    def read(self, filename):
        f = open(filename, 'r')
        r = f.readlines()
        f.close()

        records = []
        record = {}
        for line in r:
            s = line.replace('\n', '').replace('\r', '')
            if '!ID ' in s:
                if len(record) > 0:
                    records.append(record)
                record = {}
            else:
                ign, tag, content = s.split('!')
                if not tag in record.keys():
                    record[tag] = []
                content = content.replace('^', 'BREAKSUBF^')
                subfields = content.split('BREAKSUBF')
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
        if len(record) > 0:
            records.append(record)
        return records

    def save(self, filename, records):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        f = open(filename, 'w')
        f.write(self._format_file(records))
        f.close()


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
        from tempfile import mkstemp

        _, temp = mkstemp()
        self.id2i(id_filename, temp)

        if reset:
            self.create('null count=0', mst_filename)
        self.append(temp, mst_filename)
        os.remove(temp)

    def i2id(self, mst_filename, id_filename):
        cmd = self.cisis_path + '/i2id ' + mst_filename + ' > ' + id_filename 
        os.system(cmd)

    def mst2iso(self, mst_filename, iso_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' iso=' + iso_filename + ' now -all' 
        os.system(cmd)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        os.system(cmd)

    def find_record(self, mst_filename, expression):
        r = mst_filename + expression
        cmd = self.cisis_path + '/mx ' + mst_filename + ' bool="' + expression + '"  lw=999 "pft=mfn/" now > ' + r

        os.system(cmd)
        f = open(r, 'r')
        c = f.readlines()
        f.close()

        a = []
        for l in c:
            a.append(l.replace('\n', ''))

        return a
