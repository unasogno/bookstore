# -*- coding:utf8 -*-

import hashlib
import re
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
import MySQLdb as mysql
from Crypto.Cipher import AES
import binascii
import config
import helpers

class IdentityError(Exception):
  pass

class DbError(Exception):
  pass

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
    token = self._to_token(expire_date)
    cipher = self._encrypt_token(token, secret.hex)

    db.save_token(self.user_id, token, secret.hex)
    return cipher

  def _encrypt_token(self, text, secret):
    key = AES.new(secret)
    cipher = key.encrypt(text)
    return binascii.hexlify(cipher)

  def _decrypt_token(self, cipher, secret):
    cipher = binascii.unhexlify(cipher)
    key = AES.new(secret)
    text = key.decrypt(cipher)

    if 16 <> len(text) or (not text.isdigit()): 
      raise ValueError('Invalid cipher')
    return text

  def _to_token(self, date):
    year = str(date.year)
    month = helpers.pad_str(str(date.month), 2)
    day = helpers.pad_str(str(date.day), 2)
    hour = helpers.pad_str(str(date.hour), 2)
    minute = helpers.pad_str(str(date.minute), 2)
    second = helpers.pad_str(str(date.second), 2)

    self.text = helpers.pad_str(year + month + day + hour + minute + second, 16)

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
    sql = '''
          update `user` 
          set token = '%s', secret = '%s'
          where user_id = %d 
          ''' % (token, secret, user_id)

    self._exec(sql)

  def get_password(self, identity_is_email, identity):
    global _logger
    statement = '''
                select `password` from `user` where %s = '%s';
                '''
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_INST)

    try:

      field = 'email' if identity_is_email else 'phone_number'
      db.query(statement % (field, identity))
      r = db.store_result()
      total = db.affected_rows()
      if 1 < total: 
        raise DbError(
          'More than one user with the identity "%s" is found' % identity)

      if 0 == total: return None
      rows = r.fetch_row(total)
      return rows[0][0]

    except:
      _logger.error(helpers.format_exception())
      raise
    finally:
      db.close()

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
    except:
      _logger.error(helpers.format_exception())
      raise
    finally:
      db.close()

_logger = helpers.init_logger(__name__, config.LOG_PATH) 
