# coding:utf-8
import requests
import json
from models.Model import House
from models.Model import db

url = "https://woyaozufang.live/v2/houses"

payload = {"city": "深圳", "fromPrice": "1000", "source": "", "keyword": "宝安,西乡,坪洲"}
# payload = '{"city":"%s","fromPrice":"1000","source":"","keyword":"%s"}'%("深圳","桂庙,地铁站")

headers = {
    'accept': "application/json, text/plain, */*",
    'origin': "https://house-map.cn",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/72.0.3626.96 Safari/537.36",
    'dnt': "1",
    'content-type': "application/json;charset=UTF-8",
    'cache-control': "no-cache",
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

print(response.text)

count = 0
houses = response.json().get('data')
print(len(houses))

for house in houses:
    house = House(title=house.get('title'), pubTime=house.get('pubTime'),displaySource=house.get('displaySource'))
    try:
        db.session.add(house)
        db.session.commit()

    except Exception as e:
        print(e)
        pass
    # count += 1
    # if count % 100 == 0:
    #     db.session.flush()
