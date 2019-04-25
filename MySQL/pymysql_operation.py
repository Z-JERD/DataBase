
##################pymysql的安装##############

"""
PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。
在python安装pymysql pip install pymysql 报错时
用pip install -i http://pypi.douban.com/simple/ pymysql
或者 pip install -i http://pypi.douban.com/simple/ pymysql pymysql 安装


"""

##################pymysql的使用###############

"""
import pymysql
1.连接配置信息：       
    config = { 
        'host':'127.0.0.1', 
        'port':3306, 
        'user':'root', 
        'password':'123', 
        'db':'t1', 
        'charset':'utf8mb4',         
        'cursorclass':pymysql.cursors.DictCursor, 
        'connect_timeout': 3.0,
        'autocommit': True   #自动提交
    }        
2.建立连接  
    connection = pymysql.connect(**config)   
3.创建游标
    conn = connection.cursor()  
4.定义要执行的SQL语句
    sql='select * from useinfo where name=%s and pwd=%s;'
5.执行SQL，并返回收影响行数，如果发生错误就回滚
    try:
        
        row = conn.execute(sql, args)
        #connection.commit()
    
    except:
        conn.rollback()
6.关闭光标对象
    conn.close()
7.关闭数据库连接
    connection.close()


"""


##################增删改查操作#################

"""
 如果配置信息中为定义自动提交，则执行INSERT UPDATE DELETE SQL语句后需要手动提交才会connection.commit() 操作才会生效
 cursor =conn.cursor() 默认返回元祖类型的数据,定义返回字典的格式  cursor =conn.cursor(cursor=pymysql.cursors.DictCursor)

1.INSERT:
    sql = "INSERT INTO person(name,age) VALUES(%s,%s)"
    逐个增加：  cursor.execute(sql,("jerry",20))
    批量增加：  cursor.executemany(sql,(('python',3),('java',4)))

2.UPDATE: 
     sql='UPDATE useinfo SET pwd=%s where name=%s;'
     cursor.execute(sql,("JERRY","DAN"))    需保证值的顺序
     
3.DELETE:   
    sql='DELETE from useinfo where name=%s;'
    cursor.execute(sql,("dan"))
    
4.SELECT:
    查询不存在的数据，不会报错，返回的结果为空
    对于select操作，执行sql后获取结果需要额外的操作
    conn.fetchone()     取得一条数据
    conn.fetchmany(n)   取得n条数据
    conn.fetchall()    取得全部的数据


rowcount    sql操作的返回的数据行数或影响行数    
description     列名的相关信息,    查询操作时具有的属性
    使用场景：判定SQL语句是不是查询操作
        例：
             row = conn.execute(sql, args)
             if conn.description:conn.fetchone()
        

lastrowid       最新自增ID          添加操作时的属性   
    使用场景：新增数据后，获取到最新的id
        例:
            if not conn.lastrowid:
                return conn.lastrowid
"""

####################事务操作###################

"""

MySQL默认使用autocommit模式，也就是说，当你执行一个更新操作后，MySQL会立刻将结果进行提交。关闭自动提交命令为：set autocommit=0;

如果配置信息中开启了自动提交设置,则事务会无效

import pymysql
import traceback

conn =pymysql.connect(host="10.110.1.230",
                      port=3306,
                      user="root",
                      password="123456789",
                      database="zgf",
                      charset="utf8mb4" ,
                      cursorclass=pymysql.cursors.DictCursor,
                      connect_timeout=3.0,
                      #autocommit= True
                      )
cursor =conn.cursor()

sq1_1 = "update index_demo set remarks = '测试_2' where id = 1"
sql_2 = "update index_demo set card= %s where id = %s"

try:
    r = cursor.execute(sq1_1)
    r = cursor.execute(sql_2,("测试",2))
except Exception as e:
    conn.rollback()
    err = traceback.format_exc()
    print(err)
else:
    conn.commit()

"""

#####################异常种类##################

"""
异常	                    描述
Warning	                当有严重警告时触发，例如插入数据是被截断等等。必须是 StandardError 的子类。
Error	                警告以外所有其他错误类。必须是 StandardError 的子类。
InterfaceError	        当有数据库接口模块本身的错误（而不是数据库的错误）发生时触发。 必须是Error的子类。
DatabaseError	        和数据库有关的错误发生时触发。 必须是Error的子类。
DataError	            当有数据处理时的错误发生时触发，例如：除零错误，数据超范围等等。 必须是DatabaseError的子类。
OperationalError	    指非用户控制的，而是操作数据库时发生的错误。例如：连接意外断开、 数据库名未找到、事务处理失败、内存分配错误等等操作数据库是发生的错误。 必须是DatabaseError的子类。
IntegrityError	        完整性相关的错误，例如外键检查失败等。必须是DatabaseError子类。
InternalError	        数据库的内部错误，例如游标（cursor）失效了、事务同步失败等等。 必须是DatabaseError子类。
ProgrammingError	    程序错误，例如数据表（table）没找到或已存在、SQL语句语法错误、 参数数量错误等等。必须是D



1.pymysql.err.InternalError:
        1. insert时，数值的数据类型和定义的类型不同时，发生此异常
        2. insert时，列名和列值数量不一致
        3. 连接的数据库不存在

    
2.pymysql.err.ProgrammingError:
        SQL语句语法错误 参数数量错误
        例：
            sql = "insert into person values(%s,%s)"
            cursor.execute(sql, ('zhao'))
3.pymysql.err.OperationalError
        操作数据库时发生的错误  如：连接意外断开、 数据库密码错误 
4.pymysql.err.IntegrityError
        如某个字段设置了unique,但添加重复值，会抛出此异常

5.查看具体的异常信息
    import traceback
    exc = traceback.format_exc()

"""

#####################in / not in 的使用################
"""
操作字段的类型为int：
    错误的写法：
        sql = 'select * from goods where id in %s'%(('1,2'))
        
        未知变量%s需要用()包起来

    拼接可以成功：   
        a = [1, 2]
        b = ",".join([str(i) for i in a])
        sql = "select * from goods where id in (%s)"%b
        row = cursor.execute(sql )
        
    传参执行失败;
        sql = "select * from goods where id in (%s)"
        print(sql)
        row = cursor.execute(sql,(b,) )


操作的字段为char类型：
    sql = "select * from goods where name in ('jerd','jerry')"
    等同于：
        sql = "select * from goods where name in (%s)"%("'jerry', 'jerd'")   
    
    a = ['jerry', 'jerd']
    b = ",".join(["'" + i + "'" for i in a])
    
    SQL拼接能够成功：
        sql = "select * from goods where name in (%s)"% b
    传参的方式会失败
        sql = "select * from goods where name in (%s)"
        row = cursor.execute(sql, (b,) )
  """

#####################Json字段##################

"""
查询字段类型为JSON的值 表中数据如下：
    +----+-------+-----+-------+------------------+
    | id | name  | age | count | content          |
    +----+-------+-----+-------+------------------+
    |  1 | jerd  |  30 |   200 | {"uid1": "zhao"} |
    |  2 | jerry |  25 |    22 | NULL             |
    |  3 | zhao  |  22 |   100 | NULL             |
    |  4 | fei   |  21 |   222 | NULL             |
    |  5 | zhao  |  20 |   100 | {"uid5": null}   |
    +----+-------+-----+-------+------------------+

1.查询content不为空的数据
     mysql> select * from goods where content is not null;
    +----+------+-----+-------+------------------+
    | id | name | age | count | content          |
    +----+------+-----+-------+------------------+
    |  1 | jerd |  30 |   200 | {"uid1": "zhao"} |
    |  5 | zhao |  20 |   100 | {"uid5": null}   |
    +----+------+-----+-------+------------------+

2.查询id为1的的content的value值是否为null，不为null 打印数据
    mysql> select * from goods where content -> '$.uid1' is not null;
    +----+------+-----+-------+------------------+
    | id | name | age | count | content          |
    +----+------+-----+-------+------------------+
    |  1 | jerd |  30 |   200 | {"uid1": "zhao"} |
    +----+------+-----+-------+------------------+
    
    mysql> select * from goods where content -> '$.uid1' is  null;
    +----+-------+-----+-------+----------------+
    | id | name  | age | count | content        |
    +----+-------+-----+-------+----------------+
    |  2 | jerry |  25 |    22 | NULL           |
    |  3 | zhao  |  22 |   100 | NULL           |
    |  4 | fei   |  21 |   222 | NULL           |
    |  5 | zhao  |  20 |   100 | {"uid5": null} |
    +----+-------+-----+-------+----------------+
    
PyMySQL 传参查询
    SQL = "select * from goods where content -> '$.uid%s' is not null"
    ROW = cursor.execute(SQL, (5,))
    
    Pro = cursor.fetchall()
    print(Pro[0]['content'], type(Pro[0]['content']))       <class 'str'>
    print(type(json.loads(Pro[0]['content'])))              <class 'dict'>

添加JSON数据：
    sql = "insert into goods(name, age, count, content) values(%s, %s, %s, %s)"
    args = ('ruby', 19, 200, json.dumps({'uid6': 'ruby/19'}))
    row = cursor.execute(sql, args)

"""

#####################select中if的用法##################
"""

if(sex=0,'女','男') as sex 如果sex等于0 则显示为女 否则显示为男

mysql> SELECT * FROM goods;
    +----+---------+-----+-------+---------------------+--------+
    | id | name    | age | count | content             | status |
    +----+---------+-----+-------+---------------------+--------+
    |  1 | jerd    |  30 |   200 | {"uid1": "zhao"}    |      1 |
    |  2 | jerry   |  30 |   100 | NULL                |      2 |
    |  3 | zhao    |  22 |   100 | NULL                |      2 |
    |  4 | fei     |  22 |   100 | NULL                |      2 |
    |  6 | ruby    |  25 |   200 | {"uid6": "ruby/19"} |      3 |
    |  7 | jinyan  |  20 |   100 | NULL                |      3 |
    |  8 | jinxing |  23 |   100 | NULL                |      3 |
    |  9 | haha    |  22 |   122 | NULL                |      1 |
    +----+---------+-----+-------+---------------------+--------+
    8 rows in set (0.00 sec)


mysql> select id,if(status=3,1,0) as chech_status from goods;
    +----+--------------+
    | id | chech_status |
    +----+--------------+
    |  1 |            0 |
    |  2 |            0 |
    |  3 |            0 |
    |  4 |            0 |
    |  6 |            1 |
    |  7 |            1 |
    |  8 |            1 |
    |  9 |            0 |
    +----+--------------+
    8 rows in set (0.00 sec)

mysql> select id,if(status=3,'通过','未通过') as chech_status from goods;
    +----+--------------+
    | id | chech_status |
    +----+--------------+
    |  1 | 未通过       |
    |  2 | 未通过       |
    |  3 | 未通过       |
    |  4 | 未通过       |
    |  6 | 通过         |
    |  7 | 通过         |
    |  8 | 通过         |
    |  9 | 未通过       |
    +----+--------------+
    8 rows in set (0.00 sec)

"""
