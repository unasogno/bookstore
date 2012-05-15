# -*- coding:utf8 -*-

import xapian
from mmseg import seg_txt
import handler
import helpers
import config

def get_search(url, headers, body):
  query = headers.get('QUERY')
  params = dict((n,v) for n, v in (i.split('=', 1) for i in s.split('&')))
  text = params['text']
  search_query = helpers.decode_urlencoding(text)
  # helpers.log_search_query(search_query)

  terms = seg_txt(search_query)
  print terms
  return 200, 'OK', ''

logger = helpers.init_logger('search', config.LOG_PATH)

try:
  handlers = { 'GET': get_search }
  handler.run("tcp://127.0.0.1:9993", "tcp://127.0.0.1:9992", handlers)
except:
  logger.error(helpers.format_exception())
