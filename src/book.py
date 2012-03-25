# _*_ coding=utf8 _*_

from mongrel2 import handler
import json
from uuid import uuid4
import logging
import data_access as da

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

def extract_arguments(s):
  if (None == s):
    return None;
  return dict((n,v) for n, v in (i.split('=', 1) for i in s.split('&')))

logger = init_logger()

sender_id = uuid4().hex

conn = handler.Connection(
    sender_id, "tcp://127.0.0.1:9995",
    "tcp://127.0.0.1:9994")

logger.debug('connected')

while True:
  logger.debug('waiting for request')

  req = conn.recv()

  if req.is_disconnect():
    logger.debug('disconnect')
    continue
  else:
    query_string = req.headers.get('QUERY')
    arguments = extract_arguments(query_string)
    logger.debug(arguments)
    json = da.query_book(arguments)
    response = json

  conn.reply_http(req, response)
