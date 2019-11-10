import hashlib
import time
import uuid

import requests

YOUDAO_URL = 'https://openapi.youdao.com/api'

app_id = '5b4b7ac40359fff9'
app_key = 'EfDJHNLmJ0x0Z0VpGx7ApPUvUb1TTkkX'


def translate(q, l_from, l_to):
    return translate_raw(q, l_from, l_to)['translation'][0]


def translate_auto(q):
    return translate(q, 'auto', 'auto')


def translate_ch2en(q):
    return translate(q, 'zh_CHS', 'en')


def translate_en2ch(q):
    return translate(q, 'en', 'zh_CHS')


def translate_raw(q, l_from, l_to):
    data = gen_data(q, l_from, l_to)
    return do_request(data)


def gen_data(q, l_from, l_to):
    data = {}

    sign_type = 'v3'
    salt = gen_salt()
    curtime = str(int(time.time()))
    # 生成签名
    input_str = q if len(q) <= 20 else q[0:10] + q[-10:]
    sign_str = app_id + input_str + salt + curtime + app_key
    sign = gen_sign(sign_str)

    data['q'] = q
    data['from'] = l_from
    data['to'] = l_to
    data['appKey'] = app_id
    data['salt'] = salt
    data['sign'] = sign
    data['signType'] = sign_type
    data['curtime'] = curtime

    return data


def gen_salt():
    return str(uuid.uuid1())


def gen_sign(sign_str):
    h = hashlib.sha256()
    h.update(sign_str.encode('utf-8'))
    return h.hexdigest()


def do_request(data):
    r = requests.get(YOUDAO_URL, data)
    return r.json()


if __name__ == '__main__':
    print(translate_auto("bad"))
