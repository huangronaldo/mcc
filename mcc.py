import grequests  # 实际上就是requests + gevent
import requests
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# SMTP服务
mail_host = "smtp.aliyun.com"
mail_user = "huangronaldo@aliyun.com"
mail_pass = "0803102088huangt"

sender = "huangronaldo@aliyun.com"
receivers = ['huangronaldo@aliyun.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


# 登录
login_url = 'https://mcc.xunliandata.com/mc/login'
# 查询卡
cards_url = 'https://mcc.xunliandata.com/mc/user/cards'
# 选择卡
select_cards_url = 'https://mcc.xunliandata.com/mc/user/select-card'
# 选择臻选权益
zhen_rights_url = 'https://mcc.xunliandata.com/mc/user/zhen-rights'
# 选择权益
select_home_url = 'https://mcc.xunliandata.com/mc/coupon/select-home'

'''
card_list = [
        {
            "bank": "中国光大银行",
            "card_no": "9875",
            "card_type": "world",
            "id": "5ebaaf624b8e0005926aaea3",
            "last_used": 1604652748,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        },
        {
            "bank": "招商银行",
            "card_no": "2243",
            "card_type": "world",
            "id": "5f9987539a8c0aefc0524ee3",
            "last_used": 1604652614,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        },
        {
            "bank": "招商银行",
            "card_no": "4867",
            "card_type": "world",
            "id": "5e8c743c4b8e000592333106",
            "last_used": 1604652230,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        },
        {
            "bank": "招商银行",
            "card_no": "5140",
            "card_type": "world",
            "id": "5f9986e89a8c0aefc0524b4f",
            "last_used": 1604651789,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": ""
        },
        {
            "bank": "招商银行",
            "card_no": "0229",
            "card_type": "world",
            "id": "5f99872a9a8c0aefc0524cf8",
            "last_used": 1604651690,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": ""
        }
    ]
'''
card_list = [
        {
            "bank": "中国光大银行",
            "card_no": "9875",
            "card_type": "world",
            "id": "5ebaaf624b8e0005926aaea3",
            "last_used": 1604652748,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        },
        {
            "bank": "招商银行",
            "card_no": "2243",
            "card_type": "world",
            "id": "5f9987539a8c0aefc0524ee3",
            "last_used": 1604652614,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        },
        {
            "bank": "招商银行",
            "card_no": "4867",
            "card_type": "world",
            "id": "5e8c743c4b8e000592333106",
            "last_used": 1604652230,
            "phone": "18520810812",
            "points": 0,
            "status": "enable",
            "zhen_rights_type": "home"
        }
    ]

count = 1

zhen_rights_param = {"type": "home"}

select_cards_param = {"id": ""}

select_home_param_150 = {"level": "150", "type": "hema"}
select_home_param_250 = {"level": "250", "type": "hema"}
select_home_param_500 = {"level": "500", "type": "zsh"}

login_param = {"phone": "18520810812", "captcha": "161101"}

def mail_send(msg):

    message = MIMEText(msg, 'html', 'utf-8')
    message['From'] = Header("RONALDO.HUANG<huangronaldo@aliyun.com>", 'utf-8')
    message['To'] = Header("罗尼<huangronaldo@aliyun.com>", 'utf-8')

    subject = '万事达权益活动信息'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def zhen_rights(login_header, login_cookies):

    tasks = [grequests.post(zhen_rights_url, json=zhen_rights_param, headers=login_header, cookies=login_cookies) for u in range(count)]
    t1 = time.time()
    # ##### 执行并获取响应列表 #####
    res = grequests.map(tasks, exception_handler=err_handler)
    for u in range(count):
        zhen_res = json.loads(res[u].text)
        if zhen_res["status"] == 1:
            mail_send("臻选权益选择：" + zhen_res["msg"])
        print("臻选权益选择：" + zhen_res["msg"])

def mcc():
    login_seesion = requests.Session()

    login_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }

    login_cookies = {}
    response = login_seesion.post(login_url, json=login_param, headers=login_header)
    # print(response.cookies)
    if response.status_code != requests.codes.OK:
        login_cookies = response.cookies
    else:
        login_cookies = {"_mc": "5fab50996f1a4c36f3e7f3cf"}

    # cards_response = login_seesion.get(cards_url, headers=login_header, cookies=login_cookies)
    # card_list = json.loads(cards_response.text)['cards']
    while True:
        login_status = 0
        # print("所有卡：" + cards)
        for card in card_list:

            print("__________________________________________________________________")

            zhen_rights_type = card['zhen_rights_type']

            select_cards_param['id'] = card_id = card['id']
            select_cards_response = login_seesion.post(select_cards_url, json=select_cards_param, headers=login_header, cookies=login_cookies)

            if zhen_rights_type == '':
                zhen_rights(login_header, login_cookies)
                #login_seesion.post(zhen_rights_url, json=zhen_rights_param, headers=login_header, cookies=login_cookies)

            select_home_500 = login_seesion.post(select_home_url, json=select_home_param_500, headers=login_header, cookies=login_cookies)
            status = json.loads(select_home_500.text)["status"]

            login_status = status
            if status == 37 or status == 3:
                # mail_send("卡尾号：" + card['card_no'] + ", 权益500结果: " + select_home_500.text)
                break
            elif status == 1:
                mail_send("卡尾号：" + card['card_no'] + ", 权益500结果: " + select_home_500.text)

            print("卡尾号：" + card['card_no'] + ", 权益500结果: " + select_home_500.text)
            print("__________________________________________________________________")

        if login_status == 3:
            print("登录失效，请重新登录。账号：" + login_param["phone"])
            mail_send("登录失效，请重新登录。账号：" + login_param["phone"])
            break

        print("------------------------------等待1800秒------------------------------")
        time.sleep(1800)

def err_handler(request, exception):
    print("请求出错")

if __name__ == '__main__':
    mcc()