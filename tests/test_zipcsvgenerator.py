import os
import re
import unittest

from tools import ZipCsvGenerator


class TestDecrypt(unittest.TestCase):
    def setUp(self) -> None:
        self.zip_dir = 'zip_dir'
        self.csv_dir = 'csv_dir'

        self.zcg = ZipCsvGenerator(self.zip_dir, self.csv_dir)

    def test_exist_out_directories(self):
        zip_dir_exist = os.path.exists(os.path.join('../', self.zcg.zip_dir))
        csv_dir_exist = os.path.exists(os.path.join('../', self.zcg.csv_dir))

        self.assertTrue(zip_dir_exist and csv_dir_exist)

    def test_xml_structure(self):
        xml = self.zcg.generate_xml().replace('\n', '')
        with open('xml_template.txt', 'r') as rin:
            xml_reg_template = re.compile(rin.read())

            matched = re.search(xml_reg_template, xml)

            self.assertTrue(matched)
