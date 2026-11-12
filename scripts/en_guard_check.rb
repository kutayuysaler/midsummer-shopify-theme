# Render every JSON template's sections in a locale, optionally with the protected (non-language)
# settings scrambled the way a machine translation would; compare the outputs to prove the guard.
# usage: ruby scripts/en_guard_check.rb theme it 1 /tmp/out scripts/en_guard_protect.json
# usage: ruby r35.rb THEME LOCALE POISON(0|1) OUTDIR PROTECT.json
require 'liquid'; require 'json'; require 'digest'; require 'fileutils'
THEME, LOC, POISON, OUTDIR, PROT = ARGV
POISON_ON = POISON == '1'
strip = ->(s) { s.sub(%r{\A\s*/\*.*?\*/}m, '') }
LOCF = LOC == 'en' ? 'en.default.json' : "#{LOC}.json"
LOCD = JSON.parse(strip.(File.read(File.join(THEME, 'locales', LOCF))))
PROTECT = JSON.parse(File.read(PROT))
class RawBlock < Liquid::Block
  def parse(tokens); @body = ''; while (t = tokens.shift); return if t =~ /\A{%-?\s*end#{block_name}\s*-?%}\z/; end; end
  def render_to_output_buffer(_c, out); out; end
end
%w[schema javascript].each { |n| Liquid::Template.register_tag(n, Class.new(RawBlock)) }
class PassBlock < Liquid::Block; end
%w[form style stylesheet paginate].each { |n| Liquid::Template.register_tag(n, Class.new(PassBlock)) }
class PassTag < Liquid::Tag; def render_to_output_buffer(_c, out); out; end; end
%w[content_for layout section sections].each { |n| Liquid::Template.register_tag(n, Class.new(PassTag)) }
module ShopFilters
  def src_of(v); v.is_a?(Hash) ? (v['src'] || v['url'] || '') : v.to_s; end
  def image_url(v, *a); v.nil? || v == '' ? '' : src_of(v) + '?w=1'; end
  def img_url(v, *a); image_url(v); end
  def asset_url(v); "/assets/#{v}"; end
  def asset_img_url(v, *a); "/assets/#{v}?#{a.join}"; end
  def file_url(v); "/files/#{v}"; end
  def json(v); JSON.generate(v.respond_to?(:to_liquid) && !v.is_a?(String) && !v.is_a?(Numeric) && !v.nil? && !v.is_a?(Array) && !v.is_a?(Hash) ? v.to_s : v); end
  def md5(v); Digest::MD5.hexdigest(v.to_s); end
  def handleize(v); v.to_s.downcase.gsub(/[^a-z0-9]+/, '-').gsub(/\A-|-\z/, ''); end
  def handle(v); handleize(v); end
  def t(k, *a); v = k.to_s.split('.').reduce(LOCD) { |o, x| o.is_a?(Hash) ? o[x] : nil }; v.is_a?(String) ? v : "translation missing: #{LOC}.#{k}"; end
  def money(v); "€#{v.to_i / 100}"; end
  def link_to(v, url, *a); %(<a href="#{url}">#{v}</a>); end
  def stylesheet_tag(v, *a); ''; end
  def script_tag(v); ''; end
  def image_tag(v, *a); %(<img src="#{v}">); end
  def placeholder_svg_tag(v, *a); '<svg></svg>'; end
  def structured_data(v); '{}'; end
  def font_face(v, *a); ''; end
  def font_url(v, *a); ''; end
  def color_to_rgb(v); v; end
end
Liquid::Template.register_filter(ShopFilters)
class EmptyDrop < Liquid::Drop; def liquid_method_missing(_k); ''; end; def to_s; ''; end; def blank?; true; end; end
class Coll < Liquid::Drop
  def initialize(h); @h = h; end
  def liquid_method_missing(k); @h.key?(k.to_s) ? @h[k.to_s] : EmptyDrop.new; end
  def [](k); liquid_method_missing(k); end
  def each(&b); @h.values.each(&b); end
  def size; @h.size; end
end
press = JSON.parse(strip.(File.read(File.join(THEME, 'templates/blog.press.json'))))['sections'].values.flat_map { |s| (s['blocks'] || {}).values }.map { |b| (b['settings'] || {})['link'].to_s.split('/').last }.compact
blogs = {}
press.each_with_index { |h, i| blogs[h] = { 'handle' => h, 'title' => "Press: #{h}", 'articles_count' => (i % 3 == 0 ? 0 : 2), 'url' => "/#{LOC == 'en' ? '' : LOC + '/'}blogs/#{h}", 'articles' => [] } }
%w[news journal projects press].each { |h| blogs[h] = { 'handle' => h, 'title' => h.capitalize, 'articles_count' => 0, 'url' => "/blogs/#{h}", 'articles' => [] } }
sd = JSON.parse(strip.(File.read(File.join(THEME, 'config/settings_data.json'))))
gsettings = sd['current'].is_a?(Hash) ? sd['current'].reject { |k, _| k == 'sections' || k == 'blocks' } : {}
base_ctx = {
  'request' => { 'locale' => { 'iso_code' => LOC, 'primary' => LOC == 'en', 'root_url' => LOC == 'en' ? '/' : "/#{LOC}" }, 'path' => '/x', 'design_mode' => false, 'page_type' => 'page', 'host' => 'midsummer-milano.com' },
  'shop' => { 'name' => 'Midsummer Milano', 'url' => 'https://midsummer-milano.com', 'locale' => LOC, 'published_locales' => [] },
  'settings' => gsettings, 'blogs' => Coll.new(blogs), 'collections' => Coll.new({}), 'pages' => Coll.new({}), 'all_products' => Coll.new({}), 'linklists' => Coll.new({}),
  'blog' => blogs['press'], 'localization' => { 'available_languages' => [] }, 'routes' => { 'root_url' => '/', 'search_url' => '/search', 'cart_url' => '/cart' }, 'canonical_url' => 'https://midsummer-milano.com/x'
}
class SnipFS
  def initialize(dir); @dir = dir; end
  def read_template_file(name); f = File.join(@dir, name + '.liquid'); raise Liquid::FileSystemError, "No such template '#{name}'" unless File.exist?(f); File.read(f, encoding: 'UTF-8'); end
end
fs = SnipFS.new(File.join(THEME, 'snippets'))
schemas = {}
schema_of = ->(type) { schemas[type] ||= (JSON.parse(File.read(File.join(THEME, 'sections', type + '.liquid'))[/{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema/m, 1]) rescue {}) }
defaults = lambda do |settings, values|
  out = {}; (settings || []).each { |s| out[s['id']] = s['default'] if s['id'] && s.key?('default') }
  out.merge!(values || {}); out.each { |k, v| out[k] = nil if v == '' }; out
end
poison = ->(v) { v.is_a?(String) && !v.empty? ? "trad-#{v.reverse}-ita" : v }
prot = ->(type, btype, id) { PROTECT.any? { |p| p[0] == type && p[1] == btype && p[2] == id } }
parsed = {}
FileUtils.mkdir_p(OUTDIR)
nerr = 0
Dir[File.join(THEME, 'templates', '*.json')].sort.each do |f|
  name = File.basename(f, '.json')
  tpl = JSON.parse(strip.(File.read(f))) rescue next
  next unless tpl['sections']
  base, suffix = name.split('.', 2)
  ctx = base_ctx.merge('template' => { 'name' => base, 'suffix' => suffix, 'directory' => nil })
  html = +''
  tpl['order'].each do |key|
    data = tpl['sections'][key]; next if data['disabled']
    type = data['type']; next unless File.exist?(File.join(THEME, 'sections', type + '.liquid'))
    sch = schema_of.(type); local = (sch['blocks'] || []).map { |b| [b['type'], b] }.to_h
    bord = data['block_order'] || (data['blocks'] || {}).keys
    ss = (data['settings'] || {}).dup
    ss.each_key { |k| ss[k] = poison.(ss[k]) if POISON_ON && prot.(type, nil, k) }
    blocks = bord.map do |bid|
      b = data['blocks'][bid]; bs = (b['settings'] || {}).dup
      bs.each_key { |k| bs[k] = poison.(bs[k]) if POISON_ON && prot.(type, b['type'], k) }
      { 'id' => bid, 'type' => b['type'], 'settings' => defaults.((local[b['type']] || {})['settings'], bs), 'shopify_attributes' => '' }
    end
    sec = { 'id' => "template--1__#{key}", 'settings' => defaults.(sch['settings'], ss), 'blocks' => blocks }
    t = (parsed[type] ||= Liquid::Template.parse(File.read(File.join(THEME, 'sections', type + '.liquid')).gsub(/\{%-?\s*render\s+block\s*-?%\}/, ''), error_mode: :strict, line_numbers: true))
    lc = Liquid::Context.build(environments: [{ 'section' => sec }], static_environments: [ctx], registers: { file_system: fs }, rethrow_errors: false)
    out = t.render(lc)
    errs = lc.errors.map { |e| e.message.lines.first.strip }.uniq
    unless errs.empty?
      nerr += 1
      puts "#{name} #{key} #{type}: #{errs.first(3).join(' | ')}" if ENV['SHOWERR']
    end
    html << "<!-- #{key} #{type} -->\n" << out << "\n"
  end
  File.write(File.join(OUTDIR, name + '.html'), html)
end
puts "rendered #{Dir[File.join(OUTDIR, '*.html')].size} templates, sections with errors: #{nerr}"
