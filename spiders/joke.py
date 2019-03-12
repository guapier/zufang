import random

import requests


def get_joke():
    while True:
        try:
            url = "http://www.mxnzp.com/api/jokes/list"

            querystring = {"page": str(random.randint(1, 900))}

            headers = {
                'connection': "keep-alive",
                'pragma': "no-cache",
                'cache-control': "no-cache",
                'upgrade-insecure-requests': "1",
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                'dnt': "1",
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'accept-encoding': "gzip, deflate",
                'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)
            return response
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    get_joke()