# -*- coding:utf8 -*-

import handler
import helpers
import config

def get_search(url, header, body):
  query = req.headers.get('QUERY')

logger = helpers.init_logger('search', config.LOG_PATH)

try:
  handlers = { 'GET': get_search }
  handler.run(handlers)
except:
  logger.error(helpers.format_exception())
