import grequests  # 实际上就是requests + gevent
import requests
import bs4
import time

url = 'https://mcc.xunliandata.com/mc/user/zhen-rights'

def run_requset():
    tasks = [grequests.post(url) for u in range(100)]
    t1 = time.time()
    # ##### 执行并获取响应列表 #####
    res = grequests.map(tasks, exception_handler=err_handler)

    [print(res[0].text) for u in range(100)]
    t2 = time.time()
    print('run_requset', t2 - t1)

def err_handler(request, exception):
    print("请求出错")

if __name__ == '__main__':
    run_requset()