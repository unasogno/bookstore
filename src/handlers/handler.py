# _*_ coding=utf8 _*_

from mongrel2 import handler
import json
from uuid import uuid4

def run(send_spec, recv_spec, handlers):
  sender_id = uuid4().hex

  conn = handler.Connection(
    sender_id, send_spec, recv_spec)

  while True:
    req = conn.recv()

    if req.is_disconnect():
      continue
    else:
      method = req.headers.get('METHOD')

      code = 500
      status = 'Internal Server Error'
      response = 'Server Error'
      try:
        if method not in handlers:
          code = 405
          status = 'Method Not Allowed'
          response = 'The given method of %s is not supported' % method
        else:
          code, status, response = handlers[method](
            req.path, req.headers, req.body)
      except:
        raise
      finally:
        conn.reply_http(req, response, code, status)