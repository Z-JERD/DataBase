##在python中使用redis##
"""
	redis单线程,单进程的处理
	Redis Python API同时提供Redis和StrictRedis用于实现Redis的命令，其中：
    StrictRedis用于实现大部分官方的命令，并使用官方的语法和命令
    Redis是StrictRedis的子类，用于向后兼容旧版本的Redis Python API。 官方推荐使用StrictRedis类

	pip install redis
	1.每次建立：Redis
		import redis
		1.r=redis.Redis(host='10.211.55.4', port=6379,password = '123456',db=0)
		2.r=redis.StrictRedis(host='10.211.55.4', port=6379,password = '123456',db=0)
		值均为bytes类型
		    conn.get('name') b'zhao'
		    conn.hgetall('zhao_1')  {b'k1': b"{'k1_1': 'v1_1'}", b'k2': b'v2'}
		r=redis.Redis(host='127.0.0.1', port=6379,password = '123456',db=0,decode_responses=True)
		    conn.get('name') 'zhao'
		    conn.hgetall('zhao_1')  {'k1': "{'k1_1': 'v1_1'}", 'k2': 'v2'}


	2.使用连接池：
		本质:维护一个已经和服务端连接成功的socket,以后再次发送数据,
			 直接获取一个socket,直接send数据
		1.每个Redis实例都会维护一个自己的连接池
		2.使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销
		3.直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
		import redis
		pool=redis.ConnectionPool(host='10.211.55.4', port=6379)
		1.r=redis.Redis(connection_pool=pool)
		2.r=redis.StrictRedis(connection_pool=pool)
		r.set(key,value)

"""

#在django中使用redis##
"""
在django中使用redis
	1.pip install django-redis
	2.在stting中配置CACHES
		CACHES = {
			"default": {
				"BACKEND": "django_redis.cache.RedisCache",
				"LOCATION": "redis://127.0.0.1:6379/1", #默认用的数据库0
				"OPTIONS": {
					"CLIENT_CLASS": "django_redis.client.DefaultClient",
					"CONNECTION_POOL_KWARGS": {"max_connections": 100}
					# "PASSWORD": "密码",
				}
			}
		}
	3.调用
		from django_redis import get_redis_connection
		conn = get_redis_connection("default")
		conn.set('a','b')
		或者
		from django.core.cache import cache
		cache.set('a','b')
"""

##管道和事物##
"""
管道(事物):pipline 将数据操作放在内存中，只有成功后，才会一次性全部放入redis
	每次请求都会创建和断开一次连接操作,如果想在一次请求中指定多个命令
	使用pipline来实现
		import redis
		pool=redis.ConnectionPool(host='10.211.55.4', port=6379)
		r=redis.Redis(connection_pool=pool)
		pipe=r.pipline(transaction=True) #打开事务
		pipe.multi()
		pipe.set("name","zhao")
		pipe.set("age",18)
		pipe.excute()
		
使用事务DEMO：
	import redis
    from redis import WatchError
    from threading import Thread

    r=redis.Redis(host='127.0.0.1', port=6379,password = '123456',db=0,decode_responses=True)

    # 减库存函数, 循环直到减库存完成
    # 库存充足, 减库存成功, 返回True
    # 库存不足, 减库存失败, 返回False
    def decr_stock(i):
        # python中redis事务是通过pipeline的封装实现的
        with r.pipeline() as pipe:
            while True:
                try:
                    # watch 监控库存键, multi后如果该key被其他客户端改变, 事务操作会抛出WatchError异常
                    pipe.watch('goods_num')
                    count = int(pipe.get('goods_num'))
                    if count > 0:  # 有库存
                        # 事务开始
                        pipe.multi()
                        pipe.decr('goods_num',2) #每次减少2
                        # execute返回命令执行结果列表, 这里只有一个decr返回当前值
                        print("this is thread {} is working,value is {}".format(i,pipe.execute()[0]))
                        return True
                    else:
                        return False
                except WatchError as ex:
                    # 打印WatchError异常, 观察被watch锁住的情况
                    print(ex )
                    pipe.unwatch()

    def worker(i):
        while True:
            # 没有库存就退出
            if not decr_stock(i):
                break

    r.set("goods_num", 100)
    # 多进程模拟多个客户端提交
    for i in range(1,3):
        Thread(target=worker,args=(i,)).start()
"""

##发布订阅##
"""
发布和订阅：
    Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息
        r = redis.Redis(...)
        订阅：
            p = r.pubsub()
        1.subscribe(channel2,channel3)  订阅一个或多个符合给定模式的频道
        2.psubscribe('my-*', ..)
            每个模式以 * 作为匹配符，比如 it* 匹配所有以 it 开头的频道
        3.p.get_message() 查看订阅的消息  如果无消息返回None
         p.listen() 读取消息会阻塞，一直等待接收到消息
        4.取消订阅
            1.p.unsubscribe()
            2.p.punsubscribe('my-*')
        发布：
            r.publish(channel message) 将信息发送到指定的频道
DEMO:
	import redis
	class RedisHelper:
		def __init__(self):
			self.__conn = redis.Redis(host='127.0.0.1', port=6379,password = '123456',db=0)
			self.chan_pub= 'test'

	#发送消息
		def public(self,msg):
			self.__conn.publish(self.chan_pub,msg)
			return True
	#订阅
		def subscribe(self):
			#打开收音机
			pub = self.__conn.pubsub()
			#调频道
			pub.subscribe(self.chan_pub)
			#准备接收
			pub.parse_response()
			return pub
	#订阅者：
	obj = RedisHelper()
	redis_sub = obj.subscribe()

	while True:
		msg = redis_sub.parse_response()
		print('接收：',msg)

	'''
	发布者
	'''

	from  redishelper import RedisHelper

	obj = RedisHelper()
	obj.public('how are you?')
"""



