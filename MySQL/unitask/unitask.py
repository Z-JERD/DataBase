import json
import sys
import time
import traceback
import uuid

import redis
import yaml
import uwsgi


class UniTask(object):
    unitask_prefix = None

    masterkey = '_system_master'

    _work_masterkey = '_%s_master'
    _work_key = '_%s_work'
    _work_pool = '_%s_workpool'

    workconfig = {}

    def __init__(self):
        """
            加载配置文件，连接Reids  定义self.sys_master

        """

        self.load_config()

        assert self.myself, 'Config not loaded.'

        self.puid = uuid.uuid4().hex

        self.sys_master = None

        self.update_master_conf()
        print("-----init----sys_master:%s,unitask_prefix:%s, unitask_port:%s, unitask_mode:%s"%(self.sys_master,self.unitask_prefix, self.unitask_port,self.unitask_mode) )
        return

    def load_config(self):
        print("=====load_config=====")

        with open('/etc/hyjh/myself.yaml', 'r') as fp:
            self.myself = yaml.load(fp)

        with open('/etc/hyjh/unitask.yaml', 'r') as fp:
            self.unitask_conf = yaml.load(fp)

        # self.unitask_port = self.myself['unitask_port']

        self.service_name = uwsgi.opt.get('srv_name', b'').decode('ascii')
        self.unitask_prefix = self.unitask_prefix if self.unitask_prefix else self.service_name

        self.unitask_port = uwsgi.opt.get('unitask_port', b'').decode('ascii')
        self.unitask_port = int(self.unitask_port) if self.unitask_port else self.unitask_conf['unitask_port']

        self.unitask_mode = uwsgi.opt.get('unitask_mode', b'').decode('ascii')

        assert self.unitask_prefix, 'unitask_name must be exists.'

        self.work_masterkey = self._work_masterkey % self.unitask_prefix
        self.work_key = self._work_key % self.unitask_prefix
        self.work_pool = self._work_pool % self.unitask_prefix

        return

    def get_one_redis(self):
        print("=====get_one_redis=====")
        # 如果uwsgi配置文件中配置了unitask_mode和unitask_port 就连接本地的redis
        if self.unitask_mode == 'master':
            return redis.Redis(host='localhost', port=self.unitask_port, decode_responses=True)
        # 连接配置的远程redis
        for uip in self.unitask_conf['unitask_ip']:
            try:
                rs = redis.Redis(host=uip, port=self.unitask_port, decode_responses=True)
                rs.ping()
                return rs
            except redis.ConnectionError:

                pass

        raise redis.ConnectionError('redis server can not connected')

        return

    def update_master_conf(self, force=False):
        print("=====update_master_conf=====")

        if force == False and self.sys_master != None:
            return True

        try:
            # 连接到redis
            rs = self.get_one_redis()
            self.sys_master = json.loads(rs.get(self.masterkey))

            return True

        except Exception as e:
            print("+++++++++++++++++++++++++++++++++++")
            print(e)

        self.sys_master = None

        return False

    def get_master_redis(self):

        try:

            rs = redis.Redis(host=self.sys_master['intranet'], port=self.unitask_port,decode_responses=True)
            rs.ping()
            return rs

        except redis.ConnectionError:
            print('%s Pika server not running' % self.masterkey)
            return

    def system_heartbeat(self, sig=None):
        print("+++++++++++++++++:system_heartbeat")
        # 获取redis中self.masterkey的值 如果不存在就新建
        masterinfo = self.get_one_redis().get(self.masterkey)
        masterinfo = json.loads(masterinfo) if masterinfo else self.myself.copy()

        if masterinfo['server-id'] != self.myself.get('server-id') and (
                time.time() - masterinfo.get('heartbeat', 0)) < 60 * 5:
            return

        masterinfo['heartbeat'] = int(time.time())

        self.get_one_redis().set(self.masterkey, json.dumps(masterinfo))

        return

    def heartbeat(self, sig=None):
        print("+++++++++++++++++:heartbeat")

        if self.update_master_conf(True) == False:
            return

        try:
            rs = self.get_master_redis()
        except redis.ConnectionError:
            print('%s Pika server not running' % self.masterkey)
            return

        masterinfo = rs.get(self.work_masterkey)
        masterinfo = json.loads(masterinfo) if masterinfo else self.myself.copy()

        if masterinfo['server-id'] != self.myself.get('server-id') and (
                time.time() - masterinfo.get('heartbeat', 0)) < 60 * 5:
            return

        masterinfo['heartbeat'] = int(time.time())
        rs.set(self.work_masterkey, json.dumps(masterinfo))

        return

    def make_work_info(self, w, d, nowt):

        wconf = self.workconfig[w]

        wname = w
        if wconf['keys'] != None:
            wname += ':' + '&'.join([str(d[k]) for k in wconf['keys']])

        milestone = None
        if wconf['milestone'] != None:
            if type(wconf['milestone']) == list:
                milestone = '&'.join([str(d[k]) for k in wconf['milestone']])
            elif callable(wconf['milestone']):
                milestone = wconf['milestone'](d)

        winf = {
            'work': w,
            'name': wname,
            'milestone': milestone,
            'args': d,
            'time_create': nowt,
            'time_start': None,
            'time_end': None,
            'time_used': None,
            'node_accepted': None,
            'error': None,
        }

        return wname, winf

    def check_work(self, new, old):

        wconf = self.workconfig[new['work']]

        # print('----new',new,type(new['time_create']))
        # print('----old:',json.loads(old),type(old))
        # print('-----wconf:',wconf['min-interval'],type(wconf['min-interval']))

        if old == None:
            return True

        if wconf.get('min-interval', None) and (new['time_create'] - old['time_create']) < wconf['min-interval']:
            return False

        if new['milestone'] != old['milestone']:
            return True

        if old['time_end']:
            return False

        last_time = old['time_start'] if old['time_start'] else old['time_create']

        if wconf.get('timeout') and (new['time_create'] - last_time) > wconf['timeout']:
            return True

        return False

    def put_work(self, works):

        nowt = int(time.time())

        winfs = [
            self.make_work_info(w, d, nowt)
            for w, d in works
        ]

        if winfs:

            wnames = list(zip(*winfs))[0]

            master_redis = self.get_master_redis()

            currentworkstt = master_redis.hmget(self.work_key, wnames)

            winfs = {
                w: json.dumps(d, ensure_ascii=False)
                for (w, d), s in zip(winfs, currentworkstt)
                if self.check_work(d, json.loads(s) if s else None)
            }

            if winfs:
                master_redis.hmset(self.work_key, winfs)
                master_redis.sadd(self.work_pool, *list(winfs.keys()))

        return

    def get_work(self):

        master_redis = self.get_master_redis()

        wname = master_redis.spop(self.work_pool)

        if wname is None:
            return

        w = master_redis.hget(self.work_key, wname)

        if w is None:
            return

        return json.loads(w)

    def master_is_me(self):

        try:
            rs = self.get_one_redis()
        except redis.ConnectionError as e:
            print(e)
            return

        masterinfo = rs.get(self.masterkey)

        if not masterinfo:
            return False

        masterinfo = json.loads(masterinfo)

        return bool(masterinfo['server-id'] == self.myself.get('server-id'))

    def unitask_master_is_me(self):

        try:
            rs = self.get_one_redis()
        except redis.ConnectionError as e:
            print(e)
            return

        masterinfo = rs.get(self.work_masterkey)

        if not masterinfo:
            return False

        masterinfo = json.loads(masterinfo)

        return bool(masterinfo['server-id'] == self.myself.get('server-id'))

    def routine(self, sig=None):
        print("+++++++++++++++++:routine")

        if not self.unitask_master_is_me():
            return

        nowt = int(time.time())

        for wname, wconf in self.workconfig.items():
            if 'routine' not in wconf:
                continue
            self.put_work([(wname, {'routine': int(nowt / wconf['routine']) * wconf['routine']})])

        return

    def do_work(self, sig=None):
        print("+++++++++++++++++:do work")

        if self.update_master_conf() == False:
            return

        w = self.get_work()

        if w is None:
            return

        st = time.time()
        w['time_start'] = int(st)
        w['node_accepted'] = self.myself['node']

        ee = None

        if self.unitask_mode == 'master':
            try:
                self.redis = self.get_one_redis()
            except redis.ConnectionError as e:
                print(e)
                return
        else:
            self.redis = self.get_master_redis()

        try:
            self.redis.hset(self.work_key, w['name'], json.dumps(w))
            getattr(self, 'work__' + w['work'])(**w['args'])
        except Exception as e:
            traceback.print_exc()
            et, ev, tb = sys.exc_info()
            f, lineno = traceback.walk_tb(tb).__next__()
            e = f.f_code.co_filename, str(lineno), et.__name__, str(ev)
            ee = str(e)

        ed = time.time()
        w['time_end'] = int(ed)
        w['time_used'] = max(ed - st, 0.001)
        w['error'] = ee

        try:
            self.redis.hset(self.work_key, w['name'], json.dumps(w))
        except Exception as e:
            print(e)

        return

    def regist_signal(self):
        print("================:regist_signal---:",self.unitask_mode)
        if self.unitask_mode == 'master':
            print("================:regist_signal 1---:")
            uwsgi.register_signal(1, "", self.system_heartbeat)
            uwsgi.add_timer(1, 60)

        uwsgi.register_signal(2, "", self.heartbeat)
        uwsgi.add_timer(2, 60)

        uwsgi.register_signal(3, "", self.do_work)
        uwsgi.add_timer(3, 3)

        uwsgi.register_signal(4, "", self.routine)
        uwsgi.add_timer(4, 30)

        return
