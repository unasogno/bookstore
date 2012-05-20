# _*_ coding=utf8 _*_

import json
import handler
import data_access as da
import config
import helpers

def __extract_arguments(s):
  if (None == s):
    return None;
  return dict((n,v) for n, v in (i.split('=', 1) for i in s.split('&')))

def post(path, query, body):
  if None == body:
    return 400, 'Bad Request', 'book id expected', None
  
  try:  
    decoded = helpers.decode_urlencoding(body)
    arguments = __extract_arguments(decoded)
    if 'idList' not in arguments:
      return 400, 'Bad Request', 'book id expected', None

    id_str = arguments['idList']
    if '' == id_str.strip():
      return 400, 'Bad Request', 'book id expected', None
    '''  
    if (not book_id.isdigit()):
      return 400, 'Bad Request', 'book id expected', None
    '''
  except:
    return 500, 'Internal Server Error', 'unknown error', None
  
  try:
    return 200, 'OK', da.query_books(id_str), {
      'Content-Type': 'application/json;charset=UTF-8'}
    return 200, 'OK', 'Test', None 
  except:
    return 500, 'Internal Server Error' 'database error', None

handlers = { 'POST': post }
logger = helpers.init_logger('books', config.LOG_PATH)

if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['books']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
