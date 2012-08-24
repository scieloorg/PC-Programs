import os.path

class ISSN_Table:
    def __init__(self, filename):
        c = []
        self.issn_list = {}
        if os.path.exists(filename):

            f = open(filename, 'r')
            c = f.readlines()
            f.close()
        
        for line in c:
            issn, journal_title, location, status = line.strip('\n').split('|')
            key = self.normalize_text(journal_title)
            loc = self.normalize_text(location)
            if not key in self.issn_list.keys():
                self.issn_list[key] = {}
            if loc == '':
                loc = 'ND'
            self.issn_list[key][loc] = (issn, journal_title, location, status)

    
    def normalize_text(self, text):
        j = text.upper()

        j = [ c for c in j if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' ]
        j = ''.join(j)
        return j

    def return_issn_and_title(self, journal_title, local = ''):
        j = self.normalize_text(journal_title)

        issn = ''
        title = ''
        if j in self.issn_list.keys():
            found = self.issn_list[j]
            if len(found) == 0:
                issn = ''
            elif len(found) == 1:
                r = found.values()

                issn = r[0][0]
                title = r[0][1]
            else:
                if local != '':
                    loc  = self.normalize_text(location)
                    if loc in found.keys():
                        issn = found[loc][0]
                        title = found[loc][1]
            if len(issn) != 9:
                issn = ''
        return issn