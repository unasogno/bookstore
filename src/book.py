# _*_ coding=utf8 _*_

import json
import data_access as da

def __extract_arguments(s):
  if (None == s):
    return None;
  return dict((n,v) for n, v in (i.split('=', 1) for i in s.split('&')))

def put(path, query, body):
  pass

def get(path, query, body):
  if ('/' == path.strip()):
    arguments = __extract_arguments(query)
  else:
    book_id = path.split('/')[1]
    
    if (not book_id.isdigit()):
      return 400, 'Bad Request', 'book id expected', None
    
    arguments = { 'book_id': book_id }  
        
  return 200, 'OK', da.query_book(arguments), {
    'Content-Type': 'application/json;charset=UTF-8'}

def post(path, query, body):
  pass

def delete(path, query, body):
  pass
