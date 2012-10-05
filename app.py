from bottle import Bottle, request, response

import mplayer, requests
from bs4 import BeautifulSoup

import os, re

app = Bottle()

player = None 

import json

def parse_video(url, format='nomal'):
    browser = requests.session()
    browser.config['base_headers']['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11'

    r = browser.get('http://www.flvcd.com/parse.php?kw=%s&flag=one&format=%s'%(url, format))

    r.encoding = 'GBK'
    html = BeautifulSoup(r.text)

    mform = html.find('form', {'name':'mform', 'method':'post'})
    if mform:
        name = mform.find('input', {'name':'name'}).get('value')
        info = mform.find('input', {'name':'inf'}).get('value')
        urls = [u for u in re.findall(r'<u>(.+)', info, re.I) if u]
        return urls
    return None

@app.post('/play')
def play():
    global player
    data = request.forms.get('json', None)
    if data is None:
        return {'err':'403', 'msg':'request error'}
    print(data)
    data = json.loads(data)
    files = data.get('files', [])
    url = data.get('url')
    last = data.get('start', 0)
    fullscreen = data.get('fullscreen', False)
    volume = data.get('volume')
    if url:
        format = data.get('format', 'nomal')
        files = parse_video(url, format)
    if files is None or len(files)==0:
        return {'err':'403', 'msg':'request error'}
    if player is None or not player.is_alive():
        player = mplayer.Player()
    if fullscreen:
        player.fullscreen = bool(fullscreen)
    if volume:
        player.volume = float(volume)
    for fn in files:
        player.loadfile(fn, last)
        last += 1 

    return {'last': last}

@app.post('/pause')
def pause():
    if player and player.is_alive():
        player.pause()
        return {'paused':player.paused}
    else:
        return {'err':'403', 'msg':'player is quit'}

@app.get('/paused')
def paused():
    if player and player.is_alive():
        return {'paused':player.paused}
    else:
        return {'err':'403', 'msg':'player is quit'}

@app.post('/quit')
def quit():
    global player
    if player and player.is_alive():
        player.quit()
        player = None
    return {'msg':'quit'}

@app.post('/fullscreen')
def fullscreen(is_set=True):
    if player and player.is_alive():
        if is_set:
            player.fullscreen = not player.fullscreen
        return {'fullscreen':player.fullscreen}
    return {'err':'403', 'msg':'player is quit'}

@app.get('/fullscreen')
def _fullscreen():
    return fullscreen(False)

@app.post('/volume')
def volume(is_set=True):
    if player and player.is_alive():
        if is_set:
            volume = request.forms.get('value', 100.0)
            player.volume = float(volume)
        return {'volume':player.volume}
    return {'err':'403', 'msg':'player is quit'}

@app.get('/volume')
def _volume():
    return volume(False)

@app.post('/seek')
def seek():
    if player and player.is_alive():
        value = request.forms.get('value', 0)
        type = request.forms.get('type', 0)
        player.seek(float(value), int(type))
        return {'length':player.length, 'position':player.percent_pos}
    return {'err':'403', 'msg':'player is quit'}

@app.post('/pt_step')
def pt_step():
    if player and player.is_alive():
        value = request.forms.get('value', 1)
        force = request.forms.get('force', 0)
        if force:
            player.pt_step(int(value), int(force))
        else:
            player.pt_step(int(value))
        return {'filename':player.filename}
    else:
        return {'err':'403', 'msg':'player is quit'}

@app.get('/status')
def status():
    if player and player.is_alive():
        return {'filename':player.filename, 'position':player.percent_pos, 'length':player.length}
    else:
        return {'err':'403', 'msg':'player is quit'}

@app.post('/mute')
def mute():
    if player and player.is_alive():
        player.mute = not player.mute
        return {'mute':player.mute}
    else:
        return {'err':'403', 'msg':'player is quit'}

if __name__ == '__main__':
    from bottle import run
    run(app)
