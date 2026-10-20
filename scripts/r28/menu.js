
/* Round 28: the phone menu, refined. The page behind it inert while it is open, focus taken into it
   and given back to the button; the phone's back gesture (or the browser's back) closes it, or goes
   back a level; a swipe to the right does the same; the page you are on is marked; the pages it
   leads to are fetched ahead as a finger comes down on them. The menu itself is ms-site.js's. */
(function () {
  'use strict';
  var menu = document.querySelector('[data-ms-menu]');
  if (!menu || !window.MutationObserver) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var opener = null, pushed = false, leaving = false, made = [], specd = false;
  if (!menu.id) menu.id = 'ms-menu';
  menu.setAttribute('tabindex', '-1');
  document.querySelectorAll('[data-ms-menu-open]').forEach(function (b) { b.setAttribute('aria-controls', menu.id); });
  function q(s) { return menu.querySelector(s); }
  function inSub() { var r = q('[data-ms-mroot]'); return !!(r && r.hidden); }

  // everything but the menu and the way up to it
  function setInert(on) {
    if (!on) { made.forEach(function (el) { el.inert = false; }); made = []; return; }
    for (var el = menu; el && el.parentElement && el !== document.body; el = el.parentElement) {
      Array.prototype.forEach.call(el.parentElement.children, function (s) {
        if (s !== el && !s.inert && !/^(SCRIPT|STYLE|LINK|TEMPLATE|META)$/.test(s.tagName)) { s.inert = true; made.push(s); }
      });
    }
  }
  function here() {
    var p = location.pathname.replace(/\/$/, '');
    menu.querySelectorAll('a[href]').forEach(function (a) {
      var u; try { u = new URL(a.href, location.href); } catch (e) { return; }
      var on = u.origin === location.origin && p !== '' && u.pathname.replace(/\/$/, '') === p && !u.hash;
      if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    menu.querySelectorAll('[data-ms-msub-open]').forEach(function (b) {
      var s = q('[data-ms-msub="' + b.getAttribute('data-ms-msub-open') + '"]');
      b.classList.toggle('is-here', !!(s && s.querySelector('a[aria-current="page"]')));
    });
  }
  function speculate() {
    if (specd || !window.HTMLScriptElement || !HTMLScriptElement.supports || !HTMLScriptElement.supports('speculationrules')) return;
    specd = true;
    var s = document.createElement('script');
    s.type = 'speculationrules';
    s.textContent = JSON.stringify({ prefetch: [{ where: { and: [{ selector_matches: '[data-ms-menu] a[href]' }, { not: { selector_matches: '[data-ms-enquire], [data-ms-quiz-link]' } }, { not: { href_matches: '/cart*' } }] }, eagerness: 'moderate' }] });
    document.head.appendChild(s);
  }
  function opened() {
    opener = document.activeElement && document.activeElement !== document.body ? document.activeElement : document.querySelector('[data-ms-menu-open]');
    leaving = false;
    setInert(true);
    here();
    speculate();
    try { history.pushState({ msMenu: 1 }, ''); pushed = true; } catch (e) { pushed = false; }
    menu.focus({ preventScroll: true });
  }
  function closed() {
    setInert(false);
    if (pushed && !leaving && history.state && history.state.msMenu) history.back();
    pushed = false;
    var o = opener; opener = null;
    var d = document.querySelector('[data-ms-drawer]');
    if (o && o.focus && !(d && !d.hidden) && o.offsetParent !== null) o.focus({ preventScroll: true });
  }
  new MutationObserver(function () {
    if (!menu.hidden && !pushed && !opener) opened();
    else if (menu.hidden && (pushed || opener)) closed();
  }).observe(menu, { attributes: true, attributeFilter: ['hidden'] });

  // back: a level up, then out
  window.addEventListener('popstate', function () {
    if (menu.hidden || !pushed) return;
    if (inSub()) {
      var b = q('[data-ms-msub-back]'); if (b) b.click();
      try { history.pushState({ msMenu: 1 }, ''); } catch (e) {}
      return;
    }
    pushed = false;
    var c = q('[data-ms-menu-close]'); if (c) c.click();
  });

  // a link to another page: the menu's own step in the history is taken back first, so the back
  // button from the next page returns here in one step
  menu.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    // the enquiry sheet and the five questions open over this page: the menu's step is simply taken back
    if (!a || a.matches('[data-ms-enquire], [data-ms-quiz-link], a[href="/pages/contact"], a[href*="view=ms-quiz"], a[href$="#find-your-midsummer"]')) return;
    var u; try { u = new URL(a.href, location.href); } catch (err) { return; }
    leaving = true;
    if (!pushed || e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if ((a.target && a.target !== '_self') || a.hasAttribute('download') || u.origin !== location.origin || u.pathname === location.pathname) return;
    e.preventDefault();
    var go = function () { if (go) { go = null; location.assign(u.href); } };
    window.addEventListener('popstate', function () { if (go) go(); }, { once: true });
    pushed = false;
    history.back();
    setTimeout(function () { if (go) go(); }, 450);
  }, true);

  // keyboard: into a level and back out of it, focus follows
  menu.addEventListener('click', function (e) {
    var s = e.target.closest('[data-ms-msub-open]');
    if (s) { menu.dataset.msFrom = s.getAttribute('data-ms-msub-open'); var b = q('[data-ms-msub-back]'); if (b) setTimeout(function () { b.focus({ preventScroll: true }); }, 0); return; }
    if (e.target.closest('[data-ms-msub-back]')) {
      var k = menu.dataset.msFrom, r = k && q('[data-ms-msub-open="' + k + '"]');
      if (r) setTimeout(function () { r.focus({ preventScroll: true }); }, 0);
    }
  });

  // a swipe to the right: a level up, or closed; the page follows the finger a little
  var x0 = null, y0 = 0, t0 = 0, mb = q('[data-ms="mbody"]'), live = false;
  menu.addEventListener('touchstart', function (e) {
    if (e.touches.length !== 1) { x0 = null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; t0 = Date.now(); live = false;
  }, { passive: true });
  menu.addEventListener('touchmove', function (e) {
    if (x0 === null || !mb || reduce) return;
    var dx = e.touches[0].clientX - x0, dy = e.touches[0].clientY - y0;
    if (!live && Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy) * 1.6) live = true;
    if (live && dx > 0) { mb.style.transition = 'none'; mb.style.transform = 'translateX(' + Math.min(dx * .35, 60) + 'px)'; mb.style.opacity = String(1 - Math.min(dx / 600, .25)); }
  }, { passive: true });
  menu.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0;
    x0 = null;
    if (mb) { mb.style.transition = 'transform .35s cubic-bezier(.2,.7,.2,1), opacity .35s'; mb.style.transform = ''; mb.style.opacity = ''; }
    if (dx > 70 && Math.abs(dy) < dx * .6 && Date.now() - t0 < 700) {
      var b = inSub() ? q('[data-ms-msub-back]') : q('[data-ms-menu-close]');
      if (b) b.click();
    }
  }, { passive: true });
})();
