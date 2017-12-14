# coding=utf-8

import os
import shutil

from ...generics import fs_utils
from ...generics import encoding
from . import symbols


class SGMLHTMLDocment(object):

    def __init__(self, xml_name, html_filename):
        self.xml_name = xml_name
        self.html_filename = html_filename
        self.html_path = os.path.dirname(self.html_filename)
        self.html_basename = os.path.basename(self.html_filename)
        self.html_name, ext = os.path.splitext(self.html_basename)
        self._html_content = None

    @property
    def html_content(self):
        if self._html_content is None:
            self._html_content = fs_utils.read_file(self.html_filename, encoding.SYS_DEFAULT_ENCODING) or ''
        return self._html_content

    @property
    def html_img_path(self):
        path = None
        for item in os.listdir(self.html_path):
            if os.path.isdir(self.html_path + '/' + item) and item.startswith(self.html_name):
                path = self.html_path + '/' + item
                break
        if path is None:
            path = self._alternative_html_img_path(self.html_path, self.html_name)
        if path is None:
            path = self.html_path
        return path

    def _alternative_html_img_path(self):
        #name_image001
        new_html_folder = self.html_path + '/' + self.html_name + '_arquivosalt'
        if not os.path.isdir(new_html_folder):
            os.makedirs(new_html_folder)
        for item in os.listdir(self.html_path):
            if os.path.isfile(self.html_path + '/' + item) and item.startswith(self.html_name + '_image'):
                new_name = item[len(self.html_name)+1:]
                shutil.copyfile(self.html_path + '/' + item, new_html_folder + '/' + new_name)
        return new_html_folder

    @property
    def img_files(self):
        return os.listdir(self.html_img_path)

    @property
    def img_href_items(self):
        return [item for item in self.unknown_href_items if item != 'None']

    @property
    def unknown_href_items(self):
        """
        [graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        """
        html_content = self.html_content
        if 'href=&quot;?' in html_content:
            html_content = html_content.replace('href=&quot;?', 'href="?')
        """
        if '“' in html_content:
            html_content = html_content.replace('“', '"')
        if '”' in html_content:
            html_content = html_content.replace('”', '"')
        """
        _items = html_content.replace('href="?', 'href="?--~BREAK~FIXHREF--FIXHREF').split('--~BREAK~FIXHREF--')
        items = [item for item in _items if item.startswith('FIXHREF')]
        img_src = []
        for item in items:
            if 'src="' in item:
                src = item[item.find('src="') + len('src="'):]
                src = src[0:src.find('"')]
                if '/' in src:
                    src = src[src.find('/') + 1:]
                if len(src) > 0:
                    img_src.append(src)
            else:
                img_src.append('None')
        return img_src

    def get_fontsymbols(self):
        r = []
        html_content = self.html_content
        if '[fontsymbol]' in html_content.lower():
            for style in ['italic', 'sup', 'sub', 'bold']:
                html_content = html_content.replace('<' + style + '>', '[' + style + ']')
                html_content = html_content.replace('</' + style + '>', '[/' + style + ']')

            html_content = html_content.replace('[fontsymbol]'.upper(), '[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]'.upper(), '[/fontsymbol]')
            html_content = html_content.replace('[fontsymbol]', '~BREAK~[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]', '[/fontsymbol]~BREAK~')

            html_fontsymbol_items = [item for item in html_content.split('~BREAK~') if item.startswith('[fontsymbol]')]
            for item in html_fontsymbol_items:
                item = item.replace('[fontsymbol]', '').replace('[/fontsymbol]', '')
                item = item.replace('<', '~BREAK~<').replace('>', '>~BREAK~')
                item = item.replace('[', '~BREAK~[').replace(']', ']~BREAK~')
                parts = [part for part in item.split('~BREAK~') if not part.endswith('>') and not part.startswith('<')]

                new = ''
                for part in parts:
                    if part.startswith('['):
                        new += part
                    else:

                        for c in part:
                            _c = c.strip()
                            if _c.isdigit() or _c == '':
                                n = c
                            else:
                                try:
                                    n = symbols.get_symbol(c)
                                except:
                                    n = '?'
                            new += n
                for style in ['italic', 'sup', 'sub', 'bold']:
                    new = new.replace('[' + style + ']', '<' + style + '>')
                    new = new.replace('[/' + style + ']', '</' + style + '>')
                r.append(new)
        return r
