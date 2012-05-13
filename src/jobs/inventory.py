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

  def add_mapping(self, docs):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST) 

    try:
      statement = '''
                  INSERT INTO book_index (book_id, doc_id)
                  VALUES (%d, %d);
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
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST) 

    try:
      statement = '''
                  SELECT book_id, title, isbn, p.name as publisher, 
                    year(publish_date) as publish_year, `class`, author
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
      
    except:
      db.rollback()
      raise
    finally:
      db.close()

  def get_updated_documents(self):
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PWD, config.DB_INST)

    try:
      statement = '''
                  SELECT book_id, title, isbn, p.name as publisher, 
                    year(publish_date) as publish_year, `class`, author
                  FROM book b
                  INNER JOIN publisher p
                    on b.publisher_id = p.publisher_id
                  INNER JOIN book_index bi
                    on b.book_id = bi.book_id
                  ORDER BY book_id;
                  '''
      db.query(statement)

      result = db.store_result()
      total = db.affected_rows()
      rows = result.fetch_row(total)
    except:
      db.rollback()
      raise
    finally:
      db.close()
