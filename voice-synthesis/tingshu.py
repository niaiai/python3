# -*- coding: UTF-8 -*-
import requests


def Token():
    """提供API Key及 Secret Key 获取access token"""
    url = 'https://openapi.baidu.com/oauth/2.0/token'
    API = 'lxy99hZINwWTyOmPeokAhSqD'
    Secret = '6cj069otTDLywW5YdULA4COk6UvEONxz'
    data = {'grant_type': 'client_credentials', 'client_id': API, 'client_secret': Secret}
    r = requests.post(url, data=data)
    res = r.json()
    return res['access_token']


def txt2mp3(path, text, spd=5, pit=5, vol=5, per=0):
    """传入输出文件路径, 转换的文本, 及默认值
    spd 语速, pit 音调, vol 音量 取值0-9, 默认为5,
    per 0为女声, 1为男声, 默认为女声"""
    toke = Token()
    url = 'http://tsn.baidu.com/text2audio'
    f = open(path, 'wb')
    num = 500
    times = 1
    for i in range(int(len(text)/num)+1):
        txt = text[num * i:num * i + num]
        data = {'tex': txt, 'ctp': 1, 'lan': 'zh', 'cuid': '123456', 'tok': toke, 'spd': spd, 'pit': pit, 'vol': vol, 'per': per }
        r = requests.get(url, params=data)
        if len(r.content) < 43:
            print('合成错误')
            continue
        else:
            print('正在写入第%s 段语音' % times)
            f.write(r.content)
        times += 1
    f.close()

text = ''
path = '青蛙.mp3'
temp = "%s只青蛙%s张嘴%s个眼睛%s条腿"
for i in range(1, 10):
    h = temp % (i, i, 2*i, 4*i)
    text += h

txt2mp3(path, text, spd=9)
