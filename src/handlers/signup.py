 # _*_ coding=utf8 _*_

import rsa
import hashlib
import json
import base64
import handler
import config
import helpers

def load_private():
  with open('private.pem', 'r') as fp:
    pem = fp.read()
    fp.close()
  return rsa.PrivateKey.load_pkcs1(pem)

def decrypt(cipher, priv):
  global logger
  cipher = helpers.decode_urlencoding(cipher)
  cipher = int(cipher, 16)
  logger.debug('cipher = %d', cipher)

  cipher = rsa.transform.int2bytes(cipher)
  return rsa.decrypt(cipher, priv)

def is_email(identity):
  return True

def is_phone_number(identity):
  return True

def create_with_email(identity, password):
  pass

def create_with_phone_number(identity, password):
  pass

def put(path, headers, body):
  pass

def get(path, headers, body):
  global logger

  query = headers.get('QUERY')
  arguments = helpers.parse_query_string(query)

  try:
    priv = load_private()
    identity = decrypt(arguments['identity'], priv)
    if is_email(identity):
      password = decrypt(arguments['password'], priv)
      password = hashlib.new('md5', password).hexdigest()
      create_with_email(identity, password)
    elif is_phone_number(identity):
      password = decrypt(arguments['password'], priv)
      password = hashlib.new('md5', password).hexdigest()
      create_with_phone_number(identity, password)
    else:
      pass

    return 200, 'OK', message, {
      'Content-Type': 'text/plain'}
  except rsa.DecryptionError:
    logger.error(helpers.format_exception())
    return 500, 'Internal Server Error', 'Decryption failed', {}

def post(path, headers, body):
  pass

def delete(path, headers, body):
  pass

handlers = {
  'PUT': put, 'GET': get, 'post': post, 'delete': delete }
logger = helpers.init_logger('signup', config.LOG_PATH)

if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['signup']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
