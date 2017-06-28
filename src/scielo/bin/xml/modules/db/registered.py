# coding=utf-8

from ..__init__ import _

from . import xc_models
from ..validations import package_validations


class RegisteredIssueData(object):

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.articles_db_manager = None
        self.issue_error_msg = None
        self.issue_models = None
        self.issue_files = None
        self.serial_path = None

    def get_data(self, pkgissuedata):
        if self.db_manager is None:
            journals_list = xc_models.JournalsList()
            pkgissuedata.journal = journals_list.get_journal(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
            pkgissuedata.journal_data = journals_list.get_journal_data(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
        else:
            acron_issue_label, self.issue_models, self.issue_error_msg, pkgissuedata.journal, pkgissuedata.journal_data = self.db_manager.get_registered_data(pkgissuedata.pkg_journal_title, pkgissuedata.pkg_issue_label, pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn)
            ign, pkgissuedata._issue_label = acron_issue_label.split(' ')
            if self.issue_error_msg is None:
                self.issue_files = self.db_manager.get_issue_files(self.issue_models)
                self.articles_db_manager = xc_models.ArticlesManager(self.db_manager.db_isis, self.issue_files)
        return pkgissuedata

    @property
    def registered_articles(self):
        articles = {}
        if self.articles_db_manager is not None:
            articles = registered_issue_data.articles_db_manager.registered_articles
        return articles


class RegisteredArticles(dict):

    def __init__(self, registered_articles):
        dict.__init__(self, registered_articles)

    def registered_item(self, name, article):
        found = None
        registered = self.get(name)
        if registered is not None:
            comparison = package_validations.ArticlesComparison(registered, article)
            if registered.order == article.order and comparison.are_similar:
                found = registered
        return found

    def registered_order(self, order):
        return [reg_name for reg_name, reg in self.items() if reg.order == order]

    def registered_titles_and_authors(self, article):
        similar_items = []
        for name, registered in self.items():
            comparison = package_validations.ArticlesComparison(registered, article)
            if comparison.are_similar:
                similar_items.append(name)
        return similar_items

    def search_articles(self, name, article):
        registered = self.registered_item(name, article)
        registered_titaut = registered
        registered_name = registered
        registered_order = registered
        if registered is None:
            matched_titaut_article_names = self.registered_titles_and_authors(article)
            matched_order_article_names = self.registered_order(article.order)
            registered_titaut = self.registered_items_by_names(matched_titaut_article_names)
            registered_order = self.registered_items_by_names(matched_order_article_names)
            registered_name = self.get(name)
        return (registered_titaut, registered_name, registered_order)

    def registered_items_by_names(self, found_names):
        if len(found_names) == 0:
            return None
        elif len(found_names) == 1:
            return self.get(found_names[0])
        else:
            return {name: self.get(name) for name in found_names}

    def analyze_registered_articles(self, name, registered_titaut, registered_name, registered_order):
        actions = None
        conflicts = None
        old_name = None
        #print('analyze_registered_articles')
        #print([registered_titaut, registered_name, registered_order])
        #print('-')
        if registered_titaut is None and registered_order is None and registered_name is None:
            actions = 'add'
        elif all([registered_titaut, registered_order, registered_name]):
            if id(registered_titaut) == id(registered_order) == id(registered_name):
                actions = 'update'
            elif id(registered_titaut) == id(registered_name):
                # titaut + name != order
                # rejeitar
                conflicts = {_('registered article retrieved by the order'): registered_order, _('registered article retrieved by title/authors/name'): registered_titaut}
            elif id(registered_titaut) == id(registered_order):
                # titaut + order != name
                # rejeitar
                conflicts = {'registered article retrieved by title/authors/order': registered_order, _('registered article retrieved by name'): registered_name}
            elif id(registered_name) == id(registered_order):
                # order + name != titaut
                # rejeitar
                conflicts = {'registered article retrieved by name/order': registered_order, _('registered article retrieved by title/authors'): registered_titaut}
            else:
                # order != name != titaut
                # rejeitar
                conflicts = {_('name'): registered_name, _('registered article retrieved by the order'): registered_order, _('title/authors'): registered_titaut}
        elif all([registered_titaut, registered_order]):
            if id(registered_titaut) == id(registered_order):
                if registered_order.is_ex_aop:
                    actions = 'reject'
                else:
                    actions = 'name change'
                    old_name = registered_titaut.xml_name
            else:
                conflicts = {_('registered article retrieved by the order'): registered_order, _('title/authors'): registered_titaut}
        elif all([registered_titaut, registered_name]):
            if id(registered_titaut) == id(registered_name):
                if registered_name.is_ex_aop:
                    actions = 'reject'
                else:
                    actions = 'order change'
            else:
                conflicts = {_('registered article retrieved by title/authors'): registered_titaut, _('registered article retrieved by name'): registered_name}
        elif all([registered_order, registered_name]):
            if id(registered_order) == id(registered_name):
                # titulo autores etc muito diferentes
                conflicts = {_('registered article retrieved by the order'): registered_order}
            else:
                conflicts = {_('registered article retrieved by the order'): registered_order, _('registered article retrieved by name'): registered_name}
        elif registered_titaut is not None:
            # order e name nao encontrados; order testar antes de atualizar;
            if registered_titaut.is_ex_aop:
                actions = 'reject'
            else:
                actions = 'order change, name change'
                old_name = registered_titaut.xml_name
        elif registered_name is not None:
            conflicts = {_('registered article retrieved by name'): registered_name}
        elif registered_order is not None:
            conflicts = {_('registered article retrieved by the order'): registered_order}
        return (actions, old_name, conflicts)
