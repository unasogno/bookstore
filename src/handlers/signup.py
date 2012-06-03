# _*_ coding=utf8 _*_

import rsa
import json
import handler
import config
import helpers

def put(path, headers, body):
  pass

def get(path, headers, body):
  query = headers.get('QUERY')
  arguments = helpers.parse_query_string(query)
  priv = rsa.PrivateKey.load_pkcs1('priv.txt')
  message = rsa.decrypt(arguments['cipher'], priv)

  return 200, 'OK', message, {
    'Content-Type': 'text/plain'}

def post(path, headers, body):
  pass

def delete(path, headers, body):
  pass

handlers = {
  'PUT': put, 'GET': get, 'post': post, 'delete': delete }
logger = helpers.init_logger('signup', config.LOG_PATH)

if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['signup']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
