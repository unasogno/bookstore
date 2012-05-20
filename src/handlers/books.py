# _*_ coding=utf8 _*_

import json
import handler
import data_access as da
import config
import helpers

def post(path, query, body):
  if None == body:
    return 400, 'Bad Request', 'book id expected', None
  
  try:  
    id_list = helpers.decode_urlencoding(body)
    logger.debug(id_list)
    if '' == id_list.strip():
      return 400, 'Bad Request', 'book id expected', None
    '''  
    if (not book_id.isdigit()):
      return 400, 'Bad Request', 'book id expected', None
    '''
  except:
    return 500, 'Internal Server Error', 'unknown error', None
  
  try:
    ''' 
    return 200, 'OK', da.query_books(id_list), {
      'Content-Type': 'application/json;charset=UTF-8'}
    '''
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
