mplayer-control-server
======================

A control-server for mplayer. You can control mplayer from the web

服务端：

    virtualenv -p python3 venv
    . venv/bin/activate
    easy_install bottle
    easy_install beautifulsoup4
    easy_install requests
    easy_install mplayer.py
    python app.py

Python 客户端
=============

播放视频:

    import requests
    import json
    
    def api(uri):
        return 'http://127.0.0.1:8080' + uri
    
    data = {
            'url':'http://v.youku.com/v_show/id_XNDU3NjM0NzMy.html',# require
            'files', [], # require
            'start':0, # 0 为立即播放
            'format': 'nomal', # nomal, super
            'fullscreen': True,
            'volume': 90
            } # files/url, 必须有一个，url > files
    r = requests.post(api('/play'), data={'json':json.dumps(data)})
    print(r.json)

查看是否全屏：

    r = requests.get(api('/fullscreen'))
    print(r.json)

改变全屏状态：

    r = requests.post(api('/fullscreen'))
    print(r.json)

查看音量:

    r = requests.get(api('/volume'))
    print(r.json)

修改音量：

    r = requests.post(api('/volume'), data={'value':50})
    print(r.json)

查看是否暂停：

    r = requests.get(api('/paused'))
    print(r.json)

修改暂停状态：

    r = requests.post(api('/pause'))
    print(r.json)

定位：

    r = requests.post(api('/seek'), data={
                'value':20,
                'type':0 # 可选,0 是一个相对定位+/- <value>（默认值）。
                         #      1 是定位<value>％在电影里。
                         #      2 是寻求一个绝对位置的<value>秒。
            })
    print(r.json)

下一个/上一个视频：
    
    r = requests.post(api('/pt_step'), data={
                'value':1 # 1 为下一个，-1 上一个
                'force':0 # 可选 默认为 0
            })
    print(r.json)

静音：

    r = requests.post(api('/mute'))
    print(r.json)

查看状态：

    r = requests.get(api('/status'))
    print(r.json)

退出：

    r = requests.post(api('/quit'))
    print(r.json)
