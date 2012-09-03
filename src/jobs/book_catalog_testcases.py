# -*- coding:utf8 -*-

import unittest
from unittest import TestCase
from mocker import Mocker

from book_catalog import CatalogReader
from book_catalog import CatalogItem
from book_catalog import CatalogMySQLWriter

class CatalogReaderTestCase(TestCase):
    
    def test_read_basic_fields(self):
        mocker = Mocker()
        csv_reader = mocker.mock()

        csv_reader.next()
        header_line = [
            'title', 'isbn', 'publisher', 'list_price', 'publish_date',
            'class_', 'sheet_numbers', 'folio', 'print_type', 'author',
            'barcode', 'comments']
        mocker.result(header_line)

        csv_reader.next()
        first_line = [
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb', 'a',
            'blahblahblah' ]
        mocker.result(first_line)

        mocker.replay()

        field_map = {'title': 0, 'isbn': 1, 'publisher': 2, 'list_price': 3,
            'publish_date': 4, 'class_': 5, 'sheet_numbers': 6, 'folio': 7, 
            'print_type': 8, 'author': 9, 'barcode': 10, 'comments': 11 }

        reader = CatalogReader(csv_reader, field_map)
        item = reader.read()
        
        self.assertIsInstance(item, CatalogItem)

        mocker.restore()
        mocker.verify()

    def test_read_tags(self):
        mocker = Mocker()
        csv_reader = mocker.mock()

        headers = [
            'title', 'isbn', 'publisher', 'list_price', 'publish_date',
            'class_', 'sheet_numbers', 'folio', 'print_type', 'author',
            'barcode', 'comments', 'audience', 'awards']
        first_line = [
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb', 'a',
            'blahblahblah', 'ms', 'annual']
        field_map = {'title': 0, 'isbn': 1, 'publisher': 2, 'list_price': 3,
            'publish_date': 4, 'class_': 5, 'sheet_numbers': 6, 'folio': 7, 
            'print_type': 8, 'author': 9, 'barcode': 10, 'comments': 11 }

        csv_reader.next() # read headers
        mocker.result(headers)
        
        csv_reader.next() # read first line
        mocker.result(first_line)

        mocker.replay()

        reader = CatalogReader(csv_reader, field_map)
        item = reader.read()
        
        self.assertIsInstance(item, CatalogItem)
        self.assertEquals(2, len(item.tags))
        
        tag1 = item.tags[0]
        self.assertEquals('audience', tag1[0])
        self.assertEquals('ms', tag1[1])

        tag2 = item.tags[1]
        self.assertEquals('awards', tag2[0])
        self.assertEquals('annual', tag2[1])

        mocker.restore()
        mocker.verify()

    def test_required_field_missing(self):
        mocker = Mocker()
        csv_reader = mocker.mock()
        
        headers = [
            'title', 'isbn', 'publisher', 'list_price', 'publish_date',
            'class_', 'sheet_numbers', 'folio', 'print_type', 'author',
            'barcode']
        first_line = [
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb', 'a']
        field_map = {
            'title': 0, 'isbn': 1, 'publisher': 2, 'list_price': 3,
            'publish_date': 4, 'class_': 5, 'sheet_numbers': 6, 'folio': 7,
            'print_type': 8, 'author': 9, 'barcode': 10, 'comments': 11 }

        csv_reader.next() # read headers
        mocker.result(headers)
            
        csv_reader.next() # read first line
        mocker.result(first_line)

        mocker.replay()

        reader = CatalogReader(csv_reader, field_map)
        item = reader.read()

        self.assertIsNone(item.comments)

        mocker.restore()
        mocker.verify()

class CatalogMySQLWriterTestCase(TestCase):

    def test_write(self):
        mocker = Mocker()
        db = mocker.mock()

        insert_book = 'insert into book (title, isbn, publisher, list_price,\
                        publish_date, class, sheet_numbers, folio, print_type,\
                        author, barcode, comments)\
                        values (\'a\', \'1234\', \'aph\', \'30\', \'2012\',\
                        \'I.\', 18, \'4\', \'mono\', \'sb\', \'a\',\
                        \'blahblahblah\')'
        db.query(insert_book)
        mocker.replay()

        writer = CatalogMySQLWriter(db)
        item = CatalogItem(
            'a', '1234', 'aph', '30', '2012', 'I.', '18', '4', 'mono', 'sb',
            '4567', 'blahblahblah', { 'audience': 'ms', 'awards': 'annual' })
        writer.write(item)

        mocker.restore()
        mocker.verify()

if '__main__' == __name__:
    unittest.main()

    
    
