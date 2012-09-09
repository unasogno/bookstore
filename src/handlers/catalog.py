# -*- coding:utf8 -*-

from mongrel2 import handler
import json
import hashlib
from StringIO import StringIO

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

def get(path, headers, body):
  pass

def post(path, headers, body):
  if headers.get('x-mongrel2-upload-done', None):
    expected = req.headers.get('x-mongrel2-upload-start', "BAD")
    upload = req.headers.get('x-mongrel2-upload-done', None)

    if expected != upload:
      logger.info("GOT THE WRONG TARGET FILE: %s, %s", expected, upload)
      return

    content = open(upload, 'r').read()
    print "UPLOAD DONE: BODY IS %d long, content length is %s" % (
            len(body), req.headers['content-length'])

    response = "UPLOAD GOOD: %s" % hashlib.md5(body).hexdigest()

  elif headers.get('x-mongrel2-upload-start', None):
    logger.debug('begin to upload file - %s', headers)
    return

  elif 'multipart/form-data' == headers.get('content-type', None):
    logger.debug("body = %s", body)
    content_type, content = parse(headers, body)

handlers = { 'POST': post }
logger = helpers.init_logger()

if '__main__' == __name__:
  try:
    handler_config = config.HANDLER_CONFIG['catalog']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handler_registry[__name__] = handlers
