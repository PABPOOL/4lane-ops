# 운영 웹앱 화면(자동신청.gs의 APP_HTML)을 github.io 페이지(index.html)로 만든다. 2026-10-30
# script.google.com 위에서 열면 맨 위에 구글 회색 안내 띠가 붙는다 → 화면은 여기서 그리고, 데이터만 팀용 배포(doPost 'ops')에 관리자 키로 묻는다.
# 화면 코드를 고치면: python3 build_ops.py → git push. 서버 코드는 전처럼 편집기에 붙여넣고 배포 두 개 새 버전.
# 키가 없으면 안내 + 예전 웹앱 링크. manifest는 넣지 않는다(아이폰이 홈 화면 시작 주소를 키 없는 주소로 잡음).
import pathlib
here = pathlib.Path(__file__).parent
gs = (here.parent / 'apps_script' / '자동신청.gs').read_text()
html = gs[gs.index('String.raw`') + 11:gs.rindex('`;')]
team = (here / 'team.html').read_text()
api = team.split("var API = '", 1)[1].split("'", 1)[0]  # 팀원용 배포(액세스: 모든 사용자) 주소. team.html과 같은 것

head = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>4LANE OPS</title>
<meta name="robots" content="noindex, nofollow">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="4LANE OPS">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<link rel="apple-touch-icon" href="apple-touch-icon.png?v=3">
<link rel="icon" type="image/png" href="icon_salane_192.png?v=3">
<script>
// 관리자 키: ?p=키로 한 번 열면 이 기기에 기억(홈 화면 앱은 사파리와 저장소가 따로라 주소의 키가 기준)
var OPS_API = '%s';
var OPS_URL = 'https://script.google.com/macros/s/AKfycbzF59Jy6CBq9xRus5EGmIFu-6Utbj4C2J2E3amJDA61Qp1PvNTqYhPZoFPJc8J7T1xYeg/exec';
var OPS_KEY = (location.search.match(/[?&]p=([^&]+)/) || [])[1] || '';
try { if (OPS_KEY) localStorage.setItem('ops-key', OPS_KEY); else OPS_KEY = localStorage.getItem('ops-key') || ''; } catch (e) {}
if (!OPS_KEY) document.addEventListener('DOMContentLoaded', function () {  // 키 없이 열림 → 조용히 구글로 넘기지 않고 알려준다
  document.body.innerHTML = '<div style="padding:60px 24px;text-align:center;font-family:Arial;color:#8EA1BC;line-height:1.7">'
    + '관리자 링크(?p=키)로 열어주세요.<br>홈 화면 아이콘은 그 링크를 사파리에서 연 화면에서 추가해야 해요.<br><br>'
    + '<a href="' + OPS_URL + '" style="color:#38D3EE">예전 웹앱으로 열기</a></div>';
});
// google.script.run 흉내: 같은 함수 이름을 doPost 'ops'로 보낸다
(function () {
  function runner(ok, fail) {
    return new Proxy({}, { get: function (_, k) {
      if (k === 'withSuccessHandler') return function (f) { return runner(f, fail); };
      if (k === 'withFailureHandler') return function (f) { return runner(ok, f); };
      return function () {
        var args = Array.prototype.slice.call(arguments);
        fetch(OPS_API, { method: 'POST', body: JSON.stringify({ p: OPS_KEY, op: 'ops', fn: k, args: args }) })  // 문자열 본문 = 사전 확인 요청 없음
          .then(function (r) { return r.json(); })
          .then(function (j) { if (j.ok) { ok && ok(j.data); } else if (fail) fail(new Error(j.error)); })
          .catch(function (e) { fail && fail(new Error('연결이 안 돼요. 잠깐 뒤 ⟳을 눌러주세요')); });
      };
    } });
  }
  window.google = { script: { run: runner(null, null) } };
})();
</script>""" % api

html = html.replace('<base target="_top"><meta charset="utf-8">', head, 1)
assert 'OPS_API' in html, 'APP_HTML 머리 부분이 바뀌었어요'
(here / 'index.html').write_text(html)
print('index.html 만듦 (API = ' + api[-20:] + ')')
