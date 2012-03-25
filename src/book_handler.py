# _*_ coding=utf8 _*_

from mongrel2 import handler
import json
from uuid import uuid4
import logging
import book

LOG_PATH = '/home/kai/mongrel2/logs/book.py.log'
FORMAT = '%(asctime)s - %(name)s -%(levelname)s - %(message)s'

def init_logger():
  logger = logging.getLogger('book_handler')

  formatter = logging.Formatter(FORMAT)

  file_handler = logging.FileHandler(
    filename = LOG_PATH, mode = 'a', encoding = 'utf-8')
  file_handler.setFormatter(formatter)

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)
  logger.setLevel(logging.DEBUG)
  return logger

logger = init_logger()

sender_id = uuid4().hex

conn = handler.Connection(
    sender_id, "tcp://127.0.0.1:9995",
    "tcp://127.0.0.1:9994")

logger.debug('connected')

handlers = {
  'PUT': book.put, 'GET': book.get, 'post': book.post, 'delete': book.delete }

while True:
  logger.debug('waiting for request')

  req = conn.recv()

  if req.is_disconnect():
    logger.debug('disconnect')
    continue
  else:
    query_string = req.headers.get('QUERY')
    logger.debug(query_string)
    method = req.headers.get('METHOD')

    code = 500
    status = 'Internal Server Error'
    response = 'Server Error'
    try:
      code, status, response = handlers[method](
        req.path.split('/book', 1)[1], query_string, req.body)
    except Exception as ex:
      logger.error("Failed to handle request: %s - %s", req, ex)
    finally:
      conn.reply_http(req, response, code, status)
