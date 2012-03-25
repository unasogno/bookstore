# _*_ coding:utf8 _*_

import MySQLdb as mysql
import json

server = 'localhost'
username = 'root'
password = '!Q@W3e4r'
schema = 'bookstore'

def dump_json(rows):
    l = []
    for row in rows:
        d = { "book_id": row[0], "title": unicode(row[1]), 
              "isbn": unicode(row[2]), "publisher_id": row[3], 
              "class": unicode(row[4]), "publish_date": row[5].__str__(),
              "author": unicode(row[6]), "barcode": unicode(row[7]), 
              "list_price": float(row[8]), "sheet_numbers": float(row[9]), 
              "folio": row[10], "print_type": row[11], 
              "comments": unicode(row[12])}
        l.append(d)

    return json.dumps(l, ensure_ascii = False).encode('utf8')

def filter_dict(d, keys):
    result = {}
    if d == None: return result
    for key in keys:
        if d.has_key(key):
            result[key] = d[key]
    return result

def query_book(d):
    if (None == d):
        args = {}
   
    expected = ['title', 'name'] 
    args = filter_dict(d, expected)

    global server, schema, username, password
    
    db = mysql.connect(
      server, username, password, schema, charset = 'utf8', use_unicode = True);

    sql = "select book_id, \
            title, isbn, name as publisher, class, publish_date, author, barcode, \
            list_price, sheet_numbers, folio, print_type, comments \
            from book b \
            inner join publisher p \
              on b.publisher_id = p.publisher_id" 

    where = " and ".join([
        "=".join([k.__str__(), args[k].__str__().join(["'", "'"])]) for k in args])

    if (where.strip() != ""):
        where = " where " + where

    # sql = sql + " limit 10;"
    sql = sql + where + ";"

    print sql

    try:    
        db.query(sql)
        r = db.store_result()
        if 0 == r.num_rows():
          return json.dumps([])
        rows = r.fetch_row(maxrows = 0, how = 0)
        json_str = dump_json(rows)
        db.commit()
        return json_str
    except:
        raise
        db.rollback()
    finally:
        db.close()
        


