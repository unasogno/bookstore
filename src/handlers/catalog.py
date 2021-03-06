# -*- coding:utf8 -*-

import os
import uuid

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
    self.content_file = None
    
  def get_content_stream(self):
    if None <> self.stream:
      self.stream.close()
    if not os.path.exists(self.content_file):
      return None
    self.stream = open(self.content_file, 'r')
    return self.stream

  def __del__(self):
    if None <> self.stream:
      self.stream.close()
      self.stream = None
    if os.path.exists(self.content_file):
      os.remove(self.content_file)

  @staticmethod
  def parse(stream, boundary):
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

    # body
    # todo: implement dispose method to release stream object
    filename = str(uuid.uuid4())
    path = config.TMP_PATH + filename
    with open(path, 'wb+') as output_stream:
      
      while True:
        line = stream.readline()
        if '' == line: raise RequestBodyError('Missing boundary')
        # encoding of body could be various
        '''
        if line.startswith('---'):
          print 'line = <%s>' % line
          if not line.startswith(boundary):
            print 'boundary => [%s]' % helpers.to_binary_string(boundary)
            print 'line => [%s]' % helpers.to_binary_string(line)
        '''
        
        if line.startswith(boundary):
          break
        output_stream.write(line)
      output_stream.flush()
      output_stream.close()
      part.content_file = path
      
    return part

def parse_file(stream):
  parts = []

  boundary = stream.readline()
  if '' == boundary: return parts
  boundary = boundary[:-2] # trim the tailing '\r\n'
  
  while True:
    part = Part.parse(stream, boundary)
    if None == part: break
    parts.append(part)

  return parts

# logger = helpers.init_logger('catalog', config.LOG_PATH)
