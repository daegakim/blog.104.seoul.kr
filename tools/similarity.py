#!/usr/bin/env python3
"""유사성 검토 — 새 글이 (1) 원문을 베끼지 않았는지, (2) 내 사이트들의 기존 글과 겹치지 않는지 확인.

사용: python3 tools/similarity.py <새글.txt> [--source 원문.txt ...] [--compare 폴더 ...]
  새글.txt   : 새 글 한국어 본문(태그 없는 텍스트)
  --source   : 참고한 원문을 텍스트로 저장한 파일(여러 개 가능). 번역·요약 글이므로 문장 단위 그대로 옮긴 비율을 본다.
  --compare  : 기존 글 HTML/JS가 있는 폴더(예: kr/blog  ../fth-japan-medical/kr/blog). 하위 index.html·.js 전부 비교.
판정(문자 5-gram 기준):
  원문 대비 포함률 ≥ 0.15  → FAIL (문장을 너무 그대로 옮김: 다시 풀어 쓰기)
  기존 글 대비 유사도 ≥ 0.30 → FAIL (같은 내용 중복: 주제·관점 바꾸기)
  기존 글 대비 0.15~0.30     → WARN (일부 겹침: 겹치는 문단을 다르게 쓰기)
종료코드 0=통과, 1=FAIL
"""
import sys, re, os, glob, html

def text_of(path):
    s = open(path, encoding='utf-8', errors='ignore').read()
    if path.endswith(('.html', '.htm')):
        m = re.search(r'<article[^>]*>(.*?)</article>', s, re.S)
        s = m.group(1) if m else s
        s = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S)
        s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    return s

def grams(s, n=5):
    s = re.sub(r'\s+', '', s.lower())
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}

def main(a):
    new = a[0]; src = []; cmp = []; cur = None
    for x in a[1:]:
        if x in ('--source', '--compare'): cur = x; continue
        (src if cur == '--source' else cmp).append(x)
    g = grams(text_of(new)); fail = False
    if not g: print('빈 글'); return 1
    for f in src:
        c = len(g & grams(text_of(f))) / len(g)
        st = 'FAIL' if c >= 0.15 else 'OK'; fail |= st == 'FAIL'
        print(f'[원문] {st} 포함률 {c:.2f}  {f}')
    files = []
    for d in cmp:
        files += glob.glob(os.path.join(d, '**', 'index.html'), recursive=True) + glob.glob(os.path.join(d, '**', '*.js'), recursive=True)
    worst = []
    for f in files:
        if os.path.abspath(f) == os.path.abspath(new): continue
        h = grams(text_of(f))
        if not h: continue
        j = len(g & h) / len(g | h); worst.append((j, f))
    for j, f in sorted(worst, reverse=True)[:5]:
        st = 'FAIL' if j >= 0.30 else 'WARN' if j >= 0.15 else 'OK'; fail |= st == 'FAIL'
        print(f'[기존글] {st} 유사도 {j:.2f}  {f}')
    print('결과:', 'FAIL' if fail else 'PASS')
    return 1 if fail else 0

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(0)
    sys.exit(main(sys.argv[1:]))
