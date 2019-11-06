import hashlib
import random

import requests

BAIDU_URL_HTTP = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
BAIDU_URL_HTTPS = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

app_id = '20191026000344585'
app_key = 'xMgpa9AarVMxgFbqhO9L'


def translate_auto(q):
    return translate(q, 'auto', 'auto')


def translate_ch2en(q):
    return translate(q, 'zh', 'en')


def translate_en2ch(q):
    return translate(q, 'en', 'zh')


def translate(q, l_from, l_to):
    return translate_raw(q, l_from, l_to)['trans_result'][0]['dst']


def translate_raw(q, l_from, l_to):
    data = gen_data(q, l_from, l_to)
    return do_request(data)


def gen_data(q, l_from, l_to):
    data = {}

    salt = gen_salt()
    # 生成签名
    sign_str = app_id + q + salt + app_key
    sign = gen_sign(sign_str)

    data['q'] = q
    data['from'] = l_from
    data['to'] = l_to
    data['appid'] = app_id
    data['salt'] = salt
    data['sign'] = sign

    return data


def gen_salt():
    return str(random.randint(32768, 65536))


def gen_sign(sign_str):
    h = hashlib.md5()
    h.update(sign_str.encode('utf-8'))
    return h.hexdigest().lower()


def do_request(data):
    r = requests.get(BAIDU_URL_HTTPS, data)
    return r.json()


if __name__ == '__main__':
    print(translate_auto("good"))
