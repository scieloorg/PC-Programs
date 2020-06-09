# coding=utf-8

from prodtools import _

from prodtools.validations import article_data_reports


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


class RegisteredArticles(dict):

    def __init__(self, registered_articles):
        dict.__init__(self, registered_articles)

    def registered_titles_and_authors(self, article):
        similar_items = {}
        for name, registered in self.items():
            comparison = article_data_reports.ArticlesComparison(registered, article)
            if comparison.are_similar:
                similar_items.update({name: registered})
        return similar_items
