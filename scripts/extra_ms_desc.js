  // the description, put in order: whatever admin holds (paragraphs or line breaks, an opening
  // quotation, headings such as "Sizes (cm)" or "Finishings", "Standard measures: 160x220", the
  // delivery small print) becomes an epigraph, a lead, the text, and facts in the list above
  (function () {
    var box = document.querySelector('.ms-pm__more .ms-pm__desc[data-ms-desc]');
    if (!box || box.hasAttribute('data-ms-desc-done')) return;
    box.setAttribute('data-ms-desc-done', '');
    var L = { dims: box.getAttribute('data-l-dims') || 'Dimensions', height: box.getAttribute('data-l-height') || 'Height', comp: box.getAttribute('data-l-comp') || 'Composition', fin: box.getAttribute('data-l-fin') || 'Finishings', care: box.getAttribute('data-l-care') || 'Care', order: box.getAttribute('data-l-order') || 'Made to order' };
    var html = box.innerHTML
      .replace(/<!--[\s\S]*?-->/g, '')
      .replace(/<\/?(span|font)[^>]*>/gi, '')
      .replace(/\s(data-[\w-]+|class|style|title|dir)="[^"]*"/gi, '')
      .replace(/<h[1-6][^>]*>/gi, '\n§H§').replace(/<\/h[1-6]>/gi, '\n')
      .replace(/<li[^>]*>/gi, '\n§L§').replace(/<\/li>/gi, '\n')
      .replace(/<br[^>]*>\s*(&nbsp;|\s)*<br[^>]*>/gi, '\n')
      .replace(/<br[^>]*>/gi, '\n§B§')
      .replace(/<\/?(p|div|ul|ol|blockquote|section|article|table|tbody|tr|td)[^>]*>/gi, '\n')
      .replace(/<hr[^>]*>/gi, '\n');
    var blocks = [];
    html.split('\n').forEach(function (raw) {
      var kind = 'p', soft = false, s = raw;
      if (s.indexOf('§H§') === 0) { kind = 'h'; s = s.slice(3); }
      else if (s.indexOf('§L§') === 0) { kind = 'li'; s = s.slice(3); }
      else if (s.indexOf('§B§') === 0) { soft = true; s = s.slice(3); }
      var d = document.createElement('div'); d.innerHTML = s;
      var text = d.textContent.replace(/ /g, ' ').replace(/\s+/g, ' ').trim();
      if (!text) return;
      // a line set in capitals reads as a line, a name in capitals as a name
      var inner = s.trim();
      if (text.length > 3 && text === text.toUpperCase() && /[A-Z]{3}/.test(text)) {
        var sc = text.toLowerCase().replace(/(^|[.!?]\s+)(\p{L})/gu, function (m, a, b) { return a + b.toUpperCase(); });
        inner = sc; text = sc;
      } else {
        inner = inner.replace(/\b([A-ZÀ-Ž]{4,})\b/g, function (w) { return w.charAt(0) + w.slice(1).toLowerCase(); });
        text = text.replace(/\b([A-ZÀ-Ž]{4,})\b/g, function (w) { return w.charAt(0) + w.slice(1).toLowerCase(); });
      }
      // one name, written one way
      inner = inner.replace(/Midsummer-Milano/g, 'Midsummer Milano'); text = text.replace(/Midsummer-Milano/g, 'Midsummer Milano');
      // a heading of its own words only: a short line in bold
      if (kind === 'p' && /^<(strong|b)>[^<]{2,48}<\/(strong|b)>$/i.test(inner)) kind = 'h';
      // a sentence set as a heading reads as a sentence; a heading that holds its value ("Height: 9-10 cm") is a line of facts
      if (kind === 'h' && (text.length > 60 || /[.!?]$/.test(text))) { kind = 'p'; inner = text; }
      if (kind === 'h' && /^[^:]{2,28}:\s*\S/.test(text)) { kind = 'p'; inner = text; }
      if (kind === 'h') { text = text.replace(/\s*:\s*$/, ''); inner = inner.replace(/\s*:\s*(<\/(strong|b)>)?\s*$/i, '$1'); }
      // a link alone on its line, said as where it goes rather than "click here"
      var lone = inner.match(/^<a\s[^>]*href="([^"]+)"[^>]*>([^<]*)<\/a>$/i);
      if (kind === 'p' && lone) {
        kind = 'a';
        if (/^(click here|clicca qui|more info|for more information|read more)/i.test(lone[2].trim())) {
          var host = lone[1].replace(/^https?:\/\/(www\.)?/i, '').split('/')[0];
          if (host) { text = (box.getAttribute('data-l-more') || 'More at') + ' ' + host; inner = inner.replace(/>[^<]*<\/a>$/, '>' + text + '</a>'); }
        }
      }
      // a sentence left without its full stop
      if (kind === 'p' && text.length > 30 && /\p{L}$/u.test(text)) inner += '.';
      blocks.push({ k: kind, soft: soft, html: inner, text: text });
    });
    // the build stays the atelier's: where the theme is set to keep it private (the default), what
    // names springs, layers or the core is left out of what is shown. A sentence that names them goes
    // on its own and the rest of its paragraph stays; a run of short lines with one of them in it (a
    // list of what lies under what is the build itself) goes whole; so does a heading over such words
    if (box.hasAttribute('data-discreet')) {
      var CON = /\b(layers?|strat[oi]|springs?|micro-?springs?|mini-?molle|molle|sommier|knots?|nodi|coils?|pocket(ed)?|insacchettat\w*|hourglass|clessidra|core|nucleo)\b|пружин|слой|слоя|слоёв|слоев/i;
      var HEADX = /\b(padding|imbottitura|struttura|structure|construction|costruzione|inside|interno)\b/i;
      var said = function (s) { return CON.test(s.replace(/dreamy springs|box-?springs?|spring\s*(\/|and|e)\s*summer|\b(in|of|the|this|every|early|late)\s+spring\b/gi, '')); };
      var kept = [], head = null, group = [];
      var flush = function () {
        var out = [], run = [];
        var dimsHead = head && /^(sizes?|dimensions?|measures?|misure|dimensioni|heights?|altezz)/i.test(head.text);
        var close = function () { if (!run.some(function (b) { return said(b.text); })) out = out.concat(run); run = []; };
        group.forEach(function (b) {
          if (dimsHead) { if (!said(b.text)) out.push(b); return; }
          if (b.k !== 'p' || b.text.length < 80) { run.push(b); return; }
          close();
          if (!said(b.text)) { out.push(b); return; }
          var ok = b.text.split(/(?<=[.!?])\s+/).filter(function (s) { return !said(s); });
          if (!ok.length) return;
          b.text = ok.join(' '); b.html = b.text.replace(/[&<>]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]; });
          out.push(b);
        });
        close();
        if (head && !said(head.text) && !HEADX.test(head.text) && (out.length || !group.length)) kept.push(head);
        if (!head || (!said(head.text) && !HEADX.test(head.text))) kept = kept.concat(out);
        head = null; group = [];
      };
      blocks.forEach(function (b) { if (b.k === 'h') { flush(); head = b; } else group.push(b); });
      flush();
      blocks = kept;
    }
    if (!blocks.length) {
      if (box.closest('details')) box.closest('details').hidden = true;
      var tl0 = document.querySelector('.ms-pm__tagline[data-ms-auto]'); if (tl0) tl0.hidden = true;
      return;
    }
    var facts = [], note = [], parts = [], epi = null;
    // an opening quotation: "words - Author", or quoted lines and then the author alone on a line
    var q = blocks[0].text.match(/^[“"«]?(.{6,280}?)[”"»]?\s+[-–—]\s*([^-–—]{2,60})$/);
    if (q && q[2].split(' ').length <= 6) { epi = { q: q[1], a: q[2] }; blocks.shift(); }
    else if ((function () {
      // the quotation over several lines, its author on a line of their own after a dash: "… - Claude Monet"
      for (var i = 1; i < Math.min(blocks.length, 6); i++) {
        var m = blocks[i].text.match(/^[-–—]\s*(.{2,60})$/);
        if (m && m[1].split(' ').length <= 6) {
          epi = { q: blocks.slice(0, i).map(function (b) { return b.text; }).join(' ').replace(/^[“"«]|[”"»]$/g, ''), a: m[1] };
          blocks.splice(0, i + 1);
          return true;
        }
        if (blocks[i].text.length > 160) break;
      }
      return false;
    })()) {}
    else if (/^[“"«]/.test(blocks[0].text)) {
      for (var i = 1; i < Math.min(blocks.length, 5); i++) {
        var t = blocks[i].text;
        if (t.split(' ').length <= 4 && !/[.!?:]$/.test(t) && /^\p{Lu}/u.test(t)) {
          epi = { q: blocks.slice(0, i).map(function (b) { return b.text; }).join(' ').replace(/^[“"«]|[”"»]$/g, ''), a: t };
          blocks.splice(0, i + 1);
          break;
        }
      }
    }
    var FACT = [[/^(sizes?|dimensions?|measures?|misure|dimensioni|standard (sizes?|measures?))\b/i, 'dims'], [/^(heights?|altezza)\b/i, 'height'], [/^(finish(ing)?s?|finiture|details)\b/i, 'fin'],
                [/^(materials?|composition|composizione|materiali)\b/i, 'comp'], [/^(care|washing|maintenance|cura|lavaggio)\b/i, 'care']];
    function factKey(t) { for (var i = 0; i < FACT.length; i++) if (FACT[i][0].test(t)) return FACT[i][1]; return null; }
    var cur = null;
    blocks.forEach(function (b) {
      if (/slow manufactur|delivery times?|tempi di consegna|made only on request|once the order has been placed/i.test(b.text)) { note.push(b.html); return; }
      if (b.k === 'h') {
        var fk = factKey(b.text.replace(/\(.*?\)/g, '').trim());
        if (fk) { var un = b.text.match(/\((cm|mm)\)/i); cur = { fact: fk, unit: un ? un[1].toLowerCase() : '', items: [] }; facts.push(cur); return; }
        cur = { head: b.html, items: [] }; parts.push(cur); return;
      }
      var lv = b.text.match(/^([A-Za-zÀ-Ž][\wÀ-Ž ()\/]{1,28}):\s*(.{1,200})$/);
      if (lv && b.k !== 'li') {
        var fk2 = factKey(lv[1]);
        if (fk2 || /width|length|weight|larghezza|lunghezza|peso/i.test(lv[1])) { facts.push({ fact: fk2 || 'dims', label: fk2 ? null : lv[1], items: [{ k: 'p', html: lv[2] }] }); cur = null; return; }
      }
      if (cur && cur.fact) { cur.items.push(b); return; }
      if (!cur || cur.fact) { cur = { items: [] }; parts.push(cur); }
      cur.items.push(b);
    });
    // what it is made of, said in the text as percentages ("70% cashmere and 30% silk")
    var all = blocks.map(function (b) { return b.text; }).join(' ');
    var comp = all.match(/\b\d{1,3}\s?%\s?(?:(?:extra[- ]?fine|superfine|fine|pure|kid|baby|virgin|merino)\s)*(cashmere|silk|wool|linen|cotton|mohair|alpaca|yak|camel|vicu[ñn]a|merino|viscose|lurex|lyocell|polyamide|polyester|nylon|elastane|leather)\b/gi);
    if (comp && !facts.some(function (f) { return f.fact === 'comp'; })) {
      var seen = {}; comp = comp.filter(function (c) { var k = c.toLowerCase().replace(/\s/g, ''); if (seen[k]) return false; seen[k] = 1; return true; });
      facts.push({ fact: 'comp', items: [{ k: 'p', html: comp.join(', ') }] });
    }
    // writing it out
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
    function items(list) {
      var out = '', inList = false;
      list.forEach(function (b) {
        if (b.k === 'li') { if (!inList) { out += '<ul>'; inList = true; } out += '<li>' + b.html + '</li>'; return; }
        if (inList) { out += '</ul>'; inList = false; }
        out += b.k === 'a' ? '<p class="ms-desc__link">' + b.html + '</p>' : '<p>' + b.html + '</p>';
      });
      return out + (inList ? '</ul>' : '');
    }
    var out = '';
    if (epi) out += '<figure class="ms-desc__epi"><blockquote>' + esc(epi.q) + '</blockquote><figcaption>' + esc(epi.a) + '</figcaption></figure>';
    var leadAt = null;
    parts.some(function (g, gi) { return (!g.head || gi === 0) && g.items.some(function (b) { if (b.k === 'p' && b.text.length > 50) { leadAt = b; return true; } }); });
    if (!leadAt && parts.length && !parts[0].head && parts[0].items[0] && parts[0].items[0].k === 'p') leadAt = parts[0].items[0];
    parts.forEach(function (g) {
      if (g.head) out += '<h4 class="ms-desc__h">' + g.head + '</h4>';
      g.items.forEach(function (b, i) {
        if (b === leadAt) { out += '<p class="ms-desc__lead">' + b.html + '</p>'; return; }
        out += items([b]);
      });
    });
    var fl = box.closest('.ms-pm__sticky') && box.closest('.ms-pm__sticky').querySelector('.ms-pm__facts');
    var have = {};
    if (fl) fl.querySelectorAll('dt').forEach(function (dt) { have[dt.textContent.trim().toLowerCase()] = dt; });
    var rest = '';
    facts.forEach(function (f) {
      var label = f.label ? f.label.charAt(0).toUpperCase() + f.label.slice(1) : L[f.fact];
      var body = items(f.items);
      if (!body) return;
      // measures written one way: 160 × 220, 4 cm
      if (f.fact === 'dims' || f.fact === 'height') {
        body = body.replace(/(\d)\s*[x×X]\s*(?=\d)/g, '$1 × ').replace(/(\d)(cm|mm)\b/gi, function (m, a, u) { return a + ' ' + u.toLowerCase(); });
        // the unit the heading gave ("Sizes (cm)"), written after each bare measure
        if (f.unit) body = body.replace(/(\d)(\s*)(<\/(li|p)>)/g, '$1 ' + f.unit + '$3');
      }
      var dt = have[label.toLowerCase()];
      // a row that only says what every piece shares gives way to what this piece's own text says
      if (fl && dt && dt.parentNode.classList.contains('is-generic')) { dt.nextElementSibling.innerHTML = body; dt.parentNode.classList.remove('is-generic'); dt.parentNode.classList.add('is-from-text'); return; }
      if (fl && !dt) {
        var row = document.createElement('div'); row.className = 'is-from-text';
        row.innerHTML = '<dt>' + esc(label) + '</dt><dd>' + body + '</dd>';
        fl.appendChild(row); have[label.toLowerCase()] = row;
      } else if (fl && dt && dt.parentNode.classList.contains('is-from-text')) {
        dt.nextElementSibling.insertAdjacentHTML('beforeend', body);
      } else if (fl && dt) {
        // the house's own row for this already says it
      } else {
        rest += '<div><dt>' + esc(label) + '</dt><dd>' + body + '</dd></div>';
      }
    });
    if (rest) out += '<dl class="ms-desc__facts">' + rest + '</dl>';
    if (note.length) out += '<div class="ms-desc__note"><span>' + esc(L.order) + '</span>' + note.map(function (n) { return '<p>' + n + '</p>'; }).join('') + '</div>';
    box.innerHTML = out;
    box.classList.add('ms-desc');
    // the line under the name, when it was the start of the description: the lead's first sentence
    var tl = document.querySelector('.ms-pm__tagline[data-ms-auto]');
    var lead = box.querySelector('.ms-desc__lead');
    if (tl && !lead) tl.hidden = true;
    if (tl && lead) {
      var lt = lead.textContent.trim(), first = lt.match(/^.{12,200}?[.!?](\s|$)/), taken = 0;
      if (first) taken = first[0].length;
      else { var cut = lt.slice(0, 200).search(/[:;](?=[^:;]*$)/); if (cut > 40) { first = [lt.slice(0, cut) + '.']; taken = cut + 1; } }
      tl.textContent = first ? first[0].trim() : lt.split(' ').slice(0, 22).join(' ') + '…';
      // what the line under the name already says is not said again just below
      if (first) {
        if (lt.slice(taken).trim().length < 2) {
          lead.parentNode.removeChild(lead);
          var next = box.querySelector(':scope > p:not(.ms-desc__link)');
          if (next && next.textContent.trim().length > 50) next.className = 'ms-desc__lead';
        } else {
          var raw = lead.textContent, skip = raw.length - raw.replace(/^\s+/, '').length + taken;
          var w = document.createTreeWalker(lead, NodeFilter.SHOW_TEXT), n, fresh = true;
          while ((n = w.nextNode())) {
            if (skip > 0) { var c = Math.min(skip, n.nodeValue.length); n.nodeValue = n.nodeValue.slice(c); skip -= c; }
            if (skip <= 0 && fresh) { var r = n.nodeValue.replace(/^[\s:;,.–—-]+/, ''); n.nodeValue = r ? r.charAt(0).toUpperCase() + r.slice(1) : ''; if (r) fresh = false; }
          }
        }
        // nothing left to read here: the section closes rather than stand empty
        if (!box.textContent.trim()) { var dtl = box.closest('details'); if (dtl) dtl.hidden = true; }
      }
    }
    // a lead is a sentence or two: a long first paragraph gives the rest of itself to the text
    var ld = box.querySelector('.ms-desc__lead');
    if (ld && !ld.children.length && ld.textContent.length > 260) {
      var ss2 = ld.textContent.trim().split(/(?<=[.!?])\s+/), head2 = '';
      while (ss2.length > 1 && head2.length < 100) head2 += (head2 ? ' ' : '') + ss2.shift();
      if (ss2.length) { ld.textContent = head2; var rp = document.createElement('p'); rp.textContent = ss2.join(' '); ld.parentNode.insertBefore(rp, ld.nextSibling); }
    }
  })();
