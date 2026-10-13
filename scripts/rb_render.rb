# Render a JSON template's sections with Ruby Liquid (the engine Shopify runs), strict parse,
# reporting runtime errors and resource scores per section.
# usage: ruby rb_render.rb THEME TEMPLATE CTX.json [OUT.html]
require 'liquid'
require 'json'
THEME, TPL, CTXF, OUT = ARGV

class RawBlock < Liquid::Block
  def parse(tokens); @body = ''; while (t = tokens.shift); return if t =~ /\A{%-?\s*end#{block_name}\s*-?%}\z/; end; end
  def render_to_output_buffer(_c, out); out; end
end
%w[schema javascript].each { |n| Liquid::Template.register_tag(n, Class.new(RawBlock)) }
class PassBlock < Liquid::Block; end
%w[form style stylesheet paginate].each { |n| Liquid::Template.register_tag(n, Class.new(PassBlock)) }
class PassTag < Liquid::Tag; def render_to_output_buffer(_c, out); out; end; end
%w[content_for layout].each { |n| Liquid::Template.register_tag(n, Class.new(PassTag)) }
class GroupTag < Liquid::Tag
  def initialize(n, markup, o); super; @name = markup.strip.delete(%q('")); end
  def render_to_output_buffer(c, out)
    if tag_name == 'sections'
      g = JSON.parse(File.read(File.join(THEME, 'sections', @name + '.json')).sub(%r{\A\s*/\*.*?\*/}m, ''))
      (g['order'] || g['sections'].keys).each { |id| out << RENDER_SECTION.call(g['sections'][id]['type'], id, g['sections'][id], "group #{@name}") }
    else
      sd = (JSON.parse(File.read(File.join(THEME, 'config/settings_data.json')).sub(%r{\A\s*/\*.*?\*/}m, ''))['current']['sections'] || {}) rescue {}
      out << RENDER_SECTION.call(@name, @name, sd[@name] || { 'settings' => {} }, 'static')
    end
    out
  end
end
%w[section sections].each { |n| Liquid::Template.register_tag(n, GroupTag) }

LOC = JSON.parse(File.read(File.join(THEME, 'locales/en.default.json')).sub(%r{\A\s*/\*.*?\*/}m, '')) rescue {}
module ShopFilters
  def src_of(v); v.is_a?(Hash) ? (v['src'] || v['url'] || '') : v.to_s; end
  def image_url(v, *a); v.nil? || v == '' ? '' : src_of(v) + '?w=1'; end
  def img_url(v, *a); image_url(v); end
  def asset_url(v); "/assets/#{v}"; end
  def asset_img_url(v, *a); "/assets/#{v}"; end
  def file_url(v); "/files/#{v}"; end
  def file_img_url(v, *a); "/files/#{v}"; end
  def stylesheet_tag(v, *a); %(<link rel="stylesheet" href="#{v}">); end
  def script_tag(v); %(<script src="#{v}"></script>); end
  def image_tag(v, *a); %(<img src="#{v}">); end
  def placeholder_svg_tag(v, *a); '<svg></svg>'; end
  def json(v); JSON.generate(v); end
  def money(v); "€#{v.to_i / 100}"; end
  def money_without_trailing_zeros(v); money(v); end
  def money_with_currency(v); money(v); end
  def handleize(v); v.to_s.downcase.gsub(/[^a-z0-9]+/, '-').gsub(/\A-|-\z/, ''); end
  def handle(v); handleize(v); end
  def t(k, *a); v = k.to_s.split('.').reduce(LOC) { |o, x| o.is_a?(Hash) ? o[x] : nil }; v.is_a?(String) ? v : k; end
  def link_to(v, url, *a); %(<a href="#{url}">#{v}</a>); end
  def within(v, *a); v; end
  def time_tag(v, *a); v.to_s; end
  def default_pagination(v, *a); ''; end
  def font_face(v, *a); ''; end
  def font_url(v, *a); ''; end
  def font_modify(v, *a); v; end
  def color_to_rgb(v); v; end
  def color_modify(v, *a); v; end
  def structured_data(v); '{}'; end
  def metafield_tag(v, *a); v.to_s; end
  def metafield_text(v, *a); v.to_s; end
  def preload_tag(v, *a); ''; end
  def inline_asset_content(v); ''; end
end
Liquid::Template.register_filter(ShopFilters)

ctx = JSON.parse(File.read(CTXF))
LOOKUPS = Hash.new(0)
class CountDrop < Liquid::Drop
  def initialize(name, h); @name = name; @h = h; end
  def liquid_method_missing(k); LOOKUPS[@name] += 1; LOOKUPS["#{@name}[#{k}]"] += 1; @h[k.to_s]; end
  def key?(k); true; end
  def [](k); liquid_method_missing(k); end
  def to_liquid; self; end
  def size; @h.size; end
  def each(&b); @h.values.each(&b); end
end
%w[collections pages blogs all_products linklists].each { |n| ctx[n] = CountDrop.new(n, ctx[n].is_a?(Hash) ? ctx[n] : {}) }
class SnipFS
  def initialize(dir); @dir = dir; end
  def read_template_file(name)
    f = File.join(@dir, name + '.liquid')
    raise Liquid::FileSystemError, "No such template '#{name}'" unless File.exist?(f)
    File.read(f, encoding: 'UTF-8')
  end
end
fs = SnipFS.new(File.join(THEME, 'snippets'))
strip = ->(s) { s.sub(%r{\A\s*/\*.*?\*/}m, '') }
tpl = JSON.parse(strip.(File.read(File.join(THEME, 'templates', TPL + '.json'))))
schema_of = lambda do |type|
  src = File.read(File.join(THEME, 'sections', type + '.liquid'))
  JSON.parse(src[/{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema/m, 1])
end
defaults = lambda do |settings, values|
  out = {}
  (settings || []).each { |s| out[s['id']] = s['default'] if s['id'] && s.key?('default') }
  out.merge!(values || {})
  # Shopify hands a blank text setting to Liquid as nil
  out.each { |k, v| out[k] = nil if v == '' }
  out
end
html = +''
total = { 'render' => 0, 'assign' => 0 }
RENDER_SECTION = lambda do |type, id, data, where|
  next '' if data['disabled']
  sch = schema_of.(type) rescue {}
  local = (sch['blocks'] || []).map { |b| [b['type'], b] }.to_h
  border = data['block_order'] || (data['blocks'] || {}).keys
  blocks = border.map { |bid| b = data['blocks'][bid]; { 'id' => bid, 'type' => b['type'], 'settings' => defaults.((local[b['type']] || {})['settings'], b['settings']), 'shopify_attributes' => '' } }
  sec = { 'id' => id, 'settings' => defaults.(sch['settings'], data['settings']), 'blocks' => blocks }
  src = File.read(File.join(THEME, 'sections', type + '.liquid')).gsub(/\{%-?\s*render\s+block\s*-?%\}/, '')
  begin
    t = Liquid::Template.parse(src, error_mode: :strict, line_numbers: true)
  rescue => e
    puts "PARSE #{type}: #{e.message}"; next ''
  end
  t0 = Time.now
  lc = Liquid::Context.build(environments: [{ 'section' => sec }], static_environments: [ctx], registers: { file_system: fs }, rethrow_errors: false)
  out = t.render(lc)
  dt = ((Time.now - t0) * 1000).round
  rl = lc.resource_limits
  errs = lc.errors.map { |e| e.message.lines.first.strip }.uniq
  puts format('%-24s %-22s %6d ms  out %7d  render_score %8d  assign_score %9d  %s', id, type, dt, out.bytesize, rl.cumulative_render_score.to_i, rl.cumulative_assign_score.to_i, errs.empty? ? 'ok' : "ERRORS #{errs.size}")
  errs.first(8).each { |m| puts "    ! #{m}" }
  out.scan(/Liquid (?:syntax )?error[^<\n]{0,160}/).uniq.first(8).each { |m| puts "    ! in output: #{m}" }
  total["render"] += rl.cumulative_render_score.to_i; total["assign"] += rl.cumulative_assign_score.to_i
  %(<div id="shopify-section-#{id}" class="shopify-section">#{out}</div>)
end
tpl['order'].each { |id| html << RENDER_SECTION.call(tpl['sections'][id]['type'], id, tpl['sections'][id], 'template') }
puts "SECTIONS render_score #{total['render']} assign_score #{total['assign']} bytes #{html.bytesize}"
if ENV['LAYOUT'] != '0'
  lname = tpl['layout'] || 'theme'
  lsrc = File.read(File.join(THEME, 'layout', lname + '.liquid'))
  lt = Liquid::Template.parse(lsrc, error_mode: :strict, line_numbers: true)
  lc = Liquid::Context.build(environments: [{}], static_environments: [ctx.merge('content_for_layout' => html, 'content_for_header' => '<!-- header -->')], registers: { file_system: fs }, rethrow_errors: false)
  t0 = Time.now
  page = lt.render(lc)
  puts format('LAYOUT %-10s %6d ms  out %7d  %s', lname, ((Time.now - t0) * 1000).round, page.bytesize, lc.errors.empty? ? 'ok' : "ERRORS #{lc.errors.size}")
  lc.errors.map { |e| e.message.lines.first.strip }.uniq.first(10).each { |m| puts "    ! #{m}" }
  html = page
end
File.write(OUT, html) if OUT
puts 'LOOKUPS ' + %w[collections pages blogs all_products linklists].map { |n| "#{n}=#{LOOKUPS[n]}" }.join(' ')
puts '  allp: ' + LOOKUPS.keys.grep(/^all_products\[/).join(' ')
puts '  top: ' + LOOKUPS.reject { |k, _| !k.include?('[') }.sort_by { |_, v| -v }.first(12).map { |k, v| "#{k}:#{v}" }.join(' ')
