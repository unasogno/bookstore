# _*_ coding=utf8 _*_

def is_debug():
  global DEBUG
  try:
    return DEBUG
  except:
    return True

if is_debug():
  import mongrel2_dummy_handler as handler
else:
  from mongrel2 import handler
import json
import Cookie
from uuid import uuid4
import helpers
import config

handler_registry = {}

def run(send_spec, recv_spec, handlers):
  logger = helpers.init_logger('handler', config.LOG_PATH)
  sender_id = uuid4().hex

  conn = handler.Connection(
    sender_id, send_spec, recv_spec)

  while True:
    logger.debug('wait for request')
    req = conn.recv()

    if req.is_disconnect():
      logger.debug('request disconnected')
      continue
    else:
      logger.debug('incoming request')
      method = req.headers.get('METHOD')

      code = 500
      status = 'Internal Server Error'
      response = 'Server Error'
      headers = None
      try:
        if method not in handlers:
          code = 405
          status = 'Method Not Allowed'
          response = 'The given method of %s is not supported' % method
        else:
          code, status, response, headers = handlers[method](
            req.path, req.headers, req.body)
      finally:
        logger.debug('Sending response - %s', response)
        conn.reply_http(req, response, code, status, headers)
        logger.debug('Request handled')
