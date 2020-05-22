# coding=utf-8

import os
import html

from tempfile import mkdtemp, NamedTemporaryFile

from prodtoos.utils import fs_utils
from prodtoos.utils import encoding
from prodtoos.utils import system


PRESERVECIRC = '[PRESERVECIRC]'


def remove_break_lines_characters(content):
    content = content or ""
    return ' '.join(content.split())


def format_value(content):
    """
    Formata o valor de um subcampo ou campo sem subcampo
    """
    return remove_break_lines_characters(
        content).strip().replace('^', PRESERVECIRC)


class IDFile(object):

    MAX_DIGITS_QTD = 6
    VALID_ID_RANGE = range(1, 10**MAX_DIGITS_QTD)

    def __init__(self, content_formatter=None):
        self.content_formatter = content_formatter

    def _format_file(self, records):
        r = []
        index = 0
        for item in records:
            index += 1
            r.append(self._format_id(index) + self._format_record(item))
        return "".join(r)

    def _format_id(self, index):
        """
        Cria o ID do registro
        """
        if index in self.VALID_ID_RANGE:
            return '!ID {}\n'.format(str(index).zfill(self.MAX_DIGITS_QTD))
        raise IndexError("IDFile._format_id: {} is out of range".format(index))

    def _format_record(self, record):
        """
        Formata o registro
        """
        if record:
            items = []
            for tag_i in sorted([int(s) for s in record.keys()]):
                tag = str(tag_i)
                items.extend(self._tag_data(tag, record[tag]))
            result = "".join(items)
            if self.content_formatter:
                result = self.content_formatter(result)
            return result
        return ""

    def _tag_data(self, tag, data):
        """
        Cria os campos com respectivos conteúdos
        """
        if not data:
            return []
        occs = []
        if not isinstance(data, list):
            data = [data]
        for item in data:
            occs.append(self._tag_occ(tag, item))
        return occs

    def _tag_occ(self, tag, data):
        """
        Cria cada ocorrência de um dado campo
        """
        if not data:
            return ""
        try:
            data = {"_": data + ""}
        except TypeError:
            if not isinstance(data, dict):
                raise TypeError("IDFile.tag_occ expects dict or str")
        return self._tag_content(tag, self._format_subfields(data))

    def _format_subfield(self, subf, subf_value):
        if subf_value and subf in 'abcdefghijklmnopqrstuvwxyz123456789':
            return '^' + subf + format_value(subf_value)
        return ""

    def _format_subfields(self, subf_and_value_list):
        first = format_value(subf_and_value_list.get('_') or "")
        values = [self._format_subfield(k, v)
                  for k, v in subf_and_value_list.items()]
        value = "".join(sorted(values))
        return first + value

    def _tag_content(self, tag, value):
        if not 0 < int(tag) <= 999:
            raise ValueError("IDFile.tag_content expects tag <= 999")
        if not value:
            return ""
        return '!v{}!{}\n'.format(tag.zfill(3), value)

    def _get_field_data(self, field_content):
        subfields = field_content.split("^")
        subfields = [c.replace(PRESERVECIRC, "^") for c in subfields]

        if len(subfields) == 1:
            # sem subcampos
            return subfields[0]
        # com subcampos
        d = {}
        if subfields[0]:
            d.update({"_": subfields[0]})
        for subf in subfields[1:]:
            d.update({subf[0]: subf[1:]})
        return d

    def _get_record_data(self, record):
        record_content = record[6:]
        fields = record_content.split("\n!v")[1:]
        data = {}
        for field in fields:
            field_tag, field_content = field.strip().split("!")
            field_tag = str(int(field_tag))
            field_data = self._get_field_data(field_content)
            data[field_tag] = data.get(field_tag, [])
            data[field_tag].append(field_data)

        for tag, tag_content in data.items():
            if len(tag_content) == 1:
                data[tag] = tag_content[0]
        return data

    def read(self, filename):
        rec_list = []
        iso_content = fs_utils.read_file(filename, 'iso-8859-1')
        utf8_content = encoding.decode(iso_content)
        utf8_content = html.unescape(utf8_content)
        utf8_content = utf8_content.replace("\\^", PRESERVECIRC)

        records = utf8_content.split('!ID ')
        for record in records[1:]:
            data = self._get_record_data(record)
            rec_list.append(data)
        return rec_list

    def write(self, filename, records):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        content = self._format_file(records)
        content = html.unescape(content)

        content = content.replace(PRESERVECIRC, "\\^")

        # converterá a entidades, os caracteres utf-8 que não tem
        # correspondencia em iso-8859-1
        content = encoding.encode(content, "iso-8859-1")
        content = encoding.decode(content, "iso-8859-1")

        try:
            fs_utils.write_file(filename, content, 'iso-8859-1')
        except (UnicodeError, IOError, OSError) as e:
            print("Nao foi possivel escrever o arquivo {}: {}".format(
                filename, str(e)))


class CISIS(object):

    def __init__(self, cisis_path):
        self.cisis_path = None
        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path

    @property
    def is_available(self):
        cmd = self.cisis_path + '/mx what > ./status'
        system.run_command(cmd)
        content = fs_utils.read_file('./status')
        return None if content is None else content.startswith('CISIS')

    def crunchmf(self, mst_filename, wmst_filename):
        cmd = self.cisis_path + '/crunchmf ' + mst_filename + ' ' + wmst_filename
        system.run_command(cmd)

    def id2i(self, id_filename, mst_filename):
        cmd = self.cisis_path + '/id2i ' + id_filename + ' create=' + mst_filename
        system.run_command(cmd)

    def append(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + '  append=' + dest + ' now -all'
        system.run_command(cmd)

    def create(self, src, dest):
        cmd = self.cisis_path + '/mx ' + src + ' create=' + dest + ' now -all'
        system.run_command(cmd)

    def append_id_to_master(self, id_filename, mst_filename, reset):
        if reset:
            self.id2i(id_filename, mst_filename)
        else:
            temp = id_filename.replace('.id', u'')
            self.id2i(id_filename, temp)
            self.append(temp, mst_filename)
            try:
                fs_utils.delete_file_or_folder(temp + '.mst')
                fs_utils.delete_file_or_folder(temp + '.xrf')
            except:
                pass

    def i2id(self, mst_filename, id_filename):
        cmd = self.cisis_path + '/i2id ' + mst_filename + ' > ' + id_filename
        system.run_command(cmd)

    def mst2iso(self, mst_filename, iso_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' iso=' + iso_filename + ' now -all'
        system.run_command(cmd)

    def iso2mst(self, iso_filename, mst_filename):
        cmd = self.cisis_path + '/mx iso=' + iso_filename + ' create=' + mst_filename + ' now -all'
        system.run_command(cmd)

    def copy_record(self, src_mst_filename, mfn, dest_mst_filename):
        cmd = self.cisis_path + '/mx ' + src_mst_filename + ' from=' + mfn + ' count=1 ' + ' append=' + dest_mst_filename + ' now -all'
        system.run_command(cmd)

    def modify_records(self, mst_filename, proc):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "proc=' + proc + '" copy=' + mst_filename + ' now -all'
        system.run_command(cmd)

    def find_record(self, mst_filename, expression):
        r = mst_filename + expression
        cmd = self.cisis_path + '/mx ' + mst_filename + ' "bool=' + expression + '"  lw=999 "pft=mfn/" now > ' + r
        system.run_command(cmd)
        return fs_utils.read_file_lines(r, 'iso-8859-1')

    def new(self, mst_filename):
        cmd = self.cisis_path + '/mx null count=0 create="' + mst_filename + '" now -all'
        system.run_command(cmd)

    def search(self, mst_filename, expression, result_filename):
        fs_utils.delete_file_or_folder(result_filename + '.mst')
        fs_utils.delete_file_or_folder(result_filename + '.xrf')
        cmd = self.cisis_path + '/mx btell=0 ' + mst_filename + ' "bool=' + expression + '"  lw=999 append=' + result_filename + ' now -all'
        system.run_command(cmd)

    def generate_indexes(self, mst_filename, fst_filename, inverted_filename):
        cmd = self.cisis_path + '/mx ' + mst_filename + ' fst=@' + fst_filename + ' fullinv=' + inverted_filename
        system.run_command(cmd)

    def is_readable(self, mst_filename):
        s = u''
        if os.path.isfile(mst_filename + '.mst'):
            temp_file = NamedTemporaryFile(delete=False)
            temp_file.close()

            cmd = self.cisis_path + '/mx ' + mst_filename + ' +control now > ' + temp_file.name.replace('\\', '/')
            system.run_command(cmd)
            if os.path.isfile(temp_file.name):
                s = fs_utils.read_file(temp_file.name)
                try:
                    fs_utils.delete_file_or_folder(temp_file.name)
                except:
                    encoding.debugging('dbm_isis.is_readable()', os.path.isfile(temp_file.name))
        return len(s) > 0


class UCISIS(object):

    def __init__(self, cisis1030, cisis1660):
        self.cisis1030 = cisis1030
        self.cisis1660 = cisis1660

    @property
    def is_available(self):
        return self.cisis1660.is_available or self.cisis1030.is_available

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
            temp_file = NamedTemporaryFile(delete=False)
            temp_file.close()
            self.cisis1660.mst2iso(mst_filename, temp_file.name)
            self.cisis1030.iso2mst(temp_file.name, mst_filename)
            fs_utils.delete_file_or_folder(temp_file.name)

    def crunchmf(self, mst_filename, wmst_filename):
        self.cisis(mst_filename).crunchmf(mst_filename, wmst_filename)

    def id2i(self, id_filename, mst_filename):
        self.cisis(mst_filename).id2i(id_filename, mst_filename)

    def append(self, src, dest):
        self.cisis(src).append(src, dest)

    def create(self, src, dest):
        self.cisis(src).create(src, dest)

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
        self.idfile = IDFile()

    def save_records(self, records, db_filename, fst_filename=None):
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.close()
        self.idfile.write(temp_file.name, records)
        self.cisis.id2i(temp_file.name, db_filename)
        fs_utils.delete_file_or_folder(temp_file.name)
        self.update_indexes(db_filename, fst_filename)

    def update_indexes(self, db_filename, fst_filename):
        if fst_filename is not None:
            self.cisis.generate_indexes(db_filename, fst_filename, db_filename)

    def append_records(self, records, db_filename, fst_filename=None):
        path = os.path.dirname(db_filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.close()
        self.idfile.write(temp_file.name, records)
        self.cisis.append_id_to_master(temp_file.name, db_filename, False)
        fs_utils.delete_file_or_folder(temp_file.name)
        self.update_indexes(db_filename, fst_filename)

    def save_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.id2i(id_filename, db_filename)
        self.update_indexes(db_filename, fst_filename)

    def append_id_records(self, id_filename, db_filename, fst_filename=None):
        self.cisis.append_id_to_master(id_filename, db_filename, False)
        self.update_indexes(db_filename, fst_filename)

    def get_records(self, db_filename, expr=None):
        temp_dir = None
        if expr is None:
            base = db_filename
        else:
            temp_dir = mkdtemp().replace('\\', '/')
            base = temp_dir + '/' + os.path.basename(db_filename)
            self.cisis.search(db_filename, expr, base)

        r = []
        id_filename = base + '.id'
        if os.path.isfile(base + '.mst'):
            self.cisis.i2id(base, id_filename)
            r = self.idfile.read(id_filename)

        if temp_dir is not None:
            try:
                fs_utils.delete_file_or_folder(temp_dir)
            except:
                pass
        try:
            fs_utils.delete_file_or_folder(id_filename)
        except:
            pass
        return r

    def get_id_records(self, id_filename):
        return self.idfile.read(id_filename)

    def save_id(self, id_filename, records, content_formatter=None):
        if content_formatter:
            IDFile(content_formatter).write(id_filename, records)
        else:
            self.idfile.write(id_filename, records)


class IsisDB(object):

    def __init__(self, cisis, db_filename, fst_filename):
        self.cisis = cisis
        self.db_filename = db_filename
        self.fst_filename = fst_filename
        self.idfile = IDFile()

    def save_records(self, records):
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.close()
        self.idfile.write(temp_file.name, records)
        self.cisis.id2i(temp_file.name, self.db_filename)
        fs_utils.delete_file_or_folder(temp_file.name)
        self.update_indexes()

    def update_indexes(self):
        if self.fst_filename is not None:
            self.cisis.generate_indexes(self.db_filename, self.fst_filename, self.db_filename)

    def append_records(self, records):
        path = os.path.dirname(self.db_filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.close()
        self.idfile.write(temp_file.name, records)
        self.cisis.append_id_to_master(temp_file.name, self.db_filename, False)
        fs_utils.delete_file_or_folder(temp_file.name)
        self.update_indexes()

    def save_id_records(self, id_filename):
        self.cisis.id2i(id_filename, self.db_filename)
        self.update_indexes()

    def append_id_records(self, id_filename):
        self.cisis.append_id_to_master(id_filename, self.db_filename, False)
        self.update_indexes()

    def get_records(self, expr=None):
        temp_dir = None
        if expr is None:
            base = self.db_filename
        else:
            temp_dir = mkdtemp().replace('\\', '/')
            base = temp_dir + '/' + os.path.basename(self.db_filename)
            self.cisis.search(self.db_filename, expr, base)

        r = []
        id_filename = base + '.id'
        if os.path.isfile(base + '.mst'):
            self.cisis.i2id(base, id_filename)
            r = self.idfile.read(id_filename)

        if temp_dir is not None:
            try:
                fs_utils.delete_file_or_folder(temp_dir)
            except:
                pass
        if os.path.isfile(id_filename):
            fs_utils.delete_file_or_folder(id_filename)

        return r

    def get_id_records(self, id_filename):
        return self.idfile.read(id_filename)

    def save_id(self, id_filename, records, content_formatter=None):
        if content_formatter:
            IDFile(content_formatter).write(id_filename, records)
        else:
            self.idfile.write(id_filename, records)

