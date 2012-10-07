# -*- coding:utf8 -*-

import handler
import os
import json
import uuid
import hashlib
from StringIO import StringIO
from csv import reader

import helpers
import config

class RequestBodyError(Exception):
  pass

class MapFormatError(Exception):
  pass

class CatalogFormatError(Exception):
  pass

class Part(object):
  def __init__(self):
    self.stream = None
    
  def get_content_stream(self):
    if None <> self.stream:
      self.stream.close()
    if not os.path.exists(self.content_file):
      return None
    self.stream = open(self.content_file, 'r')
    return self.stream

  def dispose(self):
    if None <> self.stream:
      self.stream.close()
      self.stream = None
    if os.path.exists(self.content_file):
      os.remove(self.content_file)

def parse_field_map(stream):
  csv_reader = reader(stream, delimiter=':', quotechar='"')
  
  field_map = {}
  for line in csv_reader:
    field_map[line[0]] = int(line[1])
  
  return field_map

def parse_file(stream):
  parts = []
  
  boundary = stream.readline()
  if '' == boundary: return parts
  boundary = boundary[:-1]
  
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

  # Content-Disposition: form-data; name="name"; filename="filename.ext"
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

  line = stream.readline()
  print line

  # body
  # todo: implement dispose method to release stream object
  filename = str(uuid.uuid4())
  path = config.TMP_PATH + filename
  with open(path, 'wb+') as output_stream:
    
    while True:
      line = stream.readline()
      if '' == line: raise RequestBodyError('Missing boundary')
      if line.startswith(boundary):
        break
      output_stream.write(line)
    output_stream.flush()
    output_stream.close()
    part.content_file = path
    
  return part

def parse_attributes(string):
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

def import_catalog(catalog, field_map):
  pass

def post(path, headers, body):
  if headers.get('x-mongrel2-upload-done', None):
    expected = req.headers.get('x-mongrel2-upload-start', "BAD")
    upload = req.headers.get('x-mongrel2-upload-done', None)

    if expected != upload:
      logger.info("GOT THE WRONG TARGET FILE: %s, %s", expected, upload)
      return

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
      # todo: return HTTP status code
      return 400, 'Bad Request', 'invalid format', None

    import_catalog(parts[0].get_content_stream(), parts[1].get_content_stream())

    response = "UPLOAD GOOD: %s" % hashlib.md5(body).hexdigest()

    return 200, 'OK', response, {
      'Content-Type': 'application/json;charset=UTF-8'}

  elif headers.get('x-mongrel2-upload-start', None):
    logger.debug('begin to upload file - %s', headers)
    # todo: returns nothing?
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
  handler.handler_registry[__name__] = handlers
