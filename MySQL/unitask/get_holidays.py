import calendar
import datetime
import json
import urllib.parse
from pyquery import PyQuery as PQ

import grab

class BaiduCalendar(object):
    def __init__(self):
        for i in range(3):
            try:
                self.make_g()
                break
            except TimeoutError as e:
                pass
        # else:
        #     raise
        return

    def make_g(self):
        h = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "http://www.baidu.com",
            "Connection": "Keep-Alive",
        }

        g = grab.Grab(h)
        self.g = g

        return

    def get_month_calendar(self, year, month):
        url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?'
        d = {
            'query': '%s年%s月' % (year, month),
            'resource_id': 6018,
            'ie': 'utf8',
            'oe': 'gbk',
            'format': 'json',
            'tn': 'baidu'
        }
        url += urllib.parse.urlencode(d)
        print(url)
        r = self.g.get(url).read().decode('gbk')

        info = json.loads(r)
        # print(json.dumps(info, indent=4))

        ret = dict()
        holidays = info['data'][0].get('holiday', None)

        if holidays:
            if type(holidays) == list:
                for holiday in holidays:
                    # print('holiday:', holiday)
                    for day in holiday.get('list', list()):
                        ret['%04d%02d%02d' % tuple([int(d) for d in day['date'].split('-')])] = \
                            {
                                'rest': 1 if day['status'] == '1' else 0,
                                'name': [holiday['name']] if day['status'] == '1' else None,
                                'weekday': None,
                            }

            elif type(holidays) == dict:
                for day in holidays.get('list', list()):
                    ret['%04d%02d%02d' % tuple([int(d) for d in day['date'].split('-')])] = \
                        {
                            'rest': 1 if day['status'] == '1' else 0,
                            'name': [holidays['name']] if day['status'] == '1' else None,
                            'weekday': None,
                        }


        # print(ret)
        return ret



# http://wannianrili.51240.com/
class Wannianrili(object):
    FILTER_LIST = [
        '护士节',
        '植树节',
    ]

    def __init__(self):
        for i in range(3):
            try:
                self.make_g()
                break
            except TimeoutError as e:
                pass
        # else:
        #     raise
        return

    def make_g(self):
        h = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "http://wannianrili.51240.com/",
            "Connection": "Keep-Alive",
        }

        g = grab.Grab(h)
        self.g = g

        return

    def get_month_calendar(self, year, month):
        url = 'http://wannianrili.51240.com/ajax/?q=%s-%02d' % (year, month)
        print(url)
        r = self.g.get(url).read().decode('utf8')
        dom = PQ(r)

        html_divs = dom('div.wnrl_riqi')
        # print(len(html_divs))

        ret = dict()
        for div in html_divs:
            speical_day = PQ(div)('span.wnrl_td_bzl.wnrl_td_bzl_hong')
            if speical_day:
                name = PQ(speical_day).text()

                if name.endswith('日') or name in Wannianrili.FILTER_LIST:
                    continue

                # print(name)
                # if name in self.Holiday_list:
                ret['%04d%02d%02d' % (year, month, int(PQ(div)('span.wnrl_td_gl').text()))] = name

        # print(ret)
        return ret


class HolidayFetcher(object):
    def __init__(self):
        # self.db = dbconn.Database('etl')
        self.bc =  BaiduCalendar()
        self.wnrl = Wannianrili()

    def get_holidays(self, start_year, end_year):

        holidays = {}

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                bc_month_info = self.bc.get_month_calendar(year, month)
                wnrl_month_info = self.wnrl.get_month_calendar(year, month)

                print(bc_month_info)
                print(wnrl_month_info)

                xx, month_day_cnt = calendar.monthrange(year, month)

                for day in range(1, month_day_cnt + 1):
                    day_str = '%2d%02d%02d' % (year, month, day)
                    day_info = bc_month_info.get(day_str, {
                        'rest': None,
                        'name': None,
                        'weekday': None,
                    })

                    wnrl_name = wnrl_month_info.get(day_str, None)
                    if wnrl_name:
                        ori_name = day_info['name']
                        if ori_name and wnrl_name not in ori_name:
                            # print(day_info['name'])
                            day_info['name'].append(wnrl_name)
                            # print(day_info['name'])
                        else:
                            day_info['name'] = [wnrl_name]

                    day_info['week_ordinal'] = datetime.datetime(year, month, day).isocalendar()[1]

                    weekday = calendar.weekday(year, month, day)
                    day_info['weekday'] = weekday + 1

                    if day_info['rest'] is None:
                        if weekday in (5, 6):
                            day_info['rest'] = 1
                        else:
                            day_info['rest'] = 0

                    if day_info['name']:
                        day_info['name'] = '/'.join(day_info['name'])

                    if day_info['rest']:
                        # print(day_str)
                        # print(day_info)
                        holidays[day_str]=int(day_str)

        return holidays

                    # self.db('insert into calendar values(null, %s, %s, %s, %s, %s, %s, %s, %s) '
                    #         'ON DUPLICATE KEY UPDATE year=%s, month=%s, day=%s, week_ordinal=%s, weekday=%s, '
                    #         'name=%s, rest=%s',
                    #         (day_str, year, month, day,
                    #          day_info['week_ordinal'], day_info['weekday'], day_info['name'], day_info['rest'],
                    #          year, month, day,
                    #          day_info['week_ordinal'], day_info['weekday'], day_info['name'], day_info['rest'],))

            #     break
            # break



if __name__ == '__main__' :
    # BaiduCalendar().get_month_calendar(2011, 10)
    # Wannianrili().get_month_calendar(2016, 2)

    fetcher = HolidayFetcher()
    fetcher.get_holidays(2019, 2019)
