
#windows下的配置
"""
安装Complete Type 修改下配置即可
安装Custom Type 需要自定义 如下：
开启的端口:27017
把安装包中的bin文件路径添加到环境变量
    1.MongoDB将数据目录存储在db目录下,需要手动创建 创建一个data/db
        /data/db 是 MongoDB 默认的启动的数据库路径 如果数据库目录不是/data/db，可以通过 --dbpath 来指定。
        启动服务端：mongod --dbpath D:\MongoDB\data\db
    2.启动客户端：mongo
    3.将MongoDB服务器作为Windows服务运行:通过任务管理器手动打开服务
        1.在data中创建log文件夹 
        2.在data的同目录下创建一个mongod.cfg文件；
            先创建一个mongo.txt文件，再打开，点击”另存为“，将底下的文件类型更改为”全部类型“，并更改文件名称为mongo.config。
        3.编辑mongod.config文件，添加以下信息；
            dbpath=D:\software\MongoDB\data\db
            logpath=D:\software\MongoDB\data\log\mongo.log
        4.在MongoDB的安装路径bin目录下下执行:
            mongod --config "D:\Mongodb\mongod.config" --install --serviceName "MongoDB"
设置密码：
    1.设置root用户
        1.use admin
        2.db.createUser({user:"testAdmin",pwd:"123456",roles:[{role:"userAdminAnyDatabase",db:"admin"}]})
        3.重启mongodb服务
            mongod --dbpath D:\MongoDB\data\db --auth
    2.对单个数据库设置用户、密码
        1.use test1
        2.db.createUser({user:'test2admin',pwd:'123456',roles:[{role:'readWrite',db:'test1'}]})
"""

#MongoDB：非关系型数据库
'''
1.介于关系型数据库和非关系数据库之间的产品,是非关系数据库中功能最丰富的
2.MongoDB和关系型数据库最大的区别就是约束性,没有主键约束和数据类型约束等
    1.MongoDB，作为优秀的非关系型数据库,更适合于存储文档等非结构型数据。彼此独立的文档更适合于使用mongoDB存储
    2.查询功能比较强大，擅长查询JSON数据，能存储海量数据，但是不支持事务,对于CPU占用非常小
    3.MongoDB支持一个upsert选项，即：“如果记录存在那么更新，否则插入”。MongoDB的update方法还支持Modifier
    通过Modifier可实现在服务端即时更新，省去客户端和服务端的通讯
3.应用场景：数据表结构变化较为频繁，数据量特别大
4.内存管理机制
    Redis数据全部存在内存，定期写入磁盘，当内存不够时，可以选择指定的LRU算法删除数据。
    MongoDB数据存在内存，由linux系统mmap实现，当内存不够时，只将热点数据放入内存，其他数据存在磁盘。
MongoDB的数据结构:
User=[
    {
        "_id":ObjectId("514sx23465571d22"),
		"name"="zhao",
        "age"=18,
        'gender':"man"
    },
    {
         "_id":ObjectId("514sx23465571d22"),
		"name"="ruby",
        "age"=18,
        'gender':"woman"
    },
]

MongoDB的每个表(Collection)中存储的每条数据(Documents)都是一个一个的Json,Json中的每一个字段(Key)我们称之为:Field
'''

#MongoDB的数据类型
'''
1.Object ID :Documents自生成的_id 无法被序列化 需要转换为str
2.String :字符串,必须是utf-8
3.Boolean：布尔值 true或false
4.Integer:整数
5.Double：双精度浮点值(没有float类型,所有的小数都是Double）
6.Arrays：数组或者列表
7.object:python中的字典
8.Null 空数据类型 none null
9.Timestamp 时间戳
10.Date 当前时间
'''

#MongoDB的增删改查操作
'''
MongoDB的默认数据库为"db"
创建数据库和表
数据库：
    1.创建并使用数据库：use
        use zhaoguangfei (数据库不存在就新建,存在就使用) 
        db.auth("adminUser", "adminPass") #验证用户名和密码
        查看当前数据库：db
    2.查看所有的数据库：show dbs    新创建的数据库不会显示，需要增加数据后才会显示
    3.删除数据库：db.dropDatabase()  删除当前数据库
集合：(数据表)：
    1.创建表:db.jerd
    2.查看:show tables
    2.删除表：db.jerd.drop()
       
增,删,改,查操作
1.添加:db.collection.insert(document)
    1.insert:插入一条或者多条。不再推荐
              1.一条:db.jerd.insert({"name":"ruby"})
              2.多条:db.jerd.insert([{"name":"go"},{"name":"ruby"}])
              3.将插入的数据定义为一个变量：
              相同key值得value的类型可以不同
              document = ({"name":"菜鸟教程",'price':30,'publish':'北京出版社'})
               document = ({"name":"python",'price':'100','publish':'北京出版社'})
              db.jerd.insert(document)
              
    推荐的写法,和insert的返回值不同
    1.insertOne:插入一条,
                db.jerd.insertOne({"name":"ruby"})
    2.insertMany：插入多条
                 db.jerd.insertMany([{"name":"go"},{"name":"ruby"}])
2.查询(find,findone)
    1.find() 将该表中所有符合条件的数据全部返回
    2.findOne() 查找一条数据,有多条数据符合条件的话,只返回最靠前的那条数据
        db.jerd.findOne({"name":"go"})
3.修改/更新数据
    ({"条件"},{"关键字":{"修改内容"}})
    1.update:不推荐 如果条件为空,会修改所有的数据
    推荐的写法：
    1.updateOne:修改一条数据的内容
        db.jerd.updateOne({"name":"go"},{$set:{"name":"ruby"}})
    2.updateMany：多条修改
        db.jerd.updateMany({"name":"ruby"},{$set:{"name":"Ruby"}})
4.删除数据:
        不推荐：1.remove 删除所有的数据
                 db.jerd.remove({})
               2.remove({"name":"Ruby}) 删除满足条件的所有数据
                db.jerd.remove({"name":"Ruby}
        推荐的写法:
        1.deleteOne
            db.jerd.deleteOne({"name":"Ruby"})
        2.deleteMany 删除所有满足条件的数据
            db.jerd.deleteMany({"name":"Ruby"})
'''

#update操作之修饰器$
'''
修改器 $inc $set $unset $push $pull $pop
    "$"  在 update中加上关键字 就 变成了 修改器
    $ 字符代表下标,位置 使用update的话,满足条件的数据下标位置就会传递到$字符中
    $ 只储存一个下标
    1.$inc 将查询到的结果加上某个值,然后保存 
     db.jerd.updateMany({"username":"jerd"},{$inc:{"age":1}})
     减法操作：
     db.jerd.updatemany({"username":"jerd"},{$inc:{"age":-1})
    2.$set:1.修改指定的 Field 字段
            2.字段不存在就新建
    
    3.$unset:用来删除Field
    db.jerd.updatemany({"username":"jerd"},{'$unset':{"english":1})
    {$unset:{"english" : 1}} 就是删除 "english" 这个 field
    4.$push
    用来对Arry(list)尾端数据进行增加新数据
    db.jerd.updatemany({"username":"jerd"},{'$push':{"test_list":6})
    5.$pull:制定删除Array中的某一元素
    如果Array中有多个6,会全部删除
    db.jerd.updatemany({"username":"jerd"},{'$pull':{"test_list":6})
    6.$pop 删除指定的Array中的第一个或者最后一个元素
    删除最后一个元素：
        db.jerd.updateMany({"username":"jerd"},{'$pop':{"test_list":1}})
    删除第一个元素：
        db.jerd.updateMany({"username":"jerd"},{'$pop':{"test_list":-1}})
'''


#MongoDB的查询操作之关键字(条件操作符)
'''
1.关键字:$lt $gt $gte $lte $in  $type
    1.$lt 小于
    db.jerd.find({"sorce":{'$lt':80}})
    2.$gt 大于
    db.jerd.find({"age":{'$gt':20}})
    3.$gte 大于等于
    db.jerd.find({"age":{'$gte':20}})
    4.$lte 小于等于
    db.jerd.find({"age":{'$lte':25}}
    db.jerd.find({"age":{'$lt':25,'$gt':20}}
    5.or
    db.jerd.find({id:{'$in':[100,200,300]}})
    6.and
    db.jerd.find({id:{'$gt':100,'$lt':200}})
    6.$type根据数据类型进行匹配
        类型           数字
        Double          1
        String          2
        Object          3
        Arrays          4
        Object ID       7
        Boolean         8
    db.demo.find({"title" : {$type : 2}}) 查找title值为String的数据

        

'''

#对Array Object的查询操作
'''
{
    "name" : "jerd",
    "price" : [
        19800,
        19500,
        19000,
        18800
    ],
    "other" : {
        "start" : "2018年8月1日",
        "start_time" : "08:30",
        "count" : 150
    }
}
Array操作：
    {"username":"jerd","test_list":[1,2,3,4,5],"price":[19800,19500,19000,18800]}
    1.将test_list中的第一个元素改成6
        db.jerd.updatemany({"username":"jerd"},{$set:{"test_list.0":6})
    2.保存满足条件的元素的下标。不知道某个元素的下表时
    db.jerd.updateOne({"price":{$get:1900}},{$inc:{"price.$":-100}})
    3.混合用法,如果price.1小于19800,就加200
    db.jerd.updateOne({"username":"jerd","price.1":{$lt:19800}},{$inc:{"price.1":200}})	
Object操作：
1.把other中 count 改为 199
db.jerd.updateOne({"username":"jerd"},{$set:{"other.count":199}})
注意:如果没有"other.count"这个field的话,会自动创建
{
    "name" : "jerd",
    "price" : [
        {
            "start_time" : "08:30",
            "count" : 150
        },
        {
            "start_time" : "09:30",
            "count" : 160
        },
}
把count大于160的field加 15
db.jerd.updateOne({"username":"jerd","price.count":{$gt:160}},{$inc:{"price.$.count":15}})

'''

#MongoDB的查询操作之limit skip sort
'''
db.jerd.insertMany(
                  [{"name":"python","price":19800},
                    {"name":"go","price":17800},
                    {"name":"linux","price":16800},
				   ])

1.limit 从第一条开始获取,指定获取的个数
获取前两条：
    db.jerd.find().limit(2)
2.skip 跳过指定的个数
获取第三条：
    db.jerd.find().skip(2)
limit和skip结合 skip的优先级高
获取第二条和第三条数据
    db.jerd.find().skip(1).limit(2)
3.sort排序： mysql中使用order by排序
    升序：
        db.jerd.find().sort({"price":1}) 
    降序：
        db.jerd.find.sort({"price":-1}) 
    pymongo操作sort时,使用 db.jerd.find.sort({"price":-1})会报错
    正确用法：db.jerd.find.sort([("price",-1)])
选取第二条第三条 并 按照 price 进行 升序排列
db.jerd.find().skip(1).limit(2).sort({"price":1})
结果：
    {"name":"go","price":17800},
    {"name":"python","price":19800},
按照执行应该是：
    {"name":"linux","price":16800},               
    {"name":"go","price":17800},
重点： Sort + Skip + Limit 是有执行优先级的  
      优先 Sort 其次 Skip 最后 Limt
'''
#在python中操作mongodb pymongodb
'''
#连接pymongo

1.pip install pymongo==3.1.1
2.from pymongo import MongoClient
client = MongoClient('localhost', 27017)
3.选择制定的数据库 账号密码认证
db=client.story
db.authenticate("account", "password")
4.选择操作的表 db.video

#增删改查

1.增：
    单条：insert_one()
    多条：insert_many()
2.删除：
    单条：delete_one
    所有满足条件的：delete_many
改:  
    单条：update_one
    所有：update_many
2.查
    单条：find_one()
    所有：find()  #值为生成器
    


'''
#练习题
'''
STUDENT_LIST = [
    {"username": "小黑", "age": 20, "gender": "男", "hobby": ["女孩", "王者荣耀"],
     "course": [{"name": "Python", "scour": 60},
                {"name": "JavaScript", "scour": 59}]},
    {"username": "小白", "age": 21, "gender": "女", "hobby": ["男孩", "王者荣耀"],
     "course": [{"name": "Python", "scour": 80},
                {"name": "JavaScript", "scour": 99}]}
]
# 小黑改为小帅帅 + 小白改为小漂漂
# 小帅帅,小漂漂,原有年龄+5岁
# 小帅帅的hobby + 吃鸡
# 小漂漂的hobby + 奇迹暖暖
# 小帅帅和小漂漂 加入学科HTML 分数为 70
# 查询爱好"女孩"的学生性别
# 查询爱好"奇迹暖暖"的学生名称
# 小帅帅和小漂漂 谁有60分以下的课程
# 小帅帅和小漂漂 谁有80分以上的课程
#  小帅帅和小漂漂 谁有60分以下的课程 并显示课程名 分数 姓名
# 小帅帅和小漂漂 谁有80分以上的课程 并显示课程名 分数 姓名
# 学科中加入comment : "优秀"  ( <60 : 不及格, >=60 <80: 中 , >=80 <90: 良 , >=90 优)	


'''