# _*_ coding=utf8 _*_

import logging
import traceback
import sys
import urllib2

FORMAT = '%(asctime)s - %(name)s -%(levelname)s - %(message)s'

def init_logger(name, log_path):
  logger = logging.getLogger(name)

  formatter = logging.Formatter(FORMAT)

  file_handler = logging.FileHandler(
    filename = log_path, mode = 'a', encoding = 'utf-8')
  file_handler.setFormatter(formatter)

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)
  logger.setLevel(logging.DEBUG)
  return logger

def to_binary_string(text):
  binary = bytearray(text)
  string = ''
  for char in binary:
    string += '%d ' % char
  return string

def print_chars(text, printer = None):
  chars = bytearray(text)
  chars_list = [hex(char) for char in chars]
  if None == printer:
    print chars_list
  else:
    printer(chars_list)
      

def format_exception():
  return traceback.format_exc()

def decode_urlencoding(text):
   return urllib2.unquote(text.encode('utf8'))

def parse_query_string(query):
  if (None == query):
    return None;
  return dict((n,v) for n, v in (i.split('=', 1) for i in query.split('&')))

def pad_str(str, total, pad_left = True, char = '0'):
  length = total - len(str)
  if length == 0: return str
  if length < 0:
    raise ValueError('string too long to pad - \'%s\'' % str)
  if len(char) > 1:
    raise ValueError('padding character too long - \'%s\'' % char)
  if pad_left:
    return char * length + str
  else:
    return str + char * length

