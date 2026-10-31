# 구글 블로거 자동 발행 — 하루 2편 (사용자 지정 2026-10-26, 주제 방식 변경 2026-10-29)
블로그: https://fthco.blogspot.com/ (일본 암치료 정보센터). 세 사이트에 **없는 주제**를 새로 조사해 써서 자동 발행한다(topics.md, 네이버와 다른 주제). 발행은 대표님 계정의 Apps Script(`_ops/naver/drive-image-sync.gs`의 publishBlogger, 1시간마다)가 블로거 '이메일로 게시' 비밀 주소로 메일을 보내 한다(Blogger API는 기본 GCP 프로젝트 권한 문제로 쓰지 않음). 라벨은 메일 발행에서 붙지 않는다.

## 주제 (사용자 지정 2026-10-29 — 사이트 글 요약 중단)
- 세 사이트 글을 요약하지 않는다. `_ops/blogger/topics.md` 규칙대로 사이트에 없는 주제를 하나 골라 **새로 조사해서** 쓴다(WebSearch·WebFetch로 일본 정부·병원·학회·해외 논문 원문 확인. 한국 사이트 자료 금지. 자사 세 사이트는 WebFetch로 열지 않고 저장소 파일로 확인).
- 네이버와 같은 실행에서 다른 칸의 주제를 쓴다(위 '주제' 참고).
- 폴더 `posts/YYYY-MM-DD-am|pm/`가 이미 있으면 다시 만들지 않는다. 예시: `_ops/blogger/2026-10-26-am/`(형식만 참고).
- '▶ 자세히 보기'는 주제와 가장 가까운 세 사이트 글(없으면 그 사이트 첫 화면 /kr/) 1개. style_post.py의 사이트 인자는 그 링크의 도메인.

## 글 규칙
- 질문형 구성: 요약 첫 문단(핵심 검색어·핵심 숫자) → 질문형 h2 4–5개 → 표 1개 → 자주 묻는 질문(h3) 3개 → 출처(원문 링크 3–4개) → '▶ 자세히 보기' 원본 사이트 글 링크 1개 → 일반 정보 안내.
- 한국어 1,500–2,000자(공백 제외). `python3 tools/similarity.py post.txt --compare <자세히 보기로 연결한 사이트 글이 든 폴더>` 0.15 미만(그 글 HTML을 임시 폴더에 index.html로 복사해 비교). 숫자·승인 여부·연도는 원문 그대로, 출처 3–4개 모두 직접 확인한 원문.
- 네이버 글 규칙(‘상담’ 금지, 의료법, 희망적·정확, 한국 자료 금지, 물결표·번역투 0)을 똑같이 지킨다. 문의 연락처는 style_post.py의 '일본 치료 준비 안내' 상자(모든 글 같은 내용, 사용자 지정 2026-10-29)와 '일본 의료기관 정보문의' 상자가 모든 글(109·ivr 포함)에 넣는다 — 본문에 따로 쓰지 않는다.
- 그림: `naver_card.py`로 대표그림·한눈에보기(네이버와 다른 문구·구성) → Read로 확인 → `images/s104-YYYY-MM-DD-am|pm-cover.jpg`, `-info.jpg`로 복사·커밋·push. 본문 맨 위에 대표그림, 중간에 한눈에보기 `<img src="https://raw.githubusercontent.com/daegakim/blog.104.seoul.kr/main/images/s104-YYYY-MM-DD-am|pm-cover.jpg" alt="...">`.
- 제목 45자 이하, 핵심 검색어로 시작. 라벨 3–5개.
- 블로그 시간대는 대표님이 (GMT+09:00) 서울로 설정(2026-10-29). 블로그 바닥글·떠 있는 전화/카카오톡 버튼·사이드바 회사 정보는 블로그 레이아웃(가젯) 몫이므로 글 HTML에는 넣지 않는다.

## 꾸미기 (사용자 지정 2026-10-26: 글자가 작고 표가 왼쪽으로 쏠리는 문제)
- post.html은 `<p class="lead">`(첫 요약), `<h2>`, `<table>`(thead/tbody, 속성 없이), `<h3>`+`<p>`(자주 묻는 질문), `<h2>출처</h2><ul>`, `<p class="more"><a href=원본>자세히 보기 문구</a></p>`, `<p class="note">`(안내)로 쓴다.
- `python3 tools/style_post.py post.html styled.html <원본 사이트 도메인>`(글 끝에 '일본 의료기관 정보문의' 상자: 원본 사이트 문의하기·전화 02-517-5117·세 사이트 링크 자동 — 사용자 지정 2026-10-26, 블로거는 109·ivr 글도 넣음) → 인라인 스타일(본문 17px·줄간격 1.85·표 전체 폭·FAQ 카드·버튼) → queue.json의 content는 **styled.html**. 로컬 미리보기(560px·390px)를 Playwright로 찍어 확인.

## 전달
- `queue.json` = {"key","title","labels","images"[그림 주소 2개],"source","content"(HTML)} → Google Drive `blogger_queue` 폴더(id 1tPm57dCxTHFdc7q5d3-SiBpi5E_YUlKw)에 create_file(contentMimeType `application/json`, disableConversionToGoogleType true, 이름 `YYYY-MM-DD-am|pm.json`).
- Apps Script가 그림 주소가 열리는 것을 확인한 뒤 발행하고 파일을 `blogger_published`(id 1Da354_9H1W4EFGUqnkndXDm-EaXzz6MT)로 옮긴다(파일 설명에 '메일 발행 시각').
- 다음 실행 때 `blogger_published`에서 지난 글이 옮겨졌는지(설명의 메일 발행 시각) 확인해 보고에 넣는다. queue에 3시간 넘게 남은 파일이 있으면 발행 실패로 보고.
