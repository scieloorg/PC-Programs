# coding=utf-8

from ...__init__ import _
from ...generics import xml_utils
from ...generics.reports import validation_status


class ArticleDispFormulasValidator(object):

    def __init__(self, article, config):
        self.article = article
        self.config = config
        self.acceptable_elements = None

    def validate(self):
        self.acceptable_elements = [
            'graphic',
            '{http://www.w3.org/1998/Math/MathML}math',
            'math',
            'tex-math',
            'alternatives',
            ]
        if self.config.coded_formula_required:
            self.acceptable_elements.remove('graphic')
        return self.result()

    @property
    def result(self):
        results = []
        required_at_least_one_child = self.acceptable_elements
        for disp_formula_node in self.article.disp_formula_elements:
            found = False
            for child in disp_formula_node.findall('*'):
                if child.tag in required_at_least_one_child:
                    if child.tag == 'graphic':
                        found = self.is_not_empty_attribute(child, '{http://www.w3.org/1999/xlink}href')
                    elif child.tag in ['{http://www.w3.org/1998/Math/MathML}math', 'math', 'tex-math']:
                        found = self.is_not_empty_element(child)
                    elif child.tag in ['alternatives']:
                        found = False
                        if 'graphic' in required_at_least_one_child:
                            graphic = child.find('graphic')
                            found = grafic is not None and self.is_not_empty_attribute(graphic, '{http://www.w3.org/1999/xlink}href')

                        found = any([found, self.is_not_empty_element(child.find('math')),
                                self.is_not_empty_element(child.find('{http://www.w3.org/1998/Math/MathML}math')),
                                self.is_not_empty_element(child.find('tex-math')),
                                ])                    
                if found:
                    break
            if not found:
                results.append(('disp-formula', validation_status.STATUS_FATAL_ERROR, _('{element} is not complete, it requires {children} with valid structure. ').format(children=_(' or ').join(required_at_least_one_child), element='disp-formula'), xml_utils.node_xml(disp_formula_node)))
        return results

    def is_not_empty_element(self, node):
        if node is not None:
            return len(xml_utils.remove_tags(xml_utils.node_text(node))) > 0

    def is_not_empty_attribute(self, node, attr_name):
        if node is not None:
            return node.attrib.get(attr_name) != ''
