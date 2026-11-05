/* Mellow Oaks concept: "Search or ask" panel. Instant page search from site-index.json,
   plus the Ask Mellow Oaks assistant (/api/ask, Cloudflare Workers AI) that only answers from this site. */
(function () {
  var btns = document.querySelectorAll('.ask-btn');
  if (!btns.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pages = null, history = [], busy = false, lastFocus = null;
  var SUGGEST = ['How do I apply for 2027?', 'Where can I see the school fees?', 'When is Open Day?', 'Which sports can learners play?'];

  var box = document.createElement('div');
  box.className = 'ask';
  box.id = 'ask';
  box.hidden = true;
  box.innerHTML =
    '<div class="ask-scrim" data-close></div>' +
    '<div class="ask-panel" role="dialog" aria-modal="true" aria-labelledby="ask-title">' +
      '<div class="ask-top">' +
        '<h2 id="ask-title">Search or ask</h2>' +
        '<button class="ask-x" type="button" data-close aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>' +
      '</div>' +
      '<form class="ask-form" autocomplete="off">' +
        '<label class="sr" for="ask-q">Search the website or ask a question</label>' +
        '<svg class="ask-glass" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
        '<input id="ask-q" type="search" maxlength="400" placeholder="Search or ask a question" enterkeyhint="send">' +
        '<button class="btn btn-leaf ask-go" type="submit">Ask</button>' +
      '</form>' +
      '<div class="ask-body" aria-live="polite">' +
        '<div class="ask-chips"></div>' +
        '<ol class="ask-pages" aria-label="Matching pages"></ol>' +
        '<div class="ask-chat"></div>' +
      '</div>' +
      '<p class="ask-foot">Ask Mellow Oaks only answers from this website. For anything important, call the office on <a href="tel:+27119585176">011 958 5176</a>.</p>' +
    '</div>';
  document.body.appendChild(box);

  var input = box.querySelector('#ask-q'), form = box.querySelector('.ask-form');
  var list = box.querySelector('.ask-pages'), chat = box.querySelector('.ask-chat'), chips = box.querySelector('.ask-chips');

  SUGGEST.forEach(function (s) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'ask-chip'; b.textContent = s;
    b.addEventListener('click', function () { input.value = s; send(); });
    chips.appendChild(b);
  });

  function loadPages() {
    if (pages) return Promise.resolve(pages);
    return fetch('/site-index.json').then(function (r) { return r.json(); }).then(function (d) { pages = d; return d; }).catch(function () { pages = []; return pages; });
  }
  function norm(s) { return (s || '').toLowerCase().normalize('NFKD').replace(/[^a-z0-9 ]+/g, ' '); }
  function findPages(q) {
    var ws = norm(q).split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!ws.length || !pages) return [];
    return pages.map(function (p) {
      var t = norm(p.t), d = norm(p.d + ' ' + p.h.join(' ')), s = 0;
      ws.forEach(function (w) {
        var stem = w.replace(/(ings|ing|ies|es|s)$/, '');
        if (t.indexOf(stem) > -1) s += 5;
        if (d.indexOf(stem) > -1) s += 1.5;
      });
      if (p.news) s *= 0.6;
      return { p: p, s: s };
    }).filter(function (r) { return r.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 5);
  }
  function showPages(q) {
    list.innerHTML = '';
    findPages(q).forEach(function (r) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = r.p.u;
      a.innerHTML = '<b></b><span></span>';
      a.querySelector('b').textContent = r.p.t;
      a.querySelector('span').textContent = r.p.d;
      li.appendChild(a); list.appendChild(li);
    });
  }
  input.addEventListener('input', function () {
    var q = input.value.trim();
    chips.hidden = !!q || chat.children.length > 0;
    loadPages().then(function () { showPages(q); });
  });

  /* answers: plain text with [label](/path) links only */
  function render(el, text) {
    var re = /\[([^\]]+)\]\(([^)\s]+)\)/g, last = 0, m;
    text = text.replace(/\*\*([^*]+)\*\*/g, '$1');
    while ((m = re.exec(text))) {
      el.appendChild(document.createTextNode(text.slice(last, m.index)));
      var a = document.createElement('a'); a.href = m[2]; a.textContent = m[1];
      if (/^https?:/.test(m[2])) a.rel = 'noopener';
      el.appendChild(a); last = re.lastIndex;
    }
    el.appendChild(document.createTextNode(text.slice(last)));
  }
  function bubble(role, text) {
    var d = document.createElement('div');
    d.className = 'msg ' + role;
    if (text) render(d, text);
    chat.appendChild(d);
    if (!reduce) d.classList.add('pop');
    d.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
    return d;
  }
  function send() {
    var q = input.value.trim();
    if (!q || busy) return;
    busy = true; chips.hidden = true; list.innerHTML = '';
    bubble('me', q);
    input.value = '';
    var wait = bubble('bot typing', '');
    wait.innerHTML = '<span></span><span></span><span></span>';
    wait.setAttribute('aria-label', 'Looking that up');
    fetch('/api/ask', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ q: q, history: history }) })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        wait.remove();
        var text = d.answer || '';
        if (!text) {
          text = d.sources && d.sources.length
            ? 'The assistant is resting right now, but these pages should help:'
            : (d.error || 'The assistant is resting right now. Try searching for a word like “fees” or “apply”, or call the office on 011 958 5176.');
        }
        var b = bubble('bot', text);
        if (d.sources && d.sources.length) {
          var s = document.createElement('p'); s.className = 'msg-src';
          s.appendChild(document.createTextNode('From: '));
          d.sources.forEach(function (x, i) {
            if (i) s.appendChild(document.createTextNode(', '));
            var a = document.createElement('a'); a.href = x.url; a.textContent = x.title; s.appendChild(a);
          });
          b.appendChild(s);
        }
        if (d.answer) { history.push({ role: 'user', content: q }, { role: 'assistant', content: d.answer }); history = history.slice(-6); }
      })
      .catch(function () {
        wait.remove();
        bubble('bot', 'I couldn’t reach the assistant. Check your connection, or call the office on 011 958 5176.');
      })
      .then(function () { busy = false; input.focus(); });
  }
  form.addEventListener('submit', function (e) { e.preventDefault(); send(); });

  function open() {
    lastFocus = document.activeElement;
    box.hidden = false;
    document.documentElement.classList.add('ask-open');
    btns.forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    requestAnimationFrame(function () { box.classList.add('on'); });
    loadPages();
    setTimeout(function () { input.focus(); }, reduce ? 0 : 60);
  }
  function close() {
    box.classList.remove('on');
    document.documentElement.classList.remove('ask-open');
    btns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    setTimeout(function () { box.hidden = true; }, reduce ? 0 : 260);
    if (lastFocus) lastFocus.focus();
  }
  btns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); b.addEventListener('click', open); });
  box.addEventListener('click', function (e) { if (e.target.closest('[data-close]')) close(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !box.hidden) { e.stopPropagation(); close(); }
    if (e.key === '/' && box.hidden && !/input|textarea|select/i.test((document.activeElement || {}).tagName || '')) { e.preventDefault(); open(); }
    if (e.key === 'Tab' && !box.hidden) {
      var f = box.querySelectorAll('button:not([hidden]), input, a[href]'), first = f[0], lastEl = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastEl.focus(); }
      else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); first.focus(); }
    }
  }, true);
})();
