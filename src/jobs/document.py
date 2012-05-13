# -*- coding:utf8 -*-

from mmseg import seg_txt
import config

class Book(object):
  
  def __init__(self, data, fields, docid = 0):
    self._data = data
    self._fields = fields
    self._docid = docid

  def get_docid(self):
    return self._docid

  def set_docid(docid):
    self._docid = docid

  def get_data(self):
    return self._data[0]

  def get_terms(self):
    values = []
    for field in self._fields:
      values.append(self._data[field].encode('utf8'))

    text = ' '.join(values)

    terms = []
    for term in seg_txt(txt):
      terms.add(term.decode('utf8'))

    return terms
