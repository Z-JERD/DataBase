import json
import time
import os
import datetime
import uuid

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import ewsgi
import edb
import tools
import unitask
import hxsto
import traceback


class Server(unitask.UniTask):
    """幻灯片数据操作
    uwsgi 配置文件：master 和 srv_name 必须配置
        slide:
          master: master
          srv_name: slide
          wsgi-file: srv_slide.py
          socket: /var/wsgi/slide.socket
          pidfile:  /var/wsgi/slide.pid
          daemonize:  /var/wsgi/slide.log

    查看redis中的数据
        import redis
        res = redis.Redis(host='10.110.1.99', port=9221, decode_responses=True)
        res.hgetall('_slide_work')
        res.delete('_slide_work')
        res.hget('_slide_work','generate_images:(123, 1)')


    redis 中的数据：
            {
            'bind_slide_has_picture':
                    '{  "work": "bind_slide_has_picture",
                        "name": "bind_slide_has_picture",
                        "milestone": "2019-05-25 00:0",
                        "args": {"routine": 1558713600},
                        "time_create": 1558713610, "time_start": 1558713613, "time_end": 1558713613,
                        "time_used": 0.009007930755615234, "node_accepted": "dev99", "error": null
                        }',

            "generate_images:(123, 1, '2019-05-16 10:39:25')":
                        '{  "work": "generate_images",
                            "name": "generate_images:(123, 1, \'2019-05-16 10:39:25\')",
                            "milestone": "2019-05-16 10:39:25",
                            "args": {"slide_id_uid_time": [123, 1, "2019-05-16 10:39:25"], "execution_time": "2019-05-16 10:39:25"},
                            "time_create": 1557974365, "time_start": 1557974365, "time_end": 1557974374, "time_used": 9.519343614578247,
                            "node_accepted": "dev99", "error": null}',

        }

    res.get('_unitask_demo_master')：查看heartbeat的redis信息
    '{"node": "dev99", "server-id": 99, "intranet": "10.110.1.99", "inner_api_address": ["10.110.1.99], "unitask_ip": "10.110.1.99", "unitask_port": 9221, "heartbeat": 1561014570}'


    """

    def __init__(self):
        super().__init__()

        self.db = edb.Database('arch2018')
        self.get_slide_url = "http://127.0.0.1:12018/intra/generate_img/#/main"
        self.chrome_path = "/usr/bin/chromedriver"
        self.screen_path = "/tmp/slider_screenshot/"

        self.catalog = 'slider'
        self.upload_file_url = 'http://127.0.0.1:12018/inner/ucs/upload'

        self.workconfig = {
            'bind_slide_has_picture': {'routine': 2 * 60, 'min-interval': 60, 'keys': None,
                                       'milestone': lambda x: datetime.datetime.fromtimestamp(x['routine']).strftime(
                                           '%Y-%m-%d %H:%M')[0:-1]},

            'generate_images': {'min-interval': 60, 'keys': ['slide_id_uid_time'], 'milestone': ['execution_time'],
                                'timeout': 120}
        }

    def screenshot(self, id):
        """获取幻灯片内容并生成截图"""
        url = self.get_slide_url + '?id=%s' % id
        if not os.path.exists(self.screen_path):
            os.mkdir(self.screen_path)

        filename = str(uuid.uuid4()).split('-')[0] + '.png'
        filepath = os.path.join(self.screen_path, filename)

        screensize = (800, 900)
        options = Options()

        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")

        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=%s,%s' % screensize)
        options.add_argument('--window-position=0,0')

        driver = webdriver.Chrome(self.chrome_path, chrome_options=options)

        driver.get(url)

        try:
            print('sleep')
            time.sleep(4)
            scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(scroll_width, scroll_height)
            # driver.set_window_size(836, 15000)
            time.sleep(1)
            print('screenshot', scroll_width, scroll_height)
            driver.save_screenshot(filepath)
        except Exception as e:

            traceback.print_exc()

        driver.quit()

        return filepath

    def screenshot_upload(self, filepath, uid):
        """将生成的文件上传得到返回的序列号"""
        try:
            files = {'file': open(filepath, 'rb')}
            payload = {
                "uid": uid,
                "catalog": self.catalog,
            }
            res = requests.request("POST", self.upload_file_url, data=payload, files=files)
        except Exception as e:
            traceback.print_exc()
            print("-----路径为:%s的图片上传失败" % filepath)
            return None
        return res.text

    def work__bind_slide_has_picture(self, routine=None):
        """查询到picture_milestone last_modify不一致的数据"""

        project = self.db.slide_files.where(invalid=0).select()
        images_works = [
             ('generate_images', {
                'slide_id_uid_time': (data['id'], data['user_id'], data['last_modify'].strftime('%Y-%m-%d %X')),
                'execution_time': datetime.datetime.now().strftime('%Y-%m-%d %X')
            }) for data in project if data['picture_milestone'] != data['last_modify']
        ]
        self.put_work(images_works)

        return

    def work__generate_images(self, slide_id_uid_time, execution_time):
        """执行生成图片的功能并修改picture_milestone"""
        slide_id, uid, last_modify_time = slide_id_uid_time
        filepath = self.screenshot(slide_id)
        # filepath = '/home/zhaoguangfei/goods001.jpg'
        if not os.path.exists(filepath):
            raise Exception('----:id为%s的数据生成截图失败' % slide_id)
        print('----:id为%s的数据生成截图成功' % slide_id)

        try:
            response = self.screenshot_upload(filepath, uid)
            os.remove(filepath)
        except:
            pass

        try:
            response = json.loads(response)
            filecode = response['result']['filecode']
        except Exception as e:
            print("-----id为%s的数据获取返回的filecode失败,response为：%s" % (slide_id, response))
            raise

        print("---上传成功,返回的图片编码为：", filecode)
        last_modify_time = datetime.datetime.strptime(last_modify_time, '%Y-%m-%d %X')
        project = self.db.slide_files.where(id=slide_id, invalid=0).update(picture_milestone=last_modify_time,
                                                                           picture_code=filecode)

        return


class SlideProjector(ewsgi.JrWsgiServer):

    def __init__(self):

        super().__init__()
        self.db = edb.Database('arch2018')
        self.serv = Server()

    def put_slide_work(self, id):
        """保存幻灯片数据后，将其加到unitask中"""
        data = self.db.slide_files.where(id=id, invalid=0).unique()
        images_works = [
            ('generate_images', {
                'slide_id_uid_time': (data['id'], data['user_id'], data['last_modify'].strftime('%Y-%m-%d %X')),
                'execution_time': datetime.datetime.now().strftime('%Y-%m-%d %X')
            })
        ]

        self.serv.put_work(images_works)

        return

    def url__slide__add_project(self, info: dict) -> bool:
        """
            新增幻灯片数据
            接收的数据：
                info = {
                        "title": "2019年03月票房统计",        幻灯片名称
                        "year": 2019                         幻灯片填写年份
                        "month":2                           幻灯片填写月份
                        "content": [{...},{...},{...}]      幻灯片内容
                    }
        """
        assert info['content'], '幻灯片内容不能为空'
        uid = self.session.uid
        content = info.pop("content", [])
        info["content"] = json.dumps(content)
        info.update({'user_id': uid})
        res = self.db.slide_files.append(info)

        if res:
            self.put_slide_work(res)
            return True
        else:
            return self.BadRequest([], '新增数据失败')

    def url__slide__get_project(self, id: int = None, title: str = None, page: int = 1, pagesize: int = 20) -> list:
        """获取幻灯片数据"""
        where = [" id > %s and invalid = %s "]
        args = [0, 0]

        if id != None:
            assert id > 0, '幻灯片ID不能为空'
            where[0] = " id = %s and invalid = %s "
            args[0] = id

        if title != None:
            where.append(" and title like %s ")
            args.append('%' + title + '%')

        sql = "select count(*) as row_num from slide_files where %s" % (''.join(where))
        res = self.db(sql, tuple(args))
        total = res[0]["row_num"]
        page_info = tools.pageinfo(page, pagesize, total)
        sql = "select id, title, year, month,content, picture_code, create_time,user_id,picture_milestone, last_modify from slide_files where %s order by last_modify desc,id desc limit %s offset %s " % (
            ''.join(where), page_info["pagesize"], page_info["offset"])
        project = self.db(sql, tuple(args))

        # 获取生成的截图
        for data in project:

            if data['picture_code'] and data['picture_milestone'] == data['last_modify']:
                filecode, uid = data['picture_code'], data['user_id']
                address = hxsto.private(self.serv.catalog, filecode, uid)
                data['has_pictures'] = True
                data['pictures_url'] = address
            else:
                data['has_pictures'] = False
                data['pictures_url'] = None

        return {"pageinfo": page_info, "project": project}

    def url__slide__get_specified_project(self, id: int) -> dict:
        """获取指定id的幻灯片数据"""
        assert id > 0, "幻灯片ID不能为空"
        project = self.db.slide_files.where(id=id, invalid=0).unique()

        return project

    def url__inner__slide__get_specified_project(self, id: int) -> dict:
        """内部获取指定id的幻灯片数据"""
        assert id > 0, "幻灯片ID不能为空"
        project = self.db.slide_files.where(id=id, invalid=0).unique()

        return project

    def url__slide__save_project(self, id: int, info: dict) -> bool:
        """
            保存修改的幻灯片数据
            接受的数据：
                id 当前项目id
                info = {
                        "title": "2019年03月票房统计",        幻灯片名称
                        "year": 2019,                         幻灯片填写年份
                        "month":2,                          幻灯片填写月份
                        "content": [{...},{...},{...}]      幻灯片内容
                    }

        """
        assert id > 0, "幻灯片ID不能为空"
        content = info.get("content", None)
        assert content, '幻灯片内容不能为空'
        dt = datetime.datetime.now().strftime('%Y-%m-%d %X')
        current_time = datetime.datetime.strptime(dt, '%Y-%m-%d %X')
        info.update({'last_modify': current_time})

        content = info.pop("content", [])
        info["content"] = json.dumps(content)
        res = self.db.slide_files.where(id=id, invalid=0).update(**info)

        if res:
            self.put_slide_work(id)

        return True

    def url__slide__remove_project(self, id: int) -> bool:
        """删除幻灯片数据"""
        assert id > 0, '幻灯片ID不能为空'
        res = self.db.slide_files.where(id=id, invalid=0).unique()
        assert res, '数据不存在'
        self.db.slide_files.where(id=id, invalid=0).update(invalid=1)
        return True

    def url__slide__get_pictures_addr(self, ids: list) -> list:
        """获取指定数据的图片下载地址
            ids = [1,2,3,4,5 .....]
        """
        projects = self.db.slide_files.where(invalid=0).where_in(id=ids).select()
        response = []
        for data in projects:
            base_info = {'id': data['id']}

            if data['picture_code'] and data['picture_milestone'] == data['last_modify']:
                filecode, uid = data['picture_code'], data['user_id']
                address = hxsto.private(self.serv.catalog, filecode, uid)
                base_info['has_pictures'] = True
                base_info['pictures_url'] = address
            else:
                base_info['has_pictures'] = False
                base_info['pictures_url'] = None

            response.append(base_info)

        return response

    # def url__slide__download_pictures(self, id:int) -> dict:
    #     """
    #     下载对应数据的图片
    #         返回数据：
    #              {
    #                 'has_pictures':False,
    #                 'pictures_url':None
    #             }
    #     """
    #     data = self.db.slide_files.where(id=id, invalid=0).unique()
    #     if  data['picture_code'] and data['picture_milestone'] != data['last_modify']:
    #         return {
    #                 'has_pictures':False,
    #                 'pictures_url':None
    #             }
    #     filecode, uid = data['picture_code'], data['user_id']
    #     address = hxsto.private(self.serv.catalog, filecode, uid)
    #     return {
    #                 'has_pictures':True,
    #                 'pictures_url':address
    #             }


if __name__.startswith('uwsgi_file_'):
    application = SlideProjector()
    # 监控生成截图
    application.serv.regist_signal()



