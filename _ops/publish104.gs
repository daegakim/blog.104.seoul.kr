/**
 * 104.seoul.kr 전용 구글 블로거 자동 발행 (사용자 지정 2026-10-29)
 * - 지금 쓰는 Apps Script 프로젝트(fthvht@gmail.com, drive-image-sync.gs가 있는 곳)에 '파일 추가'로 이 파일을 새로 넣는다.
 * - 블로그는 다른 구글 아이디에 있어도 된다: 그 블로그의 '이메일로 게시' 비밀 주소로 메일을 보내면 발행된다.
 * - POST_EMAIL_104에 새 블로그의 비밀 주소를 넣고 setup104를 한 번 실행한다(기존 setup은 다시 실행하지 않아도 됨).
 *   기존 setup()을 다시 실행하면 이 예약도 지워지므로, 그때는 setup104도 다시 실행한다.
 */
var QUEUE_ID_104 = '1VZJFP42mKCPTjxh6bTRRpDhXJC6nfsTT';   // Drive seoul104_queue
var DONE_ID_104 = '18lI2fptZWdA12ZiTGjsyolJOk-o_t6fj';    // Drive seoul104_published
var POST_EMAIL_104 = '여기에_새_블로그_메일_주소';          // 새 블로그 설정 > 이메일 > 이메일을 사용하여 게시 (비공개)

function setup104() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'publish104') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('publish104').timeBased().everyHours(1).create();
  publish104();
}

function publish104() {
  if (POST_EMAIL_104.indexOf('@blogger.com') < 0) { console.log('POST_EMAIL_104를 먼저 넣어 주세요'); return; }
  var files = DriveApp.getFolderById(QUEUE_ID_104).getFiles(), done = DriveApp.getFolderById(DONE_ID_104);
  var sent = 0;
  while (files.hasNext() && sent < 1) {            // 한 번에 1편만(하루 1편 유지)
    var f = files.next();
    var d = JSON.parse(f.getBlob().getDataAsString('UTF-8'));
    var ready = (d.images || []).every(function (u) { return UrlFetchApp.fetch(u, { muteHttpExceptions: true }).getResponseCode() === 200; });
    if (!ready) { console.log('그림이 아직 없음, 다음 시간에: ' + d.title); continue; }
    MailApp.sendEmail({ to: POST_EMAIL_104, subject: d.title, htmlBody: d.content, name: '104' });
    f.setDescription('메일 발행 ' + new Date().toISOString());
    f.moveTo(done);
    sent++;
    console.log('발행: ' + d.title);
  }
}
