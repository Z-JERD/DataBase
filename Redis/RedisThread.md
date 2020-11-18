# Redis 为什么是单线程的

    Redis 中使用了 Reactor 单线程模型， 模型结构如下图所示：
    
   ![avatar](https://mmbiz.qpic.cn/mmbiz_png/g6hBZ0jzZb0Zb0XiaaR6bGaN80wicXIIP7j3SxhEXDibAdYCbYm28oUqFSbsFuJav9yGBNyoYbLl730vnc5YUyzqg/640)
    
    该模型中：接收到用户的请求后，全部推送到一个队列里，然后交给文件事件分派器，而它是单线程的工作方式。
              Redis 又是基于它工作的，所以说 Redis 是单线程的

# Redis为什么这么快？
## 参考文档: https://mp.weixin.qq.com/s?__biz=MzIzMzMzOTI3Nw==&mid=2247493427&idx=2&sn=b88f09ce2dd66f28e3d9d7d663f8663b

## 1. 基于内存实现

    对于磁盘数据库来说，是需要将数据读取到内存里的，这个过程会受到磁盘 I/O 的限制
    
    而对于内存数据库来说，本身数据就存在于内存里，也就没有了这方面的开销
    
## 2. 高效的数据结构

    Redis 中有多种数据类型，每种数据类型的底层都由一种或多种数据结构来支持。正是因为有了这些数据结构，Redis 在存储与读取上的速度才不受阻碍
    
   ![avatar](https://mmbiz.qpic.cn/mmbiz_png/g6hBZ0jzZb0Zb0XiaaR6bGaN80wicXIIP74T85YN4xkMF6icjicicf0NCpGU4yia2VNK4YKSmLf7Viaj7ia64m4buiaGiajg/640)
    
    
## 3. 合理的数据编码
    
    每一种数据类型来说，底层的支持可能是多种数据结构，什么时候使用哪种数据结构，这就涉及到了编码转化的问题。
    
    
    
    那我们就来看看，不同的数据类型是如何进行编码转化的：
    
    
    
    String：存储数字的话，采用int类型的编码，如果是非数字的话，采用 raw 编码；
    
    
    
    List：字符串长度及元素个数小于一定范围使用 ziplist 编码，任意条件不满足，则转化为 linkedlist 编码；
    
    
    
    Hash：hash 对象保存的键值对内的键和值字符串长度小于一定值及键值对；
    
    
    
    Set：保存元素为整数及元素个数小于一定范围使用 intset 编码，任意条件不满足，则使用 hashtable 编码；
    
    
    
    Zset：zset 对象中保存的元素个数小于及成员长度小于一定值使用 ziplist 编码，任意条件不满足，则使用 skiplist 编码。


    
## 4. 合适的线程模型

    1. I/O 多路复用模型同时监听客户端连接:
    
        应对大量的请求，Redis 中使用 I/O 多路复用程序同时监听多个套接字，并将这些事件推送到一个队列里，然后逐个被执行。
        最终将结果返回给客户端。
        
    2. 单线程在执行过程中不需要进行上下文切换，减少了耗时:
        
        多线程在执行过程中需要进行 CPU 的上下文切换，这个操作比较耗时。
        Redis 又是基于内存实现的，对于内存来说，没有上下文切换效率就是最高的
    
    
    
 ## 总结
 
    1.基于内存实现

        数据都存储在内存里，减少了一些不必要的 I/O 操作，操作速率很快。



    2. 高效的数据结构

        底层多种数据结构支持不同的数据类型，支持 Redis 存储不同的数据；

        不同数据结构的设计，使得数据存储时间复杂度降到最低。

   

    3. 合理的数据编码

        根据字符串的长度及元素的个数适配不同的编码格式。



    4.合适的线程模型

        I/O 多路复用模型同时监听客户端连接；

        单线程在执行过程中不需要进行上下文切换，减少了耗时。