# coding=utf-8

from prodtools import _
from prodtools.reports import validation_status


class ArticleDispFormulasValidator(object):

    def __init__(self, config):
        self.config = config
        self.acceptable_elements = [
            'graphic',
            '{http://www.w3.org/1998/Math/MathML}math',
            'math',
            'tex-math',
            'alternatives',
            ]
        if self.config.coded_formula_required:
            self.acceptable_elements.remove('graphic')

    def validate(self, article):
        results = []
        error = False
        for formula in article.formulas:
            error = False
            if len(formula.codes) + len(formula.graphics) == 0:
                error = True
            elif self.config.coded_formula_required and len(formula.codes) == 0:
                error = True
            if error is True:
                results.append(
                    (formula.tag,
                        validation_status.STATUS_FATAL_ERROR,
                        _('{element} is not complete, it requires {children} with valid structure. ').format(
                            children=_(' or ').join(self.acceptable_elements),
                            element=formula.tag),
                        formula.xml))
        return results
