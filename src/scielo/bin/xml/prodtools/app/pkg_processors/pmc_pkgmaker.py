# coding=utf-8
import logging
import logging.config
import os
import shutil

from ...__init__ import _

from ...generics import encoding
from ...generics import xml_utils
from ...generics.reports import html_reports
from ..validations import sps_xml_validators
from . import xml_versions
from ..data import workarea
from ..data import article


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class PMCPackageMaker(object):

    def __init__(self, pkg):
        self.wk = pkg.wk
        self.article_items = pkg.articles
        self.outputs = pkg.outputs
        self.pkg_files = pkg.files

    def make_package(self):
        doit = False

        encoding.display_message('\n')
        encoding.display_message(_('Generating PMC Package'))
        n = '/' + str(len(self.article_items))
        index = 0

        for xml_name, doc in self.article_items.items():
            index += 1
            item_label = str(index) + n + ': ' + xml_name
            encoding.display_message(item_label)

            pmc_filename = os.path.join(
                self.wk.pmc_package_path, xml_name + '.xml')

            doit = PMCPackageItemMaker(
                self.outputs[xml_name],
                self.pkg_files[xml_name],
                self.article_items[xml_name],
                pmc_filename).make_package()

        if doit:
            workarea.MultiDocsPackageFolder(self.wk.pmc_package_path).zip()


class PMCPackageItemMaker(object):

    def __init__(self, outputs, scielo_pkg_files, article, pmc_xml_filepath):
        self.outputs = outputs
        self.scielo_pkg_files = scielo_pkg_files
        self.article = article
        self.pmc_pkg_files = None
        self.pmc_xml_filepath = pmc_xml_filepath

    def make_package(self):
        scielo_dtd_files = xml_versions.dtd_files(
            self.article.sps_version_number)
        pmc_dtd_files = xml_versions.dtd_files(
            self.article.sps_version_number, database="pmc")

        if self.article.journal_id_nlm_ta is None:
            html_reports.save(
                self.outputs.pmc_style_report_filename, 'PMC Style Checker',
                _('{label} is a mandatory data, and it was not informed. '
                  ).format(label='journal-id (nlm-ta)'))
        else:
            self.make_xml(scielo_dtd_files, pmc_dtd_files)
            return True

    def make_xml(self, scielo_dtd_files, pmc_dtd_files):

        sps_xml = self.article.tree
        # j1.1/xsl/sgml2xml/xml2pmc.xsl
        pmc_xml = xml_utils.transform(sps_xml, scielo_dtd_files.xsl_output)
        xml_utils.write(self.pmc_xml_filepath, pmc_xml)

        # recarrega
        pmc_xml = xml_utils.SuitableXML(self.pmc_xml_filepath)

        filenames, changed = self._get_filenames(pmc_xml.xml)
        numbers = self._insert_math_id(pmc_xml.xml)

        if numbers or changed:
            pmc_xml.write(self.pmc_xml_filepath)

        dirname = os.path.dirname(self.pmc_xml_filepath)
        for old, new in filenames:
            old = os.path.join(self.scielo_pkg_files.path, old)
            if os.path.isfile(old):
                new = os.path.join(dirname, new)
                shutil.copyfile(old, new)
            else:
                logging.info(
                    "File not found %s to compose PMC Package %s",
                    old, self.pmc_xml_filepath)

        # j1.1/xsl/sgml2xml/pmc.xsl
        result = xml_utils.transform(pmc_xml.xml, pmc_dtd_files.xsl_output)
        xml_utils.write(self.pmc_xml_filepath, result)

        # validate
        xml_validator = sps_xml_validators.PMCXMLValidator(pmc_dtd_files)
        xml_validator.validate(
            self.pmc_xml_filepath,
            self.outputs.pmc_dtd_report_filename,
            self.outputs.pmc_style_report_filename
            )

    def _insert_math_id(self, tree):
        # PMC exige o atributo @id para math
        n = 0
        for math in tree.findall(
                "{http://www.w3.org/1998/Math/MathML}math"):
            if math.get("id") is None:
                n += 1
                math.set("id", 'math{}'.format(n))
        return n

    def _get_filenames(self, tree):
        files = []
        delete = False
        rename = False
        tiff_items = self.scielo_pkg_files.tiff_name_and_basename_items
        for node in article.nodes_which_have_xlink_href(tree):
            if node.get("specific-use") == "scielo-web":
                node.tag = "REMOVE"
                delete = True
                continue

            href = node.attrib['{http://www.w3.org/1999/xlink}href']
            name, ext = os.path.splitext(href)

            # substitui o valor de href por ativo digital em tiffs
            tiff = tiff_items.get(name)
            if tiff and href != tiff:
                rename = True
                node.set("{http://www.w3.org/1999/xlink}href", tiff)
                href = tiff

            # remove o sufixo -en dos ativos digitais da versao ingles
            name, ext = os.path.splitext(href)
            if name.endswith("-en"):
                new = name[:-3] + ext
                files.append((href, new))
                rename = True
                node.set("{http://www.w3.org/1999/xlink}href", new)
            else:
                files.append((href, href))

        if delete:
            xml_utils.etree.strip_tags(tree, "REMOVE")
            for node in tree.findall(".//alternatives"):
                if len(node.getchildren()) == 1:
                    logger.info(
                        "Remove alternatives: {}".format(
                            xml_utils.tostring(node)))
                    node.tag = "REMOVE"
            xml_utils.etree.strip_tags(tree, "REMOVE")
        return files, delete or rename
