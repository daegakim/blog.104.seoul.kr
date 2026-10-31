#!/usr/bin/env python3
"""네이버 블로그용 만화풍 이미지 만들기 (FTH 세 사이트 공통).

사용: python3 tools/naver_card.py <spec.json> <출력폴더>
  → <slug>-naver-cover.jpg   대표사진 1:1 (1080x1080, 네이버 글 맨 위)
  → <slug>-naver-info.jpg    본문 만화풍 정보 그림 (가로 1080, 세로 자동)
  두 파일 모두 JPEG 안에 제목·설명·키워드·만든 곳·저작권 정보(EXIF·XMP)를 넣는다.

spec.json 예시는 _ops/style-guide.md 참고.
- 글자는 모두 코드로 넣는다(그림 생성 AI가 숫자·한글을 틀리게 쓰는 문제 방지). 숫자는 원문 그대로.
- 캐릭터·장식은 이 파일의 SVG(FTH 자체 제작)만 쓴다. 실존 인물·병원 로고·다른 회사 캐릭터는 쓰지 않는다.
"""
import json, os, sys, html, asyncio, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_CSS = 'file://' + os.path.join(HERE, 'fonts', 'jua', 'index.css')
INK = '#4a3a34'

PAL = {  # 섹션 제목 알약 색
    'pink': ('#ffd9df', '#ffb3c0'), 'mint': ('#d4f2e6', '#9fdcc4'), 'sky': ('#d8ecfb', '#a9d2f2'),
    'lemon': ('#fff1c4', '#ffd96b'), 'lilac': ('#e7defb', '#c9b6f2'), 'peach': ('#ffe3cc', '#ffc08f'),
}

# ---------- 캐릭터·장식 (FTH 자체 제작 SVG) ----------
def face(cx, cy, s=1.0, mood='smile'):
    e = 7 * s
    mouth = (f'<path d="M{cx-9*s},{cy+8*s} Q{cx},{cy+18*s} {cx+9*s},{cy+8*s}" stroke="{INK}" stroke-width="{3*s}" fill="none" stroke-linecap="round"/>'
             if mood == 'smile' else
             f'<path d="M{cx-8*s},{cy+10*s} Q{cx},{cy+20*s} {cx+8*s},{cy+10*s} Z" fill="#e8636f" stroke="{INK}" stroke-width="{2.5*s}"/>')
    return (f'<circle cx="{cx-15*s}" cy="{cy-2*s}" r="{e/1.6}" fill="{INK}"/><circle cx="{cx+15*s}" cy="{cy-2*s}" r="{e/1.6}" fill="{INK}"/>'
            f'<circle cx="{cx-14*s}" cy="{cy-4*s}" r="{1.6*s}" fill="#fff"/><circle cx="{cx+16*s}" cy="{cy-4*s}" r="{1.6*s}" fill="#fff"/>'
            f'<ellipse cx="{cx-26*s}" cy="{cy+8*s}" rx="{7*s}" ry="{4.5*s}" fill="#ff9fb0" opacity=".75"/>'
            f'<ellipse cx="{cx+26*s}" cy="{cy+8*s}" rx="{7*s}" ry="{4.5*s}" fill="#ff9fb0" opacity=".75"/>' + mouth)

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'

def ch_doctor(size=200):
    b = (f'<path d="M40,200 Q40,130 100,128 Q160,130 160,200 Z" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M100,130 L88,200 M100,130 L112,200" stroke="#9fc7e8" stroke-width="5"/>'
         f'<path d="M72,140 Q66,175 84,182" stroke="{INK}" stroke-width="4" fill="none"/><circle cx="86" cy="184" r="6" fill="#9fdcc4" stroke="{INK}" stroke-width="3"/>'
         f'<circle cx="100" cy="82" r="50" fill="#ffe2cc" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M52,74 Q56,26 102,28 Q150,30 150,76 Q130,52 100,56 Q70,58 52,74 Z" fill="#5b4038" stroke="{INK}" stroke-width="4"/>'
         + face(100, 88, 1.0))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def ch_patient(size=200):
    b = (f'<path d="M44,200 Q44,134 100,132 Q156,134 156,200 Z" fill="#ffc2cf" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M48,92 Q40,150 64,160 L64,90 Z M152,92 Q160,150 136,160 L136,90 Z" fill="#8a5a44" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="100" cy="86" r="50" fill="#ffe2cc" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M50,84 Q48,30 100,30 Q152,30 150,84 Q138,58 112,54 Q96,70 66,70 Q56,74 50,84 Z" fill="#8a5a44" stroke="{INK}" stroke-width="4"/>'
         + face(100, 92, 1.0))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def ch_beam(size=200, color='#ffcf4d'):
    """중입자선(빛 알갱이) 캐릭터"""
    rays = ''.join(f'<line x1="100" y1="100" x2="{100+92*__import__("math").cos(a*0.5236):.1f}" y2="{100+92*__import__("math").sin(a*0.5236):.1f}" stroke="#ffb84d" stroke-width="6" stroke-linecap="round" opacity=".7"/>' for a in range(12))
    b = (f'<circle cx="100" cy="100" r="88" fill="#fff4cc" opacity=".8"/>{rays}'
         f'<circle cx="100" cy="100" r="58" fill="{color}" stroke="{INK}" stroke-width="5"/>'
         f'<circle cx="80" cy="76" r="10" fill="#fff" opacity=".7"/>' + face(100, 104, 1.0))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def ch_calendar(size=120, mood='smile'):
    b = (f'<rect x="20" y="30" width="160" height="150" rx="22" fill="#fff" stroke="{INK}" stroke-width="5"/>'
         f'<path d="M20,52 Q20,30 42,30 L158,30 Q180,30 180,52 L180,70 L20,70 Z" fill="#ff8fa3" stroke="{INK}" stroke-width="5"/>'
         + ''.join(f'<rect x="{50+i*40}" y="14" width="10" height="30" rx="5" fill="{INK}"/>' for i in range(3))
         + face(100, 120, 1.0, mood))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def ch_shield(size=120):
    b = (f'<path d="M100,18 L170,44 Q170,140 100,184 Q30,140 30,44 Z" fill="#9fdcc4" stroke="{INK}" stroke-width="6"/>'
         f'<path d="M66,100 L92,126 L138,76" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def ch_folder(size=120):
    b = (f'<path d="M24,58 Q24,40 42,40 L82,40 L96,56 L158,56 Q176,56 176,74 L176,160 Q176,176 158,176 L42,176 Q24,176 24,160 Z" fill="#ffd96b" stroke="{INK}" stroke-width="5"/>'
         + face(100, 120, 1.0))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def deco_star(size=60, color='#ffd96b'):
    b = (f'<path d="M100,14 L124,72 L186,76 L138,116 L154,178 L100,144 L46,178 L62,116 L14,76 L76,72 Z" fill="{color}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
         + face(100, 104, 1.0))
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def deco_heart(size=50, color='#ff9fb0'):
    b = f'<path d="M100,176 Q20,120 24,70 Q30,26 74,28 Q94,30 100,54 Q106,30 126,28 Q170,26 176,70 Q180,120 100,176 Z" fill="{color}" stroke="{INK}" stroke-width="9"/>'
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

def deco_bubble(size=40):
    b = '<circle cx="100" cy="100" r="80" fill="#e9f6ff" stroke="#b8dcf5" stroke-width="10" opacity=".9"/><circle cx="72" cy="70" r="16" fill="#fff"/>'
    return svg(200, 200, b).replace('width="200" height="200"', f'width="{size}" height="{size}"')

CHARS = {'doctor': ch_doctor, 'patient': ch_patient, 'beam': ch_beam, 'calendar': ch_calendar,
         'shield': ch_shield, 'folder': ch_folder, 'star': deco_star, 'heart': deco_heart}

CSS = """
@import url('%s');
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;word-break:keep-all;background:#fff8ec;font-family:'Jua','Noto Sans CJK KR',sans-serif;color:%s}
.page{position:relative;padding:56px 54px 44px;overflow:hidden}
.deco{position:absolute}
h1{font-size:66px;line-height:1.22;text-align:center;letter-spacing:-1px;color:%s;text-shadow:3px 3px 0 #fff,-3px -3px 0 #fff,3px -3px 0 #fff,-3px 3px 0 #fff}
h1 .hl{color:#e8627a} h1 .hl2{color:#f2a33a}
.summary{margin:30px auto 0;background:#ffe1e6;border-radius:44px;padding:26px 40px;text-align:center;font-family:'Noto Sans CJK KR',sans-serif;font-weight:500;font-size:29px;line-height:1.55}
.summary small{display:block;margin-top:8px;font-size:21px;opacity:.75}
.card{position:relative;margin-top:62px;background:#fff;border:5px solid %s;border-radius:46px;padding:66px 38px 34px}
.pill{position:absolute;top:-34px;left:50%%;transform:translateX(-50%%);white-space:nowrap;border:5px solid %s;border-radius:40px;padding:10px 34px;font-size:38px}
.row{display:flex;align-items:center;gap:24px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.stat{border-radius:30px;padding:22px 16px;text-align:center}
.stat .v{font-size:66px;line-height:1.05}
.stat .l{font-size:29px;margin-top:6px}
.stat .n{font-family:'Noto Sans CJK KR',sans-serif;font-size:21px;margin-top:6px;opacity:.8}
.bar{margin:16px 0}
.bar .lab{font-size:28px;margin-bottom:6px}
.bar .track{height:52px;border:4px solid %s;border-radius:30px;background:#f3f0ea;overflow:hidden}
.bar .fill{height:100%%;border-radius:26px;display:flex;align-items:center;justify-content:flex-end;padding-right:18px;font-size:30px}
.steps{display:flex;justify-content:space-between;gap:10px}
.step{flex:1;text-align:center}
.step .t{font-size:28px;margin-top:4px}
.step .s{font-family:'Noto Sans CJK KR',sans-serif;font-size:21px;opacity:.8}
ul.lst{list-style:none}
ul.lst li{font-family:'Noto Sans CJK KR',sans-serif;font-weight:500;font-size:27px;line-height:1.5;padding:12px 0 12px 54px;position:relative;border-bottom:3px dashed #f1e4d6}
ul.lst li:last-child{border-bottom:0}
ul.lst li:before{content:'';position:absolute;left:4px;top:18px;width:30px;height:30px;border-radius:50%%;background:#9fdcc4;border:4px solid %s}
ul.lst li b{font-family:'Jua',sans-serif;font-weight:400;font-size:30px}
.bubble{position:relative;background:#fff;border:4px solid %s;border-radius:34px;padding:22px 28px;font-family:'Noto Sans CJK KR',sans-serif;font-weight:500;font-size:27px;line-height:1.55}
.foot{margin-top:40px;text-align:center;font-family:'Noto Sans CJK KR',sans-serif;font-size:20px;line-height:1.6;opacity:.8}
.brand{margin-top:12px;text-align:center;font-size:26px}
""" % (FONT_CSS, INK, INK, INK, INK, INK, INK, INK)

def esc(s): return html.escape(str(s))

def pill(title, color):
    a, b = PAL.get(color, PAL['mint'])
    return f'<div class="pill" style="background:{a}">{esc(title)}</div>'

def section(sec):
    t = sec.get('type'); color = sec.get('color', 'mint'); a, b = PAL.get(color, PAL['mint'])
    out = f'<div class="card">{pill(sec["title"], color)}'
    ch = sec.get('character')
    chhtml = CHARS[ch](150) if ch in CHARS else ''
    if t == 'stats':
        cells = ''.join(f'<div class="stat" style="background:{PAL[c][0]}"><div class="v">{esc(i["value"])}</div><div class="l">{esc(i["label"])}</div>' + (f'<div class="n">{esc(i["note"])}</div>' if i.get('note') else '') + '</div>'
                        for i, c in zip(sec['items'], ['pink', 'mint', 'sky', 'lemon', 'lilac', 'peach']))
        out += (f'<div class="row" style="margin-bottom:18px;justify-content:center">{chhtml}<div class="bubble" style="flex:1">{esc(sec.get("lead",""))}</div></div>' if sec.get('lead') else '') + f'<div class="grid">{cells}</div>'
    elif t == 'bars':
        mx = max(float(i['value']) for i in sec['items']) or 1
        out += (f'<div class="row" style="margin-bottom:10px">{chhtml}<div class="bubble" style="flex:1">{esc(sec.get("lead",""))}</div></div>' if sec.get('lead') else '')
        for i, c in zip(sec['items'], ['sky', 'mint', 'pink', 'lemon', 'lilac']):
            w = max(18, float(i['value']) / mx * 100)
            out += f'<div class="bar"><div class="lab">{esc(i["label"])}</div><div class="track"><div class="fill" style="width:{w:.0f}%;background:{PAL[c][1]}">{esc(i["display"])}</div></div></div>'
    elif t == 'steps':
        out += '<div class="steps">' + ''.join(f'<div class="step">{ch_calendar(130, "open" if n == len(sec["items"]) - 1 else "smile")}<div class="t">{esc(i["title"])}</div><div class="s">{esc(i.get("sub",""))}</div></div>' for n, i in enumerate(sec['items'])) + '</div>'
        if sec.get('lead'): out += f'<div class="bubble" style="margin-top:22px">{esc(sec["lead"])}</div>'
    elif t == 'list':
        out += (f'<div class="row" style="align-items:flex-start">' + (f'<div style="flex:none;padding-top:8px">{chhtml}</div>' if chhtml else '') +
                '<ul class="lst" style="flex:1">' + ''.join(f'<li><b>{esc(i["head"])}</b><br>{esc(i["text"])}</li>' if isinstance(i, dict) else f'<li>{esc(i)}</li>' for i in sec['items']) + '</ul></div>')
    elif t == 'note':
        out += f'<div class="row">{chhtml}<div class="bubble" style="flex:1;background:{a}">{esc(sec["text"])}</div></div>'
    return out + '</div>'

def decos(n_seed, height):
    import random
    r = random.Random(n_seed); out = ''
    makers = [lambda: deco_star(r.randint(54, 78), r.choice(['#ffd96b', '#ffe38f'])), lambda: deco_heart(r.randint(40, 58), r.choice(['#ff9fb0', '#d9c4f5'])), lambda: deco_bubble(r.randint(30, 50))]
    for i in range(10):
        side = r.choice(['left', 'right'])
        out += f'<div class="deco" style="{side}:{r.randint(6, 26)}px;top:{r.randint(10, height)}px">{r.choice(makers)()}</div>'
    return out

def info_html(sp):
    t = sp['info_title']
    title = '<br>'.join(t['lines']).replace('[[', '<span class="hl">').replace(']]', '</span>').replace('{{', '<span class="hl2">').replace('}}', '</span>')
    body = ''.join(section(s) for s in sp['sections'])
    top = (f'<div class="deco" style="left:40px;top:40px">{deco_star(84)}</div><div class="deco" style="right:44px;top:34px">{deco_heart(70)}</div>'
           f'<div class="deco" style="left:70px;top:135px">{deco_bubble(38)}</div><div class="deco" style="right:70px;top:130px">{deco_star(60, "#ffe38f")}</div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="page">{top}'
            f'<h1>{title}</h1><div class="summary">{esc(sp["summary"])}<small>{esc(sp["source_line"])}</small></div>{body}'
            f'<div class="foot">{esc(sp["footer"]).replace(chr(10), "<br>")}</div><div class="brand">FTH · {esc(sp["site"])}</div></div></body></html>')

def cover_html(sp):
    c = sp['cover']
    title = '<br>'.join(c['lines']).replace('[[', '<span class="hl">').replace(']]', '</span>').replace('{{', '<span class="hl2">').replace('}}', '</span>')
    chars = ''.join(f'<div>{CHARS[x](190)}</div>' for x in c.get('characters', ['doctor', 'beam', 'patient']))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}'
            'body{height:1080px}.cv{position:relative;width:1080px;height:1080px;background:radial-gradient(circle at 50% 35%,#fffdf6 0,#fff3dc 60%,#ffe9cf 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px;overflow:hidden}'
            '.tag{background:#d4f2e6;border:5px solid ' + INK + ';border-radius:40px;padding:10px 34px;font-size:38px;margin-bottom:30px}'
            '.cv h1{font-size:76px;line-height:1.22;text-align:center}.sub{margin-top:26px;font-size:40px;background:#ffe1e6;border-radius:40px;padding:12px 36px}'
            '.chars{display:flex;gap:20px;align-items:flex-end;margin-top:26px}.badges{display:flex;gap:22px;margin-top:30px}.bd{border:5px solid '+INK+';border-radius:34px;padding:12px 28px;text-align:center}.bd b{display:block;font-weight:400;font-size:62px;line-height:1.05}.bd span{font-size:28px}.brand{position:absolute;bottom:34px;font-size:30px}</style></head><body><div class="cv">'
            f'<div class="deco" style="left:60px;top:70px">{deco_star(96)}</div><div class="deco" style="right:70px;top:80px">{deco_heart(80)}</div>'
            f'<div class="deco" style="left:90px;bottom:150px">{deco_bubble(56)}</div><div class="deco" style="right:90px;bottom:170px">{deco_star(70, "#ffe38f")}</div>'
            f'<div class="tag">{esc(c["tag"])}</div><h1>{title}</h1><div class="sub">{esc(c["sub"])}</div>'
            + ('<div class="badges">' + ''.join(f'<div class="bd" style="background:{PAL[col][0]}"><b>{esc(b["value"])}</b><span>{esc(b["label"])}</span></div>' for b, col in zip(c.get("badges", []), ["pink", "mint", "sky"])) + '</div>' if c.get("badges") else '')
            + f'<div class="chars">{chars}</div>'
            f'<div class="brand">FTH · {esc(sp["site"])}</div></div></body></html>')

# ---------- 메타데이터(EXIF·XMP) ----------
def xmp_packet(m):
    e = lambda s: html.escape(str(s), quote=False)
    subj = ''.join(f'<rdf:li>{e(k)}</rdf:li>' for k in m['keywords'])
    return ('<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
            '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">'
            f'<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{e(m["title"])}</rdf:li></rdf:Alt></dc:title>'
            f'<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{e(m["description"])}</rdf:li></rdf:Alt></dc:description>'
            f'<dc:creator><rdf:Seq><rdf:li>{e(m["creator"])}</rdf:li></rdf:Seq></dc:creator>'
            f'<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{e(m["rights"])}</rdf:li></rdf:Alt></dc:rights>'
            f'<dc:subject><rdf:Bag>{subj}</rdf:Bag></dc:subject>'
            f'<photoshop:Credit>{e(m["creator"])}</photoshop:Credit><photoshop:Source>{e(m["source"])}</photoshop:Source>'
            f'<Iptc4xmpCore:AltTextAccessibility><rdf:Alt><rdf:li xml:lang="x-default">{e(m["alt"])}</rdf:li></rdf:Alt></Iptc4xmpCore:AltTextAccessibility>'
            '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>')

def save_jpeg(png, out, m):
    from PIL import Image
    im = Image.open(png).convert('RGB')
    ex = Image.Exif()
    u16 = lambda s: (str(s) + '\0').encode('utf-16le')
    ex[0x010e] = m['title'].encode('utf-8')           # ImageDescription
    ex[0x013b] = m['creator'].encode('utf-8')         # Artist
    ex[0x8298] = m['rights'].encode('utf-8')          # Copyright
    ex[0x0131] = 'FTH naver_card.py'  # Software
    ex[0x0132] = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    ex[0x9c9b] = u16(m['title'])      # XPTitle
    ex[0x9c9c] = u16(m['description'])  # XPComment
    ex[0x9c9d] = u16(m['creator'])    # XPAuthor
    ex[0x9c9e] = u16(';'.join(m['keywords']))  # XPKeywords
    ex[0x9c9f] = u16(m['alt'])        # XPSubject
    im.save(out, 'JPEG', quality=90, optimize=True, exif=ex, xmp=xmp_packet(m).encode('utf-8'))

async def render(htmlstr, png, w, h=None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(**({'executable_path': os.environ['CHROME_PATH'], 'args': ['--no-sandbox']} if os.environ.get('CHROME_PATH') else {}))
        pg = await b.new_page(viewport={'width': w, 'height': h or 1000}, device_scale_factor=1)
        tmp = png + '.html'; open(tmp, 'w', encoding='utf-8').write(htmlstr)
        await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=png, full_page=h is None)
        await b.close(); os.remove(tmp)

def main(spec, outdir):
    sp = json.load(open(spec, encoding='utf-8')); outdir = os.path.abspath(outdir); os.makedirs(outdir, exist_ok=True)
    s = sp['slug']; meta = sp['meta']
    for kind, h, fn in (('cover', 1080, cover_html), ('info', None, info_html)):
        png = os.path.join(outdir, f'{s}-naver-{kind}.png')
        asyncio.run(render(fn(sp), png, 1080, h))
        m = dict(meta, title=meta['title'] + (' — 대표 그림' if kind == 'cover' else ' — 한눈에 보기'), alt=meta['alt_' + kind])
        name = sp.get('file_ko', s) + ('-대표그림' if kind == 'cover' else '-한눈에보기') + '.jpg'
        save_jpeg(png, os.path.join(outdir, name), m); os.remove(png)
        print('ok', os.path.join(outdir, name))

if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
