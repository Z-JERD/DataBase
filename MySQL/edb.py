
import os
import time
import re
import json
import traceback
import threading

import pymysql
import pymysql.cursors
import pymysql.constants
import pymysql.converters
import pymysql.connections

RE_AFF = re.compile(r'\s*(UPDATE|DELETE)', re.IGNORECASE)
pymysql.converters.conversions[pymysql.constants.FIELD_TYPE.JSON] = json.loads


def escapeKeyword(s, charset, mapping=None):
    return str(s)

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

pymysql.converters.encoders[Keyword] = escapeKeyword
pymysql.converters.conversions[Keyword] = escapeKeyword

_key = Keyword



class Database(object):
    conf = {}

    default_dbargs = {
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor, #返回数据类型为dict
        'connect_timeout': 3.0,
        'autocommit': True   #自动提交
    }

    @classmethod
    def loadconfig(cls, filename="database.yaml"):
        """加载数据库配置文件"""

        cls._load_config('./', filename, set())

        return

    @classmethod
    def _load_config(cls, basedir, configfile, loadedset):
        """
            conf =
            {
                'connection': {'sqllog': 'print', 'retrys': 3},
                 'arch2018': {'host': '10.110.1.90', 'user': 'php', 'passwd': 'MySQL57.huayingjuhe.com', 'db': 'arch2018'},
                 'fdm': {'host': '10.110.1.90', 'user': 'php', 'passwd': 'MySQL57.huayingjuhe.com', 'db': 'fdm'}
            }
        """

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

    def __init__(self,database=None,**kwargs):
        """连接数据库"""

        if database is None and 'host' not in kwargs:
            raise  Exception('argument error')

        dbargs = self.default_dbargs.copy()
        if database != None:
            dbargs.update(self.conf[database])
        dbargs.update(kwargs)
        self._dbargs = dbargs
        self.init2()
        return

    def init2(self):

        self.lastconntime = time.time()
        """为每个线程保存一个单独的数据供当前线程操作"""
        self.tvar = threading.local()
        self.tvar.conn = self.make_conn()

        return

    def get_conn(self):
        """根据时间间隔是否需要重新连接数据库"""
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
        """执行sql发生异常导致连接断开,重新建立连接"""

        if e.args[0] in (0, 2006, 2013):
            self.tvar.conn = self.make_conn()

        return

    def make_conn(self):
        return pymysql.connect(**self._dbargs)

    def __call__(self,sql,args=()):
        """对象加上()后触发call,执行sql语句"""
        return self.execute(sql,args)

    def tuple(self,sql,args=()):
        return self.execute(sql,args,cursor=pymysql.cursors.Cursor)

    def ordered_dict(self,sql,args=()):
        pass

    def execute(self,sql,args,cursor=None):
        """执行sql语句,完成数据库操作"""
        ee = None
        exc = ''
        for i in range(int(self.conf['connection']['retrys'])):
            """
            sql未执行成功就重试.description 列名的相关信息,查询操作时具有的属性
                                rowcount    sql操作的数据行数
                                lastrowid   最新自增ID    添加操作时的属性
            
            """
            conn = None
            try:
                conn = self.get_conn()
                with conn.cursor(cursor) as csr:
                    csr._defer_warnings = True
                    csr.execute(sql,args)
                    if csr.description:
                        """sql查询操作  """
                        r = csr.fetchall()
                    else:
                        """如果是update/delete操作就返回执行execute()方法后影响的行数
                            如果是insert操作就返回最新自增ID
                        """
                        if RE_AFF.match(sql):
                            r = csr.rowcount
                        else:
                            r = csr.lastrowid
                self.recycle_conn(conn)

                return r

            except pymysql.err.OperationalError as e:
                """操作数据库时发生的错误。例如：连接意外断开、 数据库名未找到"""
                self.drop_conn(conn, e)
                # 获取详细的异常信息 能知道是哪个文件在哪一行发生了错误
                exc = traceback.format_exc()
                ee = e

            except pymysql.err.IntegrityError as e:
                """数据库接口模块本身的错误"""
                self.drop_conn(conn, e)
                exc = traceback.format_exc()
                ee = e

            finally:
                pass

        if ee == None:
            print(exc)
            raise Exception('can not be reach here')

        raise  ee

    def commit(self):
        self.tvar.conn.commit()

    def rollback(self):
        self.tvar.conn.rollback()

    def __getattr__(self, key):
        """调用不存在的属性时，会试图调用此方法获取属性，并且返回value
            基于自定义的方法完成数据库的操作
            Expr(self,key)  self 当前操作对象
            将Database对象作为Expr对象的一个属性
        """
        return Expr(self,key)

class Expr(object):
    """
        db = Database()
        新增：
            1.  db.table1.insert(a=1,b=2,c=3)
            2.  db.table2.append({'a':1,'b':2,'c':3})
            3.  db.table.add({'a':1,'b':2,'c':3})

        连表查询：
    """

    def __init__(self,conn,table):
        self._conn = conn
        self.tb1_name = table
        self.tb1_alias = None

        self.join_expr = []
        self.join_values = []

        self.where_expr = []
        self.where_args = []
        self.where_force = []
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

        if self.tb1_alias:
            fmt =  '`{0}`.{1}'.format(self.tb1_alias, fmt)
        self.where_expr.extend([fmt.format(*c, v= ','.join(['%s'] * len(c[-1]))) for c in conds])
        self.where_args.extend([v for c in conds for v in c[-1]])

        return self

    def where(self, __none_ignore=False, **kwargs):
        """
            查询出满足条件的数据 并自定义是否忽略值为None的参数
            等同于 where id = 1

            eg. where(a=1, b=2)
            eg. where(a=1, b=None) b 会被当作 b = NULL
            eg. where(True, a=1, b=None)  此时参数 b 会被忽略
            将变量和值分开 如：where(a=1, b=2,c= None)
              where_expr = ['a=%s', 'b=%s','c is %s']
              where_args = [1, 2,null]

              is 一般情况下和 null 连用，比较该字段的值是否为空
              = 比较两个值是否相等
        """
        nullconds = [(k, [v]) for k, v in kwargs.items() if v is None]
        conds = [(k,[v]) for k, v in kwargs.items() if v is not None]

        if __none_ignore:
            return self._where(True, '`{0}`={v}', conds)

        return self._where(True,'`{0}` is {v}', nullconds)._where(True, '{0}={v}', conds)

    def where_not_eq(self, _none_ignore=False, **kwargs):
        """
            等同于 where id ！= 1
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
            等同于 where id > 1
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`>{v}', conds)

    def where_lt(self, _none_ignore=False, **kwargs):
        """
        等同于 where id < 1
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`<{v}', conds)

    def where_ge(self, _none_ignore=False, **kwargs):
        """
            等同于 where id >= 1
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`>={v}', conds)

    def where_le(self, _none_ignore=False, **kwargs):
        """
            等同于 where id <= 1
        """
        conds = [(k, [v]) for k, v in kwargs.items() if _none_ignore == False or v is not None]
        return self._where(True, '`{0}`<={v}', conds)

    def where_in(self, **kwargs):
        """
            eg. where_in(a=(1,2,3))  where id in (1,2,3)
        """
        conds = [(k, self._setvalue(v)) for k, v in kwargs.items()]
        conds = [(k, v) for k, v in conds if len(v) != 0]

        return self._where(True, '`{0}` IN ({v})', conds)

    def where_not_in(self, **kwargs):
        """
            eg. where_nin(a=(1,2,3))  where id not in (1,2,3)
        """
        conds = [(k, self._setvalue(v)) for k, v in kwargs.items()]
        conds = [(k, v) for k, v in conds if len(v) != 0]

        return self._where(False, '`{0}` NOT IN ({v})', conds)

    where_nin = where_not_in

    def where_like(self, _like_format=None, **kwargs):
        """
            模糊查询：%代表一个或多个字符的通配符
                      _代表仅仅一个字符的通配符
            eg. where_like(a='%hello%')
            eg. where_like('%{}%',a='hello')
        """

        conds = [(k, v) for k, v in kwargs.items() if v is not None]
        if _like_format:
            conds = [(k, [_like_format.format(v)]) for k, v in conds]

        return self._where(True, '`{0}` LIKE {v}', conds)

    like = where_like

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

    def _join(self, tablename, alianame, _conds):
        """对kwargs做处理"""

        conds = []
        _tb1 = alianame if alianame else tablename

        for k1, k2 in _conds:
            if type(k2) == tuple:
                if len(k2) == 1:
                    conds.append('`{0}`.`{1}` = `{2}`.`{3}`'.format(_tb1, k1, self.tb1_alias if self.tb1_alias else self.tb1_name))
                elif len(k2) == 2:
                    conds.append('`{0}`.`{1}` = `{2}`.`{3}`'.format(_tb1, k1, *k2))

            else:
                conds.append('`{0}`.`{1}` = {2}'.format(_tbl, k1, k2))

        if alianame:
            self.join_expr.append('JOIN {0} AS {1} ON {2}'.format(tablename, alianame, 'AND'.join(conds)))

        else:
            self.join_expr.append('JOIN {0} ON {1}'.format(tablename, 'AND'.join(conds)))

        return self

    def join(self,tablename, alias=None, **kwargs):
        """
            连表查询：
                eg. table0.join('table1', 't', id=('table0','id',))
                  .select(('table0', all), ('t', 'g'),('t', 'e', 'eee'))
                等同于：select table0.*， t.g, t.e AS eee FROM table0 JOIN  ON table1 as t
                        where  table1.id = table0.id
        """
        if len(kwargs) < 1:
            raise Exception('must have 1 least cond when join a table.')
        return self._join(tablename, alias, list(kwargs.items()))


    @staticmethod
    def _colsafe(col):
        """
            对查询的参数作处理
            eg: select('user_id', 'user_name',  )
                处理后:['user_id','user_name']
            eg. select((None,"id","pid"),)
                处理后：["id" AS "pid"]
            eg：select(('tableA', 'user_id', 'user_id_alias'),)
                处理后:['`tableA`.`user_id` AS `user_id_alias`']
            eg. select(('tableA', 'user_id'), ('tableB', 'email'),)
                处理后：['`tableA`.`user_id`', '`tableB`.`email`']
            eg. select(('tableA', all),)
                处理后：['`tableA`.*']
        """
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
            分组操作
        eg. groupby('col_a', ('table1', all) ,('table1', 'col_a'), ('table1', 'col_b', 'col_b_alias') )
        """
        self.group_by_cols = [self._colsafe(a) for a in args]
        return self

    def orderby(self, *args):
        """
        排序操作
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
        限制查询的行数
        eg. limit(5)
        """
        self.limit_expr = 'LIMIT %s' % int(i)
        return self

    def offset(self, i):
        """
        offset的使用必须有limit
        eg. offset(5)
        """
        if self.limit_expr is None:
            raise Exception('can not offset before limit')

        self.offset_expr = 'OFFSET %s' % int(i)

        return self

    def _select_makeup(self, cols, forupdate):
        """对查询的字段处理后生成标准的sql语句"""

        return '''SELECT {COLS} FROM {TBL} {AS}
{JOIN_EXPR} {WHERE} {WHERE_EXPR} 
{GROUPBY} {GROUPBY_COLS} {ORDERBY} {ORDERBY_COLS}
{LIMIT} {OFFSET} {FORUPDATE}'''.format(
            COLS=','.join(cols),
            TBL=self.tb1_name,
            AS='AS ' + self.tb1_alias if self.tb1_alias else '',
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
        """sql执行的具体的值"""
        return tuple(self.where_args)

    def select(self,*args):
        """
            获取指定字段的值
            eg. select('user_id', 'user_name',  )

            和其他表 join 时，为了避免字段名冲突，可以这样写
            eg. select(('tableA', 'user_id', 'user_id_alias'),)
            eg. select(('tableA', 'user_id'), ('tableB', 'email'),)
            eg. select(('tableA', all),)
        """
        cols = [self._colsafe(a) for a in args]
        cols = cols if cols else ['*']
        """调用Database中的__call__"""
        return self._conn(self._select_makeup(cols, False), self._select_values())

    def select_for_update(self, *args):
        """
        加排它锁：
        对结果集中每行数据都添加排他锁，其他线程对该记录的更新与删除操作都会阻塞
        """
        cols = [self._colsafe(a) for a in args]
        cols = cols if cols else ['*']
        return self._conn(self._select_makeup(cols, True), self._select_values())

    def count(self):
        """
            统计查询到的行数
        """
        cols = ['count(1)']
        return self._conn(self._select_makeup(cols, False), self._select_values())[0][cols[0]]

    def one(self, col=None, default=None):
        """
            返回一条数据  返回的字段值有限制
                        如果col为None，则获取数据的所有字段值
                                     要么获取某个字段值
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
            返回一条数据  返回的字段值无限制
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

    def _insert_makeup(self):
        """对添加值得字段处理后生成标准的sql语句"""
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
            新增数据 接收dict的数据格式 如果value值为list，tuple，dict 则需将value序列化
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
            新增数据 数据格式为关键字
        """
        return self.append(kwargs)

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
        """新增"""
        return self.add(kwargs)

    def _update_makeup(self):
        """"对更新值的字段处理后生成标准的sql语句"""
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
            更新操作
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




Database.loadconfig('edb.yaml')
print(Database('fdm').pro_investment_project.select("id","pid"))
print(Database('fdm').pro_investment_project.where(id = 20).select("id","pid"))
