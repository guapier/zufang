import requests
import time
import urllib
from datetime import datetime
from urllib import request
import json

'''
发送开发者服务微信
data里面的值，看需求决定参数
user_id 微信推送id
info_url 点击微信需要跳转的地址
'''
'''
当需要传输的数据是json格式的时候使用
'''


def post_json(url, value):
    try:
        new_value = json.dumps(value).encode(encoding='utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
        req = requests.post(url=url, data=new_value, headers=headers)
        print(req.text)

    except Exception as e:
        raise e  # 抛出这个异常


def send_dev_wx(user_id, info_url, subject, send_time, task):
    url = "http://wxmsg.dingliqc.com/send"
    values = {
        "userIds": [user_id],
        "template_id": "4YscLc2uaCnsdrEdUJ9HGAGAkdBcEQM9bUBy0gs69Hw",
        "url": info_url,
        "data": {
            "first": {
                "value": "【" + subject + "】",
                "color": "#d0021b"
            },
            "keyword1": {
                "value": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                "color": "#173177"
            },
            "keyword2": {
                "value": "来自：这里有房  ******",
                "color": "#173177"
            },
            "remark": {
                "value": "房源地址：" + task,
                "color": "#173177"
            }
        }
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               "Content-Type": "application/json"}
    response = post_json(url, values)
    # print(response)


if __name__ == '__main__':
    user_id = ""
    info_url = "http://www.baidu.com"
    subject = "这里有房招到合适的房源，请及时查看"
    send_time = ''
    task = '深圳-西乡-宝体-坪洲'
    send_dev_wx(user_id, info_url, subject, send_time, task)
