"""Helpers that turn Figma REST nodes (fetched with geometry=paths) into css/svg."""
import json, math, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '.cache')
PROJ = os.path.abspath(os.path.join(HERE, '..', '..'))
doc = json.load(open(f'{CACHE}/geom.json'))
dims = json.load(open(f'{CACHE}/imgdims.json'))
IMG_URL = '/figma/{}.webp'

img_need = {}  # ref -> needed max side in design px


def r3(v):
    v = round(v, 3)
    return int(v) if v == int(v) else v


def px(v):
    return f'{r3(v)}px'


def rgba(c, op=1.0):
    a = c.get('a', 1) * op
    r, g, b = (round(c[k] * 255) for k in 'rgb')
    if a >= 0.999:
        return f'#{r:02x}{g:02x}{b:02x}'
    return f'rgba({r},{g},{b},{r3(a)})'


def visible(p):
    return p.get('visible', True) and p.get('opacity', 1) > 0


class Ctx:
    def __init__(self, prefix):
        self.prefix = prefix
        self.n = 0

    def uid(self):
        self.n += 1
        return f'{self.prefix}{self.n}'


# ---------- paths ----------
TOK = re.compile(r'[MLCQZHVmlcqzhv]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?')


def transform_path(d, m):
    (a, c, e), (b, dd, f) = m
    out, toks, i, cmd = [], TOK.findall(d), 0, None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            assert cmd in 'MLCQZ', cmd
            out.append(cmd)
            i += 1
            continue
        x, y = float(toks[i]), float(toks[i + 1])
        i += 2
        out.append(f'{r3(a * x + c * y + e)} {r3(b * x + dd * y + f)}')
    return ' '.join(out)


def rounded_rect_path(w, h, radii):
    tl, tr, br, bl = (min(r, w / 2, h / 2) for r in radii)
    k = 0.5522847498
    p = [f'M{r3(tl)} 0', f'L{r3(w - tr)} 0']
    if tr: p.append(f'C{r3(w - tr + tr * k)} 0 {r3(w)} {r3(tr - tr * k)} {r3(w)} {r3(tr)}')
    p.append(f'L{r3(w)} {r3(h - br)}')
    if br: p.append(f'C{r3(w)} {r3(h - br + br * k)} {r3(w - br + br * k)} {r3(h)} {r3(w - br)} {r3(h)}')
    p.append(f'L{r3(bl)} {r3(h)}')
    if bl: p.append(f'C{r3(bl - bl * k)} {r3(h)} 0 {r3(h - bl + bl * k)} 0 {r3(h - bl)}')
    p.append(f'L0 {r3(tl)}')
    if tl: p.append(f'C0 {r3(tl - tl * k)} {r3(tl - tl * k)} 0 {r3(tl)} 0')
    p.append('Z')
    return ''.join(p)


def radii_of(n):
    if n.get('rectangleCornerRadii'):
        return n['rectangleCornerRadii']
    r = n.get('cornerRadius', 0)
    return [r, r, r, r]


# ---------- paints ----------
def note_img(p, w, h):
    ref = p['imageRef']
    iw, ih, _ = dims[ref]
    mode = p.get('scaleMode', 'FILL')
    if mode == 'FIT':
        s = min(w / iw, h / ih)
    elif mode == 'TILE':
        s = p.get('scalingFactor', 1)
    else:
        s = max(w / iw, h / ih)
        t = p.get('imageTransform')
        if mode == 'STRETCH' and t:
            s /= max(1e-3, min(abs(t[0][0]), abs(t[1][1])))
    img_need[ref] = max(img_need.get(ref, 0), s * max(iw, ih))


def inv(m):
    (a, c, e), (b, d, f) = m
    det = a * d - b * c
    return [[d / det, -c / det, (c * f - d * e) / det], [-b / det, a / det, (b * e - a * f) / det]]


def svg_paint(p, w, h, ctx, defs):
    """Return (fill value, opacity) for an svg element."""
    t = p['type']
    op = p.get('opacity', 1)
    if t == 'SOLID':
        return rgba(p['color'], op)
    if t.startswith('GRADIENT'):
        gid = ctx.uid()
        stops = ''.join(
            f'<stop offset="{r3(s["position"])}" stop-color="{rgba({**s["color"], "a": 1})}"'
            + (f' stop-opacity="{r3(s["color"]["a"] * op)}"' if s['color']['a'] * op < 0.999 else '') + '/>'
            for s in p['gradientStops'])
        hp = [(q['x'] * w, q['y'] * h) for q in p['gradientHandlePositions']]
        if t == 'GRADIENT_LINEAR':
            defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{r3(hp[0][0])}" y1="{r3(hp[0][1])}" '
                        f'x2="{r3(hp[1][0])}" y2="{r3(hp[1][1])}">{stops}</linearGradient>')
        else:
            (x0, y0), (x1, y1), (x2, y2) = hp
            mtx = f'matrix({r3(x1 - x0)} {r3(y1 - y0)} {r3(x2 - x0)} {r3(y2 - y0)} {r3(x0)} {r3(y0)})'
            defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" '
                        f'gradientTransform="{mtx}">{stops}</radialGradient>')
        return f'url(#{gid})'
    if t == 'IMAGE':
        note_img(p, w, h)
        pid = ctx.uid()
        ref = p['imageRef']
        href = IMG_URL.format(ref)
        mode = p.get('scaleMode', 'FILL')
        opa = f' opacity="{r3(op)}"' if op < 1 else ''
        if mode == 'TILE':
            iw, ih, _ = dims[ref]
            s = p.get('scalingFactor', 1)
            defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{r3(iw * s)}" height="{r3(ih * s)}">'
                        f'<image href="{href}" width="{r3(iw * s)}" height="{r3(ih * s)}"{opa}/></pattern>')
        elif mode == 'STRETCH' and p.get('imageTransform'):
            it = inv(p['imageTransform'])
            (a, c, e), (b, d, f) = it
            defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{r3(w)}" height="{r3(h)}">'
                        f'<image href="{href}" width="1" height="1" preserveAspectRatio="none"{opa} '
                        f'transform="matrix({r3(a * w)} {r3(b * h)} {r3(c * w)} {r3(d * h)} {r3(e * w)} {r3(f * h)})"/></pattern>')
        else:
            par = {'FILL': 'xMidYMid slice', 'FIT': 'xMidYMid meet'}.get(mode, 'none')
            defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{r3(max(w, .01))}" height="{r3(max(h, .01))}">'
                        f'<image href="{href}" width="{r3(w)}" height="{r3(h)}" preserveAspectRatio="{par}"{opa}/></pattern>')
        return f'url(#{pid})'
    return None


def css_gradient(p, w, h):
    """CSS background layer for a gradient paint over a w x h box (used for text)."""
    op = p.get('opacity', 1)
    hp = [(q['x'] * w, q['y'] * h) for q in p['gradientHandlePositions']]
    stops_raw = p['gradientStops']
    if p['type'] == 'GRADIENT_LINEAR':
        (x0, y0), (x1, y1) = hp[0], hp[1]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        ux, uy = dx / ln, dy / ln
        ang = math.degrees(math.atan2(ux, -uy))
        L = abs(w * ux) + abs(h * uy)
        sx, sy = w / 2 - ux * L / 2, h / 2 - uy * L / 2
        p0 = ((x0 - sx) * ux + (y0 - sy) * uy) / L
        p1 = ((x1 - sx) * ux + (y1 - sy) * uy) / L
        stops = ', '.join(f'{rgba(s["color"], op)} {r3((p0 + s["position"] * (p1 - p0)) * 100)}%' for s in stops_raw)
        return f'linear-gradient({r3(ang)}deg, {stops})'
    (x0, y0), (x1, y1), (x2, y2) = hp
    rx, ry = math.hypot(x1 - x0, y1 - y0), math.hypot(x2 - x0, y2 - y0)
    stops = ', '.join(f'{rgba(s["color"], op)} {r3(s["position"] * 100)}%' for s in stops_raw)
    return f'radial-gradient({px(rx)} {px(ry)} at {px(x0)} {px(y0)}, {stops})'


# ---------- nodes ----------
def pos_style(n, root=False):
    w, h = n['size']['x'], n['size']['y']
    if root:
        return [f'position:relative', f'width:{px(w)}', f'height:{px(h)}']
    (a, c, e), (b, d, f) = n['relativeTransform']
    s = ['position:absolute', f'width:{px(w)}', f'height:{px(h)}']
    if abs(a - 1) < 1e-4 and abs(d - 1) < 1e-4 and abs(b) < 1e-4 and abs(c) < 1e-4:
        s += [f'left:{px(e)}', f'top:{px(f)}']
    else:
        s += ['left:0', 'top:0', 'transform-origin:0 0',
              f'transform:matrix({r3(a)},{r3(b)},{r3(c)},{r3(d)},{r3(e)},{r3(f)})']
    return s


BLEND = {'MULTIPLY': 'multiply', 'SCREEN': 'screen', 'OVERLAY': 'overlay', 'DARKEN': 'darken', 'LIGHTEN': 'lighten',
         'COLOR_DODGE': 'color-dodge', 'COLOR_BURN': 'color-burn', 'HARD_LIGHT': 'hard-light',
         'SOFT_LIGHT': 'soft-light', 'DIFFERENCE': 'difference', 'EXCLUSION': 'exclusion', 'HUE': 'hue',
         'SATURATION': 'saturation', 'COLOR': 'color', 'LUMINOSITY': 'luminosity'}


def common_style(n):
    s = []
    if n.get('opacity', 1) < 1:
        s.append(f'opacity:{r3(n["opacity"])}')
    if n.get('blendMode') in BLEND:
        s.append(f'mix-blend-mode:{BLEND[n["blendMode"]]}')
    filters = []
    for e in n.get('effects', []):
        if not e.get('visible', True):
            continue
        if e['type'] == 'LAYER_BLUR':
            filters.append(f'blur({px(e["radius"] / 2)})')
        elif e['type'] == 'BACKGROUND_BLUR':
            s.append(f'backdrop-filter:blur({px(e["radius"] / 2)});-webkit-backdrop-filter:blur({px(e["radius"] / 2)})')
        elif e['type'] == 'DROP_SHADOW' and n['type'] not in ('FRAME', 'COMPONENT', 'INSTANCE'):
            filters.append(f'drop-shadow({px(e["offset"]["x"])} {px(e["offset"]["y"])} {px(e["radius"] / 2)} {rgba(e["color"])})')
    if filters:
        s.append('filter:' + ' '.join(filters))
    return s


def shape_parts(n, ctx, w, h, fill_paths, stroke_paths):
    """(defs, body) svg markup for the fills/strokes of a node."""
    defs, body = [], []
    for p in n.get('fills', []):
        if not visible(p):
            continue
        fill = svg_paint(p, w, h, ctx, defs)
        if fill is None:
            continue
        for g in fill_paths:
            rule = ' fill-rule="evenodd"' if g.get('windingRule') == 'EVENODD' else ''
            body.append(f'<path d="{g["path"]}" fill="{fill}"{rule}/>')
    for p in n.get('strokes', []):
        if not visible(p):
            continue
        fill = svg_paint(p, w, h, ctx, defs)
        if fill is None:
            continue
        for g in stroke_paths:
            body.append(f'<path d="{g["path"]}" fill="{fill}"/>')
    return defs, body


def shape_svg(n, ctx, w, h, fill_paths, stroke_paths):
    defs, body = shape_parts(n, ctx, w, h, fill_paths, stroke_paths)
    if not body:
        return None
    d = f'<defs>{"".join(defs)}</defs>' if defs else ''
    return (f'<svg class="fg-svg" width="{r3(max(w, 1))}" height="{r3(max(h, 1))}" '
            f'xmlns="http://www.w3.org/2000/svg">{d}{"".join(body)}</svg>')


def frame_svg(n, ctx, w, h):
    """Fill + stroke of a frame drawn as svg rect/path."""
    radii = radii_of(n)
    fill_paths = [{'path': rounded_rect_path(w, h, radii)}]
    stroke_paths = []
    sw = n.get('strokeWeight', 0)
    if any(visible(p) for p in n.get('strokes', [])) and sw:
        al = n.get('strokeAlign', 'INSIDE')
        off = {'INSIDE': 0, 'CENTER': sw / 2, 'OUTSIDE': sw}[al]
        # ring = outer rounded rect minus inner rounded rect (evenodd)
        ow, oh = w + 2 * off, h + 2 * off
        outer = transform_path(rounded_rect_path(ow, oh, [r + off if r else 0 for r in radii]), [[1, 0, -off], [0, 1, -off]])
        iw_, ih_ = ow - 2 * sw, oh - 2 * sw
        io = sw - off
        inner = transform_path(rounded_rect_path(iw_, ih_, [max(0, r + off - sw) for r in radii]), [[1, 0, io], [0, 1, io]])
        stroke_paths = [{'path': outer + ' ' + inner}]
    svg = shape_svg({**n, 'strokes': []}, ctx, w, h, fill_paths, [])
    ssvg = None
    if stroke_paths:
        ssvg = shape_svg({'fills': [], 'strokes': n['strokes']}, ctx, w, h, [], stroke_paths)
        if ssvg:
            ssvg = ssvg.replace('<path ', '<path fill-rule="evenodd" ')
    return svg, ssvg


def text_node(n, ctx, texts, slide_key):
    w, h = n['size']['x'], n['size']['y']
    st = n['style']
    s = pos_style(n) + common_style(n)
    va = {'TOP': 'flex-start', 'CENTER': 'center', 'BOTTOM': 'flex-end'}.get(st.get('textAlignVertical', 'TOP'), 'flex-start')
    s += ['display:flex', 'flex-direction:column', f'justify-content:{va}']
    s += text_fill_css(n.get('fills', []), w, h)
    auto = st.get('textAutoResize', 'NONE')
    al = st.get('textAlignHorizontal', 'LEFT')
    p = ['margin:0', 'flex:none'] + font_css(st)
    p.append({'LEFT': 'text-align:left', 'CENTER': 'text-align:center', 'RIGHT': 'text-align:right',
              'JUSTIFIED': 'text-align:justify'}[al])
    if auto == 'WIDTH_AND_HEIGHT':
        p.append('white-space:pre')
        p.append(f'width:{px(w)}')
    else:
        slack = 4
        p.append('white-space:pre-wrap;overflow-wrap:break-word')
        p.append(f'width:{px(w + slack)}')
        if al == 'CENTER':
            p.append(f'margin-left:{px(-slack / 2)}')
        elif al == 'RIGHT':
            p.append(f'margin-left:{px(-slack)}')
    key = f't{len(texts)}'
    chars = n['characters']
    ovr = n.get('characterStyleOverrides') or []
    table = n.get('styleOverrideTable') or {}
    node = {'s': ';'.join(s), 't': {'p': ';'.join(p)}}
    if any(ovr):
        runs, cur, start = [], None, 0
        ids = [ovr[i] if i < len(ovr) else 0 for i in range(len(chars))]
        for i in range(len(chars) + 1):
            v = ids[i] if i < len(chars) else None
            if i == len(chars) or v != cur:
                if i > start:
                    runs.append((cur, chars[start:i]))
                cur, start = v, i
        texts[key] = [r[1] for r in runs]
        rs = []
        for oid, _ in runs:
            o = table.get(str(oid), {}) if oid else {}
            css = font_css(o, partial=True)
            if 'fills' in o:
                css += text_fill_css(o['fills'], w, h, span=True)
            rs.append(';'.join(css))
        node['t']['r'] = rs
    else:
        texts[key] = chars
    node['t']['k'] = f'{slide_key}.{key}'
    return node


def font_css(st, partial=False):
    c = []
    if 'fontFamily' in st:
        c.append(f"font-family:'{st['fontFamily']}'")
    if 'fontWeight' in st:
        c.append(f'font-weight:{st["fontWeight"]}')
    if 'fontSize' in st:
        c.append(f'font-size:{px(st["fontSize"])}')
    if 'lineHeightPx' in st and not (partial and st.get('lineHeightUnit') == 'INTRINSIC_%'):
        c.append(f'line-height:{px(st["lineHeightPx"])}')
    if st.get('letterSpacing'):
        c.append(f'letter-spacing:{px(st["letterSpacing"])}')
    if st.get('italic'):
        c.append('font-style:italic')
    tc = st.get('textCase')
    if tc in ('UPPER', 'LOWER', 'TITLE'):
        c.append('text-transform:' + {'UPPER': 'uppercase', 'LOWER': 'lowercase', 'TITLE': 'capitalize'}[tc])
    td = st.get('textDecoration')
    if td in ('UNDERLINE', 'STRIKETHROUGH'):
        c.append('text-decoration:' + ('underline' if td == 'UNDERLINE' else 'line-through'))
    return c


def text_fill_css(fills, w, h, span=False):
    fills = [f for f in fills if visible(f)]
    if not fills:
        return ['color:transparent']
    if len(fills) == 1 and fills[0]['type'] == 'SOLID':
        c = rgba(fills[0]['color'], fills[0].get('opacity', 1))
        return [f'color:{c}', f'-webkit-text-fill-color:{c}'] if span else [f'color:{c}']
    layers = []
    for f in reversed(fills):
        if f['type'] == 'SOLID':
            c = rgba(f['color'], f.get('opacity', 1))
            layers.append(f'linear-gradient({c},{c})')
        elif f['type'].startswith('GRADIENT'):
            layers.append(css_gradient(f, w, h))
    return [f'background-image:{", ".join(layers)}', '-webkit-background-clip:text', 'background-clip:text',
            'color:transparent', '-webkit-text-fill-color:transparent']


CONTAINERS = ('FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'COMPONENT_SET', 'SECTION')
SHAPES = ('VECTOR', 'ELLIPSE', 'RECTANGLE', 'REGULAR_POLYGON', 'STAR', 'LINE', 'BOOLEAN_OPERATION')


def build(n, ctx, texts, slide_key, root=False):
    if not n.get('visible', True):
        return None
    t = n['type']
    w, h = n['size']['x'], n['size']['y']
    if t == 'TEXT':
        return text_node(n, ctx, texts, slide_key)
    s = pos_style(n, root) + common_style(n)
    node = {}
    pre, post = [], []
    if t in SHAPES:
        svg = shape_svg(n, ctx, w, h, n.get('fillGeometry', []), n.get('strokeGeometry', []))
        if not svg:
            return None
        node['h'] = svg
    elif t in CONTAINERS:
        radii = radii_of(n)
        rad = ' '.join(px(min(r, w / 2, h / 2)) for r in radii)
        if any(radii):
            s.append(f'border-radius:{rad}')
        if n.get('clipsContent') and t != 'GROUP':
            s.append('overflow:hidden')
        if t != 'GROUP':
            fsvg, ssvg = frame_svg(n, ctx, w, h)
            if fsvg:
                node['h'] = fsvg
            if ssvg:
                post.append({'s': 'position:absolute;inset:0;pointer-events:none', 'h': ssvg})
        shadows, inset = [], []
        for e in n.get('effects', []):
            if not e.get('visible', True):
                continue
            if e['type'] == 'DROP_SHADOW':
                shadows.append(f'{px(e["offset"]["x"])} {px(e["offset"]["y"])} {px(e["radius"])} {px(e.get("spread", 0))} {rgba(e["color"])}')
            elif e['type'] == 'INNER_SHADOW':
                inset.append(f'inset {px(e["offset"]["x"])} {px(e["offset"]["y"])} {px(e["radius"])} {px(e.get("spread", 0))} {rgba(e["color"])}')
            elif e['type'] == 'GLASS':
                s.append('backdrop-filter:blur(12px) saturate(140%);-webkit-backdrop-filter:blur(12px) saturate(140%)')
                inset.append('inset 1.5px 1.5px 0 rgba(255,255,255,0.28)')
                inset.append('inset -1px -1px 0 rgba(255,255,255,0.1)')
            elif e['type'] == 'NOISE':
                pre.append({'s': f'position:absolute;inset:0;pointer-events:none;border-radius:{rad};opacity:{r3(e["color"]["a"])}',
                            'cl': 'fg-noise'})
        if shadows:
            s.append('box-shadow:' + ','.join(shadows))
        if inset:
            post.append({'s': f'position:absolute;inset:0;pointer-events:none;border-radius:{rad};box-shadow:{",".join(inset)}'})
    else:
        print('skip type', t, file=sys.stderr)
        return None
    node['s'] = ';'.join(s)
    kids = pre[:]
    if t in CONTAINERS:
        kids += build_children(n.get('children', []), ctx, texts, slide_key)
    kids += post
    if kids:
        node['c'] = kids
    return node


def build_children(children, ctx, texts, slide_key):
    out = []
    for i, c in enumerate(children):
        if c.get('isMask') and c.get('visible', True):
            geo = c.get('fillGeometry') or [{'path': rounded_rect_path(c['size']['x'], c['size']['y'], radii_of(c))}]
            d = ' '.join(transform_path(g['path'], c['relativeTransform']) for g in geo)
            inner = build_children(children[i + 1:], ctx, texts, slide_key)
            out.append({'s': f"position:absolute;left:0;top:0;width:100%;height:100%;clip-path:path('{d}')", 'c': inner})
            return out
        b = build(c, ctx, texts, slide_key)
        if b:
            out.append(b)
    return out


def root_bg(f):
    for p in reversed(f.get('fills', [])):
        if visible(p):
            if p['type'] == 'SOLID':
                return rgba(p['color'])
            if p['type'].startswith('GRADIENT'):
                return rgba(p['gradientStops'][0]['color'])
    return '#000'
