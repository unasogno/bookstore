# -*- coding:utf8 -*-

import handler
import helpers
import config

def get_search(url, header, body):
  query = headers.get('QUERY')
  print query

logger = helpers.init_logger('search', config.LOG_PATH)

try:
  handlers = { 'GET': get_search }
  handler.run("tcp://127.0.0.1:9993", "tcp://127.0.0.1:9992", handlers)
except:
  logger.error(helpers.format_exception())
