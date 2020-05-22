# coding=utf-8

from prodtools import _
from prodtools.reports import validation_status


class ArticleTableWrapValidator(object):

    def __init__(self, config):
        self.config = config
        self.acceptable_elements = [
            'graphic',
            'table',
            'alternatives',
            ]
        if self.config.coded_table_required:
            self.acceptable_elements.remove('graphic')

    def validate(self, article):
        results = []
        error = False
        for tablewrap in article.tablewraps:
            error = False
            if len(tablewrap.codes) + len(tablewrap.graphics) == 0:
                error = True
            elif self.config.coded_table_required and len(tablewrap.codes) == 0:
                error = True
            if error is True and tablewrap.lang is None:
                results.append(
                    (tablewrap.tag,
                        validation_status.STATUS_FATAL_ERROR,
                        _('{element} is not complete, it requires {children} with valid structure. ').format(
                            children=_(' or ').join(self.acceptable_elements),
                            element=tablewrap.tag),
                        tablewrap.xml))
        return results
