/* Mellow Oaks concept: studio layer. Intro curtain, split-text, scrubbed statement, counters, marquee,
   phase preview, parallax, clip reveals, magnetic buttons, cursor, progress bar. No dependencies. */
(function () {
  var doc = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  /* ---------- scroll progress (works with reduced motion too: it is information, not motion) ---------- */
  var bar = document.createElement('div');
  bar.className = 'scrollbar'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  /* counters work in every mode */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), t0 = null, dur = 1600;
    if (reduce || isNaN(to)) { el.textContent = to; return; }
    (function step(t) {
      if (t0 === null) t0 = t;
      var p = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(to * e);
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  if (reduce) {
    $$('[data-count]').forEach(function (el) { el.textContent = el.getAttribute('data-count'); });
    var tick0 = false;
    addEventListener('scroll', function () {
      if (tick0) return; tick0 = true;
      requestAnimationFrame(function () {
        var h = doc.scrollHeight - innerHeight;
        bar.style.setProperty('--sp', h > 0 ? clamp(scrollY / h, 0, 1).toFixed(4) : 0);
        tick0 = false;
      });
    }, { passive: true });
    doc.classList.add('fx-ready');
    return;
  }

  /* ---------- text splitting ---------- */
  function splitNode(node, state) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
          var w = document.createElement('span'), i = document.createElement('span');
          w.className = 'w'; i.className = 'wi'; i.textContent = part;
          i.style.setProperty('--i', state.i++);
          w.appendChild(i); frag.appendChild(w);
        });
        n.parentNode.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') {
        splitNode(n, state);
      }
    });
  }
  function split(el) {
    if (el.classList.contains('sp')) return;
    var label = el.textContent.replace(/\s+/g, ' ').trim();
    el.setAttribute('aria-label', label);
    var st = { i: 0 };
    splitNode(el, st);
    $$('.w', el).forEach(function (w) { w.setAttribute('aria-hidden', 'true'); });
    el.classList.add('sp');
  }
  var reveal = function (el, base) { el.style.setProperty('--base', (base || 0) + 'ms'); el.classList.add('in'); };

  /* scrubbed statement words */
  $$('[data-scrub]').forEach(function (p) {
    var label = p.textContent.replace(/\s+/g, ' ').trim();
    p.setAttribute('aria-label', label);
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var f = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { f.appendChild(document.createTextNode(' ')); return; }
            var s = document.createElement('span'); s.className = 'sw'; s.textContent = part; s.setAttribute('aria-hidden', 'true'); f.appendChild(s);
          });
          n.parentNode.replaceChild(f, n);
        } else if (n.nodeType === 1) walk(n);
      });
    })(p);
    p._words = $$('.sw', p);
  });

  var headings = $$('.hero h1, .ph-copy h1, .post-head h1, .apply-hero h1, .head h2, .split-copy h2, .cta h2, .visit h2, .card-plain h2');
  headings.forEach(split);

  /* ---------- intro curtain ---------- */
  var curtain = $('.curtain');
  function release() {
    doc.classList.add('fx-ready');
    $$('.hero h1.sp, .ph-copy h1.sp, .post-head h1.sp, .apply-hero h1.sp').forEach(function (h) { reveal(h, 120); });
  }
  if (curtain && doc.classList.contains('fx-intro')) {
    var cnt = $('.cur-count', curtain), t0 = null, dur = 1250;
    try { sessionStorage.setItem('mo_intro', '1'); } catch (e) {}
    (function step(t) {
      if (t0 === null) t0 = t;
      var p = clamp((t - t0) / dur, 0, 1), e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      cnt.textContent = Math.round(e * 100);
      curtain.style.setProperty('--c', e.toFixed(3));
      if (p < 1) return requestAnimationFrame(step);
      setTimeout(function () {
        curtain.classList.add('go');
        doc.classList.remove('fx-intro');
        setTimeout(release, 420);
        setTimeout(function () { curtain.remove(); }, 1300);
      }, 180);
    })(performance.now());
  } else {
    doc.classList.remove('fx-intro');
    requestAnimationFrame(release);
  }

  /* ---------- reveal on view ---------- */
  var vh = innerHeight;
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        if (el.classList.contains('sp')) reveal(el, 0); else el.classList.add('in');
        if (el.hasAttribute('data-count')) countUp(el);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: .12 });
    headings.forEach(function (h) {
      if (h.matches('.hero h1, .ph-copy h1, .post-head h1, .apply-hero h1')) return;
      io.observe(h);
    });
    $$('.split-photo, .ph-photo, .post-cover, .video, .map').forEach(function (el) {
      if (el.getBoundingClientRect().top < vh * .9) return;
      el.classList.add('clip'); io.observe(el);
    });
    $$('[data-count]').forEach(function (el) { el.textContent = '0'; io.observe(el); });
    var wm = $('.wordmark'); if (wm) io.observe(wm);
  } else {
    $$('.sp').forEach(function (el) { reveal(el, 0); });
    $$('[data-count]').forEach(function (el) { el.textContent = el.getAttribute('data-count'); });
    var wm2 = $('.wordmark'); if (wm2) wm2.classList.add('in');
  }

  /* ---------- marquee driven by scroll speed ---------- */
  var mq = $('.mq-track'), mqAnim = null;
  if (mq && mq.animate) {
    mqAnim = mq.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(-50%)' }], { duration: 38000, iterations: Infinity });
  }

  /* ---------- phase list: photo follows the pointer ---------- */
  var pl = $('.plist'), peek = null;
  if (pl && fine) {
    peek = document.createElement('div');
    peek.className = 'plist-peek'; peek.setAttribute('aria-hidden', 'true');
    $$('a[data-img]', pl).forEach(function (a) {
      var im = new Image(); im.alt = ''; im.decoding = 'async'; im.src = a.getAttribute('data-img'); im.dataset.k = a.getAttribute('href'); peek.appendChild(im);
    });
    document.body.appendChild(peek);
    var px = 0, py = 0, tx = 0, ty = 0, pOn = false;
    pl.addEventListener('mousemove', function (e) { tx = e.clientX + 36; ty = e.clientY - peek.offsetHeight / 2; });
    $$('a', pl).forEach(function (a) {
      var show = function () {
        var k = a.getAttribute('href');
        $$('img', peek).forEach(function (im) { im.classList.toggle('on', im.dataset.k === k); });
        peek.classList.add('on'); pOn = true;
      };
      a.addEventListener('mouseenter', show); a.addEventListener('focus', function () {
        var r = a.getBoundingClientRect(); tx = r.right - peek.offsetWidth - 80; ty = r.top - peek.offsetHeight / 2 + r.height / 2; show();
      });
      a.addEventListener('mouseleave', function () { peek.classList.remove('on'); pOn = false; });
      a.addEventListener('blur', function () { peek.classList.remove('on'); pOn = false; });
    });
    (function loop() {
      px += (tx - px) * .14; py += (ty - py) * .14;
      peek.style.transform = 'translate3d(' + px.toFixed(1) + 'px,' + py.toFixed(1) + 'px,0)';
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- magnetic buttons ---------- */
  if (fine) {
    $$('.btn, .hero-badge, .ask-btn').forEach(function (b) {
      b.classList.add('magnet');
      b.addEventListener('mousemove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--mx', ((e.clientX - r.left - r.width / 2) * .22).toFixed(1) + 'px');
        b.style.setProperty('--my', ((e.clientY - r.top - r.height / 2) * .32).toFixed(1) + 'px');
      });
      b.addEventListener('mouseleave', function () { b.style.setProperty('--mx', '0px'); b.style.setProperty('--my', '0px'); });
    });

    /* ---------- cursor ---------- */
    var dot = document.createElement('div'), ring = document.createElement('div'), lab = document.createElement('span');
    dot.className = 'cur-dot'; ring.className = 'cur-ring'; ring.appendChild(lab);
    dot.setAttribute('aria-hidden', 'true'); ring.setAttribute('aria-hidden', 'true');
    document.body.appendChild(dot); document.body.appendChild(ring);
    var mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my, seen = false;
    addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!seen) { seen = true; rx = mx; ry = my; doc.classList.add('fx-cursor'); }
      var t = e.target.closest ? e.target : null;
      var tag = t && t.closest('[data-cursor]'), link = t && t.closest('a, button, label, summary'), field = t && t.closest('input, select, textarea, iframe');
      ring.classList.toggle('label', !!tag);
      ring.classList.toggle('link', !!link && !tag);
      ring.classList.toggle('field', !!field); dot.classList.toggle('field', !!field);
      if (tag) lab.textContent = tag.getAttribute('data-cursor');
    }, { passive: true });
    document.addEventListener('mouseleave', function () { doc.classList.remove('fx-cursor'); seen = false; });
    addEventListener('mousedown', function () { ring.classList.add('down'); });
    addEventListener('mouseup', function () { ring.classList.remove('down'); });
    (function loop() {
      rx += (mx - rx) * .18; ry += (my - ry) * .18;
      dot.style.transform = 'translate3d(' + mx + 'px,' + my + 'px,0)';
      ring.style.transform = 'translate3d(' + rx.toFixed(1) + 'px,' + ry.toFixed(1) + 'px,0)';
      requestAnimationFrame(loop);
    })();
    $$('.ptile, .card, .news.rich a, .split-photo').forEach(function (el) { if (!el.hasAttribute('data-cursor') && el.tagName === 'A') el.setAttribute('data-cursor', 'View'); });
    $$('.video-btn').forEach(function (el) { el.setAttribute('data-cursor', 'Play'); });
    $$('.plist a').forEach(function (el) { el.setAttribute('data-cursor', 'Open'); });
  }

  /* ---------- scroll loop: progress, header, hero shrink, parallax, scrub, marquee speed ---------- */
  var header = $('.site-header'), hero = $('.hero-home'), lastY = scrollY, vel = 0, ticking = false;
  var par = $$('.split-photo img, .n-img img, .post-cover img, .ptile img');
  var scrubs = $$('[data-scrub]');
  var navBtn = $('.menu-btn');

  function frame() {
    ticking = false;
    var y = scrollY, h = doc.scrollHeight - innerHeight, dy = y - lastY;
    lastY = y;
    bar.style.setProperty('--sp', h > 0 ? clamp(y / h, 0, 1).toFixed(4) : 0);

    if (header) {
      var menuOpen = navBtn && navBtn.getAttribute('aria-expanded') === 'true';
      var focusIn = header.contains(document.activeElement) && document.activeElement !== document.body;
      if (y > 320 && dy > 6 && !menuOpen && !focusIn) header.classList.add('hide');
      else if (dy < -4 || y < 200 || menuOpen) header.classList.remove('hide');
    }

    if (hero) {
      var p = clamp(y / (hero.offsetHeight * .8), 0, 1);
      hero.style.setProperty('--hr', (p * 44).toFixed(1) + 'px');
    }

    par.forEach(function (img) {
      var box = img.parentNode, r = box.getBoundingClientRect();
      if (r.bottom < -80 || r.top > innerHeight + 80) return;
      var t = ((r.top + r.height / 2) - innerHeight / 2) / (innerHeight / 2 + r.height / 2);
      img.style.setProperty('--fy', (clamp(t, -1, 1) * r.height * -.06).toFixed(1) + 'px');
    });

    scrubs.forEach(function (p) {
      var r = p.getBoundingClientRect();
      if (r.bottom < -50 || r.top > innerHeight) return;
      var prog = clamp((innerHeight * .88 - r.top) / (innerHeight * .55 + r.height * .6), 0, 1.05), n = p._words.length;
      p._words.forEach(function (w, i) { w.classList.toggle('on', i / n < prog); });
    });

    if (mqAnim) {
      vel += (clamp(dy, -60, 60) - vel) * .2;
      var rate = (vel === 0 ? 1 : (vel > 0 ? 1 : -1)) * (1 + Math.abs(vel) * .35);
      mqAnim.updatePlaybackRate(rate);
    }
    if (Math.abs(vel) > .2 || (mqAnim && Math.abs(dy) > 0)) request();
  }
  function request() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);
  /* marquee glides back to normal speed after scrolling stops */
  setInterval(function () { if (mqAnim && Math.abs(vel) > .05) { vel *= .8; request(); } else if (mqAnim && mqAnim.playbackRate !== 1) { mqAnim.updatePlaybackRate(1); vel = 0; } }, 60);
  frame();

  /* anchors on the same page glide, but never fight the browser's own jump on load */
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1), t = id && document.getElementById(id);
      if (!t) return;
      e.preventDefault();
      t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', '#' + id);
    });
  });
})();
