import requests
import json

HOST = 'http://127.0.0.1:8080'

def api(uri):
    return HOST + uri

def play():
    data = {
            'url':'',# require
            'files', [], # require
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

def volume():
    r = reqiests.get(api('/volume'))
    print(r.json)

    r = requests.post(api('/volume'), data={'value': 50})
    print(r.json)

def quit():
    r = requests.post(api('/quit'))
    print(r.json)

def main(script, function):
    if function == 'play':
        play()
    elif function == 'fullscreen':
        fullscreen()
    elif function == 'volume':
        volume()
    elif function == 'quit':
        quit()
    else:
        play()

if __name__ == '__main__':
    import sys
    main(*sys.argv)
