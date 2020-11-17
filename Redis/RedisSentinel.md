# Redis哨兵（Sentinel）模式
## 参考文档： https://www.jianshu.com/p/06ab9daf921d  https://zhuanlan.zhihu.com/p/94662132

## Sentinel概念
    
    哨兵是一个独立的进程，作为进程，它会独立运行。其原理是哨兵通过发送命令，等待Redis服务器响应，从而监控运行的多个Redis实例
    
### 作用：
    1. 集群监控：负责监控Redis master和slave进程是否正常工作

    2. 消息通知：如果某个Redis实例有故障，那么哨兵负责发送消息作为报警通知给管理员
    
    3. 故障转移：如果master node挂掉了，会自动转移到slave node上
    
    4. 配置中心：如果故障转移发生了，通知client客户端新的master地址
    
## Sentinel 故障切换(failover) 原理
    
    假设主服务器A宕机，哨兵1先检测到这个结果, 系统并不会马上进行failover过程, 哨兵1 广播一个 SDOWN（自己主观认为的）消息给其他 sentinel
    后面的哨兵也检测到主服务器A不可用，并且数量达到一定值时，那么哨兵之间就会进行一次投票。 
    
    投票的结果由一个哨兵发起，进行failover操作。一个新的 master 会被选出来 如从服务器B被选为新的master, 切换成功后，就会通过发布订阅模式，让各个哨兵把自己监控的从服务器实现切换主机
    改为复制服务器B, 客户端也改为连接 B。 如果服务器A恢复, 服务器A成为服务器B的从机
    
    
    redis 的设定是只有当超过 50% 的 Sentinel 进程可以连通并投票选取新的 master 时，才会真正发生主从切换。

### 选出新master的依据
    
    1. 首先判断优先级，选择优先级较小的
        优先级是在配置文件中配置的，默认为 100
        
    2. 如果优先级相同，选择复制 offset 更大的
        slave 与 master 同步后，offset 会自动增加
        
    3. 如果复制下标也相同，就选择 runid 小的
        每个 Redis 实例都会有一个 runid，是在启动时设置的随机字符串  
    
### sentinel 有多个，具体谁来执行故障转移？
    
    多个 sentinel 会选出一个 leader，具体的选举机制是依据 Raft 分布式一致性协议
    

### sentinel 是怎么发现 slave 和其他 sentinel 的？
    
    1. 发现 slave 比较简单
     
            通过向master 发送info命令 就可以得到 slave 的地址
        
    2. 发现其他 sentinel 
            
            通过“发布/订阅”机制实现的
            每个 sentinel 都会向 __sentinel__:hello 这个频道发送消息，每秒一次，报告自己的存在
            每个 sentinel 也会订阅这个频道，就可以发现其他的 sentinel 了
            
###  故障转移后 client 怎么知道新的master地址？
    
    sentinel 就像是一个服务注册中心，可以请求 sentinel 获取当前的 master 信息
    
    Master-Slave切换后，master_redis.conf、slave_redis.conf 和 sentinel.conf的内容都会发生改变，
    即 master_redis.conf 中会多一行slaveof的配置，sentinel.conf 的监控目标会随之调换
    
### Sentinel的工作方式:
    
    1. 每个Sentinel以每秒钟一次的频率向它所知的Master，Slave以及其他 Sentinel 实例发送一个 PING 命令
    2. 每个 Sentinel 会以每 10 秒一次的频率向它已知的所有Master，Slave发送 INFO 命令
    
## Redis配置哨兵模式

### 配置3个哨兵和1主2从的Redis服务器
    服务类型	是否是主服务器	  IP地址	     端口
    Redis	    是	        192.168.11.128	6379
    Redis	    否	        192.168.11.129	6379
    Redis	    否	        192.168.11.130	6379
    Sentinel	 -	        192.168.11.128	26379
    Sentinel	 -	        192.168.11.129	26379
    Sentinel	 -	        192.168.11.130	26379

### 1. 主服务器配置 redis.conf
    
    # 使得Redis服务器可以跨网络访问
    bind 0.0.0.0
    # 设置密码
    requirepass "123456"
    
### 2. 从服务的配置 redis.conf
    # 从服务器比主服务器多一个slaveof的配置和密码
    # 使得Redis服务器可以跨网络访问
    bind 0.0.0.0
    # 设置密码
    requirepass "123456"
    # 指定主服务器
    slaveof 192.168.11.128 6379
    # 主服务器密码
    masterauth 123456
    
### 3. 哨兵配置 
    # 在Redis安装目录下有一个sentinel.conf文件  配置3个哨兵，每个哨兵的配置都是一样的
    # 禁止保护模式
    protected-mode no
    # 配置监听的主服务器，这里sentinel monitor代表监控，mymaster代表服务器的名称，可以自定义，192.168.11.128代表监控的主服务器，6379代表端口，2代表只有两个或两个以上的哨兵认为主服务器不可用的时候，才会进行failover操作。
    sentinel monitor mymaster 192.168.11.128 6379 2
    # sentinel auth-pass定义服务的密码，mymaster是服务名称，123456是Redis服务器密码
    sentinel auth-pass mymaster 123456

### 服务启动顺序
    
    首先是主机的Redis服务进程，然后启动从机的服务进程，最后启动3个哨兵的服务进程
 
### 实现流程：

    1. Sentinel集群通过配置文件发现master，启动时会监控master
    
    2. 向master发送info命令，获取其所有slave节点
    
    3. Sentinel集群向Redis主从服务器发送hello信息（心跳），包括Sentinel本身的ip、端口、id等内容，以此来向其他Sentinel宣告自己的存在
    
    4. Sentinel集群通过订阅接收其他Sentinel发送的hello信息，以此来发现监视同一个主服务器的其他Sentinel；
       集群之间会互相创建命令连接用于通信，因为已经有主从服务器作为发送和接收hello信息的中介，Sentinel之间不会创建订阅连接
    
    5. Sentinel集群使用ping命令来检测实例的状态，如果在指定的时间内（down-after-milliseconds）没有回复或则返回错误的回复，
       那么该实例被判为下线
    
    6. 当failover主备切换被触发后，并不会马上进行，还需要Sentinel中的大多数sentinel授权后才可以进行failover，
       即进行failover的Sentinel会去获得指定quorum个的Sentinel的授权，成功后进入ODOWN状态。如在5个Sentinel中配置了2个quorum，
       等到2个Sentinel认为master死了就执行failover
    
    7. Sentinel向选为master的slave发送 SLAVEOF NO ONE 命令，选择slave的条件是Sentinel首先会根据slaves的优先级来进行排序，
       优先级越小排名越靠前。如果优先级相同，则查看复制的下标，哪个从master接收的复制数据多，哪个就靠前。如果优先级和下标都相同，
       就选择进程ID较小的
    8. Sentinel被授权后，它将会获得宕掉的master的一份最新配置版本号(config-epoch)，当failover执行结束以后，
       这个版本号将会被用于最新的配置，通过广播形式通知其它sentinel，其它的sentinel则更新对应master的配置。</li>   

## Redis 复制(Replication)
    
    通过复制，实现Redis的高可用性，实现对数据的冗余备份，保证数据和服务的高度可靠性
    
### 复制过程

    1. 从数据库向主数据库发送sync(数据同步)命令。

    2. 主数据库接收同步命令后，会保存快照，创建一个RDB文件。此后客户端所有的写操作都会放到缓存中

    3. 当主数据库执行完保持快照后，会向从数据库发送RDB文件，而从数据库会接收并载入该文件。

    4. 主数据库将缓冲区的所有写命令发给从服务器执行。

    5. 以上处理完之后，之后主数据库每执行一个写命令，都会将被执行的写命令发送给从数据库。
    
## Redis 集群
    参考文档： https://juejin.im/post/5b8fc5536fb9a05d2d01fb11 
## Sentinel  实现简单的高可用
    
    高可用：在各种出现异常的情况下，依然可以正常提供服务；或者宽松一些，出现异常的情况下，只经过很短暂的时间即可恢复正常服务
    
    实现： https://juejin.im/post/5baa0169f265da0b001f34be
    
 ## Redis 主从复制、哨兵和集群这三个有什么区别
    1. 主从复制是为了数据备份
    2. 哨兵是为了高可用
    3. 集群则是因为单实例能力有限，搞多个分散压力
