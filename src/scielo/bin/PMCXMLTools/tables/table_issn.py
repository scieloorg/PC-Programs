import os.path

class ISSN_Table:
    def __init__(self, match_filename = 'inputs/issn_and_titles.seq', normalized_filename = 'inputs/issn_norm_titles.seq'):
        
        self.issn_and_journal_list = {}
        self.normalized_titles = {}

        c = []
        if os.path.exists(match_filename):
            f = open(match_filename, 'r')
            c = f.readlines()
            f.close()
        
        for line in c:
            issn, journal_title = line.strip('\n').split('|')
            self.issn_and_journal_list[journal_title] = issn

        c = []
        if os.path.exists(normalized_filename):
            f = open(normalized_filename, 'r')
            c = f.readlines()
            f.close()
        for line in c:
            issn, journal_title = line.strip('\n').split('|')
            self.normalized_titles[issn] = journal_title

    
    def normalize_title(self, t):
        title = t.upper().replace('  ', ' ')
        chr_title = [ character for character in title if  character in ' ABCDEFGHIJKLMNOPQRSTUVWXYZ' ]
        return  ''.join(chr_title)


    def return_issn_and_normalized_title(self, journal_title, local = ''):
        j = self.normalize_title(journal_title)

        issn = ''
        title = ''
        if j in self.issn_and_journal_list.keys():
            issn = self.issn_and_journal_list[j]
            if issn in self.normalized_titles.keys():
                title = self.normalized_titles[issn]
        return (issn, title)

