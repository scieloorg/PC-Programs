# coding=utf-8

from prodtools.db.registered import RegisteredArticles
from prodtools.reports import validation_status
from prodtools.validations import article_data_reports


ACTION_DELETE = 'delete'
ACTION_SOLVE_TITAUT_CONFLICTS = 'TITAUT_CONFLICTS'
ACTION_UPDATE = 'update'
ACTION_CHECK_ORDER_AND_NAME = 'CHECK_ORDER_AND_NAME'

HISTORY_REGISTERED = 'registered article'
HISTORY_PACKAGE = 'package'
HISTORY_DELETED = 'excluded article'
HISTORY_ACCEPTED = 'accepted'
HISTORY_SOLVED = 'solved'
HISTORY_REJECTED = 'rejected'

HISTORY_TITAUT_CONFLICTS = 'detected different titles/authors'
HISTORY_CHECK_ORDER_AND_NAME = 'need to check order and/or name'
HISTORY_PKG_ORDER_CONFLICTS = 'detected order conflict in package'
HISTORY_CREATED = 'created'
HISTORY_ORDER_AND_NAME_CONFLICTS = 'order and name conflicts'
HISTORY_ORDER_CHANGED = 'order changed'
HISTORY_UNMATCHED = 'unmatched data'
HISTORY_REPLACE = 'replace'
HISTORY_NAME_CHANGED = 'name changed'
HISTORY_REPLACED_BY = 'replaced by'


class MergedArticlesData(object):

    def __init__(self, merged_articles, is_db_generation):
        self.merged_articles = merged_articles
        self.ERROR_LEVEL_FOR_UNIQUE_VALUES = {'order': validation_status.STATUS_BLOCKING_ERROR, 'doi': validation_status.STATUS_BLOCKING_ERROR, 'elocation id': validation_status.STATUS_BLOCKING_ERROR, 'fpage-lpage-seq-elocation-id': validation_status.STATUS_ERROR}
        if not is_db_generation:
            self.ERROR_LEVEL_FOR_UNIQUE_VALUES['order'] = validation_status.STATUS_WARNING
        self.IGNORE_NONE = ['journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', ]
        self.EXPECTED_COMMON_VALUES_LABELS = ['journal-title', 'journal-id (nlm-ta)', 'e-ISSN', 'print ISSN', 'issue label', 'issue pub date', 'license']
        self.REQUIRED_DATA = ['journal-title', 'journal ISSN', 'publisher name', 'issue label', 'issue pub date', ]
        self.EXPECTED_UNIQUE_VALUE_LABELS = ['order', 'doi', 'elocation id', 'fpage-lpage-seq-elocation-id']

    @property
    def articles(self):
        l = sorted([(article.order, xml_name) for xml_name, article in self.merged_articles.items()])
        l = [(xml_name, self.merged_articles[xml_name]) for order, xml_name in l]
        return l

    @property
    def is_aop_issue(self):
        return any([a.is_ahead for a in self.merged_articles.values()])

    @property
    def is_rolling_pass(self):
        return all([a for a in self.merged_articles.values() if a.is_rolling_pass])

    @property
    def common_data(self):
        data = {}
        for label in self.EXPECTED_COMMON_VALUES_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if label in self.IGNORE_NONE and value is None:
                    pass
                else:
                    if value not in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data

    @property
    def missing_required_data(self):
        required_items = {}
        for label in self.REQUIRED_DATA:
            if label in self.common_data.keys():
                if None in self.common_data[label].keys():
                    required_items[label] = self.common_data[label][None]
        return required_items

    @property
    def conflicting_values(self):
        data = {}
        for label, values in self.common_data.items():
            if len(values) > 1:
                data[label] = values
        return data

    @property
    def duplicated_values(self):
        duplicated_labels = {}
        for label, values in self.unique_values.items():
            if len(values) > 0 and len(values) != len(self.articles):
                duplicated = {value: xml_files for value, xml_files in values.items() if len(xml_files) > 1}
                if len(duplicated) > 0:
                    duplicated_labels[label] = duplicated
        return duplicated_labels

    @property
    def unique_values(self):
        data = {}
        for label in self.EXPECTED_UNIQUE_VALUE_LABELS:
            values = {}
            for xml_name, article in self.merged_articles.items():
                value = article.summary[label]
                if value is not None:
                    if value not in values:
                        values[value] = []
                    values[value].append(xml_name)

            data[label] = values
        return data


class ArticlesMergence(object):

    def __init__(self, registered_articles, articles, is_db_generation):
        self.is_db_generation = is_db_generation
        self.registered_articles = RegisteredArticles(registered_articles)
        self.articles = articles
        self.titaut_conflicts = None
        self.name_order_conflicts = None
        self.name_changes = None
        self.order_changes = None
        self.excluded_orders = None
        self._merged_articles = None
        self._accepted_articles = {}

    @property
    def pkg_articles_by_order_and_name(self):
        return {a.order + name: name for name, a in self.articles.items()}

    @property
    def registered_articles_by_order_and_name(self):
        if self.is_db_generation:
            return {a.order + name: name for name, a in self.registered_articles.items()}
        return {}

    @property
    def registered_articles_by_order(self):
        if self.is_db_generation:
            return {a.order: name for name, a in self.registered_articles.items()}
        return {}

    @property
    def accepted_articles(self):
        return self._accepted_articles

    @property
    def pkg_order_conflicts(self):
        # pkg order conflicts
        if self.is_db_generation:
            pkg_orders = {a.order: [] for name, a in self.articles.items() if a.marked_to_delete is False}
            for name, a in self.articles.items():
                if not a.marked_to_delete:
                    pkg_orders[a.order].append(name)
            return {order: names for order, names in pkg_orders.items() if len(names) > 1}
        return {}

    @property
    def merged_articles(self):
        if self._merged_articles is None:
            self._merged_articles = self.merge_articles()
        return self._merged_articles

    def merge_articles(self):
        # registered
        self.history_items = {name: [HISTORY_REGISTERED] for name in self.registered_articles.keys()}

        # package
        for name, a in self.articles.items():
            if name not in self.history_items.keys():
                self.history_items[name] = []
            self.history_items[name].append(HISTORY_PACKAGE)

        # analyze package
        results = self.analyze_pkg_articles()
        merged = self.registered_articles.copy()

        # delete
        for name in results.get(ACTION_DELETE, []):
            del merged[name]
            self.history_items[name].append(HISTORY_DELETED)

        # update
        merged.update({name: self.articles.get(name) for name in results.get(ACTION_UPDATE, [])})
        for name in results.get(ACTION_UPDATE, []):
            self.history_items[name].append(HISTORY_ACCEPTED)
            self._accepted_articles[name] = self.articles.get(name)

        # found titaut conflicts
        for name in results.get(ACTION_SOLVE_TITAUT_CONFLICTS, []):
            self.history_items[name].append(HISTORY_TITAUT_CONFLICTS)
            self.history_items[name].append(HISTORY_REJECTED)

        # solve titaut conflicts
        solved = self.evaluate_titaut_conflicts(
            results.get(ACTION_SOLVE_TITAUT_CONFLICTS, []))
        for name in solved:
            merged[name] = self.articles[name]
            #self.history_items[name].remove(HISTORY_REJECTED)
            self.history_items[name].pop()
            self.history_items[name].append(HISTORY_SOLVED)
            self._accepted_articles[name] = self.articles.get(name)

        # need to check name/order
        for name in results.get(ACTION_CHECK_ORDER_AND_NAME, []):
            self.history_items[name].append(HISTORY_CHECK_ORDER_AND_NAME)

        # solve name/order
        solved = self.evaluate_check_order_and_name(
            results.get(ACTION_CHECK_ORDER_AND_NAME, []),
            results.get(ACTION_DELETE, [])
            )
        for name in solved:
            merged[name] = self.articles[name]
            #self.history_items[name].remove(HISTORY_REJECTED)
            self.history_items[name].pop()
            self.history_items[name].append(HISTORY_SOLVED)
            self._accepted_articles[name] = self.articles.get(name)

        # delete name changed
        for name in self.name_changes.values():
            del merged[name]

        self.excluded_items = {name: self.articles[name].order for name in results.get(ACTION_DELETE, [])}
        self.excluded_orders = [self.articles[name].order for name in results.get(ACTION_DELETE, [])]
        self.excluded_orders.extend([previous for previous, current in self.order_changes.values()])
        return merged

    def analyze_pkg_articles(self):
        results = {}
        for k, a_name in self.pkg_articles_by_order_and_name.items():
            registered_name = self.registered_articles_by_order_and_name.get(k)
            if registered_name is not None:
                article_comparison = article_data_reports.ArticlesComparison(
                    self.registered_articles.get(a_name),
                    self.articles.get(a_name))
                if not article_comparison.are_similar:
                    status = ACTION_SOLVE_TITAUT_CONFLICTS
                elif self.articles[a_name].marked_to_delete:
                    status = ACTION_DELETE
                else:
                    status = ACTION_UPDATE
            else:
                status = ACTION_CHECK_ORDER_AND_NAME
            if status not in results.keys():
                results[status] = []
            results[status].append(a_name)
        return results

    def evaluate_titaut_conflicts(self, names):
        solved = []
        self.titaut_conflicts = {}
        if names is not None:
            for name in names:
                similars = self.registered_articles.registered_titles_and_authors(self.articles.get(name))
                if len(similars) == 0:
                    solved.append(name)
                elif len(similars) == 1 and name in similars.keys():
                    solved.append(name)
                else:
                    self.titaut_conflicts[name] = similars
        return solved

    def evaluate_check_order_and_name(self, names, deleted):
        solved = []
        self.name_order_conflicts = {}
        self.order_changes = {}
        self.name_changes = {}
        if names is not None:
            for name in names:
                order = self.articles.get(name).order
                if order in self.pkg_order_conflicts.keys():
                    # order conflicts; duplicity of order in pkg
                    self.name_order_conflicts[name] = {_name: self.articles.get(_name) for _name in self.pkg_order_conflicts[order] if name != _name}
                    self.history_items[name].append(HISTORY_PKG_ORDER_CONFLICTS)
                else:
                    # valid order
                    found = [registered_name for registered_name, a in self.registered_articles.items() if a.order == order]
                    found_by_order = found[0] if len(found) == 1 else None
                    found_by_name = name if self.registered_articles.get(name) is not None else None
                    if found_by_name in deleted:
                        found_by_name = None
                    if found_by_order in deleted:
                        found_by_order = None
                    if found_by_name is None and found_by_order is None:
                        solved.append(name)
                        self.history_items[name].append(HISTORY_CREATED)
                    elif all([found_by_name, found_by_order]):
                        # found both in different records
                        self.name_order_conflicts[name] = {found_by_name: self.registered_articles.get(found_by_name), found_by_order: self.registered_articles.get(found_by_order)}
                        self.history_items[name].append(HISTORY_ORDER_AND_NAME_CONFLICTS)
                    elif found_by_name is not None:
                        # order not found
                        if self.are_similar(found_by_name, name, False, True):
                            # order changed
                            solved.append(name)
                            self.order_changes[name] = (self.registered_articles.get(name).order, order)
                            self.history_items[name].append(HISTORY_ORDER_CHANGED)
                        else:
                            # only name is identical
                            self.name_order_conflicts[name] = {found_by_name: self.registered_articles.get(found_by_name)}
                            self.history_items[name].append(HISTORY_UNMATCHED)
                    elif found_by_order is not None:
                        # name not found
                        if self.are_similar(found_by_order, name, True, False):
                            # name changed
                            solved.append(name)
                            self.name_changes[name] = found_by_order
                            self.history_items[name].append(HISTORY_NAME_CHANGED)
                            self.history_items[name].append(HISTORY_REPLACE + ' ' + found_by_order)
                            self.history_items[found_by_order].append(HISTORY_REPLACED_BY + ' ' + name)
                        else:
                            # only order is identical
                            self.name_order_conflicts[name] = {found_by_order: self.registered_articles.get(found_by_order)}
                            self.history_items[name].append(HISTORY_UNMATCHED)
        return solved

    def are_similar(self, registered_name, pkg_name, ign_name, ign_order):
        article_comparison = article_data_reports.ArticlesComparison(
                self.registered_articles.get(registered_name),
                self.articles.get(pkg_name),
                ign_name,
                ign_order)
        return article_comparison.are_similar
