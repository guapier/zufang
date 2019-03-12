import random
from models.Model import HouseSource, db
import requests
import re
import time


def get_city_and_group(city, page):
    url = "https://www.douban.com/group/search"

    # querystring = {"start": "0", "cat": "1013", "group": "106955", "sort": "time", "q": "深圳租房"}
    querystring = {"start": page, "cat": "1013", "sort": "time", "q": city + "租房"}

    headers = {
        'connection': "keep-alive",
        'pragma': "no-cache",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'dnt': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'referer': "https://www.douban.com/group/search?cat=1013&group=106955&sort=time&q={}".format((city+'租房').encode('utf-8')),
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': "bid=XAVSr6iGi8s; ll=\"118282\"; _pk_ses.100001.8cb4=*; __utma=30149280.1684344548.1550591704.1550591704.1550591704.1; __utmc=30149280; __utmz=30149280.1550591704.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; ap_v=0,6.0; __yadk_uid=mvKQGomVlfkTA9ZpKBPeGpaOa57uwZEe; douban-fav-remind=1; _pk_id.100001.8cb4=f572c715bc327f5a.1550591704.1.1550592136.1550591704.; __utmb=30149280.109.6.1550592136361",
    }

    response = requests.request("GET", url, headers=headers, params=querystring, verify=False)

    # print(response.text)

    groups = re.findall(r'<td><a href="https://www.douban.com/group/(.*?)/" class="">', response.text)
    names = re.findall(r'class="">(.*?)</a>', response.text)
    result = dict(zip(names, groups))
    for k in list(result.keys()):
        if city in k and '租房' in k:
            try:
                print(k, result.get(k))
                house_source = HouseSource(name=k, group=result.get(k), source='douban', city=city)
                db.session.add(house_source)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        else:
            pass
    return result


pages = [i * 50 for i in range(0, 4)]
cities = ['深圳', '上海', '北京', '广州', '杭州', '成都', '武汉', '南京', '重庆', '天津', '苏州', '西安', '郑州', '厦门', '合肥']
data_list = []
data_dict = {}

for city in cities:
    for page in pages:
        print(city,page)
        get_city_and_group(city, str(page))
        time.sleep(random.uniform(3.0, 5.0))
