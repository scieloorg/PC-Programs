import os
import unittest
import tempfile

from prodtools.data.workarea import MultiDocsPackageOuputs


class TestMultiDocsPackageOuputs(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.output_container = MultiDocsPackageOuputs(self.temp_directory)

    def test_when_initialized_it_should_create_a_default_temporary_scielo_dir(self):
        self.assertTrue(os.path.exists(self.output_container.scielo_package_path))

    def test_when_initialized_it_should_create_a_default_temporary_reporth_dir(self):
        self.assertTrue(os.path.exists(self.output_container.reports_path))

    def test_when_initialized_it_should_create_a_default_temporary_tmp_dir(self):
        self.assertTrue(os.path.exists(self.output_container.tmp_path))

    def test_when_initialized_it_should_create_a_default_temporary_pmc_package_dir(
        self,
    ):
        self.assertTrue(os.path.exists(self.output_container.pmc_package_path))

    def test_when_used_a_package_name_it_should_create_a_temporary_scielo_dir_using_the_name(
        self,
    ):
        output_container = MultiDocsPackageOuputs(
            self.temp_directory, package_name="random-package"
        )
        self.assertTrue(os.path.exists(output_container.scielo_package_path))
        self.assertTrue(output_container.scielo_package_path.endswith("random-package"))

