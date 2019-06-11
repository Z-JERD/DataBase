# 手动提交：
    import pymysql
    import traceback
    
    conn =pymysql.connect(host="10.110.1.110",
                          port=3306,
                          user="root",
                          password="123456789",
                          database="zgf",
                          charset="utf8" ,
                          cursorclass=pymysql.cursors.DictCursor,
                          connect_timeout=3.0,
                          #autocommit= True
                          )
    cursor =conn.cursor()
    
    
    sql = "update goods set age= %s where id = %s"
    sq12 = "update goods set  age= %s where id = %s"

## sql和sql2全部执行成功，数据库才会更新，如sq1执行成功，sql2的执行失败 则sql的执行也不会更新到数据库中
    try:
        row = cursor.execute(sql, (30, 1))
        print(row)
        row = cursor.execute(sq12, ('haha', 2))
        print(row)
    
    except Exception as e:
        conn.rollback()
        err = traceback.format_exc()
        print(err)
    else:
        conn.commit()
    
## sql执行失败则sql2就不会再执行， sql执行成功。sql2执行失败则sql的操作会更新到数据库中
    try:
        row = cursor.execute(sql, (30, 1))
        conn.commit()
        row = cursor.execute(sq12, ('haha', 2))
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        err = traceback.format_exc()
        print(err)

## 并发库存问题：

    sql = "select count from goods where id = 1"
    sq12 = "update goods set  count= %s where id = 1"
    
    try:
        row = cursor.execute(sql)
        count = cursor .fetchone()
        print(count['count'])
        new_count = count['count'] - 5
        time.sleep(10)
        row = cursor.execute(sq12,(new_count))
        print(row)
    except Exception as e:
        conn.rollback()
        err = traceback.format_exc()
        print(err)
    else:
        conn.commit()
    
    启动两个终端同时执行以上代码 结果如下：
    终端1： 18 1
    终端2： 18 0
    终端1成功执行，并减掉库存，终端2读取到初始库存，修改时会判断库中的count数据和刚开始读取的数据是否相同 若不同 则不会进行修改

# 开启自动提交：
    conn =pymysql.connect(host="10.110.1.110",
                          port=3306,
                          user="root",
                          password="123456789",
                          database="zgf",
                          charset="utf8" ,
                          cursorclass=pymysql.cursors.DictCursor,
                          connect_timeout=3.0,
                          autocommit= True
                          )
                          
    cursor =conn.cursor()
    sql = "update goods set age= %s where id = %s"
    sq12 = "update goods set  age= %s where id = %s"
    
    try:
        row = cursor.execute(sql, (30, 1))
        print(row)
        row = cursor.execute(sq12, ('haha', 2))
        print(row)
    
    except Exception as e:
        conn.rollback()
        err = traceback.format_exc()
        print(err)
    sql执行失败则sql2就不会再执行， sql执行成功。sql2执行失败则sql的操作会更新到数据库中
    
    并发库存问题：自动提交和手动提交的结果一样


# Django中并发处理
    对于Django中并发处理：Django 的默认行为和mysql是一样的 是运行在自动提交模式下。任何一个查询都立即被提交到数据库中
    Django数据库事务管理API atomic(using=None, savepoint=True)
        在底层，Django的事务管理代码：
        当进入到最外层的 atomic 代码块时会打开一个事务;
        当进入到内层atomic代码块时会创建一个保存点;
        当退出内部块时会释放或回滚保存点;
        当退出外部块时提交或回退事物。
        可以通过设置savepoint 参数为 False来使对内层的保存点失效
        from django.db import transaction

    @transaction.atomic
    def viewfunc(request):
        # This code executes inside a transaction.
        do_stuff()
    
## 1.未处理订单(库存修改)并发问题
     def post(self, request):
        sku_id = request.POST.get('addr_id')
        count = request.POST.get('count')
         try:
                sku = GoodsSKU.objects.get(id=sku_id)
         except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})
        
         # 更改库存量
         sku.stock -= int(count)
         sku.save()
    
      return JsonResponse({'res': 5, 'errmsg': '订单创建成功'})  #A B 同时下单，库存都减5 如原库存为20 则A B 同时下单后库存量为15
      
## 2.悲观锁处理创建订单
        #A B 同时下单，库存都减5 如原库存为20 则A查询后加排它锁，A的事务未提交之前，B不能查询，直到A提交commit后才能查询，此时B查询的库存是15
        @transaction.atomic
        def post(self, request):
            sku_id = request.POST.get('addr_id')
            count = request.POST.get('count')
            # 设置事务保存点
            sid = transaction.savepoint()
             try:
                sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
            except GoodsSKU.DoesNotExist:
                # 回滚事务到sid保存点
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})
            # 减少商品库存，增加销量
             try:
                sku.stock -= int(count)
                sku.save()
             except Exception as e:
                # 回滚事务到sid保存点
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 7, 'errmsg': '下单失败1'})
             return JsonResponse({'res': 5, 'errmsg': '订单创建成功'}) 
             
## 3.乐观锁处理创建订单
        #A B 同时下单，库存都减5 如原库存为20 则A查询为20,B查询也为20，A修改提交后库存为15，B此时提交修改，会检查数据库此时库存是否为之前查的20
        若不相同，则更新失败
        @transaction.atomic
        def post(self, request):
            sku_id = request.POST.get('addr_id')
            count = request.POST.get('count')
            # 设置事务保存点
            sid = transaction.savepoint()
            for i in range(3):
                # 根据id获取商品的信息
                try:
                    sku = GoodsSKU.objects.get(id=sku_id)
                except GoodsSKU.DoesNotExist:
                    # 回滚事务到sid保存点
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})
                new_stock =  sku.stock- int(count)
                res = GoodsSKU.objects.filter(id=sku_id, stock=sku.stock).update(stock=new_stock)
                
                if res == 0:
                    if i == 2:
                        # 回滚事务到sid保存点
                        transaction.savepoint_rollback(sid)
                        # 连续尝试了3次，仍然下单失败，下单失败
                        return JsonResponse({'res': 7, 'errmsg': '下单失败2'})
                    # 更新失败，重新进行尝试
                    continue
                # 更新成功，跳出循环
                break
            
            return JsonResponse({'res': 5, 'errmsg': '订单创建成功'})
