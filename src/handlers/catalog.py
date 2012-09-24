# -*- coding:utf8 -*-

# from mongrel2 import handler
import json
import hashlib
from StringIO import StringIO

import helpers
import config

class RequestBodyError(Exception):
  pass

class MapFormatError(Exception):
  pass

class CatalogFormatError(Exception):
  pass

class Part(object):
  pass

def parse_file(stream):
  parts = []
  
  boundary = stream.readline()
  if '' == boundary: return parts
  boundary = boundary[:-1]
  print 'boundary => "%s"' % boundary
  
  while True:
    part = parse_part(stream, boundary)
    if None == part: break
    parts.append(part)

  return parts

def parse_part(stream, boundary):
  line = stream.readline()
  if '' == line: return None

  part = Part()

  def parse_attribute(attribute, expected_name):
    if expected_name <> attribute[0].strip():
      raise RequestBodyError('expecting %s' % expected_name)
    return attribute[1].strip()

  # Content-Disposition: form-data; name="file1"; filename="3.txt"
  attributes = line.split(';')
  
  attribute = attributes[0].split(':')
  part.content_disposition = parse_attribute(attribute, 'Content-Disposition')

  attribute = attributes[1].split('=')
  part.name = parse_attribute(attribute, 'name')[1:-1]
  
  attribute = attributes[2].split('=')
  part.filename = parse_attribute(attribute, 'filename')[1:-1]

  # Content-Type: text/plain
  line = stream.readline()
  if '' == line: raise RequestBodyError('expecting Content-Type')
  attribute = line.split(':')
  part.content_type = parse_attribute(attribute, 'Content-Type')
  
  while True:
    line = stream.readline()
    if '' == line: raise RequestBodyError('Missing boundary')
    print 'reading =>', line
    if line.startswith(boundary):
      break
    else:
      print '"%s" doesn\'t start with "%s"' % (line, boundary)
  return part

def parse_attributes(string):
  print 'parsing', string
  return dict((n.strip(),v.strip()) \
              for n, v in (i.split('=', 1) \
                           for i in string.split(';')))

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
logger = helpers.init_logger('book', config.LOG_PATH)

if '__main__' == __name__:
  try:
    handler_config = config.HANDLER_CONFIG['catalog']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  pass
  # handler.handler_registry[__name__] = handlers
