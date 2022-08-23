# -*- coding: UTF-8 -*-
import unittest
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TESTS_DIR, 'data')


def mk_parent_dir_if_not_exist(local_path):
    """为指定路径创建父目录,如果父目录不存在的话"""
    parent_dir = os.path.dirname(local_path)
    if not os.path.exists(parent_dir):
        mkdir_if_not_exist(parent_dir)


def mkdir_if_not_exist(local_path):
    """在指定位置创建目录,如果不存在的话"""
    if os.path.isfile(local_path):
        raise ValueError('cannot create dir for the same name is a regular file. path=' + local_path)
    if os.path.isdir(local_path):
        return
    if not os.path.exists(local_path):
        os.makedirs(local_path)


class GoogleParserTests(unittest.TestCase):

    def setUp(self):
        pass

    def get_data_path(self, file: str):
        u'生成文件全路径'
        return os.path.join(TEST_DATA_DIR, file)

    def get_data(self, file_name: str):
        u'返回按指定路径相对于数据目录的任何文件的内容'
        with open(self.get_data_path(file_name), 'r') as fin:
            text = fin.read()
        return text

    def write_data(self, file_name: str, html: str):
        u'把 html 写入文件'
        local_path = self.get_data_path(file_name)
        mk_parent_dir_if_not_exist(local_path)
        with open(local_path, 'w', encoding='utf-8') as fout:
            fout.write(html)


if __name__ == '__main__':
    suite = unittest.TestLoader().discover(TESTS_DIR)
    unittest.TextTestRunner(verbosity=2).run(suite)
