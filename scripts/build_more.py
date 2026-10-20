"""Round nine: the store's other beds (headboards, outdoor), the map's own atlas, the Journal's
subjects, and the smaller things. Runs after build_extra.py, on what it wrote."""
import glob, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from conv import SP, THEME

# ── the agents map draws its own detail: no third-party map, nothing to fail when zooming in
shutil.copy(SP + '/vendor/ms-world-detail.json', THEME + '/assets/ms-world-detail.json')
shutil.copy(SP + '/vendor/ms-world-mid.json', THEME + '/assets/ms-world-mid.json')
shutil.copy(SP + '/vendor/ms-world-layers.json', THEME + '/assets/ms-world-layers.json')   # tools/build_layers.js: Natural Earth 1:10m around the places
if os.path.exists(THEME + '/assets/ms-world-50m.json'):
    os.remove(THEME + '/assets/ms-world-50m.json')
print('map atlas: ok')

# ── the size drawing: a fixed stage, the bed drawn to scale inside it and moving smoothly from one
def size_drawing():
    #    size to the next (nothing around it moves), with its two dimensions written on it like a plan
    p = THEME + '/sections/ms-product-reasons.liquid'
    t = open(p).read()
    OLD_BOX = '<div style="display: flex; align-items: flex-end; gap: 20px; margin-top: 22px;">{{ section.settings.t10 }}</div>'
    NEW_BOX = '''<div class="ms-sz" data-ms-sz>
    <svg class="ms-sz__svg" viewBox="0 0 250 192" aria-hidden="true" focusable="false">
    <defs><pattern id="ms-sz-floor-{{ section.id }}" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="rgba(126,98,59,.11)" stroke-width=".6"/></pattern></defs>
    <rect x="0" y="0" width="250" height="192" fill="url(#ms-sz-floor-{{ section.id }})"/>
    <rect class="ms-sz__ref" data-sz-ref x="0" y="0" width="0" height="0"/>
    <g data-sz-bed><rect class="ms-sz__bed" data-sz-rect x="0" y="0" width="0" height="0" rx="2"/><path class="ms-sz__turn" data-sz-turn d=""/><rect class="ms-sz__pil" data-sz-p1 x="0" y="0" width="0" height="0" rx="3"/><rect class="ms-sz__pil" data-sz-p2 x="0" y="0" width="0" height="0" rx="3"/></g>
    <g class="ms-sz__dim"><path data-sz-dw d=""/><path data-sz-dl d=""/><text data-sz-tw x="0" y="0" text-anchor="middle"></text><text data-sz-tl x="0" y="0" text-anchor="middle"></text></g>
    </svg>
    <div class="ms-sz__txt"><span data-ms-size-name class="ms-sz__name"></span><span data-ms-size-figure class="ms-sz__fig"></span></div>
    </div>'''
    assert OLD_BOX in t
    t = t.replace(OLD_BOX, NEW_BOX, 1)
    OLD_JS = "    var p = root.querySelector('[data-ms-plan]');\n    if (p) { p.style.width = Math.round(d[0] * 0.46) + 'px'; p.style.height = Math.round(d[1] * 0.46) + 'px'; }\n"
    assert OLD_JS in t
    t = t.replace(OLD_JS, "    draw(d);\n", 1)
    DRAW = r'''  var sz = root.querySelector('[data-ms-sz]'), cur = null, raf = 0;
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      var big = dims.reduce(function (m, d) { return [Math.max(m[0], +d[0] || 0), Math.max(m[1], +d[1] || 0)]; }, [0, 0]);
      var S = Math.min(150 / (big[0] || 200), 136 / (big[1] || 210)), CX = 110, TOP = 14;
      function q(sel) { return sz.querySelector(sel); }
      function box(el, x, y, w, h) { el.setAttribute('x', x.toFixed(1)); el.setAttribute('y', y.toFixed(1)); el.setAttribute('width', Math.max(0, w).toFixed(1)); el.setAttribute('height', Math.max(0, h).toFixed(1)); }
      function paint(w, l) {
        var W = w * S, L = l * S, x = CX - W / 2, y = TOP;
        box(q('[data-sz-rect]'), x, y, W, L);
        q('[data-sz-turn]').setAttribute('d', 'M' + (x + 3).toFixed(1) + ' ' + (y + L * .3).toFixed(1) + 'H' + (x + W - 3).toFixed(1));
        var two = w >= 120, pw = two ? (W - 16) / 2 : W - 12, ph = Math.min(18, L * .12);
        box(q('[data-sz-p1]'), x + 6, y + 6, pw, ph);
        box(q('[data-sz-p2]'), two ? x + W - 6 - pw : x, y + 6, two ? pw : 0, two ? ph : 0);
        var yb = y + L + 12, xr = x + W + 12;
        q('[data-sz-dw]').setAttribute('d', 'M' + x.toFixed(1) + ' ' + (yb - 4) + 'v8M' + x.toFixed(1) + ' ' + yb + 'H' + (x + W).toFixed(1) + 'M' + (x + W).toFixed(1) + ' ' + (yb - 4) + 'v8');
        q('[data-sz-dl]').setAttribute('d', 'M' + (xr - 4).toFixed(1) + ' ' + y + 'h8M' + xr.toFixed(1) + ' ' + y + 'V' + (y + L).toFixed(1) + 'M' + (xr - 4).toFixed(1) + ' ' + (y + L).toFixed(1) + 'h8');
        var tw = q('[data-sz-tw]'), tl = q('[data-sz-tl]');
        tw.setAttribute('x', CX); tw.setAttribute('y', yb + 14); tw.textContent = Math.round(w);
        tl.setAttribute('x', xr + 13); tl.setAttribute('y', y + L / 2 + 4); tl.textContent = Math.round(l);
      }
      function draw(d) {
        if (!sz) return;
        var to = [+d[0] || 160, +d[1] || 200];
        if (!big[0]) big = to;
        box(q('[data-sz-ref]'), CX - big[0] * S / 2, TOP, big[0] * S, big[1] * S);
        if (!cur || reduce) { cur = to; paint(to[0], to[1]); return; }
        var from = cur.slice(), t0 = null; cancelAnimationFrame(raf);
        (function step(ts) {
          if (t0 === null) t0 = ts;
          var k = Math.min(1, (ts - t0) / 460), e = 1 - Math.pow(1 - k, 3);
          cur = [from[0] + (to[0] - from[0]) * e, from[1] + (to[1] - from[1]) * e];
          paint(cur[0], cur[1]);
          if (k < 1) raf = requestAnimationFrame(step); else cur = to;
        })(performance.now());
      }
    '''
    OLD_PICK = "  function pick(i) {"
    assert OLD_PICK in t
    t = t.replace(OLD_PICK, DRAW + OLD_PICK, 1)
    OLD_CSS_START = t.index('  .ms-plan {')
    OLD_CSS_END = t.index('  .ms-plan::after { right: 9%; }') + len('  .ms-plan::after { right: 9%; }')
    t = t[:OLD_CSS_START] + '''  .ms-sz { display: flex; align-items: center; gap: 18px; margin-top: 18px; }
      .ms-sz__svg { flex: 0 0 auto; width: 250px; max-width: 62%; height: auto; overflow: visible; }
      .ms-sz__ref { fill: none; stroke: rgba(23, 20, 15, .22); stroke-width: .8; stroke-dasharray: 3 3; }
      .ms-sz__bed { fill: #EFE7D9; stroke: #17140F; stroke-width: 1; }
      .ms-sz__turn { fill: none; stroke: rgba(23, 20, 15, .45); stroke-width: .8; }
      .ms-sz__pil { fill: #FBF9F5; stroke: rgba(23, 20, 15, .5); stroke-width: .8; }
      .ms-sz__dim path { fill: none; stroke: #7E623B; stroke-width: .8; }
      .ms-sz__dim text { font-family: "Red Hat Text", system-ui, sans-serif; font-size: 9.5px; letter-spacing: .08em; fill: #7E623B; font-variant-numeric: tabular-nums; }
      .ms-sz__txt { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
      .ms-sz__name { font-family: Newsreader, Georgia, serif; font-size: 17px; line-height: 1.2; }
      .ms-sz__fig { font-size: 12px; letter-spacing: .1em; font-variant-numeric: tabular-nums; color: #6E675C; }''' + t[OLD_CSS_END:]
    open(p, 'w').write(t)
    print('size drawing: ok')


if 'data-ms-sz' not in open(THEME + '/sections/ms-product-reasons.liquid').read():
    size_drawing()


# ── the fibre marks are never cut: drawn whole whatever the box around them
p = THEME + '/snippets/ms-fibre-mark.liquid'
t = open(p).read()
if 'overflow="visible"' not in t:
    t = t.replace('<svg class="ms-fm ms-fm--{{ ic }}" viewBox="0 0 40 40"', '<svg class="ms-fm ms-fm--{{ ic }}" viewBox="0 0 40 40" overflow="visible" shape-rendering="geometricPrecision"', 1)
    assert 'overflow="visible"' in t
    open(p, 'w').write(t)
print('fibre marks: whole')

# ── the fibre marks drawn again, as filled silhouettes on one grid (icons/marks.py)
sys.path.insert(0, SP + '/icons')
from marks import MARKS
p = THEME + '/snippets/ms-fibre-mark.liquid'
t = open(p).read()
i = t.index('<svg class="ms-fm')
body = ''.join("{%%- when '%s' -%%}%s" % (k, v) for k, v in MARKS.items())
t = t[:i] + ('<svg class="ms-fm ms-fm--{{ ic }}" viewBox="0 0 40 40" width="{{ sz }}" height="{{ sz }}" fill="currentColor" stroke="none" '
             'aria-hidden="true" focusable="false" overflow="visible" shape-rendering="geometricPrecision">{%- case ic -%}' + body + '{%- endcase -%}</svg>\n')
open(p, 'w').write(t)
print('fibre marks: silhouettes,', len(MARKS))

# ── what a product is: a sleep system (with its template key), a bed with headboard, the outdoor
#    Tangram, a boxspring, or something else. Every page that changes with the product asks this.
from beds_data import HANDLE_KEY, SYSTEM_KEYS, BOXSPRING_HANDLES, HEADBOARD, HB_ALIASES, TANGRAM, drawing, y as hy

sys_list = ',' + ','.join(SYSTEM_KEYS) + ','
hk_cases = {}
for h, k in HANDLE_KEY.items():
    hk_cases.setdefault(k, []).append(h)
hb_cases = {}
for h in HEADBOARD:
    hb_cases.setdefault(h, [h])
for a, h in HB_ALIASES.items():
    hb_cases[h].append(a)
lines = ["{%- comment -%}",
         "  What a product is, as 'kind|key|bed': kind is system, headboard, outdoor, boxspring or other;",
         "  key is the sleep system's template (its fibres, cloth and craft), bed the headboard bed's data.",
         "  The template chosen in admin wins; otherwise the store's own handles, then the product type and",
         "  its collections. Generated by bin/build_more.py.",
         "{%- endcomment -%}",
         "{%- liquid",
         "  assign h = p.handle",
         "  assign sfx = p.template_suffix | default: ''",
         "  assign key = ''",
         "  assign bed = ''",
         "  assign kind = 'other'",
         "  assign probe = ',' | append: sfx | append: ','",
         "  if sfx != '' and '%s' contains probe" % sys_list,
         "    assign key = sfx",
         "  else",
         "    case h"]
for k, hs in sorted(hk_cases.items()):
    lines.append("      when %s" % ', '.join("'%s'" % x for x in hs))
    lines.append("        assign key = '%s'" % k)
lines.append("    endcase")
lines.append("  endif")
# the store's handle "roma" was the Roma mohair plaid before it was the Roma bed: a handle that
# names a system but whose product is a plaid or a blanket is not that system
lines += [
    "  if sfx == '' and key != ''",
    "    assign tt = p.title | append: ' ' | append: p.type | downcase",
    "    assign dd = p.description | strip_html | downcase | truncate: 600",
    "    if tt contains 'plaid' or tt contains 'blanket' or tt contains 'throw' or dd contains 'mohair plaid' or dd contains 'this plaid' or dd contains 'this blanket'",
    "      assign key = ''",
    "    endif",
    "  endif"]
# the store gives its Medium & High and Thin toppers the Roma topper's template: told apart by name
lines += [
    "  if key == '' or key == 'topper-roma'",
    "    assign tt = p.title | append: ' ' | append: h | downcase",
    "    if tt contains 'topper'",
    "      unless tt contains 'roma'",
    "        if tt contains 'thin' or tt contains 'sottile'",
    "          assign key = 'topper-thin'",
    "        elsif tt contains 'high' or tt contains 'medium' or tt contains 'alto' or tt contains 'medio'",
    "          assign key = 'topper-high'",
    "        endif",
    "      endunless",
    "    endif",
    "  endif"]
lines.append("  case h")
for k, hs in sorted(hb_cases.items()):
    lines.append("    when %s" % ', '.join("'%s'" % x for x in hs))
    lines.append("      assign bed = '%s'" % k)
lines.append("  endcase")
lines += [
    "  if sfx == 'headboard' and bed == ''",
    "    assign bed = 'pure'",
    "  endif",
    "  assign ty = p.type | downcase",
    "  if key != ''",
    "    assign kind = 'system'",
    "  elsif bed != '' or sfx == 'headboard'",
    "    assign kind = 'headboard'",
    "  elsif h == 'tangram' or sfx == 'tangram' or sfx == 'outdoor' or ty contains 'outdoor'",
    "    assign kind = 'outdoor'",
    "  elsif ty == 'boxspring' or '%s' contains h" % (',' + ','.join(BOXSPRING_HANDLES) + ','),
    "    assign kind = 'boxspring'",
    "  else",
    "    for c in p.collections",
    "      if c.handle == 'beds-with-headboards'",
    "        assign kind = 'headboard'",
    "        break",
    "      elsif c.handle contains 'outdoor'",
    "        assign kind = 'outdoor'",
    "        break",
    "      endif",
    "    endfor",
    "    if kind == 'other' and ty == 'bed'",
    "      assign kind = 'headboard'",
    "    endif",
    "  endif",
    "  echo kind | append: '|' | append: key | append: '|' | append: bed",
    "-%}"]
open(THEME + '/snippets/ms-kind.liquid', 'w').write('\n'.join(lines) + '\n')

# the headboard beds' words
fields = ['title', 'line', 'hb', 'uph', 'width', 'base', 'legs', 'quote', 'author', 'height']
out = ["{%- comment -%} A bed with headboard, in words: {% render 'ms-bed-data', key: 'tulip', part: 'line' %}. Generated by bin/build_more.py from bin/beds_data.py. {%- endcomment -%}",
       "{%- liquid", "  case key"]
for k, d in HEADBOARD.items():
    out.append("    when '%s'" % k)
    out.append("      case part")
    for f in fields:
        v = str(d[f]).replace("'", "’")
        out.append("        when '%s'" % f)
        out.append("          echo '%s'" % v)
    out.append("      endcase")
out += ["  endcase", "-%}"]
open(THEME + '/snippets/ms-bed-data.liquid', 'w').write('\n'.join(out) + '\n')

# the headboard beds' drawings: the bed from its foot, to one scale; crop: true frames it close
out = ["{%- comment -%} The bed, drawn from its foot, to one scale (1 cm = 1.75 units) so that beds side by side compare.",
       "  {% render 'ms-bed-drawing', key: 'tulip', u: section.id, crop: true, l_aria: …, l_headboard: …, l_mattress: …, l_base: … %}",
       "  Generated by bin/build_more.py from bin/beds_data.py. {%- endcomment -%}",
       "{%- assign u = u | default: 'b' | append: key | replace: '-', '' -%}",
       "{%- case key -%}"]
for k, d in HEADBOARD.items():
    svg = drawing(k, '__U__')
    top = max(0, int(hy(max(d['height'], 108)) - 34))
    svg = svg.replace('viewBox="0 0 640 392"', 'viewBox="{%% if crop == \'lineup\' %%}95 96 450 296{%% elsif crop %%}0 %d 640 %d{%% else %%}0 0 640 392{%% endif %%}"' % (top, 392 - top))
    svg = svg.replace('__U__', '{{ u }}').replace('[aria]', '{{ l_aria | escape }}').replace('[headboard]', '{{ l_headboard | escape }}').replace('[mattress]', '{{ l_mattress | escape }}').replace('[base]', '{{ l_base | escape }}')
    out.append("{%%- when '%s' -%%}%s" % (k, svg))
out.append("{%- endcase -%}")
open(THEME + '/snippets/ms-bed-drawing.liquid', 'w').write('\n'.join(out) + '\n')
print('beds: kind, data, drawings')

# ── the product page asks what the product is before speaking of its cloth or showing its sizes
p = THEME + '/sections/ms-product-reasons.liquid'
t = open(p).read()
if 'ms-kind' not in t:
    t = t.replace("{% render 'ms-product-cloth', key: template.suffix, handle: product.handle, part: 'reason' %}",
                  "{%- capture mk -%}{% render 'ms-kind', p: product %}{%- endcapture -%}{%- assign mkp = mk | split: '|' -%}{% render 'ms-product-cloth', key: mkp[1], handle: '', part: 'reason' %}", 1)
    assert 'ms-kind' in t
    # the Tangram is not a bed made to size and regenerated: its own section says what it is
    t = "{%- liquid\n  assign rs_show = true\n  if template.name == 'product' and product != blank\n    capture rk\n      render 'ms-kind', p: product\n    endcapture\n    assign rkp = rk | split: '|'\n    if rkp[0] == 'outdoor' or rkp[0] == 'other'\n      assign rs_show = false\n    endif\n  endif\n-%}\n{%- if rs_show -%}\n" + t
    i = t.index('{% schema %}')
    t = t[:i].rstrip() + '\n{%- endif -%}\n\n' + t[i:]
    open(p, 'w').write(t)

# ── the default product and collection templates carry the beds with headboards and the Tangram
def tpl_load(name):
    raw = open(THEME + '/templates/' + name).read()
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, flags=re.S)
    head = m.group(1) if m else ''
    return head, json.loads(raw[len(head):])


def tpl_save(name, head, data):
    open(THEME + '/templates/' + name, 'w').write(head + json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def insert_after(data, after_type, key, typ, settings=None):
    if any(v['type'] == typ for v in data['sections'].values()):
        return
    data['sections'][key] = {'type': typ, 'settings': settings or {}}
    order = data['order']
    pos = next((i + 1 for i, k in enumerate(order) if data['sections'][k]['type'] == after_type), len(order))
    order.insert(pos, key)


head, d = tpl_load('product.json')
insert_after(d, 'ms-craft', 'bed', 'ms-bed-anatomy')
insert_after(d, 'ms-bed-anatomy', 'tangram', 'ms-tangram')
tpl_save('product.json', head, d)
head, d = tpl_load('collection.json')
insert_after(d, 'ms-collection-intro', 'lineup', 'ms-bed-lineup')
insert_after(d, 'ms-bed-lineup', 'tangram', 'ms-tangram')
tpl_save('collection.json', head, d)
print('templates: beds and Tangram in the defaults')

# ── links: the store's bed systems and outdoor collections, by their real handles
p = THEME + '/snippets/ms-link.liquid'
t = open(p).read()
if "when 'outdoor'" not in t:
    t = t.replace("""    when 'headboards'
      assign c = 'beds-with-headboards,gallery-beds,headboards'""", """    when 'headboards'
      assign c = 'beds-with-headboards,gallery-beds,headboards'
    when 'systems'
      assign c = 'designer-beds,bed-systems,sleep-systems'
    when 'outdoor'
      assign c = 'outdoor-1,outdoor,outdoor-collection'""", 1)
    assert "when 'outdoor'" in t
    open(p, 'w').write(t)

# ── a collection says what it holds: systems, beds, mattresses, pieces
p = THEME + '/sections/ms-collection-intro.liquid'
t = open(p).read()
if 'ms_count_label' not in t:
    t = t.replace("""  assign own = collection.description | strip_html | strip""", """  assign ms_count_label = section.settings.t1
  case collection.handle
    when 'essentials', 'signature', 'icons', 'icon', 'designer-beds'
      assign ms_count_label = section.settings.t1
    when 'beds-with-headboards'
      assign ms_count_label = 'Beds'
    when 'mattresses'
      assign ms_count_label = 'Mattresses'
    when 'mattress-toppers'
      assign ms_count_label = 'Toppers'
    else
      if collection.handle contains 'outdoor'
        assign ms_count_label = 'Pieces'
      elsif collection.handle != 'all'
        assign ms_count_label = 'Pieces'
      endif
  endcase
  assign own = collection.description | strip_html | strip""", 1)
    t = t.replace("{{ section.settings.t1 }}</div><div style=\"font-family: Newsreader, Georgia, serif; font-size: 26px; margin-top: 8px;\">{{ count }}", "{{ ms_count_label }}</div><div style=\"font-family: Newsreader, Georgia, serif; font-size: 26px; margin-top: 8px;\">{{ count }}", 1)
    assert 'ms_count_label }}</div>' in t
    open(p, 'w').write(t)
# a collection without words of its own: its figures stand alone, from the left
p = THEME + '/sections/ms-collection-intro.liquid'
t = open(p).read()
a = '<p style="font-family: Newsreader, Georgia, serif; font-size: clamp(19px, 2.3vw, 27px); line-height: 1.55; font-style: italic; color: rgb(74, 68, 59);">{{ desc }}</p>'
if a in t:
    t = t.replace(a, '{%- if desc != blank -%}' + a + '{%- endif -%}', 1)
    open(p, 'w').write(t)
assert '{%- if desc != blank -%}' in t
print('links and collection intro: ok')

p = THEME + '/sections/ms-qa.liquid'
t = open(p).read()
if 'qa_show' not in t:
    t = "{%- liquid\n  assign qa_show = true\n  if template.name == 'product' and product != blank\n    capture qk\n      render 'ms-kind', p: product\n    endcapture\n    assign qkp = qk | split: '|'\n    if qkp[0] == 'outdoor' or qkp[0] == 'other'\n      assign qa_show = false\n    endif\n  endif\n-%}\n{%- if qa_show -%}\n" + t
    i = t.index('{% schema %}')
    t = t[:i].rstrip() + '\n{%- endif -%}\n\n' + t[i:]
    open(p, 'w').write(t)
print('questions: beds only')

# ── the house's collections, by their real handles, in the menus and on the collections page
p = THEME + '/snippets/ms-link.liquid'
t = open(p).read()
if "when 'throws'" not in t:
    t = t.replace("""    when 'bedding'
      assign c = 'duvets,bedding,bed-linen,gallery-blankets-and-throws'""", """    when 'bedding'
      assign c = 'duvets,bed-sheets,bedding,bed-linen'
    when 'throws'
      assign c = 'gallery-blankets-and-throws,blankets-and-throws,throws'
    when 'cushions'
      assign c = 'cushions-and-screens,cushions'
    when 'lamps'
      assign c = 'gallery-lamps,lamps'
    when 'wallcoverings'
      assign c = 'wallcovering-and-fabrics,wallcoverings'
    when 'treasures'
      assign c = 'midsummer-treasures,treasures'""", 1)
    assert "when 'throws'" in t
    open(p, 'w').write(t)
p = THEME + '/snippets/ms-mega.liquid'
t = open(p).read()
old_types = """        {%- assign types = 'mattresses,toppers,headboards,bedding,furniture' | split: ',' -%}
        {%- assign type_names = 'Mattresses,Toppers,Beds with headboards,Duvets and sheets,Furniture' | split: ',' -%}"""
if old_types in t:
    t = t.replace(old_types, """        {%- assign types = 'systems,headboards,mattresses,toppers,outdoor,bedding,throws,furniture' | split: ',' -%}
        {%- assign type_names = 'Bed systems,Beds with headboards,Mattresses,Toppers,Outdoor,Duvets and sheets,Blankets and throws,Furniture' | split: ',' -%}""", 1)
    open(p, 'w').write(t)
p = THEME + '/sections/ms-header.liquid'
t = open(p).read()
anchor = '</div><div data-ms-msub="heritage"'
if 'ms-mkinds' not in t:
    kinds = ("<div class=\"ms-mkinds\">{%- assign mk_types = 'systems,headboards,mattresses,toppers,outdoor,bedding,throws,furniture' | split: ',' -%}"
             "{%- assign mk_names = 'Bed systems,Beds with headboards,Mattresses,Toppers,Outdoor,Duvets and sheets,Blankets and throws,Furniture' | split: ',' -%}"
             "{%- for t in mk_types -%}{%- capture tu -%}{% render 'ms-link', to: t, strict: true %}{%- endcapture -%}"
             "{%- if tu != blank -%}<a href=\"{{ tu }}\">{{ mk_names[forloop.index0] }}</a>{%- endif -%}{%- endfor -%}</div>"
             "<style>.ms-mkinds { display: flex; flex-wrap: wrap; gap: 8px 18px; padding: 16px 0 6px; border-top: 1px solid rgb(221, 214, 201); } .ms-site .ms-mkinds a { font-size: 14px; color: #17140F; border-bottom: 1px solid #DDD6C9; padding-bottom: 3px; }</style>")
    assert t.count(anchor) == 1
    t = t.replace(anchor, kinds + anchor, 1)
    open(p, 'w').write(t)
for name in ('list-collections.json', 'page.collections.json'):
    head, d = tpl_load(name)
    for k, v in d['sections'].items():
        if v['type'] == 'ms-beds-03':
            d['sections'][k] = {'type': 'ms-collection-index', 'settings': {}}
    tpl_save(name, head, d)

# the "Our beds" menu in the same order as the collection pages' own navigation: by kind, then
# the rest of the bedroom, then the help to choose; the three collections stay the cards
p = THEME + '/snippets/ms-mega.liquid'
t = open(p).read()
if 'ms-mg__grp' not in t:
    a = t.index('      <ul class="ms-mg__minor" role="list">')
    b = t.index('      </ul>', a) + len('      </ul>')
    t = t[:a] + """      {%- assign groups = 'systems,headboards,mattresses,toppers,outdoor|bedding,throws,furniture' | split: '|' -%}
      {%- assign group_names = 'By kind|For the bedroom' | split: '|' -%}
      {%- assign all_names = 'systems:Bed systems,headboards:Beds with headboards,mattresses:Mattresses,toppers:Toppers,outdoor:Outdoor,bedding:Duvets and sheets,throws:Blankets and throws,furniture:Furniture' | split: ',' -%}
      {%- for g in groups -%}
        {%- assign gl = '' -%}
        {%- assign keys = g | split: ',' -%}
        {%- for t in keys -%}
          {%- capture tu -%}{% render 'ms-link', to: t, strict: true %}{%- endcapture -%}
          {%- if tu != blank -%}
            {%- for n in all_names -%}{%- assign np = n | split: ':' -%}{%- if np[0] == t -%}{%- assign gl = gl | append: '<li><a href="' | append: tu | append: '">' | append: np[1] | append: '</a></li>' -%}{%- endif -%}{%- endfor -%}
          {%- endif -%}
        {%- endfor -%}
        {%- if gl != '' -%}<p class="ms-mg__grp">{{ group_names[forloop.index0] }}</p><ul class="ms-mg__minor" role="list">{{ gl }}</ul>{%- endif -%}
      {%- endfor -%}
      <p class="ms-mg__grp">Choosing</p>
      <ul class="ms-mg__minor" role="list">
        <li><a href="{{ u_compare }}">{{ ss.mg_compare }}</a></li>
        <li><a href="{{ u_quiz }}" data-ms-quiz-link>{{ ss.mg_quiz }}</a></li>
        <li><a href="{{ u_proposal }}#enquire" data-ms-landing>{{ ss.mg_proposal }}</a></li>
      </ul>""" + t[b:]
    t = t.replace("  .ms-mg__minor { list-style: none; margin: 30px 0 0; padding: 22px 0 0; border-top: 1px solid #DDD6C9; display: grid; gap: 10px; }",
                  "  .ms-mg__minor { list-style: none; margin: 0; padding: 0; display: grid; gap: 9px; }\n  .ms-mg__grp { margin: 22px 0 10px; padding-top: 16px; border-top: 1px solid #DDD6C9; font-family: Newsreader, Georgia, serif; font-size: 14px; color: #9A8F7E; }\n  .ms-mg__grp:first-of-type { margin-top: 26px; }", 1)
    assert 'ms-mg__grp {' in t
    open(p, 'w').write(t)
print('collections: index, menus, links')

# ── the Journal's subjects: weighted, tested on the store's own notes (bin/journal_subjects.py)
from journal_subjects import liquid as subjects_liquid
open(THEME + '/snippets/ms-note-cat.liquid', 'w').write(subjects_liquid())
print('journal: subjects')

# ── the Journal's notes read like a page of a book, whatever the editor left in them:
#    empty paragraphs and double breaks go, bold lines become headings, pasted fonts give way,
#    the spacing is one rhythm; the reading time is whole minutes; sharing has its marks
SHARE_ICONS = {
    'WhatsApp': '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M12 3.2a8.7 8.7 0 0 0-7.5 13.1L3.3 20.8l4.6-1.2A8.7 8.7 0 1 0 12 3.2Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/><path d="M9.2 8.3c.2-.4.5-.4.7-.4h.5c.2 0 .4.1.5.4l.7 1.6c.1.2 0 .5-.1.6l-.5.6c-.1.2-.1.4 0 .5.6 1 1.5 1.8 2.5 2.3.2.1.4.1.5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.2.1.3.3.3.5v.4c0 .5-.4 1.2-1.4 1.4-1 .2-2.4-.2-4.1-1.6-1.9-1.6-2.6-3.3-2.6-4.3 0-.8.4-1.5.6-1.9Z" fill="currentColor"/></svg>',
    'LinkedIn': '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M8 10.3v6.2M8 7.6v.1M11.2 16.5v-6.2M11.2 13c0-1.7 1-2.8 2.4-2.8 1.3 0 2.2.9 2.2 2.6v3.7" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>',
    'Pinterest': '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><circle cx="12" cy="12" r="8.7" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M11.2 9.2c.8-1.4 3.8-1.6 4.3.5.5 2-1 4.4-2.8 4.1-1.1-.2-1.3-1.2-1.1-1.9M11.9 11.4l-2 8.4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
    'Email': '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M4 6.5l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>',
    'Copy': '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M10.3 13.7a3.6 3.6 0 0 0 5.1 0l3.1-3.1a3.6 3.6 0 0 0-5.1-5.1l-1.2 1.2M13.7 10.3a3.6 3.6 0 0 0-5.1 0l-3.1 3.1a3.6 3.6 0 0 0 5.1 5.1l1.2-1.2" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>',
}
NORMALIZE = r'''<script>
  /* the note, put in order before it is read: nothing of its words is changed */
  (function () {
    var body = document.currentScript.previousElementSibling;
    if (!body || !body.classList.contains('ms-article-body')) return;
    var blank = function (el) { return !el.querySelector('img, iframe, video, svg, picture, table, hr') && !(el.textContent || '').replace(/[\s ​]+/g, ''); };
    body.querySelectorAll('meta, link, style, o\\:p').forEach(function (el) { el.remove(); });
    body.querySelectorAll('[style]').forEach(function (el) { if (!/^(IMG|IFRAME|VIDEO)$/.test(el.tagName)) el.removeAttribute('style'); });
    body.querySelectorAll('[data-mce-fragment], [data-mce-style]').forEach(function (el) { el.removeAttribute('data-mce-fragment'); el.removeAttribute('data-mce-style'); });
    // wrappers around whole blocks (a div from another editor, a pasted bold or span) are taken away
    var BLOCK = 'p, h1, h2, h3, h4, h5, h6, ul, ol, blockquote, figure, table, div, section';
    for (var pass = 0; pass < 6; pass++) {
      var wraps = Array.prototype.filter.call(body.querySelectorAll('div, section, article, main, header, footer, b, strong, span, font'), function (w) {
        return w.querySelector(BLOCK) && !w.querySelector('iframe, video') && !w.closest('li, table, blockquote');
      });
      if (!wraps.length) break;
      wraps.forEach(function (w) { if (!w.parentNode) return; while (w.firstChild) w.parentNode.insertBefore(w.firstChild, w); w.remove(); });
    }
    body.querySelectorAll('span, font').forEach(function (el) { if (!el.attributes.length || el.tagName === 'FONT' || /^s\d+$/.test(el.className)) { while (el.firstChild) el.parentNode.insertBefore(el.firstChild, el); el.remove(); } });
    // a div holding only words is a paragraph
    body.querySelectorAll('div').forEach(function (d) { if (!d.querySelector('div, p, ul, ol, table, figure, img, iframe, h1, h2, h3, h4, h5, h6')) { var p = document.createElement('p'); while (d.firstChild) p.appendChild(d.firstChild); d.replaceWith(p); } });
    // two line breaks are a new paragraph
    Array.prototype.slice.call(body.querySelectorAll('p')).forEach(function (p) {
      var kids = Array.prototype.slice.call(p.childNodes), parts = [[]], last = null;
      kids.forEach(function (n) {
        var isBr = n.nodeName === 'BR', ws = n.nodeType === 3 && !n.textContent.trim();
        if (isBr && last === 'br') { parts.push([]); last = 'split'; return; }
        if (isBr && last === 'split') return;
        if (ws) { parts[parts.length - 1].push(n); return; }
        if (isBr) { parts[parts.length - 1].push(n); last = 'br'; return; }
        last = null; parts[parts.length - 1].push(n);
      });
      if (parts.length < 2) return;
      parts.forEach(function (ns) {
        while (ns.length && (ns[ns.length - 1].nodeName === 'BR' || (ns[ns.length - 1].nodeType === 3 && !ns[ns.length - 1].textContent.trim()))) ns.pop();
        if (!ns.length) return;
        var q = document.createElement('p'); ns.forEach(function (n) { q.appendChild(n); }); p.parentNode.insertBefore(q, p);
      });
      p.remove();
    });
    // a paragraph of several long lines (each a sentence, or a bold label and its words) becomes
    // one line each, with a little air between, so a wrapped line is not mistaken for the next
    Array.prototype.slice.call(body.querySelectorAll(':scope > p')).forEach(function (p) {
      var lines = [[]];
      Array.prototype.slice.call(p.childNodes).forEach(function (n) { if (n.nodeName === 'BR') lines.push([]); else lines[lines.length - 1].push(n); });
      lines = lines.filter(function (ns) { return ns.some(function (n) { return (n.textContent || '').trim(); }); });
      if (lines.length < 2) return;
      var len = lines.map(function (ns) { return ns.map(function (n) { return n.textContent || ''; }).join('').trim().length; });
      var long = len.filter(function (l) { return l >= 38; }).length;
      if (long < lines.length - 1) return;
      var labelled = lines.every(function (ns) { var f = ns.filter(function (n) { return !(n.nodeType === 3 && !n.textContent.trim()); })[0]; return f && /^(B|STRONG)$/.test(f.nodeName); });
      lines.forEach(function (ns) { var q = document.createElement('p'); q.className = 'ms-art-line' + (labelled ? ' ms-art-line--item' : ''); ns.forEach(function (n) { q.appendChild(n); }); p.parentNode.insertBefore(q, p); });
      p.remove();
    });
    // in a list item that opens with a bold question, the break after it is the bold's own
    body.querySelectorAll('li').forEach(function (li) { var k = Array.prototype.filter.call(li.childNodes, function (n) { return !(n.nodeType === 3 && !n.textContent.trim()); }); if (k.length > 1 && /^(B|STRONG)$/.test(k[0].nodeName) && k[1].nodeName === 'BR') k[1].remove(); });
    // stray breaks at the end of a paragraph, and paragraphs with nothing in them
    body.querySelectorAll('p, li').forEach(function (p) { var n = p.lastChild; while (n && (n.nodeName === 'BR' || (n.nodeType === 3 && !n.textContent.trim()))) { var prev = n.previousSibling; n.remove(); n = prev; } });
    body.querySelectorAll('p, div, h1, h2, h3, h4, h5, h6, li').forEach(function (el) { if (blank(el)) el.remove(); });
    // one level of headings in the note: a bold line on its own is one too
    body.querySelectorAll('h1').forEach(function (h) { var n = document.createElement('h2'); n.innerHTML = h.innerHTML; h.replaceWith(n); });
    body.querySelectorAll('h4, h5, h6').forEach(function (h) { var n = document.createElement('h3'); n.innerHTML = h.innerHTML; h.replaceWith(n); });
    // empty inline wrappers and breaks at the edge of bold text say nothing
    body.querySelectorAll('i, em, b, strong, u').forEach(function (el) { if (blank(el)) el.remove(); });
    body.querySelectorAll('b, strong').forEach(function (el) { var n = el.lastChild; while (n && n.nodeName === 'BR') { el.parentNode.insertBefore(n, el.nextSibling); n = el.lastChild; } });
    // a bold line followed by a break, at the head of a paragraph, is that paragraph's heading
    Array.prototype.slice.call(body.querySelectorAll(':scope > p')).forEach(function (p) {
      var k = Array.prototype.filter.call(p.childNodes, function (n) { return !(n.nodeType === 3 && !n.textContent.trim()); });
      if (k.length > 2 && /^(B|STRONG)$/.test(k[0].nodeName) && k[1].nodeName === 'BR') {
        var t = k[0].textContent.trim();
        if (t.length > 2 && t.length < 110 && !/[.,;:]$/.test(t)) { var h = document.createElement('h3'); h.textContent = t; p.parentNode.insertBefore(h, p); k[0].remove(); k[1].remove(); }
      }
    });
    body.querySelectorAll('p').forEach(function (p) {
      var els = Array.prototype.filter.call(p.childNodes, function (n) { return !(n.nodeType === 3 && !n.textContent.trim()) && n.nodeName !== 'BR'; });
      var t = p.textContent.trim();
      if (els.length === 1 && /^(B|STRONG)$/.test(els[0].nodeName) && t.length > 2 && t.length < 110 && !/[.,;]$/.test(t)) { var h = document.createElement('h3'); h.textContent = t; p.replaceWith(h); }
    });
    // the first paragraph opens the note; a short last line from the team signs it
    var ps = body.querySelectorAll(':scope > p');
    if (ps.length) { ps[0].classList.add('ms-art-lede'); var l = ps[ps.length - 1], lt = l.textContent.trim(); if (ps.length > 2 && lt.length < 70 && /(team|midsummer|chiara|atelier)/i.test(lt) && !/[.?!]$/.test(lt)) l.classList.add('ms-art-sign'); }
    // a paragraph that is only a link is an invitation
    body.querySelectorAll(':scope > p').forEach(function (p) { var k = Array.prototype.filter.call(p.childNodes, function (n) { return !(n.nodeType === 3 && !n.textContent.trim()); }); if (k.length === 1 && k[0].nodeName === 'A' && k[0].textContent.trim().length < 80) p.classList.add('ms-art-cta'); });
    body.querySelectorAll(':scope > p').forEach(function (p) { if (p.querySelector('img') && !p.textContent.trim()) p.classList.add('ms-art-pic'); });
    body.classList.add('is-tidy');
  })();
</script>'''
TIDY_CSS = '''
  /* one rhythm for every note, whatever its editor left behind */
  .ms-site .ms-article-body.is-tidy { display: block; font-size: 17px !important; line-height: 1.8 !important; }
  .ms-site .ms-article-body.is-tidy > * { margin: 0; }
  .ms-site .ms-article-body.is-tidy > * + * { margin-top: 1.2em; }
  .ms-site .ms-article-body.is-tidy > h2 { margin-top: 2.4em; padding-top: 0; border-top: 0; font-size: clamp(28px, 2.8vw, 36px); line-height: 1.15; }
  .ms-site .ms-article-body.is-tidy > h3 { margin-top: 2em; font-weight: 300; font-size: clamp(21px, 2vw, 25px); line-height: 1.3; }
  .ms-site .ms-article-body.is-tidy > h2 + h3 { margin-top: .7em; color: #4A443B; }
  .ms-site .ms-article-body.is-tidy > h2 + *, .ms-site .ms-article-body.is-tidy > h3 + * { margin-top: .7em; }
  .ms-site .ms-article-body.is-tidy > :first-child { margin-top: 0; padding-top: 0; border-top: 0; }
  .ms-site .ms-article-body.is-tidy > ol, .ms-site .ms-article-body.is-tidy > ul, .ms-site .ms-article-body.is-tidy > blockquote { margin-top: 1.6em; }
  .ms-site .ms-article-body.is-tidy > ol + *, .ms-site .ms-article-body.is-tidy > ul + *, .ms-site .ms-article-body.is-tidy > blockquote + * { margin-top: 1.6em; }
  .ms-site .ms-article-body.is-tidy .ms-art-line + .ms-art-line { margin-top: .55em; }
  .ms-site .ms-article-body.is-tidy .ms-art-line--item { padding-left: 18px; position: relative; }
  .ms-site .ms-article-body.is-tidy .ms-art-line--item::before { content: ''; position: absolute; left: 0; top: .9em; width: 7px; border-top: 1px solid #B5AA97; }
  .ms-site .ms-article-body.is-tidy .ms-art-lede { font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: clamp(21px, 2vw, 25px); line-height: 1.55; color: #17140F; padding-left: 0; }
  .ms-site .ms-article-body.is-tidy .ms-art-lede::before { display: none; }
  .ms-site .ms-article-body.is-tidy .ms-art-cta a { display: inline-flex; align-items: center; gap: 10px; font-size: 11.5px; letter-spacing: .24em; text-transform: uppercase; text-decoration: none; border-bottom: 1px solid #17140F; padding-bottom: 6px; color: #17140F; }
  .ms-site .ms-article-body.is-tidy .ms-art-sign { font-family: Newsreader, Georgia, serif; font-style: italic; font-size: 19px; line-height: 1.5; color: #4A443B; margin-top: 2.6em; padding-top: 22px; border-top: 1px solid #DDD6C9; padding-left: 0; }
  .ms-site .ms-article-body.is-tidy .ms-art-sign::before { display: none; }
  .ms-site .ms-article-body.is-tidy .ms-art-sign em, .ms-site .ms-article-body.is-tidy .ms-art-sign i { display: block; font-size: 15px; color: #7E623B; }
  .ms-site .ms-article-body.is-tidy ol > li { line-height: 1.65; }
  .ms-site .ms-article-body.is-tidy ol > li strong:first-child, .ms-site .ms-article-body.is-tidy ol > li b:first-child { margin-bottom: 6px; }
  .ms-site .ms-article-body .ms-art-pic { margin-top: 1.8em; margin-bottom: .6em; }
  .ms-site .ms-article-body li + li { margin-top: .45em; }
  .ms-site .ms-article-body ol > li + li { margin-top: 0; }
  .ms-site .ms-article-body b, .ms-site .ms-article-body strong { font-weight: 500; color: #17140F; }
  .ms-site .ms-article-body [style] { font-size: inherit !important; line-height: inherit !important; font-family: inherit !important; color: inherit !important; background: none !important; }
  .ms-site .ms-article-body > p:empty { display: none; }
  .ms-site .ms-art-share a, .ms-site .ms-art-share button { display: inline-flex; align-items: center; gap: 10px; }
  .ms-art-share svg { flex: 0 0 auto; color: #7E623B; }
  .ms-site .ms-art-share a:hover svg, .ms-site .ms-art-share button:hover svg { color: #17140F; }
'''
p = THEME + '/sections/ms-article.liquid'
t = open(p).read()
if 'is-tidy' not in t:
    t = t.replace("{%- assign minutes = words | divided_by: 200 | at_least: 1 -%}", "{%- assign minutes = words | plus: 199 | divided_by: 200 | floor | at_least: 1 -%}", 1)
    t = t.replace("{{ article.content }}\n  </div>", "{{ article.content }}\n  </div>\n" + NORMALIZE, 1)
    for label, key in (('WhatsApp</a>', 'WhatsApp'), ('LinkedIn</a>', 'LinkedIn'), ('Pinterest</a>', 'Pinterest'), ('">Email</a>', 'Email')):
        i = t.index(label)
        j = t.rindex('>', 0, i + (2 if label.startswith('"') else 0)) + 1
        t = t[:j] + SHARE_ICONS[key] + t[j:]
    t = t.replace("<button type=\"button\" data-ms-copy=\"{{ shop.url | append: article.url }}\">{{ section.settings.copy | default: 'Copy link' }}</button>",
                  "<button type=\"button\" data-ms-copy=\"{{ shop.url | append: article.url }}\">" + SHARE_ICONS['Copy'] + "<span>{{ section.settings.copy | default: 'Copy link' }}</span></button>", 1)
    i = t.rindex('</style>')
    t = t[:i] + TIDY_CSS + t[i:]
    t = t.replace("var t = b.textContent; (navigator.clipboard", "var s = b.querySelector('span') || b, t = s.textContent; (navigator.clipboard", 1)
    t = t.replace("b.textContent = '✓'; setTimeout(function () { b.textContent = t; }, 1600);", "s.textContent = '✓'; setTimeout(function () { s.textContent = t; }, 1600);", 1)
    assert 'is-tidy' in t and t.count('<svg viewBox="0 0 24 24" width="15"') >= 5, t.count('<svg viewBox="0 0 24 24" width="15"')
    open(p, 'w').write(t)
print('article: tidy notes, share marks')

# ── Inside the bed, drawn for each system: its cloths, ribbons, stitching, legs, drawers, shape
from craft_draw import drawing as craft_drawing
from lp_data import CRAFT as _CRAFT
out = ["{%- comment -%} The bed drawn for each system (snippets/ms-kind gives the key): its own cloths, ribbons,",
       "  stitching, legs, drawers or round shape; parts it does not include in outline. Generated by",
       "  bin/build_more.py from bin/craft_draw.py. {%- endcomment -%}", "{%- case key -%}"]
def craft_liq(svg):
    return svg.replace('{{U}}', '{{ u }}').replace('[aria]', '{{ aria | escape }}').replace('[t1]', '{{ t1 | escape }}').replace('[t2]', '{{ t2 | escape }}').replace('[t3]', '{{ t3 | escape }}').replace('[t0]', '{{ t0 | escape }}').replace('[to]', '{{ to | escape }}')
# One snippet per system (Shopify refuses any Liquid file over 256 KB; all of them in one file
# came to 280 KB, and the upload dropped it). This snippet only picks the right one.
CRAFT_ARGS = ", u: u, aria: aria, t0: t0, to: to, t1: t1, t2: t2, t3: t3 %}"
craft_files = set()
for k, c in _CRAFT.items():
    name = 'ms-craft-svg-' + k
    craft_files.add(name + '.liquid')
    open(THEME + '/snippets/' + name + '.liquid', 'w').write(craft_liq(craft_drawing(k, c['kind'])) + '\n')
    out.append("{%%- when '%s' -%%}{%%- render '%s'%s" % (k, name, CRAFT_ARGS))
craft_files.add('ms-craft-svg-system.liquid')
open(THEME + '/snippets/ms-craft-svg-system.liquid', 'w').write(craft_liq(craft_drawing('', 'system')) + '\n')
out.append("{%- else -%}{%- render 'ms-craft-svg-system'" + CRAFT_ARGS)
out.append("{%- endcase -%}")
open(THEME + '/snippets/ms-craft-svg.liquid', 'w').write('\n'.join(out) + '\n')
for f in os.listdir(THEME + '/snippets'):
    if f.startswith('ms-craft-svg-') and f not in craft_files:
        os.remove(THEME + '/snippets/' + f)
# what completes a mattress, a topper or a boxspring (Inside the bed, for the parts it does not include)
from lp_data import MATES as _MATES, SPARE as _SPARE
ml = ["{%- comment -%}",
      "  What completes a product in Inside the bed: for a part it does not include (topper, mattress or",
      "  base), its own companions first, then the store's collection of that kind, else the house's own",
      "  pieces. Output: first link^the collection's link^first image^the list's items. Generated by",
      "  bin/build_more.py from bin/lp_data.py.",
      "{%- endcomment -%}",
      "{%- liquid",
      "  assign own = ''",
      "  case key"]
for k, v in _MATES.items():
    ml.append("    when '%s'" % k)
    first = True
    for part, hs in v.items():
        ml.append("      %s part == '%s'" % ('if' if first else 'elsif', part))
        ml.append("        assign own = '%s'" % hs)
        first = False
    ml.append("      endif")
ml += ["  endcase",
       "  case part"]
for part, place in (('topper', 'toppers'), ('mattress', 'mattresses'), ('base', 'bases')):
    ml += ["    when '%s'" % part, "      assign place = '%s'" % place, "      assign spare = '%s'" % _SPARE[part]]
ml += ["  endcase",
       "  capture chs",
       "    render 'ms-link', to: place, handles: true",
       "  endcapture",
       "  assign col = nil",
       "  assign chl = chs | strip | split: ','",
       "  for ch in chl",
       "    assign cc = collections[ch]",
       "    if cc != blank and cc.products_count > 0",
       "      assign col = cc",
       "      break",
       "    endif",
       "  endfor",
       "  assign seen = ','",
       "  if product != blank",
       "    assign seen = seen | append: product.handle | append: ','",
       "  endif",
       "  assign hs = own",
       "  if col == nil",
       "    assign hs = hs | append: ',' | append: spare",
       "  endif",
       "  assign hs = hs | split: ','",
       "  assign n = 0",
       "  assign first = ''",
       "  assign img = ''",
       "  assign items = ''",
       "  for h in hs",
       "    if h == blank or n >= 3",
       "      continue",
       "    endif",
       "    assign mp = all_products[h]",
       "    if mp == blank or mp.handle == blank",
       "      continue",
       "    endif",
       "    capture mk",
       "      render 'ms-kind', p: mp",
       "    endcapture",
       "    assign mk = mk | split: '|' | first",
       "    if mk == 'other'",
       "      continue",
       "    endif",
       "    assign probe = ',' | append: mp.handle | append: ','",
       "    if seen contains probe",
       "      continue",
       "    endif",
       "    assign seen = seen | append: mp.handle | append: ','",
       "    capture it",
       "      render 'ms-craft-mate', mp: mp",
       "    endcapture",
       "    assign items = items | append: it",
       "    if first == ''",
       "      assign first = mp.url",
       "      if mp.featured_image",
       "        assign img = mp.featured_image | image_url: width: 900",
       "      endif",
       "    endif",
       "    assign n = n | plus: 1",
       "  endfor",
       "  if col != nil",
       "    for mp in col.products limit: 8",
       "      if n >= 3",
       "        break",
       "      endif",
       "      assign probe = ',' | append: mp.handle | append: ','",
       "      if seen contains probe",
       "        continue",
       "      endif",
       "      assign seen = seen | append: mp.handle | append: ','",
       "      capture it",
       "        render 'ms-craft-mate', mp: mp",
       "      endcapture",
       "      assign items = items | append: it",
       "      if first == ''",
       "        assign first = mp.url",
       "        if mp.featured_image",
       "          assign img = mp.featured_image | image_url: width: 900",
       "        endif",
       "      endif",
       "      assign n = n | plus: 1",
       "    endfor",
       "  endif",
       "  assign all = ''",
       "  if col != nil",
       "    assign all = col.url",
       "    if first == ''",
       "      assign first = col.url",
       "    endif",
       "  endif",
       "  echo first | append: '^' | append: all | append: '^' | append: img | append: '^' | append: items",
       "-%}"]
open(THEME + '/snippets/ms-craft-mates.liquid', 'w').write('\n'.join(ml) + '\n')
open(THEME + '/snippets/ms-craft-mate.liquid', 'w').write(
    "{%- comment -%} One piece that completes the bed, in Inside the bed: its photograph and its name, leading to its page. Generated by bin/build_more.py. {%- endcomment -%}\n"
    "<li><a class=\"ms-cr__mate\" href=\"{{ mp.url }}\"><span class=\"ms-cr__mimg\">{%- if mp.featured_image -%}<img src=\"{{ mp.featured_image | image_url: width: 160 }}\" alt=\"\" width=\"80\" height=\"80\" loading=\"lazy\">{%- endif -%}</span><span class=\"ms-cr__mname\">{{ mp.title | escape }}</span><span class=\"ms-cr__marr\" aria-hidden=\"true\">→</span></a></li>\n")
print('craft mates:', len(_MATES))
from craft_draw import tint as craft_tint
tl = ["{%- comment -%} The craft section's ground for each system: the house's warm paper, touched by the colour of its base. Generated by bin/build_more.py. {%- endcomment -%}", "{%- case key -%}"]
for k in _CRAFT:
    tl.append("{%%- when '%s' -%%}%s" % (k, craft_tint(k)))
tl.append("{%- endcase -%}")
open(THEME + '/snippets/ms-craft-tint.liquid', 'w').write('\n'.join(tl) + '\n')
print('craft drawings:', len(_CRAFT))

# ── the beds are made by hand in Italy; Milan is where the house and its atelier are
ITALY = [
    ('Two artisans, start to finish, in our Milan atelier.', 'Two artisans, start to finish, in Italy.'),
    ('Two artisans, start to finish, in our Milan atelier', 'Two artisans, start to finish, in Italy'),
    ('Handmade in Milan', 'Handmade in Italy'),
    ('A house of beds, made by hand in Milan.', 'A house of beds from Milan, made by hand in Italy.'),
    ('each built to order by two artisans in Milan', 'each built to order by two Italian artisans'),
    ('The beds are made in Milano and can be lain on there.', 'The beds are made by hand in Italy, and can be lain on at the atelier in Milano.'),
    (', in our atelier on Via Andegari. That', '. That'),
    (' in our atelier on Via Andegari.', '.'),
    ('made by hand in Milan', 'made by hand in Italy'),
    ('By hand, in Milan', 'By hand, in Italy'),
    ('made in Milan by hand', 'made by hand in Italy'),
    ('handmade in Milan', 'handmade in Italy'),
    ('specified and built in Italy by the Midsummer Milano atelier', 'specified with the Midsummer Milano atelier and made by hand in Italy'),
    ('the system the atelier would build for you', 'the system we would make for you'),
    ('Where every system is made, and can be lain on.', 'Where every system can be seen, specified and lain on.'),
    ('It gives the mattress its springiness and keeps air moving through the core.', 'It gives the mattress its resilience and keeps the air moving through it.'),
    ('at fifteen years the atelier opens, cleans and rebuilds the mattress, by hand, for fifteen more', 'at fifteen years it goes back to our artisans in Italy, who renew it by hand for fifteen more'),
    ('fifteen years, then fifteen more after the atelier renews it by hand', 'fifteen years, then fifteen more once our artisans have renewed it by hand'),
    ('The cloth, cut by hand at the atelier.', 'The cloth, cut by hand by our artisans.'),
    ('fibres before they are laid, and the atelier at work', 'fibres as they arrive, and our artisans at work'),
    ('the Midsummer Milano system the atelier would build for you', 'the Midsummer Milano system we would make for you'),
]
n_it = 0
for f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/templates/*.json') + glob.glob(THEME + '/snippets/ms-*.liquid') + [THEME + '/snippets/meta-tags.liquid'] + glob.glob(THEME + '/locales/*.json'):
    t = open(f).read(); u = t
    for a, b in ITALY:
        u = u.replace(a, b)
    if u != t:
        n_it += 1
        open(f, 'w').write(u)
print('made in Italy:', n_it, 'files')

# ── Instagram: the house's latest posts, through a feed address (Theme settings) or an app block. The feed
# service holds the Instagram connection, so no token is ever written into the page (Round 18).
p = THEME + '/config/settings_schema.json'
raw = open(p).read()
if 'ms_instagram_feed' not in raw or 'ms_instagram_token' in raw:
    sch = json.loads(raw)
    for grp in sch:
        if grp.get('name') == 'Midsummer · Social and WhatsApp':
            grp['settings'] = [x for x in grp['settings'] if x.get('id') not in ('ms_instagram_token', 'ms_instagram_feed')]
            i = next(i for i, x in enumerate(grp['settings']) if x.get('id') == 'ms_social_instagram')
            grp['settings'][i + 1:i + 1] = [
                {"type": "text", "id": "ms_instagram_feed", "label": "Instagram feed address (latest posts)",
                 "info": "Optional. A JSON feed address, e.g. from behold.so, shows the latest posts. See INSTALL.md, section 41."}]
    open(p, 'w').write(json.dumps(sch, indent=2, ensure_ascii=False) + '\n')
print('instagram: feed setting')

# ── natural materials: each fibre at its source (licensed photographs, toned as one series: scripts/fibre_plates.py)
keep = set()
for f in glob.glob(SP + '/vendor/fibres/ms-fibre-photo-*.jpg'):
    shutil.copy(f, THEME + '/assets/' + os.path.basename(f)); keep.add(os.path.basename(f))
for f in glob.glob(THEME + '/assets/ms-fibre-photo-*.jpg'):
    if os.path.basename(f) not in keep:
        os.remove(f)
FIBRE_BLOCKS = [
    ('fibre', {'photo': 'vicuna', 'name': 'Vicuña', 'latin': 'Vicugna vicugna', 'origin': 'The Andes, Peru',
               'line': 'The rarest and finest fibre we work with: silky, light and remarkably warm.'}),
    ('fibre', {'photo': 'yak', 'name': 'Yak', 'latin': 'Bos grunniens', 'line': 'Fine, warm and particularly robust, with a softness close to cashmere.'}),
    ('fibre', {'photo': 'cashmere', 'name': 'Cashmere', 'latin': 'Capra hircus', 'line': 'The fine undercoat of the goat: warmth without weight.'}),
    ('fibre', {'photo': 'wool', 'name': 'Wool', 'latin': 'Ovis aries', 'line': 'Long, resilient fibres that hold their shape, night after night.'}),
    ('fibre', {'photo': 'silk', 'name': 'Silk', 'latin': 'Bombyx mori', 'line': 'Cool to the touch and smooth, with a lustre of its own.'}),
    ('fibre', {'photo': 'horsehair', 'name': 'Horsehair', 'latin': 'Equus caballus', 'line': 'Long and resilient; it keeps the air moving through the bed.'}),
    ('fibre', {'photo': 'cotton', 'name': 'Cotton', 'latin': 'Gossypium', 'line': 'Fresh and breathable, for the warmer months.'}),
]


def fibre_gallery(name, after_type):
    head, d = tpl_load(name)
    if any(v['type'] == 'ms-fibre-gallery' for v in d['sections'].values()):
        return
    insert_after(d, after_type, 'fibres', 'ms-fibre-gallery')
    blocks, order = {}, []
    for i, (typ, st) in enumerate(FIBRE_BLOCKS):
        k = '%s_%d' % (typ, i + 1)
        blocks[k] = {'type': typ, 'settings': st}
        order.append(k)
    d['sections']['fibres']['blocks'] = blocks
    d['sections']['fibres']['block_order'] = order
    tpl_save(name, head, d)


# ── natural materials: one atlas of the fibres, where the plates and the cards used to stand apart
#    (sections/ms-fibre-atlas; its words and figures in bin/fibre_atlas.py, from the catalogue)
from fibre_atlas import ATLAS, SLUG_NAMES
from fibre_draw import draw as fibre_draw, STYLE as DRAW_STYLE
for f in glob.glob(THEME + '/assets/ms-fibre-draw-*.svg'):
    os.remove(f)
for slug in DRAW_STYLE:
    open(THEME + '/assets/ms-fibre-draw-%s.svg' % slug, 'w').write(fibre_draw(slug))
# the world in dots, for the atlas's "Where it comes from" (tools/gen/dotworld.js, Natural Earth 50m)
shutil.copy(SP + '/vendor/ms-fibre-world.svg', THEME + '/assets/ms-fibre-world.svg')
# the store's own Natural materials page may use the default page template: there too, the atlas
# (shown only on that page, like the default template's other designed sections)
_OURS = sorted(os.path.basename(f)[5:-5] for f in glob.glob(THEME + '/templates/page.*.json'))
_p = THEME + '/sections/ms-fibre-atlas.liquid'
_s = open(_p).read()
if 'ms_show' not in _s:
    _gate = ("{%%- liquid\n  assign ms_show = true\n  if template.name == 'page'\n    assign ms_show = false\n"
             "    assign ms_ours = '%s' | split: ','\n    if ms_ours contains template.suffix\n      assign ms_show = true\n    else\n"
             "      capture ms_key\n        render 'ms-page-key'\n      endcapture\n      if ms_key == 'materials'\n        assign ms_show = true\n      endif\n"
             "    endif\n  endif\n-%%}\n{%%- if ms_show -%%}\n") % ','.join(_OURS)
    _i = _s.index('{% schema %}')
    _s = _gate + _s[:_i].rstrip() + '\n{%- endif -%}\n\n' + _s[_i:]
    open(_p, 'w').write(_s)
for _f in ('page.natural-materials.json', 'collection.ms-materials.json', 'page.json'):
    _h, _d = tpl_load(_f)
    _anchor = 'ms-banner'
    if _f == 'page.json':
        _ks = [k for k in _d['order'] if _d['sections'][k]['type'] in ('ms-materials-01', 'ms-materials-02')]
        if _ks:
            _pos = _d['order'].index(_ks[0])
            _anchor = _d['sections'][_d['order'][_pos - 1]]['type']
    for _k in [k for k, v in _d['sections'].items() if v['type'] in ('ms-fibre-gallery', 'ms-materials-02', 'ms-materials-01')]:
        del _d['sections'][_k]
        _d['order'].remove(_k)
    for _k in [k for k, v in _d['sections'].items() if v['type'] == 'ms-fibre-atlas']:
        _blocks = {}
        for i, st in enumerate(ATLAS, 1):
            _blocks['fibre_%d' % i] = {'type': 'fibre', 'settings': st}
        _d['sections'][_k]['blocks'] = _blocks
        _d['sections'][_k]['block_order'] = list(_blocks)
    if not any(v['type'] == 'ms-fibre-atlas' for v in _d['sections'].values()):
        insert_after(_d, _anchor, 'atlas', 'ms-fibre-atlas', {
            'heading': 'Chosen for what they do to your sleep.',
            'text': 'Our mattresses and bed bases are made only with natural materials, chosen for their quality, durability and comfort. '
                    'They come from farms where animals are treated ethically: cashmere only from Mongolia, horsehair from Argentina, '
                    'where horses live free, and wool from small farms. Read them by what matters most to you.'})
        blocks = {}
        for i, st in enumerate(ATLAS, 1):
            blocks['fibre_%d' % i] = {'type': 'fibre', 'settings': st}
        _d['sections']['atlas']['blocks'] = blocks
        _d['sections']['atlas']['block_order'] = list(blocks)
    tpl_save(_f, _h, _d)
# which beds are made with each fibre: by system key, from the systems' own fibre lists
from lp_data import FIBRES as _SYSF
from beds_data import HANDLE_KEY as _HK
_TITLE = {'top-2': 'Top', 'vivaldi-2': 'Vivaldi', 'dreamy-2': 'Dreamy', 'giotto': 'Giotto Round', 'vicuna': 'Vicuña', 'my-dream': 'My Dream',
          'topper-roma': 'Roma Topper', 'topper-high': 'Medium & High Topper', 'topper-thin': 'Thin Topper', 'vivaldi-plus': 'Vivaldi Plus',
          'ultra-dry': 'Ultra Dry', 'dreamy-springs': 'Dreamy Springs', 'first-dream': 'First Dream'}
_out = ["{%- comment -%} The beds made with a fibre, by the atlas's fibre: part 'keys' (system keys, as snippets/ms-kind gives them) or 'names'. Generated by bin/build_more.py from bin/lp_data.py. {%- endcomment -%}",
        "{%- case fibre -%}"]
for slug, names in SLUG_NAMES.items():
    keys = [k for k, fl in _SYSF.items() if any(n in fl for n in names)]
    titles = [_TITLE.get(k, k.replace('-', ' ').title()) for k in keys]
    _out.append("{%%- when '%s' -%%}{%%- if part == 'names' -%%}%s{%%- else -%%}%s{%%- endif -%%}" % (slug, '|'.join(titles), ','.join(keys)))
_out.append("{%- endcase -%}")
open(THEME + '/snippets/ms-fibre-beds.liquid', 'w').write('\n'.join(_out) + '\n')
# a fibre's place in the atlas, from any of its names (the product pages link each fibre there)
_sl = ["{%- comment -%} A fibre's entry in the Natural materials atlas (#fibre-<slug>), from its name. Generated by bin/build_more.py. {%- endcomment -%}",
       "{%- assign fname = name | downcase | strip -%}", "{%- case fname -%}"]
for slug, names in SLUG_NAMES.items():
    _sl.append("{%%- when %s -%%}%s" % (', '.join("'%s'" % n.lower() for n in names), slug))
_sl.append("{%- endcase -%}")
open(THEME + '/snippets/ms-fibre-slug.liquid', 'w').write('\n'.join(_sl) + '\n')
print('materials: one atlas,', len(ATLAS), 'fibres')
FIBRE_ALT = {'vicuna': 'Four vicuñas on a ridge at dusk.', 'yak': 'A yak on a misty mountainside.', 'cashmere': 'A herd of goats coming down a mountain valley.', 'wool': 'Sheep in full fleece, close together.', 'silk': 'Silk satin falling in soft folds, catching the light.', 'horsehair': 'The long, pale mane of a horse, close up.', 'cotton': 'Cotton bolls opening on the plant.'}
for _f in ('page.natural-materials.json', 'collection.ms-materials.json'):
    _h, _d = tpl_load(_f)
    _ch = False
    for _s in _d['sections'].values():
        if _s['type'] != 'ms-fibre-gallery': continue
        for _b in _s.get('blocks', {}).values():
            _k = _b.get('settings', {}).get('photo')
            if _k in FIBRE_ALT and _b['settings'].get('alt') != FIBRE_ALT[_k]:
                _b['settings']['alt'] = FIBRE_ALT[_k]; _ch = True
    if _ch: tpl_save(_f, _h, _d)

print('materials: fibres up close')

# ── projects: postcards on a map of Italy, on the blogs named in the theme settings
it = json.load(open(SP + '/vendor/italy.json'))
open(THEME + '/snippets/ms-italy-map.liquid', 'w').write(
    '{%- comment -%} Italy and its neighbours for the projects map, generated from the atlas (tools/build_italy.js). {%- endcomment -%}\n'
    '<path class="ms-pj__near" d="' + it['nd'] + '"></path><path class="ms-pj__it" d="' + it['d'] + '"></path>\n')
open(THEME + '/snippets/ms-italy-places.liquid', 'w').write(
    '{%- comment -%} Places a project can name: key|name|x|y, in the map\'s own coordinates, most particular first. {%- endcomment -%}\n'
    + ';'.join('%s|%s|%s|%s' % (k, n, x, y) for k, n, x, y in it['places']) + '\n')
p = THEME + '/config/settings_schema.json'
sch = json.loads(open(p).read())
if 'ms_projects_blogs' not in json.dumps(sch):
    for grp in sch:
        if grp.get('name') == 'Midsummer · Where links go':
            grp['settings'].append({"type": "text", "id": "ms_projects_blogs", "label": "Blogs shown as projects", "default": "projects,hotels,progetti,portfolio",
                                    "info": "Blog handles, separated by commas. These blogs show as postcards on a map of Italy instead of the Journal list."})
    open(p, 'w').write(json.dumps(sch, indent=2, ensure_ascii=False) + '\n')
GUARD = """{%- liquid
  assign ms_pj_blogs = settings.ms_projects_blogs | default: 'projects,hotels,progetti,portfolio' | downcase | remove: ' ' | split: ','
  assign ms_pj_skip = false
  if blog and ms_pj_blogs contains blog.handle
    assign ms_pj_skip = true
  endif
-%}
{%- unless ms_pj_skip -%}
"""
for name in ('ms-journal-head', 'ms-journal-list'):
    p = THEME + '/sections/' + name + '.liquid'
    t = open(p).read()
    if 'ms_pj_skip' in t:
        continue
    i = t.index('{% schema %}')
    m = re.match(r'(\{%-? comment -?%\}.*?\{%-? endcomment -?%\}\s*)', t, flags=re.S)
    start = m.end() if m else 0
    t = t[:start] + GUARD + t[start:i].rstrip() + '\n{%- endunless -%}\n' + t[i:]
    open(p, 'w').write(t)
head, d = tpl_load('blog.json')
insert_after(d, 'ms-journal-head', 'projects', 'ms-projects')
tpl_save('blog.json', head, d)
print('projects: map of Italy,', len(it['places']), 'places')

# ── 15 + 15: thirty years side by side, an industrial mattress against one of ours
REGEN_STAGES = [
    (0, 'New.', 'It takes a few weeks to learn your shape. Then it keeps it.'),
    (3, 'Settled.', 'The fibres have found their place. So have you.'),
    (8, 'The age most mattresses are thrown away.', 'Ours is just getting comfortable.'),
    (15, 'A short visit to Italy.', 'It comes home to our artisans: inspected, its wool recarded by hand, the outer renewed only where it needs it.'),
    (16, 'Fifteen years more.', 'Back in its room. Same structure, same fabric, same character.'),
    (24, 'Still not tired.', 'Neither, with luck, are you.'),
    (30, 'Thirty.', 'One mattress, thirty years. A fairly good argument for doing things slowly.'),
]


def regen_years(name):
    head, d = tpl_load(name)
    if any(v['type'] == 'ms-regen-years' for v in d['sections'].values()):
        return
    insert_after(d, 'ms-regen-04', 'years', 'ms-regen-years')
    tpl_save(name, head, d)


for f in glob.glob(THEME + '/templates/*.json'):
    # page.json, the catch-all page, already holds Shopify's limit of 25 sections
    if '"ms-regen-04"' in open(f).read() and os.path.basename(f) != 'page.json':
        regen_years(os.path.basename(f))
print('regeneration: thirty years in one line')

# ── at a glance: the house in six figures, all taken from the facts below them
FIGURES = [
    ('2014', False, 'Founded in Milan', 'By an architect who wanted the bed designed like the rest of the room.'),
    ('2', True, 'Artisans per bed', 'Start to finish, one bed at a time.'),
    ('14', True, 'Natural fibres', 'From Cheviot wool and horsehair to vicuña.'),
    ('15 + 15', False, 'Years', 'Fifteen, a short visit to Italy, fifteen more.'),
    ('8', True, 'Countries with our beds on show', 'From Milano to Hong Kong.'),
    ('0', False, 'Tooling charges', 'Not even for a round bed.'),
]
for name in ('page.facts.json', 'collection.ms-facts.json'):
    if not os.path.exists(THEME + '/templates/' + name):
        continue
    head, d = tpl_load(name)
    if any(v['type'] == 'ms-figures' for v in d['sections'].values()):
        continue
    insert_after(d, 'ms-facts', 'figures', 'ms-figures')
    d['sections']['figures']['blocks'] = {'fig_%d' % i: {'type': 'figure', 'settings': {'number': n, 'count': c, 'label': l, 'line': x}} for i, (n, c, l, x) in enumerate(FIGURES)}
    d['sections']['figures']['block_order'] = ['fig_%d' % i for i in range(len(FIGURES))]
    tpl_save(name, head, d)
print('facts: six figures')

# ── what each sleep product is (bed system, mattress, topper), from the catalogue, and the small
#    drawings that say it on the collection pages
whats = {}
for k, v in _CRAFT.items():
    whats.setdefault(v['kind'], []).append(k)
lines = ["{%- comment -%} What a sleep product is, by its key (snippets/ms-kind): system, mattress or topper. From the 2026 catalogue (bin/lp_data.py), generated by bin/build_more.py. {%- endcomment -%}",
         "{%- case key -%}"]
for kind in ('mattress', 'topper', 'system'):
    if kind == 'system':
        continue
    lines.append("{%- when " + ", ".join("'%s'" % k for k in sorted(whats.get(kind, []))) + " -%}" + kind)
lines.append("{%- else -%}system{%- endcase -%}")
open(THEME + '/snippets/ms-what.liquid', 'w').write('\n'.join(lines) + '\n')
GLYPHS = {
    # a topper on a mattress on its boxspring
    'system': '<rect x="3.5" y="4" width="25" height="2.6" rx="1.3"/><rect x="3" y="7.6" width="26" height="4.6" rx="1.6"/><path d="M4 13.2h24v3.2H4z"/><path d="M6.5 16.4v2M25.5 16.4v2"/>',
    # a mattress, tufted
    'mattress': '<rect x="3" y="6.5" width="26" height="7" rx="2.2"/><path d="M9 10h.01M16 10h.01M23 10h.01" stroke-width="1.8"/>',
    # a topper, thin and soft
    'topper': '<path d="M3.5 11.2c0-1.2.9-2 2.1-2h20.8c1.2 0 2.1.8 2.1 2s-.9 2-2.1 2H5.6c-1.2 0-2.1-.8-2.1-2z"/><path d="M8.5 11.2h.01M16 11.2h.01M23.5 11.2h.01" stroke-width="1.6"/>',
    # a boxspring on its legs
    'boxspring': '<path d="M4 8h24v6H4z"/><path d="M4 11h24" opacity=".45"/><path d="M7 14v3.5M25 14v3.5"/>',
    # a bed with its headboard
    'headboard': '<path d="M3.5 17V5.2c0-.9.7-1.6 1.6-1.6h2.8c.9 0 1.6.7 1.6 1.6V17"/><rect x="9.5" y="9" width="19" height="3.6" rx="1.3"/><path d="M9.5 12.6h19v2.8h-19"/><path d="M27 15.4v2.2"/>',
    # Tangram: a square and a triangle
    'outdoor': '<path d="M4 16.5h12L10 10.5z"/><rect x="17" y="8.5" width="8" height="8" transform="rotate(0 21 12.5)"/><path d="M10 10.5l6-6 6 4"/>',
}
g = ["{%- comment -%} A small drawing of what a product is: kind is system, mattress, topper, boxspring, headboard or outdoor. Generated by bin/build_more.py. {%- endcomment -%}",
     "{%- case kind -%}"]
for k, d in GLYPHS.items():
    g.append("{%- when '" + k + "' -%}<svg class=\"ms-kg ms-kg--" + k + "\" viewBox=\"0 0 32 20\" width=\"32\" height=\"20\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\" focusable=\"false\" overflow=\"visible\" shape-rendering=\"geometricPrecision\">" + d + "</svg>")
g.append("{%- endcase -%}")
open(THEME + '/snippets/ms-kind-glyph.liquid', 'w').write('\n'.join(g) + '\n')
print('collections: what each product is, drawn')

# ── one hand for every small icon: the social marks in fine line, like the share row; the
#    sustainability columns' handmade and repair marks drawn again (needle and thread, a stitched seam)
LINE = 'fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"'
SOCIAL_LINE = {
    'instagram': '<rect x="3.5" y="3.5" width="17" height="17" rx="5" %s/><circle cx="12" cy="12" r="4" %s/><path d="M16.9 7.1h.01" %s stroke-width="2"/>' % (LINE, LINE, LINE),
    'pinterest': '<circle cx="12" cy="12" r="8.8" %s/><path d="M11 9.1c.9-1.5 4.2-1.7 4.8.6c.6 2.2-1.1 4.9-3.2 4.6c-1.2-.2-1.5-1.3-1.2-2.1M11.8 11.5l-2.2 9" %s/>' % (LINE, LINE),
    'linkedin': '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5" %s/><path d="M8 10.4v6.2M8 7.6v.1M11.3 16.6v-6.2M11.3 13.1c0-1.7 1-2.8 2.4-2.8c1.3 0 2.2.9 2.2 2.6v3.7" %s/>' % (LINE, LINE),
    'whatsapp': '<path d="M12 3.3a8.7 8.7 0 0 0-7.5 13.1l-1.2 4.4l4.6-1.2A8.7 8.7 0 1 0 12 3.3z" %s/><path d="M9.2 8.4c.2-.4.5-.4.7-.4h.5c.2 0 .4.1.5.4l.7 1.6c.1.2 0 .5-.1.6l-.5.6c-.1.2-.1.4 0 .5c.6 1 1.5 1.8 2.5 2.3c.2.1.4.1.5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.2.1.3.3.3.5v.4c0 .5-.4 1.2-1.4 1.4c-1 .2-2.4-.2-4.1-1.6c-1.9-1.6-2.6-3.3-2.6-4.3c0-.8.4-1.5.6-1.9z" fill="currentColor"/>' % LINE,
    'telegram': '<path d="M20.6 4.2L3.6 10.8c-.8.3-.8 1.4 0 1.6l4.2 1.3l1.6 5c.2.7 1.1.9 1.6.4l2.4-2.3l4.3 3.2c.6.4 1.4.1 1.6-.6l2.6-14c.2-.8-.6-1.4-1.3-1.2z" %s/><path d="M7.8 13.7l9.4-6.2l-7.2 7.6" %s/>' % (LINE, LINE),
}
p = THEME + '/snippets/ms-social.liquid'
t = open(p).read()
for n, body in SOCIAL_LINE.items():
    m = re.search(r"\{%%- when '%s' -%%\}.*?(?=\{%%- when|\{%%- endcase)" % n, t, flags=re.S)
    assert m, n
    t = t[:m.start()] + "{%%- when '%s' -%%}%s\n            " % (n, body) + t[m.end():]
open(p, 'w').write(t)
SUS = {
    'M6 21 V13 C6 9 9 6 12 6 C15 6 18 9 18 13 V21':    # handmade: a needle and its thread
        '<svg aria-hidden="true" height="22" style="display: block; flex: 0 0 auto;" viewBox="0 0 24 24" width="22" fill="none" stroke="#7E623B" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.6 19.4L16.4 7.6"/><ellipse cx="17.9" cy="6.1" rx="2.2" ry="1" transform="rotate(-45 17.9 6.1)"/><path d="M19.1 4.9c2.2 1.6 1.8 5-1 6.2c-2.4 1-3.4 3.4-2.4 5.6c.8 1.8 2.8 2.6 4.6 2"/></svg>',
    'M14 4 L20 10 L16 14 L10 8 Z':                     # repairable: a seam, stitched by hand
        '<svg aria-hidden="true" height="22" style="display: block; flex: 0 0 auto;" viewBox="0 0 24 24" width="22" fill="none" stroke="#7E623B" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7.2c3 1.2 6 1.2 9 0s6-1.2 9 0M3 16.8c3-1.2 6-1.2 9 0s6 1.2 9 0" stroke-opacity=".55"/><path d="M3.5 12h17"/><path d="M6.2 9.4l2.2 5.2M10.4 9.4l2.2 5.2M14.6 9.4l2.2 5.2"/></svg>',
}
n_sus = 0
for f in glob.glob(THEME + '/sections/*.liquid'):
    t = open(f).read(); u = t
    for key, svg in SUS.items():
        u = re.sub(r'<svg[^>]*>(?:(?!</svg>).)*?' + re.escape(key) + r'.*?</svg>', svg, u, flags=re.S)
    if u != t:
        n_sus += 1; open(f, 'w').write(u)
print('icons: fine-line socials; handmade and repair marks in', n_sus, 'sections')

# ── the professional pages and the atelier: a specification drawing, a project's steps, the
#    thirty years per room, and the atelier's week
STEPS = [
    ('The drawing', 'Send us the room: the plan, the elevations and the bed\'s place in it.'),
    ('The specification', 'Dimensions, firmness, fibres and cloth, set with one person at the atelier.'),
    ('The samples', 'Cloths and fibres sent to your studio, to be chosen against the room.'),
    ('The making', 'By hand in Italy, by two artisans, from start to finish.'),
    ('The delivery', 'By our own team: brought into the room, assembled and dressed.'),
]


def add_section(name, after_type, key, typ, settings=None, blocks=None):
    if not os.path.exists(THEME + '/templates/' + name):
        return
    head, d = tpl_load(name)
    if any(v['type'] == typ and k == key for k, v in d['sections'].items()):
        return
    insert_after(d, after_type, key, typ, settings)
    if blocks:
        d['sections'][key]['blocks'] = {'%s_%d' % (b[0], i): {'type': b[0], 'settings': b[1]} for i, b in enumerate(blocks)}
        d['sections'][key]['block_order'] = ['%s_%d' % (blocks[i][0], i) for i in range(len(blocks))]
    tpl_save(name, head, d)


for name in ('page.professionals.json', 'collection.ms-professionals.json'):
    add_section(name, 'ms-pro-02', 'spec', 'ms-spec')
    add_section(name, 'ms-spec', 'steps', 'ms-steps', None, [('step', {'title': t, 'text': x}) for t, x in STEPS])
HOSP_SPEC = {'eyebrow': 'For every room', 'heading': 'Drawn to the plan of each room.',
             'text': 'Each bed is made to order: for a suite, a villa or a cabin, width, length and height are set to the plan, and the cloth to the room.'}
HOSP_YEARS = {'eyebrow': 'Thirty years, per room', 'heading': 'One bed per room, for thirty years.',
              'text': 'An industrial mattress is replaced every eight to ten years. A Midsummer mattress goes back to the artisans who made it at fifteen, and returns to the room for fifteen more.'}
for name in ('page.hospitality.json', 'collection.ms-hospitality.json'):
    add_section(name, 'ms-hosp-02', 'spec', 'ms-spec', HOSP_SPEC)
    add_section(name, 'ms-hosp-03', 'years', 'ms-regen-years', HOSP_YEARS)
for name in ('page.atelier.json', 'collection.ms-atelier.json'):
    add_section(name, 'ms-statement', 'hours', 'ms-hours', {'map_url': 'https://www.google.com/maps/search/?api=1&query=Via+Andegari+4+20121+Milano'})
print('professionals, hospitality, atelier: drawing, steps, thirty years, hours')

# ── one catalogue navigation under the opening of every collection page (sections/ms-cat-nav)
add_section('collection.json', 'ms-collection-hero', 'catnav', 'ms-cat-nav')
for name in ('collection.ms-essentials.json', 'collection.ms-signature.json', 'collection.ms-icons.json'):
    add_section(name, 'ms-banner', 'catnav', 'ms-cat-nav')
print('collections: one navigation, by kind and by collection')


# ── the product's description, as plain words for search engines: paragraphs kept apart by a space
p = THEME + '/sections/ms-seo.liquid'
t = open(p).read()
a = '"description": {{ product.description | strip_html | truncate: 600 | json }},'
if a in t:
    t = t.replace(a, '"description": {{ product.description | newline_to_br | replace: \'<br />\', \' \' | replace: \'</p>\', \' </p>\' | replace: \'</h4>\', \' </h4>\' | replace: \'</li>\', \' </li>\' | strip_html | split: \' \' | join: \' \' | truncate: 600 | json }},', 1)
    open(p, 'w').write(t)
assert 'product.description | strip_html | truncate: 600' not in t
print('seo: product description in plain words')

# ── the fibres, named the same everywhere: the fourteen of the Natural materials atlas (bin/fibre_atlas.py)
FIBRE_LISTS = [
    ('Baby alpaca, Cheviot wool, horsehair, vegetable horsehair, yak hair, mohair, cashmere, silk, linen, organic cotton and Orange Fiber',
     'Baby alpaca, camel hair, Cheviot and Falkland wool, horsehair, vegetable horsehair, yak hair, mohair, cashmere, silk, linen, organic cotton, Ingeo and Orange Fiber'),
    ('Baby alpaca, Cheviot wool, horsehair, vegetable horsehair, yak, mohair, cashmere, silk, linen, organic cotton and Orange Fiber',
     'Baby alpaca, camel hair, Cheviot and Falkland wool, horsehair, vegetable horsehair, yak, mohair, cashmere, silk, linen, organic cotton, Ingeo and Orange Fiber'),
]
_n = 0
for f in glob.glob(THEME + '/templates/*.json') + glob.glob(THEME + '/sections/*.liquid'):
    s = open(f).read()
    s2 = s
    for a, b in FIBRE_LISTS:
        s2 = s2.replace(a, b)
    if s2 != s:
        open(f, 'w').write(s2); _n += 1
print('fibres named alike in', _n, 'files')

# ── on a phone the four social marks stay on one line in the footer's narrow column
p = THEME + '/snippets/ms-social.liquid'
t = open(p).read()
a = '  .ms-social { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }'
if a in t and 'ms-social-narrow' not in t:
    t = t.replace(a, a + '\n  /* ms-social-narrow */ @media (max-width: 600px) { .ms-social { gap: 5px; } .ms-site .ms-social a { width: 35px; height: 35px; } }', 1)
    open(p, 'w').write(t)
assert 'ms-social-narrow' in t
print('socials: one line on a phone')

# the agents map's street map: MapLibre GL 5.24.0 (BSD-3-Clause, vendor/maplibre-LICENSE.txt), and
# the house's map style (bin/map_style.py), inline on the page
shutil.copy(SP + '/vendor/ms-maplibre.js', THEME + '/assets/ms-maplibre.js')
shutil.copy(SP + '/vendor/ms-maplibre.css', THEME + '/assets/ms-maplibre.css')
from map_style import style as _map_style
_ms = json.dumps(_map_style(), separators=(',', ':'), ensure_ascii=False)
assert '{{' not in _ms and '{%' not in _ms and '</' not in _ms
open(THEME + '/snippets/ms-map-style.liquid', 'w').write(_ms + '\n')
print('street map: MapLibre', os.path.getsize(THEME + '/assets/ms-maplibre.js') // 1024, 'KB; style', len(_ms) // 1024, 'KB')

# ── claims, as the house's own audit asked (Oct 2026): nothing literal that production across the
#    workshops might not bear out. No "two artisans" or "the same two hands", no count of systems,
#    no promise about tooling charges; what stays is what every bed is: made by hand in Italy, to
#    order, one at a time, to the client's drawing.
CLAIMS = [
    ('how a Midsummer bed is made, by two artisans, start to finish.', 'how a Midsummer bed is made, by hand, start to finish.'),
    ('Any diameter, with no tooling charge.', 'Any diameter, made to measure.'),
    ('Any dimension, height or radius, round beds included, with no tooling charge.', 'Any dimension, height or radius, round beds included, made to your drawing.'),
    ('Any size, including round, with no tooling charge', 'Made to measure, round included'),
    ('Any size, round included, with no tooling charge.', 'Made to measure, round included.'),
    ('Any width, length or height, round beds included, with no tooling charge.', 'Any width, length or height, round beds included, made to your drawing.'),
    ('Any width, length or shape, round included, is made to order without tooling charges.', 'Any width, length or shape, round included, is made to order.'),
    ('By hand in Italy, by two artisans, from start to finish.', 'By hand in Italy, from start to finish.'),
    ('By hand in Italy, by two artisans, start to finish', 'By hand in Italy, to order'),
    ('By hand in Italy, one by one, by two artisans, start to finish.', 'By hand in Italy, one by one, start to finish.'),
    ('are worked to your drawing, with no tooling charge.', 'are worked to your drawing.'),
    ('made by hand in Italy, by the same two artisans, from natural fibres only.', 'made by hand in Italy, from natural fibres only.'),
    ('is made to order by two artisans, which means', 'is made to order, which means'),
    ('Every bed is made by two artisans, start to finish.', 'Every bed is made by hand in Italy, to order, one at a time.'),
    ('by hand in Italy by two artisans, from natural fibres', 'by hand in Italy, from natural fibres'),
    ('Every piece is built by hand, from start to finish, by the same two Italian artisans:', 'Every piece is built by hand in Italy, from start to finish:'),
    ('Every sleep system is built by hand, one by one, by two artisans, start to finish.', 'Every sleep system is built by hand, one by one, start to finish.'),
    ('Every sleep system is built one by one by two artisans, start to finish — the same two hands that begin the bed sew its final seam.', 'Every sleep system is built by hand, one by one, from the first stitch to the final seam.'),
    ('round beds included, without tooling charges.', 'round beds included.'),
    ('is made by hand in Italy by the same two artisans, from natural fibres only.', 'is made by hand in Italy, from natural fibres only.'),
    ('Handmade in Italy, by two artisans', 'Handmade in Italy, to order'),
    ('built one by one by two artisans in Italy', 'built one by one, by hand, in Italy'),
    ('How a Midsummer bed is made: two artisans in Italy tuft, stitch and finish every mattress, topper and boxspring by hand, from start to finish.',
     'How a Midsummer bed is made: in Italy, every mattress, topper and boxspring is tufted, stitched and finished by hand, from start to finish.'),
    ('It is made to order by two artisans, start to finish.', 'It is made to order, by hand, one at a time.'),
    ('It is made, by the same two pairs of hands, from the core to the last stitch.', 'It is made, by hand, from the first gesture to the last stitch.'),
    ('is made, by the same two pairs of hands, from the core to the last stitch', 'is made, by hand, from the first gesture to the last stitch'),
    ('are worked to your drawing. No tooling charge.', 'are worked to your drawing.'),
    ('Non-standard widths, heights and radii — including round — without tooling charges.', 'Non-standard widths, heights and radii — including round — worked to your drawing.'),
    ('Non-standard widths, heights and radii, including round, carry no tooling charge.', 'Non-standard widths, heights and radii, round included, are worked to your drawing.'),
    ('returns to the two artisans who made it', 'returns to the artisans who made it'),
    ('The same two artisans for every bed in the programme.', 'Every bed in the programme made by hand in Italy.'),
    ('No production line. The same two hands begin the bed and sew its final seam.', 'No production line: each bed is made by hand, from the first stitch to the final seam.'),
    ('The same two hands begin the bed and sew its final seam.', 'Begun and finished by hand, to the final seam.'),
    ('The same two hands that begin the bed sew its final seam, which is why', 'Each bed is made by hand from the first stitch to the last, which is why'),
    ('The same two, from the first stitch to the last.', 'By hand, from the first stitch to the last.'),
    ('Then two artisans make the bed, start to finish, and our own team delivers it.', 'Then the bed is made by hand, start to finish, and our own team delivers it.'),
    ('All twenty-four →', 'All systems →'),
    ('Three collections, twenty-four systems, made to your dimensions.', 'Three collections, every system made to your dimensions.'),
    ('Twenty-four systems in three collections, each built to order by two Italian artisans.', 'Three collections of systems, each built to order by hand in Italy.'),
    ('Twenty-four systems in three collections, each one built to order.', 'Three collections of systems, each one built to order.'),
    ('Twenty-four systems in three collections.', 'Three collections of systems.'),
    ('Two artisans build each system start to finish, in Italy.', 'Each system is built by hand, start to finish, in Italy.'),
    ('Two artisans build your system, start to finish.', 'Your system is built by hand, start to finish.'),
    ('Two artisans, by hand, start to finish, in Italy', 'By hand, start to finish, in Italy'),
    ('Two artisans, start to finish, in Italy.', 'By hand, start to finish, in Italy.'),
    ('Two artisans, one bed', 'One bed at a time'),
    ('Two artisans. One bed.', 'By hand. One bed at a time.'),
    ('Two artisans.<br/>One bed.', 'By hand.<br/>One bed at a time.'),
    ('the bed is finished by the same two people who started it.', 'the bed is finished by hand, as it was begun.'),
    ('"label": "No production line. The same two h…"', '"label": "No production line…"'),
    ('"label": "The same two hands open the spring…"', '"label": "Text"'),
    ('"label": "Twenty-four systems in three colle…"', '"label": "Three collections…"'),
    ('"label": "Two artisans build each system sta…"', '"label": "Each system is built by hand…"'),
    ('"label": "Two artisans build your system, st…"', '"label": "Your system is built by hand…"'),
    ('"label": "Two artisans.One bed."', '"label": "By hand. One bed at a time."'),
    # the publications, spelt as they spell themselves
    ('"name": "L Officiel"', '"name": "L’Officiel"'),
    ('"name": "Festival dell Etica"', '"name": "Festival dell’Etica"'),
    ('"name": "Lust und Leben"', '"name": "Lust & Leben"'),
    ('"label": "Please proceed with your enquiry."', '"label": "Heading"'),
    ('"default": "Please proceed with your enquiry."', '"default": "Write to the atelier."'),
    # natural fibres, without "only": a boxspring for contract use is not all fibre inside
    ('Hand-built, natural fibres only', 'Hand-built, in natural fibres'),
    ('from natural fibres only', 'from natural fibres'),
    ('No line, no tooling to amortise, no minimum run.', 'No production line and no minimum run.'),
    ('Natural fibres, nothing synthetic', 'Made to order, by hand in Italy'),
    # the part is the boxspring, by its name, wherever the bed's parts are named
    ('Paisley: Katai, a pure silk, on the base and the border of the mattress.', 'Paisley: Katai, a pure silk, on the boxspring and the border of the mattress.'),
    ('Katai, a pure silk, on the base and the mattress border.', 'Katai, a pure silk, on the boxspring and the mattress border.'),
    ('For the wider sizes, the base can be split in two, on request.', 'For the wider sizes, the boxspring can be split in two, on request.'),
    ('Connemara linen on the base and the summer side', 'Connemara linen on the boxspring and the summer side'),
    ('Connemara linen on the base and the mattress', 'Connemara linen on the boxspring and the mattress'),
    ('Wish bouclé on the base: both wool and cashmere', 'Wish bouclé on the boxspring: both wool and cashmere'),
]
CLAIM_FILES = (glob.glob(THEME + '/templates/*.json') + glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/snippets/*.liquid')
               + glob.glob(THEME + '/config/*.json') + glob.glob(THEME + '/locales/*.json') + glob.glob(THEME + '/templates/*.liquid'))
_n = 0
for _f in CLAIM_FILES:
    _t = open(_f, encoding='utf-8').read()
    _o = _t
    for a, b in CLAIMS:
        _t = _t.replace(a, b)
    if _t != _o:
        open(_f, 'w', encoding='utf-8').write(_t)
        _n += 1
# the figures that counted them: the home page's first chapter and the house at a glance
for _f in glob.glob(THEME + '/templates/*.json'):
    _h, _d = tpl_load(_f.split('/')[-1])
    _ch = False
    for _sec in _d['sections'].values():
        st = _sec.get('settings', {})
        if st.get('stat1_value') == '2' and 'Artisans' in st.get('stat1_label', ''):
            st['stat1_value'], st['stat1_label'] = '15 + 15', 'Years: renewed by hand at fifteen, for fifteen more'
            _ch = True
        if st.get('stat2_value') == '24':
            st['stat2_value'], st['stat2_label'] = '3', 'Collections: Essentials, Signature and Icons'
            _ch = True
        for _b in (_sec.get('blocks') or {}).values():
            bs = _b.get('settings', {})
            if bs.get('label') == 'Artisans per bed':
                bs.update({'number': '1', 'count': True, 'label': 'Bed at a time', 'line': 'Made by hand in Italy, from the first stitch to the last.'})
                _ch = True
            if bs.get('label') == 'Tooling charges':
                bs.update({'number': '100%', 'count': False, 'label': 'Made to order', 'line': 'To your measure, round beds included.'})
                _ch = True
    if _ch:
        tpl_save(_f.split('/')[-1], _h, _d)
        _n += 1
print('claims: made literal no more, in', _n, 'files')

# ── search engines while prices are on request (the house's audit, Oct 2026), and the photographs'
#    tone: two theme settings
p = THEME + '/config/settings_schema.json'
sch = json.loads(open(p).read())
if 'ms_schema_unpriced' not in json.dumps(sch):
    for grp in sch:
        if grp.get('name') == 'Enquiry-led commerce':
            grp['settings'].append({"type": "select", "id": "ms_schema_unpriced", "label": "Search engines, while prices are on request",
                "options": [{"value": "thing", "label": "Describe each bed, without a price"}, {"value": "product", "label": "As a product, without a price"}],
                "default": "thing",
                "info": "Google asks a product for a price (or reviews). Without one it reports an error in Search Console; described plainly, it does not. With prices or a starting price shown, the product always carries its offer."})
    sch.append({"name": "Midsummer · Photographs", "settings": [
        {"type": "paragraph", "content": "One gentle tone over the site's photographs, so pictures from different shoots sit together: a little warmth, a little softer colour. Fabric swatches, logos, drawings and maps keep their true colours."},
        {"type": "checkbox", "id": "ms_photo_tone", "label": "Tone the photographs", "default": True},
        {"type": "range", "id": "ms_photo_tone_strength", "label": "Strength", "min": 0, "max": 100, "step": 5, "unit": "%", "default": 40}]})
    open(p, 'w').write(json.dumps(sch, indent=2, ensure_ascii=False) + '\n')
print('settings: search engines while on request; the photographs\' tone')

# ── the photographs' tone (Theme settings → Midsummer · Photographs): one gentle tone over every
#    photograph; swatches (backgrounds), logos, drawings, maps and icons keep their true colours
open(THEME + '/snippets/ms-photo-tone.liquid', 'w').write('''{%- comment -%}
  One gentle tone over the site's photographs, so pictures from different shoots sit together:
  a little warmth, a little softer colour, at the strength set in Theme settings → Midsummer ·
  Photographs. Not on drawings and logos (SVG), the press marks, the Loro Piana Interiors cloths,
  the fibre plates' drawings or the map. Generated by bin/build_more.py.
{%- endcomment -%}
{%- if settings.ms_photo_tone -%}
  {%- liquid
    assign k = settings.ms_photo_tone_strength | default: 40 | divided_by: 100.0
    assign sep = k | times: 0.16 | round: 3
    assign sat = k | times: 0.14 | round: 3
    assign sat = 1 | minus: sat
    assign con = k | times: 0.04 | round: 3
    assign con = 1 | minus: con
    assign bri = k | times: 0.02 | plus: 1 | round: 3
  -%}
  <style>
    .ms-site img:not([src*=".svg"]):not([src*="ms-press-"]):not([src*="ms-fibre-draw"]):not([src*="logo"]):not(.ms-no-tone),
    .ms-site video { filter: sepia({{ sep }}) saturate({{ sat }}) contrast({{ con }}) brightness({{ bri }}); }
    .ms-site .ms-lf img, .ms-site .ms-pr img, .ms-site .ms-sl__map img, .ms-site .ms-fa__world, .ms-site [class*="__logo"] img, .ms-site [class*="swatch"] img { filter: none; }
  </style>
{%- endif -%}
''')
for lay in ('ms.liquid', 'theme.liquid'):
    p = THEME + '/layout/' + lay
    t = open(p).read()
    if "render 'ms-photo-tone'" not in t:
        t = t.replace("{{ 'ms-site.css' | asset_url | stylesheet_tag }}", "{{ 'ms-site.css' | asset_url | stylesheet_tag }}\n    {%- render 'ms-photo-tone' -%}", 1)
        assert "render 'ms-photo-tone'" in t, lay
        open(p, 'w').write(t)
print('photographs: one gentle tone')

# ── meta tags (the house's audit, Oct 2026): one spelling of the name, a description of its own for
#    each blog, nothing escaped twice (&amp;amp;), and the contact page said as it is
p = THEME + '/snippets/meta-tags.liquid'
t = open(p).read()
if 'ms_desc_blog' not in t:
    t = t.replace("""  # Meta description, with fallbacks so no page ships without one.
  assign ms_desc = page_description | strip_html | strip""", """  # one spelling of the house's name, whatever the store is called in admin
  assign ms_brand = 'Midsummer Milano'
  # Meta description, with fallbacks so no page ships without one.
  assign ms_desc = page_description | strip_html | strip""", 1)
    t = t.replace("""    assign ms_desc = article.title | append: ' — ' | append: blog.title | append: ' feature on ' | append: shop.name | append: ', Italian luxury beds and mattresses handmade in natural materials.'""",
                  """    assign ms_desc = article.title | append: ' — ' | append: blog.title | append: ' on ' | append: ms_brand | append: ', Italian luxury beds and mattresses handmade in natural materials.'""", 1)
    t = t.replace("""  if ms_desc == blank and request.page_type == 'blog'
    assign ms_desc = blog.title | append: ' — press coverage and stories from ' | append: shop.name | append: ', Italian luxury beds and mattresses handmade in natural materials.'
  endif""", """  # each blog says what it holds: a publication's pieces, the projects, the collaborations, the journal
  if ms_desc == blank and request.page_type == 'blog'
    assign ms_desc_blog = blog.handle | downcase
    if ms_desc_blog contains 'press-'
      assign ms_desc = blog.title | append: ' on ' | append: ms_brand | append: ': the pieces it has written about the house’s handmade beds and mattresses, and where to read them.'
    elsif ms_desc_blog == 'press'
      assign ms_desc = 'The press on ' | append: ms_brand | append: ': magazines, newspapers and awards on the house’s beds and mattresses, made by hand in Italy from natural fibres.'
    elsif ms_desc_blog contains 'project' or ms_desc_blog contains 'progett' or ms_desc_blog contains 'portfolio' or ms_desc_blog contains 'hotel'
      assign ms_desc = 'Projects by ' | append: ms_brand | append: ': handmade beds for homes, hotels, villas and yachts, specified with the Milan atelier and made to measure in Italy.'
    elsif ms_desc_blog contains 'collab'
      assign ms_desc = 'Collaborations by ' | append: ms_brand | append: ': designers, houses and artisans the atelier has worked with, and the beds made together.'
    else
      assign ms_desc = 'The ' | append: ms_brand | append: ' journal: sleep, natural materials, craft, the bedroom and news from the Milan atelier.'
    endif
  endif""", 1)
    # the contact page: what it is for, not the first words of its text
    t = t.replace("""  if ms_desc == blank and request.page_type == 'page'
    assign ms_desc = page.content | strip_html | strip
  endif""", """  if ms_desc == blank and request.page_type == 'page'
    assign ms_desc = page.content | strip_html | strip
  endif
  if request.page_type == 'page' and page.handle == 'contact' or request.page_type == 'page' and template.suffix == 'contact'
    assign ms_desc_c = ms_desc | downcase
    if ms_desc == blank or ms_desc_c contains 'please contact' or ms_desc_c contains 'info@'
      assign ms_desc = 'Book an appointment at the Milan atelier, ask for a proposal, or write to ' | append: ms_brand | append: ' about a bed, a project or becoming a partner.'
    endif
  endif""", 1)
    # nothing escaped twice: what the store already escaped is unescaped first
    t = t.replace("""  assign ms_desc = ms_desc | strip | truncate: 158""", """  assign ms_desc = ms_desc | replace: '&amp;', '&' | replace: '&#39;', '’' | replace: '&quot;', '"' | replace: '&nbsp;', ' ' | strip | truncate: 158""", 1)
    t = t.replace("""  assign og_title = page_title | default: shop.name""", """  assign og_title = page_title | default: ms_brand | replace: '&amp;', '&'""", 1)
    t = t.replace("""  assign og_description = ms_desc | default: shop.name""", """  assign og_description = ms_desc | default: ms_brand""", 1)
    t = t.replace("""  property="og:site_name"
  content="{{ shop.name }}\"""", """  property="og:site_name"
  content="{{ ms_brand }}\"""", 1)
    t = t.replace("""  assign ms_brand = 'Midsummer Milano'
  assign ms_title = page_title | strip""", """  assign ms_title = page_title | replace: '&amp;', '&' | strip""", 1)
    t = t.replace("""  {{ ms_title }}
  {%- if current_tags""", """  {{ ms_title | escape }}
  {%- if current_tags""", 1)
    assert 'ms_desc_blog' in t and "content=\"{{ ms_brand }}\"" in t and "{{ ms_title | escape }}" in t, 'meta-tags patch'
    open(p, 'w').write(t)
print('meta tags: one name, each blog its own description, nothing escaped twice')
# the house's name, one spelling, in the copy and the product data too
for f in glob.glob(THEME + '/templates/*.json') + glob.glob(THEME + '/sections/*.liquid'):
    t0 = open(f, encoding='utf-8').read()
    t1 = t0.replace('Midsummer-Milano & Strega del Castello', 'Midsummer Milano & Strega del Castello').replace('Art inspired beds by Midsummer-Milano', 'Art-inspired beds by Midsummer Milano')
    if f.endswith('ms-product-main.liquid'):
        t1 = t1.replace('"brand": { "@type": "Brand", "name": {{ shop.name | json }} },', '"brand": { "@type": "Brand", "name": "Midsummer Milano" },')
    if t1 != t0:
        open(f, 'w', encoding='utf-8').write(t1)

# ── every picture says what it shows (the house's audit, Oct 2026: images without alt text): the
#    house's own photographs by what is in them, products and pieces by their names
PHOTO_ALT = {
    'ms-graded-arches.jpg': 'A Midsummer bed beneath tall wrought-iron arched windows',
    'ms-graded-bougainvillea.jpg': 'A Midsummer bed by a whitewashed wall, under bougainvillea',
    'ms-graded-dune.jpg': 'A Midsummer bed on a sand dune, under a summer sky',
    'ms-graded-horse.jpg': 'A white horse beside a Midsummer bed in a meadow',
    'ms-graded-ochre-room.jpg': 'A Midsummer bed with an upholstered headboard, against a patterned wall',
    'ms-photo-my-dream-sleep.jpg': 'A woman resting on a Midsummer mattress',
}
ALTS = {
    'sections/ms-collection-index.liquid': [('<img src="{{ pic | image_url: width: 900 }}" alt=""', '<img src="{{ pic | image_url: width: 900 }}" alt="{{ c.title | escape }}"'),
                                            ('<img src="{{ house | asset_url }}" alt=""', '<img src="{{ house | asset_url }}" alt="{{ c.title | escape }}"')],
    'snippets/ms-mega-panel.liquid': [('<img src="{{ feature | image_url: width: 900 }}" alt=""', '<img src="{{ feature | image_url: width: 900 }}" alt="{{ f[1] | strip | escape }}"'),
                                      ('<img src="{{ f[3] | strip }}" alt=""', '<img src="{{ f[3] | strip }}" alt="{{ f[1] | strip | escape }}"')],
    'sections/ms-next-read.liquid': [('<img src="{{ img | asset_url }}" alt=""', '{%- capture nr_alt -%}{% render \'ms-next-read-data\', k: key, f: \'title\' %}{%- endcapture -%}<img src="{{ img | asset_url }}" alt="{{ nr_alt | strip | escape }}"')],
    'sections/ms-process.liquid': [('<img src="{{ src }}" alt="" data-ms-pc-img', '<img src="{{ src }}" alt="{{ block.settings.title | escape }}" data-ms-pc-img')],
    'sections/ms-link-cards.liquid': [("fallback: b.image_fallback, width: 900 %}\" alt=\"\"", "fallback: b.image_fallback, width: 900 %}\" alt=\"{{ b.title | escape }}\"")],
    'sections/ms-follow.liquid': [('{% else %}{{ fb }}{% endif %}" alt=""', '{% else %}{{ fb }}{% endif %}" alt="{{ handle | escape }} on Instagram"')],
    'sections/ms-systems.liquid': [('<img class="ms-card__alt" alt=""', '<img class="ms-card__alt" alt="{{ product.title | escape }}"'),
                                   ('<img src="{{ product.featured_media | image_url: width: 160 }}" alt=""', '<img src="{{ product.featured_media | image_url: width: 160 }}" alt="{{ product.title | escape }}"')],
    'sections/ms-collection-grid.liquid': [('<img class="ms-card__alt" alt=""', '<img class="ms-card__alt" alt="{{ product.title | escape }}"')],
    'sections/ms-journal-list.liquid': [('<img class="ms-jl__thumb" src="{{ article.image | image_url: width: 200 }}" alt=""', '<img class="ms-jl__thumb" src="{{ article.image | image_url: width: 200 }}" alt="{{ article.image.alt | default: article.title | escape }}"')],
    'sections/ms-product-fibres.liquid': [('<img src="{{ block.settings.icon | image_url: width: 160 }}" alt=""', '<img src="{{ block.settings.icon | image_url: width: 160 }}" alt="{{ block.settings.name | escape }}"')],
    'sections/ms-product-main.liquid': [('<img src="{{ media | image_url: width: 200 }}" alt=""', '<img src="{{ media | image_url: width: 200 }}" alt="{{ media.alt | default: product.title | escape }}"')],
    'snippets/ms-craft-mate.liquid': [('alt="" width="80" height="80"', 'alt="{{ mp.title | escape }}" width="80" height="80"')],
    'sections/ms-fibre-atlas.liquid': [("echo '<img src=\"' | append: ep[3] | append: '\" alt=\"\" width=\"120\"", "assign bal = ep[2] | escape\n                          echo '<img src=\"' | append: ep[3] | append: '\" alt=\"' | append: bal | append: '\" width=\"120\"")],
    'sections/ms-hp-proof.liquid': [("echo '<img src=\"' | append: src | append: '\" alt=\"\" width=\"150\" height=\"40\">'", "echo '<img src=\"' | append: src | append: '\" alt=\"' | append: ename | append: '\" width=\"150\" height=\"40\">'"),
                                    ("append: alogo | append: '\" alt=\"\" width=\"150\" height=\"40\"></button></li>'", "append: alogo | append: '\" alt=\"' | append: eby | append: '\" width=\"150\" height=\"40\"></button></li>'"),
                                    ("echo '<div class=\"ms-pr__mark\"><img src=\"' | append: alogo | append: '\" alt=\"\" width=\"200\" height=\"56\"></div>'", "assign eby0 = s.award_by | escape\n      echo '<div class=\"ms-pr__mark\"><img src=\"' | append: alogo | append: '\" alt=\"' | append: eby0 | append: '\" width=\"200\" height=\"56\"></div>'")],
    'sections/ms-home-14.liquid': [('Vicuna-mattress.jpg', None), ('ms-graded-horse.jpg', None), ('giotto_SANGALGANO.jpg', None)],
    'sections/ms-regen-01.liquid': [('Untitled_Project_4_copia.jpg', None)],
    'snippets/ms-mega.liquid': [('Vicuna-mattress.jpg?width=900', None)],
}
FILE_ALT = {'Vicuna-mattress.jpg': 'The Vicuña mattress', 'ms-graded-horse.jpg': PHOTO_ALT['ms-graded-horse.jpg'],
            'giotto_SANGALGANO.jpg': 'Giotto Round, the round bed, in a Tuscan abbey', 'Untitled_Project_4_copia.jpg': 'Artisans’ hands at work on a mattress',
            'Vicuna-mattress.jpg?width=900': 'The Vicuña mattress'}
_na = 0
def _alt_in_tags(t, key, alt):
    """alt="" becomes the given words, in every <img> tag that names this file"""
    out, n = [], 0
    for m in re.finditer(r'<img\b[^>]*>', t):
        pass
    def rep(m):
        nonlocal n
        tag = m.group(0)
        if key in tag and 'alt=""' in tag:
            n += 1
            return tag.replace('alt=""', 'alt="%s"' % alt.replace('"', '&quot;'), 1)
        return tag
    return re.sub(r'<img\b[^>]*>', rep, t), n
for rel, reps in ALTS.items():
    p = THEME + '/' + rel
    if not os.path.exists(p):
        continue
    t = open(p, encoding='utf-8').read()
    for a, b in reps:
        if b is None:
            t, k = _alt_in_tags(t, a, FILE_ALT[a])
            _na += k
        elif a in t:
            t = t.replace(a, b)
            _na += 1
    open(p, 'w', encoding='utf-8').write(t)
for f in glob.glob(THEME + '/sections/*.liquid') + glob.glob(THEME + '/snippets/*.liquid'):
    t = open(f, encoding='utf-8').read()
    t0 = t
    for fn, alt in PHOTO_ALT.items():
        t, k = _alt_in_tags(t, fn, alt)
        _na += k
    if t != t0:
        open(f, 'w', encoding='utf-8').write(t)
print('pictures: alt text in', _na, 'places')

# ── the Icons collection is called Icons, even where the store still names it "Icon" (its handle
#    /collections/icon is the store's; renaming it in admin, with a redirect, is in INSTALL.md)
open(THEME + '/snippets/ms-coll-name.liquid', 'w').write(
    "{%- comment -%} A collection's name as the house says it: Icons, never Icon. Generated by bin/build_more.py. {%- endcomment -%}\n"
    "{%- liquid\n  assign cn = c.title\n  assign cl = cn | downcase | strip\n  if cl == 'icon'\n    assign cn = 'Icons'\n  endif\n  echo cn\n-%}\n")
p = THEME + '/sections/ms-collection-hero.liquid'
t = open(p).read()
if "render 'ms-coll-name'" not in t:
    t = t.replace('{{ collection.title }}</h1>', "{% render 'ms-coll-name', c: collection %}</h1>").replace('alt="{{ collection.title | escape }}"', 'alt="{%- render \'ms-coll-name\', c: collection -%}"')
    assert "render 'ms-coll-name'" in t
    open(p, 'w').write(t)
p = THEME + '/snippets/meta-tags.liquid'
t = open(p).read()
if 'ms_coll_icon' not in t:
    t = t.replace("""  assign ms_title = page_title | replace: '&amp;', '&' | strip | remove_last: ' | midsummer-milano' | remove_last: ' | Midsummer-Milano' | remove_last: ' | Midsummer Milano' | strip""", """  assign ms_title = page_title | replace: '&amp;', '&' | strip | remove_last: ' | midsummer-milano' | remove_last: ' | Midsummer-Milano' | remove_last: ' | Midsummer Milano' | strip
  # the Icons collection, even where the store still calls it Icon
  assign ms_coll_icon = ms_title | downcase | strip
  if request.page_type == 'collection' and ms_coll_icon == 'icon'
    assign ms_title = 'Icons'
  endif""", 1)
    t = t.replace("""  assign og_title = page_title | default: ms_brand | replace: '&amp;', '&'""", """  assign og_title = page_title | default: ms_brand | replace: '&amp;', '&'
  if request.page_type == 'collection' and collection.title == 'Icon'
    assign og_title = 'Icons | ' | append: ms_brand
  endif""", 1)
    assert 'ms_coll_icon' in t
    open(p, 'w').write(t)
print('collections: Icons, by its name')

# ── the Journal's subjects, each a page of its own: /blogs/<journal>?view=<subject> lists every note
#    of that subject (sections/ms-journal-list files them with snippets/ms-note-cat)
from journal_subjects import SHOWN as _SUBJ, LABELS as _SUBJ_L
_bh, _bd = tpl_load('blog.json')
for _k in _SUBJ:
    tpl_save('blog.%s.json' % _k, _bh.replace('blog.json', 'blog.%s.json' % _k) if _bh else _bh, json.loads(json.dumps(_bd)))
for _f in (THEME + '/snippets/ms-mega.liquid', THEME + '/snippets/ms-article-end.liquid', THEME + '/sections/ms-article.liquid'):
    if os.path.exists(_f):
        _t = open(_f).read()
        _t2 = _t.replace('{{ u_journal }}?cat={{ k }}', '{{ u_journal }}?view={{ k }}').replace('?cat={{ cat }}', '?view={{ cat }}')
        if _t2 != _t:
            open(_f, 'w').write(_t2)
SUBJ_DESC = {
    'sleep': 'Notes on sleep from the Midsummer Milano journal: how we rest, the seasons of the bed, and what natural fibres change at night.',
    'materials': 'Notes on natural materials from the Midsummer Milano journal: wool, cashmere, vicuña, horsehair, linen and the other fibres in our beds.',
    'craft': 'Notes on craft from the Midsummer Milano journal: how a bed is made by hand in Italy, from the first stitch to the last.',
    'design': 'Notes on the bedroom from the Midsummer Milano journal: design, colour, light and the rooms we sleep in.',
    'italy': 'Notes on Italian living from the Midsummer Milano journal: places, food, reading and a slower way of life.',
    'regen': 'Notes on sustainability from the Midsummer Milano journal: beds that last, regeneration at fifteen years, less waste.',
    'projects': 'Projects from the Midsummer Milano journal: bedrooms in homes, villas and hotels, made with the Milan atelier.',
    'news': 'News and press from the Midsummer Milano journal: the Salone, collaborations, awards and features.',
}
p = THEME + '/snippets/meta-tags.liquid'
t = open(p).read()
if 'ms_subj' not in t:
    cases = ''.join("      when '%s'\n        assign ms_view_title = '%s · ' | append: blog.title\n        assign ms_desc = '%s'\n" % (k, _SUBJ_L[k], SUBJ_DESC[k].replace("'", '’')) for k in _SUBJ)
    t = t.replace("""  assign og_title = page_title | default: ms_brand""", """  # the Journal's subjects, each a page of its own (?view=sleep …)
  if request.page_type == 'blog' and template.suffix != blank
    assign ms_subj = template.suffix
    case ms_subj
""" + cases + """    endcase
  endif
  assign og_title = page_title | default: ms_brand""", 1)
    assert 'ms_subj' in t
    open(p, 'w').write(t)
print('journal: a page for each subject,', len(_SUBJ))

# the Icons' fallback list names systems, not the pieces that share a handle with them: "giotto"
# is the headboard bed, "dreamy-springs" the boxspring and "roma" was the mohair plaid
_p = THEME + '/snippets/ms-tier.liquid'
_t = open(_p).read()
_t2 = _t.replace('giotto|giotto-round', 'giotto-round').replace(',dreamy-springs,', ',dreamy-springs-1|dreamy-springs-mattress,').replace(',roma,', ',mystic-river|roma,').replace(',ultra-dry,', ',ultra-dry|ultra-dry-mattress,').replace(',vicuna,', ',vicuna|vicuna-mattress,').replace('essentials-topper\'', 'essentials-topper|topper-basso\'').replace('signature-topper\'', 'signature-topper|topper-medio|topper-alto\'')
if _t2 != _t:
    open(_p, 'w').write(_t2)
print('icons fallback: systems by their own handles')


# the house's own photographs: the artisans at work (Drive, "Foto artigiani per WWTS") in place of a
# stock picture of a seamstress; the cloth cared for as it is, removable, by its label
PHOTO_SWAP = [('ms-photo-seamstress-portrait.jpg', 'ms-photo-artisan-portrait.jpg'), ('ms-photo-seamstress.jpg', 'ms-photo-artisan-wool.jpg'),
              ('The cloth, cut by hand at the atelier.', 'Wool, shaped by hand along the edge of the bed.'),
              ('Loro Piana Interiors upholstery should be dry-cleaned by a specialist only; the atelier can arrange this.',
               'Loro Piana Interiors upholstery is removable: clean it as its care label directs, and ask the atelier whenever in doubt.'),
              ('Loro Piana Interiors upholstery is dry-cleaned by a specialist only; the atelier can arrange it.',
               'Loro Piana Interiors upholstery is removable: clean it as its care label directs, and ask the atelier whenever in doubt.')]
PHOTO_SWAP_ALT = {'ms-photo-artisan-portrait.jpg': 'A Midsummer artisan opening natural fibre by hand',
                  'ms-photo-artisan-wool.jpg': 'A Midsummer artisan shaping wool along the edge of a bed',
                  'ms-photo-flora-side.jpg': 'The Flora mattress and topper on its bouclé boxspring',
                  'ms-photo-flora-corner.jpg': 'Flora: the Loro Piana Interiors Cardi topper over the mattress and the Wish bouclé boxspring',
                  'ms-photo-flora-wide.jpg': 'Flora in Loro Piana Interiors Cardi and Wish'}
_ns = 0
for _f in CLAIM_FILES:
    _t = open(_f, encoding='utf-8').read()
    _t2 = _t
    for _a, _b in PHOTO_SWAP:
        _t2 = _t2.replace(_a, _b)
    for _k, _alt in PHOTO_SWAP_ALT.items():
        _t2, _ = _alt_in_tags(_t2, _k, _alt)
    if _t2 != _t:
        open(_f, 'w', encoding='utf-8').write(_t2)
        _ns += 1
for _old in ('ms-photo-seamstress-portrait.jpg', 'ms-photo-seamstress.jpg'):
    _used = any(_old in open(_f, encoding='utf-8').read() for _f in CLAIM_FILES + glob.glob(THEME + '/layout/*.liquid') + glob.glob(THEME + '/blocks/*.liquid') + glob.glob(THEME + '/assets/*.css') + glob.glob(THEME + '/assets/*.js'))
    if not _used and os.path.exists(THEME + '/assets/' + _old):
        os.remove(THEME + '/assets/' + _old)
print('photographs: the artisans at work, in %d files' % _ns)

# Questions: the topics as an index beside the answers, which follows the reader down the page; the
# opening words speak to the reader, not to search engines
_p = THEME + '/sections/ms-faq-02.liquid'
_t = open(_p).read()
if 'ms-faq-index' not in _t:
    _s0 = _t.index('<div data-dc-tpl="1137" class="ms-faq-side"')
    _s1 = _t.index('{{ section.settings.t3 }}</a>\n</div>', _s0) + len('{{ section.settings.t3 }}</a>\n</div>')
    _side_old = _t[_s0:_s1]
    _side_new = ('<div data-dc-tpl="1137" class="ms-faq-side">\n'
                 "{%- assign topics = section.blocks | where: 'type', 'topic' -%}\n"
                 '{%- if topics.size > 1 -%}\n'
                 '<nav class="ms-faq-index" aria-label="{{ section.settings.t1 | default: \'Topics\' | escape }}"><ol>'
                 '{%- for tb in topics -%}<li><a href="#{{ tb.settings.title | handleize }}" data-faq-to="{{ tb.settings.title | handleize }}"><span>{{ forloop.index | prepend: \'0\' | slice: -2, 2 }}</span>{{ tb.settings.title }}</a></li>{%- endfor -%}'
                 '</ol></nav>\n{%- endif -%}\n'
                 '<div class="ms-faq-ask">\n'
                 '<div class="ms-faq-ask__e">{{ section.settings.t1 }}</div>\n'
                 '<p>{{ section.settings.t2 }}</p>\n'
                 '<a data-ms="cta" data-ms-enquire="" href="{% render \'ms-link\', to: \'contact\' %}">{{ section.settings.t3 }}</a>\n'
                 '</div>\n</div>')
    _t = _t.replace(_side_old, _side_new, 1)
    _nav = _t[_t.index("{%- assign topics = section.blocks | where: 'type', 'topic' -%}\n{%- if topics.size > 1 -%}\n<nav class=\"ms-faq-topics\""):]
    _nav = _nav[:_nav.index('{%- endif -%}') + len('{%- endif -%}')]
    _t = _t.replace(_nav, '', 1)
    _t = _t.replace('grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: clamp(28px, 5vw, 88px); align-items: start;',
                    'grid-template-columns: minmax(220px, 3fr) minmax(0, 7fr); gap: clamp(28px, 6vw, 120px); align-items: start;', 1)
    _css = '''
  .ms-faq-side { max-width: none; }
  .ms-faq-index ol { list-style: none; margin: 0; padding: 0; border-top: 1px solid #DDD6C9; }
  .ms-faq-index li { border-bottom: 1px solid #DDD6C9; }
  .ms-site .ms-faq-index a { display: flex; align-items: baseline; gap: 14px; padding: 15px 0; font-family: Newsreader, Georgia, serif; font-size: 19px; line-height: 1.3; color: #6E675C; transition: color .3s ease, padding .3s ease; }
  .ms-faq-index a span { font-family: inherit; font-size: 11px; letter-spacing: .18em; color: #A08B6C; min-width: 22px; }
  .ms-site .ms-faq-index a:hover, .ms-site .ms-faq-index a[aria-current="true"] { color: #17140F; }
  .ms-site .ms-faq-index a[aria-current="true"] { padding-left: 8px; }
  .ms-faq-ask { margin-top: clamp(28px, 3vw, 44px); padding: 22px 24px; background: #F3EEE5; }
  .ms-faq-ask__e { font-size: 11px; letter-spacing: .28em; text-transform: uppercase; color: #6E675C; }
  .ms-faq-ask p { font-size: 14.5px; line-height: 1.85; color: #4A443B; margin: 12px 0 0; }
  .ms-site .ms-faq-ask a { display: inline-block; margin-top: 16px; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; border-bottom: 1px solid #17140F; padding-bottom: 7px; color: #17140F; }
  .ms-faq-topic:first-of-type { margin-top: 0 !important; }
  @media (max-width: 999px) {
    .ms-faq-index ol { display: flex; flex-wrap: wrap; gap: 4px 18px; border: 0; }
    .ms-faq-index li { border: 0; }
    .ms-site .ms-faq-index a { font-family: inherit; font-size: 11px; letter-spacing: .2em; text-transform: uppercase; padding: 8px 0; border-bottom: 1px solid #DDD6C9; }
    .ms-faq-index a span { display: none; }
    .ms-faq-ask { order: 3; }
  }
</style>
<script>
  /* the index follows the reader: the topic in view is the one marked */
  (function () {
    var nav = document.querySelector('.ms-faq-index'); if (!nav || !('IntersectionObserver' in window)) return;
    var links = {}; nav.querySelectorAll('a[data-faq-to]').forEach(function (a) { links[a.getAttribute('data-faq-to')] = a; });
    var heads = Array.prototype.slice.call(document.querySelectorAll('.ms-faq-topic[id]'));
    function mark(id) { Object.keys(links).forEach(function (k) { if (k === id) links[k].setAttribute('aria-current', 'true'); else links[k].removeAttribute('aria-current'); }); }
    var io = new IntersectionObserver(function () {
      var cur = heads[0]; heads.forEach(function (h) { if (h.getBoundingClientRect().top < innerHeight * .35) cur = h; });
      if (cur) mark(cur.id);
    }, { rootMargin: '0px 0px -60% 0px', threshold: [0, 1] });
    heads.forEach(function (h) { io.observe(h); });
    addEventListener('scroll', function () { var cur = heads[0]; heads.forEach(function (h) { if (h.getBoundingClientRect().top < innerHeight * .35) cur = h; }); if (cur) mark(cur.id); }, { passive: true });
    if (heads[0]) mark(heads[0].id);
  })();
</script>'''
    _t = _t.replace('\n</style>', _css, 1)
    open(_p, 'w').write(_t)
for _f in [THEME + '/sections/ms-faq-01.liquid'] + glob.glob(THEME + '/templates/*.json'):
    _t = open(_f).read()
    _u = _t.replace(' Each one answers in its first sentence, which is the part search engines and AI assistants quote.', '')
    if _u != _t:
        open(_f, 'w').write(_u)
print('questions: an index beside the answers')


# the trade and hotel pages: every system measured, from the 2026 catalogue (sections/ms-sizes)
import sys as _sys
_sys.path.insert(0, os.path.dirname(__file__))
from lp_data import CLOTH as _CLOTH
_STD = '100 × 200, 160 × 200, 180 × 200, 200 × 200; Queen 153 × 203, King 193 × 203'
_SIZES = [  # name, product handle, collection, overall height (catalogue 2026), sizes, cloth key
    ('Amalfi', 'amalfi', 'Essentials', '52 cm', _STD, 'amalfi'),
    ('Capri', 'capri', 'Essentials', '55 cm', _STD, 'capri'),
    ('Dreamy', 'dreamy', 'Signature', '62 cm', _STD, 'dreamy-2'),
    ('Brera', 'brera', 'Signature', '50 cm', _STD, 'brera'),
    ('Top', 'top', 'Icons', '65 cm', _STD, 'top-2'),
    ('Giotto Round', 'giotto-round', 'Icons', '55 cm', 'Ø 225 or 245', 'giotto'),
    ('Bellini', 'bellini', 'Icons', '65 cm', _STD, 'bellini'),
    ('Storage', 'storage', 'Icons', '55 cm', _STD, 'storage'),
    ('Flora', 'flora', 'Icons', '62 cm', _STD, 'flora'),
    ('Paisley', 'paisley', 'Icons', '55 cm', _STD, 'paisley'),
]
_rows = [('system', {'name': n, 'handle': h, 'collection': c, 'height': ht, 'sizes': sz, 'cloth': _CLOTH.get(ck, {}).get('cover', '')}) for n, h, c, ht, sz, ck in _SIZES]
for name in ('page.professionals.json', 'collection.ms-professionals.json'):
    add_section(name, 'ms-steps', 'sizes', 'ms-sizes', None, _rows)
for name in ('page.hospitality.json', 'collection.ms-hospitality.json'):
    add_section(name, 'ms-spec', 'sizes', 'ms-sizes', {'eyebrow': 'Systems, measured', 'heading': 'For every room: heights, sizes and cloths.',
                'text': 'The figures a room plan needs, from the 2026 catalogue. A suite, a villa or a cabin each sets its own width, length and height.',
                'note': 'Other sizes, heights and shapes are made on request.', 'link_label': 'Start a hotel project'}, _rows)
print('professionals, hospitality: the systems measured')

# Round 15: one photograph per product card, no second one on hover (the store's own cards included)
_sdp = THEME + '/config/settings_data.json'
_sdt = open(_sdp, encoding='utf-8').read()
_sdm = re.match(r'\s*/\*.*?\*/\s*', _sdt, re.S)
_sdh = _sdm.group(0) if _sdm else ''
_sdj = json.loads(_sdt[len(_sdh):])
_cur = _sdj['current'] if isinstance(_sdj.get('current'), dict) else None
if _cur is not None and _cur.get('show_second_image_on_hover') is not False:
    _cur['show_second_image_on_hover'] = False
    open(_sdp, 'w', encoding='utf-8').write(_sdh + json.dumps(_sdj, indent=2, ensure_ascii=False) + '\n')
print('cards: one photograph, no second on hover')

# Round 15: on a phone the homepage film is shown whole, under the header, with the words beneath it
# (a landscape film cropped to a tall screen showed only a blur of fabric)
p = THEME + '/sections/ms-home-01.liquid'
t = open(p, encoding='utf-8').read()
if 'ms-hero__film' not in t:
    t = t.replace('<section data-dc-tpl="196" style="', '<section class="ms-hero" data-dc-tpl="196" style="', 1)
    t = t.replace('<video autoplay="" loop="" muted="" playsinline=""', '<video class="ms-hero__film" autoplay="" loop="" muted="" playsinline=""', 1)
    t = t.replace('<div style="position: absolute; inset: 0px; background: linear-gradient(', '<div class="ms-hero__shade" style="position: absolute; inset: 0px; background: linear-gradient(', 1)
    t = t.replace('<div style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content: space-between;', '<div class="ms-hero__words" style="position: absolute; inset: 0px; display: flex; flex-direction: column; justify-content: space-between;', 1)
    assert t.count('ms-hero__') == 3, t.count('ms-hero__')
    css = ('<style>\n'
           '  @media (max-width: 700px) {\n'
           '    .ms-site .ms-hero { height: auto !important; min-height: 0 !important; display: flex; flex-direction: column; padding-top: 84px; }\n'
           '    .ms-site .ms-hero .ms-hero__film { position: relative !important; inset: auto !important; display: block; width: 100%; height: auto !important; aspect-ratio: var(--ms-film-ar, 16 / 9); object-fit: cover; }\n'
           '    .ms-site .ms-hero .ms-hero__shade { display: none; }\n'
           '    .ms-site .ms-hero .ms-hero__words { position: relative !important; inset: auto !important; padding: 30px 22px 38px !important; gap: 0 !important; }\n'
           '    .ms-site .ms-hero .ms-hero__words > div[aria-hidden] { display: none; }\n'
           '    .ms-site .ms-hero h1 { font-size: clamp(32px, 9vw, 40px) !important; }\n'
           '  }\n'
           '</style>\n'
           '<script>\n'
           '  (function () {\n'
           '    var v = document.currentScript && document.currentScript.previousElementSibling;\n'
           '    while (v && !(v.classList && v.classList.contains(\'ms-hero\'))) v = v.previousElementSibling;\n'
           '    var f = v && v.querySelector(\'.ms-hero__film\');\n'
           '    if (!f) return;\n'
           '    function ar() { if (f.videoWidth && f.videoHeight) v.style.setProperty(\'--ms-film-ar\', f.videoWidth + \' / \' + f.videoHeight); }\n'
           '    if (f.readyState >= 1) ar(); else f.addEventListener(\'loadedmetadata\', ar);\n'
           '  })();\n'
           '</script>\n')
    t = t.replace('</section>\n{% schema %}', '</section>\n' + css + '{% schema %}', 1)
    assert '--ms-film-ar' in t
    open(p, 'w', encoding='utf-8').write(t)
print('home film: whole on a phone')

# Round 15: the professionals' pages share one bar (architects, hospitality, portfolio, agents and
# the trade desk), and the menu's Professionals panel lists the same places in the same order
for _name, _cur in (('page.professionals.json', 'architects'), ('collection.ms-professionals.json', 'architects'),
                    ('page.hospitality.json', 'hospitality'), ('collection.ms-hospitality.json', 'hospitality')):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _h, _d = tpl_load(_name)
    if not any(v['type'] == 'ms-pro-nav' for v in _d['sections'].values()):
        _d['sections']['pronav'] = {'type': 'ms-pro-nav', 'settings': {'current': _cur}}
        _d['order'].insert(0, 'pronav')
        tpl_save(_name, _h, _d)
p = THEME + '/snippets/ms-mega.liquid'
t = open(p, encoding='utf-8').read()
_old = """{{ u_pro }}|{{ ss.mg_p1 }}|{{ ss.mg_p1_note }}|{{ 'ms-photo-fresco-bed.jpg' | asset_url }}|
§{{ u_hosp }}|{{ ss.mg_p2 }}|{{ ss.mg_p2_note }}|{{ 'ms-photo-glass-house.jpg' | asset_url }}|
§{{ u_portfolio }}|{{ ss.mg_p3 }}|{{ ss.mg_p3_note }}|{{ 'ms-graded-arches.jpg' | asset_url }}|
§{{ u_partner }}#enquire|{{ ss.mg_p4 }}|{{ ss.mg_p4_note }}|{{ 'ms-photo-atelier-pure.jpg' | asset_url }}|landing
§{{ u_trade }}#enquire|{{ ss.mg_p5 }}|{{ ss.mg_p5_note }}|{{ cdn }}Vicuna-mattress.jpg?width=900|landing"""
if _old in t:
    t = t.replace(_old, """{{ u_pro }}|{{ ss.mg_p1 }}|{{ ss.mg_p1_note }}|{{ 'ms-photo-fresco-bed.jpg' | asset_url }}|
§{{ u_hosp }}|{{ ss.mg_p2 }}|{{ ss.mg_p2_note }}|{{ 'ms-photo-glass-house.jpg' | asset_url }}|
§{{ u_portfolio }}|{{ ss.mg_p3 }}|{{ ss.mg_p3_note }}|{{ 'ms-graded-arches.jpg' | asset_url }}|
§{{ u_agents }}|{{ ss.mg_pro_cta1 }}|Where to see the beds, and how to represent them|{{ 'ms-photo-atelier-pure.jpg' | asset_url }}|
§{{ u_trade }}#enquire|{{ ss.mg_p5 }}|{{ ss.mg_p5_note }}|{{ cdn }}Vicuna-mattress.jpg?width=900|landing""", 1)
    if 'assign u_trade_e' not in t:
        t = t.replace("{%- render 'ms-mega-panel', key: 'pro',", "{%- assign u_trade_e = u_trade | strip | append: '#enquire' -%}\n{%- render 'ms-mega-panel', key: 'pro',", 1)
    t = t.replace("foot: foot, cta1_url: u_agents, cta1_label: ss.mg_pro_cta1 -%}", "foot: foot, cta1_url: u_trade_e, cta1_label: 'Open a project file', cta1_landing: true -%}", 1)
    assert 'Open a project file' in t
    open(p, 'w', encoding='utf-8').write(t)
# Round 16: agents and resellers belong to Contact, where the menu files them: the Professionals bar
# is not shown there, and the Professionals panel offers the partner enquiry instead
for _name in ('page.agents-and-resellers.json', 'page.agents-resellers.json', 'collection.ms-agents.json'):
    if not os.path.exists(THEME + '/templates/' + _name):
        continue
    _h, _d = tpl_load(_name)
    _ids = [k for k, v in _d['sections'].items() if v['type'] == 'ms-pro-nav']
    if _ids:
        for k in _ids:
            del _d['sections'][k]
            _d['order'].remove(k)
        tpl_save(_name, _h, _d)
p = THEME + '/snippets/ms-mega.liquid'
t = open(p, encoding='utf-8').read()
_ag = "§{{ u_agents }}|{{ ss.mg_pro_cta1 }}|Where to see the beds, and how to represent them|{{ 'ms-photo-atelier-pure.jpg' | asset_url }}|"
if _ag in t:
    t = t.replace(_ag, "§{{ u_partner }}#enquire|{{ ss.mg_p4 }}|{{ ss.mg_p4_note }}|{{ 'ms-photo-atelier-pure.jpg' | asset_url }}|landing", 1)
    open(p, 'w', encoding='utf-8').write(t)
assert _ag not in t
print('professionals: one bar, one menu')
# the phone menu's Professionals: the same places as the bar and the panel
p = THEME + '/sections/ms-header.liquid'
t = open(p, encoding='utf-8').read()
if 'ms-pn-phone' not in t:
    i = t.index('data-ms-msub="pro')
    j = t.find('data-ms-msub=', i + 20)
    j = j if j > 0 else len(t)
    seg = t[i:j]
    m = re.search(r'<a href="\{% render \'ms-link\', to: \'enquire\', q: \'enquiry=partner\' %\}#enquire"(.*?)</a>', seg, re.S)
    assert m, 'phone partner link'
    a = m.group(0)
    agents = (a.replace("{% render 'ms-link', to: 'enquire', q: 'enquiry=partner' %}#enquire", "{% render 'ms-link', to: 'agents' %}\" data-ms-pn-phone=\"", 1)
               .replace('>Become a partner<', '>Agents &amp; Resellers<', 1).replace('>Represent Midsummer<', '>Where to see the beds, and how to represent them<', 1))
    trade = (a.replace("q: 'enquiry=partner' %}#enquire\"", "q: 'enquiry=trade' %}#enquire\" data-ms-landing=\"\" data-ms-pn-phone=\"\"", 1)
              .replace('>Become a partner<', '>Open a project file<', 1).replace('>Represent Midsummer<', '>Samples, drawings and pricing, from the trade desk<', 1))
    assert agents != a and trade != a
    seg = seg.replace(a, a + trade, 1)
    t = t[:i] + seg + t[j:]
    open(p, 'w', encoding='utf-8').write(t)
print('professionals: the phone menu too')

# Round 15: the project desk, composed: the steps of a project beside a room and a detail
p = THEME + '/sections/ms-pro-04.liquid'
t = open(p, encoding='utf-8').read()
if 'ms-pd__steps' not in t:
    a = t.index('<section data-dc-tpl="888"')
    b = t.index('</section>', a) + len('</section>')
    body = '''<section class="ms-pd">
  <div class="ms-pd__in">
    <div class="ms-pd__text">
      <div class="ms-pd__eye">{{ section.settings.t1 }}</div>
      <h2 class="ms-pd__h">{{ section.settings.t2 }}</h2>
      <p class="ms-pd__p">{{ section.settings.t3 }}</p>
      <ol class="ms-pd__steps" role="list">
        {%- for i in (1..3) -%}
          {%- assign kt = 'step' | append: i | append: '_title' -%}{%- assign kx = 'step' | append: i | append: '_text' -%}
          {%- if section.settings[kt] != blank -%}<li><span class="ms-pd__n">0{{ i }}</span><span><b>{{ section.settings[kt] }}</b>{{ section.settings[kx] }}</span></li>{%- endif -%}
        {%- endfor -%}
      </ol>
      <div class="ms-pd__ctas">
        <a class="ms-pd__btn" href="{% render 'ms-link', to: 'enquire', q: 'enquiry=trade' %}#enquire" data-ms-landing>{{ section.settings.t4 }}</a>
        <a class="ms-pd__link" data-ms-enquire="" href="{% render 'ms-link', to: 'contact' %}">{{ section.settings.t5 }}</a>
      </div>
    </div>
    <figure class="ms-pd__fig">
      <img class="ms-pd__big" width="1500" height="2000" loading="lazy" alt="A Midsummer bed in a frescoed loft, beneath a spiral stair" src="{% if section.settings.img1 != blank %}{{ section.settings.img1 | image_url: width: 1600 }}{% else %}{{ 'ms-photo-loft.jpg' | asset_url }}{% endif %}">
      <img class="ms-pd__inset" width="2000" height="1335" loading="lazy" alt="The Midsummer Milano label on a mattress border" src="{{ 'ms-photo-mattress-label.jpg' | asset_url }}">
    </figure>
  </div>
</section>
<style>
  .ms-pd { background: #F1ECE3; padding: clamp(64px, 9vw, 140px) clamp(20px, 5vw, 80px); }
  .ms-pd__in { max-width: 1320px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(40px, 7vw, 120px); align-items: center; }
  .ms-pd__eye { font-size: 11px; letter-spacing: .28em; text-transform: uppercase; color: #7E623B; }
  .ms-pd__h { font-family: Newsreader, Georgia, serif; font-weight: 200; font-size: clamp(32px, 4vw, 56px); line-height: 1.04; letter-spacing: -.02em; margin-top: 16px; }
  .ms-pd__p { font-size: 15px; line-height: 1.9; color: #4A443B; margin-top: 20px; max-width: 46ch; }
  .ms-pd__steps { list-style: none; margin: clamp(28px, 3vw, 40px) 0 0; padding: 0; border-top: 1px solid rgba(23, 20, 15, .16); }
  .ms-pd__steps li { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 12px; padding: 18px 0; border-bottom: 1px solid rgba(23, 20, 15, .16); font-size: 14px; line-height: 1.7; color: #4A443B; }
  .ms-pd__steps b { display: block; font-family: Newsreader, Georgia, serif; font-weight: 300; font-size: 20px; line-height: 1.3; color: #17140F; margin-bottom: 4px; }
  .ms-pd__n { font-family: Newsreader, Georgia, serif; font-size: 15px; color: #7E623B; padding-top: 4px; }
  .ms-pd__ctas { display: flex; flex-wrap: wrap; align-items: center; gap: 18px 30px; margin-top: clamp(28px, 3vw, 40px); }
  .ms-site .ms-pd__btn { display: inline-block; background: #17140F; color: #FBF9F5; padding: 19px 38px; font-size: 11px; letter-spacing: .26em; text-transform: uppercase; }
  .ms-site .ms-pd__link { font-size: 11px; letter-spacing: .24em; text-transform: uppercase; border-bottom: 1px solid #17140F; padding-bottom: 6px; color: #17140F; }
  .ms-pd__fig { position: relative; margin: 0; padding: 0 0 clamp(40px, 6vw, 80px) clamp(40px, 6vw, 96px); }
  .ms-pd__big { display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; }
  .ms-pd__inset { position: absolute; left: 0; bottom: 0; width: 46%; aspect-ratio: 4 / 3; object-fit: cover; box-shadow: 0 0 0 10px #F1ECE3; }
  @media (max-width: 860px) {
    .ms-pd__in { grid-template-columns: minmax(0, 1fr); }
    .ms-pd__fig { order: -1; padding: 0 0 48px 32px; }
    .ms-pd__inset { width: 52%; box-shadow: 0 0 0 7px #F1ECE3; }
  }
</style>'''
    t = t[:a] + body + t[b:]
    t = t.replace('"label": "Image: A Midsummer bed dressed in L"', '"label": "Room photograph"', 1)
    t = t.replace('      "default": "Open a project"\n    },', '      "default": "Open a project file"\n    },', 1)
    steps = (',\n    { "type": "text", "id": "step1_title", "label": "Step 1", "default": "The brief" },\n'
             '    { "type": "text", "id": "step1_text", "label": "Step 1 line", "default": "The plans, the rooms and the feel you want. A person at the atelier answers within one working day." },\n'
             '    { "type": "text", "id": "step2_title", "label": "Step 2", "default": "Drawings and samples" },\n'
             '    { "type": "text", "id": "step2_text", "label": "Step 2 line", "default": "Each system drawn to its room, with the Loro Piana Interiors cloths and the fibres sent to you by post." },\n'
             '    { "type": "text", "id": "step3_title", "label": "Step 3", "default": "Made, delivered, installed" },\n'
             '    { "type": "text", "id": "step3_text", "label": "Step 3 line", "default": "Made by hand in Italy, delivered and dressed by our own team, and regenerated at fifteen years." }\n  ]')
    k = t.rindex('\n  ]')
    t = t[:k] + steps + t[k + len('\n  ]'):]
    json.loads(re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema', t, re.S).group(1))
    open(p, 'w', encoding='utf-8').write(t)
print('professionals: the project desk composed')

# Round 15: every enquiry reaches the store's mail clearly: Shopify's own name field carries the
# visitor's title and name (the mail's sender line and the reply), and each says where it was sent from
p = THEME + '/assets/ms-site.js'
t = open(p, encoding='utf-8').read()
if 'ms-mail-name' not in t:
    t += '''
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
    put('Sent from', [(document.title || '').replace(/\\s+/g, ' ').trim(), '(' + location.origin + location.pathname + location.search + ')'].filter(Boolean).join(' '), mode);
  }, true);
})();
'''
    open(p, 'w', encoding='utf-8').write(t)
print('enquiries: named, and from where')

# Round 16: its own file, run in this one's scope
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r16.py'), encoding='utf-8').read())

# Round 17: its own file, run in this one's scope
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r17.py'), encoding='utf-8').read())

# Round 18: pictures at the width they are seen; the rest of the optimisation pass
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r18.py'), encoding='utf-8').read())

# Round 20: sizes as examples, in cm, and your own size; the rest of Round 20
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r20.py'), encoding='utf-8').read())

# Round 21: new photographs (Inside the bed, Handmade in Italy), and the copy the owner asked for
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r21.py'), encoding='utf-8').read())
# Round 22: the way back clear of the photographs on a phone; white studio grounds laid into the paper
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r22.py'), encoding='utf-8').read())
# Round 24: no regeneration for hotels; a too-bright photograph softened
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r24.py'), encoding='utf-8').read())
# Round 25: photographs, the press wall, hospitality and private jets, a night at Sleep Culture, the atelier's rooms
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r25.py'), encoding='utf-8').read())
# Round 26: the editor's previews, the collection photographs untinted, the press line endless, the galleries composed, the award on Top, the drawings refined
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r26.py'), encoding='utf-8').read())
# Round 27: the award on Top a quiet label, the rooms kept for rest each its own room
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r27.py'), encoding='utf-8').read())
# Round 28: the press line under the system's hand, the award at the corner, the drawings true, phones
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r28.py'), encoding='utf-8').read())
# Round 29: the languages, quietly, in the header, the phone menu and the footer
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_r29.py'), encoding='utf-8').read())
