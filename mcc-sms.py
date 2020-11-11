import grequests  # 实际上就是requests + gevent
import requests
import bs4
import time


sms_send_url = 'https://mcc.xunliandata.com/mc/sms-send'

sms_send_param = {
    "merchant_code": "mastercard",
    "mobile": "18928495412"
}

def sms_send():
    sms_seesion = requests.Session()
    sms_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        "Connection":"keep-alive",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests":"1",
        "Cache-Control":"max-age=0",
    }

    res = sms_seesion.post(sms_send_url, json=sms_send_param, headers=sms_header)

    if res.status_code != requests.codes.OK:
        print(res.text)
        print(res.cookies)

    print(res.text)

def err_handler(request, exception):
    print("请求出错")

if __name__ == '__main__':
    sms_send()