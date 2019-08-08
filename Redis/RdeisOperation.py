"""
Python操作redis：https://cloud.tencent.com/developer/article/1151834

windows环境下：
    1.开启服务端：在cmd下切换到redis的安装目录下执行：redis-server.exe redis.windows.conf
    2.开启客户端：redis-cli.exe -h 127.0.0.1 -p 6379
    3.查看是否设置密码：
        CONFIG get requirepass #如果requirepass的参数为空,即未设置密码
    4.Redis设置密码
        CONFIG set requirepass password
    设置密码后,客户端连接 redis 服务就需要密码验证
    AUTH password   #成功后才能操作

Redis：6379
redis是一个key-value存储系统：
	通过在内存中缓存数据和对象来减少读取数据库的次数，从而提高动态、数据库驱动网站的速度

支持存储的value类型：
	String: 字符串  一般做一些复杂的计数功能的缓存。 redis的string可以包含任何数据。比如jpg图片或者序列化的对象 。
	Hash: 散列,存储用户信息  适合用于存储对象
	List: 列表:做简单的消息队列的功能,做基于redis的分页功能
	Set: 集合  全局去重的功能  添加，删除，查找的复杂度都是O(1)
	Sorted Set: 有序集合 排行榜应用

Redis操作：
	redis的本质就是是大字典
	Redis={
			key:value
		}

	String操作:一个key对应一个value
		设置值:set
			1.set(name,value,ex=None,px=None,nx=False, xx=False)
				不存在则创建,存在则修改
				ex,过期时间(秒) px 毫秒 nx=True 只有name不存在时,才执行
										xx=True 只有name存在时,才执行
				子操作：
					setnx(name, value) name不存在时,才执行
					setex(name, value, time) time过期时间(秒)
					psetnx(name,time_ms,value) time_ms过期时间(毫秒)
			2.mset(*args,**kwargs)批量设置
				mset(k1="v1",k2="v2")或mset({'k1': 'v1', 'k2': 'v2'})
			3.追加过期时间：
                expire(name,time) 秒
		获取值:get
			1.get(name)
			    name不存在返回None  name的值不是一个str 会返回NameError
			2.mget(keys)批量获取mget('jerd',"jerry") mget(['jerd',"jerry"])
			3.getset(name,value) 设置新值并获取原来的值
			4.strlen(name) 返回name对应值的字节长度
			5.append(key,value) 在name对应的值后面追加内容
			6.getrange(name,start,end) 取范围值
			7.查看过期时间 ttl(name)
			8.判断name是否存在 exists(name)
			9.decr(name,count) 存的值为int,m每次递减count
			 incr(name,count) 递增
	Hash操作：
		redis中Hash在内存中的存储格式
			Redis={
					name--->hash
					name:{key:value}
				}
		以h开头的操作均是对hash的操作,用hash操作,数据均以bytes存储
		{
			shopping_car_key：{b'title': b'Python\xe5\x85\xa8\xe6',
					}
		}
		1.添加:hset
			1.hset(name,key,value)
				不存在就创建,存在就修改
				 r.hset('zhao','k1','v1')
			2.hmset(name,maping) 在name对应的hash中批量设置键值对
				 r.hmset('zhao', {'k1':'v1', 'k2': 'v2'})
		2.查看：
			1.hget(name,key) 在name对应的hash中获取根据key获取value
			2.hmget(name,key,*args)
				获取多个key的值 r.mget("zhao",['k1','k2']
								r.hmget("zhao","k1,"k2")
			3.hgetall(name) 获取name对应hash的所有值
			4.hkeys(name) 获取对应的所有key值
			5.hvals(name) 获取对应的所有value值
			6.hexits:
				1.exists(name) 判断是否存在当前传入的key
					if not r.exists('zhao'):
				2.hexists(name,key) 判断name对应的hash是否存在当前传入的key
					if not r.exists('zhao','k1'):
			7.hscan_iter
				利用yield封装hscan创建生成器，实现分批去redis中获取数据
				name模糊匹配查看时使用scan_iter
				redis={
					zhao_1_1：{key_1：value1,key_2：value2},
					zhao_1_2：{key：value},
				}
				迭代key值:
				for i in conn.hscan_iter('zhao_1_1','key_*'):
				    print(i)
				                (b'k1_1', b'v1')
                                (b'k1_2', b'v2')
				迭代name值:
				for i in conn.scan_iter("zhao_1_*"):
				  print(i)   zhao_1_1
							 zhao_1_2
		3.删除:
			1.删除name对应的值：
				hdel(name,*keys) 将name对应的hash中指定key的键值对删除
				r.hdel('zhao',*['k1','k2'])
				r.hdel('zhao','k1')
			2.删除name对应的整条数据
				1.逐个删除
					r.delete("zhao_1_1")
					r.delete("zhao_1_2")
				2.删除
					conn.delete(*["zhao_1_1","zhao_1_2"])
				3.全部删除
					r.flushall()
	List操作：
		Redis={
					name--->list
					name:[v1,v2]
				}
	1.添加：
		1.lpush(name,values)
			每个新的元素都添加到列表的最左边
			r.lpush("zhao",11,55,88) lsit的值为[88,55,11]   list 的头部添加字符串元素
			 rpush name value  list 的尾部添加字符串元素
		2.llen(name) name对应的list元素的个数
		3.linsert(name,where,refvalue,value)
			在name对应的列表的某一个值前或后插入一个新值
			r.linsert("zhao",before,55,22) 在55前添加22
	2.删除：
		r.lrem(name, value, num)
			在name对应的list中删除指定的值,num表示删除的个数
		lpop(name) 删除列表的第一个元素
	3.修改：
		r.lset(name, index, value)
			对name对应的list中的某一个索引位置重新赋值
	4.查：
        1.lindex(name,index) 根据索引获取列表元素
        2.lrange(name, start, end) 根据列表分片获取数据

    Set操作
        1.添加：
            sadd(name,value1,vaule2...)
        2.查看
            smembers(name) 查看value值
            scard(name)  命令返回集合中元素的数量
            srandmember(name) 返回集合中的一个随机元素
        3.删除
            1.spop(name) 移除一个随机
            2.srem(name,value1,value2)  用于移除集合中的一个或多个成员元素元素
        4.sscan 用于迭代集合键中的元素
            sscan(name,cursor,match,count)
            conn.sscan('myset',0,'h*')
        5.集合间的操作：
            1.sdiff(name1,name2) 命令返回给定集合之间的差集
            2.sinter(name,name2) 返回给定所有集合的交集
            3.sunion(name1,name2)返回给定所有集合的并集
	    
     有序集合操作：https://www.cnblogs.com/huchong/p/9656882.html#_label8	   
"""
