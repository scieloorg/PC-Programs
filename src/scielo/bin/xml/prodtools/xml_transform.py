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
from __future__ import print_function, unicode_literals
import argparse
import os
import logging
import logging.config

from prodtools.utils.xml_utils import (
    transform,
    get_xml_object,
)

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='XML Transformer for Markup cli utility')
    parser.add_argument(
        "xml_filepath",
        help="filesystem path to the XML")
    parser.add_argument(
        "xsl_filepath",
        help="filesystem path to the XSL"
    )
    parser.add_argument(
        "result_filepath",
        help="filesystem path to the transformation result")
    parser.add_argument(
        "ctrl_filepath",
        help="filesystem path to the control file"
    )
    parser.add_argument(
        "err_filepath",
        help="filesystem path to the error report")

    parser.add_argument('--loglevel', default='WARNING')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    ctrl_filepath = args.ctrl_filepath
    err_filepath = args.err_filepath
    result_filepath = args.result_filepath
    xml_filepath = args.xml_filepath
    xsl_filepath = args.xsl_filepath

    for f in (ctrl_filepath, err_filepath, result_filepath):
        if os.path.exists(f):
            try:
                os.unlink(f)
            except OSError as e:
                finish(ctrl_filepath, err_filepath, result_filepath,
                       "Unable to delete {}".format(f))
    try:
        xml_obj = get_xml_object(xml_filepath)
        result_tree = transform(xml_obj, xsl_filepath)
        if result_tree is not None:
            result_tree.write(
                result_filepath, method="text", encoding="iso-8859-1")
    except Exception as e:
        finish(ctrl_filepath, err_filepath, result_filepath, str(e))
    finally:
        with open(ctrl_filepath, "w") as fp:
            fp.write("done")


def finish(ctrl_filepath, err_filepath, result_filepath, err_msg):
    with open(err_filepath, "w") as fp:
        fp.write("err_msg")
    with open(result_filepath, "w") as fp:
        fp.write("")
    with open(ctrl_filepath, "w") as fp:
        fp.write("done")
