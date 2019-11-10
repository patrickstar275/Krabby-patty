import requests

api_key = '4e5524a31627df47165d4b52f23578b7'


def translate(q, l_from, l_to):
    data = {
        'from': l_from,
        'to': l_to,
        'src_text': q,
        'apikey': api_key,
    }
    r = requests.get('http://api.niutrans.vip/NiuTransServer/translation', params=data)
    return r.json()['tgt_text'].strip()


def translate_en2ch(q):
    return translate(q, 'en', 'zh')


def translate_ch2en(q):
    return translate(q, 'zh', 'en')


if __name__ == '__main__':
    print(translate_en2ch('hello'))
