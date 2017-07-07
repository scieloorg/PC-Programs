# coding=utf-8

from ..db import registered
from ..validations import validation_status
from ..useful import article_data_reports


ACTION_DELETE = 'delete'
ACTION_SOLVE_TITAUT_CONFLICTS = 'TITAUT_CONFLICTS'
ACTION_UPDATE = 'update'
ACTION_CHECK_ORDER_AND_NAME = 'CHECK_ORDER_AND_NAME'


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
    def is_processed_in_batches(self):
        return any([self.is_aop_issue, self.is_rolling_pass])

    @property
    def is_aop_issue(self):
        return any([a.is_ahead for a in self.merged_articles.values()])

    @property
    def is_rolling_pass(self):
        return all([a for a in self.merged_articles.values() if a.is_epub_only])

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
                    if not value in values:
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

    @property
    def orders_conflicts(self):
        orders = {}
        for name, article in self.merged_articles.items():
            if not article.order in orders.keys():
                orders[article.order] = []
            orders[article.order].append(name)
        return {order: names for order, names in orders.items() if len(names) > 1}


class MergingResult(object):

    def __init__(self):
        self.exclusions = []
        self.conflicts = {}
        self.actions = {}
        self.name_changes = {}
        self.order_changes = {}
        self.excluded_orders = None
        self.total_to_convert = 0
        self.articles_to_convert = None
        self.history_items = None
        self.articles_to_convert = None


class ArticlesMerger(object):

    def __init__(self, registered_articles, articles):
        self.registered_articles = registered.RegisteredArticles(registered_articles)
        self.articles = articles
        self.merging_result = MergingResult()

    @property
    def pkg_articles_by_order_and_name(self):
        return {a.order + name: name for name, a in self.articles.items()}

    @property
    def registered_articles_by_order_and_name(self):
        return {a.order + name: name for name, a in self.registered_articles.items()}

    @property
    def pkg_articles_by_order(self):
        r = {k: [] for k in self.articles.keys()}
        for name, a in self.articles.items():
            r[name].append(a)
        return r

    @property
    def registered_articles_by_order(self):
        return {a.order: name for name, a in self.registered_articles.items()}

    @property
    def merged_articles(self):
        return self._merged_articles

    @property
    def total_to_convert(self):
        return len(self.articles)

    @property
    def articles_to_convert(self):
        return self.articles

    def merge(self):
        results = self.analyze_pkg_articles()
        merged_articles = self.registered_articles.copy()
        for name in results.get(ACTION_DELETE, []):
            del merged_articles[name]
        merged_articles.update({name: self.articles.get(name) for name in results.get(ACTION_UPDATE)})

        solved, conflicts = self.evaluate_titaut_conflicts(results.get(ACTION_SOLVE_TITAUT_CONFLICTS))
        for name in solved:
            merged_articles[name] = self.articles[name]

        solved2, conflicts2 = self.evaluate_check_order_and_name(results.get(ACTION_CHECK_ORDER_AND_NAME))
        for name in solved2:
            merged_articles[name] = self.articles[name]

    def analyze_pkg_articles(self):
        results = {}
        for k, a_name in self.pkg_articles_by_order_and_name.items():
            registered_name = self.registered_articles_by_order_and_name.get(k)
            if registered_name is not None:
                article_comparison = article_data_reports.ArticlesComparison(self.registered_articles.get(a_name), self.articles.get(a_name))
                if article_comparison.articles_similarity_result == validation_status.STATUS_BLOCKING_ERROR:
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
        conflicts = {}
        if names is not None:
            for name in names:
                similars = self.registered_articles.registered_titles_and_authors(self.articles.get(name))
                if similars == 0:
                    solved.append(name)
                elif similars == 1 and similars[0] == name:
                    solved.append(name)
                else:
                    conflicts[name] = similars
        return solved, conflicts

    def evaluate_check_order_and_name(self, names):
        solved = []
        conflicts = {}
        if names is not None:
            for name in names:
                order = self.articles.get(name).order
                found = [name for name, a in self.registered_articles.items() if a.order == order]
                found_by_order = found[0] if len(found) == 1 else None
                found_by_name = name if self.registered_articles.get(name) is not None else None
                if found_by_name is None and found_by_order is None:
                    solved.append(name)
                elif all([found_by_name, found_by_order]):
                    if found_by_name != found_by_order:
                elif found_by_name is not None:

                elif found_by_order is not None:
                    
                    self.identify_order_and_name_conflicts(name, found_by_order, found_by_name)
        return solved, conflicts

    def identify_order_and_name_conflicts(self, name, found_by_order, found_by_name):
        similars = []
        for order_name in found_by_order:
            article_comparison = article_data_reports.ArticlesComparison(
                    self.registered_articles.get(order_name),
                    self.articles.get(name),
                    ign_name=True)
            if article_comparison.are_similar:
                similars.append(order_name)
        if len(similars) == 0:
            conflicts.append()



    def analyze_pkg_article(self, name, pkg_article):
        registered_titaut, registered_name, registered_order = self.registered_articles.search_articles(name, pkg_article)
        action, old_name, conflicts = self.registered_articles.analyze_registered_articles(name, registered_titaut, registered_name, registered_order)
        return (action, old_name, conflicts)

    @property
    def excluded_orders(self):
        #excluded_orders
        items = {}
        orders = [article.order for article in self.merged_articles.values()]
        for name, article in self.registered_articles.items():
            if not article.order in orders:
                items[name] = article.order
        return {name: article.order for name, article in self.registered_articles.items() if not article.order in orders}

    def old_merge(self):
        self.old_analyze_pkg()
        self.old_update_articles()

    def old_analyze_pkg(self):
        for name, article in self.articles.items():
            action, old_name, conflicts = self.analyze_pkg_article(name, article)
            if conflicts is not None:
                conflicts['package'] = article
                self.merging_result.conflicts[name] = conflicts
            if action is not None:
                self.merging_result.actions[name] = action
            if action == 'update' and article.marked_to_delete:
                self.merging_result.exclusions.append(name)
            if old_name is not None:
                self.merging_result.name_changes[old_name] = name
            if name in self.registered_articles.keys():
                if article.order != self.registered_articles[name].order:
                    self.merging_result.order_changes[name] = (self.registered_articles[name].order, article.order)

    def old_update_articles(self):
        self.merging_result.history_items = {}
        # starts history with registered articles data
        self.merging_result.history_items = {name: [('registered article', article)] for name, article in self.registered_articles.items()}

        # exclude registered items
        for name in self.merging_result.exclusions:
            self.merging_result.history_items[name].append(('excluded article', self._merged_articles[name]))
            del self._merged_articles[name]

        # indicates package articles reception
        for name, article in self.articles.items():
            if not name in self.merging_result.history_items.keys():
                self.merging_result.history_items[name] = []
            self.merging_result.history_items[name].append(('package', article))

        # indicates names changes, and exclude old names
        for previous_name, name in self.merging_result.name_changes.items():
            self.merging_result.history_items[previous_name].append(('replaced by', self.articles[name]))

            self.merging_result.history_items[name].append(('replaces', self._merged_articles[previous_name]))
            del self._merged_articles[previous_name]

        # merge pkg and registered, considering some of them are rejected
        orders_to_check = []
        for name, article in self.articles.items():
            if not article.marked_to_delete:
                action = self.merging_result.actions.get(name)
                if name in self.merging_result.conflicts.keys():
                    action = 'reject'
                if not action in ['reject', None]:
                    self._merged_articles[name] = self.articles[name]

        self.merging_result.excluded_orders = self.excluded_orders
        self.merging_result.total_to_convert = self.total_to_convert
        self.merging_result.articles_to_convert = self.articles_to_convert

