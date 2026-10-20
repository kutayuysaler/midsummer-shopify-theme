/* Midsummer Milano: the behaviour of the approved preview, without a framework.
   Header states, the five panels, the phone menu, the enquiry sheet and the
   scroll reveal. Section-specific behaviour lives with each section. */
(function () {
  'use strict';
  var body = document.body;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wrap = document.getElementById('ms-header-wrap');

  /* ── header: clear over the opening photograph until scrolled; hides on phone scroll ── */
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop || 0;
    body.classList.toggle('ms-scrolled', y > 40);
    var narrow = document.documentElement.clientWidth < 761;
    var hide = wrap && wrap.classList.contains('is-hidden');
    var dy = y - lastY;
    if (!narrow || y < 160 || body.classList.contains('ms-lock')) hide = false;
    else if (dy > 8) hide = true;
    else if (dy < -8) hide = false;
    lastY = y;
    if (wrap) wrap.classList.toggle('is-hidden', !!hide);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── the five panels: a click opens one, a second click closes it ── */
  function closeMega() {
    document.querySelectorAll('[data-ms-panel]').forEach(function (p) { p.hidden = true; });
    document.querySelectorAll('[data-ms-mega]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    body.classList.remove('ms-mega-open');
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ms-mega]');
    if (b) {
      e.preventDefault();
      var key = b.getAttribute('data-ms-mega');
      var panel = document.querySelector('[data-ms-panel="' + key + '"]');
      var open = panel && panel.hidden;
      closeMega();
      if (open) {
        panel.hidden = false;
        b.setAttribute('aria-expanded', 'true');
        body.classList.add('ms-mega-open');
      }
      return;
    }
    if (body.classList.contains('ms-mega-open') && !e.target.closest('[data-ms-header]')) closeMega();
  });

  /* ── the phone menu ── */
  var menu = document.querySelector('[data-ms-menu]');
  function animateMenu(from) {
    if (reduce || !menu || !Element.prototype.animate) return;
    menu.querySelectorAll('[data-ms="mbody"] > div:not([hidden]) > nav > *, [data-ms="mbody"] > div:not([hidden]) > a, [data-ms="mbody"] > div:not([hidden]) > div').forEach(function (el, i) {
      var a = el.animate([{ opacity: 0, transform: from }, { opacity: 1, transform: 'none' }], { duration: 560, delay: 50 + i * 48, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
      setTimeout(function () { try { if (a.playState !== 'finished') a.finish(); } catch (err) {} }, 2000);
    });
  }
  function showSub(key) {
    if (!menu) return;
    menu.querySelectorAll('[data-ms-msub]').forEach(function (s) { s.hidden = s.getAttribute('data-ms-msub') !== key; });
    var root = menu.querySelector('[data-ms-mroot]');
    if (root) root.hidden = !!key;
    var back = menu.querySelector('[data-ms-msub-back]');
    var logo = menu.querySelector('[data-ms-mroot-only]');
    if (back) back.hidden = !key;
    if (logo) logo.hidden = !!key;
    var mb = menu.querySelector('[data-ms="mbody"]');
    if (mb) mb.scrollTop = 0;
  }
  function openMenu() {
    if (!menu) return;
    closeMega();
    showSub(null);
    menu.hidden = false;
    body.classList.add('ms-lock');
    document.querySelectorAll('[data-ms-menu-open]').forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    if (!reduce && menu.animate) menu.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 240, easing: 'ease-out' });
    animateMenu('translateY(16px)');
  }
  function closeMenu() {
    if (!menu) return;
    menu.hidden = true;
    body.classList.remove('ms-lock');
    document.querySelectorAll('[data-ms-menu-open]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-ms-menu-open]')) { e.preventDefault(); openMenu(); return; }
    if (e.target.closest('[data-ms-menu-close]')) { e.preventDefault(); closeMenu(); return; }
    var s = e.target.closest('[data-ms-msub-open]');
    if (s) { e.preventDefault(); showSub(s.getAttribute('data-ms-msub-open')); animateMenu('translateX(32px)'); return; }
    if (e.target.closest('[data-ms-msub-back]')) { e.preventDefault(); showSub(null); animateMenu('translateX(-32px)'); return; }
    if (menu && !menu.hidden && e.target.closest('[data-ms-menu] a')) closeMenu();
  });

  /* ── the enquiry sheet ── */
  var drawer = document.querySelector('[data-ms-drawer]');
  var onContact = /\/pages\/contact\/?$/.test(location.pathname) || !!document.querySelector('[data-ms-enq-page]');
  var lastFocus = null;
  var closing = null;
  function openDrawer(source) {
    if (!drawer) return false;
    if (closing) { closing.forEach(function (a) { try { a.cancel(); } catch (err) {} }); closing = null; }
    closeMega();
    closeMenu();
    lastFocus = document.activeElement;
    drawer.hidden = false;
    body.classList.add('ms-lock');
    var sheet = drawer.querySelector('[data-ms="sheet"]');
    if (sheet) { sheet.style.transform = ''; sheet.style.transition = ''; }
    var c = drawer.querySelector('[data-ms-drawer-close]');
    if (c) setTimeout(function () { c.focus({ preventScroll: true }); }, 30);
    document.dispatchEvent(new CustomEvent('ms:enquiry-open', { detail: { source: source || null } }));
    return true;
  }
  function closeDrawer() {
    if (!drawer || drawer.hidden || closing) return;
    var sheet = drawer.querySelector('[data-ms="sheet"]'), veil = drawer.querySelector('[data-ms-drawer] > [data-ms-drawer-close]');
    closing = [];
    function done() {
      if (!closing) return;
      closing.forEach(function (a) { try { a.cancel(); } catch (err) {} });
      closing = null;
      drawer.hidden = true;
      if (sheet) { sheet.style.transform = ''; sheet.style.transition = ''; }
      if (veil) veil.style.opacity = '';
      body.classList.remove('ms-lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
    // Round 29: the sheet goes back the way it came, from wherever a finger left it, the room brightening
    if (reduce || !sheet || !sheet.animate) { done(); return; }
    var phone = window.matchMedia('(max-width: 760px)').matches, from = getComputedStyle(sheet).transform;
    var a = sheet.animate([{ transform: from && from !== 'none' ? from : 'translate3d(0, 0, 0)' }, { transform: phone ? 'translate3d(0, 100%, 0)' : 'translate3d(100%, 0, 0)' }],
      { duration: phone ? 340 : 400, easing: 'cubic-bezier(.32, 0, .67, 0)', fill: 'forwards' });
    closing.push(a);
    if (veil) closing.push(veil.animate([{ opacity: getComputedStyle(veil).opacity }, { opacity: 0 }], { duration: phone ? 340 : 400, easing: 'ease-in', fill: 'forwards' }));
    a.onfinish = done;
    setTimeout(done, 700);
  }
  window.msEnquiry = { open: openDrawer, close: closeDrawer };
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
    var a = e.target.closest('[data-ms-enquire], a[href="/pages/contact"]');
    if (a && !onContact && !a.closest('[data-ms-drawer]')) {
      if (openDrawer(a)) e.preventDefault();
      return;
    }
    if (e.target.closest('[data-ms-drawer-close]')) { e.preventDefault(); closeDrawer(); }
  });
  // reopen after a submission from the sheet, so the visitor sees the confirmation
  if (drawer && /contact_posted=true/.test(location.search) && /ms-drawer/.test(location.hash) && !onContact) openDrawer(null);

  // drag the sheet down to dismiss (phones)
  document.addEventListener('pointerdown', function (e) {
    var grip = e.target.closest('[data-ms="grip"]');
    if (!grip) return;
    var sheet = grip.closest('[data-ms="sheet"]');
    var y0 = e.clientY, t0 = Date.now(), veil = sheet.parentNode.querySelector(':scope > [data-ms-drawer-close]');
    function move(ev) { var dy = Math.max(0, ev.clientY - y0); sheet.style.transform = 'translateY(' + dy + 'px)'; sheet.style.transition = 'none'; if (veil) veil.style.opacity = String(Math.max(.25, 1 - dy / 520)); }
    function up(ev) {
      window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up);
      var dy = Math.max(0, ev.clientY - y0);
      // far enough, or a quick flick: it goes; otherwise it settles back
      if (dy > 110 || (dy > 36 && Date.now() - t0 < 260)) { closeDrawer(); return; }
      sheet.style.transition = 'transform .32s cubic-bezier(.22,1,.36,1)';
      sheet.style.transform = 'translateY(0)';
      if (veil) veil.style.opacity = '';
    }
    window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
  });

  /* ── Find your Midsummer as an overlay, where the store has no quiz page ── */
  var quizDlg = document.querySelector('[data-ms-quiz-dialog]');
  function openQuiz() { if (!quizDlg) return false; closeMega(); closeMenu(); closeDrawer(); quizDlg.hidden = false; body.classList.add('ms-lock'); var c = quizDlg.querySelector('[data-ms-quiz-close]'); if (c) c.focus({ preventScroll: true }); return true; }
  function closeQuiz() { if (!quizDlg || quizDlg.hidden) return; quizDlg.hidden = true; body.classList.remove('ms-lock'); if (location.hash === '#find-your-midsummer') history.replaceState(null, '', location.pathname + location.search); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href$="#find-your-midsummer"], a[href*="view=ms-quiz"]');
    if (a && (e.metaKey || e.ctrlKey)) return;
    if (a && quizDlg) { e.preventDefault(); openQuiz(); return; }
    if (e.target.closest('[data-ms-quiz-close]')) { e.preventDefault(); closeQuiz(); }
  });
  if (location.hash === '#find-your-midsummer') openQuiz();

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (quizDlg && !quizDlg.hidden) { closeQuiz(); return; }
    if (drawer && !drawer.hidden) closeDrawer();
    else if (menu && !menu.hidden) closeMenu();
    else closeMega();
  });

  /* ── enquiry forms: the four intentions rewrite the labels, as in the preview ── */
  var TABS = {
    'Request brochure': { note: 'The full catalogue of systems, fibres and Loro Piana Interiors fabrics, sent to you by the atelier.', five: 'City', six: 'Enquiry type*', sixHint: 'General · Trade · Press', notes: 'How did you hear about us?' },
    'Book appointment': { title: 'Book an appointment', note: 'Visit the atelier on Via Andegari, or meet us by video. We confirm within one working day.', five: 'Phone*', six: 'Preferred date*', sixHint: 'Monday to Friday', notes: 'Notes' },
    'Request callback': { title: 'Request a callback', note: 'Tell us when suits and one of the atelier team will call you.', five: 'Phone*', six: 'Preferred time*', sixHint: 'Select a time', notes: 'Please tell us about your enquiry*' },
    'Leave a message': { note: 'Anything else — regeneration, care or press.', five: 'Phone', six: 'Subject', sixHint: 'Optional', notes: 'Message*' },
    'Request a proposal': { note: 'Tell us the system, the size and the room. The atelier replies with a written specification and its price.', five: 'Phone', six: 'System and size', sixHint: 'e.g. Paisley, 180 × 200', notes: 'About the room*' },
    'Trade enquiry': { note: 'For architects, interior designers and hospitality: drawings, samples and trade terms for your project.', five: 'Company*', six: 'Project*', sixHint: 'Residence, hotel, yacht…', notes: 'Tell us about the project*' },
    'Become a partner': { note: 'To represent Midsummer Milano in your market, as a showroom, an agent or a reseller.', five: 'Company*', six: 'Market*', sixHint: 'City and country', notes: 'Tell us about your showroom*' }
  };
  var T = function (s) { var d = window.msT; return (d && d[s]) || s; };
  var SLUG = { appointment: 'Book appointment', proposal: 'Request a proposal', brochure: 'Request brochure', callback: 'Request callback', message: 'Leave a message', trade: 'Trade enquiry', partner: 'Become a partner' };
  function slugOf(t) { for (var k in SLUG) if (SLUG[k] === t) return k; return ''; }
  // Round 29: on a phone the kinds of enquiry are a strip that scrolls sideways; the chosen one comes fully into it
  function keepInView(b) {
    var l = b.parentNode;
    if (!l || l.scrollWidth <= l.clientWidth + 1) return;
    var lr = l.getBoundingClientRect(), br = b.getBoundingClientRect();
    if (br.left >= lr.left + 4 && br.right <= lr.right - 4) return;
    l.scrollBy({ left: br.left - lr.left - (lr.width - br.width) / 2, behavior: reduce ? 'auto' : 'smooth' });
  }
  function setTab(form, t) {
    var copy = TABS[t];
    if (!copy) return;
    form.querySelectorAll('[data-ms-tab]').forEach(function (b) {
      var on = b.getAttribute('data-ms-tab') === t;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) keepInView(b);
      var dot = b.querySelector('[data-ms-dot]');
      if (dot) { dot.style.background = on ? '#7E623B' : 'transparent'; dot.style.boxShadow = 'inset 0 0 0 1px ' + (on ? '#7E623B' : '#DDD6C9'); }
      var lab = b.querySelector('[data-ms-tablabel]');
      if (lab) lab.style.color = on ? '#17140F' : '#6E675C';
      if (b.hasAttribute('data-ms-chip')) {
        b.style.background = on ? '#17140F' : 'transparent';
        b.style.color = on ? '#FBF9F5' : '#4A443B';
        b.style.borderColor = on ? '#17140F' : '#DDD6C9';
      }
    });
    var set = function (sel, v) { form.querySelectorAll(sel).forEach(function (el) { el.textContent = v; }); };
    set('[data-ms-copy="note"]', T(copy.note));
    set('[data-ms-copy="five"]', T(copy.five));
    set('[data-ms-copy="six"]', T(copy.six));
    set('[data-ms-copy="notes"]', T(copy.notes));
    form.querySelectorAll('[data-ms-copy="sixHint"]').forEach(function (el) { el.setAttribute('placeholder', T(copy.sixHint)); });
    var five = form.querySelector('[data-ms-field="five"]');
    if (five) { five.name = 'contact[' + copy.five.replace('*', '') + ']'; five.required = /\*$/.test(copy.five); five.type = /phone/i.test(copy.five) ? 'tel' : 'text'; }
    var six = form.querySelector('[data-ms-field="six"]');
    if (six) { six.name = 'contact[' + copy.six.replace('*', '') + ']'; six.required = /\*$/.test(copy.six); }
    var notes = form.querySelector('[data-ms-field="notes"]');
    if (notes) { notes.name = 'contact[' + copy.notes.replace('*', '').replace(/\?$/, '') + ']'; notes.required = /\*$/.test(copy.notes); }
    var mode = form.querySelector('[data-ms-enq-mode-field]');
    if (mode) mode.value = t;
    set('[data-ms-copy="title"]', T(copy.title || t));
    // the sheet's link to the full page carries the chosen enquiry with it
    var full = form.closest('[data-ms-drawer]') && form.closest('[data-ms-drawer]').querySelector('a[data-ms="cta"]');
    if (full) { var fu = new URL(full.getAttribute('href'), location.href); fu.searchParams.set('enquiry', slugOf(t)); fu.hash = 'enquire'; full.setAttribute('href', fu.pathname + fu.search + fu.hash); }
    form.dispatchEvent(new CustomEvent('ms:enquiry-tab', { bubbles: true, detail: { tab: t, slug: slugOf(t) } }));
    form.querySelectorAll('[data-ms-brochure]').forEach(function (a) { a.hidden = t !== 'Request brochure'; });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ms-tab]');
    if (!b) return;
    e.preventDefault();
    setTab(b.closest('[data-ms-enq]'), b.getAttribute('data-ms-tab'));
  });
  document.querySelectorAll('[data-ms-enq]').forEach(function (f) { setTab(f, f.getAttribute('data-ms-enq') || 'Book appointment'); });

  /* the sheet opens on the enquiry its button asks for (data-ms-enquiry="proposal") */
  document.addEventListener('ms:enquiry-open', function (e) {
    var src = e.detail && e.detail.source;
    var want = src && src.getAttribute && SLUG[src.getAttribute('data-ms-enquiry')];
    if (!want && src && src.textContent) {
      var w = src.textContent.toLowerCase();
      want = /proposal|quote|specif|propost|preventiv|предложен|смет/.test(w) ? 'Request a proposal' : /brochure|catalog|брошюр|каталог/.test(w) ? 'Request brochure' : /call ?back|richiam|перезвон|звонок/.test(w) ? 'Request callback'
        : /partner|represent|rappresent|партн|представ/.test(w) ? 'Become a partner' : /trade|professionist|профессионал/.test(w) ? 'Trade enquiry' : null;
    }
    var f = drawer && drawer.querySelector('[data-ms-enq]');
    if (f) setTab(f, want || 'Book appointment');
    // a button can start the message (data-ms-note), e.g. an introduction to a showroom
    var note = src && src.getAttribute && src.getAttribute('data-ms-note');
    var area = f && f.querySelector('[data-ms-field="notes"]');
    if (area && note && (!area.value || area.getAttribute('data-ms-prefilled') === '1')) { area.value = note; area.setAttribute('data-ms-prefilled', '1'); }
  });

  /* the enquiry landing page: ?enquiry=trade opens that form; menu links on the page itself don't reload */
  var landing = document.querySelector('[data-ms-enq-page] [data-ms-enq]');
  function landOn(slug, hash) {
    if (!landing) return false;
    if (slug && SLUG[slug]) setTab(landing, SLUG[slug]);
    var target = hash && document.getElementById(hash.replace('#', ''));
    if (target) target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    return true;
  }
  if (landing) {
    var q = new URLSearchParams(location.search).get('enquiry');
    if (q && SLUG[q]) setTab(landing, SLUG[q]);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-ms-landing]');
    if (!a || !landing || e.metaKey || e.ctrlKey) return;
    var u = new URL(a.href, location.href);
    if (u.pathname !== location.pathname || u.searchParams.get('view') !== new URLSearchParams(location.search).get('view')) return;
    e.preventDefault();
    closeMega(); closeMenu();
    history.replaceState(null, '', u.pathname + u.search + u.hash);
    landOn(u.searchParams.get('enquiry'), u.hash);
  });

  /* figures count up the first time they come into view: <div data-ms-count>24</div>, or 15 / 15 */
  if (!reduce && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var nodes = [], w = document.createTreeWalker(en.target, NodeFilter.SHOW_TEXT);
        while (w.nextNode()) if (/^\s*\d{1,4}\s*$/.test(w.currentNode.nodeValue)) nodes.push(w.currentNode);
        nodes.forEach(function (n) {
          var to = parseInt(n.nodeValue, 10), pad = n.nodeValue.match(/^\s*/)[0], t0 = null;
          if (to < 2) return;
          function step(t) {
            if (!t0) t0 = t;
            var k = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - k, 3);
            n.nodeValue = pad + Math.round(to * e);
            if (k < 1) requestAnimationFrame(step);
          }
          n.nodeValue = pad + '0';
          requestAnimationFrame(step);
        });
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-ms-count]').forEach(function (el) { cio.observe(el); });
  }

  /* a link ending #care opens the first question on the page that mentions care */
  (function () {
    var h = decodeURIComponent(location.hash.slice(1) || '').toLowerCase();
    if (!h || document.getElementById(h)) return;
    var hit = Array.prototype.find.call(document.querySelectorAll('main details'), function (d) {
      var s = d.querySelector('summary'); return s && s.textContent.toLowerCase().indexOf(h) > -1;
    });
    if (!hit) return;
    document.querySelectorAll('main details[open]').forEach(function (d) { if (d !== hit) d.open = false; });
    hit.open = true;
    setTimeout(function () { hit.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' }); }, 120);
  })();

  /* Cookies: the banner's preferences (iubenda's, or Shopify's own); otherwise the cookie policy */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-ms-cookies]');
    if (!a) return;
    var iub = window._iub && window._iub.cs && window._iub.cs.api;
    if (iub && typeof iub.openPreferences === 'function') { e.preventDefault(); iub.openPreferences(); return; }
    var pb = window.privacyBanner;
    if (pb && typeof pb.showPreferences === 'function') { e.preventDefault(); pb.showPreferences(); }
  });
  document.addEventListener('change', function (e) {
    if (e.target.matches && e.target.matches('select.ms-field')) e.target.classList.toggle('is-set', !!e.target.value);
  });

  /* ── scroll reveal: Web Animations with no lasting fill, so a stalled clock never hides content ── */
  if (!reduce && 'IntersectionObserver' in window && Element.prototype.animate) {
    var ez = 'cubic-bezier(.2,.7,.2,1)';
    var io = new IntersectionObserver(function (entries) {
      var k = 0;
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; io.unobserve(el);
        var img = el.tagName === 'IMG';
        var a = el.animate(img
          ? [{ opacity: 0, transform: 'scale(1.045)' }, { opacity: 1, transform: 'none' }]
          : [{ opacity: 0, transform: 'translateY(22px)' }, { opacity: 1, transform: 'none' }],
          { duration: img ? 1150 : 780, delay: Math.min(k++, 6) * 75, easing: ez, fill: 'backwards' });
        setTimeout(function () { try { if (a.playState !== 'finished') a.finish(); } catch (err) {} }, 2800);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    var scan = function (root) {
      (root || document).querySelectorAll('main section h1, main section h2, main section h3, main section p, main section img, main section [data-ms="prodgrid"] > *, [data-ms-footer] > div').forEach(function (el) {
        if (el.__msSeen || el.closest('header, [role="dialog"], [data-ms="sheet"], [data-ms="pressrow"]')) return;
        if (el.tagName === 'IMG' && el.closest('[data-ms="prodgrid"]')) return;
        var p = getComputedStyle(el).position; if (p === 'absolute' || p === 'fixed') return;
        var r = el.getBoundingClientRect(); if (r.top < window.innerHeight * 0.9 && r.bottom > 0 && !root) { el.__msSeen = true; return; }
        el.__msSeen = true; io.observe(el);
      });
    };
    scan();
    window.msReveal = scan;
    document.addEventListener('shopify:section:load', function (e) { scan(e.target); });
  }
})();

/* ── rows without an orphan: on a tablet or a computer, a grid of cards whose last row would hold a single
      card takes the nearest number of columns that leaves none alone (three and one become two and two) ── */
(function () {
  var MIN = 170;
  function cards(g) {
    return Array.prototype.filter.call(g.children, function (k) { var cs = getComputedStyle(k); return cs.display !== 'none' && cs.position !== 'absolute' && k.getBoundingClientRect().height > 40; });
  }
  function balance() {
    var wide = window.innerWidth > 760;
    document.querySelectorAll('[data-ms-balanced]').forEach(function (g) { g.style.gridTemplateColumns = g.getAttribute('data-ms-balanced'); g.removeAttribute('data-ms-balanced'); });
    if (!wide) return;
    document.querySelectorAll('main *').forEach(function (g) {
      var cs = getComputedStyle(g);
      if (cs.display !== 'grid' || g.querySelector('input, textarea, select') || g.closest('[data-ms-drawer], [data-ms-panel], [data-ms-menu], .ms-article-body')) return;
      var ks = cards(g); var n = ks.length; if (n < 3) return;
      if (ks.some(function (k) { var c = getComputedStyle(k).gridColumnEnd; return c === '-1' || /span/.test(c) || /span/.test(getComputedStyle(k).gridColumnStart); })) return;
      var cols = cs.gridTemplateColumns.split(' ').filter(Boolean).length;
      if (cols < 2 || n <= cols || n % cols !== 1) return;
      var gap = parseFloat(cs.columnGap) || 0, w = g.clientWidth;
      var fits = function (c) { return (w - gap * (c - 1)) / c >= MIN; };
      var pick = null;
      [cols + 1, cols - 1, cols + 2, cols - 2].some(function (c) { if (c >= 2 && n % c !== 1 && (c < cols || fits(c))) { pick = c; return true; } return false; });
      if (!pick) return;
      g.setAttribute('data-ms-balanced', g.style.gridTemplateColumns || '');
      g.style.gridTemplateColumns = 'repeat(' + pick + ', minmax(0, 1fr))';
    });
  }
  var t = null;
  function soon() { clearTimeout(t); t = setTimeout(balance, 120); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', soon); else soon();
  window.addEventListener('load', soon);
  window.addEventListener('resize', soon);
  document.addEventListener('ms:balance', soon);
  // filters (the Journal's subjects, the palette's weaves) change what is shown
  document.addEventListener('click', function (e) { if (e.target.closest('button, [data-cat], [role="tab"]')) soon(); });
})();

/* ms-mail-name: before an enquiry is sent, Shopify's name field takes the visitor's title and name,
   and the page it was sent from is named, so the mail at the store reads clearly */
(function () {
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || !f.querySelector || !f.querySelector('[name="contact[Enquiry mode]"]')) return;
    var v = function (n) { var el = f.querySelector('[name="contact[' + n + ']"]'); return el && el.value ? el.value.trim() : ''; };
    var put = function (n, val, before) {
      var el = f.querySelector('input[type="hidden"][name="contact[' + n + ']"]');
      if (!el) { el = document.createElement('input'); el.type = 'hidden'; el.name = 'contact[' + n + ']'; if (before && before.parentNode) before.parentNode.insertBefore(el, before.nextSibling); else f.appendChild(el); }
      el.value = val;
    };
    var mode = f.querySelector('[name="contact[Enquiry mode]"]');
    var name = [v('Title'), v('First name'), v('Last name')].filter(Boolean).join(' ');
    if (name) put('name', name, mode);
    put('Sent from', [(document.title || '').replace(/\s+/g, ' ').trim(), '(' + location.origin + location.pathname + location.search + ')'].filter(Boolean).join(' '), mode);
  }, true);
})();

// rows that scroll sideways (on a phone): reachable from the keyboard, and named for screen readers
(function () {
  function mark() {
    document.querySelectorAll('[data-ms="rail"]').forEach(function (r) {
      var scrolls = r.scrollWidth > r.clientWidth + 2;
      if (scrolls && !r.hasAttribute('tabindex')) {
        r.setAttribute('tabindex', '0'); r.setAttribute('data-ms-kb', '');
        if (!r.getAttribute('role')) r.setAttribute('role', 'region');
        if (!r.getAttribute('aria-label')) { var sec = r.closest('section, .shopify-section'); var h = sec && sec.querySelector('h1, h2, h3'); r.setAttribute('aria-label', h ? h.textContent.trim().slice(0, 80) : document.title); }
      } else if (!scrolls && r.hasAttribute('data-ms-kb')) {
        r.removeAttribute('tabindex'); r.removeAttribute('data-ms-kb'); r.removeAttribute('role');
      }
    });
  }
  mark();
  window.addEventListener('resize', function () { clearTimeout(mark.t); mark.t = setTimeout(mark, 200); });
})();

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
/* Round 29: the phone menu's few photographs are fetched as it opens, already as a finger comes down on
   the menu button (left to load lazily, the five questions' photograph came late), and a hairline marks
   its head once the list has moved under it. Round 28's block above stays as it was */
(function () {
  'use strict';
  var menu = document.querySelector('[data-ms-menu]');
  if (!menu || !window.MutationObserver) return;
  var mb = menu.querySelector('[data-ms="mbody"]');
  function eager() { menu.querySelectorAll('img[loading="lazy"]').forEach(function (i) { i.loading = 'eager'; }); }
  // a head start: as a finger comes down on the menu button
  document.addEventListener('pointerdown', function (e) { if (e.target.closest && e.target.closest('[data-ms-menu-open]')) eager(); }, { passive: true });
  new MutationObserver(function () { if (!menu.hidden) { eager(); menu.classList.toggle('is-scrolled', !!mb && mb.scrollTop > 2); } })
    .observe(menu, { attributes: true, attributeFilter: ['hidden'] });
  if (mb) mb.addEventListener('scroll', function () { menu.classList.toggle('is-scrolled', mb.scrollTop > 2); }, { passive: true });
})();
