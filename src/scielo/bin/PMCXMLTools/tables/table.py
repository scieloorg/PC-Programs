class Table:
    def __init__(self, filename):
        f = open(filename, 'r')
        content = f.readlines()
        f.close()

        self.dict = {}

        for row in content:
            cols = row.replace('\n', '').split('|')
            self.dict[cols[0]] = cols

    