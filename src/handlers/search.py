# -*- coding:utf8 -*-

import xapian
from mmseg import seg_txt
import handler
import helpers
import config

def get_search(url, headers, body):
  query = headers.get('QUERY')
  params = dict((n,v) for n, v in (i.split('=', 1) for i in query.split('&')))
  text = params['terms']
  search_query = helpers.decode_urlencoding(text)
  # helpers.log_search_query(search_query)

  terms = seg_txt(search_query)

  database = xapian.Database('../indexes/')
  enquire = xapian.Enquire(database)

  l = []
  for term in terms:
    l.append(term)

  q = xapian.Query(xapian.Query.OP_OR, l)

  enquire.set_query(q)
  matches = enquire.get_mset(0, 10)

  print '%i results found.' % matches.get_matches_estimated()
  print 'Result - %i:' % matches.size()

  for m in matches:
    print '%i: %i%% docid=%i [%s]' % (m.rank + 1, m.percent, m.docid,\
    m.document.get_data())

  return 200, 'OK', ''

logger = helpers.init_logger('search', config.LOG_PATH)

try:
  handlers = { 'GET': get_search }
  handler.run("tcp://127.0.0.1:9993", "tcp://127.0.0.1:9992", handlers)
except:
  logger.error(helpers.format_exception())
