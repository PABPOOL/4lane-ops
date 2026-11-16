// 안드로이드 '앱 설치'(주소창 없이 열기)용. 캐시는 하지 않고 그대로 통과시킨다(2026-11-16)
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
