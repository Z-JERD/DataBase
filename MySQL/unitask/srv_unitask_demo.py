import datetime
import ewsgi
import unitask_sim

class Server(unitask_sim.UniTask):
    """
        {
        'business_calendar':
                '{
                    "work": "business_calendar",
                     "name": "business_calendar",
                     "milestone": "2019-07",
                     "args": {"routine": 1563334200},
                     "time_create": 1563334225, "time_start": 1563334228, "time_end": 1563334228, "time_used": 0.001,
                     "node_accepted": "dev99", "error": null
                 }',
        'push_holiday_to_check':
                    '{
                        "work": "push_holiday_to_check",
                         "name": "push_holiday_to_check",
                         "milestone": "1563334250",
                         "args": {"routine": 1563334250},
                          "time_create": 1563334255, "time_start": 1563334258, "time_end": 1563334258, "time_used": 0.001,
                          "node_accepted": "dev99", "error": null
                  }'
}

    """

    def __init__(self):
        super().__init__()
        self.workconfig = {
            'business_calendar': {'routine': 2 * 60, 'min-interval': 60, 'keys': None,
                                  'milestone': lambda x: datetime.datetime.fromtimestamp(x['routine']).strftime(
                                      '%Y-%m')},
            'push_holiday_to_check': {'routine': 10, 'min-interval': 10, 'keys': None, 'milestone': ['routine']},  #在注册routine的时候每30s注册一次 因此每30s推送一次

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