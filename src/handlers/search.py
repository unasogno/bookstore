# -*- coding:utf8 -*-

import xapian
from mmseg import seg_txt
import json
import handler
import helpers
import config

def get(url, headers, body):
  query = headers.get('QUERY')
  if query.strip() == '':
    return 400, 'Bad Request', 'query field is not found.', None
  params = dict((n,v) for n, v in (i.split('=', 1) for i in query.split('&')))
  if 'query' not in params:
    return 400, 'Bad Request', 'query field is not found.', None
  text = params['query']
  search_query = helpers.decode_urlencoding(text)
  # helpers.log_search_query(search_query)
  global logger
  logger.debug('incoming query: %s', text)

  terms = seg_txt(search_query)

  logger.debug('terms from query: %s', terms)

  database = xapian.Database('../indexes/')
  enquire = xapian.Enquire(database)

  l = []
  for term in terms:
    l.append(term)

  q = xapian.Query(xapian.Query.OP_OR, l)

  enquire.set_query(q)
  matches = enquire.get_mset(0, 100)

  print '%i results found.' % matches.get_matches_estimated()
  print 'Result - %i:' % matches.size()

  r = []
  for m in matches:
    # print '%i: %i%% docid=%i [%s]' % (m.rank + 1, m.percent, m.docid,\
    # m.document.get_data())
    r.append(m.document.get_data())

  print json.dumps(r)

  return 200, 'OK', json.dumps(r), None 

handlers = { 'GET': get }
logger = helpers.init_logger('search', config.LOG_PATH)

if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['search']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
