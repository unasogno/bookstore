# -*- coding:utf8 -*-

import MySQLdb as mysql
import document
import config

class Inventory(object):
  
  def __init__(self):
    pass

  def begin_trans(self):
    pass

  def commit(self):
    pass

  def rollback(self):
    pass

  def close(self):
    pass

  def update_high_water_mark(self):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST) 

    try:
      statement = '''
                  update high_water_mark, 
                  (
                    select max(time_stamp) mark from book
                  ) mark 
                  set time_stamp = mark.mark 
                  where app_id = 1 and entity_id = 1;
                  '''

      db.query(statement)
      db.commit()
    except:
      db.rollback()
      raise
    finally:
      db.close()

  def add_mapping(self, docs):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST) 

    try:
      statement = '''
                  INSERT INTO book_index (book_id, doc_id)
                  VALUES (%s, %d);
                  '''

      for doc in docs:
        db.query(statement % (doc.get_data(), doc.get_docid()))

      db.commit()
    except:
      db.rollback()
      raise
    finally:
      db.close()


  def get_new_documents(self):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST,
      charset = 'utf8', use_unicode = True) 

    try:
      statement = '''
                  SELECT b.book_id, title, isbn, p.name as publisher, 
                    BIN(year(publish_date)) as publish_year, 
                    `class`, author
                  FROM book b
                  INNER JOIN publisher p
                    on b.publisher_id = p.publisher_id
                  LEFT JOIN book_index bi
                    on b.book_id = bi.book_id
                  WHERE doc_id IS NULL
                  ORDER BY book_id;
                  '''
      db.query(statement)

      result = db.store_result()
      total = db.affected_rows()
      rows = result.fetch_row(total)
     
      for row in rows:
        yield document.Book(row, [1, 2, 3, 4, 5, 6]) 
    except:
      db.rollback()
      raise
    finally:
      db.close()

  def get_updated_documents(self):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST,
      charset = 'utf8', use_unicode = True)

    try:
      statement = '''
                  SELECT time_stamp FROM high_water_mark 
                  WHERE entity_id = 1 AND app_id = 1; 
                  '''
      db.query(statement)
      result = db.store_result()
      if 0 == db.affected_rows():
        mark = '0000-00-00 00:00:00'
      else:
        mark = result.fetch_row()[0]

      statement = '''
                  SELECT b.book_id, title, isbn, p.name as publisher, 
                    BIN(year(publish_date)) as publish_year, 
                    `class`, author
                  FROM book b
                  INNER JOIN publisher p
                    on b.publisher_id = p.publisher_id
                  INNER JOIN book_index bi
                    on b.book_id = bi.book_id
                  WHERE b.time_stamp > '%s'
                  ORDER BY book_id;
                  ''' % mark
      db.query(statement)

      result = db.store_result()
      total = db.affected_rows()
      rows = result.fetch_row(total)

      for row in rows:
        yield document.Book(row, [1, 2, 3, 4, 5, 6]) 
    except:
      db.rollback()
      raise
    finally:
      db.close()
