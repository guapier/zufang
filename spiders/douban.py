import random
import requests
import re
import time
import datetime

from dateutil import rrule

from models.Model import db, House
from dateutil.parser import parse
from utils.LogHandler import log

# from proxy import proxy_list

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class Douban:
    """
    豆瓣租房小组爬虫
    """

    def __init__(self):
        self.headers = {
            'Connection': "keep-alive",
            'Pragma': "no-cache",
            'Cache-Control': "no-cache",
            'Upgrade-Insecure-Requests': "1",
            'DNT': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "https://www.douban.com/group/search?start=150&cat=1013&sort=time&q=%E8%A5%BF%E4%B9%A1",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Cookie': 'bid=_lbmlOE7lG0; douban-fav-remind=1; viewed="10590856"; gr_user_id=0c36eb26-68d4-4be7-8fa0-2965cdb3c2c0; _vwo_uuid_v2=D025F31E7327CFD1C7C244E460AEB005B|b5bc2f26a59ec8754a258ec2e71b1649; ll="118282"; __utmc=30149280; dbcl2="85113769:l0nXY9xEXqs"; ck=62Yg; push_noty_num=0; push_doumail_num=0; __utmz=30149280.1552382957.7.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmv=30149280.8511; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1552384987%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fwww.douban.com%252Fgroup%252Fsearch%253Fstart%253D50%2526cat%253D1013%2526sort%253Dtime%2526q%253D%2525E8%2525A5%2525BF%2525E4%2525B9%2525A1%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.598908853.1535592198.1552382957.1552384988.8; __utmt=1; _pk_id.100001.8cb4=7ef906054d56f6a3.1535592197.7.1552384996.1552382976.; __utmb=30149280.4.10.1552384988',
            'cache-control': "no-cache",
        }

    def crawl(self, group_id, keyword, city):
        query_words = keyword.split(',')
        print('查询关键词为：{}'.format(keyword))
        for word in query_words:
            while True:
                try:
                    url = "https://www.douban.com/group/search"
                    querystring = {"start": "0", "cat": "1013", "group": group_id, "sort": "time", "q": word}

                    # 可以自行替换代理，也可以不用代理，如果需要长时间稳定运行，最好添加代理
                    # ip = proxy_list[random.randint(0, 510)]
                    # proxies = {'http': '47.99.113.175:8118', 'https': '47.99.113.175:8118'}
                    # print(proxies)
                    # response = requests.get(url, headers=self.headers, params=querystring, proxies=proxies,
                    #                         verify=False)
                    response = requests.get(url, headers=self.headers, params=querystring,
                                            verify=False)
                    if '检测到有异常请求' in response.text:
                        time.sleep(60)
                        log.error('豆瓣检查到有异常请求，请登录你的豆瓣账号后重新再试或者隔一段时间再试')
                    else:
                        titles = re.findall(r'\)" title="(.*?)">', response.text)
                        hrefs = re.findall(r'class="" href="(.*?)" onclick=', response.text)
                        pubTimes = re.findall(r'"td-time" title="(.*?)"', response.text)
                        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        print(titles, hrefs, pubTimes, current_time)
                        for i in range(len(titles)):
                            if rrule.rrule(rrule.DAILY, dtstart=parse(pubTimes[i]),
                                           until=datetime.date.today()).count() < 15:
                                house = House(title=titles[i], onlineURL=hrefs[i], pubTime=pubTimes[i], city=city)
                                log.info('抓取到house信息：{}'.format(house))
                                try:
                                    db.session.add(house)
                                    db.session.commit()
                                except Exception as e:
                                    log.info(e)
                                    db.session.rollback()
                            else:
                                continue
                        time.sleep(random.uniform(5.0, 7.0))
                        break
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    douban = Douban()

    douban.crawl('551176', '西乡,宝体,坪洲', '深圳')
