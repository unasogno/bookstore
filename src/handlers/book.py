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

def put(path, query, body):
  pass

def get(path, query, body):
  if ('/' == path.strip()):
    arguments = __extract_arguments(query)
  else:
    book_id = path.split('/')[1]
    
    if (not book_id.isdigit()):
      return 400, 'Bad Request', 'book id expected', None
    
    arguments = { 'book_id': book_id }  
        
  return 200, 'OK', da.query_book(arguments), {
    'Content-Type': 'application/json;charset=UTF-8'}

def post(path, query, body):
  pass

def delete(path, query, body):
  pass

handlers = {
  'PUT': put, 'GET': get, 'post': post, 'delete': delete }


if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['book']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
