# coding=utf-8


class RegisteredIssue(object):

    def __init__(self):
        self.articles_db_manager = None
        self.issue_error_msg = None
        self.issue_models = None
        self.issue_files = None

    @property
    def registered_articles(self):
        if self.articles_db_manager is not None:
            return self.articles_db_manager.registered_articles
        return {}
