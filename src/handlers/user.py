# -*- coding:utf8 -*-

import hashlib
import re
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
import MySQLdb as mysql
from Crypto.Cipher import AES
import binascii
import base64
import config
import helpers

class IdentityError(Exception):
  pass

class DbError(Exception):
  pass

class Token(object):

  @staticmethod
  def to_token_str(date):
    year = str(date.year)
    month = helpers.pad_str(str(date.month), 2)
    day = helpers.pad_str(str(date.day), 2)
    hour = helpers.pad_str(str(date.hour), 2)
    minute = helpers.pad_str(str(date.minute), 2)
    second = helpers.pad_str(str(date.second), 2)

    return helpers.pad_str(year + month + day + hour + minute + second, 16)

  @staticmethod
  def from_date(date, secret):
    token_str = Token.to_token_str(date)
    return Token(token_str, secret)

  def __init__(self, token_str, secret):
    if None == token_str: raise ValueError('token_str is None.')
    if None == secret: raise ValueError('secret is None.')
    self.__token_str = token_str
    self.__secret = secret

  def verify(self, cipher):
    token = self._decrypt_token(cipher)
    return token == self.__token_str

  def text(self):
    return self.__token_str

  def cipher(self):
    key = AES.new(self.__secret)
    cipher = key.encrypt(self.__token_str)
    return binascii.hexlify(cipher)

  def _decrypt_token(self, cipher):
    cipher = binascii.unhexlify(cipher)
    key = AES.new(self.__secret)
    text = key.decrypt(cipher)

    if 16 <> len(text) or (not text.isdigit()): 
      raise ValueError('Invalid cipher')
    return text

class Identity(object):
  @staticmethod
  def is_email(identity_str):
    if len(identity_str) > 256: return False
    m = re.match(
      '^\w[\w\.-]+@[\w][\.\-\w]*.[a-zA-Z]+', identity_str)
    if m == None: return False
    return m.group() == identity_str

  @staticmethod
  def is_phone_number(identity_str):
    if None == identity_str: return False
    if len(identity_str) > 18: return False
    m = re.match(
      '^[\d]+[\-]\d+', identity_str)
    if m == None: return False
    return m.group() == identity_str

  @staticmethod
  def load(db, identity_str):
    if db == None: raise ValueError('db is None')

    if Identity.is_email(identity_str): 
      user_id = db.get_user_id_by_email(identity_str)
      if -1 <> user_id:
        return Identity(db, user_id, email = identity_str)
    if Identity.is_phone_number(identity_str):
      user_id = db.get_user_id_by_phone_number(identity_str)
      if -1 <> user_id:
        return Identity(db, user_id, phone_number = identity_str)
    else:
      raise IdentityError()

  def __init__(self, db, user_id, email = None, phone_number = None):
    if db == None:
      raise ValueError('db is None.')
    if email == None and phone_number == None:
      raise ValueError('Either email or phone_number is None.')
    if email <> None:
      if not Identity.is_email(email):
        raise ValueError('Invalid email address - \'%s\'.' % email)
    if phone_number <> None:
      if not Identity.is_phone_number(phone_number):
        raise ValueError('Invalid phone number - \'%s\'.' % phone_number)

    self._db = db
    self.user_id = user_id
    self.email = email
    self.phone_number = phone_number

  def validate(self, password):
    if None == password or '' == password:
      return VaueError('No password to validate')
    password = hashlib.new('md5', password).hexdigest()
    is_email = self.email <> None
    stored = self._db.get_password(
      is_email, self.email if is_email else self.phone_number)
    return stored == password

  def create_token(self, db):
    secret = uuid4()
    expire_date = datetime.now() + timedelta(days = 30)
    token = Token.from_date(expire_date, secret.hex)
    cipher = token.cipher()

    db.save_token(self.user_id, token.text(), secret.hex)
    return cipher

  def _to_token(self, date):
    year = str(date.year)
    month = helpers.pad_str(str(date.month), 2)
    day = helpers.pad_str(str(date.day), 2)
    hour = helpers.pad_str(str(date.hour), 2)
    minute = helpers.pad_str(str(date.minute), 2)
    second = helpers.pad_str(str(date.second), 2)

    return helpers.pad_str(year + month + day + hour + minute + second, 16)

  def _to_date(self, text):
    year = int(text[2:6])
    month = int(text[7:8])
    day = int(text[9:10])
    hour = int(text[11:12])
    minute = int(text[13:14])
    second = int(text[15:16])

    return datetime(year, month, day, hour, minute, second)

class Database(object):
  def __init__(self):
    pass

  def save_token(self, user_id, token, secret):
    global _logger
    sql = '''
          update `user` 
          set token = '%s', secret = '%s'
          where user_id = %d 
          ''' % (token, secret, user_id)

    def handler(db):
      rows = db.affected_rows()
      db.commit()
      return rows

    total = self._exec(sql, handler)
    _logger.debug('%d user(s) updated.', total)

  def load_token(self, user_id):
    sql = '''
          select token, secret
          from `user`
          where user_id = %d
          ''' % user_id

    def handler(db):
      r = db.store_result()
      total = db.affected_rows()
      if total == 0: return None
      if total > 1: raise DbError()
      rows = r.fetch_row(1)
      return rows[0][0], rows[0][1]

    return self._exec(sql, handler)

  def get_password(self, identity_is_email, identity):
    field = 'email' if identity_is_email else 'phone_number'
    sql = '''
          select `password` from `user` where %s = '%s';
          ''' % (field, identity)

    def handler(db):
      r = db.store_result()
      total = db.affected_rows()
      if 1 < total: 
        raise DbError(
          'More than one user with the identity "%s" is found' % identity)

      if 0 == total: return None
      rows = r.fetch_row(total)
      return rows[0][0]

    return self._exec(sql, handler)

  def get_user_id_by_phone_number(self, phone_number):
    return self.__get_user_id_by_identity('phone_number', phone_number)

  def get_user_id_by_email(self, email):
    return self.__get_user_id_by_identity('email', email)

  def __get_user_id_by_identity(self, identity_type, identity):
    sql = '''
          select user_id from `user` where %s = '%s'
          ''' % (identity_type, identity)

    def handler(db):
      r = db.store_result()
      if db.affected_rows() == 0: return -1
      rows = r.fetch_row() 
      return rows[0][0]

    return self._exec(sql, handler)

  def email_exists(self, email):
    return self.identity_exists('email', email)

  def phone_number_exists(self, phone_number):
    return self.identity_exists('phone_number', phone_number)

  def identity_exists(self, field, identity):
    statement = '''
                select count(1) from `user` where %s = '%s';
                ''' % (field, identity)

    def handler(db):
      db.query(statement % (field, identity))
      r = db.store_result()
      rows = r.fetch_row(1)
      return rows[0][0]

    count = self._exec(statement, handler)
    if count > 1:
      raise DbError(
        'More than one user with the identity "%s" is found' % identity)
    return count == 1

  def _exec(self, statement, handler = None):
    global _logger
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_INST)

    try:
      db.query(statement)
      if None <> handler:
        return handler(db)
      else:
        return db.affected_rows()
    except:
      _logger.error(helpers.format_exception())
      raise
    finally:
      db.close()

def verify_token(func):
  def impl(path, headers, body):
    global _logger
    if headers == None:
      return 401, 'Unauthorized', 'Authorization missing', {
        'WWW-Authorization': 'token required'}

    _logger.debug("headers = %s", headers)

    field = 'authorization'
    if not field in headers:
      return 401, 'Unauthorized', 'Authorization missing', {
        'WWW-Authorization': 'token required'}
    token_cipher = headers[field]
    try:
      _logger.debug("token = %s", auth_token)
      auth_token = token_cipher
    except:
      return 401, 'Unauthorized', 'Invalid token', {}

    field = 'identity'
    if not field in headers:
      return 400, 'Bad Request', 'Identity missing', {}
    identity_str = headers[field]
    _logger.debug("identity = %s", identity_str)

    global db
    if None == db: raise ValueError('global varialbe \'db\' is None')
    identity = Identity.load(db, identity_str)
    token_str, secret = db.load_token(identity.user_id)

    token = Token(token_str, secret)
    if not token.verify(auth_token):
      return 401, 'Unauthorized', 'Invalid token', {}
    return func(path, headers, body)

  return impl

_logger = helpers.init_logger(__name__, config.LOG_PATH)
db = Database()
