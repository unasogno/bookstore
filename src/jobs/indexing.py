# -*- coding:utf8 -*-

import xapian
import config

class Indexer(object):
  def __init__(self):
    self._db = xapian.WritableDatabase(
      config.INDEX_PATH, xapian.DB_CREATE_OR_OPEN)

  def create_index(self, item):
    doc = self._create_doc(item)
    docid = self._db.add_document(doc)
    item.set_docid(docid)

  def update_index(self, item):
    doc = self._create_doc(item)
    docid = item.get_docid()
    self._db.replace_document(docid, doc)

  def _create_doc(self, item):
    terms = item.get_terms()
    doc = xapian.Document()
    for term in terms:
      doc.add_term(term)
    doc.set_data(item.get_data())
    return doc

  def begin_trans(self):
    self._db.begin_transaction()

  def commit(self):
    self._db.commit_transaction()
    self._db.flush()

  def rollback(self):
    self._db.cancel_transaction()

  def close(self):
    self._db.flush()

def process(lib):

  indexer = Indexer()

  lib.begin_trans()
  indexer.begin_trans()

  try:
    
    for doc in lib.get_updated_documents():
      indexer.update_index(doc)

    incremental = []
    for doc in lib.get_new_documents():
      indexer.create_index(doc)
      incremental.append(doc)
    lib.add_mapping(incremental)
    lib.update_high_water_mark()

    lib.commit()
    indexer.commit()
  except:
    lib.rollback()
    indexer.rollback()
    raise

  finally:
    lib.close()

