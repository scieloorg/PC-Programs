import os


class Workarea(object):

    def __init__(self, filename):
        self.filename = filename
        self.dirname = os.path.dirname(filename)
        self.basename = os.path.basename(filename)
        self.name, self.ext = os.path.splitext(self.basename)
        self.new_name = self.name

    @property
    def new_filename(self):
        return self.dirname + '/' + self.new_name

    def extensions(self, filename):
        return list(set([f[f.rfind('.'):] for f in os.listdir(self.dirname) if f.startswith(filename + '.')]))

    def name_with_extension(self, href, new_href):
        if '.' not in new_href:
            extensions = self.extensions(href)
            if len(extensions) > 1:
                extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
            if len(extensions) > 0:
                new_href += extensions[0]
        return new_href

    @property
    def article_files(self):
        r = [item for item in os.listdir(self.dirname) if (item.startswith(self.name + '-') or item.startswith(self.name + '.')) and not item.endswith('.xml')]
        suffixes = ['t', 'f', 'e', 'img', 'image']
        suffixes.extend(['-'+s for s in suffixes])
        for suffix in suffixes:
            r += [item for item in os.listdir(self.dirname) if item.startswith(self.name + suffix)]
        r = list(set(r))
        r = [item for item in r if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
        return sorted(r)

    @property
    def sorted_article_files(self):
        files = {}
        for f in self.article_files:
            name, ext = os.path.splitext(f)
            if name not in files.keys():
                files[name] = []
            files[name].append(ext)
        return files
