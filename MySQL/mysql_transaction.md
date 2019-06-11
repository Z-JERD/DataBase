## MySQL事务：
    比如说，在人员管理系统中，你删除一个人员，你即需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！
    1.在 MySQL 中只有使用了 Innodb 数据库引擎的数据库或表才支持事务。
    
    2.事务处理可以用来维护数据库的完整性，保证成批的 SQL 语句要么全部执行，要么全部不执行。
    
    3.事务用来管理 insert,update,delete 语句
    
    在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。因此要显式地开启一个事务务须使用命令 BEGIN 或 START TRANSACTION，或者执行命令 SET AUTOCOMMIT=0，用来禁止使用当前会话的自动提交。
    
## 事务的性质：必须满足4个条件（ACID）
    1.原子性：一个事务中的所有操作，要么全部完成，要么全部不完成

    2.一致性：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。

    3.隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力

    4.持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
    
## 事务控制语句：
    1.BEGIN 或 START TRANSACTION 显式地开启一个事务；
    
    2.COMMIT 会提交事务，并使已对数据库进行的所有修改成为永久性的；
    
    3.ROLLBACK 回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；
    
    4.SAVEPOINT identifier，SAVEPOINT 允许在事务中创建一个保存点，
    
    5.SET TRANSACTION 用来设置事务的隔离级别。
    
## MYSQL 事务处理主要有两种方法：
    1、用 BEGIN, ROLLBACK, COMMIT来实现
    
        BEGIN 开始一个事务
        ROLLBACK 事务回滚
        COMMIT 事务确认
    2、直接用 SET 来改变 MySQL 的自动提交模式:
    
        SET AUTOCOMMIT=0 禁止自动提交
        SET AUTOCOMMIT=1 开启自动提交

## MYSQL事务并发处理:
    1.事务的并发问题
        脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据
        
        不可重复读：事务 A 多次读取同一数据，事务 B 在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果 不一致。
        
        幻读：系统管理员A将数据库中所有学生的成绩从具体分数改为ABCDE等级，但是系统管理员B就在这个时候插入了一条具体分数的记录，
                当系统管理员A改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读
    2.事务隔离级别
        MYSQL为了解决并发问题，其数据库底层设计了几种隔离级别来解决存在的事务并发问题。
        mysql默认的事务隔离级别为repeatable-read
        
        事务隔离级别	                    脏读	            不可重复读	            幻读
        读未提交（read-uncommitted）	     是	                是	                  是
        不可重复读（read-committed）	     否	                是	                  是
        可重复读（repeatable-read）	     否	                否	                  是
        串行化（serializable）	         否	                否	                  否
        
    3.并发的处理机制;  
        对于多数应用程序，可以优先考虑把数据库系统的隔离级别设为Read Committed，它能够避免脏读取，而且具有较好的并发性能。
        但是它会导致不可重复读、幻读这些并发问题。这些问题我们可以由应用程序等采用悲观锁或乐观锁来控制

## 事务隔离机制：
    1、read-uncommitted
        打开两个客户端A和B，并设置其当前事务模式为read uncommitted，然后查询该表，可以看到二者查询到的数据和原始数据相同
        客户端C未开始事务
        
        客户端A:
        
        mysql> set session transaction isolation level read uncommitted;
        Query OK, 0 rows affected (0.00 sec)
        
        mysql> start transaction;
        Query OK, 0 rows affected (0.00 sec)
        
        mysql> select * from goods;
        +----+-------+-----+-------+
        | id | name  | age | count |
        +----+-------+-----+-------+
        |  1 | jerd  |  30 |    25 |
        |  2 | jerry |  25 |    22 |
        +----+-------+-----+-------+
    
    
        客户端B进行修改:
        
            mysql> set session transaction isolation level read uncommitted;
            Query OK, 0 rows affected (0.00 sec)
            mysql> start transaction;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> update goods set count = 100 where id = 1;
            Query OK, 1 row affected (0.00 sec)
            Rows matched: 1  Changed: 1  Warnings: 0
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
           
        此时，客户端B的事务还未提交，由客户端A和C查询一下表数据 可以看到从客户端A中立马就可以查询到客户端B所做的修改。
        
            客户端A:
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
            
            
            客户端C:
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |    25 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
        
        此时，我们回滚客户端B中的操作
        客户端B：
            mysql> rollback;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |    25 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
            
        客户端A：
        mysql> select * from goods;
        +----+-------+-----+-------+
        | id | name  | age | count |
        +----+-------+-----+-------+
        |  1 | jerd  |  30 |    25 |
        |  2 | jerry |  25 |    22 |
        +----+-------+-----+-------+
        2 rows in set (0.00 sec)
        
        客户端A所获取到的数据100为脏数据。要想解决这一问题，我们必须保证其他客户端正在修改但并未提交的数据不应该被本客户端获取 需要上升事务隔离级别为read-committed
        
    2、read-committed
        打开两个客户端A和B，并设置其当前事务模式为read committed
        客户端A：
            mysql> set session transaction isolation level read committed;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> start transaction;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |    25 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
    
        客户端B进行修改：
            mysql> set session transaction isolation level read committed;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> update goods set count = 100 where id = 1;
            Query OK, 1 row affected (0.01 sec)
            Rows matched: 1  Changed: 1  Warnings: 0
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
        
        此时，客户端B的事务还未提交，由客户端A和C再来查询一下表数据，可以看到从客户端A中没有看到客户端B中的修改
            客户端A：
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                2 rows in set (0.00 sec)
        
            客户端C：
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                2 rows in set (0.00 sec)
                
        从客户端B中提交刚才的事务 查看客户端A和C中的数据变化
        
        客户端B：
            mysql> commit;
            Query OK, 0 rows affected (0.01 sec)
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
    
        客户端A：
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
    
        
            客户端C：
                mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |   100 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            2 rows in set (0.00 sec)
            
        客户端A的当前事务中查询表数据，发现数据发生了变化，但客户端A的用户未在当前事务中修改该数据为100 。这就引发了同一事务中的数据重复读取不一致问题，即不可重复读的问题
        
        如何解决事务并发时的不可重复读问题呢？我们需要把事务隔离级别进一步上升为MYSQL默认的事务隔离级别repeatable read(可重复读)。
    
    3、repeatable-read
            打开两个客户端A和B，并设置其当前事务模式为repeatable-read，然后查询该表，可以看到二者查询到的数据和原始数据相同。
            客户端A：
            mysql>  set session transaction isolation level repeatable read;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql>  start transaction;
            Query OK, 0 rows affected (0.00 sec)
            
            mysql> select * from goods;
            +----+-------+-----+-------+
            | id | name  | age | count |
            +----+-------+-----+-------+
            |  1 | jerd  |  30 |    25 |
            |  2 | jerry |  25 |    22 |
            +----+-------+-----+-------+
            
            客户端B进行修改：
                mysql>  set session transaction isolation level repeatable read;
                Query OK, 0 rows affected (0.00 sec)
                
                mysql>  start transaction;
                Query OK, 0 rows affected (0.00 sec)
                
                mysql> update goods set count=100  where id = 1;
                Query OK, 1 row affected (0.00 sec)
                Rows matched: 1  Changed: 1  Warnings: 0
                
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |   100 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                
            此时，客户端B的事务还未提交，由客户端A和C再来查询一下表数据 A和C均改变
            客户端A：
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                2 rows in set (0.00 sec)
                
            客户端C：   
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                2 rows in set (0.00 sec)
    
            从客户端B中提交刚才的事务，在客户端A的当前事务中查询表数据,数据仍不变
                客户端B：
                    mysql> commit;
                    Query OK, 0 rows affected (0.01 sec)
                    
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |   100 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
                    2 rows in set (0.00 sec)
                客户端A：   
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |    25 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
    
                客户端C：
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |   100 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
                    
            从客户端A提交当前事务，并查询表数据，会发现数据变了 。这会让客户端A的用户认为刚才事务中操作时读取的数据不对，即产生幻觉。我们称之为幻读
            客户端A：
                mysql> commit;
                Query OK, 0 rows affected (0.00 sec)
                
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |   100 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                2 rows in set (0.00 sec)
    
            如何解决事件并发的幻读问题呢？那就需要进一步提升事件隔离级别为serializable
    
    4、serializable(串行化)
        打开两个客户端A和B，并设置其当前事务模式为serializable，然后查询该表，可以看到二者查询到的数据和原始数据相同。
            客户端A：
                mysql> set session transaction isolation level serializable;
                Query OK, 0 rows affected (0.00 sec)
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
            客户端B：
                mysql> set session transaction isolation level serializable;
                Query OK, 0 rows affected (0.00 sec)
                
                mysql> start transaction;
                Query OK, 0 rows affected (0.00 sec)
                
                
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |   100 |
                |  2 | jerry |  25 |    22 |
            
    
    
                
            再在客户端A中修改数据，会报错，提示表被锁，无法插入
            客户端A：
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |    25 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
                    mysql> update goods set count=200  where id = 1;
                    ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
                    
            客户端C:
                
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |    25 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                
            客户端B提交后，A再去更新，能够成功
            客户端B：
                mysql> commit;
                Query OK, 0 rows affected (0.00 sec)
                
                mysql> select * from goods;
                +----+-------+-----+-------+
                | id | name  | age | count |
                +----+-------+-----+-------+
                |  1 | jerd  |  30 |   100 |
                |  2 | jerry |  25 |    22 |
                +----+-------+-----+-------+
                
            客户端A：
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |   100 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
                    2 rows in set (0.00 sec)
                    
                    mysql> update goods set count=200  where id = 1;
                    Query OK, 1 row affected (0.00 sec)
                    Rows matched: 1  Changed: 1  Warnings: 0
                    
                    mysql> select * from goods;
                    +----+-------+-----+-------+
                    | id | name  | age | count |
                    +----+-------+-----+-------+
                    |  1 | jerd  |  30 |   200 |
                    |  2 | jerry |  25 |    22 |
                    +----+-------+-----+-------+
