# -*- coding:utf8 -*-

import hashlib
import re
import MySQLdb as mysql
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
      '[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+', identity_str)
    return m <> None

  @staticmethod
  def is_phone_number(identity_str):
    if len(identity_str) > 11: return False
    return True

  @staticmethod
  def load(db, identity_str):
    if db == None: raise ValueError('db is None')

    if Identity.is_email(identity_str) and db.email_exists(identity_str):
      return Identity(db, email = identity_str)
    elif Identity.is_phone_number(identity_str) and db.phone_number_exists(
      identity_str):
      return Identity(db, phone_number = identity_str)
    else:
      raise IdentityError()

  def __init__(self, db, email = None, phone_number = None):
    if db == None:
      raise ValueError('db is None.')
    if email == None and phone_number == None:
      raise ValueError('Either email or phone_number is None.')

    self._db = db
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

class Database(object):
  def __init__(self):
    pass

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
    finally:
      db.close()

  def email_exists(self, email):
    pass

  def phone_number_exists(self, phone_number):
    pass

  def identity_exists(self, field, identity):
    statement = '''
                select count(1) from `user` where %s = '%s';
                '''
    db = mysql.connect(
      config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_INST)

    try:
      db.query(statement % (field, identity))
      r = db.store_result()
      rows = r.fetch_row(1)
      count = rows[0][0]

    except:
      _logger.error(helpers.format_exception())
    finally:
      db.close()

    if count > 1:
      raise DbError(
        'More than one user with the identity "%s" is found' % identity)
    return count == 1

_logger = helpers.init_logger(__name__, config.LOG_PATH) 
