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
