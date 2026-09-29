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
  var onContact = /\/pages\/contact\/?$/.test(location.pathname);
  var lastFocus = null;
  function openDrawer(source) {
    if (!drawer) return false;
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
    if (!drawer || drawer.hidden) return;
    drawer.hidden = true;
    body.classList.remove('ms-lock');
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
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
    var y0 = e.clientY;
    function move(ev) { var dy = Math.max(0, ev.clientY - y0); sheet.style.transform = 'translateY(' + dy + 'px)'; sheet.style.transition = 'none'; }
    function up(ev) {
      window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up);
      var dy = Math.max(0, ev.clientY - y0);
      if (dy > 110) { closeDrawer(); return; }
      sheet.style.transition = 'transform .28s cubic-bezier(.22,1,.36,1)';
      sheet.style.transform = 'translateY(0)';
    }
    window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (drawer && !drawer.hidden) closeDrawer();
    else if (menu && !menu.hidden) closeMenu();
    else closeMega();
  });

  /* ── enquiry forms: the four intentions rewrite the labels, as in the preview ── */
  var TABS = {
    'Request brochure': { note: 'The full catalogue of systems, fibres and Loro Piana Interiors fabrics, as a PDF.', five: 'City', six: 'Enquiry type*', sixHint: 'General · Trade · Press', notes: 'How did you hear about us?' },
    'Book appointment': { note: 'Visit the atelier on Via Andegari, or meet us by video. We confirm within one working day.', five: 'Phone*', six: 'Preferred date*', sixHint: 'Monday to Friday', notes: 'Notes' },
    'Request callback': { note: 'Tell us when suits and one of the atelier team will call you.', five: 'Phone*', six: 'Preferred time*', sixHint: 'Select a time', notes: 'Please tell us about your enquiry*' },
    'Leave a message': { note: 'Anything else — regeneration, care, press or partnership.', five: 'Phone', six: 'Subject', sixHint: 'Optional', notes: 'Message*' }
  };
  function setTab(form, t) {
    var copy = TABS[t];
    if (!copy) return;
    form.querySelectorAll('[data-ms-tab]').forEach(function (b) {
      var on = b.getAttribute('data-ms-tab') === t;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var dot = b.querySelector('[data-ms-dot]');
      if (dot) { dot.style.background = on ? '#9A7B4F' : 'transparent'; dot.style.boxShadow = 'inset 0 0 0 1px ' + (on ? '#9A7B4F' : '#DDD6C9'); }
      var lab = b.querySelector('[data-ms-tablabel]');
      if (lab) lab.style.color = on ? '#17140F' : '#6E675C';
      if (b.hasAttribute('data-ms-chip')) {
        b.style.background = on ? '#17140F' : 'transparent';
        b.style.color = on ? '#FBF9F5' : '#4A443B';
        b.style.borderColor = on ? '#17140F' : '#DDD6C9';
      }
    });
    var set = function (sel, v) { form.querySelectorAll(sel).forEach(function (el) { el.textContent = v; }); };
    set('[data-ms-copy="note"]', copy.note);
    set('[data-ms-copy="five"]', copy.five);
    set('[data-ms-copy="six"]', copy.six);
    set('[data-ms-copy="notes"]', copy.notes);
    form.querySelectorAll('[data-ms-copy="sixHint"]').forEach(function (el) { el.setAttribute('placeholder', copy.sixHint); });
    var five = form.querySelector('[data-ms-field="five"]');
    if (five) { five.name = 'contact[' + copy.five.replace('*', '') + ']'; five.required = /\*$/.test(copy.five); five.type = /phone/i.test(copy.five) ? 'tel' : 'text'; }
    var six = form.querySelector('[data-ms-field="six"]');
    if (six) { six.name = 'contact[' + copy.six.replace('*', '') + ']'; six.required = /\*$/.test(copy.six); }
    var notes = form.querySelector('[data-ms-field="notes"]');
    if (notes) { notes.name = 'contact[' + copy.notes.replace('*', '').replace(/\?$/, '') + ']'; notes.required = /\*$/.test(copy.notes); }
    var mode = form.querySelector('[data-ms-enq-mode-field]');
    if (mode) mode.value = t;
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ms-tab]');
    if (!b) return;
    e.preventDefault();
    setTab(b.closest('[data-ms-enq]'), b.getAttribute('data-ms-tab'));
  });
  document.querySelectorAll('[data-ms-enq]').forEach(function (f) { setTab(f, f.getAttribute('data-ms-enq') || 'Book appointment'); });
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
