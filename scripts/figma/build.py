"""Extract assets and texts for the landing from the cached Figma file.

Writes:
  src/assets/icons/*.svg      vector icons / logo
  src/figma/art/*.json        decorative compositions rendered by <FigmaArt>
  src/figma/images.ts         named raster images (object-fit, crop, placement)
  src/locales/{uz,ru,en}.json texts with semantic keys
  .cache/imgjobs.json         resize/crop jobs for images.mjs
"""
import json
import os
import re

import lib
from lib import (CONTAINERS, SHAPES, Ctx, build, frame_svg, img_need, r3, radii_of, rounded_rect_path, shape_parts,
                 visible)

PROJ, CACHE = lib.PROJ, lib.CACHE
sections = {s['name'].split()[-1]: sorted(s['children'], key=lambda f: int(f['name'].split()[-1]))
            for s in lib.doc['document']['children'][0]['children']}


def frame(lang, slide):
    return sections[lang][slide - 1]


def walk(n, fn, path=()):
    if not n.get('visible', True):
        return
    fn(n, path)
    seen = {}
    for i, c in enumerate(n.get('children', [])):
        k = seen[c['name']] = seen.get(c['name'], -1) + 1
        walk(c, fn, path + ((i, c['name'], k),))


def find(root, pred):
    found = []
    walk(root, lambda n, p: found.append(n) if pred(n) else None)
    return found


def by_name(slide, name, lang='uz'):
    res = find(frame(lang, slide), lambda n: n['name'] == name)
    assert res, (slide, name)
    return max(res, key=lambda n: n['size']['x'])


def image_fill(n):
    return next(p for p in n.get('fills', []) if p['type'] == 'IMAGE' and visible(p))


def by_ref(slide, prefix):
    res = find(frame('uz', slide), lambda n: any(p['type'] == 'IMAGE' and p['imageRef'].startswith(prefix) and visible(p)
                                                 for p in n.get('fills', [])))
    assert res, (slide, prefix)
    return res[0]


def rel_box(n, slide, lang='uz'):
    f = frame(lang, slide)['absoluteBoundingBox']
    b = n['absoluteBoundingBox']
    return b['x'] - f['x'], b['y'] - f['y'], b['width'], b['height']


# ---------------------------------------------------------------- icons (svg)
def svg_tree(n, ctx, root=False):
    if not n.get('visible', True) or n['type'] == 'TEXT':
        return ''
    w, h = n['size']['x'], n['size']['y']
    defs, body = [], []
    if n['type'] in SHAPES:
        defs, body = shape_parts(n, ctx, w, h, n.get('fillGeometry', []), n.get('strokeGeometry', []))
    elif n['type'] in CONTAINERS and n['type'] != 'GROUP' and n.get('fills'):
        defs, body = shape_parts(n, ctx, w, h, [{'path': rounded_rect_path(w, h, radii_of(n))}], [])
    kids = ''
    if n['type'] in CONTAINERS:
        kids = ''.join(svg_tree(c, ctx) for c in n.get('children', []))
    if not body and not kids:
        return ''
    op = f' opacity="{r3(n["opacity"])}"' if n.get('opacity', 1) < 1 else ''
    tr = ''
    if not root:
        (a, c, e), (b, d, f) = n['relativeTransform']
        tr = f' transform="matrix({r3(a)} {r3(b)} {r3(c)} {r3(d)} {r3(e)} {r3(f)})"'
    d = f'<defs>{"".join(defs)}</defs>' if defs else ''
    return f'<g{tr}{op}>{d}{"".join(body)}{kids}</g>'


def export_svg(n, name):
    w, h = n['size']['x'], n['size']['y']
    ctx = Ctx(f'{name}-')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{r3(w)}" height="{r3(h)}" viewBox="0 0 {r3(w)} {r3(h)}" '
           f'fill="none">{svg_tree(n, ctx, root=True)}</svg>')
    os.makedirs(f'{PROJ}/src/assets/icons', exist_ok=True)
    open(f'{PROJ}/src/assets/icons/{name}.svg', 'w').write(svg)


ICONS = {  # file name -> (slide, node name)
    'logo': (1, 'logo 2'),
    'bullet': (3, 'Polygon 4'),
    'leaf': (4, 'Frame 78'),
    'mortarboard': (4, 'mortarboard-02'),
    'academy-leaf': (4, 'Vector', ),
    'user-group-02': (8, 'user-group-02'),
    'pie-chart-08': (4, 'pie-chart-08'),
    'analytics-up': (8, 'analytics-up'),
    'alert-square': (4, 'alert-square'),
    'computer-phone-sync': (5, 'computer-phone-sync'),
    'credit-card-change': (5, 'credit-card-change'),
    'money-receive-02': (5, 'money-receive-02'),
    'api': (5, 'api'),
    'mentoring': (6, 'mentoring'),
    'online-learning-02': (6, 'online-learning-02'),
    'computer-video-call': (6, 'computer-video-call'),
    'certificate-02': (6, 'certificate-02'),
    'ai-voice-01': (7, 'ai-voice-01'),
    'chat-bot': (7, 'chat-bot'),
    'artificial-intelligence-04': (7, 'artificial-intelligence-04'),
    'ai-content-generator-02': (7, 'ai-content-generator-02'),
    'ai-computer': (7, 'ai-computer'),
    'ai-programming': (7, 'ai-programming'),
    'user-add-01': (8, 'user-add-01'),
    'user-round-key': (8, 'user-round-key'),
    'inspect-code': (8, 'inspect-code'),
    'notebook': (9, 'notebook'),
    'login-method': (9, 'login-method'),
    'dashboard-square-setting': (9, 'dashboard-square-setting'),
    'rocket-01': (9, 'rocket-01'),
    'user-group-03': (10, 'user-group-03'),
    'search-dollar': (10, 'search-dollar'),
    'brochure': (10, 'brochure'),
    'chart-down': (10, 'chart-down'),
    'dashboard-square-01': (10, 'dashboard-square-01'),
    'qr-frame': (12, 'Union'),
}


def export_icons():
    for name, (slide, node) in ICONS.items():
        if name == 'academy-leaf':  # big decorative shape inside the Academy card
            n = by_name(4, 'App')
            n = next(x for x in find(n, lambda x: x['type'] == 'VECTOR' and x['size']['x'] > 200))
        else:
            n = by_name(slide, node)
        export_svg(n, name)


# ---------------------------------------------------------------- raster images
imgjobs = {}
images_ts = {}


def image(name, n, fit=None):
    p = image_fill(n)
    ref = p['imageRef']
    iw, ih, _ = lib.dims[ref]
    w, h = n['size']['x'], n['size']['y']
    mode = p.get('scaleMode', 'FILL')
    crop = None
    if mode == 'STRETCH' and p.get('imageTransform'):
        (a, _, e), (_, d, f) = p['imageTransform']
        x0, y0 = max(0, e), max(0, f)
        x1, y1 = min(1, e + a), min(1, f + d)
        crop = [round(x0 * iw), round(y0 * ih), round((x1 - x0) * iw), round((y1 - y0) * ih)]
    imgjobs[name] = {'ref': ref, 'crop': crop, 'size': max(w, h)}
    images_ts[name] = {'src': f'/figma/img/{name}.webp', 'w': r3(w), 'h': r3(h),
                       'fit': fit or {'FILL': 'cover', 'FIT': 'contain'}.get(mode, 'fill')}
    return images_ts[name]


def placed(name, n, container):
    """Image placed inside a (clipping) container, as percentages of the container box."""
    info = image(name, n)
    cb, nb = container['absoluteBoundingBox'], n['absoluteBoundingBox']
    info['box'] = [r3((nb['x'] - cb['x']) / cb['width'] * 100), r3((nb['y'] - cb['y']) / cb['height'] * 100),
                   r3(nb['width'] / cb['width'] * 100), r3(nb['height'] / cb['height'] * 100)]
    info['aspect'] = r3(cb['width'] / cb['height'])
    return info


IMAGES = {  # name -> (slide, ref prefix)
    'value-innovation': (2, '020abcb6'), 'value-reliability': (2, '0372fc17'), 'value-flexibility': (2, 'e9aebbc4'),
    'service-phone': (3, 'bf53261c'), 'service-card': (3, '945ecc83'), 'service-api': (3, '1e8cd173'),
    'app-biznes': (4, '0d3d68f3'), 'app-credit': (4, 'e3f2fa1a'), 'app-superapp': (4, '01981a46'),
    'app-smile': (4, '418d172c'), 'app-ailab': (4, '510f9add'), 'app-findiag': (4, 'bcc23863'),
    'app-aicall': (4, 'a68c7571'), 'app-voicepay': (4, '72593b4c'), 'app-buyurtmam': (4, 'afc73472'),
    'app-biznesim': (4, 'fd60f8c9'), 'app-crm': (4, 'f39c0832'), 'app-hrm': (4, 'e111fc91'), 'app-edo': (4, 'fc459678'),
    'app-dev': (4, '99d0bf5c'), 'app-audit': (4, 'e2e13aac'), 'app-consulting': (4, '7be2b65f'),
    'feature-superapp': (5, '176f605e'), 'feature-biometric': (5, 'b180e68f'), 'feature-internship': (6, '63b779d8'),
    'ai-visual': (7, 'af1424cb'), 'outsourcing-visual': (8, 'cdf44056'), 'b2b-visual': (9, 'd498a1ad'),
    'qr': (12, 'a05538f0'),
}


def export_images():
    for name, (slide, prefix) in IMAGES.items():
        image(name, by_ref(slide, prefix))
    # partner logos and certificates: keep their placement inside the white cards
    f = frame('uz', 11)
    rows = [by_name(11, 'Frame 2131328563'), by_name(11, 'Frame 2131328564'),
            by_name(11, 'Frame 2131328567'), by_name(11, 'Frame 2131328568')]
    local, intl = [], []
    for ri, row in enumerate(rows):
        for ci, card in enumerate(row['children']):
            logo = next(c for c in card['children'] if c.get('visible', True))
            name = f'partner-{"local" if ri < 2 else "intl"}-{ri % 2 * len(row["children"]) + ci + 1}'
            (local if ri < 2 else intl).append(name)
            placed(name, logo, card)
    certs = []
    for i, prefix in enumerate(['95faf48c', 'b7af108b', 'd3f0a79a', 'c6f79c0b']):
        n = by_ref(11, prefix)
        certs.append(f'cert-{i + 1}')
        image(f'cert-{i + 1}', n, fit='contain')
    assert f
    return {'partnersLocal': local, 'partnersIntl': intl, 'certs': certs}


# ---------------------------------------------------------------- art islands
def art(name, slide, nodes, clip=None, box=None, lang='uz'):
    """Render nodes (children of full-frame wrappers) as a positioned composition.

    `clip` limits the composition to an area, `box` sets it exactly (e.g. to keep a blurred glow).
    """
    fr = frame(lang, slide)
    ns = [by_name(slide, x, lang) for x in nodes]
    boxes = [rel_box(n, slide, lang) for n in ns]
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes)
    y1 = max(b[1] + b[3] for b in boxes)
    if clip:
        x0, y0, x1, y1 = max(x0, clip[0]), max(y0, clip[1]), min(x1, clip[2]), min(y1, clip[3])
    if box:
        x0, y0, x1, y1 = box
    ctx = Ctx(f'art-{name}-')
    kids = [build(n, ctx, {}, 'x') for n in ns]
    root = {'s': f'position:relative;width:{r3(x1 - x0)}px;height:{r3(y1 - y0)}px;overflow:hidden',
            'c': [{'s': f'position:absolute;left:{r3(-x0)}px;top:{r3(-y0)}px;width:0;height:0',
                   'c': [k for k in kids if k]}]}
    os.makedirs(f'{PROJ}/src/figma/art', exist_ok=True)
    json.dump({'w': r3(x1 - x0), 'h': r3(y1 - y0), 'x': r3(x0), 'y': r3(y0), 'root': root},
              open(f'{PROJ}/src/figma/art/{name}.json', 'w'), separators=(',', ':'), ensure_ascii=False)
    assert fr


def export_art():
    W, H = 3508, 2480
    art('cover', 1, ['Polygon 1', 'Line 8'], clip=(0, 0, W, H))
    art('contacts', 12, ['Polygon 1', 'Line 8'], clip=(0, 0, W, H))
    art('globe', 2, ['Ellipse 3', 'image 83'], box=(0, 0, W, H))
    art('fintech-visual', 5, ['Group 1597880398', 'image 54'])
    art('education-visual', 6, ['Group 2087326148'])
    art('bank-visual', 10, ['Group 2087326149', 'image 118'], clip=(0, 0, W, H))


# ---------------------------------------------------------------- texts
def texts_of(lang, slide):
    """Visible text nodes of a slide in document order: (node, path, x, y)."""
    fr = frame(lang, slide)
    out = []

    def add(n, p):
        if n['type'] == 'TEXT':
            x, y, _, _ = rel_box(n, slide, lang)
            out.append((n, p, x, y))

    walk(fr, add)
    return out


def raw(n):
    if any(n.get('characterStyleOverrides') or []):
        chars, ovr = n['characters'], n['characterStyleOverrides']
        ids = [ovr[i] if i < len(ovr) else 0 for i in range(len(chars))]
        runs, start = [], 0
        for i in range(1, len(chars) + 1):
            if i == len(chars) or ids[i] != ids[start]:
                runs.append(chars[start:i])
                start = i
        return runs
    return n['characters']


def clean(s, keep_newlines=False):
    s = s.replace('\r\n', '\n').replace('\r', '\n').replace(' ', '\n')
    s = re.sub(r'^▸\s*', '', s.strip())
    if keep_newlines:
        s = '\n'.join(re.sub(r'[ \t]+', ' ', line).strip() for line in s.split('\n'))
    else:
        s = re.sub(r'\s*\n\s*', ' ', s)
        s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\s+([,.:;!?])', r'\1', s)
    return s.strip()


review = []
# texts the automatic matching gets wrong: (lang, slide, uz index) -> start of the right text
PICK = {('ru', 5, 9): 'FinTech-стартапы'}


def match(lang, slide, idx):
    uz = texts_of('uz', slide)
    if lang == 'uz':
        return uz[idx][0]
    un, upath, ux, uy = uz[idx]
    cand = texts_of(lang, slide)
    if slide == 7:  # the visible page is the last wrapper frame
        last = len(frame(lang, 7)['children']) - 1
        cand = [c for c in cand if c[1][0][0] == last]
    def names(p):  # text nodes are named after their content, so compare them by index
        return tuple((nm, k) for _, nm, k in p[:-1]) + (p[-1][0],)

    if (lang, slide, idx) in PICK:
        return next(c[0] for c in cand if c[0]['characters'].startswith(PICK[lang, slide, idx]))
    same = [c for c in cand if names(c[1]) == names(upath)]
    if len(same) == 1:
        return same[0][0]
    best = min(cand, key=lambda c: abs(c[2] - ux) + 2 * abs(c[3] - uy))
    review.append((lang, slide, idx, un['characters'][:40], best[0]['characters'][:40]))
    return best[0]


def T(slide, idx, part=None, nl=False):
    return ('T', slide, idx, part, nl)


def resolve(spec, lang):
    if isinstance(spec, dict):
        return {k: resolve(v, lang) for k, v in spec.items()}
    if isinstance(spec, list):
        return [resolve(v, lang) for v in spec]
    _, slide, idx, part, nl = spec
    v = raw(match(lang, slide, idx))
    if part is None:
        return clean(''.join(v) if isinstance(v, list) else v, nl)
    runs = v if isinstance(v, list) else [v]
    if part == 'base':
        return clean(''.join(runs[:-1]) if len(runs) > 1 else runs[0], nl)
    return clean(runs[-1], nl) if len(runs) > 1 else ''


def pairs(slide, *idx):
    return [{'title': T(slide, i), 'text': T(slide, i + 1)} for i in idx]


def direction(slide, title, num, sub, paras, feats, aud_title, aud):
    return {'number': T(slide, num), 'title': T(slide, title), 'subtitle': T(slide, sub),
            'paragraphs': [T(slide, p) for p in paras], 'features': pairs(slide, *feats),
            'audienceTitle': T(slide, aud_title), 'audience': [T(slide, a) for a in aud]}


SPEC = {
    'cover': {'profile': T(1, 0), 'year': T(1, 1)},
    'about': {
        'title': T(2, 11, 'base'), 'titleAccent': T(2, 11, 'accent'),
        'paragraphs': [T(2, 12), T(2, 13), T(2, 14)],
        'resultsTitle': T(2, 0),
        'stats': [{'value': T(2, 5), 'label': T(2, 6)}, {'value': T(2, 7), 'label': T(2, 8)},
                  {'value': T(2, 9), 'label': T(2, 10)}],
        'valuesTitle': T(2, 1), 'values': [T(2, 2), T(2, 3), T(2, 4)],
    },
    'services': {
        'title': T(3, 30, 'base'), 'titleAccent': T(3, 30, 'accent'), 'subtitle': T(3, 31),
        'cards': {
            'design': {'title': T(3, 18), 'text': T(3, 19), 'items': pairs(3, 20, 22)},
            'product': {'title': T(3, 12), 'text': T(3, 13), 'items': pairs(3, 14, 16)},
            'quality': {'title': T(3, 24), 'text': T(3, 25), 'items': pairs(3, 26, 28)},
            'digital': {'title': T(3, 0), 'text': T(3, 1), 'items': pairs(3, 2, 4)},
            'engineering': {'title': T(3, 6), 'text': T(3, 7), 'items': pairs(3, 8, 10)},
        },
    },
    'directions': {
        'title': T(4, 0, 'base'), 'titleAccent': T(4, 0, 'accent'),
        'fintech': {'title': T(4, 1), 'text': T(4, 2), 'apps': [T(4, i) for i in range(3, 7)]},
        'ai': {'title': T(4, 34), 'text': T(4, 35), 'apps': [T(4, i) for i in range(36, 40)]},
        'social': {'title': T(4, 14), 'text': T(4, 15), 'apps': [T(4, i) for i in range(16, 19)]},
        'bank': {'title': T(4, 19), 'text': T(4, 20), 'items': pairs(4, 21, 23, 25, 27)},
        'education': {'title': T(4, 7), 'text': T(4, 8), 'academy': T(4, 9), 'academyText': T(4, 10),
                      'tags': [T(4, 11), T(4, 12), T(4, 13)]},
        'outsourcing': {'title': T(4, 40), 'text': T(4, 41), 'apps': [T(4, i) for i in range(42, 45)]},
        'b2b': {'title': T(4, 29), 'text': T(4, 30), 'apps': [T(4, i) for i in range(31, 34)]},
    },
    'fintech': {**direction(5, 0, 1, 2, [3], [10, 12, 14, 16, 18, 20], 5, [6, 7, 8, 9]), 'featuresTitle': T(5, 4)},
    'education': direction(6, 0, 1, 2, [3, 4], [5, 7, 9, 11, 13], 15, [16, 17, 18, 19]),
    'ai': direction(7, 18, 19, 20, [21, 22], [28, 30, 32, 34, 36, 38], 23, [24, 25, 26, 27]),
    'outsourcing': direction(8, 0, 1, 2, [3, 4], [5, 7, 9, 11, 13], 15, [16, 17, 18, 19]),
    'b2b': direction(9, 0, 1, 2, [3, 4], [9, 11, 13, 15, 17], 5, [6, 7, 8]),
    'bank': direction(10, 0, 1, 2, [3, 4], [9, 11, 13, 15, 17], 5, [6, 7, 8]),
    'partners': {
        'title': T(11, 0), 'lead': T(11, 1), 'text': T(11, 2), 'local': T(11, 13), 'international': T(11, 14),
        'certsTitle': T(11, 3), 'certsText': T(11, 4),
        'certs': [{'title': T(11, i), 'text': T(11, i + 1)} for i in (5, 7, 9, 11)],
    },
    'contacts': {
        'addressLabel': T(12, 0), 'address': T(12, 1, nl=True), 'emailLabel': T(12, 2), 'email': T(12, 3),
        'phoneLabel': T(12, 4), 'phone': T(12, 5), 'website': T(12, 6),
    },
}


def en_contacts():
    """The en contacts page merges the block into one text node."""
    texts = [n['characters'] for n, *_ in texts_of('en', 12)]
    lines = [clean(x) for x in texts[0].replace('\r\n', '\n').split('\n') if x.strip()]
    return {'addressLabel': lines[0], 'address': '\n'.join(lines[1:3]), 'emailLabel': lines[3], 'email': lines[4],
            'phoneLabel': lines[5], 'phone': lines[6], 'website': clean(texts[1])}


def export_locales():
    for lang in ('uz', 'ru', 'en'):
        spec = {k: v for k, v in SPEC.items() if not (lang == 'en' and k == 'contacts')}
        data = resolve(spec, lang)
        if lang == 'en':
            data['contacts'] = en_contacts()
        data = {k: data[k] for k in SPEC}
        json.dump(data, open(f'{PROJ}/src/locales/{lang}.json', 'w'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    export_icons()
    groups = export_images()
    export_art()
    export_locales()
    with open(f'{PROJ}/src/figma/images.ts', 'w') as fh:
        fh.write('// Generated by scripts/figma/build.py — do not edit.\n')
        fh.write("export type FigmaImage = { src: string; w: number; h: number; fit: 'cover' | 'contain' | 'fill'; "
                 'box?: number[]; aspect?: number }\n\n')
        fh.write(f'export const images = {json.dumps(images_ts, indent=2, ensure_ascii=False)} as const satisfies '
                 'Record<string, FigmaImage>\n\n')
        fh.write(f'export const groups = {json.dumps(groups, indent=2)} as const\n')
    json.dump(imgjobs, open(f'{CACHE}/imgjobs.json', 'w'))
    json.dump(img_need, open(f'{CACHE}/imgneed.json', 'w'))
    for r in review:
        print('matched by position:', r)
    print('icons', len(ICONS), 'images', len(images_ts), 'art refs', len(img_need))
