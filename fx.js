/* Mellow Oaks Academy: motion layer (GSAP, ScrollTrigger, SplitText, Lenis). See DESIGN.md.
   Verb: grow outward. One clock: everything runs on the GSAP ticker. Reduced motion: nothing is hidden, nothing is pinned. */
(function () {
  var doc = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  function ready() { doc.classList.add('fx-ready'); }
  function staticState() {
    $$('[data-count]').forEach(function (el) { el.textContent = el.getAttribute('data-count'); });
    $$('.rs-ring').forEach(function (r) { r.style.strokeDasharray = 'none'; });
    ready();
  }
  if (reduce || !window.gsap || !window.ScrollTrigger || !window.SplitText) { staticState(); return; }

  try { init(); } catch (e) { console.error(e); ready(); }

  function init() {
    gsap.registerPlugin(ScrollTrigger, SplitText);
    gsap.defaults({ ease: 'power3.out', duration: 1 });

    /* smooth scroll, on the same clock */
    var lenis = null;
    /* smooth scroll only for a real mouse on a wide screen; phones, tablets and narrow windows keep native scrolling */
    if (window.Lenis && matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1001px)').matches) {
      lenis = new Lenis({ lerp: .11, smoothWheel: true });
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
      /* panels that scroll on their own must keep native wheel behaviour */
      $$('#nav, .ask-panel, .ask-body').forEach(function (el) { el.setAttribute('data-lenis-prevent', ''); });
      new MutationObserver(function () {
        doc.classList.contains('ask-open') ? lenis.stop() : lenis.start();
      }).observe(doc, { attributes: true, attributeFilter: ['class'] });
      $$('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var t = document.getElementById(a.getAttribute('href').slice(1));
          if (!t) return;
          e.preventDefault(); lenis.scrollTo(t, { offset: -90 });
        });
      });
    }

    /* buttons: the fill grows outward from where the pointer entered */
    $$('.btn').forEach(function (b) {
      var set = function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--bx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        b.style.setProperty('--by', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      };
      b.addEventListener('pointerenter', set); b.addEventListener('pointerleave', set);
    });

    /* ---------- first screen ---------- */
    var intro = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
    var hero = $('.hero-home');
    if (hero) {
      var rings = $$('.hr-rings circle', hero);
      gsap.set(rings, { strokeDasharray: 1, strokeDashoffset: 1 });
      gsap.set('.hd-photo', { opacity: 1, clipPath: 'circle(0% at 50% 50%)' });
      gsap.set('.hero-copy .pill,.hero-copy .lede,.hero-copy .btn-row', { opacity: 0, y: 22 });
      gsap.set('.hero-facts li', { opacity: 0, y: 16 });
      intro.to('.hd-photo', { clipPath: 'circle(72% at 50% 50%)', duration: 1.7, ease: 'power2.inOut' }, 0)
           .to(rings, { strokeDashoffset: 0, duration: 2.4, stagger: .14, ease: 'power2.inOut' }, .2)
           .to('.hero-copy .pill', { opacity: 1, y: 0 }, .35)
           .to('.hero-copy .lede', { opacity: 1, y: 0 }, .75)
           .to('.hero-copy .btn-row', { opacity: 1, y: 0 }, .9)
           .to('.hero-facts li', { opacity: 1, y: 0, stagger: .1 }, 1.2);
      gsap.to('.hr-rings', { scale: 1.015, duration: 7, yoyo: true, repeat: -1, ease: 'sine.inOut', transformOrigin: '50% 50%' });
    }
    var inner = $('.page-hero');
    if (inner) {
      gsap.set('.ph-disc', { opacity: 1, clipPath: 'circle(0% at 50% 50%)' });
      gsap.set('.ph-rings circle', { transformOrigin: '50% 50%', scale: .8, opacity: 0 });
      gsap.set('.ph-copy .crumbs,.ph-copy .kicker,.ph-copy .lede,.ph-copy .btn-row', { opacity: 0, y: 18 });
      intro.to('.ph-disc', { clipPath: 'circle(72% at 50% 50%)', duration: 1.5, ease: 'power2.inOut' }, 0)
           .to('.ph-rings circle', { scale: 1, opacity: 1, duration: 1.6, stagger: .1 }, .1)
           .to('.ph-copy .crumbs,.ph-copy .kicker', { opacity: 1, y: 0 }, .2)
           .to('.ph-copy .lede', { opacity: 1, y: 0 }, .7)
           .to('.ph-copy .btn-row', { opacity: 1, y: 0 }, .85);
      gsap.to('.ph-rings', { scale: 1.012, duration: 7, yoyo: true, repeat: -1, ease: 'sine.inOut', transformOrigin: '50% 50%' });
    }
    var h1 = $('main h1');
    function revealLines(el, st) {
      return SplitText.create(el, {
        type: 'lines', mask: 'lines', autoSplit: true, aria: 'auto',
        onSplit: function (self) {
          return gsap.from(self.lines, Object.assign({ yPercent: 108, duration: 1.1, stagger: .09 }, st ? { scrollTrigger: st } : { delay: .05 }));
        }
      });
    }
    var fontsReady = (document.fonts && document.fonts.ready) || Promise.resolve();
    Promise.race([fontsReady, new Promise(function (r) { setTimeout(r, 1500); })]).then(function () {
      if (h1) revealLines(h1);
      ready();
      intro.play(0);
    });

    /* ---------- on scroll ---------- */
    $$('main h2').forEach(function (h) {
      if (h.closest('.rings-copy')) return;
      revealLines(h, { trigger: h, start: 'top 88%', once: true });
    });

    var rise = $$('.split-copy > *:not(h2), .features li, .steps li, .tile, .fee, .card-plain, .roles li, .ticks li, .note, .fee-grid + *, .news.rich li, .video-grid > div:first-child > *, .visit-copy > *, .cta-inner > *, .statement .btn-row, .head > p, .contact-grid > *, .post-body > *, .gallery img, .apply-side, .chips');
    gsap.set(rise, { opacity: 0, y: 26 });
    ScrollTrigger.batch(rise, { start: 'top 90%', once: true, onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: .9, stagger: .08, overwrite: true }); } });

    $$('.split-photo, .video, .map, .post-cover').forEach(function (el) {
      gsap.set(el, { opacity: 1, clipPath: 'circle(0% at 50% 50%)' });
      gsap.to(el, { clipPath: 'circle(75% at 50% 50%)', duration: 1.5, ease: 'power2.inOut', scrollTrigger: { trigger: el, start: 'top 88%', once: true }, onComplete: function () { gsap.set(el, { clearProps: 'clipPath' }); } });
    });
    $$('.life-img').forEach(function (el, i) {
      gsap.set(el, { opacity: 1, clipPath: 'circle(0% at 50% 50%)' });
      gsap.to(el, { clipPath: 'circle(50% at 50% 50%)', duration: 1.4, delay: i * .12, ease: 'power2.inOut', scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
    });
    $$('.path .ring').forEach(function (r, i) {
      gsap.from(r, { scale: .4, opacity: 0, duration: 1, delay: i * .1, scrollTrigger: { trigger: r, start: 'top 92%', once: true } });
    });

    $$('[data-count]').forEach(function (el) {
      var to = parseFloat(el.getAttribute('data-count')), o = { v: 0 };
      el.textContent = '0';
      gsap.to(o, { v: to, duration: 1.6, ease: 'power2.out', onUpdate: function () { el.textContent = Math.round(o.v); },
        scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
    });

    /* ---------- the trunk section: no scroll tricks. Point at or focus a phase and its ring lights up and the photo changes. ---------- */
    var R = $('.rings');
    if (R) {
      var items = $$('.rings-list li', R), rs = $$('.rs-ring', R), imgs = $$('.rs-img', R);
      var show = function (i) {
        items.forEach(function (li, k) { li.classList.toggle('on', k === i); });
        rs.forEach(function (r, k) { r.classList.toggle('on', k === i); });
        imgs.forEach(function (im, k) { gsap.to(im, { opacity: k === i ? 1 : 0, duration: .7, overwrite: 'auto' }); });
      };
      items.forEach(function (li, i) {
        li.addEventListener('mouseenter', function () { show(i); });
        li.addEventListener('focusin', function () { show(i); });
      });
      show(0);
      gsap.set(rs, { strokeDasharray: 1, strokeDashoffset: 1 });
      gsap.to(rs, { strokeDashoffset: 0, duration: 1.8, stagger: .15, ease: 'power2.inOut', scrollTrigger: { trigger: R, start: 'top 70%', once: true } });
      gsap.to($('.rings-stage svg', R), { scale: 1.012, duration: 7, yoyo: true, repeat: -1, ease: 'sine.inOut', transformOrigin: '50% 50%' });
    }

    addEventListener('load', function () { ScrollTrigger.refresh(); });
  }
})();
