# -*- coding:utf8 -*-

DEBUG = True

class HandlerConfig(object):
  
  def __init__(self, module_name, send_spec, recv_spec):
    self.module_name = module_name
    self.send_spec = send_spec
    self.recv_spec = recv_spec

HANDLER_CONFIG = {
    'books':  HandlerConfig(
      'books',  'tcp://127.0.0.1:9997', 'tcp://127.0.0.1:9996'),
    'book':   HandlerConfig(
      'book',   'tcp://127.0.0.1:9995', 'tcp://127.0.0.1:9994'),
    'search': HandlerConfig(
      'search', 'tcp://127.0.0.1:9993', 'tcp://127.0.0.1:9992'),
    'signup': HandlerConfig(
      'signup', 'tcp://127.0.0.1:9989', 'tcp://127.0.0.1:9988'),
    'signin': HandlerConfig(
      'signin', 'tcp://127.0.0.1:9987', 'tcp://127.0.0.1:9986'),
    'catalog_handler': HandlerConfig(
      'catalog_handler', 'tcp://127.0.0.1:9985', 'tcp://127.0.0.1:9984')
  }

LOG_PATH = 'log/search.log'
TMP_PATH = 'tmp/'

DB_HOST = '127.0.0.1'
DB_USER = 'api'
DB_PASSWORD = '123'
DB_INST = 'bookstore'

DB_PARAMETERS = {
  'host' : DB_HOST, 'user' : DB_USER, 'passwd' : DB_PASSWORD, 'db': DB_INST}
