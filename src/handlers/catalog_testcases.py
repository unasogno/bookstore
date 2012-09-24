# -*- coding:utf8 -*-

import unittest
from unittest import TestCase
# todo: mock modules
from mocker import Mocker

from catalog import parse_file
from catalog import RequestBodyError
from catalog import MapFormatError
from catalog import CatalogFormatError

CATALOG_BODY_SAMPLE = 'upload.sample.txt'

class CatalogHandlerTestCases(TestCase):
    def test_parse_file(self):
        with open(CATALOG_BODY_SAMPLE, 'r') as fp:
            parts = parse_file(fp)
            fp.close()

        self.assertEqual(2, len(parts))

        self.assert_part(parts[0], 'file1', '3.txt', 'form-data', 'text/plain');
        self.assert_stream(parts[0].get_content_stream(),
                           ['a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            'a b c d e f g h i j k l m n\n',
                            '\n'])
        
        self.assert_part(parts[1], 'file2', '1.txt', 'form-data', 'text/plain');
        self.assert_stream(parts[1].get_content_stream(),
                           ['1,a\n', '2,b\n', '3,c\n',])

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

if '__main__' == __name__:
    mocker = Mocker()
    mongrel2 = mocker.mock()
    unittest.main()

