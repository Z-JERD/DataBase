 ## 操作数据库方式：

###1.查询：
    1.使用原生sql
        self.db_fdm("select *  from fdm_message where receiver=%s and read_status=1 order by id desc limit 5" % me['user_id'])
    2.acct_users 表名
        简单查询：
         r = self.db.acct_users.select() 
        条件查询：
         r = self.db.acct_users.where(user_id=self.session.uid).unique()  获取到单个对象所有的字段
         r = self.db.sys_options.where(scope='sys').select()  获取满足条件所有对象的全部字段
         r = self.db.sys_options.where(scope='sys').select("type", "value", "key")  获取指定的字段
         
         self.db.ccc_chains.where(user_id=uid).unique(default={})  
         self.db.cert_private.where(id=cert['id']).unique('id', 'privatekey')
         self.db.acct_users.where_in(employed=p['organization']).where(account=account).unique()  ？？？ employed --> bigint
         
    3.连表查询：
        表1：sys_role  表2：sys_role_feature 两表相同的字段：where sys_role.role_key = sys_role_feature.role
        self.db.sys_role.join('sys_role_feature', 'rf', **{'role': ('role_key',)}).select()
        
        例：
         total = self.fdm.fdm_disk_express_detail.join('fdm_cinemas', code='cinema').where(**{'is_arrived':1}).where_like('%{}%', name="xxx").\
            where(is_cancel=0).where_in(diskimage=["2017006"]).count()
         对应的sql
        sql = 'select count(*) as num from fdm_disk_express_detail join fdm_cinemas on fdm_disk_express_detail.cinema = fdm_cinemas.code \
        where is_arrived=1 and name like xxxand is_cancel=0 and diskimage in ("2017006") '
        
    4.统计数量:where_in中数据类型为tuple
        self.fdm.fdm_project.where_in(cooperation_mode=('GF', 'F', 'M')).where_neq(ptype=99).where(invalid=0).count()
        对应的sql：
            select count(*) from fdm_project where cooperation_mode in ('GF', 'F', 'M') and ptype != 99 and invalid = 0  # [{'count(*)': 655}]
    
    5. in 不等于 排序    
        self.fdm.fdm_project.where_in(cooperation_mode=('GF', 'F', 'M')).where_neq(ptype=99).where(invalid=0).orderby("release_date","id").desc().limit 5.offset 2 .select("id","pid","name")
        对应的sql:
            select id, pid,name from fdm_project where cooperation_mode in ('GF', 'F', 'M') and ptype != 99 and invalid = 0 order by release_date desc, id desc limit 5 offset 2
    

### 2.增加：insert
    self.db.acct_users.insert(
            account=account.lower(),
            suffix=0,
            membership=2,
            community=community,
            inherit_roles=json.dumps(dict.fromkeys(inherit_roles, True)),
            roles=json.dumps(_roles),
            api_roles=json.dumps(_api_roles) if _api_roles else None,
            name=name,
            create_time=datetime.datetime.now()
        )
        
    append:
        添加成功返回此数据的id 
        self.db.acct_sessions.append({
                    'user_id': uid,
                    'ipaddress': self.env.get('REMOTE_ADDR', None),
                    'platform_key': p['platform_key'],
                    'invalid_after': datetime.datetime.now(),
                    'user_agent': self.env.get('HTTP_USER_AGENT'),
                    'createtime': datetime.datetime.now(),
                    'acl': json.dumps(list(acls)),
                })
                
    extend:
        批量添加
                
              

  
    

### 3.更新:update
        1.验证：
              employee = self.db.acct_users.where(account=account, employed=org['user_id']).unique_for_update()
              assert employee, '用户不存在'
        2.更新：更新成功返回1 更新失败返回0
               self.db acct_users.where(account=account, employed=org['user_id']).update(disable=1)
         

### 4.更新/新建:replace    
        存在就修改，不存在就新建    
        self.arch.ccc_cinema_contacts.replace(id=id,cinema_code=cinema_code,)
               

### 5.分页操作
    import datetime
    import json
    
    
    def pageinfo(page=1, pagesize=20, total=0 ):
        page = int(page)
        if page <= 0 :
            page = 1
    
        pagesize = int(pagesize)
        if pagesize <= 0 :
            pagesize = 20
    
        total = int(total)
        totalpage = abs(((-1) * total)// pagesize )
        print(totalpage)
        if page > totalpage and totalpage > 0:
            page = totalpage
    
        print(page)
    
        offset = (page - 1) * pagesize
    
        d = {"page" : page, "pagesize" : pagesize, "offset" : offset, "total" : total }
    
        d["first"] = 1
        d["prev"] = page - 1 if(page > 1) else 1
        d["next"] = page + 1 if(page < totalpage) else totalpage
        d["last"] = totalpage
    
        l = []
        i = -4
        while i < 6 :
            if page + i  >= 1 and page +i <= totalpage :
                l.append(page + i )
            i = i + 1
        d["links"] = l
    
        return d
    
    page_info = pageinfo(1,20,200)
    print(page_info)