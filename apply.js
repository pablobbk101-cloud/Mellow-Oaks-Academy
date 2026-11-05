/* Mellow Oaks concept: five-step online application (demo: nothing is stored or sent). */
(function () {
  var form = document.getElementById('apply');
  if (!form) return;
  document.body.classList.add('apply-page');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var steps = Array.prototype.slice.call(form.querySelectorAll('.step'));
  var prog = Array.prototype.slice.call(document.querySelectorAll('.progress li'));
  var back = document.getElementById('back'), next = document.getElementById('next');
  var cur = 0;
  var $ = function (id) { return document.getElementById(id); };

  var rules = {
    'l-grade': [function (v) { return !!v; }, 'Choose a grade.'],
    'l-year': [function (v) { return !!v; }, 'Choose an intake year.'],
    'l-first': [function (v) { return v.trim().length > 1; }, 'Enter the learner\'s first names.'],
    'l-last': [function (v) { return v.trim().length > 1; }, 'Enter the learner\'s surname.'],
    'l-dob': [function (v) { return !!v && new Date(v) < new Date(); }, 'Enter a date of birth in the past.'],
    'p1-rel': [function (v) { return !!v; }, 'Choose a relationship.'],
    'p1-name': [function (v) { return v.trim().length > 1; }, 'Enter a full name.'],
    'p1-phone': [function (v) { return v.replace(/\D/g, '').length >= 9; }, 'Enter a mobile number with at least 9 digits.'],
    'p1-email': [function (v) { return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.trim()); }, 'Enter a valid email address.'],
    'a-street': [function (v) { return v.trim().length > 3; }, 'Enter the street address.'],
    'a-suburb': [function (v) { return v.trim().length > 1; }, 'Enter the suburb.'],
    'a-city': [function (v) { return v.trim().length > 1; }, 'Enter the city or town.'],
    'a-code': [function (v) { return /^\d{4}$/.test(v.trim()); }, 'Enter a 4-digit postal code.']
  };
  var p2on = false;
  var p2rules = {
    'p2-rel': [function (v) { return !!v; }, 'Choose a relationship, or remove this person.'],
    'p2-name': [function (v) { return v.trim().length > 1; }, 'Enter a full name.'],
    'p2-phone': [function (v) { return !v || v.replace(/\D/g, '').length >= 9; }, 'Enter a mobile number with at least 9 digits.'],
    'p2-email': [function (v) { return !v || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.trim()); }, 'Enter a valid email address.']
  };

  function check(id, rule) {
    var f = $(id); if (!f) return true;
    var ok = rule[0](f.value);
    f.setAttribute('aria-invalid', ok ? 'false' : 'true');
    var e = f.parentNode.querySelector('.err'); if (e) e.textContent = ok ? '' : rule[1];
    return ok;
  }
  function validate(i) {
    var ok = true, first = null;
    var all = Object.assign({}, rules, p2on ? p2rules : {});
    steps[i].querySelectorAll('input,select').forEach(function (f) {
      if (all[f.id] && !check(f.id, all[f.id])) { ok = false; if (!first) first = f; }
    });
    if (i === 3) steps[3].querySelectorAll('.upload').forEach(function (u) {
      var miss = u.getAttribute('data-required') === '1' && !u.querySelector('input').files.length;
      u.classList.toggle('missing', miss);
      if (miss) { ok = false; if (!first) first = u.querySelector('input'); }
    });
    if (i === 4) {
      var c = $('consent').checked;
      $('consent-err').textContent = c ? '' : 'Tick the box to confirm and consent.';
      if (!c) { ok = false; first = $('consent'); }
    }
    if (first) first.focus();
    return ok;
  }
  /* clear an error as soon as it is fixed */
  form.addEventListener('input', function (e) {
    var r = rules[e.target.id] || (p2on && p2rules[e.target.id]);
    if (r && e.target.getAttribute('aria-invalid') === 'true') check(e.target.id, r);
  });

  /* second parent */
  var add = form.querySelector('.add-parent'), p2 = form.querySelector('[data-parent="2"]');
  add.addEventListener('click', function () {
    p2on = !p2on;
    p2.hidden = !p2on;
    add.textContent = p2on ? 'Remove the second parent or guardian' : '+ Add a second parent or guardian';
    if (p2on) { if (!reduce) { p2.classList.remove('reveal'); void p2.offsetWidth; p2.classList.add('reveal'); } $('p2-rel').focus(); }
  });

  /* uploads: show the chosen file name (files stay in the browser in this preview) */
  form.querySelectorAll('.upload input').forEach(function (inp) {
    inp.addEventListener('change', function () {
      var li = inp.closest('.upload'), f = inp.files[0];
      li.classList.toggle('has-file', !!f);
      li.classList.remove('missing');
      li.querySelector('.u-state').textContent = f ? (f.name.length > 22 ? f.name.slice(0, 19) + '…' : f.name) : 'Choose file';
    });
  });

  function val(id) { var f = $(id); return f ? (f.value || '').trim() : ''; }
  function review() {
    var files = Array.prototype.slice.call(form.querySelectorAll('.upload')).filter(function (u) { return u.querySelector('input').files.length; })
      .map(function (u) { return u.querySelector('b').textContent; });
    var rows = [
      ['Learner', val('l-first') + ' ' + val('l-last')],
      ['Grade', val('l-grade') + ', ' + val('l-year')],
      ['Date of birth', val('l-dob')],
      ['Parent or guardian', val('p1-name') + ' (' + val('p1-rel') + '), ' + val('p1-phone')],
      ['Email', val('p1-email')]
    ];
    if (p2on) rows.push(['Second parent or guardian', val('p2-name') + ' (' + val('p2-rel') + ')']);
    rows.push(['Address', [val('a-street'), val('a-suburb'), val('a-city'), val('a-prov'), val('a-code')].filter(Boolean).join(', ')]);
    rows.push(['Documents', files.length ? files.join(', ') : 'None yet']);
    var dl = $('review'); dl.innerHTML = '';
    rows.forEach(function (r) {
      var dt = document.createElement('dt'), dd = document.createElement('dd');
      dt.textContent = r[0]; dd.textContent = r[1]; dl.appendChild(dt); dl.appendChild(dd);
    });
  }

  function show(i) {
    var dir = i < cur ? 'in-back' : 'in';
    cur = i;
    steps.forEach(function (s, j) { s.hidden = j !== i; s.classList.remove('in', 'in-back'); });
    if (!reduce) { void steps[i].offsetWidth; steps[i].classList.add(dir); }
    prog.forEach(function (p, j) { p.classList.toggle('on', j === i); p.classList.toggle('done', j < i); if (j === i) p.setAttribute('aria-current', 'step'); else p.removeAttribute('aria-current'); });
    back.hidden = i === 0;
    next.textContent = i === steps.length - 1 ? 'Submit application' : 'Continue';
    if (i === 4) review();
    var h = steps[i].querySelector('h2'); h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true });
    var top = form.getBoundingClientRect().top + scrollY - 110;
    if (scrollY > top) scrollTo({ top: top, behavior: reduce ? 'auto' : 'smooth' });
  }
  next.addEventListener('click', function () {
    if (!validate(cur)) return;
    if (cur < steps.length - 1) { show(cur + 1); return; }
    steps.forEach(function (s) { s.hidden = true; });
    form.querySelector('.actions').hidden = true;
    prog.forEach(function (p) { p.classList.remove('on'); p.classList.add('done'); });
    var d = $('done'); d.hidden = false; d.focus();
  });
  back.addEventListener('click', function () { if (cur > 0) show(cur - 1); });
  show(0);
})();
