/* Mellow Oaks concept: calm layer. Number counters and a quiet scroll indicator. No dependencies. */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
  function run(el) {
    var to = parseFloat(el.getAttribute('data-count')), t0 = null;
    if (reduce || isNaN(to)) { el.textContent = to; return; }
    (function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min((t - t0) / 1400, 1);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  if (!reduce && 'IntersectionObserver' in window) {
    counters.forEach(function (c) { c.textContent = '0'; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); io.unobserve(e.target); } });
    }, { threshold: .4 });
    counters.forEach(function (c) { io.observe(c); });
  }
})();
