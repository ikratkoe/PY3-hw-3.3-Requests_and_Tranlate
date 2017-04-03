import requests

key = 'trnsl.1.1.20170402T223937Z.eb3033c001db0d3e.d39689d3983a9a3ac4810c62d526ff29cf7e27bf'


def translate_it(text, cuple_langs):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': key,
        'lang': cuple_langs,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def langs_list():
    params = {
        'key': key
    }
    url = "https://translate.yandex.net/api/v1.5/tr.json/getLangs"
    resp = requests.get(url, params=params).json()['dirs']
    return resp


def detect_lang(text):
    params = {
        'key': key,
        'text': text
    }
    url = "https://translate.yandex.net/api/v1.5/tr.json/detect"
    resp = requests.get(url, params=params).json()['lang']
    print(resp)
    return resp



langs = langs_list()

print("Введите файл для перевода : ")
text_path = input()

print("Введите файл для сохранения перевода : ")
text_out = input()

while True:
    print("Введите язык с которого перевести (по умолчанию автоопределение языка) : ")
    target_lan = input()
    if target_lan == '' :
        target_lan = detect_lang(text_path)
    print("Введите язык, на который перевести (по-умолчанию русский) : ")
    dest_lan = input()
    if dest_lan == '' : dest_lan = 'ru'
    cuple_langs = target_lan + '-' + dest_lan
    if cuple_langs in langs : break
    print("Невозможно сделать перевод с этой пары языков. Введите еще раз.")


with open(text_path) as f:
    trans_text = translate_it(f, cuple_langs)
with open(text_out, 'w') as f:
    f.write(trans_text)

