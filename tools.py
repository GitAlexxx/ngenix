import csv
import logging
import os.path
import random
import shutil
import string
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from zipfile import ZipFile

import lxml.etree
import xmltodict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZipCsvGenerator:
    """Класс для генерирования zip-, xml- файлов"""

    def __init__(self, zip_dir: str, csv_dir: str):
        self.zip_dir = zip_dir
        self.csv_dir = csv_dir

        shutil.rmtree(zip_dir)
        shutil.rmtree(csv_dir)

        logger.info(f'Класс {ZipCsvGenerator.__name__} инициализирован')

    def generate_zip_files(self, count: int) -> None:
        """
        Генератор заданного количества zip-файлов

        :param count: количество архивов для генерирования
        """
        for idx in range(count):
            self.create_zip(idx)

        logger.info(f'{count} zip-архивов сгенерировано')

    def create_zip(self, zip_idx: int) -> None:
        """
        Генератор одного zip-файла

        :param zip_idx: индекс генерируемого архива
        """

        zip_out_path = os.path.join(self.zip_dir, f'{zip_idx}.zip')

        for xml_idx in range(100):
            pretty_xml = self.generate_xml()

            if not os.path.exists(self.zip_dir):
                os.mkdir(self.zip_dir)

            with ZipFile(zip_out_path, 'a') as myzip:
                xml_file_name = f'{xml_idx}.xml'
                myzip.writestr(xml_file_name, pretty_xml)
                logger.debug(f'xml-файл {xml_file_name} сгенерирован')

        logger.debug(f'zip-архив №{zip_idx} сгенерирован')

    @classmethod
    def generate_xml(cls) -> str:
        """
        Генератор одного xml-файла

        :return: отформатированный текстовый xml-файл
        """

        uniq_str = str(datetime.today().timestamp()).replace('.', '')

        rand_uniq_str = ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(10)
        ) + uniq_str

        rand_num = str(random.randint(0, 100))

        root = ET.Element('root')
        ET.SubElement(root, "var", name="id", value=rand_uniq_str)
        ET.SubElement(root, "var", name="level", value=rand_num)

        objects = ET.SubElement(root, "objects")
        for _ in range(random.randint(1, 10)):
            rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50))
            ET.SubElement(objects, "object", name=rand_str)

        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        tree = lxml.etree.fromstring(xml_str)
        pretty_xml = lxml.etree.tostring(tree, encoding="unicode", pretty_print=True)

        return pretty_xml

    def generate_csv_files(self) -> None:
        """
        Разбор сгенерированных zip-файлов и запись их в csv-файлы.
        Первый: id, level - по одной строке на каждый xml файл
        Второй: id, object_name - по отдельной строке для каждого тэга object (от 1 до 10 строк на каждый xml файл)
        """

        zip_files = os.listdir(self.zip_dir)

        csv_1 = []
        csv_2 = []

        for zip_file in zip_files:
            file_path = os.path.join(self.zip_dir, zip_file)
            if zipfile.is_zipfile(file_path):
                archive = zipfile.ZipFile(file_path, 'r')
                xml_list = archive.filelist
                for xml in xml_list:
                    xml_str = archive.read(xml.filename).decode('utf8')
                    xml_dict = xmltodict.parse(xml_str)

                    var_id = [el['@value'] for el in xml_dict['root']['var'] if el['@name'] == 'id']
                    var_level = [el['@value'] for el in xml_dict['root']['var'] if el['@name'] == 'level']

                    obj_names = xml_dict['root']['objects']['object']
                    if isinstance(obj_names, list):
                        object_name_list = [el['@name'] for el in obj_names]
                    else:
                        object_name_list = [obj_names['@name']]

                    if not os.path.exists(self.csv_dir):
                        os.mkdir(self.csv_dir)

                    data = [[var_id[0], object_name] for object_name in object_name_list]

                    csv_1.append([var_id[0], var_level[0]])
                    csv_2.extend(data)

        csv_1_path = os.path.join(self.csv_dir, 'csv_1.csv')
        csv_2_path = os.path.join(self.csv_dir, 'csv_2.csv')

        header = ['id', 'level']
        with open(csv_1_path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(csv_1)
        logger.info(f'csv_1.csv сгенерирован')

        header = ['id', 'object_name']
        with open(csv_2_path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(csv_2)
        logger.info(f'csv_2.csv сгенерирован')
