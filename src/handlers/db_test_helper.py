# -*- coding:utf8 -*-

class Helper(object):
    def __init__(self, db, fail):
        self.db = db
        self.fail = fail

    def assert_unique(self, table, field, value):
        if None == value: self.fail('Value cannot be None.')
        value_expr = "'%s'" % value
        statement = '''
                    select count(1) from %s where %s = %s
                    ''' % (table, field, value_expr)

        self.db.query(statement)
        result = self.db.store_result()
        rows = result.fetch_row()
        count = rows[0][0]
        if 1 <> count:
            message = "The value of '%s' is not unique \
in the '%s' field of the '%s' table. \
%d rows found in total" % (value, field, table, count)
            self.fail(message)

    def assert_count(self, table, expected):
        if None == expected: self.fail('Expected value cannot be None.')
        statement = 'select count(1) from %s' % table
        self.db.query(statement)
        result = self.db.store_result()
        rows = result.fetch_row()
        actual = rows[0][0]
        if expected <> actual:
            message = \
                    "The total rows in the '%s' table is %d, not %d"\
                    % (table, actual, expected)
            self.fail(message)

    def assert_not_empty(self, table):
        statement = 'select count(1) from %s' % table
        self.db.query(statement)
        result = self.db.store_result()
        rows = result.fetch_row()
        count = rows[0][0]
        if 0 == count:
            message = "The '%s' table is empty." % table
            self.fail(message)

    def assert_result(self, statement, expected_rows):
        self.db.query(statement)
        result = self.db.store_result()
        count = self.db.affected_rows()
        rows = result.fetch_row(count)
        if rows <> expected_rows:
            message = '''
                    '%s' verified - 
                    '%s' expected but was '%s'
                    ''' % (statement, expected_rows, rows)
            self.fail(message)

    def empty_table(self, table):
        self.db.query("delete from %s where 1 = 1" % table)
