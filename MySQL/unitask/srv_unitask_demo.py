import datetime
import ewsgi
import unitask_sim

class Server(unitask_sim.UniTask):

    def __init__(self):
        super().__init__()
        self.workconfig = {
            'business_calendar': {'routine': 2 * 60, 'min-interval': 60, 'keys': None,
                                  'milestone': lambda x: datetime.datetime.fromtimestamp(x['routine']).strftime(
                                      '%Y-%m')},
            'push_holiday_to_check': {'routine': 10, 'min-interval': 10, 'keys': None, 'milestone': ['routine']},

        }

    def work__business_calendar(self, routine=None):
        """
        缓存节假日信息
        :return:
        """
        print("==================:","缓存节假日信息")
        return

    def work__push_holiday_to_check(self, routine=None):
        """
        推送假期到审批系统
        :return:
        """
        print("==================:", "推送假期到审批系统")
        return


class UnitaskDemo(ewsgi.JrWsgiServer):
    def __init__(self):
        super().__init__()
        self.serv = Server()

    def url__unitask_demo__get(self) -> str:
        return "unitask demo "



if __name__.startswith('uwsgi_file_'):
    application = UnitaskDemo()
    # 监控生成截图
    application.serv.regist_signal()