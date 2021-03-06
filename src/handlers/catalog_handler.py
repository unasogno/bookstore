# -*- coding:utf8 -*-

import handler
import os
import json
import uuid
import hashlib
from StringIO import StringIO
from csv import reader
import MySQLdb as mysql

from catalog import parse_file
from book_catalog import import_catalog
from book_catalog import CatalogMySQLWriter
import helpers
import config

def parse(headers, body):
  boundary = headers.get('boundary')
  lines = body.split('\r\n')
  if lines[0] <> boundary or lines[-1] <> boundary:
    return None, None

  name, value = lines[1].split(':', 1)
  if name <> 'Content-Disposition':
    return None, None

  name, value = lines[2].split(':', 1)
  if name <> 'Content-Type':
    return None, None
  
  content_type = value
  length = len(lines)

  content = StringIO()
  for i in range(3, length - 1):
    content.write(lines[i])
  content.seek(0)
  return content_type, content

def content_type_equals(headers, expected_type):
  content_type = headers.get('content-type', '')
  return content_type.find(expected_type) >= 0  

def get(path, headers, body):
  pass

def post(path, headers, body):
  if headers.get('x-mongrel2-upload-done', None):
    expected = req.headers.get('x-mongrel2-upload-start', "BAD")
    upload = req.headers.get('x-mongrel2-upload-done', None)

    if expected != upload:
      logger.info("GOT THE WRONG TARGET FILE: %s, %s", expected, upload)
      return 400, 'Bad Request', 'invalid format', None

    '''
    content = open(upload, 'r').read()
    print "UPLOAD DONE: BODY IS %d long, content length is %s" % (
            len(body), req.headers['content-length'])
    '''
    with open(upload, 'r') as fp:
      parts = parse_file(fp)
      fp.close()

    if 2 <> len(parts):
      logger.error('bad request - len(parts) == %d', len(parts))
      return 400, 'Bad Request', 'invalid format', None

    db = mysql.connect(**config.DB_PARAMETERS)
    writer = CatalogMySQLWriter(db)
    try:
      import_catalog(
        parts[0].get_content_stream(),
        parts[1].get_content_stream(),
        writer)
    finally:
      db.close()

    response = "UPLOAD GOOD: %s" % hashlib.md5(body).hexdigest()

    return 200, 'OK', response, {
      'Content-Type': 'application/json;charset=UTF-8'}

  elif headers.get('x-mongrel2-upload-start', None):
    logger.debug('begin to upload file - %s', headers)
    return 0, 'Continue', 'Upload Start', None

  elif content_type_equals(headers, 'multipart/form-data'):

    content = StringIO()
    content.write(body)
    content.seek(0)
    parts = parse_file(content)

    if 2 <> len(parts):
      logger.error('bad request - len(parts) == %d', len(parts))
      return 400, 'Bad Request', 'invalid format', None

    db = mysql.connect(**config.DB_PARAMETERS)
    writer = CatalogMySQLWriter(db)
    try:
      import_catalog(
        parts[0].get_content_stream(),
        parts[1].get_content_stream(),
        writer)
    finally:
      db.close()

    response = "UPLOAD GOOD: %s" % hashlib.md5(body).hexdigest()

    return 200, 'OK', response, {
      'Content-Type': 'application/json;charset=UTF-8'}

  else:
    return 200, 'OK', 'unknown request', None

handlers = { 'POST': post }
logger = helpers.init_logger('catalog_handler', config.LOG_PATH)

if '__main__' == __name__:
  try:
    handler_config = config.HANDLER_CONFIG['catalog_handler']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handler_registry[__name__] = handlers
