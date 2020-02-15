import time
import argparse
import requests

from json import *
from googletrans import Translator

from progressbar import *


# proxyApi = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&pack=62869&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
# proxy = requests.get(proxyApi).json()
# print(proxy)
# proxy = proxy['data'][0]
# ip = proxy['ip']
# port = proxy['port']

# print("使用ip   " + "http://%s:%s" % (ip, port))

translator = Translator(service_urls=[
    'translate.google.cn'
])

parser = argparse.ArgumentParser(description='脚本手册')
parser.add_argument("-F", "--file", help="要翻译的文件路径", required='true')
parser.add_argument("-SL", "--src", help="来源语言", default="auto")
parser.add_argument("-TL", "--dest", nargs="+", help="目标语言", required='true')
parser.add_argument("-S", "--out",  help="输出文件路径", required='true')
# SL 来源语言 TL 目标语言  S 目标文件

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

args = parser.parse_args()

file = args.file
src = args.src
dest = args.dest
out = args.out

lines = []


f = open(file, 'r')
print('开始读取文件.....')
count = 0
for i in f.readlines():
    count += 1
    if count == 3:
        lines.append(i.strip())
    if count == 4:
        count = 0
f.close()
print('开始翻译.....')

for lan in dest:
    try:
        res = []
        translations = translator.translate(lines, dest=lan, src=src)
        print('翻译' + lan + '完成')
        outfile = open('./' + out + '-' + lan + '.srt', 'wb+')
        count = 0
        j = 0
        f = open(file, 'r')
        for i in f.readlines():
            count += 1
            if count == 3:
                outfile.write(translations[j].text.encode('utf-8'))
                j += 1
            else:
                outfile.write((i.strip() + "\n").encode('utf-8'))
            if count == 4:
                count = 0
        outfile.close()
        for second in range(100, 0):
            print('上一轮翻译完成,进入等待时间,剩余%s秒' % second, end="\r")
            time.sleep(1)
        f.close()

    except JSONDecodeError as e:
        print('封IP了')
