# 索引概念
    索引:
            简单的说,相当于图书的目录,可以帮助用户快速的找到需要的内容.
            在MySQL中也叫做“键”，是存储引擎用于快速找到记录的一种数据结构。能够大大提高查询效率
    索引本质：
            通过不断地缩小想要获取数据的范围来筛选出最终想要的结果，同时把随机的事件变成顺序的事件



# 索引方法
    B+TREE索引：
        B+树是一种经典的数据结构，由平衡树和二叉查找树结合产生
        在B+树中，所有的记录节点都是按键值大小顺序存放在同一层的叶节点中。(数据存放在叶子上）
        叶节点间用指针相连，构成双向循环链表，非叶节点（根节点、枝节点）只存放键值，不存放实际数据。
        通常其高度都在2~3层，查询时可以有效减少IO次数
        系统从磁盘读取数据到内存时是以磁盘块（block）为基本单位的，位于同一磁盘块中的数据会被一次性读取出来，而不是按需读取
    
    b+树的查找过程：
        1.如果要查找数据项30，那么首先会把磁盘块1由磁盘加载到内存，此时发生一次IO，
        2.在内存中用二分查找确定30在28和65之间，锁定磁盘块1的P2指针,通过磁盘块1的P2指针的磁盘地址把磁盘块由磁盘加载到内存，发生第二次IO，
        3.30在28和35之间，锁定当前磁盘块的P1指针，通过指针加载磁盘块到内存，发生第三次IO，同时内存中做二分查找找到30，结束查询，总计三次IO
    
    HASH索引：
        hash就是一种（key=>value）形式的键值对,允许多个key对应相同的value，但不允许一个key对应多个value
        为某一列或几列建立hash索引.hash索引可以一次定位,具有极高的效率.
        f('Arjen') = 2323 对某个值加hash索引，经哈希算法作为key值，其所在的行的内存地址作为vlaue值
        solt  value
        2323  pointer to row 1
        如果索引的时范围，需要一次一次查。



# 索引类型

## 索引的种类：
    INDEX(普通索引)：         允许出现相同的索引内容
    UNIQUE(唯一索引)：        不可以出现相同的值，字段值可以为NULL
    PROMARY KEY(主键索引)：   不允许出现相同的值，且不能为空
    组合索引：                 N个字段组合成一个索引，列值的组合必须唯一

    primary key 和 unique 即是约束又是索引 

## 查看索引：
    SHOW INDEX FROM PERSON 

## 添加索引:ALTER和CREATE
    索引名index_name可选，缺省时，MySQL将根据第一个索引列赋一个名称
    ALTER TABLE 表名 ADD 索引类型 （unique,primary key,index）[索引名]（字段名）
        //唯一索引
            alter table person add unique (name)

        //主键索引
            alter table person add primary key (name)

         //普通索引
            alter table person add index index_name (name)

        // 组合索引
            alter table person add index index_name_age (name, age)

    CREATE INDEX index_name ON table_name(username(length))
        //唯一索引
             create unique index index_name on person (name)
        //普通索引
             create index index_name on person (name)
        // 组合索引
             create index name_age on person (name, age)

## 删除索引: DROP 和 ALTER
     //删除唯一索引 普通索引 合索引
          drop index index_name on person
          或
          alter table person drop index index_name

    //删除主键索引
            ALTER TABLE PERSON DROP PRIMARY KEY;
            如果当前主键为自增主键,则不能直接删除.需要先修改自增属性,再删
            alter table tb3 modify id int ,drop primary key;

    // 建表时创建索引 id：主键索引 card:唯一索引 普通索引:phone 组合索引:(age, name)
        create table index_demo(
            id int not null auto_increment primary key,
            name varchar(10) not null,
            age  int,
            card bigint not null unique,
            phone varchar(10),
            address varchar(32),
            remarks TEXT default null,
            index index_phone (phone),
            index age_name  (age,name)
    
        )ENGINE=INNODB DEFAULT CHARSET=utf8mb4;

    强制使用某个索引：select * from table force index(idx_user) limit 2。
    禁止使用某个索引：select * from table ignore index(idx_user) limit 2。
    禁用缓存(在测试时去除缓存的影响)：select SQL_NO_CACHE from table limit 2


# 组合索引详解

建了一个(a,b,c)的组合索引，那么实际等于建了(a),(a,b),(a,b,c)三个索引
最左匹配原则: 从左往右依次使用生效，如果中间某个索引没有使用，那么断点前面的索引部分起作用，断点后面的索引没有起作用；

## 组合索引示例说明：
    //  用到(abc)索引
        select * from mytable where a=3 and b=5 and c=4;
        等同于：
            select * from mytable where  c=4 and b=6 and a=3; where里面的条件顺序在查询之前会被mysql自动优化
    // 索引均未使用
        select * from mytable where b=3 and c=4;  a索引没有使用 bc都没有用上索引效果

    // 只用到a索引
        select * from mytable where a=3 and c=7

        select * from mytable where a>4 and b=7 and c=9; 用完a索引后 数据就无序了 b和c均不会走索引

    // 用到ab索引
        select * from mytable where a=3 and b>7 and c=3  b是范围值，也算断点

    语句中使用order by：是否使用索引也是看断点是否存在
        //ab索引
            select * from mytable where a=3 order by b;

        //a索引
            select * from mytable where a=3 order by c;

        //未走索引
            select * from mytable where b=3 order by a;  先执行where条件不走b索引

## 如何确定组合索引的字段顺序：：
    根据字段的值的复杂度和相似度，越复杂,相似度越低的越靠前(区分度也高)
    如：表中的name,sex，age 组合索引的顺序应是 (name, age, sex)



# 查看SQL的查询计划
## 查看查询计划：
    explain + 查询SQL -- 用于显示SQL执行信息参数，根据参考信息可以进行SQL优化
    例：
        explain  select count(*) from userinfo where  id = 1;
        
        运行上面的sql语句后你会看到，下面的表头信息：
	    select_type | table | type | possible_keys | key | key_len | ref | rows | Extra
	    
	    
	    1.select_type :                          显示查询类型： simple 简单查询 primary 最外层查询 derived 子查询 union联合
	    2.table                                  显示这一行的数据是关于哪张表的
        3.type                                   连接的类型 
                                                 type=NULL　在优化过程中就已得到结果，不用再访问表或索引
                                                 type=const/system 常量 const用于比较primary key 或者unique索引 只匹配一行数据
                                                 type=eq_ref  使用主键或唯一性索引
                                                 type=ref   这是一种索引访问
                                                 type=ALL   进行完整的表扫描 
                                                 type=index  扫描表  但index是从索引中读取的，而all是从硬盘中读
        
        4.possible_keys                          显示可能应用在这张表中的索引
        5.key                                    实际使用的索引
        6.key_len                                使用的索引的长度
        7.ref                                    显示索引的哪一列被使用了
        8.rows                                   返回请求数据的行数
        9.Extra                                  关于MYSQL如何解析查询的额外信息    



# 慢日志查询

将mysql服务器中影响数据库性能的相关SQL语句记录到日志文件，通过对这些特殊的SQL语句分析，改进以达到提高数据库性能的目的。

## 查看是否开启慢查询日志和日志的位置：
    show variables like 'slow_query%';
    Centos日志默认在：/var/lib/mysql/localhost-slow.log 

## 方式1：
    开启慢日志：
        set global slow_query_log = on;
        
    设置慢日志存放的位置
        set glbal slow_query_log_file = 'slow.log'
        
    设置超时的时间：
        set global long_query_time = 2;
        
## 方式2：
    在配置文件中配置：Linux中 在/etc/my.cnf 在[mysqld]下的下方加入添加：
        
        slow_query_log = ON
        slow_query_log_file = slow.log
        long_query_time = 1
    重启mysql服务
    
## 测试生成的Log
    select sleep(5);

## 用 mysqldumpslow 去分析：
    -t：限制输出的行数
    -s：根据什么来排序默认是平均查询时间 at
    -v：输出详细信息
    [root@localhost ~]# mysqldumpslow -v -s t  -t 10 /var/lib/mysql/localhost-slow.log




# 500W数据测试

## 1.创建表
    CREATE TABLE userInfo(
        id int NOT NULL,
        name VARCHAR(16) DEFAULT NULL,
        age int,
        sex char(1) not null,
        email varchar(64) default null
    )ENGINE=MYISAM DEFAULT CHARSET=utf8mb4;

## 2.创建存储过程
    delimiter$$
    CREATE PROCEDURE insert_user_info(IN num INT)
    BEGIN
        DECLARE val INT DEFAULT 0;
        DECLARE n INT DEFAULT 1;
        -- 循环进行数据插入
        WHILE n <= num DO
            set val = rand()*50;
            INSERT INTO userInfo(id,name,age,sex,email)values(n,concat('alex',val),rand()*50,if(val%2=0,'女','男'),concat('alex',n,'@qq.com'));
            set n=n+1;
        end while;
    END $$
    delimiter;

## 3.调用存储过程,插入500万条数据
    call insert_user_info(5000000);

## 测试索引:
    1. 在没有索引的前提下测试查询速度
        SELECT * FROM userinfo WHERE id = 4567890;
        无索引情况,把数据表从头到尾扫描一遍,此时有多少个磁盘块就需要进行多少IO操作,所以查询速度很慢.
        为某个字段段建立索引,建立速度会很慢
        CREATE INDEX idx_id on userinfo(id);
    2.在索引建立完毕后,以该字段为查询条件时,查询速度提升明显
        select * from userinfo where id  = 4567890;

