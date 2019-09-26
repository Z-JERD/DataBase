# SQL介绍
SQL可以细分为DML(Update、Insert、Delete),DDL(表结构修改),DCL(权限操作),DQL(Select)操作
查询SQL，也就是一句DQL的具体流程如下

   ![avatar](https://pic1.zhimg.com/80/v2-10642194f7905175076487d8bef7adc8_hd.jpg)
    
### SQL的状态:
SQL到达服务端后，会在一个单独的线程里进行执行,由于在一个线程里执行，总有办法能看到线程的执行状态吧。
Mysql提供了下面的命令查看
        
     SHOW [FULL] PROCESSLIST
     
    出来的结果是如下：
   ![avatar](https://pic2.zhimg.com/80/v2-62cb42411a147a640631502cf2e083d9_hd.jpg)

图里Command这一列，反应的就是这个线程当前的执行状态啦。我在这个线程的执行过程中，状态是会变化很多次。 你看图里，有一个Sleep，
这是在告诉你线程正在等待客户端发送新的请求。还有一个为Query,这代表线程正在执行查询或者正在将结果发送给客户端

### SQL的执行
#### 1.查询缓存
到达服务端后，Mysql要判断我的前6个字符是否为select！ 并且，语句中不带有SQL_NO_CACHE关键字，如果符合条件，就进入查询缓存。

查询缓存，它其实是一个哈希表，它将执行过的语句及其结果会以 key-value 对的形式，被直接缓存在内存中。 它的key是一个哈希值，
是通过查询SQL、当前要查询的数据库、客户端协议版本等，生成的一个哈希值，而它的value自然就是查询结果啦
    如果要绕过查询缓存，也很简单。可以像下面这么写:

        Select SQL_NO_CACHE * from table
        
Mysql8.0版就不存在查询缓存，查询缓存不好用的原因：
    1.只要有对一个表的更新，这个表上所有的查询缓存都会被清空
    2.SQL任何字符上的不同,如空格,注释,都会导致缓存不命中
    用查询缓存的表，只有一种情况，那就是配置表。其他的业务表，根本是无法利用查询缓存的特性
 
#### 2.分析器   
解析器和预处理器统一称为分析器
#### 解析器
SQL离开查询缓存后，进入解析器,对其进行词法分析，如SQL如下：
        
        select username from userinfo
        
解析器进行词法分析，我将你从左到右一个字符、一个字符地输入，然后根据构词规则识别单词。会生成4个Token,如下所示

   ![avatar](https://pic2.zhimg.com/80/v2-9d8c1db9eb017890011f81d0920d6d01_hd.jpg)

接下来呢，进行语法解析，判断你输入的这个 SQL 语句是否满足 MySQL 语法。然后生成下面这样一颗语法树 
   
   ![avatar](https://pic2.zhimg.com/80/v2-01626d9f24c45f18f9f6efc25edac9d5_hd.jpg)

如果语法不对，收到一个提示如下！如果语法无误，将sql送往预处理器

    You have an error in your SQL syntax
    
 #### 预处理器
 先查看SQL中的列名对不对，数据库的这张表里是不是真的有这个列。再看看表名对不对，如果不对，你会看到下面的错误
    
    Unknown column xxx in ‘where clause’
 
 再给SQL送去做权限验证，如果你没有操作这个表的权限，会报下面这个错误!
     
     ERROR 1142 (42000): SELECT command denied to user 'root'@'localhost' for table 'xxx'
  
 最后这颗语法树会传递给优化器
 
#### 3.分析器 
对语法树进行优化，如SQL如下
    
    select t1.* from Table1 t1 inner join Table2 t2  on t1.CommonID = t2.CommonID
 
 分析器就是判断一下怎么样执行更快，比如先查Table1再查Table2，还是先查Table2再查Table1呢？判断完如何执行以后，生成执行计划就好啦！
 
#### 4.执行器
 就是根据执行计划来进行执行查询啦。根据指令，逐条调用底层存储引擎，逐步执行。
    
#### 5.返回结果
  Mysql会将查询结果返回客户端。 唯一需要说明的是，如果是SELECT类型的SQL，Mysql会将查询结果缓存起来。至于其他的SQL，
  就将 该表涉及到的查询缓存清空
  
#### 6.权限验证问题
有的文章说权限验证是在执行阶段，去执行前验证权限。如果是这种方式一条查询SQL经过查询缓存、分析器、优化器，执行器。
如果到最后一个阶段执行器中才发现权限不足、那不是前面一系列流程白做了
权限验证在预处理器中执行



# SQL的查询计划
    执行计划，简单的来说，是SQL在数据库中执行时的表现情况,通常用于SQL性能分析,优化等场景。在MySQL使用 explain 关键字来查看SQL的执行计划
## 查看查询计划：
    explain + 查询SQL -- 用于显示SQL执行信息参数，根据参考信息可以进行SQL优化
    例：
        explain  select count(*) from userinfo where X=? and Y=?;
        
        运行上面的sql语句后你会看到，下面的表头信息：
	    id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra
	    
	    
#### 1.id                                 
    id相同,执行顺序由上而下，id不同,值越大越先被执行
#### 2.select_type :                      
    显示查询类型： simple 简单查询 primary 最外层查询 derived 子查询 union联合
#### 3.table                              
    table表示查询涉及的表或衍生的表
#### 4.type                               
            这个字段是优化sql的重要字段，也是我们判断sql性能和优化程度重要指标 
            type=NULL　在优化过程中就已得到结果，不用再访问表或索引
            const:当查询最多匹配一行时，常出现于where条件是＝的情况，一般常用于等值扫描或者唯一性索引扫描，比如select * from A where A.id=2，这种非常快
            system: 是const的特殊情况，此时说明表中只有一行数据，直接返回。
            eq_ref:这种相当于多表之间关联查询，select A.* from A,B where A.id=B.userId,其中A中id对于B.userId是一一对应的，
                    此时查询效率较高
            ref: 此类型通常出现在多表的联合 查询，使用了非唯一或非主键索引，或者匹配最左前缀规则索引的语句。
                  比如select A.* from A where A.name='a' and A.sex='m'，name和sex构成一个组合索引
            range: 表示使用索引范围查询，通过索引字段范围获取表中部分数据记录。
                   这个类型通常出现在 =, <>, >, >=, <, <=, IS NULL, <=>, BETWEEN, IN() 操作中。
                   比如select A.* from A where A.time between a and c
            index: 表示全索引扫描(full index scan)， index 类型扫描所有的索引， 而不扫描数据。
                   index 类型通常出现在：所要查询的数据直接在索引树中就可以获取到, 而不需要扫描数据，但是索引本身数量很多，
                   内容很大，那么执行效率很低。
            ALL: 表示全表扫描，这个类型的查询是性能最差的查询之一。 那么基本就是随着表的数量增多，执行效率越慢。
            
            执行效率：
                ALL < index < range< ref < eq_ref < const < system。对于我们平时查询执行计划，优化sql来说，最好是避免ALL和index
                
             ALL(全表扫描), index(索引扫描),range(范围扫描),ref (非唯一索引扫描),eq_ref(唯一索引扫描,),(const)常数引用, 
             访问速度依次由慢到快

#### 5.possible_keys                          
    它表示Mysql在执行该sql语句的时候，可能用到的索引信息，仅仅是可能，实际不一定会用到
#### 6.key                                    
    此字段是 mysql 在当前查询时所真正使用到的索引。 他是possible_keys的子集
#### 7.key_len                                
    表示查询优化器使用了索引的字节数，这个字段可以评估组合索引是否完全被使用， 这也是我们优化sql时，评估索引的重要指标
#### 8.filtered                               
    filtered参数，它指返回结果的行占需要读到的行(rows列的值)的百分比，
    就是百分比越高，说明需要查询到数据越准确， 百分比越小，说明查询到的数据量大，而结果集很少
#### 9.ref :                                  
    匹配条件,如果走主键索引的话,该值为: const, 全表扫描的话,为null值
#### 10.rows                                   
    rows 也是一个重要的字段，mysql 查询优化器根据统计信息，估算该sql返回结果集需要扫描读取的行数，
    这个值相关重要，索引优化之后，扫描读取的行数越多，说明要么是索引设置不对，
    要么是字段传入的类型之类的问题，说明要优化空间越大
#### 11.Extra                                  
    using filesort ：表示 mysql 对结果集进行外部排序，不能通过索引顺序达到排序效果。一般有 using filesort都建议优化去掉，因为这样的查询 cpu 资源消耗大，延时大。
    using index：覆盖索引扫描，表示查询在索引树中就可查找所需数据，不用扫描表数据文件，往往说明性能不错。
    using temporary：查询有使用临时表, 一般出现于排序， 分组和多表 join 的情况， 查询效率不高，建议优化。
    using where ：sql使用了where过滤,效率较高关于MYSQL如何解析查询的额外信息    
    
 
 #### fdm_projec中pid是唯一索引
    例1：
         mysql> explain select id, pid, name from fdm_project where name = '水形物语';
        +----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+
        | id | select_type | table       | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
        +----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+
        |  1 | SIMPLE      | fdm_project | NULL       | ALL  | NULL          | NULL | NULL    | NULL |  667 |    10.00 | Using where |
        +----+-------------+-------------+------------+------+---------------+------+---------+------+------+----------+-------------+

    
    例2：
         mysql> explain select id, pid, name from fdm_project where pid = 'F2018013';
        +----+-------------+-------------+------------+-------+---------------+------+---------+-------+------+----------+-------+
        | id | select_type | table       | partitions | type  | possible_keys | key  | key_len | ref   | rows | filtered | Extra |
        +----+-------------+-------------+------------+-------+---------------+------+---------+-------+------+----------+-------+
        |  1 | SIMPLE      | fdm_project | NULL       | const | code          | code | 202     | const |    1 |   100.00 | NULL  |
        +----+-------------+-------------+------------+-------+---------------+------+---------+-------+------+----------+-------+
        
    例3：
        mysql> explain select id, pid, name from fdm_project where pid in ('F2018013','F2018010');
        +----+-------------+-------------+------------+-------+---------------+------+---------+------+------+----------+-------------+
        | id | select_type | table       | partitions | type  | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
        +----+-------------+-------------+------------+-------+---------------+------+---------+------+------+----------+-------------+
        |  1 | SIMPLE      | fdm_project | NULL       | range | code          | code | 202     | NULL |    2 |   100.00 | Using where |
        +----+-------------+-------------+------------+-------+---------------+------+---------+------+------+----------+-------------+
    
    例4：
        mysql> explain select ps.*  from pro_secondary_project as ps  inner join fdm_project as fp on ps.pid = fp.pid;
        +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+-------------+
        | id | select_type | table | partitions | type   | possible_keys | key  | key_len | ref        | rows | filtered | Extra       |
        +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+-------------+
        |  1 | SIMPLE      | ps    | NULL       | ALL    | pid           | NULL | NULL    | NULL       |   19 |   100.00 | NULL        |
        |  1 | SIMPLE      | fp    | NULL       | eq_ref | code          | code | 202     | zgf.ps.pid |    1 |   100.00 | Using index |
        +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+-------------+
        
    例5：
        mysql> explain select ps.name  from pro_secondary_project as ps  inner join fdm_project as fp on ps.pid = fp.pid group by ps.pid;
    +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+---------------------------------+
    | id | select_type | table | partitions | type   | possible_keys | key  | key_len | ref        | rows | filtered | Extra                           |
    +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+---------------------------------+
    |  1 | SIMPLE      | ps    | NULL       | ALL    | pid           | NULL | NULL    | NULL       |   19 |   100.00 | Using temporary; Using filesort |
    |  1 | SIMPLE      | fp    | NULL       | eq_ref | code          | code | 202     | zgf.ps.pid |    1 |   100.00 | Using index                     |
    +----+-------------+-------+------------+--------+---------------+------+---------+------------+------+----------+---------------------------------+




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
