import os
import time
import itertools
import re
import json

import queue
import base64
import urllib.request
import http.client
import inspect
import traceback
from collections import defaultdict

import pymysql
import pymysql.cursors
import pymysql.constants
import pymysql.converters
import pymysql.connections

from collections import OrderedDict

import threading

RE_AFF = re.compile(r'\s*(UPDATE|DELETE)', re.IGNORECASE)

pymysql.converters.conversions[pymysql.constants.FIELD_TYPE.JSON] = json.loads


class Keyword(object):

    def __init__(self, s):
        self.s = s
        return

    def __str__(self):
        return str(self.s)

    def __repr__(self):
        return repr(self.s)

    def translate(self, t):
        return self


def escapeKeyword(s, charset, mapping=None):
    return str(s)


pymysql.converters.encoders[Keyword] = escapeKeyword
pymysql.converters.conversions[Keyword] = escapeKeyword

_key = Keyword


class OrderedDictCursor(pymysql.cursors.DictCursorMixin, pymysql.cursors.Cursor):
    dict_type = OrderedDict


class DatabaseOne(object):

    def __init__(self, **kwargs):

        self._dbargs = kwargs
        self._dbargs['autocommit'] = False

        self.conn = self.make_conn()
        self.ontrans = False

        return

    def make_conn(self):
        return pymysql.connect(**self._dbargs)

    def get_charset(self):
        return self._dbargs.get('charset', 'utf8mb4')

    def __call__(self, sql, args=()):
        return self.execute(sql, args)

    def tuple(self, sql, args=()):
        return self.execute(sql, args, cursor=pymysql.cursors.Cursor)

    def ordered_dict(self, sql, args=()):
        return self.execute(sql, args, cursor=OrderedDictCursor)

    def __enter__(self):

        if self.ontrans == True:
            raise Exception('can not enter transaction twice in one DatabaseOne object.')

        self.ontrans = True
        self.conn.begin()

        return self

    def __exit__(self, type, value, trace):

        if type == None:
            self.conn.commit()
        else:
            self.conn.rollback()

        return

    def execute(self, sql, args, cursor=None):

        if self.ontrans == False:
            raise Exception('can not execute sql before enter transaction twice in DatabaseOne object.')

        with self.conn.cursor(cursor) as csr:

            csr.execute(sql, args)

            if csr.description:
                r = csr.fetchall()
            else:
                r = csr.lastrowid

        return r

    def __getattr__(self, key):
        return Expr(self, key)


class Database(object):
    conf = {}

    default_dbargs = {
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'connect_timeout': 3.0,
        'autocommit': True
    }

    @classmethod
    def loadconfig(cls, filename="database.yaml"):

        # if not os.path.exists(filename):
        #    return
        #
        # import yaml
        #
        # with open(filename, 'r') as fp:
        #    conf = yaml.load(fp)
        #
        # for inc in cfg.get("includes", []):
        #    cls.loadconfig( inc )
        #
        # cls.conf.update(conf)

        cls._load_config('./', filename, set())

        return

    @classmethod
    def _load_config(cls, basedir, configfile, loadedset):

        cfile = os.path.join(basedir, configfile)
        cfile = os.path.abspath(cfile)
        # cfile = os.path.normcase( cfile )
        basepath, filename = os.path.split(cfile)

        if not os.path.exists(cfile):
            return

        if cfile in loadedset:
            return

        import yaml

        with open(cfile, 'r') as fp:
            conf = yaml.load(fp)

        loadedset.add(cfile)

        for inc in conf.get("includes", []):
            cls._load_config(basepath, inc, loadedset)

        cls.conf.update(conf)

        return

    def get_charset(self):
        return self._dbargs.get('charset', 'utf8mb4')

    def __init__(self, database=None, **kwargs):

        if database is None and 'host' not in kwargs:
            raise Exception('argument error.')

        dbargs = self.default_dbargs.copy()
        if database != None:
            dbargs.update(self.conf[database])
        dbargs.update(kwargs)

        self._dbargs = dbargs

        self.init2()

        return

    def init2(self):

        self.lastconntime = time.time()

        self.tvar = threading.local()
        self.tvar.conn = self.make_conn()

        return

    def get_conn(self):

        now = time.time()
        if (now - self.lastconntime > 10):
            self.tvar.conn = self.make_conn()
            return self.tvar.conn

        self.lastconntime = now

        try:
            return self.tvar.conn
        except:
            self.tvar.conn = self.make_conn()
            return self.tvar.conn

    def recycle_conn(self, conn):
        return

    def drop_conn(self, conn, e):

        if e.args[0] in (0, 2006, 2013):
            self.tvar.conn = self.make_conn()

        return

    def make_conn(self):
        return pymysql.connect(**self._dbargs)

    def __call__(self, sql, args=()):
        return self.execute(sql, args)

    def tuple(self, sql, args=()):
        return self.execute(sql, args, cursor=pymysql.cursors.Cursor)

    def ordered_dict(self, sql, args=()):
        return self.execute(sql, args, cursor=OrderedDictCursor)

    def execute(self, sql, args, cursor=None):

        ee = None
        exc = ''

        for i in range(int(self.conf['connection']['retrys'])):

            conn = None

            try:

                conn = self.get_conn()

                with conn.cursor(cursor) as csr:
                    csr._defer_warnings = True
                    csr.execute(sql, args)
                    if csr.description:
                        r = csr.fetchall()
                    else:
                        if RE_AFF.match(sql):
                            r = csr.rowcount
                        else:
                            r = csr.lastrowid

                self.recycle_conn(conn)

                return r

            except pymysql.err.OperationalError as e:

                self.drop_conn(conn, e)
                exc = traceback.format_exc()
                ee = e

            except pymysql.err.InterfaceError as e:

                self.drop_conn(conn, e)
                exc = traceback.format_exc()
                ee = e

            finally:

                pass

        if ee == None:
            print(exc)
            raise Exception('can not be reach here.')

        raise ee

    def commit(self):
        self.tvar.conn.commit()

    def rollback(self):
        self.tvar.conn.rollback()

    def __getattr__(self, key):
        return Expr(self, key)

    def _get_redirect(self, pth, table, auth):

        try:
            conn = http.client.HTTPConnection(host=self._dbargs['host'], port=8030)
            conn.request('PUT', pth, b'', {'Authorization': auth, 'Expect': '100-continue'})
        except Exception as e:
            print(e)
            raise

        resp = conn.getresponse()
        hds = dict(resp.getheaders())

        if resp.status == 307:
            return hds['Location']

        return

    def upload_csv(self, table, label, csvfile):

        with open(csvfile, 'rb') as fp:
            csvfilecontent = fp.read()

        urlpth = '/api/%s/%s/_load?label=%s&column_separator=,' % (self._dbargs['db'], table, label)

        auth = "%s:%s" % (self._dbargs['user'], self._dbargs.get('passwd', ''))
        auth = base64.b64encode(auth.encode('ascii'))
        auth = b'Basic ' + auth

        url = self._get_redirect(urlpth, table, auth)

        if url == None:
            return

        req = urllib.request.Request(
            url,
            headers={'Authorization': auth, 'Expect': '100-continue'},
            data=csvfilecontent,
            method='PUT',
        )

        try:
            r = urllib.request.urlopen(req).read()
            r = json.loads(r.decode('utf-8'))

        except Exception as e:
            print('request error ', e)

        return r

    def upload_status(self, label):

        r = self.execute(
            'SHOW LOAD FROM `{0}` WHERE `Label`=%s ORDER BY CreateTime desc  limit 1'.format(self._dbargs['db']), label)

        return r[0] if len(r) != 0 else None

    def transaction(self):

        return DatabaseOne(**self._dbargs)


class DatabaseShort(Database):

    def init2(self):
        return

    def get_conn(self):
        return self.make_conn()

    def recycle_conn(self, conn):
        return

    def drop_conn(self, conn, e):
        return


class DatabasePool(Database):

    def init2(self):
        self.q = queue.Queue()
        return

    def get_conn(self):

        try:
            conn = self.q.get(timeout=0.1)
        except queue.Empty:
            conn = self.make_conn()

        return

    def recycle_conn(self, conn):
        return

    def drop_conn(self, conn, e):
        return


# https://github.com/2shou/QuickORM/blob/master/data_handler.py

# SELECT
#    [ALL | DISTINCT | DISTINCTROW ]
#      [HIGH_PRIORITY]
#      [STRAIGHT_JOIN]
#      [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
#      [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
#    select_expr [, select_expr ...]
#    [FROM table_references
#      [PARTITION partition_list]
#    [WHERE where_condition]
#    [GROUP BY {col_name | expr | position}
#      [ASC | DESC], ... [WITH ROLLUP]]
#    [HAVING where_condition]
#    [ORDER BY {col_name | expr | position}
#      [ASC | DESC], ...]
#    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
#    [PROCEDURE procedure_name(argument_list)]
#    [INTO OUTFILE 'file_name'
#        [CHARACTER SET charset_name]
#        export_options
#      | INTO DUMPFILE 'file_name'
#      | INTO var_name [, var_name]]
#    [FOR UPDATE | LOCK IN SHARE MODE]]

class Expr(object):
    '''
    db = Database(...)
    db.Table.where(a=1).where(b=2).select(('a',),'b','c')

    db.Table1.join('Table2', id=('id',), invalid=0 ).where(user=123).select()
    SELECT * FROM T1 JOIN T2 ON T2.id = T1.id AND T2.invalid=0 WHERE T1.user = 123;

    db.T1.join('tt', 'T2', id=('id',), invalid=0 ).where(user=123).select( ('T1',all), ('T2','project'), ('T2','project','project_name') )
    SELECT T1.*, T2.project, T2.name AS project_name FROM T1 JOIN tt AS T2 ON T2.id = T1.id AND T2.invalid=0 WHERE T1.user = 123;

    db.Table1.insert(a=1,b=2,c=3)
    db.Table1.append({'a':1,'b':2,'c':3})
    db.Table1.add({'a':1,'b':2,'c':3})

    cond = {"cinema":'12345678'}
    condlike = {"cinema_name":"花园路"}

    db.Table.where(**cond).where_like(**condlike).where(invalid=0).select()

    '''

    def __init__(self, conn, table):

        self._conn = conn

        self.tbl_name = table  # table_references
        self.tbl_alias = None  # table_references

        self.join_expr = []
        self.join_values = []

        self.where_expr = []
        self.where_args = []
        self.where_force = None
        self.where_positive_cnt = 0
        self.where_negative_cnt = 0

        self.write_expr = []
        self.write_args = []
        self.ondup_expr = []
        self.ondup_args = []

        self.group_by_cols = []
        self.order_by_cols = []
        # self.order_by_desc = False
        self.order_by_ads = []

        self.limit_expr = None
        self.offset_expr = None

        self.update_expr = []

        return

    def _where(self, np, fmt, conds):

        if np:
            self.where_positive_cnt += len(conds)
        else:
            self.where_negative_cnt += len(conds)

        if self.tbl_alias:
            fmt = '`{0}`.{1}'.format(self.tbl_alias, fmt)

        self.where_expr.extend([fmt.format(*c, v=','.join(['%s'] * len(c[-1]))) for c in conds])
        self.where_args.extend([v for c in conds for v in c[-1]])

        return self

    def force(self, required=1):
        """
        执行 update 与 delete 操作时，默认情况下必须有 where 条件才能执行
        此函数用于设置 where 条件数量，使 update 和 delete 操作按照预期的方式安全执行

        概念
        正向条件，例如 where( a = 1, b = 2) 的调用，使正向条件数增加 2
        负向条件，例如 where_neq(a = 1 , b = 2, c = 3) 的调用，使负向条件数增加 3

        参数说明
        1.最多两个元素，最少一个元素的 tuple，第一个元素表示正向条件数，第二个元素表示负向条件数
          若只有一个元素，这个值表示正向条件数，负向条件数为 0
        2.int 整数，表示正向条件数

        执行 update 和 delete 操作之前，如果发现实际的正向条件数和负向条件数，达不到 force 函数所设置的数量，将抛出异常
        """
        if isinstance(required, tuple) and len(required) == 2:
            self.where_force = (required[0], required[1], required[0] + required[1])
        elif isinstance(required, tuple) and len(required) == 1:
            self.where_force = (required[0], 0, required[0])
        elif required == 0:
            self.where_force = (0, 0, 0)
        else:
            self.where_force = (required, 0, required)

        return self

    @staticmethod
    def _setvalue(v):

        if inspect.isgenerator(v):
            v = list(v)

        if type(v) not in (list, tuple, set):
            raise Exception('arg of where_in must be list, tuple, set or generator.')

        return v

    def filter(self, _op, kwargs, _none_ignore=False):

        _op = _op.upper().strip()
        p = {
            '=': True,
            '!=': False,
            '>': True,
            '<': True,
            '>=': True,
            '<=': True,
            'IN': True,
            'NOT IN': False,
            'LIKE': False,
            'NOT LIKE': False,
        }[_op]

        if _op in ('IN', 'NOT IN'):
            conds = [(self._colsafe(k), self._setvalue(v)) for k, v in kwargs.items()]
            conds = [(k, v) for k, v in conds if len(v) != 0]
            return self._where(p, ('{0} %s ({v})' % _op), conds)

        conds = [(self._colsafe(k), [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(p, ('{0} %s {v}' % _op), conds)

    def table_as(self, alias):
        self.tbl_alias = alias
        return self

    def where(self, _none_ignore=False, **kwargs):
        """
        eg. where(a=1, b=2)
        eg. where(a=1, b=None) 此时参数 b 会被当作 b = NULL
        eg. where(True, a=1, b=None) 此时参数 b 会被忽略
        """
        # conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        nullconds = [(k, [v]) for k, v in kwargs.items() if v is None]
        conds = [(k, [v]) for k, v in kwargs.items() if v is not None]

        if _none_ignore:
            return self._where(True, '`{0}`={v}', conds)

        return self._where(True, '`{0}` is {v}', nullconds)._where(True, '`{0}`={v}', conds)

    def where_not_eq(self, _none_ignore=False, **kwargs):
        """
        参考 Expr 类的 where 函数
        """
        # conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        nullconds = [(k, [v]) for k, v in kwargs.items() if v is None]
        conds = [(k, [v]) for k, v in kwargs.items() if v is not None]

        if _none_ignore:
            return self._where(False, '`{0}`!={v}', conds)

        return self._where(True, '`{0}` is not {v}', nullconds)._where(True, '`{0}`!={v}', conds)

    where_neq = where_not_eq

    def where_gt(self, _none_ignore=False, **kwargs):
        """
        参考 Expr 类的 where 函数
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`>{v}', conds)

    def where_lt(self, _none_ignore=False, **kwargs):
        """
        参考 Expr 类的 where 函数
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`<{v}', conds)

    def where_ge(self, _none_ignore=False, **kwargs):
        """
        参考 Expr 类的 where 函数
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`>={v}', conds)

    def where_le(self, _none_ignore=False, **kwargs):
        """
        参考 Expr 类的 where 函数
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`<={v}', conds)

    def where_in(self, **kwargs):
        """
        eg. where_in(a=(1,2,3))
        """
        conds = [(k, self._setvalue(v)) for k, v in kwargs.items()]
        conds = [(k, v) for k, v in conds if len(v) != 0]

        return self._where(True, '`{0}` IN ({v})', conds)

    def where_not_in(self, **kwargs):
        """
        eg. where_nin(a=(1,2,3))
        """
        conds = [(k, self._setvalue(v)) for k, v in kwargs.items()]
        conds = [(k, v) for k, v in conds if len(v) != 0]

        return self._where(False, '`{0}` NOT IN ({v})', conds)

    where_nin = where_not_in

    def where_like(self, _like_format=None, **kwargs):
        """
        eg. where_like(a='%hello%')
        eg. where_like('%{}%',a='hello')
        """

        conds = [(k, v) for k, v in kwargs.items() if v is not None]
        if _like_format:
            conds = [(k, [_like_format.format(v)]) for k, v in conds]

        return self._where(True, '`{0}` LIKE {v}', conds)

    like = where_like

    def contains(self, **kwargs):
        """
        eg. contains(a='abc') 相当于 LIKE '%abc%'
        """
        return self.where_like('%{}%', **kwargs)

    def startswith(self, **kwargs):
        """
        eg. contains(a='abc') 相当于 LIKE 'abc%'
        """
        return self.where_like('{}%', **kwargs)

    def endswith(self, **kwargs):
        """
        eg. contains(a='abc') 相当于 LIKE '%abc'
        """
        return self.where_like('%{}', **kwargs)

    def where_not_like(self, _like_format=None, **kwargs):
        """
        eg. where_like(a='hello')
        eg. where_like('%{}%',a='hello')
        """

        conds = list(kwargs.items())
        if _like_format:
            conds = [(k, [_like_format.format(v)]) for k, v in conds]

        return self._where(True, '`{0}` NOT LIKE {v}', conds)

    not_like = where_not_like

    def json_search(self, col, ooa, search_str, *args):

        ooa = {'one': 'one', 'all': 'all', 1: 'one', all: 'all'}[ooa]
        conds = [(col, [ooa, search_str] + list(args))]

        return self._where(True, 'JSON_SEARCH( `{0}`, {v} ) is not null', conds)

    def json_extract_eq(self, col, path, value):

        conds = [(col, path, [value])]

        return self._where(True, 'JSON_EXTRACT( `{0}`, "{1}" ) = {v}', conds)

    def _join(self, tablename, alianame, _conds):

        conds = []

        _tbl = alianame if alianame else tablename

        for k1, k2 in _conds:

            if type(k2) == tuple:
                if len(k2) == 1:
                    conds.append('`{0}`.`{1}` = `{2}`.`{3}`'.format(_tbl, k1,
                                                                    self.tbl_alias if self.tbl_alias else self.tbl_name,
                                                                    *k2))
                elif len(k2) == 2:
                    conds.append('`{0}`.`{1}` = `{2}`.`{3}`'.format(_tbl, k1, *k2))
            else:
                conds.append('`{0}`.`{1}` = {2}'.format(_tbl, k1, k2))

        if alianame:
            self.join_expr.append('JOIN {0} AS {1} ON {2}'.format(tablename, alianame, ' AND '.join(conds)))
        else:
            self.join_expr.append('JOIN {0} ON {1}'.format(tablename, ' AND '.join(conds)))

        return self

    def join(self, tablename, alias=None, **kwargs):
        """
        eg. table0.join('table1', 't', id=('table0','id',))
                  .join('table1', 'c', a=('a',))
                  .select(('table0', all), ('t', 'g'),('t', 'e', 'eee'))
        """
        if len(kwargs) < 1:
            raise Exception('must have 1 least cond when join a table.')

        return self._join(tablename, alias, list(kwargs.items()))

    @staticmethod
    def _colsafe(col):

        if isinstance(col, Keyword):
            return str(col)

        if type(col) == tuple:

            if len(col) == 3:

                if col[0] == None:
                    return '`{1}` AS `{2}`'.format(*col)
                return '`{0}`.`{1}` AS `{2}`'.format(*col)

            if len(col) == 2:
                if col[1] == all:
                    return '`{0}`.*'.format(*col)
                return '`{0}`.`{1}`'.format(*col)

            if len(col) == 1:
                col = col[0]

        if type(col) != str:
            raise Exception('col must be str')

        return '`{}`'.format(col)

    def groupby(self, *args):
        """
        eg. groupby('col_a', ('table1', all) ,('table1', 'col_a'), ('table1', 'col_b', 'col_b_alias') )
        """
        self.group_by_cols = [self._colsafe(a) for a in args]
        return self

    def orderby(self, *args):
        """
        eg. orderby('col_a', ('table1', all) ,('table1', 'col_a'), ('table1', 'col_b', 'col_b_alias') )
        """
        self.order_by_cols = self.order_by_cols + [self._colsafe(a) for a in args]
        self.order_by_ads = self.order_by_ads + ([''] * len(args))

        self.last_order_by_len = len(args)

        return self

    def desc(self):
        """
        eg. desc()
        """
        # if self.order_by_cols:
        #    self.order_by_desc = True
        # else:
        #    raise Exception('can not desc before orderby')

        self.order_by_ads = self.order_by_ads[:-self.last_order_by_len] + (['desc'] * self.last_order_by_len)

        return self

    def limit(self, i):
        """
        eg. limit(5)
        """
        self.limit_expr = 'LIMIT %s' % int(i)
        return self

    def offset(self, i):
        """
        eg. offset(5)
        """
        if self.limit_expr is None:
            raise Exception('can not offset before limit')

        self.offset_expr = 'OFFSET %s' % int(i)

        return self

    # SELECT
    #    [ALL | DISTINCT | DISTINCTROW ]
    #      [HIGH_PRIORITY]
    #      [STRAIGHT_JOIN]
    #      [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
    #      [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
    #    select_expr [, select_expr ...]
    #    [FROM table_references
    #      [PARTITION partition_list]
    #    [WHERE where_condition]
    #    [GROUP BY {col_name | expr | position}
    #      [ASC | DESC], ... [WITH ROLLUP]]
    #    [HAVING where_condition]
    #    [ORDER BY {col_name | expr | position}
    #      [ASC | DESC], ...]
    #    [LIMIT {[offset,] row_count | row_count OFFSET offset}]
    #    [PROCEDURE procedure_name(argument_list)]
    #    [INTO OUTFILE 'file_name'
    #        [CHARACTER SET charset_name]
    #        export_options
    #      | INTO DUMPFILE 'file_name'
    #      | INTO var_name [, var_name]]
    #    [FOR UPDATE | LOCK IN SHARE MODE]]

    def _select_makeup(self, cols, forupdate):
        return '''SELECT {COLS} FROM {TBL} {AS}
{JOIN_EXPR} {WHERE} {WHERE_EXPR} 
{GROUPBY} {GROUPBY_COLS} {ORDERBY} {ORDERBY_COLS}
{LIMIT} {OFFSET} {FORUPDATE}'''.format(
            COLS=','.join(cols),
            TBL=self.tbl_name,
            AS='AS ' + self.tbl_alias if self.tbl_alias else '',
            WHERE='WHERE' if self.where_expr else '',
            WHERE_EXPR=' AND '.join(self.where_expr),
            JOIN_EXPR=' '.join(self.join_expr),
            GROUPBY='GROUP BY' if self.group_by_cols else '',
            GROUPBY_COLS=','.join(self.group_by_cols),
            ORDERBY='ORDER BY' if self.order_by_cols else '',
            ORDERBY_COLS=','.join(['%s %s' % (col, ad) for col, ad in zip(self.order_by_cols, self.order_by_ads)]),
            # DESC='DESC' if self.order_by_desc else '',
            LIMIT='' if self.limit_expr is None else self.limit_expr,
            OFFSET='' if self.offset_expr is None else self.offset_expr,
            FORUPDATE='FOR UPDATE' if forupdate else ''
        )

    def _select_values(self):
        return tuple(self.where_args)

    def select(self, *args):
        """
        eg. select('user_id', 'user_name',  )

        和其他表 join 时，为了避免字段名冲突，可以这样写
        eg. select(('tableA', 'user_id', 'user_id_alias'),)
        eg. select(('tableA', 'user_id'), ('tableB', 'email'),)
        eg. select(('tableA', all),)
        """
        cols = [self._colsafe(a) for a in args]
        cols = cols if cols else ['*']
        return self._conn(self._select_makeup(cols, False), self._select_values())

    def select_for_update(self, *args):
        """
        eg. select('user_id', 'user_name',  )

        和其他表 join 时，为了避免字段名冲突，可以这样写
        eg. select(('tableA', 'user_id', 'user_id_alias'),)
        eg. select(('tableA', 'user_id'), ('tableB', 'email'),)
        eg. select(('tableA', all),)
        """
        cols = [self._colsafe(a) for a in args]
        cols = cols if cols else ['*']
        return self._conn(self._select_makeup(cols, True), self._select_values())

    def count(self):
        """
        eg. one()
        """
        cols = ['count(1)']
        return self._conn(self._select_makeup(cols, False), self._select_values())[0][cols[0]]

    def one(self, col=None, default=None):
        """
        eg. one(col)
        eg. one(col,'无结果')
        """

        self.limit_expr = 'LIMIT 1'
        self.offset_expr = None

        cols = [self._colsafe(col)] if col else ['*']
        r = self._conn(self._select_makeup(cols, False), self._select_values())

        if len(r) == 0:
            return default

        if col == None:
            return r[0]

        return list(r[0].values())[0]

    def one_for_update(self, col=None, default=None):

        self.limit_expr = 'LIMIT 1'
        self.offset_expr = None

        cols = [self._colsafe(col)] if col else ['*']
        r = self._conn(self._select_makeup(cols, True), self._select_values())

        if len(r) == 0:
            return default

        if col == None:
            return r[0]

        return list(r[0].values())[0]

    def unique(self, *args, default=None):
        """
        eg. unique(col_a, col_b, col_c)
        eg. unique(col_a, col_b, col_c,  default='无结果')
        """

        cols = [self._colsafe(a) for a in args] if args else ['*']
        r = self._conn(self._select_makeup(cols, False), self._select_values())

        if len(r) != 1:
            return default

        return r[0]

    def unique_for_update(self, *args, default=None):
        """
        eg. unique_for_update(col_a, col_b, col_c)
        eg. unique_for_update(col_a, col_b, col_c,  default='无结果')
        """

        cols = [self._colsafe(a) for a in args] if args else ['*']
        r = self._conn(self._select_makeup(cols, True), self._select_values())

        if len(r) != 1:
            return default

        return r[0]

    # INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    #    [INTO] tbl_name
    #    [PARTITION (partition_name [, partition_name] ...)]
    #    [(col_name [, col_name] ...)]
    #    {VALUES | VALUE} (value_list) [, (value_list)] ...
    #    [ON DUPLICATE KEY UPDATE assignment_list]
    #
    # INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    #    [INTO] tbl_name
    #    [PARTITION (partition_name [, partition_name] ...)]
    #    SET assignment_list
    #    [ON DUPLICATE KEY UPDATE assignment_list]
    #
    # INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    #    [INTO] tbl_name
    #    [PARTITION (partition_name [, partition_name] ...)]
    #    [(col_name [, col_name] ...)]
    #    SELECT ...
    #    [ON DUPLICATE KEY UPDATE assignment_list]

    def _insert_makeup(self):
        return '''INSERT INTO {TBL}
SET {ASSIGNMENT}
{ONDUP} {DUP_ASSIGNMENT}'''.format(
            TBL=self.tbl_name,
            ASSIGNMENT=','.join(self.write_expr),
            ONDUP='ON DUPLICATE KEY UPDATE' if self.ondup_expr else '',
            DUP_ASSIGNMENT=','.join(self.ondup_expr)
        )

    def _insert_values(self):
        return tuple(self.write_args + self.ondup_args)

    def _ondup(self, fmt, assignments):

        self.ondup_expr += [fmt.format(k, v='%s') for k, v in assignments]
        self.ondup_args += [v for k, v in assignments]

        return

    def ondup(self, **kwargs):
        self._ondup('`{0}`={v}', list(kwargs.items()))
        return self

    def ondup_inc(self, **kwargs):
        self._ondup('`{0}`=`{0}`+({v})', list(kwargs.items()))
        return self

    def append(self, d, *, ignore=False, jsoncol=False):
        """
        eg. append({'a':55555, 'b':4444})
        """
        assignments = list(d.items())

        if jsoncol:
            assignments = [(k, json.dumps(v) if type(v) in (dict, list, tuple) else v) for k, v in assignments]

        self.write_expr += ["`{0}`={v}".format(k, v='%s') for k, v in assignments]
        self.write_args += [v for k, v in assignments]

        return self._conn(self._insert_makeup(), self._insert_values())

    def insert(self, **kwargs):
        """
        insert(a='value0', b='value1')
        """
        return self.append(kwargs)

    def extend(self, datas, *, lot=100, ignore=False, jsoncol=False):
        """
        eg. extend([{'a':'value0', 'b':'value1'}, {'a':'value2', 'b':'value3'}])
        eg. extend([{'a':'value0', 'b':'value1'}, {'a':'value2', 'b':'value3'}] * 1000, 10)
        :param datas: 一个字典为一行数据，放在一个 list 或者 tuple 中
        :param lot: 对写入 sql 包含的数据行数进行切分
        """

        if len(datas) < lot:
            keys = set([k for d in datas for k in d.keys()])
            keys = list(keys)
        else:
            keys = self._conn.tuple(
                '''select COLUMN_NAME from information_schema.COLUMNS
                   where table_name="{0}" and table_schema = "{1}"
                                          and EXTRA!="VIRTUAL GENERATED"
                '''.format(self.tbl_name, self._conn._dbargs['db']))
            keys = [k for (k,) in keys]

        key_expr = ','.join(['`%s`' % k for k in keys])

        chrset = self._conn.get_charset()
        ignore_word = 'IGNORE' if ignore else ''

        for i in range(0, len(datas), lot):
            values = [[d.get(k, Keyword('default')) for k in keys] for d in datas[i:i + lot]]
            if jsoncol:
                values = [[(json.dumps(v) if type(v) in (dict, list, tuple) else v) for v in vs] for vs in values]
            values = [pymysql.escape_sequence(vs, chrset) for vs in values]
            # values = [pymysql.escape_sequence([d.get(k, None) for k in keys], chrset) for d in datas[i:i + lot]]
            value_expr = ','.join(values)
            expr = 'INSERT {0} INTO {1} ({2}) VALUES {3}'.format(ignore_word, self.tbl_name, key_expr, value_expr)
            self._conn(expr)

        return

    def _replace_makeup(self):
        return '''REPLACE INTO {TBL} SET {ASSIGNMENT}'''.format(
            TBL=self.tbl_name,
            ASSIGNMENT=','.join(self.write_expr),
        )

    def _replace_values(self):
        return tuple(self.write_args)

    def add(self, d, jsoncol=False):
        """
        eg. add({'a':'value0', 'b':'value1'})
        """
        assignments = list(d.items())

        if jsoncol:
            assignments = [(k, json.dumps(v) if type(v) in (dict, list, tuple) else v) for k, v in assignments]

        self.write_expr += ["`{0}`={v}".format(k, v='%s') for k, v in assignments]
        self.write_args += [v for k, v in assignments]

        return self._conn(self._replace_makeup(), self._replace_values())

    def replace(self, **kwargs):

        return self.add(kwargs)

    # UPDATE [LOW_PRIORITY] [IGNORE] table_reference
    #    SET assignment_list
    #    [WHERE where_condition]
    #    [ORDER BY ...]
    #    [LIMIT row_count]

    def _update_makeup(self):
        return '''UPDATE {TBL} SET {ASSIGNMENT}
{WHERE} {WHERE_EXPR} '''.format(
            TBL=self.tbl_name,
            ASSIGNMENT=','.join(self.write_expr),
            WHERE='WHERE' if self.where_expr else '',
            WHERE_EXPR=' AND '.join(self.where_expr),
        )

    def _update_values(self):
        return tuple(self.write_args + self.where_args)

    def update(self, **kwargs):
        """
        eg. update(a='new_value', b='new_value')
        安全性设置详见 Expr 类的 force 函数
        """
        if self.where_force is None:
            self.where_force = (1, 0, 1)

        if self.where_positive_cnt < self.where_force[0]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        if self.where_negative_cnt < self.where_force[1]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        if (self.where_negative_cnt + self.where_positive_cnt) < self.where_force[2]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        assignments = list(kwargs.items())

        self.write_expr += ["`{0}`={v}".format(k, v='%s') for k, v in assignments]
        self.write_args += [v for k, v in assignments]

        return self._conn(self._update_makeup(), self._update_values())

    def update_inc(self, **kwargs):
        """
        eg. update(a='new_value', b='new_value')
        安全性设置详见 Expr 类的 force 函数
        """
        if self.where_force is None:
            self.where_force = (1, 0, 1)

        if self.where_positive_cnt < self.where_force[0]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        if self.where_negative_cnt < self.where_force[1]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        if (self.where_negative_cnt + self.where_positive_cnt) < self.where_force[2]:
            raise Exception('update conditions not be satisfied, pls call the force function in right way.')

        assignments = list(kwargs.items())

        self.write_expr += ["`{0}`=`{0}`+({v})".format(k, v='%s') for k, v in assignments]
        self.write_args += [v for k, v in assignments]

        return self._conn(self._update_makeup(), self._update_values())

    def _delete_makeup(self):
        return '''DELETE FROM {TBL} {WHERE} {WHERE_EXPR}'''.format(
            TBL=self.tbl_name,
            WHERE='WHERE' if self.where_expr else '',
            WHERE_EXPR=' AND '.join(self.where_expr),
        )

    def _delete_values(self):
        return tuple(self.where_args)

    def delete(self):
        """
        eg. delete()
        安全性设置详见 Expr 类的 force 函数
        """
        if self.where_force is None:
            self.where_force = (1, 0, 1)

        if self.where_positive_cnt < self.where_force[0]:
            raise Exception('delete conditions not be satisfied, pls call the force function in right way.')

        if self.where_negative_cnt < self.where_force[1]:
            raise Exception('delete conditions not be satisfied, pls call the force function in right way.')

        if (self.where_negative_cnt + self.where_positive_cnt) < self.where_force[2]:
            raise Exception('delete conditions not be satisfied, pls call the force function in right way.')

        return self._conn(self._delete_makeup(), self._delete_values())


# Database.loadconfig('/etc/edb.yaml')
# Database.loadconfig('/usr/local/etc/edb.yaml')
# Database.loadconfig()
Database.loadconfig('edb.yaml')
sqllog = Database.conf.get('connection', {}).get('sqllog', None)
if sqllog == "print":
    class PConnection(pymysql.connections.Connection):
        def query(self, sql, unbuffered=False):
            print('>', sql)
            return super().query(sql, unbuffered)


    pymysql.connections.Connection = PConnection
