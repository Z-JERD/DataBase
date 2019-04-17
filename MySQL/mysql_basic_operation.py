##########################数据库的概念############################

"""
数据库(Database，简称DB).就是一个存放数据的仓库，这个仓库是按照一定的数据结构,来组织、存储的
数据库系统有3个主要的组成部分:
    1.数据库：用于存储数据的地方。
    2.数据库管理系统：用户管理数据库的软件。
    3.数据库应用程序：为了提高数据库系统的处理能力所使用的管理数据库的软件补充。
数据库的特点:
    ⑴ 实现数据共享
    ⑵ 减少数据的冗余度
    ⑶ 数据一致性和可维护性，以确保数据的安全性和可靠性
    ⑷ 故障恢复 数据库管理系统提供一套方法，可及时发现故障和修复故障


"""

#########################数据库的操作##############################

"""
在命令行启动数据库：mysql -uroot -p
1.查询当前用户所有的数据库
    show databases;
2.创建数据库
    create database jerd;
3.使用数据库
    use jerd;
4.查看当前操作所在的数据库名称
    show database();
5.删除数据库
    drop database jerd;

"""


#########################数据表的操作##############################

"""
表是一种结构化的文件，用来存储某种特定类型的数据。表中的标题成为字段

1.显示库中的所有表和表结构
    show tables
    查看表结构：desc jerd

2.创建表：
    create table jerd（
    字段名 类型（宽度） 约束条件，
    字段名 类型（宽度） 约束条件，
    ）engine=innodb charset=utf8；
    auto_increment 自增 primary key 主键(唯一且不为空)


3.删除表：
        drop table jerd
     清空表：
        truncate table jerd
        
4.修改表的结构(对字段进行修改）
    1.添加表字段
        alter table 表名 add 字段名 类型 约束;
        alter table jerd add age int not null after name;
        在name字段后添加age字段
    2.修改表字段
        alter table student modify 字段 varchar(100) null;
        alter table student change 旧字段 新字段 int not null default 0;
        change 可以改变字段名字和属性 modify只能改变字段的属性
    3.删除表字段
        alter table jerd drop name;
    4.更新表名称：
        rename table jerd to jerry；

5.复制表
    1.复制表结构和表中数据：
        create table jerry select * from jerd
    2.只复制表结构（数据和外键不复制）
        create table jerry like jerd

"""


#########################常用的数据类型##############################

"""

create table jerd(
    字段名 类型(宽度) 约束条件,
    字段名 类型(宽度) 约束条件,
)engine=innodb default charset=utf8;

1.int 存储年龄,等级,id,各种号码等
2.小数型:m总个数 d小数位数
    1.decimal(m,d) 定点类型,存放的是精确值
    2.float(m,d) 单精度(8位精度)浮点型,存放近似值
    3.double(m,d) 双精度(16位精度)浮点型,存放近似值
3.字符型
  1.char(m) 表示固定长度的字符串,浪费空间,存取速度快
  2.varchar(m) 变长,精准,节省空间,存取速度慢
  3.text   用于保存变长的大字符串
4.日期类型
    1.DATE()       日期值YYYY-MM-DD
    2.TIME()       时间值  HH:MM:SS
    3.YEAR()       年份值
    4.DATETIME()   混合日期和时间值 YYYY-MM-DD HH:MM:SS
    5.TIMESTAMP()  时间戳
5.JSON类型

"""


#########################约束条件##############################
""""
1.非空约束: not null
2.主键约束 primary key
    主键这一行的数据不能重复且不能为空
    1.创建完表结构添加主键
        alter table jerd add primary key(name)
    2.删除主键
         alter table jerd drop primary key
3.唯一约束：unique 指定的一列的值不能有重复值
    
    1.在创建表结构时添加外键约束
    2.创建完表结构添加唯一约束
        alter table jerd add unique(name)
    3.删除唯一约束
         唯一约束也是索引
        SHOW INDEX FROM jerd 找出索引的名称
         alter table jerd drop index name
4.默认值约束：default 
5.自动增长：auto_increment
    用于主键并且是一个字段的主键，才能使用auto_increment
    create table jerd(
        id int not null,
        name varchar(10) default null,
        primary key(id),
        unique key(name)  #unique (name)    UNIQUE KEY `name` (`name`)
    )
    等同于：
    create table jerd(
        did int not null  primary key,
        name varchar(10)   default null unique 
    )
6.外键约束
    1.创建表时,创建外键约束
    create table dept(
        id int not null auto_increment primary key,
        name varchar(50)
    )engine=innodb default charset=utf8;
    
    create table person(
        id int not null auto_increment primary key,
        name varchar(250) not null,
        age int not null,
        sex enum('男','女') not null default '男',
        salary double(10,2) not null,
        dept_id int,
        constraint fk_did foreign key(dept_id) references dept(id)
)engine=innodb default charset=utf8;
    
    2.已经创建表后,追加外键约束
        alter table person add constraint fk_did foreign key(dept_id) references dept(id)
    
    3.删除外键约束
        alter table jerd drop foreign key fk_did;
    
    定义外键的条件：
        1.外键对应的数据类型必须保持一致
        2.存储引擎必须是InnoDB类型
"""


#########################表间的关系##############################

"""
总体可以分为三类: 一对一 、一对多(多对一) 、多对多
1.一对一关系：
    #身份证信息表
    CREATE TABLE card (
      id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
      code varchar(18) DEFAULT NULL,
      UNIQUE un_code (CODE) -- 创建唯一索引的目的,保证身份证号码同样不能出现重复
    );
    #公民表
    CREATE TABLE people (
      id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
      name varchar(50) DEFAULT NULL,
      sex enum('男','女') not null default '男',
      c_id int UNIQUE, -- 外键添加唯一约束,确保一对一
      CONSTRAINT fk_card_id FOREIGN KEY (c_id) REFERENCES card(id)
    );

2.一对多
    //建立人员表
    CREATE TABLE people(
        id VARCHAR(12) PRIMARY KEY,
        sname VARCHAR(12),
        age INT,
        sex CHAR(1)
    );
    //建立车辆信息表
    CREATE TABLE car(
        id VARCHAR(12) PRIMARY KEY,
        mark VARCHAR(24),
        price NUMERIC(6,2),
        pid VARCHAR(12),
        CONSTRAINT fk_people FOREIGN KEY(pid) REFERENCES people(id)
    );

3.多对多关系
    //建立学生表
    CREATE TABLE student(
        id VARCHAR(10) PRIMARY KEY,
        sname VARCHAR(12),
        age INT,
        sex CHAR(1)
    );
     //建立课程表
    CREATE TABLE course(
        id VARCHAR(10) PRIMARY KEY,
        sname VARCHAR(12),
        credit DOUBLE(2,1),
        teacher VARCHAR(12)
    );
    //建立选修表
    CREATE TABLE sc(
        sid VARCHAR(10),
        cid VARCHAR(10),
        PRIMARY KEY(sid,cid),
        CONSTRAINT fk_student FOREIGN KEY(sid) REFERENCES student(id),
        CONSTRAINT fk_course FOREIGN KEY(cid) REFERENCES course(id)
    );
"""


############################数据的增,删,改,查操作#################

"""
1.增加数据 Insert:values 和 set
    
    1.标准的添加SQL语句
        INSERT INTO tablename(列名…) VALUES(列值);
        例：使用时，列名必须和列值的数一致
            INSERT INTO users(id, name, age) VALUES(1, 'jerd', 25);
    
    2.INSERT INTO tablename SET column_name1 = value1, column_name2 = value2，…;
        INSERT INTO users SET id = 1, name = 'jerd', age = 25;
    
    如果某个字段是默认值或者自增的,可以省略这些字段
        例：id是自增的字段
                INSERT INTO user(name, age) VALUES('jerd',25);
                INSERT INTO uses SET name = 'jerd', age = 25;
                
    表名后什么都不写，就表示向表中所有的字段赋值。不仅在VALUES中的值要和列数一致，而且顺序不能颠倒
        例：
            INSERT INTO users VALUES('jerd',25)  会报错 id字段必须要赋值
            INSERT INTO users () VALUES();   将使用表中每一列的默认值来插入新记录
    INSERT语句允许一次插入多条数据，set不行
        INSERT INTO users (name, age) VALUES('jerd',25),('jerry',25)

修改和删除的数据若不存在,执行SQL相当于执行一条空语句,不会报错

2.更新操作 update
    更新符合条件字段3的数据 
        update 表 set 字段1= '值1', 字段2='值2' ... where 字段3 = 值3;
        
    连表更新：UPDATE user a, room b SET a.num=a.num+1 WHERE a.room_id=b.id。
    连表删除：DELETE user FROM user,black WHERE user.id=black.id

3.删除操作 delete
    1.整表数据删除
        delete from 表;
    2. 删除符合条件的表
        delete from 表 where 字段1=值1;
4.查询操作 select
    select * from jerd
    

MySQL 一条语句实现若记录存在则更新，不存在则插入
    REPLACE INTO students (StuName, Stuid, Class) VALUES ('张三', '123456789', '1234567');
    

语句原理
    REPLACE INTO 语句要求被插入的表需要有已经定义的主键，该语句通过对主键进行检索判断记录是否存在，若记录存在，则对非主键属性进行更新操作；若记录不存在，则插入一条新记录。
    如 id为主键，则执行上述SQL就是新增数据
    指定主键：判断id是否存在
        replace into  goods(id,name, age, count) values(8,'jinxing',22,1234);
        

    
受影响的行数:
    当相同主键记录存在，且欲更新的数据与已存在的数据完全相同时（即此时什么都不做），受影响的行数为 1。
    当相同主键记录存在，且欲更新的数据与已存在的数据不完全相同时（即此时会更新数据），受影响的行数为 2。
    当相同主键记录不存在时，将插入一条新的记录，受影响的行数为 1

"""

#############################单表查询#############################

"""
1.简单查询：
    1.查询所有：select *  from jerd
    2.查询指定字段 select name,age from jerd
    3.别名设置 as
        select age as'年龄' from person
    4.剔除重复查询
        select distinct age from jerd；
2.条件查询
    1.比较运算符 > < >= <= !=
    2.null  is null,not null
    3.and or
        select name from jerd where age=18 and salary=2000
        select name from jerd where age=18 or salary=2000
        
    查询某个字段为空的字段：
        错误的SQL： SELECT * FROM PERSON WHERE PHONE = NULL
        正确的SQL:  SELECT * FROM PERSON WHERE PHONE IS NULL
        用 “a=null”，这个结果永远为 UnKnown，where 和 having 中，UnKnown 永远被视为 false
	
   SUBSTR：
   	substr(string1, 1, 2) 就是 截取 字符串string1 第1位开始2位长度的 子串
    	select name from jerd where age=18 AND SUBSTR (phone_num, 1, 3)  == '152' 手机号的前三位是152

3.区间查询 between .. and ...
    between 10 and 20 获取10到20区间的内容

4.集合查询 in not in
  1.select name from jerd where age in (19,20,21)
  2.select name from jerd where age not in (19,20,21)

5.模糊查询 like not like
    1.% ：任意多个字符
    2._:单个字符
    1.查询姓名以"j"开头的
        select name from jerd where name like "j%";
    2.查询第二字符时j的人
        select name from jerd where name like "_j%";
    3.排除名字带j的
        select name from jerd where name not like 'j%'
6.排序查询：order  by 字段1
    1.ASC 升序(默认)
    2.DESC 降序
    order by 要写在select语句末尾
    1.select name from jerd order by salary ASC;
    2.select * from person where salary >5000 order by salary DESC;
    
    order by id desc,time desc

先是按 id 降序排列  如果 id 字段 有些是一样的话   再按time 降序排列 (前提是满足id降序排列)

7.聚合函数
    1.COUNT() 2.SUM() 3.AVG()  4.MAX() 5.MIN()
    select 聚合函数(字段) from 表名;
    
    count(1)、count(*)与count(列名)的区别:
        执行效果上：  
            count(*) count(1)包括了所有的列，相当于行数，在统计结果的时候，不会忽略值为NULL的列  
            count(列名)只包括列名那一列，在统计结果的时候，会忽略列值为空的列
        执行效率上：  
            1.列名为主键，count(列名)会比count(1)快  
            2.列名不为主键，count(1)会比count(列名)快  
            3.如果表多个列并且没有主键，则 count（1） 的执行效率优于 count（*）  
            4.如果表只有一个字段，则 select count（*）最优。
    
8.分组查询
    遇到"每"的字,一般都进行分组操作
    select 被分组的字段 from 表名 group by 分组字段
        1.select avg(salary),dept from jerd group by dept
    2.查询平均薪资大于10000的部门, 并且看看这个部门的员工都有谁?
        select avg(salary),dept from person GROUP BY dept having avg(salary)>10000;

9.分页查询 limit 
    1imit (起始条数),(查询多少条数);
    1.查询前5条数据
        select * from jerd limit 5;
    2.查询第10条到第15条数据
        select * from jerd limit 10,15   
        
    limit,offset 区别：OFFSET 必须搭配着limit才能用
            SELECT  * FROM  person   LIMIT 5 OFFSET 2;  从第3条开始读，往后读5条数据
            SELECT  * FROM  person   LIMIT 5,2;  从第6条开始读，往后读2条数据


执行优先级从高到低：where > group by > having 
where 与 having区别:
    1. Where 发生在分组group by之前，因而Where中可以有任意字段，但是绝对不能使用聚合函数。
    2. Having发生在分组group by之后，因而Having中可以使用分组的字段，无法直接取到其他字段,可以使用聚合函数
    SQL 语句的执行顺序如下:
        from---where---group by ---having ---select ---order by ---limit

"""

##############################多表查询#############################

"""
1.多表联合查询
    select * from person,dept where person.did =dept.did;
2.多表连接查询
  SELECT 字段列表
    FROM 表1  INNER|LEFT|RIGHT JOIN  表2
  ON 表1.字段 = 表2.字段;
  1.内连接查询:只显示符合条件的数据
    select * from person inner join dept on person.did = dept.did;
  2.左外链接:左边表中的数据优先全部显示
    select * from person left join dept on person.did =dept.did;
    left左边表中数据全部显示,右边表得数据符合条件的才显示,不符合的以null填充
  3.右外连接查询
    select * from person right join dept on person.did = dept.did;
3.子语句查询:
  嵌套查询:查多次,第一次的查询结果可以做第二次查询的条件或者表名使用
  select * from (select * from person) as 表名
4.关键字
    1.any和some
        select * from person where a > any(1,2,3)
         select * from person where a > some(1,2,3)
    2.all
        select * from person where a > all(1,2,3)
    3.exists 和not exists
        主查询会根据子查询的结果(True和False)来决定主查询是否得以执行
        select * from person where exists (select * from dept where did=5)
    4.判断查询IF
        select name IF(p1.salary>1000,"高端人群","低端人群") as "级别" from person

5.Union查询
     UNION 查询，它可以把需要使用临时表的两条或更多的 SELECT 查询合并的一个查询中。在客户端的查询会话结束的时候，临时表会被自动删除
     从而保证数据库整齐、高效。使用 UNION 来创建查询的时候，我们只需要用 UNION作为关键字把多个 SELECT 语句连接起来就可以了，
     要注意的是所有 SELECT 语句中的字段数目要相同
     
     SELECT Name, Phone FROM client UNION SELECT Name, BirthDate FROM author UNION SELECT Name, Supplier FROM product
 
6.临时表：临时表只在当前连接可见,当关闭连接时,Mysql会自动删除表并释放所有空间
    1.直接将查询结果导入临时表
        CREATE TEMPORARY TABLE tmp_table SELECT * FROM table_name
    2.在内存中直接创建临时表
        CREATE TEMPORARY TABLE tmp_table (
         name VARCHAR(10) NOT NULL,
         value INTEGER NOT NULL
        ) TYPE = HEAP 
        
    如果在你创建名为tmp_table临时表时名为tmp_table的表在数据库中已经存在，临时表将有必要屏蔽（隐藏）非临时表tmp_table
    什么时候用临时表呢？

    应用场景1：你在短期内有很多DML操作，比如京东淘宝亚马逊的购物车表，把东西放购物车（插入），
               变更数量（更新），删除商品（删除），一旦结算金钱后，这些数据就要清掉，这时需要用临时表

    应用场景2：在导出数据时，你可能不想导完整的数据库，或者表，你可能只想要导出符合某些条件的数据，那么你可以创建临时表，
                把选择语句插入到临时表，接着导出这个临时表，导完以后通过结束会话或者事务的方式，让这些没用的数据自动清理掉

    应用场景3：你在写存储过程时，有很多的连接，比如你需要连接A，B，C，d，E，F，G，H那么多张表，才能得到你的结果表，
                同时做连接的消耗太大，你可以先A，B，C连接的结果，放在临时表，接着再把这张临时表，跟d，E，F连接，作为新的结果放在临时表，
                接着再把临时表与G，H连接，最后得到临时表数据，一次插入到结果表（永久表）。

"""


###############################SQL逻辑查询语句执行顺序##############

"""
SELECT
    a.customer_id,
    COUNT(b.order_id) as total_orders
FROM table1 AS a  LEFT JOIN table2 AS b
ON a.customer_id = b.customer_id
WHERE a.city = 'hangzhou'
GROUP BY a.customer_id
HAVING count(b.order_id) < 2
ORDER BY total_orders DESC;  

1.FROM---2.on---3.join---4.where---5.group by---6.having---7.select--8.distinct
9.order by----10.limit

"""

###############################MySQL数据的备份##########################

"""
MySQL数据的备份：mysqldump 

导出整个数据库：包括表结构和数据
    　mysqldump -u用户名 -p密码  数据库名 > 导出的文件名 
      例：mysqldump -uroot -p123456789 zgf > database.sql

多库备份：
    mysqldump -uroot -p1234567889  --databases zgf jerd > databases.sql

备份所有的库：
    mysqldump -uroot -p123456789 --all-databases > databases.sql


导出某张表：
    mysqldump -u用户名 -p 密码  数据库名 表名> 导出的文件名 
    例：mysqldump -uroot -p123456789 zgf  person > persondata.sql

只导出数据库结构或者表结构：加参数 -d
    例：mysqldump -uroot -p123456789 -d  zgf > database.sql
        mysqldump -uroot -p123456789 -d  zgf  person > persondata.sql

导入数据库:source + 文件路径
    进入数据库控制台：
        mysql>use 数据库 
        mysql>source /root/database.sql   
"""
