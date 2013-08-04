# _*_ coding=utf8 _*_

import rsa
import json
import base64
import handler
import user
import config
import helpers

def load_private():
  # DO NOT CACHE for the priviate key could be changed
  with open('priv.txt', 'r') as fp:
    pem = fp.read()
    fp.close()
  return rsa.PrivateKey.load_pkcs1(pem)

def decrypt(cipher, priv):
  global logger
  if '' == cipher:
    logger.warn('Null cipher')
    return None
  try:
    cipher = helpers.decode_urlencoding(cipher)
    cipher = int(cipher, 16)
  except:
    logger.warn('Unrecognized cipher = %s', cipher)
    return None
  logger.debug('cipher = %d', cipher)

  cipher = rsa.transform.int2bytes(cipher)
  return rsa.decrypt(cipher, priv)

def put(path, headers, body):
  pass

def get(path, headers, body):
  global logger

  query = headers.get('QUERY')
  if None == query:
    return 400, 'Bad Request', 'Missing argument(s)', {}
  arguments = helpers.parse_query_string(query)
  if 'identity' not in arguments:
    return 400, 'Bad Request', 'Missing argument(s)', {}
  if 'password' not in arguments:
    return 400, 'Bad Request', 'Missing argument(s)', {}

  try:
    priv = load_private()
    
    identity_str = decrypt(arguments['identity'], priv)
    if None == identity_str:
      message = 'The login of "%s" does not exist.' % identity_str
      return 404, 'Not found', message, {}    
    password = decrypt(arguments['password'], priv)
    if None == password:
      return 401, 'Unauthorized', 'Incorrect password.', {}
    
    db = user.Database()
    identity = user.Identity.load(db, identity_str)
    if None == identity: 
      message = 'The login of "%s" does not exist.' % identity_str
      return 404, 'Not found', message, {}
    if identity.validate(password):
      token = identity.create_token(db)
      return 200, 'OK', token, {'Content-Type': 'text/plain'}
    else:
      return 401, 'Unauthorized', 'Incorrect password.', {}
  except ValueError:
    logger.error(helpers.format_exception())
    return 400, 'Bad Request', 'Missing argument(s).', {}
  except rsa.DecryptionError:
    logger.error(helpers.format_exception())
    return 500, 'Internal Server Error', 'Decryption failed', {}
  except user.IdentityError:
    logger.error(helpers.format_exception())
    return 400, 'Bad Request', 'Unrecognized identity.', {}

def post(path, headers, body):
  pass

def delete(path, headers, body):
  pass

handlers = {
  'PUT': put, 'GET': get, 'post': post, 'delete': delete }
logger = helpers.init_logger('signin', config.LOG_PATH)

if __name__ == '__main__':
  
  try:
    handler_config = config.HANDLER_CONFIG['signin']
    handler.run(handler_config.send_spec, handler_config.recv_spec, handlers)
  except:
    logger.error(helpers.format_exception())
else:
  handler.handlers_registry[__name__] = handlers
