# -*- coding:utf8 -*-

import unittest
from unittest import TestCase
from mocker import Mocker
import db_test_helper

import MySQLdb as mysql

from book_catalog import CatalogReader
from book_catalog import CatalogItem
from book_catalog import CatalogMySQLWriter
from book_catalog import import_catalog

class CatalogReaderTestCase(TestCase):
    # @unittest.skip('wrong test case')
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

        print item.tags
        
        self.assertEquals('ms', item.tags['audience'])
        self.assertEquals('annual', item.tags['awards'])

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
        writer = CatalogMySQLWriter(self.db)
        item = CatalogItem(
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb',
            'a', 'blahblahblah', { 'audience': 'ms', 'awards': 'annual' })

        job_id = writer.begin_write()
        self.helper.assert_unique('job', 'job_id', job_id)
        try:
            writer.write(item)
            self.helper.assert_count('raw_book', 1)
            self.helper.assert_count('raw_tag', 2)
            self.helper.assert_count('raw_publisher', 1)
            self.helper.assert_result(
                "select value from raw_code where type = 7 and name = '4'",
                ((1,),))
            self.helper.assert_result(
                "select value from raw_code where type = 8 and name = 'mono'",
                ((1,),))
            writer.apply()
        finally:
            writer.undo()
            self.helper.assert_count('job', 0)
            self.helper.assert_count('raw_book', 0)
            self.helper.assert_count('raw_tag', 0)
            self.helper.assert_count('raw_publisher', 0)
            self.helper.assert_count('raw_code', 0)

    def test_undo_write(self):
        writer = CatalogMySQLWriter(self.db)
        item = CatalogItem(
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb',
            'a', 'blahblahblah', { 'audience': 'ms', 'awards': 'annual' })

        job_id = writer.begin_write()
        self.helper.assert_unique('job', 'job_id', job_id)

        writer.write(item)
        writer.undo()
        self.helper.assert_count('job', 0)
        self.helper.assert_count('raw_book', 0)
        self.helper.assert_count('raw_tag', 0)
        self.helper.assert_count('raw_publisher', 0)
        self.helper.assert_count('raw_code', 0)

    def test_write_duplicated_publisher(self):
        writer = CatalogMySQLWriter(self.db)
        item1 = CatalogItem(
            'a', '1234', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb',
            'a', 'blahblahblah', { 'audience': 'ms', 'awards': 'annual' })

        item2 = CatalogItem(
            'b', '1235', 'aph', '30', '2012', 'I.', 18, '4', 'mono', 'sb',
            'a', 'blahblahblah', { 'audience': 'ms', 'awards': 'annual' })

        job_id = writer.begin_write()
        self.helper.assert_unique('job', 'job_id', job_id)
        try:
            writer.write(item1)
            writer.write(item2)
            self.helper.assert_count('raw_book', 2)
            self.helper.assert_count('raw_tag', 4)
            self.helper.assert_count('raw_publisher', 1)
            writer.apply()
        finally:
            writer.undo()
            self.helper.assert_count('job', 0)
            self.helper.assert_count('raw_book', 0)
            self.helper.assert_count('raw_tag', 0)
            self.helper.assert_count('raw_publisher', 0)

    def setUp(self):
        self.db = mysql.connect(**STAGE_DB)
        self.helper = db_test_helper.Helper(self.db, self.fail)
        self.helper.empty_table('raw_code')

    def tearDown(self):
        self.db.close()

class DBObjectTestCase(TestCase):
    def test_sp_add_code(self):
        job_id = 1
        code_type = 1
        code_name = 'a'
        expected_code_value = 1
        statement = '''
                    call sp_add_code(%d, %d, '%s')
                    ''' % (job_id, code_type, code_name)
        cursor = self.db.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        cursor.close()
        
        self.assertEqual(1, len(rows))
        self.assertEqual(code_type, rows[0][0])
        self.assertEqual(code_name, rows[0][1])
        self.assertEqual(expected_code_value, rows[0][2])

        self.db.query(
            "delete from raw_code where type = %d and name = '%s';"
            % (code_type, code_name))
        self.db.commit()
        
    def setUp(self):
        self.db = mysql.connect(**STAGE_DB)
        self.helper = db_test_helper.Helper(self.db, self.fail)
        self.helper.empty_table('raw_code')

    def tearDown(self):
        self.db.close()

class ImportCatalogTestCase(TestCase):
    def test_import_catalog(self):

        catalog_stream = None
        field_map_stream = None
        
        try:
            catalog_stream = open(CATALOG_SAMPLE, 'rb')
            field_map_stream = open(FIELD_MAP_SAMPLE, 'rb')
            
            writer = CatalogMySQLWriter(self.db)
            import_catalog(catalog_stream, field_map_stream, writer)

            self.helper.assert_not_empty('raw_book')
            writer.undo()
            
        finally:
            if None <> catalog_stream: catalog_stream.close()
            if None <> field_map_stream: field_map_stream.close()

    def setUp(self):
        self.db = mysql.connect(**STAGE_DB)
        self.helper = db_test_helper.Helper(self.db, self.fail)

    def tearDown(self):
        self.db.close()

CATALOG_SAMPLE = 'catalog.sample.csv'
FIELD_MAP_SAMPLE = 'field_map.sample.csv'

DB_HOST = 'localhost'
DB_USER = 'bookstore_admin'
DB_PASSWORD = '1234'
STAGE = 'bookstore_stage'
BOOKSTORE = 'bookstore'
DB_CHARSET = 'gbk'

BOOKSTORE_DB = {
    'host' : DB_HOST,
    'user' : DB_USER,
    'passwd' : DB_PASSWORD,
    'db': BOOKSTORE,
    'charset' : DB_CHARSET}

STAGE_DB = {
    'host' : DB_HOST,
    'user' : DB_USER,
    'passwd' : DB_PASSWORD,
    'db': STAGE,
    'charset' : DB_CHARSET}

if '__main__' == __name__:
    unittest.main()
