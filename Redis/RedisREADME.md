
## Redis的持久化方式(RDB方式和AOF方式)
    参考文档： https://zhuanlan.zhihu.com/p/66008450
    
    持久化就是将内存中的数据永久保存到磁盘上
    1.RDB 持久化可以在指定的时间间隔内生成数据集的时间点快照，以二进制的方式保存到磁盘中
    
    2.AOF 持久化记录服务器执行的所有写操作命令，记录到 AOF 文件，并在服务器启动时，
          通过重新执行这些命令来还原数据集
    3.Redis 还可以同时使用 AOF 持久化和 RDB 持久化
        当 Redis 重启时， 它会优先使用 AOF 文件来还原数据集， 
        因为 AOF 文件保存的数据集通常比 RDB 文件所保存的数据集更完整
    
    比较：
        RDB适合用于进行备份,随时将数据集还原到不同的版本
        RDB 的缺点:
            一旦发生故障停机， 你就可能会丢失好几分钟的数据。
        AOF 的优点:
        设置不同的 fsync(同步) 策略，比如无 fsync ，每秒钟一次 fsync ，或者每次执行写入命令时 fsync
        AOF 的默认策略为每秒钟 fsync 一次,就算发生故障停机，也最多只会丢失一秒钟的数据
        AOF 的缺点:
            1.对于相同的数据集来说，AOF 文件的体积通常要大于 RDB 文件的体积。
            2.AOF 的速度可能会慢于 RDB
        3.让 AOF 的速度和 RDB 一样快:关闭 fsync
        
     redis的配置文件 /etc/redis/redis.conf     https://www.cnblogs.com/ysocean/p/9074787.html
     
     RDB 将数据库的快照（snapshot）以二进制的方式保存到磁盘中。

    
### RDB（Redis DB）快照模式
#### 两种策略：
    1、自动保存：BGSAVE（通过子线程来完成，不影响redis的相关主线程）
        （1）、按照配置的条件，当配置条件满足时就执行BGSAVE完成持久化操作
        （2）、非阻塞状态，redis可以正常接收处理客户请求（不阻塞redis服务）
        非阻塞状态说明：持久化由一个子线程来做（创建RDB文件），子线程处理完成后通知父线程，父线程接受到通知后，会将旧的RDB文件替换掉
        要增加内存服务器开销
        
        定时任务触发自动保存机制：
            save 900 1 #在900秒(15分钟)之后，如果至少有1个key发生变化，则dump内存快照。
            save 300 10 #在300秒(5分钟)之后，如果至少有10个key发生变化，则dump内存快照。
            save 60 10000 #在60秒(1分钟)之后，如果至少有10000个key发生变化，则dump内存快照
            
        目录位置：dir /var/lib/redis
        文件名称: dbfilename dump.rdb
    
    2、手动保存：SAVE（通过redis的相关主线程完成，阻塞redis服务）
        （1）、通过客户端发起 SAVE 命令 来完成持久化操作
        （2）、此操作会阻塞redis服务，阻塞状态下无法响应客户端的其他请求
    
    阻塞状态说明：通过客户端发起save命令，阻塞redis服务并执行持久化操作，此过程redis无法响应其他请求，持久化操作替换旧的RDB文件
    
#### RDB优点：
    （1）执行效率高
    （2）恢复大数据集速度较AOF快 
#### RDB缺点：
    （1）会丢失，最近写入、修改的而未能持久化的数据
    （2）子线程过程耗时，会造成毫秒级客户端的请求不能被响应
    
###  AOF（AppendOnlyFile）（追加模式、文本重演）
    
    AOF采用了追加的方式保存，默认文件为appendonly.aof ，文件记录了所有的操作命令（非查询命令），在服务启动时，通过命令恢复还原数据库
    AOF模式是默认关闭的，需要在redis.conf配置文件中手动开启 将appendonly no 改为 appendonly yes
    
    
#### 写入机制：
    AOF机制添加了个内存缓冲区；将持久化的内容写入缓冲区，当缓冲区满、或着用户手动执行fsnyc等时，才将缓冲区的内容写入磁盘
    
    
#### AOF重写机制
    重写过程：
        （1）fork(创建一个与原来进程几乎完全相同的进程，也就是两个进程可以做完全相同的事)一个子进程负责重写AOF文件
        （2）子进程会创建一个临时文件写入AOF信息
        （3）父进程会开辟一个内存缓冲区接收新的写命令
        （4）子进程重写完成后，父进程会获得一个信号，将父进程接收到的新的写操作由子进程写入到临时文件中
        （5）新文件替代旧文件
    重写的本质：就是将操作同一个键的命令，合并。从而减小AOF文件的体积
    
    重写机制的触发
    （1）手动
         客户端向服务器发送BGREWRITEAOF命令
    （2）自动
         配置文件中的选项，自动执行BGREWRITEAOF命令
        auto-aof-rewrite-min-size <size>
        auto-aof-rewrite-percentage <percent>

#### AOF持久化配置
    ############################## APPEND ONLY MODE ###############################
    使用状态：
        appendonly no                   //  AOF模式是默认关闭的 若使用AOF模式 将no改为yes
        
    同步方式：
        # appendfsync always            //每次有数据修改发生时都会写入AOF文件。 对硬盘压力大
        appendfsync everysec            //每秒钟同步一次，该策略为AOF的缺省策略。
        # appendfsync no                //从不同步。高效但是数据不会被持久化
        
    同步单写:
        no-appendfsync-on-rewrite no  是否在后台写时同步单写，默认是no，设置为no时表示新进程set会被阻塞，yes的时候新进程set不会被阻塞，等待后台所有执行完成以后再执行这部分set写入aof文件
        
    重写机制:
        auto-aof-rewrite-percentage 100    //当前的AOF文件比上次重写的怎张比例的大小
        auto-aof-rewrite-min-size 64mb    // 重写最小的文件大小
        
        rewrite是aof的一个机制，用来压缩aof文件，通过fork一个子进程，重新写一个新的aof文件，该次重写不是读取旧的aof文件进行复制，而是将读取内存中的redis数据库，重写一份aof文件
        解释：比旧aof文件大百分之百的时候（2倍），且aof文件的大小大于64mb的时候，触发重写机制；
    
    异常设置：   
        aof-load-truncated yes      // 默认值是yes，在写入AOF文件时，突然断电写了一半，设置成yes会log继续，如果设置成no，就直接恢复失败了。
              
#### AOF优缺点：
    优点：
    写入机制，默认fysnc每秒执行，性能很好不阻塞服务，最多丢失一秒的数据；
    重写机制，优化AOF文件；
    如果误操作了（FLUSHALL等），只要AOF未被重写，停止服务移除AOF文件尾部F LUSHALL命令，重启Redis，可以将数据集恢复到FLUSHALL 执行之前的状态。
    缺点：
    相同数据集，AOF文件体积较RDB大了很多；
    恢复数据库速度较RDB慢（文本，命令重演）

### 持久化恢复
    AOF 和 RDB 文件都可以用于服务器重启时的数据恢复，优先加载 AOF，当没有 AOF 时才加载 RDB。当 AOF 或者 RDB 存在错误，则加载失败。    
### 关闭持久化
#### 关闭rdb的命令：config set save ""
    （或者进入配置文件将：
    Save 900 1        
    Save 300 10    
    Save 60 10000   
    
    注释掉，并打开save "" 的注释，使得  save ""  生效，即可关闭rdb；
### 关闭aof的命令：config set appendfsync no 
    （或者进入配置文件，将appendonly设置为no，默认是 appendonly no ）





    

        