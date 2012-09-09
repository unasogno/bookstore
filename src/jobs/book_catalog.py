# -*- coding:utf8 -*-

class CatalogItem(object):

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
        line = self.__reader.next()
        arguments = {}
        for header in self.__field_map:
            index = self.__field_map[header]
            arguments[header] = line[index] if header in arguments else None

        tags = [
            (header, line[self.__tag_map[header]])
            for header in self.__tag_map]
        arguments['tags'] = tags
            
        return CatalogItem(**arguments)

class CatalogMySQLWriter(object):

    def __init__(self, db):
        self.db = db

    def write(self, item):
        # insert book
        statement = '''insert into book (title, isbn, publisher, list_price,
                        publish_date, class, sheet_numbers, folio, print_type,
                        author, barcode, comments)
                        values ()''' % item.get_values
        # insert book_tag
        self.db.query(statement)

if '__main__' == __name__:
    print 'book catalog'
