from urllib.parse import quote

import requests


def translate(q, l_from, l_to):
    data = {
        'lang': l_from + '_' + l_to,
        'src': q,
    }
    r = requests.get('https://nmt.xmu.edu.cn/nmt', params=data)
    return r.text.encode('raw_unicode_escape').decode().strip()


def translate_en2ch(q):
    return translate(q, 'en', 'zh-cn')


def translate_ch2en(q):
    return translate(q, 'zh-cn', 'en')


if __name__ == '__main__':
    src = '苹果'
    print(translate_ch2en(src))
