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

播放视频:
    import requests
    import json
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

退出：
    r = requests.post(api('/quit'))
    print(r.json)
