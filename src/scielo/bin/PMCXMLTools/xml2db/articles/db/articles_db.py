class DBArticles:
    def __init__(self, db_manager, tracker):
        self.db_manager = db_manager
        self.tracker = tracker
        
    def create_table(self, table_name, filename):
        self.db_manager.create_table(table_name, filename)

    def db2json(self, table_name):
        return self.db_manager.db2json(table_name)
   

    def put_on_the_shelf(self, issue, package):
        return self.db_manager.save_issue(issue, package)

