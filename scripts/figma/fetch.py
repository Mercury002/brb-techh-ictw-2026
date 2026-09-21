"""Download the Figma file (with vector geometry) and its image fills into .cache/.

Usage: FIGMA_TOKEN=figd_... python3 scripts/figma/fetch.py
"""
import concurrent.futures, json, os, urllib.request

FILE_KEY = 'ENDaKLye6Xc08F7tOoGx26'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')
TOKEN = os.environ['FIGMA_TOKEN']
EXT = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/gif': 'gif', 'image/webp': 'webp'}


def api(path):
    req = urllib.request.Request(f'https://api.figma.com/v1/{path}', headers={'X-Figma-Token': TOKEN})
    return urllib.request.urlopen(req).read()


os.makedirs(f'{CACHE}/imgs', exist_ok=True)
open(f'{CACHE}/geom.json', 'wb').write(api(f'files/{FILE_KEY}?geometry=paths'))
urls = json.loads(api(f'files/{FILE_KEY}/images'))['meta']['images']


def get(item):
    ref, url = item
    res = urllib.request.urlopen(url)
    ext = EXT.get(res.headers.get('Content-Type'), 'bin')
    open(f'{CACHE}/imgs/{ref}.{ext}', 'wb').write(res.read())
    return ref, ext


with concurrent.futures.ThreadPoolExecutor(12) as ex:
    exts = dict(ex.map(get, [(r, u) for r, u in urls.items() if u]))
json.dump(exts, open(f'{CACHE}/imgext.json', 'w'))
print('images', len(exts))
