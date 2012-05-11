# -*- coding:utf8 -*-

from uuid import uuid4
import json
import urllib2
import sys
import traceback

from mongrel2 import handler
import mmseg
from mmseg import seg_txt

sender_id = uuid4().hex

conn = handler.Connection(sender_id, 
    "tcp://127.0.0.1:9991", 
    "tcp://127.0.0.1:9990")

while True:
  req = conn.recv()

  if req.is_disconnect():
    continue
  else:
    query = req.headers.get("QUERY")
    method = req.headers.get("METHOD")

    code = 500
    status = "internal Server Error"
    response = "Server Error"

    try:
      params = dict(
        (n,v) for n, v in (i.split('=', 1) for i in query.split('&')))
      terms = []
      if 'text' in params:
        text = params['text']
        text = urllib2.unquote(params['text'].encode('ascii'))
        
        for term in seg_txt(text):
          terms.append(term.decode('utf8'))
      else:
        terms.append(query)
      code = 200
      status = "OK"
      response = json.dumps(terms, ensure_ascii=False).encode('utf8')

    except:
      traceback.print_exc()
    finally:
      conn.reply_http(req, response, code, status)

