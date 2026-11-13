# 104 전용 구글 블로거 — 하루 2편 자동 발행 (사용자 지정 2026-10-29: 1편 → 2편, 오전 10:13·저녁 21:13)
- 블로그: 대표님의 **다른 구글 아이디**에 만든 블로거(주소는 대표님이 알려 주면 여기에 적는다: `BLOG_URL = https://we-1st.blogspot.com/ → 맞춤 도메인 https://blog.104.seoul.kr/ 연결됨(2026-10-29, DNS CNAME 2개 Hostinger)`).
- 주제: `_ops/topics.md` — 오전은 기초·제도·승인 현황, 저녁은 104.seoul.kr처럼 질환별 해외 최신 연구(단 사이트에 쓴 같은 연구는 쓰지 않음). 사이트 글 목록은 GitHub `daegakim/104`의 `_ops/published.md`·`_ops/keywords.md`로 확인(읽기만, 수정·push 금지).
- 발행: 지금 계정(fthvht@gmail.com) Apps Script에 `_ops/publish104.gs`를 추가(새 블로그 '이메일로 게시' 주소는 대표님이 직접 넣음). Drive `seoul104_queue`(id 1VZJFP42mKCPTjxh6bTRRpDhXJC6nfsTT) → 발행 뒤 `seoul104_published`(id 18lI2fptZWdA12ZiTGjsyolJOk-o_t6fj, 파일 설명에 '메일 발행 시각').
- queue에 3시간 넘게 남은 파일이 있으면 발행이 멈춘 것이므로 새 글을 만들지 않고 보고만 한다(Apps Script publish104.gs·주소·setup104 확인).

## ★ 2026-11-13 대표님 지시 — 발행 전 품질 게이트 (이 파일의 다른 규칙보다 우선)
대표님: "네이버 이외 우리 전체 사이트는 품질 진단 사이트 구글 기준 95점 이상일 때 발행", "우리는 이미지가 부족한 것 같다."
1. 저장소 daegakim/geo-quality를 준비한다(세션에 없으면 add_repo(owner=daegakim, repo=geo-quality, access=push) 후 clone, 있으면 git pull). 루트의 GATE.md를 처음부터 끝까지 읽고 그대로 따른다.
2. 그림: 대표그림·한눈에보기 2장에 더해 본문 그림을 늘려 **본문 이미지 3장 이상**, 모두 내용을 설명하는 alt. 게이트 결과의 상위 글 이미지 대표값보다 적으면 더 넣는다(naver_card.py 등 저장소 도구).
3. queue.json을 Drive seoul104_queue에 저장(=발행 예약)하기 **전에**, styled.html을 geo-quality `queue/blog104-YYYYMMDD-am|pm-<짧은영문슬러그>.html`(+ 같은 이름 .json: keyword, base_url "https://blog.104.seoul.kr/", platform "blogger", engine "google", threshold 95, source_urls)로 올리고 `queue-results/`의 결과를 기다린다. 그림이 먼저 공개되도록 이 저장소 push는 게이트 전에 해도 된다.
4. pass(Google Q 95 이상)일 때만 queue.json을 Drive에 저장한다. 95 미만이면 **보류하지 않고** 결과(fix·short·paragraphs)대로 고쳐 -r2, -r3, … 로 다시 올리기를 95점 이상이 될 때까지 횟수 제한 없이 되풀이한다(GATE.md 3절, 대표님 지시 2026-11-13 "몇 번이고 수정해서 95점 이상"). 게이트 오류·결과 지연이면 기다렸다 다시 올린다. 이번 실행 안에 끝나지 않으면 geo-quality `queue/<이름>.progress.md`에 남기고 다음 실행 때 새 글보다 먼저 이어서 고친다.
5. 알림에 Google 품질 지수와 report_url을 함께 적는다.

## 글 규칙
- 104 저장소 `CLAUDE.md`(글쓰기 기준·의료법)를 읽고 따른다. 한국 사이트 자료 금지, 해외 공식 기관(후생노동성·PMDA·FDA·EMA·ISSCR)·논문 원문만. 확인할 수 없는 내용은 쓰지 않는다.
- 사람 대상 결과는 연구 단계(승인/임상시험 몇 상)를 분명히, 희망적이지만 정확하게. 효과 보장·완치·최고·유일 금지, 환자 후기 금지, '상담' 금지(→ 문의, 정보 안내), 물결표·번역투·겹말 0, 일본어 표기 쓰지 않음.
- 구성·디자인은 fthco 블로거와 같다(`_ops/style-guide.md`의 글 규칙·꾸미기): 질문형, 1,500–2,000자(공백 제외), lead·h2 4–5개·표 1개·h3 FAQ 3개·출처 3–4개·`class="more"`(가장 가까운 104.seoul.kr 글, 없으면 https://104.seoul.kr/kr/)·note.
- 유사성: 자세히 보기로 연결한 104.seoul.kr 글(저장소 파일)과 `python3 tools/similarity.py` 0.15 미만.
- 꾸미기: `python3 tools/style_post.py post.html styled.html 104.seoul.kr` (FTH 일본 암치료 상자 대신 '일본 줄기세포 치료 정보문의' 상자). **첫 실행 때** 104 저장소에서 실제 문의 페이지 주소를 찾아 style_post.py의 `S104_CONTACT`가 맞는지 확인·수정한다.
- 그림: `python3 tools/naver_card.py`로 대표그림·한눈에보기 2장(file_ko 한국어, site "104.seoul.kr", meta.creator "FTH 에프티에이치 (104.seoul.kr)") → Read로 확인 → `images/s104-YYYY-MM-DD-am|pm-cover.jpg`·`-info.jpg`로 복사(index.json에는 넣지 않음).
- 폴더: `posts/YYYY-MM-DD-am|pm/`(post.html·post.txt·spec.json·styled.html·queue.json·그림). 이미 있으면 다시 만들지 않는다.

## 전달
- queue.json = {"key":"s104-YYYY-MM-DD-am|pm","title"(45자 이하),"labels","images"[그림 주소 2개(`https://raw.githubusercontent.com/daegakim/blog.104.seoul.kr/main/images/s104-YYYY-MM-DD-am|pm-cover.jpg`·`-info.jpg`)],"source"(자세히 보기),"content"(styled.html)} → Drive seoul104_queue에 create_file(application/json, disableConversionToGoogleType true, 이름 `s104-YYYY-MM-DD-am|pm.json`).
- 다음 실행에서 seoul104_published에 지난 글이 옮겨졌는지 확인. queue에 3시간 넘게 남은 파일이 있으면 '발행 안 됨'으로 보고(원인: Apps Script에 publish104.gs·주소를 아직 안 넣었거나 setup104 미실행).

## 실행 환경 메모 (클라우드)
- 그림 생성: `CHROME_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome /usr/bin/python3.13 tools/naver_card.py spec.json 폴더` (playwright는 python3.13에 설치됨). 유사성 검사는 `python3 tools/similarity.py`.
