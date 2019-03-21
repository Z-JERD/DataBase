
##################pymysql的安装##############
'''
PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。
在python安装pymysql pip install pymysql 报错时
用pip install -i http://pypi.douban.com/simple/ pymysql
或者 pip install -i http://pypi.douban.com/simple/ pymysql pymysql 安装
'''
##################pymysql的使用##############
'''
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
'''

##################增删改查操作##############
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
##################异常种类##############
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
