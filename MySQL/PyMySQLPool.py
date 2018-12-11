import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=20,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=0,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456789',
    database='code_count',
    charset='utf8'
)

def on_open(cur=pymysql.cursors.DictCursor):
    """
    连接到连接池中,返回的数据格式为dict
    1.启动时会在内存中维护一个连接池
    2.当请求需要连接数据库时则去连接池中获取一个连接,如果有空闲的连接就去获取
     没有则等待或报错
    :param cur:
    :return:
    """
    conn=POOL.connection()
    cursor=conn.cursor(cursor=cur)
    return conn,cursor

def on_close(conn,cursor):
    """
     关闭连接,使用完毕后,需要将连接归还到连接池中
    """
    cursor.close()
    conn.close()
def fetchone(sql,args,cur=pymysql.cursors.DictCursor):
    """
    查询一条数据
    """
    conn,cursor = on_open(cur)
    cursor.execute(sql, args)
    result = cursor.fetchone()
    return result

def fetchall(sql,args,cur=pymysql.cursors.DictCursor):
    """
     满足条件的全部查询出来
    """
    conn, cursor = on_open(cur)
    cursor.execute(sql, args)
    result = cursor.fetchall()
    return result

def exec_sql(sql,args,cur=pymysql.cursors.DictCursor):
    """
    增,删,改操作
    """
    conn, cursor = on_open(cur)
    cursor.execute(sql, args)
    conn.commit()