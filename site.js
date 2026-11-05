/* Mellow Oaks concept: menus, dropdowns, video, enquiry form and motion. No dependencies. */
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = function () { return window.matchMedia('(min-width: 1001px)').matches; };

  /* phone and tablet menu, animated open and close */
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  function closeMenu() {
    if (!nav.classList.contains('open')) return;
    btn.setAttribute('aria-expanded', 'false');
    if (reduce) { nav.classList.remove('open'); return; }
    nav.classList.add('closing');
    var done = function () { nav.classList.remove('open', 'closing'); };
    nav.addEventListener('animationend', done, { once: true });
    setTimeout(done, 400);
  }
  if (btn && nav) {
    btn.addEventListener('click', function () {
      if (nav.classList.contains('open') && !nav.classList.contains('closing')) { closeMenu(); return; }
      nav.classList.remove('closing'); nav.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
    });
  }

  /* dropdowns: hover and focus on desktop (CSS), the arrow button on touch and keyboard, accordions on phones */
  var subs = Array.prototype.slice.call(document.querySelectorAll('.has-sub'));
  function setOpen(li, open) {
    li.classList.toggle('open', open);
    li.querySelector('.sub-toggle').setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  subs.forEach(function (li) {
    li.querySelector('.sub-toggle').addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !li.classList.contains('open');
      if (desktop()) subs.forEach(function (o) { if (o !== li) setOpen(o, false); });
      setOpen(li, open);
    });
  });
  document.addEventListener('click', function (e) {
    if (!desktop()) return;
    subs.forEach(function (li) { if (!li.contains(e.target)) setOpen(li, false); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    subs.forEach(function (li) { if (li.classList.contains('open')) { setOpen(li, false); li.querySelector('.sub-toggle').focus(); } });
    closeMenu();
  });
  /* on phones, open the section of the page you are on */
  var cur = document.querySelector('.has-sub.is-current');
  if (cur && !desktop()) setOpen(cur, true);

  /* school tour video loads only when asked */
  document.querySelectorAll('[data-video]').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.getAttribute('data-video') + '?autoplay=1&rel=0';
      f.title = 'Mellow Oaks Academy school tour video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });

  /* enquiry form (demo: nothing is sent) */
  var q = document.getElementById('enquiry');
  if (q) q.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true;
    [['q-name', function (v) { return v.trim().length > 1; }, 'Enter your name.'],
     ['q-phone', function (v) { return v.replace(/\D/g, '').length >= 9; }, 'Enter a mobile number with at least 9 digits.']].forEach(function (c) {
      var f = document.getElementById(c[0]), bad = !c[1](f.value);
      f.setAttribute('aria-invalid', bad ? 'true' : 'false');
      f.parentNode.querySelector('.err').textContent = bad ? c[2] : '';
      if (bad && ok) f.focus();
      if (bad) ok = false;
    });
    if (ok) { var d = q.querySelector('.done'); d.hidden = false; d.focus(); q.reset(); }
  });

  /* header shadow and gentle photo parallax */
  var header = document.querySelector('.site-header');
  var par = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll('.hero-media img, .ph-photo img'));
  var tick = false;
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 8);
    par.forEach(function (img) {
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      img.style.setProperty('--py', Math.max(-40, Math.min(40, -r.top * 0.08)).toFixed(1) + 'px');
    });
    tick = false;
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  if (reduce) return;

  /* lazy photos fade in as they load */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
    if (img.complete && img.naturalWidth) return;
    img.classList.add('img-wait');
    var show = function () { img.classList.remove('img-wait'); };
    img.addEventListener('load', show, { once: true });
    img.addEventListener('error', show, { once: true });
  });

  /* content below the fold glides in; groups arrive one item after another */
  if (!('IntersectionObserver' in window)) return;
  var vh = innerHeight;
  var below = function (el) { return el.getBoundingClientRect().top > vh * 0.92; };
  var targets = [];
  document.querySelectorAll('.path, .cards, .ptiles, .news, .features, .steps, .trio, .gallery, .fee-grid, .roles, .foot-grid').forEach(function (g) {
    if (!below(g)) return;
    g.setAttribute('data-rv', '');
    Array.prototype.forEach.call(g.children, function (c, i) { c.classList.add('rv'); c.style.setProperty('--d', Math.min(i, 7)); });
    targets.push(g);
  });
  document.querySelectorAll('.head, .split-photo, .split-copy, .video-grid > *, .cta-inner > *, .visit-copy, .map, .card-plain, .note, .chips').forEach(function (el) {
    if (!below(el) || el.closest('[data-rv]')) return;
    el.classList.add('rv');
    targets.push(el);
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target, items = el.hasAttribute('data-rv') ? Array.prototype.slice.call(el.children) : [el];
      items.forEach(function (it) {
        it.classList.add('in');
        setTimeout(function () { it.classList.remove('rv', 'in'); it.style.removeProperty('--d'); }, 1500);
      });
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  targets.forEach(function (t) { io.observe(t); });
})();
