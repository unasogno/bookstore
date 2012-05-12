# -*- coding:utf8 -*-

from mmseg import seg_text
import config

class Book(object):
  
  def __init__(self, data, docid = None):
    self._data = data
    self._docid = docid

  def get_docid():
    return self._docid

  def set_docid(docid):
    self._docid = docid

  def get_data():
    return self._data

  def get_terms():
    fields = config.BOOK_INDEXED_FIELDS

    values = []
    for field in fields:
      values.append(data[field].encode('utf8'))

    text = ' '.join(values)

    terms = []
    for term in seg_text(text):
      terms.add(term.decode('utf8'))

    return terms
