#!/usr/bin/env python3
"""Builds the Mellow Oaks Academy concept site.  Run: python3 tools/build.py
All school text, photos, logo and documents come from mellowoaksacademy.co.za (read 5 November 2026)."""
import hashlib, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = ("styles.css", "site.js", "apply.js", "ask.js")
VER = {a: hashlib.sha1(open(os.path.join(ROOT, a), "rb").read()).hexdigest()[:8] for a in ASSETS}
esc = lambda s: html.escape(str(s), quote=True)

UP = "https://mellowoaksacademy.co.za/wp-content/uploads/"
IMG = {  # key: (file, width, height, alt)
    "logo": ("2025/10/MellowOaksAcademy_logo2025.png", 230, 229, "Mellow Oaks Academy logo"),
    "grounds": ("2025/10/Mellow-Oaks-Academy.jpg", 1360, 1020, "A garden path under tall trees on the Mellow Oaks campus"),
    "green": ("2025/09/green_school.jpg", 1200, 800, "Green gardens and trees around the school buildings"),
    "grass": ("2025/10/Primary_MellowOaks_grass-1.jpg", 1360, 1020, "Two primary school learners sitting on the grass"),
    "lab": ("2025/10/Highschool_ScienceLab.jpg", 1360, 1020, "A high school learner in a lab coat in the science lab"),
    "science": ("2025/09/DSC_2571.jpg", 1360, 1020, "High school learners doing a science experiment"),
    "building": ("2025/09/DSC_2277.jpg", 1360, 1020, "A school building surrounded by trees"),
    "computers": ("2025/09/DSC_2583.jpg", 1360, 1020, "Learners working at computers"),
    "sport": ("2025/09/DSC_2489.jpg", 1360, 1020, "A learner playing a bat-and-ball game outdoors"),
    "class": ("2025/10/Academics.jpg", 1360, 1020, "High school learners working in class"),
    "support": ("2025/10/DSC_2582.jpg", 1360, 1020, "A learner working at a computer"),
    "soccer": ("2025/10/Soccerball.jpg", 1360, 1020, "A soccer ball on green grass"),
    "outdoor": ("2025/10/Outdoor_learning.jpg", 1360, 1020, "A classroom building with a flower garden in front"),
    "principal": ("2026/08/PrincipalPoley.jpg", 780, 470, "Principal Mr Quinten Poley at his desk"),
    "classroom": ("2026/04/classroom.jpg", 1360, 1020, "An empty, bright classroom"),
}
FEES_2026 = UP + "2026/08/SchoolFees2026.pdf"
FEES_2027 = UP + "2026/08/School-Fees-2027.pdf"
VIDEO = "w70MQ__F_-o"
OLD = "https://mellowoaksacademy.co.za/"
PHONE, PHONE_TEL = "011 958 5176", "+27119585176"
WA, WA_URL = "076 791 2582", "https://wa.me/27767912582"
EMAIL_INFO, EMAIL_RECEPTION = "info@mellowoaksacademy.co.za", "reception@mellowoaksacademy.co.za"
ADDRESS = "23 Van Brakel Crescent, Willowbrook, Roodepoort"
MAP_Q = "Mellow+Oaks+Academy+Roodepoort"
HOURS = "Monday to Friday, 09:00 to 13:00 (closed on public holidays)"
PABLO = "Pablo Lebelo, mrpoint.online, 060 452 1037"

PHASES = [  # slug, name, grades, page
    ("pre-primary", "Pre-Primary", "18 months to Grade RR", "pre-primary.html"),
    ("foundation", "Foundation Phase", "Grades R to 3", "primary-school.html"),
    ("intermediate", "Intermediate Phase", "Grades 4 to 6", "primary-school.html"),
    ("senior", "Senior Phase", "Grades 7 to 9", "high-school.html"),
    ("fet", "FET Phase", "Grades 10 to 12", "high-school.html"),
]

NAV = [
    ("About", "about.html", [("Our school", "about.html"), ("Our principal", "principal.html"), ("Careers", "careers.html")]),
    ("Academics", "academics.html", [("Overview", "academics.html"), ("Pre-Primary", "pre-primary.html"),
                                     ("Primary School", "primary-school.html"), ("High School", "high-school.html"),
                                     ("Academic Support", "academic-support.html")]),
    ("School life", "school-life.html", [("Campus life", "school-life.html"), ("Sports and clubs", "sports-and-clubs.html"),
                                         ("News", "news.html")]),
    ("Admissions", "admissions.html", [("How to apply", "admissions.html"), ("School fees", "fees.html"),
                                       ("Apply online", "apply.html")]),
]


def img(key, cls="", lazy=True, eager_pri=False):
    f, w, h, alt = IMG[key]
    return '<img src="%s%s" width="%d" height="%d" alt="%s"%s%s>' % (
        UP, f, w, h, esc(alt), ' class="%s"' % cls if cls else "",
        ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if eager_pri else ""))


ICON = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.6a1 1 0 01-.25 1z" fill="currentColor"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1112 20a8 8 0 01-3.9-1L4 20z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
    "pen": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "chev": '<svg width="12" height="8" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "fee": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3zM9 8h6M9 12h6M9 16h3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16v14H4zM4 10h16M8 3v5M16 3v5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "news": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h13v14H6a2 2 0 01-2-2V5zM17 9h3v8a2 2 0 01-2 2M7 9h7M7 13h7M7 16h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15M5 19c3-4 6-7 10-9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
}


def header(active):
    items = []
    for label, href, subs in NAV:
        cur = active in [s[1] for s in subs]
        sub = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == active else "", esc(t)) for t, h in subs)
        sid = "sub-" + label.lower().replace(" ", "-")
        items.append(
            '<li class="has-sub%s"><a class="nav-link" href="%s">%s</a>'
            '<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="%s"><span class="sr">Show %s pages</span>%s</button>'
            '<ul class="sub" id="%s">%s</ul></li>' % (" is-current" if cur else "", href, esc(label), sid, esc(label), ICON["chev"], sid, sub))
    contact_cur = ' aria-current="page"' if active == "contact.html" else ""
    return """
<a class="skip" href="#main">Skip to content</a>
<div class="concept-bar" role="note">Concept preview of a new Mellow Oaks Academy website, not the live site. Designed by <a href="https://mrpoint.online">Pablo Lebelo, mrpoint.online</a></div>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="Mellow Oaks Academy, home">%s<span class="brand-text"><b>Mellow Oaks</b><small>Academy</small></span></a>
    <nav id="nav" aria-label="Main">
      <ul class="nav-list">%s<li><a class="nav-link" href="contact.html"%s>Contact</a></li></ul>
      <a class="btn btn-sun nav-cta" href="apply.html">Apply for 2027</a>
    </nav>
    <div class="bar-actions">
      <button class="ask-btn" type="button" aria-haspopup="dialog" aria-controls="ask"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span class="ask-label">Search or ask</span></button>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav"><span class="menu-lines" aria-hidden="true"></span><span class="menu-label">Menu</span></button>
    </div>
  </div>
</header>""" % (img("logo", "brand-logo", lazy=False), "".join(items), contact_cur)


def footer():
    cols = "".join('<div><h4>%s</h4><ul>%s</ul></div>' % (esc(l), "".join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for t, h in s)) for l, _h, s in NAV[1:])
    return """
<section class="visit" aria-labelledby="visit-h">
  <div class="wrap visit-grid">
    <div class="visit-copy">
      <p class="kicker">Every Friday is Open Day</p>
      <h2 id="visit-h">Come and see the campus</h2>
      <p>Walk the gardens, see the classrooms and meet the team. Call or WhatsApp to arrange a tour.</p>
      <dl class="visit-list">
        <dt>Address</dt><dd>%s</dd>
        <dt>Phone</dt><dd><a href="tel:%s">%s</a></dd>
        <dt>WhatsApp</dt><dd><a href="%s" rel="noopener">%s</a></dd>
        <dt>Email</dt><dd><a href="mailto:%s">%s</a></dd>
        <dt>Office hours</dt><dd>%s</dd>
      </dl>
      <div class="btn-row"><a class="btn btn-sun" href="contact.html#tour">Book a tour</a><a class="btn btn-ghost-light" href="https://www.google.com/maps/search/?api=1&amp;query=%s" rel="noopener">Directions</a></div>
    </div>
    <iframe class="map" title="Map showing Mellow Oaks Academy" src="https://www.google.com/maps?q=%s&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">%s<p>A CAPS school in Roodepoort, from 18 months to Grade 12, with small classes and Christian values.</p></div>
      %s
      <div><h4>The school</h4><ul><li><a href="about.html">Our school</a></li><li><a href="principal.html">Our principal</a></li><li><a href="careers.html">Careers</a></li><li><a href="contact.html">Contact</a></li><li><a href="%sprivacypolicy/" rel="noopener">Privacy policy</a></li><li><a href="%spaia-manual/" rel="noopener">PAIA manual</a></li></ul></div>
    </div>
    <div class="legal"><p>Concept website by %s. Not the official website of Mellow Oaks Academy.</p><p>Text, photos, logo and documents are from the school's current website.</p></div>
  </div>
</footer>
<nav class="dock" aria-label="Quick actions">
  <a href="tel:%s">%sCall</a><a href="%s" rel="noopener">%sWhatsApp</a><a class="dock-main" href="apply.html">%sApply now</a>
</nav>""" % (esc(ADDRESS), PHONE_TEL, PHONE, WA_URL, WA, EMAIL_INFO, EMAIL_INFO, esc(HOURS), MAP_Q, MAP_Q,
             img("logo", "foot-logo"), cols, OLD, OLD, esc(PABLO), PHONE_TEL, ICON["phone"], WA_URL, ICON["chat"], ICON["pen"])


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Figtree:wght@400;500;600;700&display=swap">')
FAV = UP + "2025/09/MellowOaksAcademy_logosm-3.png"


def page(fn, title, desc, body, scripts=("site.js", "ask.js"), nav=None):
    doc = """<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s | Mellow Oaks Academy (concept)</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0c3b24">
<link rel="icon" href="%s">
%s
<link rel="stylesheet" href="styles.css?v=%s">
<script>["pageswap","pagereveal"].forEach(function(n){addEventListener(n,function(e){var v=e.viewTransition;if(v)["ready","finished","updateCallbackDone"].forEach(function(k){v[k]&&v[k].catch&&v[k].catch(function(){})})})});</script>
</head>
<body>%s
<main id="main">%s
</main>%s
%s
</body>
</html>
""" % (esc(title), esc(desc), FAV, FONTS, VER["styles.css"], header(nav or fn), body, footer(),
       "\n".join('<script src="%s?v=%s" defer></script>' % (s, VER[s]) for s in scripts))
    doc = re.sub(r'href="index\.html', 'href="./', doc)
    doc = re.sub(r'href="([a-z0-9-]+)\.html', r'href="\1', doc)
    open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(doc)


def hero_inner(kicker, h1, lede, key, crumbs=None, cta=True):
    cr = ""
    if crumbs:
        cr = '<p class="crumbs">' + " / ".join('<a href="%s">%s</a>' % (h, esc(t)) for t, h in crumbs) + ' / <span aria-current="page">%s</span></p>' % esc(h1)
    return """
<section class="page-hero">
  <div class="wrap page-hero-grid">
    <div class="ph-copy">%s<p class="kicker">%s</p><h1>%s</h1><p class="lede">%s</p>%s</div>
    <div class="ph-photo">%s</div>
  </div>
</section>""" % (cr, esc(kicker), esc(h1), esc(lede),
                 '<div class="btn-row"><a class="btn btn-leaf" href="apply.html">Apply online</a><a class="btn btn-line" href="contact.html#tour">Book a tour</a></div>' if cta else "",
                 img(key, lazy=False, eager_pri=True))


def prose(*paras):
    return "".join("<p>%s</p>" % esc(p) for p in paras)


def features(items):
    return '<ul class="features">%s</ul>' % "".join('<li><span class="f-ico" aria-hidden="true">%s</span><div><h3>%s</h3><p>%s</p></div></li>' % (ICON["leaf"], esc(t), esc(d)) for t, d in items)


def split(key, h2, body, flip=False):
    return '<section class="section"><div class="wrap split%s"><div class="split-photo">%s</div><div class="split-copy"><h2>%s</h2>%s</div></div></section>' % (" flip" if flip else "", img(key), esc(h2), body)


def cta_band(h2="2027 registrations are open", p="Limited spaces are available. Secure your child's place today."):
    return '<section class="cta"><div class="wrap cta-inner"><div><h2>%s</h2><p>%s</p></div><div class="btn-row"><a class="btn btn-sun" href="apply.html">Apply online</a><a class="btn btn-ghost-light" href="contact.html#tour">Book a tour</a></div></div></section>' % (esc(h2), esc(p))


def phase_path(current=None):
    nodes = []
    for i, (slug, name, grades, href) in enumerate(PHASES):
        on = ' aria-current="true"' if current and current in href else ""
        nodes.append('<li class="node"%s><a href="%s"><span class="ring" aria-hidden="true"><span>%d</span></span><span class="n-name">%s</span><span class="n-grades">%s</span></a></li>' % (on, href, i + 1, esc(name), esc(grades)))
    return '<ol class="path" aria-label="School phases from 18 months to Grade 12">%s</ol>' % "".join(nodes)


# ------------------------------------------------------------------ pages
def build_home():
    body = """
<section class="hero hero-home">
  <div class="hero-media">%s<div class="hero-shade"></div></div>
  <div class="wrap hero-inner">
    <p class="pill"><span class="dot" aria-hidden="true"></span>2027 registrations now open</p>
    <h1>Where curiosity blooms and every learner is nurtured to thrive</h1>
    <p class="lede">A CAPS school in Roodepoort, from 18 months to Grade 12, set among gardens and oak trees.</p>
    <div class="btn-row"><a class="btn btn-sun" href="apply.html">Apply for 2027</a><a class="btn btn-ghost-light" href="contact.html#tour">Book a tour</a></div>
    <ul class="facts">
      <li><b>20</b><span>learners per class, at most</span></li>
      <li><b>CAPS</b><span>curriculum with inquiry-based learning</span></li>
      <li><b>Fridays</b><span>are Open Day</span></li>
    </ul>
  </div>
</section>
%s
<section class="section news-top">
  <div class="wrap">
    <div class="head row"><h2>Latest news</h2><a class="text-link" href="news.html">All news</a></div>
    %s
  </div>
</section>
<section class="section tint">
  <div class="wrap">
    <div class="head"><p class="kicker">From first steps to matric</p><h2>One school for every stage</h2><p>Tap a phase to see what learners do there.</p></div>
    %s
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="head"><h2>Life at Mellow Oaks</h2></div>
    <div class="ptiles">
      <a class="ptile" href="academics.html">%s<span class="pt-cap"><b>Academics</b><small>CAPS with creative, inquiry-based learning</small></span></a>
      <a class="ptile" href="sports-and-clubs.html">%s<span class="pt-cap"><b>Sports and clubs</b><small>Soccer, netball, athletics, dance, chess and drama</small></span></a>
      <a class="ptile" href="school-life.html">%s<span class="pt-cap"><b>Campus life</b><small>Outdoor classrooms, gardens and leafy courtyards</small></span></a>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap video-grid">
    <div><p class="kicker">School tour</p><h2>Discover the spirit of Mellow Oaks</h2><p>From joyful classrooms and vibrant sports fields to the lush natural surroundings that inspire every learner. Watch the school tour video.</p><a class="btn btn-line" href="contact.html#tour">Book a tour in person</a></div>
    <div class="video"><button class="video-btn" type="button" data-video="%s" aria-label="Play the school tour video">%s<span class="play" aria-hidden="true"></span></button></div>
  </div>
</section>
%s""" % (img("grounds", lazy=False, eager_pri=True), quick_bar(), news_list(3), phase_path(), img("class"), img("sport"), img("outdoor"),
                   VIDEO, img("green"), cta_band())
    page("index.html", "A CAPS school in Roodepoort, 18 months to Grade 12",
         "Concept website for Mellow Oaks Academy in Roodepoort: pre-primary, primary and high school with small classes, CAPS curriculum and Christian values.", body)


# ------------------------------------------------------------------ news: the school's real blog posts (tools/posts.json, from its WordPress API)
from html.parser import HTMLParser
import html as _html, json as _json

MONTHS = "January February March April May June July August September October November December".split()


def nice_date(iso):
    y, m, d = iso[:10].split("-")
    return "%d %s %s" % (int(d), MONTHS[int(m) - 1], y)


class Clean(HTMLParser):
    KEEP = {"p", "h2", "h3", "h4", "ul", "ol", "li", "strong", "b", "em", "i", "a", "br", "figure", "figcaption", "blockquote"}

    def __init__(self, slugs):
        super().__init__(convert_charrefs=True); self.out = []; self.slugs = slugs; self.imgs = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img" and a.get("src"):
            self.imgs += 1
            w, h = a.get("width", ""), a.get("height", "")
            self.out.append('<img src="%s" alt="%s"%s loading="lazy" decoding="async">' % (
                esc(a["src"]), esc(a.get("alt") or ""), (' width="%s" height="%s"' % (w, h)) if w.isdigit() and h.isdigit() else ""))
        elif tag == "a":
            href = a.get("href", "")
            m = re.match(r"https?://(www\.)?mellowoaksacademy\.co\.za/([a-z0-9-]+)/?$", href)
            if m and m.group(2) in self.slugs:
                self.out.append('<a href="news-%s.html">' % m.group(2))
            elif href:
                self.out.append('<a href="%s" rel="noopener">' % esc(href))
            else:
                self.out.append("<a>")
        elif tag in self.KEEP:
            self.out.append("<%s>" % ("br" if tag == "br" else tag))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in self.KEEP and tag != "br":
            self.out.append("</%s>" % tag)

    def handle_data(self, data):
        self.out.append(esc(data))


def clean_html(raw, slugs):
    c = Clean(slugs); c.feed(raw)
    h = "".join(c.out)
    for _ in range(3):
        h = re.sub(r"<(p|h2|h3|h4|li|strong|em|b|i|figcaption)>\s*</\1>", "", h)
    h = re.sub(r"<figure>\s*</figure>", "", h)
    return h.strip(), c.imgs


def text_of(raw):
    return _html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))).strip()


def load_posts():
    raw = _json.load(open(os.path.join(ROOT, "tools", "posts.json"), encoding="utf-8"))
    slugs = {p["slug"] for p in raw}
    posts = []
    for p in raw:
        title = text_of(p["title"]["rendered"]).replace("Mellow Oaks Academy School Concert", "School Concert")
        body, nimg = clean_html(p["content"]["rendered"], slugs)
        media = (p.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
        sizes = media.get("media_details", {}).get("sizes", {})
        pick = lambda *ks: next((sizes[k]["source_url"] for k in ks if k in sizes), media.get("source_url", ""))
        exc = text_of(p["excerpt"]["rendered"]).replace(" [&hellip;]", "").replace(" […]", "")
        if len(exc) > 150:
            exc = exc[:147].rsplit(" ", 1)[0] + "…"
        kind = "Newsletter" if p["slug"].startswith("newsletter") else (
            "Sport" if re.search(r"netball|vs-|sport", p["slug"]) else (
            "Academics" if re.search(r"science|dissection|grade", p["slug"]) else "School news"))
        posts.append(dict(slug=p["slug"], title=title, date=p["date"][:10], kind=kind, body=body, words=len(text_of(p["content"]["rendered"]).split()),
                          thumb=pick("medium_large", "large", "medium"), big=pick("large", "full", "medium_large"),
                          alt=media.get("alt_text") or title, excerpt=exc))
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


POSTS = load_posts()


def news_list(n=None, rich=False, skip=None):
    items = [p for p in POSTS if p["slug"] != skip][:n] if n else POSTS
    return '<ul class="news rich">%s</ul>' % "".join(
        '<li><a href="news-%s.html"><span class="n-img"><img src="%s" alt="%s" loading="lazy" decoding="async"></span><span class="n-body"><span class="n-meta"><span class="tag">%s</span><time datetime="%s">%s</time></span><span class="n-title">%s</span><span class="n-sum">%s</span><span class="n-go">Read more</span></span></a></li>'
        % (p["slug"], esc(p["thumb"]), esc(p["alt"]), esc(p["kind"]), p["date"], nice_date(p["date"]), esc(p["title"]), esc(p["excerpt"])) for p in items)


def build_posts():
    for p in POSTS:
        note = ""
        body = """
<article class="post">
  <header class="post-head wrap narrow">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="news.html">News</a></p>
    <p class="n-meta"><span class="tag">%s</span><time datetime="%s">%s</time></p>
    <h1>%s</h1>
  </header>
  <div class="wrap post-wrap">
    <figure class="post-cover"><img src="%s" alt="%s" fetchpriority="high"></figure>
    <div class="post-body narrow">%s%s</div>
  </div>
</article>
<section class="section tint">
  <div class="wrap">
    <div class="head row"><h2>More news</h2><a class="text-link" href="news.html">All news</a></div>
    %s
  </div>
</section>%s""" % (esc(p["kind"]), p["date"], nice_date(p["date"]), esc(p["title"]), esc(p["big"]), esc(p["alt"]),
                   note, p["body"], news_list(3, skip=p["slug"]), cta_band())
        page("news-%s.html" % p["slug"], p["title"], (p["excerpt"] or p["title"])[:155], body, nav="news.html")


QUICK = [("fees.html", "fee", "School fees", "2026 and 2027 fees"),
         ("apply.html", "pen", "Apply online", "Five quick steps"),
         ("contact.html#tour", "cal", "Book a tour", "Fridays are Open Day"),
         ("news.html", "news", "School news", "Newsletters and events")]


def quick_bar():
    return '<nav class="quick" aria-label="Quick links"><div class="wrap"><ul>%s</ul></div></nav>' % "".join(
        '<li><a href="%s"><span class="q-ico">%s</span><span class="q-txt"><b>%s</b><small>%s</small></span></a></li>' % (h, ICON[i], esc(a), esc(b)) for h, i, a, b in QUICK)


def build_about():
    body = hero_inner("Our school", "Our school", "Nestled in the heart of Roodepoort, Mellow Oaks Academy's grounds reflect its commitment to holistic education and natural beauty.", "grounds", [("Home", "index.html")]) + \
        split("green", "A place to grow", prose(
            "At Mellow Oaks Academy, we believe that education is the foundation for a fulfilling and successful life. Our curriculum is thoughtfully crafted to be comprehensive, dynamic and learner-centred, empowering learners to thrive academically, socially and personally.",
            "Our commitment extends beyond academics. We foster a safe and supportive environment where learners feel valued and motivated to reach their full potential.")) + \
        '<section class="section tint"><div class="wrap"><div class="head"><h2>What we believe</h2></div>%s</div></section>' % features([
            ("Every learner matters", "Small class sizes, capped at just 20 learners, so educators give focused attention and tailored support."),
            ("Christian values", "Our programme is rooted in Christian principles, promoting integrity, compassion and a strong sense of community."),
            ("Character development", "Through values-based education, learners learn respect, resilience and responsibility."),
            ("Learning in nature", "Gardens, outdoor classrooms and courtyards that foster a deep appreciation for the environment.")]) + cta_band()
    page("about.html", "Our school", "About Mellow Oaks Academy: small classes, Christian values and a green campus in Roodepoort.", body)


def build_principal():
    body = hero_inner("Leadership", "Our principal", "Mellow Oaks Academy recently welcomed Mr Quinten Poley as its principal.", "principal", [("Home", "index.html"), ("About", "about.html")], cta=False) + \
        split("classroom", "Working with every family", prose(
            "Our principal collaborates closely with teachers and parents to design personalised interventions and provide targeted resources, so that each learner receives the support they need to thrive.",
            "To meet the principal or ask about your child's needs, book a visit through the school office.")
              + '<div class="btn-row"><a class="btn btn-leaf" href="contact.html#tour">Book a visit</a><a class="btn btn-line" href="news-welcoming-our-new-principal-mr-quinten-poley.html">Read the welcome post</a></div>') + cta_band()
    page("principal.html", "Our principal", "Meet Mr Quinten Poley, principal of Mellow Oaks Academy.", body)


def build_careers():
    roles = [("Business Studies and Economics", "Grades 10 to 12 (FET)"), ("EMS", "Grades 8 to 9 (Senior Phase)"), ("Maths Literacy", "Grades 10 and 12 (FET)"),
             ("Social Sciences", "Grades 8 to 9 (Senior Phase)"), ("History", "Grade 10 (FET)"), ("Tourism", "Grade 10 (FET)")]
    rows = "".join('<li><b>%s</b><span>%s</span></li>' % (esc(a), esc(b)) for a, b in roles)
    body = hero_inner("Careers", "Teach at Mellow Oaks", "If you're ready to inspire young learners and make a meaningful impact, we'd love to hear from you.", "classroom", [("Home", "index.html"), ("About", "about.html")], cta=False) + \
        '<section class="section"><div class="wrap narrow"><h2>Positions listed</h2><ul class="roles">%s</ul><div class="note"><h3>How to apply</h3><p>A complete application includes your CV, certified documents, qualifications, SACE registration and ID. Send it to <a href="mailto:quinten@mellowoaksacademy.co.za">quinten@mellowoaksacademy.co.za</a>.</p></div></div></section>' % rows
    page("careers.html", "Careers", "Teaching positions at Mellow Oaks Academy, Roodepoort.", body)


def build_academics():
    body = hero_inner("Academics", "A commitment to excellence", "We design our academic programme to challenge, inspire and nurture every learner, encouraging curiosity, resilience and a lifelong love of learning.", "class", [("Home", "index.html")]) + \
        '<section class="section"><div class="wrap"><div class="head"><h2>Choose a phase</h2></div>%s</div></section>' % phase_path() + \
        '<section class="section tint"><div class="wrap"><div class="head"><h2>Our academic philosophy</h2></div>%s</div></section>' % features([
            ("Individualised attention", "Classes are capped at just 20 learners, so every learner gets focused attention and meaningful engagement."),
            ("CAPS with inquiry", "A dynamic curriculum that blends the rigour of CAPS with creative, inquiry-based learning."),
            ("Literacy and numeracy", "A strong emphasis on foundational literacy and numeracy, backed by the Stimulus Maksima Reading Programme."),
            ("Christian values", "Learners build a moral foundation and live out their faith in their studies and everyday life.")]) + \
        split("science", "Growing with our learners", prose("Grade 11 launched in 2025, with Grade 12 to follow, extending our commitment to quality education and preparing learners for their final school years and future careers.")
              + '<a class="text-link" href="high-school.html">About High School</a>') + cta_band()
    page("academics.html", "Academics", "The Mellow Oaks Academy curriculum: CAPS, small classes and Christian values from pre-primary to Grade 12.", body)


def phase_page(fn, title, kicker, lede, key, phases_note, paras, key2, side_title):
    body = hero_inner(kicker, title, lede, key, [("Home", "index.html"), ("Academics", "academics.html")]) + \
        '<section class="section"><div class="wrap"><div class="head"><h2>%s</h2></div>%s</div></section>' % (esc(phases_note), phase_path(fn)) + \
        split(key2, side_title, prose(*paras)) + cta_band()
    page(fn, title, lede, body)


def build_phases():
    phase_page("pre-primary.html", "Pre-Primary", "18 months to Grade RR",
               "A warm, engaging space where young children explore, create and grow.", "grass", "Where it fits",
               ["Our play-based programme nurtures curiosity, builds foundational skills and inspires a lifelong love of learning.",
                "Classes are capped at 20 learners, so every child gets focused attention."], "green", "Learning through play")
    phase_page("primary-school.html", "Primary School", "Grades R to 7",
               "Core subjects, Maths, Science, English and Social Studies, blended with Art, PE and IT.", "grass", "Where it fits",
               ["We foster critical thinking, collaboration and a love for discovery, in a well-rounded and engaging learning experience.",
                "The Stimulus Maksima Reading Programme cultivates a love for reading across all grade levels."], "computers", "A well-rounded start")
    phase_page("high-school.html", "High School", "Grade 8 to matric",
               "A challenging, well-rounded curriculum that prepares learners for university and life beyond.", "lab", "Where it fits",
               ["Learners engage in advanced academics, extracurriculars and leadership development, within a supportive environment that fosters personal growth.",
                "Grade 11 launched in 2025, with Grade 12 to follow."], "science", "Ready for what comes next")


def build_support():
    items = [("Phonemic awareness", ""), ("Decoding", ""), ("Fluency", ""), ("Comprehension", ""), ("Vocabulary", "")]
    body = hero_inner("Academic support", "Academic Support", "Every learner is unique, with individual strengths and challenges.", "support", [("Home", "index.html"), ("Academics", "academics.html")]) + \
        split("classroom", "Learning support", prose(
            "Our principal collaborates closely with teachers and parents to design personalised interventions and provide targeted resources.",
            "Support includes small group sessions, individualised instruction, dedicated intervention classes and tailored learning materials.")) + \
        '<section class="section tint"><div class="wrap"><div class="head"><p class="kicker">Flagship programme</p><h2>Stimulus Maksima Reading Programme</h2><p>A structured, evidence-based approach to reading development that targets:</p></div><ul class="chips">%s</ul>%s</div></section>' % (
            "".join("<li>%s</li>" % esc(a) for a, _ in items), features([
                ("Individualised reading plans", "Each learner begins with an assessment, then follows a personalised plan."),
                ("Qualified reading specialists", "Led by certified reading specialists trained in the Stimulus Maksima methodology."),
                ("Small group sessions", "Focused attention, peer collaboration and immediate feedback.")])) + cta_band()
    page("academic-support.html", "Academic Support", "Learning support and the Stimulus Maksima Reading Programme at Mellow Oaks Academy.", body)


def build_school_life():
    body = hero_inner("School life", "Campus life", "Where learning goes beyond the classroom and every day is an opportunity to grow, connect and thrive.", "outdoor", [("Home", "index.html")]) + \
        '<section class="section"><div class="wrap"><div class="head"><h2>Nature, serenity and outdoor learning</h2><p>Among gently rolling hills and old oak trees, the campus is a sanctuary of natural beauty.</p></div>%s</div></section>' % features([
            ("Lush gardens", "Flower beds, indigenous plants and seasonal blooms create a peaceful, inspiring atmosphere."),
            ("Outdoor classrooms", "Shaded pergolas and garden nooks for reading, discussion and reflection."),
            ("Tranquil courtyards", "Benches under leafy canopies and the gentle sound of water features.")]) + \
        split("building", "The campus experience", "<ul class='ticks'><li><b>Morning assemblies</b> bring the school together to celebrate achievements and reflect on our values.</li><li><b>Interactive learning</b> integrates technology, group work and real-world applications.</li><li><b>Lunch and leisure</b>: nutritious meals and free time in courtyards, sports fields and creative corners.</li></ul>", flip=True) + \
        '<section class="section tint"><div class="wrap gallery">%s%s%s%s</div></section>' % (img("grounds"), img("science"), img("sport"), img("grass")) + cta_band()
    page("school-life.html", "Campus life", "Campus life at Mellow Oaks Academy: gardens, outdoor classrooms and courtyards in Roodepoort.", body)


def build_sports():
    body = hero_inner("School life", "Sports and clubs", "At Mellow Oaks, we don't just nurture minds, we ignite spirits.", "sport", [("Home", "index.html"), ("School life", "school-life.html")]) + \
        '<section class="section"><div class="wrap trio">%s</div></section>' % "".join(
            '<article class="tile"><h3>%s</h3><p>%s</p><ul class="chips small">%s</ul></article>' % (esc(t), esc(p), "".join("<li>%s</li>" % esc(c) for c in cs)) for t, p, cs in [
                ("Sports and PE", "Physical fitness, teamwork and personal growth, with structured coaching and friendly competition.", ["Soccer", "Netball", "Athletics", "Dance"]),
                ("Arts and culture", "Learners explore their talents and build confidence through creative expression.", ["Visual arts", "Drama", "Ballet"]),
                ("Clubs and enrichment", "Clubs that build leadership, collaboration and lifelong friendships.", ["Chess Club", "KFJ"])]) + \
        split("soccer", "More than physical activity", prose("Sports at Mellow Oaks are a celebration of teamwork, resilience and school spirit, fostering pride and camaraderie on and off the field.",
                                                             "The spacious grounds host community events like the First Kick Soccer clinic.")) + cta_band()
    page("sports-and-clubs.html", "Sports and clubs", "Sports, arts and clubs at Mellow Oaks Academy: soccer, netball, athletics, dance, drama, ballet and chess.", body)


def build_news():
    body = hero_inner("School life", "News", "Newsletters, events and updates from Mellow Oaks Academy.", "green", [("Home", "index.html"), ("School life", "school-life.html")], cta=False) + \
        '<section class="section"><div class="wrap">%s</div></section>' % news_list()
    page("news.html", "News", "News and newsletters from Mellow Oaks Academy.", body)


def build_admissions():
    steps = [("Apply online", "Complete the online application and upload your documents as you go."),
             ("We'll get back to you", "The admissions office receives your application and contacts you."),
             ("Visit the school", "See the campus and ask your questions. Every Friday is Open Day.")]
    body = hero_inner("Admissions", "Join the Mellow Oaks family", "Where curiosity blooms, character is cultivated, and every learner is nurtured to thrive.", "science", [("Home", "index.html")]) + \
        '<section class="section"><div class="wrap"><div class="head"><h2>How to apply</h2><p>Three simple steps.</p></div><ol class="steps">%s</ol><div class="btn-row center"><a class="btn btn-leaf" href="apply.html">Start your application</a></div></div></section>' % "".join(
            '<li><span class="s-num">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(t), esc(d)) for i, (t, d) in enumerate(steps)) + \
        '<section class="section tint"><div class="wrap"><div class="head"><h2>We accept applications for</h2></div>%s</div></section>' % phase_path() + \
        split("classroom", "Questions about admissions?", prose("The admissions office is open %s." % HOURS, "Prefer to talk first? Leave your details and the school will get back to you.")
              + '<div class="btn-row"><a class="btn btn-leaf" href="contact.html#tour">Leave your details</a><a class="btn btn-line" href="fees.html">See school fees</a></div>') + cta_band()
    page("admissions.html", "Admissions", "How to apply to Mellow Oaks Academy for 2027.", body)


def build_fees():
    body = hero_inner("Admissions", "School fees", "Fee structures for 2026 and 2027, from the school office.", "computers", [("Home", "index.html"), ("Admissions", "admissions.html")], cta=False) + \
        '<section class="section"><div class="wrap fee-grid">%s</div><div class="wrap"><p class="form-note">Questions about fees? Call <a href="tel:%s">%s</a> or email <a href="mailto:%s">%s</a>.</p></div></section>' % (
            "".join('<a class="fee" href="%s" rel="noopener"><span class="fee-year">%s</span><span class="fee-t">%s</span><span class="fee-go">Open the PDF</span></a>' % (u, y, t) for u, y, t in [
                (FEES_2027, "2027", "Fee structure for the 2027 school year"), (FEES_2026, "2026", "Fee structure for the current school year")]), PHONE_TEL, PHONE, EMAIL_INFO, EMAIL_INFO) + cta_band()
    page("fees.html", "School fees", "Mellow Oaks Academy school fees for 2026 and 2027.", body)


def build_contact():
    body = hero_inner("Contact", "Get in touch", "Chat to us by phone or WhatsApp, send an email, or leave your details to book a tour.", "outdoor", [("Home", "index.html")], cta=False) + """
<section class="section" id="tour">
  <div class="wrap contact-grid">
    <div class="card-plain">
      <h2>Contact details</h2>
      <dl class="visit-list dark">
        <dt>Phone</dt><dd><a href="tel:%s">%s</a></dd>
        <dt>WhatsApp</dt><dd><a href="%s" rel="noopener">%s</a></dd>
        <dt>Administrative enquiries</dt><dd><a href="mailto:%s">%s</a></dd>
        <dt>General enquiries</dt><dd><a href="mailto:%s">%s</a></dd>
        <dt>Address</dt><dd>%s</dd>
        <dt>Office hours</dt><dd>%s</dd>
      </dl>
    </div>
    <form class="card-plain enquiry" id="enquiry" novalidate>
      <h2>Book a tour or ask a question</h2>
      <div class="field"><label for="q-name">Your name</label><input id="q-name" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
      <div class="field"><label for="q-phone">Mobile number</label><input id="q-phone" type="tel" autocomplete="tel" required><span class="err" aria-live="polite"></span></div>
      <div class="field"><label for="q-type">I'd like to</label><select id="q-type"><option>Book a tour</option><option>Ask about admissions</option><option>Ask about fees</option><option>Something else</option></select></div>
      <div class="field"><label for="q-msg">Message (optional)</label><textarea id="q-msg" rows="3"></textarea></div>
      <button class="btn btn-leaf" type="submit">Send</button>
      <div class="done" hidden tabindex="-1" role="status"><b>Thank you.</b> This is a concept preview, so nothing was sent. On the live site, the school office would receive this straight away.</div>
    </form>
  </div>
</section>""" % (PHONE_TEL, PHONE, WA_URL, WA, EMAIL_INFO, EMAIL_INFO, EMAIL_RECEPTION, EMAIL_RECEPTION, esc(ADDRESS), esc(HOURS))
    page("contact.html", "Contact", "Contact Mellow Oaks Academy, book a tour or ask a question.", body)


def build_apply():
    grades = ["Pre-Primary (18 months to Grade RR)", "Grade R", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7",
              "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"]
    provinces = ["Gauteng", "Eastern Cape", "Free State", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "North West", "Northern Cape", "Western Cape"]
    opt = lambda xs: "".join("<option>%s</option>" % esc(x) for x in xs)
    rel = opt(["Mother", "Father", "Legal guardian", "Grandparent", "Other"])

    def parent(n, req):
        r = " required" if req else ""
        return """
<fieldset class="parent" data-parent="%d"%s>
  <legend>Parent or guardian %d%s</legend>
  <div class="grid2">
    <div class="field"><label for="p%d-rel">Relationship</label><select id="p%d-rel"%s><option value="">Choose</option>%s</select><span class="err"></span></div>
    <div class="field"><label for="p%d-name">Full name</label><input id="p%d-name" autocomplete="%s"%s><span class="err"></span></div>
    <div class="field"><label for="p%d-phone">Mobile number</label><input id="p%d-phone" type="tel"%s><span class="err"></span></div>
    <div class="field"><label for="p%d-email">Email</label><input id="p%d-email" type="email"%s><span class="err"></span></div>
  </div>
</fieldset>""" % (n, "" if req else ' hidden', n, "" if req else " (optional)", n, n, r, rel, n, n, "name" if n == 1 else "off", r, n, n, r, n, n, r)

    docs = [("doc-birth", "Learner's birth certificate", True), ("doc-report", "Latest school report", False),
            ("doc-id", "Parent or guardian ID copy", True), ("doc-res", "Proof of residence", False)]
    doc_html = "".join('<li class="upload" data-required="%s"><input type="file" id="%s" accept=".pdf,.jpg,.jpeg,.png"><label for="%s"><span class="u-ico" aria-hidden="true"></span><span class="u-text"><b>%s</b><small>%s PDF, JPG or PNG</small></span><span class="u-state">Choose file</span></label></li>' % (
        "1" if r else "0", i, i, esc(t), "Required." if r else "Optional.") for i, t, r in docs)
    body = """
<section class="apply-hero">
  <div class="wrap"><p class="crumbs"><a href="./">Home</a> / <a href="admissions">Admissions</a> / <span aria-current="page">Apply online</span></p>
  <h1>Apply online</h1><p class="lede">Five short steps. You can go back to any step before you submit.</p></div>
</section>
<section class="apply">
  <div class="wrap apply-grid">
    <ol class="progress" aria-label="Application steps"><li>Learner</li><li>Parents</li><li>Address</li><li>Documents</li><li>Review</li></ol>
    <form id="apply" novalidate>
      <section class="step" data-step="0" aria-labelledby="h0">
        <h2 id="h0">About the learner</h2>
        <div class="grid2">
          <div class="field"><label for="l-grade">Grade applying for</label><select id="l-grade" required><option value="">Choose a grade</option>%s</select><span class="err"></span></div>
          <div class="field"><label for="l-year">Intake year</label><select id="l-year" required><option value="">Choose</option><option>2027</option><option>2026 (this year)</option></select><span class="err"></span></div>
          <div class="field"><label for="l-first">First names</label><input id="l-first" required><span class="err"></span></div>
          <div class="field"><label for="l-last">Surname</label><input id="l-last" required><span class="err"></span></div>
          <div class="field"><label for="l-dob">Date of birth</label><input id="l-dob" type="date" required><span class="err"></span></div>
          <div class="field"><label for="l-lang">Home language</label><input id="l-lang" placeholder="e.g. English"><span class="err"></span></div>
          <div class="field wide"><label for="l-school">Current school (if any)</label><input id="l-school"><span class="err"></span></div>
        </div>
      </section>
      <section class="step" data-step="1" aria-labelledby="h1" hidden>
        <h2 id="h1">Parents and guardians</h2>
        %s%s
        <button class="add-parent" type="button" aria-controls="p2">+ Add a second parent or guardian</button>
      </section>
      <section class="step" data-step="2" aria-labelledby="h2" hidden>
        <h2 id="h2">Home address</h2>
        <div class="grid2">
          <div class="field wide"><label for="a-street">Street address</label><input id="a-street" autocomplete="street-address" required><span class="err"></span></div>
          <div class="field"><label for="a-suburb">Suburb</label><input id="a-suburb" required><span class="err"></span></div>
          <div class="field"><label for="a-city">City or town</label><input id="a-city" value="Roodepoort" required><span class="err"></span></div>
          <div class="field"><label for="a-prov">Province</label><select id="a-prov" required>%s</select><span class="err"></span></div>
          <div class="field"><label for="a-code">Postal code</label><input id="a-code" inputmode="numeric" maxlength="4" required><span class="err"></span></div>
        </div>
      </section>
      <section class="step" data-step="3" aria-labelledby="h3" hidden>
        <h2 id="h3">Documents</h2>
        <p class="form-note">Upload what you have now. The office will ask for anything that's missing.</p>
        <ul class="uploads">%s</ul>
      </section>
      <section class="step" data-step="4" aria-labelledby="h4" hidden>
        <h2 id="h4">Review and submit</h2>
        <dl class="review" id="review"></dl>
        <label class="consent"><input type="checkbox" id="consent"><span>I confirm the information is true, and I consent to Mellow Oaks Academy processing it for admissions, in line with the Protection of Personal Information Act (POPIA).</span></label>
        <span class="err" id="consent-err" aria-live="polite"></span>
        <p class="form-note">Banking details for school fees are collected securely once a place is offered, not on this form.</p>
      </section>
      <div class="done" id="done" hidden tabindex="-1" role="status">
        <div class="done-badge" aria-hidden="true"></div>
        <h2>Application received</h2>
        <p>This is a concept preview, so nothing was sent. On the live site, the admissions office would receive this application with its documents, and you would get a confirmation email straight away.</p>
        <a class="btn btn-leaf" href="./">Back to home</a>
      </div>
      <div class="actions"><button class="btn btn-line" type="button" id="back">Back</button><button class="btn btn-leaf" type="button" id="next">Continue</button></div>
    </form>
    <aside class="apply-side">
      <h2>Good to know</h2>
      <ul class="ticks"><li>Classes are capped at 20 learners.</li><li>2027 registrations are open, with limited spaces.</li><li>Every Friday is Open Day.</li></ul>
      <p>Need help? Call <a href="tel:%s">%s</a> or WhatsApp <a href="%s" rel="noopener">%s</a>.</p>
    </aside>
  </div>
</section>""" % (opt(grades), parent(1, True), parent(2, False), opt(provinces), doc_html, PHONE_TEL, PHONE, WA_URL, WA)
    page("apply.html", "Apply online", "Apply online to Mellow Oaks Academy for 2027.", body, scripts=("site.js", "ask.js", "apply.js"))



# ------------------------------------------------------------------ site index: instant search (site-index.json) and the assistant's knowledge (src/site-index.json)
def strip_tags(h):
    h = re.sub(r"(?is)<(script|style|svg|select)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|li|h[1-6]|dt|dd|tr)>", "\n", h)
    return html.unescape(re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"<[^>]+>", " ", h))).strip()


def build_index():
    pages, chunks = [], []
    for fn in sorted(x for x in os.listdir(ROOT) if x.endswith(".html")):
        doc = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        url = "/" if fn == "index.html" else "/" + fn[:-5]
        title = "Home" if fn == "index.html" else re.search(r"<title>(.*?) \|", doc).group(1)
        desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', doc).group(1))
        main = re.search(r'(?s)<main id="main">(.*)</main>', doc).group(1)
        main = re.sub(r'(?s)<section class="cta">.*?</section>', " ", main)
        main = re.sub(r'(?s)<section class="section tint">\s*<div class="wrap">\s*<div class="head row"><h2>More news</h2>.*?</section>', " ", main)
        if fn != "news.html":
            main = re.sub(r'(?s)<ul class="news rich">.*?</ul>', " ", main)
        heads = [strip_tags(h) for h in re.findall(r"(?s)<h2[^>]*>(.*?)</h2>", main)]
        pages.append({"t": html.unescape(title), "u": url, "d": desc, "h": heads[:8], "news": fn.startswith("news-")})
        parts = re.split(r"(?=<h2)", main)
        for part in parts:
            txt = re.sub(r"\n\s*\n+", "\n", strip_tags(part)).strip()
            if len(txt) < 40:
                continue
            hd = re.search(r"(?s)<h2[^>]*>(.*?)</h2>", part)
            for i in range(0, len(txt), 1100):
                chunks.append({"u": url, "t": html.unescape(title), "h": strip_tags(hd.group(1)) if hd else "", "x": txt[i:i + 1100]})
    # facts that live in the footer and header on every page
    chunks.append({"u": "/contact", "t": "Contact", "h": "Contact details and office hours",
                   "x": "Address: %s. Phone: %s. WhatsApp: %s. Email: %s and %s. Office hours: %s. Every Friday is Open Day." % (ADDRESS, PHONE, WA, EMAIL_INFO, EMAIL_RECEPTION, HOURS)})
    chunks.append({"u": "/fees", "t": "School fees", "h": "Fee documents",
                   "x": "The 2026 school fees are in this PDF: %s . The 2027 school fees are in this PDF: %s . The amounts are inside the PDFs." % (FEES_2026, FEES_2027)})
    os.makedirs(os.path.join(ROOT, "src"), exist_ok=True)
    json.dump(pages, open(os.path.join(ROOT, "site-index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    json.dump({"pages": [{"t": p["t"], "u": p["u"], "news": p["news"]} for p in pages], "chunks": chunks},
              open(os.path.join(ROOT, "src", "site-index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("index:", len(pages), "pages,", len(chunks), "chunks")


if __name__ == "__main__":
    for f in (build_home, build_about, build_principal, build_careers, build_academics, build_phases, build_support,
              build_school_life, build_sports, build_news, build_posts, build_admissions, build_fees, build_contact, build_apply):
        f()
    build_index()
    print("built", sorted(x for x in os.listdir(ROOT) if x.endswith(".html")))
