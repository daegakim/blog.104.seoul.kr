#!/usr/bin/env python3
"""블로거 글 꾸미기 — 단순 HTML 원고(post.html)를 인라인 스타일이 들어간 고급형 HTML로 바꾼다.
블로거 '이메일로 게시'는 <style>을 지울 수 있어 모든 꾸밈을 style 속성으로 넣는다.

사용: python3 tools/style_post.py post.html styled.html <원본 사이트: 114.pe.kr|109.co.kr|ivr.kr|104.seoul.kr>
  글 끝(안내문 앞)에 '일본 치료 준비 안내' 상자(모든 글 같은 내용) + FTH 문의 상자(원본 사이트 문의하기·전화 02-517-5117·세 사이트 링크)를 자동으로 넣는다.
원고 규칙(post.html):
  첫 <p class="lead"> = 요약 상자, <h2> = 질문형 소제목, <table> = 표, <h3>+<p> = 자주 묻는 질문,
  <h2>출처</h2><ul>…</ul> = 출처, <p class="more"><a href=…>…</a></p> = 자세히 보기 버튼,
  <p class="note"> = 일반 정보 안내, <img> = 그림(가로 100%·둥근 모서리).
"""
import re, sys

INK = '#22313f'; TEAL = '#2a8c82'; NAVY = '#1d3b53'
WRAP = ("font-family:'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif;font-size:17px;line-height:1.85;"
        f"color:{INK};word-break:keep-all;overflow-wrap:break-word;letter-spacing:-0.2px")
S = {
    'p': 'margin:0 0 18px',
    'lead': f'margin:22px 0 30px;padding:20px 22px;background:#f1f7f6;border-left:5px solid {TEAL};border-radius:14px;font-size:17.5px;line-height:1.8',
    'h2': f'margin:46px 0 16px;padding:0 0 10px 14px;border-left:6px solid {TEAL};border-bottom:1px solid #e3eaee;font-size:22px;line-height:1.45;font-weight:700;color:{NAVY}',
    'img': 'display:block;width:100%;max-width:100%;height:auto;margin:26px auto;border-radius:18px;box-shadow:0 6px 20px rgba(30,50,70,.10)',
    'tablewrap': 'margin:10px 0 28px;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:14px;border:1px solid #dfe7ec',
    'table': 'width:100%;min-width:480px;border-collapse:collapse;font-size:16px;line-height:1.6;background:#fff',
    'th': f'background:{NAVY};color:#fff;font-weight:700;padding:13px 12px;text-align:center;white-space:nowrap',
    'td': 'padding:13px 12px;border-top:1px solid #e8eef1;text-align:center;vertical-align:middle',
    'tdfirst': f'padding:13px 12px;border-top:1px solid #e8eef1;text-align:left;font-weight:700;color:{NAVY};white-space:nowrap',
    'num': f'color:{TEAL};font-weight:700',
    'faqbox': 'margin:14px 0;padding:18px 20px;background:#fff8ec;border:1px solid #f0e2c6;border-radius:14px',
    'faqq': f'margin:0 0 8px;font-size:17.5px;font-weight:700;color:{NAVY}',
    'faqa': 'margin:0;font-size:16.5px',
    'qmark': '#e0703e',
    'src': 'margin:0;padding:18px 20px 18px 38px;background:#f7f9fa;border-radius:14px;font-size:14.5px;line-height:1.75;color:#55606a',
    'srcli': 'margin:0 0 6px',
    'more': 'margin:34px 0 20px;text-align:center',
    'btn': f'display:inline-block;padding:14px 28px;background:{TEAL};color:#fff;border-radius:999px;text-decoration:none;font-weight:700;font-size:16.5px;box-shadow:0 4px 12px rgba(42,140,130,.25)',
    'note': 'margin:26px 0 0;padding:14px 16px;border-top:1px solid #e3eaee;font-size:13.5px;line-height:1.7;color:#7a858f',
    'a': f'color:{TEAL};text-decoration:underline',
}

def style_table(m):
    t = m.group(0)
    t = re.sub(r'<table[^>]*>', f'<table style="{S["table"]}">', t)
    t = re.sub(r'<th>', f'<th style="{S["th"]}">', t)
    rows = re.findall(r'<tr>.*?</tr>', t, re.S)
    for i, r in enumerate(re.findall(r'<tbody>.*?</tbody>', t, re.S)[0:1]):
        new = r; n = 0
        for row in re.findall(r'<tr>.*?</tr>', r, re.S):
            bg = '#ffffff' if n % 2 == 0 else '#f7fafb'; n += 1
            cells = re.findall(r'<td>(.*?)</td>', row, re.S)
            out = f'<tr style="background:{bg}">'
            for j, c in enumerate(cells):
                if j == 0: out += f'<td style="{S["tdfirst"]}">{c}</td>'
                else:
                    c2 = re.sub(r'^([0-9][0-9.,]*%?)', rf'<span style="{S["num"]}">\1</span>', c)
                    out += f'<td style="{S["td"]}">{c2}</td>'
            new = new.replace(row, out + '</tr>', 1)
        t = t.replace(r, new)
    return f'<div style="{S["tablewrap"]}">{t}</div>'

SITES = {'114.pe.kr': '일본 중입자치료 정보', '109.co.kr': '일본 의료정보', 'ivr.kr': 'IVR·고주파 열치료(RFA) 정보'}

def contact_box(site):
    site = site if site in SITES else '114.pe.kr'
    links = ' · '.join(f'<a href="https://{d}/kr/" style="color:#cfe9e5;text-decoration:underline">{d}</a> {n}' for d, n in SITES.items())
    btn = 'display:inline-block;margin:6px 4px;padding:13px 24px;border-radius:999px;text-decoration:none;font-weight:700;font-size:16.5px'
    return (f'<div style="margin:36px 0 10px;padding:26px 22px;background:{NAVY};border-radius:18px;text-align:center;color:#fff">'
            '<p style="margin:0 0 6px;font-size:20px;font-weight:700;color:#fff">일본 의료기관 정보문의</p>'
            '<p style="margin:0 0 16px;font-size:15.5px;line-height:1.7;color:#dfe8ee">일본 병원 치료 가능 여부, 비용, 준비 서류를 안내해 드립니다.</p>'
            f'<a href="https://{site}/kr/contact/" style="{btn};background:#fff;color:{NAVY}">문의하기 →</a>'
            f'<a href="tel:025175117" style="{btn};background:{TEAL};color:#fff">전화 02-517-5117</a>'
            f'<p style="margin:16px 0 0;font-size:13.5px;line-height:1.8;color:#cfe9e5">{links}</p></div>')

def guide_box():
    """모든 글 공통 '일본 치료 준비 안내' 상자 (사용자 지정 2026-10-29: 실무 정보는 매번 같은 짧은 상자로)."""
    step = ('display:inline-block;width:26px;height:26px;margin-right:8px;border-radius:50%;background:#4EBA91;color:#fff;'
            'font-weight:700;font-size:14px;line-height:26px;text-align:center;vertical-align:middle')
    li = 'margin:0 0 8px;font-size:16px;line-height:1.6'
    links = [('https://ivr.kr/kr/blog/papers/', 'IVR·RFA 최신 논문 (ivr.kr)'),
             ('https://ivr.kr/kr/blog/ivr-rfa/', 'IVR·RFA 신기술 (ivr.kr)'),
             ('https://109.co.kr/kr/blog/interpreter/interpreter-prep/', '현지 통역 준비 (109.co.kr)')]
    a = 'display:inline-block;margin:4px 6px 0 0;padding:9px 16px;border-radius:999px;border:1px solid #9fd3c3;background:#fff;color:#1d3b53;text-decoration:none;font-weight:700;font-size:14.5px'
    steps = ['진단 자료 준비', '일본어 번역·의료기관 문의', '답변 안내·현지 통역']
    return (f'<div style="margin:36px 0 0;padding:22px 22px 18px;background:#f1f7f6;border:1px solid #d3e8e2;border-radius:18px">'
            f'<p style="margin:0 0 12px;font-size:18.5px;font-weight:700;color:{NAVY}">일본 치료 준비 안내</p>'
            + ''.join(f'<p style="{li}"><span style="{step}">{i+1}</span>{t}</p>' for i, t in enumerate(steps)) +
            '<p style="margin:10px 0 6px;font-size:14.5px;line-height:1.7;color:#55606a">영상 CD 원본, 병리 결과, 최근 혈액검사, 치료 경과 기록을 준비하면 일본 의료기관 검토가 빨라집니다. 치료 여부는 일본 의료진이 진료 자료를 보고 판단합니다.</p>'
            + ''.join(f'<a href="{u}" style="{a}">{t} →</a>' for u, t in links) + '</div>')

# 104.seoul.kr 전용 블로거(다른 구글 아이디, 사용자 지정 2026-10-29) — FTH 일본 암치료 상자 대신 줄기세포 문의 상자만
S104_CONTACT = 'https://104.seoul.kr/kr/contact/'  # 첫 실행에서 daegakim/104 저장소로 실제 문의 페이지 주소를 확인해 고친다

def contact_box_104():
    btn = 'display:inline-block;margin:6px 4px;padding:13px 24px;border-radius:999px;text-decoration:none;font-weight:700;font-size:16.5px'
    return (f'<div style="margin:36px 0 10px;padding:26px 22px;background:{NAVY};border-radius:18px;text-align:center;color:#fff">'
            '<p style="margin:0 0 6px;font-size:20px;font-weight:700;color:#fff">일본 줄기세포 치료 정보문의</p>'
            '<p style="margin:0 0 16px;font-size:15.5px;line-height:1.7;color:#dfe8ee">일본 의료기관의 줄기세포 치료 정보와 진행 절차를 안내해 드립니다.</p>'
            f'<a href="{S104_CONTACT}" style="{btn};background:#fff;color:{NAVY}">문의하기 →</a>'
            f'<a href="tel:025175117" style="{btn};background:{TEAL};color:#fff">전화 02-517-5117</a>'
            '<p style="margin:16px 0 0;font-size:13.5px;line-height:1.8;color:#cfe9e5"><a href="https://104.seoul.kr/kr/" style="color:#cfe9e5;text-decoration:underline">104.seoul.kr</a> 일본 줄기세포 연구정보</p></div>')

def main(src, dst, site='114.pe.kr'):
    h = open(src, encoding='utf-8').read()
    h = re.sub(r'<p>\s*(<img[^>]*?)\s*/?>\s*</p>', r'\1>', h)
    h = re.sub(r'<img ([^>]*?)(?:width="[^"]*"\s*)?(?:height="[^"]*"\s*)?/?>', lambda m: '<img ' + re.sub(r'\s*(width|height|style)="[^"]*"', '', m.group(1)).strip() + f' style="{S["img"]}">', h)
    h = re.sub(r'<p class="lead">', f'<p style="{S["lead"]}">', h)
    # 첫 문단이 lead 클래스가 없으면 첫 <p>를 요약 상자로
    if S['lead'] not in h:
        h = h.replace('<p>', f'<p style="{S["lead"]}">', 1)
    h = re.sub(r'<table.*?</table>', style_table, h, flags=re.S)
    # 출처
    h = re.sub(r'<h2>출처</h2>\s*<ul>(.*?)</ul>', lambda m: f'<h2>출처</h2><ul style="{S["src"]}">' + m.group(1).replace('<li>', f'<li style="{S["srcli"]}">') + '</ul>', h, flags=re.S)
    # 자주 묻는 질문: h3 + p 묶음을 카드로
    h = re.sub(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', lambda m: f'<div style="{S["faqbox"]}"><p style="{S["faqq"]}"><span style="color:{S["qmark"]}">Q.</span> {m.group(1)}</p><p style="{S["faqa"]}">{m.group(2)}</p></div>', h, flags=re.S)
    # 자세히 보기 버튼
    h = re.sub(r'<p class="more">\s*<a href="([^"]+)">(.*?)</a>\s*</p>', lambda m: f'<p style="{S["more"]}"><a href="{m.group(1)}" style="{S["btn"]}">{m.group(2)} →</a></p>', h, flags=re.S)
    h = re.sub(r'<p class="note">(?:<small>)?(.*?)(?:</small>)?</p>', lambda m: f'<p style="{S["note"]}">{m.group(1)}</p>', h, flags=re.S)
    h = h.replace('<h2>', f'<h2 style="{S["h2"]}">')
    h = h.replace('<p>', f'<p style="{S["p"]}">')
    h = re.sub(r'<a href="([^"]+)">', rf'<a href="\1" style="{S["a"]}">', h)
    h = re.sub(r'<b>', f'<b style="color:{NAVY}">', h)
    box = contact_box_104() if site == '104.seoul.kr' else guide_box() + contact_box(site)
    h = re.sub(r'(<p style="margin:26px 0 0;padding:14px 16px)', box.replace('\\', '\\\\') + r'\1', h, count=1) if 'margin:26px 0 0;padding:14px 16px' in h else h + box
    out = f'<div style="{WRAP}">\n{h.strip()}\n</div>'
    open(dst, 'w', encoding='utf-8').write(out)
    print('ok', dst, len(out))

if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '114.pe.kr')
