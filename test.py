import requests
import json

HOST = 'http://127.0.0.1:8080'

def api(uri):
    return HOST + uri

def play(url):
    data = {
            'url':url,# require
            'files': [], # require
            'start':0, # 0 为立即播放
            'format': 'nomal', # nomal, super
            'fullscreen': True,
            'volume': 90
            } # files/url, 必须有一个，url > files
    r = requests.post(api('/play'), data={'json':json.dumps(data)})
    print(r.json)

def fullscreen():
    r = requests.get(api('/fullscreen'))
    print(r.json)

    r = requests.post(api('/fullscreen'))
    print(r.json)

def volume(volume):
    r = reqiests.get(api('/volume'))
    print(r.json)

    r = requests.post(api('/volume'), data={'value': volume})
    print(r.json)

def pause():
    r = requests.get(api('/paused'))
    print(r.json)

    r = requests.post(api('/pause'))
    print(r.json)

def quit():
    r = requests.post(api('/quit'))
    print(r.json)

def main(script, function, source=None):
    if function == 'play':
        play(source)
    elif function == 'fullscreen':
        fullscreen()
    elif function == 'volume':
        volume(source)
    elif function == 'quit':
        quit()
    elif function == 'pause':
        pause()
    else:
        if source is None:
            source = function 
        play(source)

if __name__ == '__main__':
    import sys
    main(*sys.argv)
