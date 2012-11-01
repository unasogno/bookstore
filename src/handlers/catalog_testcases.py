# -*- coding:utf8 -*-

import unittest
from unittest import TestCase
# todo: mock modules
from mocker import Mocker
import csv

from catalog import parse_file
from book_catalog import parse_field_map
from book_catalog import import_catalog
from catalog import RequestBodyError
from catalog import MapFormatError
from catalog import CatalogFormatError

CATALOG_BODY_SAMPLE = 'upload.sample.txt'
CATALOG_SAMPLE = 'catalog.sample.csv'
FIELD_MAP_SAMPLE = 'field_map.sample.csv'

class CatalogHandlerTestCases(TestCase):

    def test_import_catalog(self):
        try:
            fp = open(CATALOG_SAMPLE, 'r')
            map_fp = open(FIELD_MAP_SAMPLE, 'r')

            class DummyWriter(object):
                def write(self, text):
                    pass

            import_catalog(fp, map_fp, DummyWriter())
            
        finally:
            fp.close()
            map_fp.close()

    def test_parse_field_map(self):
        with open(FIELD_MAP_SAMPLE, 'r') as fp:
            field_map = parse_field_map(fp)
            fp.close()

        self.assertEqual(0, field_map['barcode'])
        self.assertEqual(9, field_map['author'])
        self.assertEqual(14, field_map['comments'])
    
    def test_parse_file(self):
        parts = self.parse_parts(CATALOG_BODY_SAMPLE)

        self.assertEqual(2, len(parts))

        self.assert_part(
            parts[0], 'catalog', 'catalog.txt', 'form-data', 'text/plain');
        self.assert_stream(parts[0].get_content_stream(),
                           ['a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            '\n'])
        
        self.assert_part(
            parts[1], 'field_map', 'field_map.txt', 'form-data', 'text/plain');
        self.assert_stream(parts[1].get_content_stream(),
                           ['1,a\n', '2,b\n', '3,c\n',])

    def parse_field_map(self, filename):
        with open(filename, 'r') as fp:
            field_map = parse_field_map(fp)
            fp.close()
        return field_map

    def parse_parts(self, filename):
        with open(filename, 'r') as fp:
            parts = parse_file(fp)
            fp.close()
        return parts

    def assert_part(
        self, part, name, filename, content_disposition, content_type):
        
        self.assertEqual(name, part.name)
        self.assertEqual(filename, part.filename)
        self.assertEqual(content_disposition, part.content_disposition)
        self.assertEqual(content_type, part.content_type)

    def assert_stream(self, stream, lines):
        i = 0
        while True:
            line = stream.readline()
            if '' == line: break
            self.assertEqual(lines[i], line)
            i+=1
        self.assertEqual(len(lines), i)

    def setUp(self):
        pass

if '__main__' == __name__:
    class DummyLogger(object):
        def debug(self, text):
            pass
    logger = DummyLogger()
    mocker = Mocker()
    mongrel2 = mocker.mock()
    unittest.main()

