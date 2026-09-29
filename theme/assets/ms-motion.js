/* Midsummer Milano: scroll reveal.
   Content below the fold fades up once as it enters the viewport. Nothing is
   hidden before this runs, content already on screen is left alone, the theme
   editor and reduced-motion visitors are skipped, and a timer finishes any
   animation that stalls. */
(() => {
  if (window.Shopify && window.Shopify.designMode) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window) || !Element.prototype.animate) return;
  const SEL = 'main .shopify-section :is(h1,h2,h3,h4,p,blockquote,img,video,.button,.product-card,product-card)';
  const SKIP = 'header, footer, dialog, [role="dialog"], .drawer, slideshow-component, marquee-component, [data-ms-static]';
  const CARD = '.product-card, product-card';
  const ez = 'cubic-bezier(.2,.7,.2,1)';
  const seen = new WeakSet();
  const io = new IntersectionObserver((entries) => {
    let k = 0;
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      const el = en.target; io.unobserve(el);
      const media = el.tagName === 'IMG' || el.tagName === 'VIDEO';
      const a = el.animate(media
        ? [{ opacity: 0, transform: 'scale(1.04)' }, { opacity: 1, transform: 'none' }]
        : [{ opacity: 0, transform: 'translateY(22px)' }, { opacity: 1, transform: 'none' }],
        { duration: media ? 1100 : 760, delay: Math.min(k++, 6) * 75, easing: ez, fill: 'backwards' });
      setTimeout(() => { try { if (a.playState !== 'finished') a.finish(); } catch (e) {} }, 2800);
    }
  }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
  const scan = (root) => {
    const vh = window.innerHeight;
    root.querySelectorAll(SEL).forEach((el) => {
      if (seen.has(el)) return; seen.add(el);
      if (el.closest(SKIP)) return;
      if (el.parentElement && el.parentElement.closest(CARD)) return;
      const pos = getComputedStyle(el).position;
      if (pos === 'absolute' || pos === 'fixed') return;
      if (el.getBoundingClientRect().top < vh) return;
      io.observe(el);
    });
  };
  const start = () => scan(document);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
