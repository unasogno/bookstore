# -*- coding:utf8 -*-

from uuid import uuid4
import json
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
        for term in seg_txt(text):
          terms.append(term)
      else:
        terms.append(query)

      code = 200
      status = "OK"
      response = json.dumps(terms)

    except:
      pass
    finally:
      conn.reply_http(req, response, code, status)

