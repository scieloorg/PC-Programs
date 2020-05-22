# coding=utf-8
"""
Usado pelo Markup para o Automata 2 que obtem XML e retorna SGML
parameters:
    - par_xmlFileName
    - par_xslFileName
    - TransformationResultFileName
    - ctrlFileName
    - transfErrorFileName
"""
import sys
import os

from prodtools.utils.xml_utils import (
    transform,
    get_xml_object,
)
from prodtools.utils import encoding


try:
    args = encoding.fix_args(sys.argv)
    script, xml_filename, xsl_filename, result_filename, ctrl_filename, err_filename = args

    if os.path.exists(ctrl_filename):
        os.unlink(ctrl_filename)
    if os.path.exists(err_filename):
        os.unlink(err_filename)

    xml_obj = get_xml_object(xml_filename)
    result_tree = transform(xml_obj, xsl_filename)
    if result_tree is not None:
        result_tree.write(
            result_filename, method="text", encoding="iso-8859-1")
except Exception as e:
    with open(result_filename, "w") as fp:
        fp.write("")
    with open(err_filename, "w") as fp:
        fp.write(str(e))
    dirname = os.path.dirname(err_filename)
    err_filename = "automata2.log"
    with open(err_filename, "w") as fp:
        fp.write(str(e))
    raise e
finally:
    with open(ctrl_filename, "w") as fp:
        fp.write("done")
