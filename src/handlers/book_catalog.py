# -*- coding:utf8 -*-

import csv
import helpers

def parse_field_map(stream):
    csv_reader = csv.reader(stream, delimiter=':', quotechar='"')
      
    field_map = {}
    for line in csv_reader:
        field_map[line[0]] = int(line[1])
      
    return field_map
    
def import_catalog(catalog_stream, field_map_stream, writer):
    catalog_reader = csv.reader(catalog_stream)
    field_map = parse_field_map(field_map_stream)
    
    reader = CatalogReader(catalog_reader, field_map)

    writer.begin_write()

    try:
        while True:
            item = reader.read()
            if None == item: break
            writer.write(item)

        writer.apply()
    except:
        writer.undo()
        raise

class CatalogItem(object):

    @staticmethod
    def meta():
        
        class DateField(object):
            '''
            supported date format:
            1. yyyy-MM-dd
            2. yyyy-MM
            3. yyyy.MM.dd
            4. yyyy.MM
            5. yyyy

            acceptable inputs:
            1. digit: 0-9
            2. delimiter: '.; and '-'
            '''
            
            def extract(self, literal):
                tokens = self._parse_token(literal)

            def _parse_token(self, literal):
                tokens = []
                token = []
                state = None
                
                def statemata(char):
                    if char.isdigit():
                        token.append(char)
                    elif char == '-':
                        if len(token) > 0:
                            tokens.append(''.join(token))
                    
                for c in literal:
                    statemata(c)
            
        class Meta(object):
            def __init__(self):
                self.fields = { 'publish_date' : DateField() }

        return Meta()

    def __init__(self, title, isbn, publisher, list_price, publish_date, class_,
                 sheet_numbers, folio, print_type, author, barcode, comments,
                 tags):
        self.title = title
        self.isbn = isbn
        self.publisher = publisher
        self.list_price = list_price
        self.publish_date = publish_date
        self.class_ = class_
        self.sheet_numbers = sheet_numbers
        self.folio = folio
        self.print_type = print_type
        self.author = author
        self.barcode = barcode
        self.comments = comments
        self.tags = tags

    def get_values(self):
        '''
        return (self.title.decode('gbk'), self.isbn.decode('gbk'),
                self.publisher.decode('gbk'), self.list_price.decode('gbk'),
                self.publish_date.decode('gbk'), self.class_.decode('gbk'),
                self.sheet_numbers, self.folio,
                self.print_type.decode('gbk'), self.author.decode('gbk'),
                self.barcode.decode('gbk'), self.comments.decode('gbk'))
        '''
        return (self.title, self.isbn,
                self.publisher, self.list_price,
                self.publish_date, self.class_,
                self.sheet_numbers, self.folio,
                self.print_type, self.author,
                self.barcode, self.comments)


    def __str__(self):
        properties = {'title':self.title, 'isbn':self.isbn,
                    'publisher':self.publisher,'list_price':self.list_price,
                    'publish_date':self.publish_date, 'class':self.class_,
                    'sheet_numbers':self.sheet_numbers, 'folio':self.folio,
                    'print_type':self.print_type, 'author':self.author,
                    'barcode':self.barcode, 'comments':self.comments}
        
        return str(properties)

class CatalogReader(object):

    def __init__(self, csv_reader, field_map):
        self.__reader = csv_reader
        self.__headers = csv_reader.next()
        self.__field_map = field_map

        all_headers = set(self.__headers)
        required_headers = set(self.__field_map.keys())
        tag_headers = list(all_headers - required_headers)

        self.__tag_map = dict(
            [(header, self.__headers.index(header))
            for header in tag_headers])

    def read(self):
        try:
            line = self.__reader.next()
        except:
            return None
        arguments = {}
        for header in self.__field_map:
            index = self.__field_map[header]
            arguments[header] = line[index] if index < len(line) else None

        tags = dict(
            (header, line[self.__tag_map[header]])
            for header in self.__tag_map)
        arguments['tags'] = tags
            
        return CatalogItem(**arguments)

class CatalogMySQLWriter(object):

    def __init__(self, db, encoding = 'gbk'):
        self.db = db
        self.job_id = 0
        self.encoding = encoding

    def begin_write(self):
        # self.db.query('set names %s;' % self.encoding)
        
        statement = 'insert into job (date_added) values (now());'
        self.db.query(statement)
        self.job_id = self.db.insert_id()
        return self.job_id

    def apply(self):
        statement = '''
                    CALL sp_apply_job(%d);
                    ''' % self.job_id
        self.db.query(statement)
        self.db.commit()

    def undo(self):
        '''
        discard all the changes made by the current job.
        '''
        
        statement = "delete from raw_code where job_id = %d;" % self.job_id
        self.db.query(statement)
        
        statement = "delete from raw_publisher where job_id = %d;" % self.job_id
        self.db.query(statement)
        
        statement = "delete from raw_tag where job_id = %d;" % self.job_id
        self.db.query(statement)
        
        statement = "delete from raw_book where job_id = %d;" % self.job_id
        self.db.query(statement)

        statement = "delete from job where job_id = %d;" % self.job_id
        self.db.query(statement)

        self.db.commit()

    def write(self, item):
        # insert book
        arguments = (self.job_id,) + item.get_values()
        statement = '''
                    insert into raw_book (job_id, title, isbn, publisher,
                    list_price, publish_date, class, sheet_numbers, folio,
                    print_type, author, barcode, comments) values
                    ('%d', '%s', '%s', '%s', '%s', '%s', '%s', 
                    %s, '%s', '%s', '%s', '%s', '%s')
                    ''' % arguments
        self.db.query(statement)

        # insert book_tag
        book_id = self.db.insert_id()
        for tag_name in item.tags:
            tag_value = item.tags[tag_name]
            statement = '''
                        insert into raw_tag
                        (job_id, book_id, tag_name, tag_value)
                        values
                        (%d, %d, '%s', '%s');
                        ''' % (self.job_id, book_id, tag_name, tag_value)
            self.db.query(statement)

        # insert publisher
        statement = '''
                    select publisher_id from raw_publisher where `name` = '%s'
                    ''' % item.publisher
        self.db.query(statement)
        result = self.db.store_result()
        row = result.fetch_row()

        row_count = self.db.affected_rows()
        if 0 == row_count:
            statement = '''
                        insert into raw_publisher
                        (job_id, `name`, date_added)
                        values
                        (%d, '%s', now())
                        ''' % (self.job_id, item.publisher)
            self.db.query(statement)
            publisher_id = self.db.insert_id()
        elif 1 == row_count:
            publisher_id = row[0][0]
        else:
            raise Exception()

        statement = '''
                    update raw_book set publisher_id = %d
                    where book_id = %d
                    ''' % (publisher_id, book_id)
        self.db.query(statement)

        # todo: write back to raw_book

        statement = "CALL sp_add_code(%d, 7, '%s')" % (self.job_id, item.folio)
        helpers.execute_result(statement, self.db)

        # todo: write back to raw_book
        
        statement = "CALL sp_add_code(%d, 8, '%s')" % (
            self.job_id, item.print_type)
        helpers.execute_result(statement, self.db)

if '__main__' == __name__:
    print 'book catalog'
