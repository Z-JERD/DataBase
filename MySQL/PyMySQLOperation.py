##################pymysql的安装###########
'''
PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。
在python安装pymysql pip install pymysql 报错时
用pip install -i http://pypi.douban.com/simple/ pymysql
或者 pip install -i http://pypi.douban.com/simple/ pymysql pymysql 安装
'''
##################pymysql的使用###########
'''
import pymysql
#连接databases
conn =pymysql.connect(host="127.0.0.1", #数据库地址
                      port=3306,         #端口号
                      user="root",
                      password="123456789",
                      database="jerd",
                      charset="utf8"     #编码注意不用-，不能写成utf-8
                      )
#得到一个可以执行SQL语句的光标对象
cursor =conn.cursor()  #默认返回元素
# 定义要执行的SQL语句
sql='select * from useinfo where name=%s and pwd=%s;'
# 执行SQL语句
cursor.execute(sql)
# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()
'''
#################pymysql注入#############
'''
sql注入
1. 我们执行的sql语句是我拿用户输入的内容动态拼接的
2. 我没有办法控制用户的输入内容  
解决办法:
让pymysql帮我拼接字符串的SQL语句
(其内部做了一些特殊符号的过滤)
# 定义一个要执行的SQL语句,用%s定义占位符
sql = 'select * from userinfo where name=%s and pwd=%s;'
# 帮我拼接字符串的SQl语句,并且去数据库执行
ret = cursor.execute(sql, [name, pwd])
'''
################增 删 改 查###############
#增 删 改等操作完成后都要提交事务 conn.commit()
#########增加操作######
'''
#1.逐个增加操作
sql='insert into useinfo (name,pwd) VALUES (%s,%s)'
# cursor.execute(sql,[name,pwd])
#2.批量增加
data=[
    ("xiaodan","dandan"),
    ("dan","960926")
        ]
cursor.executemany(sql,data)
conn.commit()
3.异常回滚
import pymysql
conn = pymysql.connect(host="127.0.0.1", #数据库地址
                      port=3306,         #端口号
                      user="root",
                      password="123456789",
                      database="jerd",
                      charset="utf8"     #编码注意不用-，不能写成utf-8
                      )
cursor =conn.cursor()
sql='insert into useinfo(name,pwd) VALUES(%s,%s);'
# cursor.execute(sql,["alex"])  #TypeError: not enough arguments for format string
try:
    cursor.execute(sql,["jock",456])
    cursor.execute(sql, ["fei"])
    conn.commit()
except Exception as e:
    print(str(e))
    # 有异常就回滚
    conn.rollback()
cursor.close()
conn.close()
4.获取最后一个id
last_id=cursor.lastrowid
print("最后的id是：",last_id)
'''
#########修改操作######
'''
sql='update useinfo set pwd=%s where name=%s;'
# cursor.execute(sql,["dan521","dan"]) #注意顺序
'''
#########删除操作######
'''
sql='delete from useinfo where name=%s;'
cursor.execute(sql,["dan"])
conn.commit()
cursor.close()
conn.close()
'''
#########查询操作######
'''
sql='select * from useinfo where name=%s and pwd=%s;'
ret=cursor.execute(sql,[name,pwd])
if ret:
    print("登陆成功")
else:print("登录失败")
如果前面已有查询语句，在没查询的内容下再进行查找
1. 查一条     --> cursor.fetchone()
2. 查所有     --> cursor.fetchall()
3. 查指定条数 --> cursor.fetchmany(3)
4. 移动光标
    1. cursor.scroll(1, mode="absolute")  光标按绝对位置移动1
    2. cursor.scroll(1, mode="relative")  光标按照相对位置(当前位置)移动1
    3.cursor.scroll(-1,mode="relative") #光标上移，只能使用relative
import pymysql
conn =pymysql.connect(host="127.0.0.1", #数据库地址
                      port=3306,         #端口号
                      user="root",
                      password="123456789",
                      database="jerd",
                      charset="utf8"     #编码注意不用-，不能写成utf-8
                      )
cursor =conn.cursor()
sql='select name,pwd from useinfo;'
cursor.execute(sql)

# print("查询指定个数")
# ret=cursor.fetchmany(2)  #显示第二条第三条 并不是第一条第二条
# print(ret)
# print("查询所有")  #显示剩下的所有
# ret=cursor.fetchall()
# print(ret)
#光标移动
cursor.scroll(1, mode="absolute") #指到第几个数据，光标就会移到哪个数据后
ret=cursor.fetchone()   #光标移到第一条数据后，显示第二条数据
print(ret)
cursor.scroll(1,mode="relative")  #当前光标在第二条数据后，移动一个到第三条数据后，取到第四条数据
ret=cursor.fetchone()
print(ret)
cursor.scroll(-1,mode="relative") #光标上移，只能使用relative
ret=cursor.fetchone()
print(ret)
cursor.close()
conn.close()
'''
##################返回字典格式数据#############
'''
import pymysql
conn =pymysql.connect(host="127.0.0.1", #数据库地址
                      port=3306,         #端口号
                      user="root",
                      password="123456789",
                      database="jerd",
                      charset="utf8"     #编码注意不用-，不能写成utf-8
                      )
# cursor =conn.cursor() 返回元祖类型的数据 ((value1,value2),(value1,value2))
cursor =conn.cursor(cursor=pymysql.cursors.DictCursor) #返回字典类型的数据 [{key1:value1,key2:value2},{key1:value1,key2:value2}]
sql='select name,pwd from useinfo;'
cursor.execute(sql)
ret=cursor.fetchmany(2)
print(ret)
cursor.close()
conn.close()
'''

