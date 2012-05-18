# -*- coding:utf8 -*-

class HandlerConfig(object):
  
  def __init__(self, module_name, send_spec, recv_spec):
    self.module_name = module_name
    self.send_spec = send_spec
    self.recv_spec = recv_spec

LOG_PATH = 'log/search.log'
HANDLER_CONFIG = {
    'search': HandlerConfig('search', 'tcp://127.0.0.1:9993', 'tcp://127.0.0.1:9992'),
    'book': HandlerConfig('book', 'tcp://127.0.0.1:9995', 'tcp://127.0.0.1:9994')
  }
