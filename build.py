#!/usr/bin/env python3
"""Generates the Scalpx static site into ./public. Run: python3 build.py"""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
SITE = "https://scalpx-orcin.vercel.app"

KEYWORDS = ("scalp treatment, scalp care, hair growth, hair loss treatment, afro hair care, natural hair care, "
            "textured hair scalp clinic, scalp analysis, scalp detox, dandruff treatment, hair thinning, "
            "trichology, healthy hair, curly hair care, scalp health")

LOGO = '''<svg viewBox="0 0 40 40" fill="none" aria-hidden="true"><rect width="40" height="40" rx="12" fill="#0c0c0c"/><path d="M20 8c-4 6-7 9.5-7 14a7 7 0 0014 0c0-4.500-3-8-7-14z" fill="#fff"/><path d="M16.500 22l7 7m0-7l-7 7" stroke="#ff5a1f" stroke-width="2.200" stroke-linecap="round"/></svg>'''
ARROW = "↗"

def nav(active):
    items = [("index.html", "Home"), ("about.html", "About"), ("treatments.html", "Treatments"), ("results.html", "Results"), ("blog.html", "Blog")]
    links = "".join(f'<a href="{h}"{" class=on" if h == active else ""}>{t}</a>' for h, t in items)
    mlinks = "".join(f'<a class="big" href="{h}">{t}<span>0{i+1}</span></a>' for i, (h, t) in enumerate(items))
    return f'''<header class="nav glass" role="banner">
 <a class="logo" href="index.html" aria-label="Scalpx home">{LOGO}<div>Scalpx<small>Scalp &amp; Hair Clinic</small></div></a>
 <nav class="links" aria-label="Primary">{links}</nav>
 <div class="nav-cta">
  <a class="login-link" data-auth="out" href="login.html">Log in</a>
  <a class="avatar" data-auth="in" href="dashboard.html" aria-label="Your dashboard" style="display:none"><span data-initial></span></a>
  <a class="btn btn-dark btn-sm" href="book.html">Book Consultation <i>{ARROW}</i></a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i></button>
 </div>
</header>
<div class="menu" aria-label="Mobile menu">{mlinks}
 <a class="big" data-auth="out" href="login.html">Log in<span>Account</span></a>
 <a class="big" data-auth="in" href="dashboard.html" style="display:none">Dashboard<span data-name></span></a>
 <a class="btn btn-acc" style="align-self:flex-start;margin-top:22px" href="book.html">Book Consultation <i>{ARROW}</i></a>
</div>'''

FOOT = f'''<footer class="foot" role="contentinfo"><div class="wrap">
 <div class="cols">
  <div><a class="logo" href="index.html">{LOGO}<div>Scalpx</div></a>
   <p style="color:#a7a5a0;max-width:340px;margin:18px 0 22px;font-size:14px">Science-led scalp care for textured, curly, coily and straight hair. Healthier hair starts at the scalp.</p>
   <form id="newsform" class="news" novalidate><input class="sr" name="hp" tabindex="-1" aria-hidden="true"><label class="sr" for="nl">Email</label>
    <input id="nl" name="email" type="email" placeholder="Your email" style="flex:1;min-width:170px;padding:14px 18px;border-radius:99px;border:1px solid #333;background:#161616;color:#fff;font:inherit;font-size:14px">
    <button class="btn btn-acc btn-sm" type="submit">Join <i>{ARROW}</i></button></form></div>
  <div><h5>Explore</h5><ul><li><a href="index.html">Home</a></li><li><a href="about.html">About</a></li><li><a href="treatments.html">Treatments</a></li><li><a href="results.html">Results</a></li><li><a href="blog.html">Blog</a></li></ul></div>
  <div><h5>Account</h5><ul><li><a href="login.html">Log in</a></li><li><a href="login.html#register">Create account</a></li><li><a href="dashboard.html">Dashboard</a></li><li><a href="book.html">Book consultation</a></li></ul></div>
  <div><h5>Care</h5><ul><li><a href="treatments.html#analysis">Scalp analysis</a></li><li><a href="treatments.html#detox">Scalp detox</a></li><li><a href="treatments.html#growth">Hair growth</a></li><li><a href="treatments.html#textured">Textured hair care</a></li></ul></div>
 </div>
 <div class="big" aria-hidden="true">scalpx</div>
 <div class="legal"><span>© 2026 Scalpx Scalp &amp; Hair Clinic. All rights reserved.</span><span>Content is informational and not medical advice.</span></div>
 <div class="tags">{" ".join(f"<span>#{t}</span>" for t in ["ScalpCare","HairGrowth","NaturalHair","AfroHair","ScalpHealth","HairLossTreatment","Trichology","CurlyHair"])}</div>
</div></footer>'''

def head(title, desc, path, extra=""):
    ld = {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness", "name": "Scalpx Scalp & Hair Clinic",
          "description": "Science-led scalp analysis, treatments and ongoing care for stronger, fuller hair.", "url": SITE,
          "image": SITE + "/img/og.jpg", "knowsAbout": ["Scalp care", "Hair growth", "Afro-textured hair", "Hair loss"]}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta name="keywords" content="{KEYWORDS}">
<meta name="theme-color" content="#f4f3ef"><link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{SITE}/img/og.jpg"><meta property="og:url" content="{SITE}/{path}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="preload" href="fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css"><script type="application/ld+json">{json.dumps(ld)}</script>{extra}</head>'''

def page(fname, title, desc, body, active=None, shell=True):
    html = head(title, desc, fname) + "<body>" + (nav(active or fname) if shell else "") + "<main id=\"main\">" + body + "</main>" + (FOOT if shell else "") + '<script src="js/main.js" defer></script></body></html>'
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)

def head_sec(eyebrow, h2, p=""):
    return f'<div class="sec-head"><div class="rv"><span class="eyebrow">{eyebrow}</span><h2 style="margin-top:16px">{h2}</h2></div><p class="rv" style="--d:.1s">{p}</p></div>'

# ---------------------------------------------------------------- HOME
home = f'''
<section class="hero">
 <div class="hero-copy">
  <span class="eyebrow">Scalp &amp; Hair Clinic</span>
  <h1><span class="l"><span>Healthier</span></span><span class="l"><span>Hair Starts</span></span><span class="l"><span class="dim">at the Scalp</span></span></h1>
  <p class="lead">Science-backed scalp treatments for stronger, fuller and longer-lasting hair health, for every texture.</p>
  <a class="btn btn-dark" href="book.html">Book Consultation <i>{ARROW}</i></a>
 </div>
 <aside class="float-card glass-dark tilt"><img src="img/gold.webp" alt="Macro view of a nourished hair follicle" loading="eager">
  <div class="row"><div><h4>Advanced<br>Scalp Treatment</h4><p>Targeted care for the root cause of hair concerns.</p></div><a class="circ w" href="treatments.html" aria-label="See treatments">{ARROW}</a></div></aside>
 <div class="hero-figure" aria-hidden="true">
  <img class="trail t2" src="img/man-cut.webp" alt=""><img class="trail t1" src="img/man-cut.webp" alt="">
  <img class="main" src="img/man-cut.webp" alt="Man with a healthy afro in profile" fetchpriority="high">
 </div>
 <div class="hero-word" aria-hidden="true">scalp<b>x</b></div>
 <div class="scroll-cue"><i></i>Scroll</div>
</section>
<div class="ticker" aria-hidden="true"><div class="tr">{"".join('<span>Scalp analysis</span><span>Hair growth</span><span>Scalp detox</span><span>Afro &amp; textured care</span><span>Anti-dandruff</span><span>Follicle health</span>' for _ in range(4))}</div></div>

<section class="sec" id="approach"><div class="wrap">
 {head_sec("Our approach", 'Advanced scalp care for <span class="acc">stronger, fuller</span> hair.', "We combine expert care with advanced technology to treat the root cause of hair concerns, because healthier hair begins with a healthier scalp.")}
 <div class="cards">
  <a class="card rv" href="treatments.html#analysis"><img src="img/blue.webp" alt="Digital scalp analysis visual" loading="lazy"><span class="tag glass-dark">01 · Scalp Analysis</span><div class="in"><h3>Understand Your Scalp Better</h3><p>In-depth scalp analysis to identify concerns and create a personalised treatment plan.</p></div><span class="circ w">{ARROW}</span></a>
  <a class="card rv" style="--d:.1s" href="treatments.html#growth"><img src="img/gold.webp" alt="Golden serum around hair follicles" loading="lazy"><span class="tag glass-dark">02 · Treatment</span><div class="in"><h3>Targeted Treatments <em>Real Results</em></h3><p>Evidence-informed protocols to improve scalp health and nurture natural hair growth.</p></div><span class="circ w">{ARROW}</span></a>
  <a class="card rv" style="--d:.2s" href="treatments.html#textured"><img src="img/black.webp" alt="Strong hair follicle rising from the scalp" loading="lazy"><span class="tag glass-dark">03 · Hair Growth</span><div class="in"><h3>Stronger Hair From the Root</h3><p>Nourish, strengthen and rejuvenate your scalp for long-term hair health.</p></div><span class="circ w">{ARROW}</span></a>
  <a class="card light rv" style="--d:.3s" href="treatments.html#detox"><img src="img/oil.webp" alt="Woman applying growth oil with a dropper" loading="lazy" style="object-position:50% 20%"><span class="tag glass">04 · Ongoing Care</span><div class="in"><h3>A Healthier Scalp for a Brighter You</h3><p>Continued care and expert guidance to maintain visible, lasting results.</p></div><span class="circ">{ARROW}</span></a>
 </div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap split">
 <div class="pic ratio-45 rvx"><img data-par=".05" src="img/woman.webp" alt="Woman with a full natural afro and healthy scalp" loading="lazy" style="height:112%"></div>
 <div>
  <span class="eyebrow rv">Built for every texture</span>
  <p class="quote rv" style="margin:18px 0 34px">Coils, curls, twists or waves, <span class="dim">your scalp is the foundation.</span> We design care around your hair’s natural pattern, not against it.</p>
  <div class="stats">
   <div class="stat"><b data-count="98">0<sup>%</sup></b><span>would recommend Scalpx*</span></div>
   <div class="stat"><b data-count="12">0<sup>wk</sup></b><span>typical plan length</span></div>
   <div class="stat"><b data-count="6">0<sup>+</sup></b><span>targeted treatments</span></div>
   <div class="stat"><b data-count="1">0<sup>:1</sup></b><span>personal specialist</span></div>
  </div>
  <p style="font-size:11px;color:var(--mute);margin-top:12px">*Illustrative sample figures for this demo site.</p>
 </div>
</div></section>

<section class="dark-sec sec" id="treat"><div class="wrap">
 <div class="orb" style="width:420px;height:420px;background:#ff5a1f;right:-120px;top:-100px"></div>
 {head_sec("Treatments", "Care that starts at the follicle.", "Six signature protocols, each built around analysis, not guesswork.")}
 <div class="tlist">
  {"".join(f'<a class="trow rv" href="treatments.html#{i}"><span class="n">0{n}</span><h3>{t}</h3><p>{d}</p><span class="circ">{ARROW}</span></a>' for n,(i,t,d) in enumerate([("analysis","Digital Scalp Analysis","Micro-imaging of density, sebum, flaking and follicle health."),("detox","Deep Scalp Detox","Clarifying care that lifts build-up without stripping coils."),("growth","Hair Growth Therapy","Serums and stimulation to support the growth cycle."),("textured","Textured Hair Ritual","Moisture-first routines for afro, curly and coily hair."),("dandruff","Dandruff &amp; Itch Relief","Calm irritation and restore a balanced scalp."),("maintain","Maintenance Plans","Monthly check-ins to protect your results.")],1))}
 </div>
</div></section>

<section class="sec"><div class="wrap split">
 <div>
  <span class="eyebrow rv">Under the surface</span>
  <h2 class="rv" style="font-size:clamp(34px,4.6vw,66px);margin:16px 0 20px">See what your scalp is really doing.</h2>
  <p class="rv" style="color:var(--mute);max-width:440px;margin-bottom:28px">Every strand grows from a living follicle. When the scalp is balanced, hydrated, clean and well-nourished, hair grows stronger and fuller. We map it, treat it and track it.</p>
  <a class="btn btn-line rv" href="about.html">How it works <i>{ARROW}</i></a>
 </div>
 <div class="pic ratio-1 rvx glass-dark" style="border-radius:40px"><img data-par="-.04" src="img/helix.webp" alt="Follicle wrapped in a golden helix" loading="lazy" style="height:112%"></div>
</div></section>

<section class="cta glass-dark" style="margin-top:20px"><img src="img/glow.webp" alt="" loading="lazy">
 <div><span class="eyebrow" style="color:#ddd">Start today</span><h2>Your healthiest hair begins with one consultation.</h2>
 <a class="btn btn-acc" href="book.html">Book Consultation <i>{ARROW}</i></a></div></section>
'''
page("index.html", "Scalpx: Scalp & Hair Clinic | Healthier Hair Starts at the Scalp",
     "Scalpx is a science-led scalp and hair clinic: scalp analysis, hair growth treatments and ongoing care for afro, curly and straight hair.", home)

# ---------------------------------------------------------------- ABOUT
about = f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">About Scalpx</span><h1>Root-cause<br><span class="dim">hair science.</span></h1>
<p>We started Scalpx because great hair care ignores the one thing that matters most: the skin it grows from.</p></div>
<div class="bgimg rvx"><img src="img/man.webp" alt="Man with a healthy afro"></div></section>
<section class="sec" style="padding-top:40px"><div class="wrap split">
 <div class="pic ratio-45 rvx"><img src="img/twists.webp" alt="Man receiving a scalp treatment on twists" style="object-position:40% 50%" loading="lazy"></div>
 <div><span class="eyebrow rv">Our story</span><h2 class="rv" style="font-size:clamp(32px,4vw,56px);margin:16px 0 20px">Hair is the result. The scalp is the cause.</h2>
 <p class="rv" style="color:var(--mute);margin-bottom:16px">Product-first routines often treat symptoms, dryness, shedding, flakes, while the scalp environment stays unbalanced. Scalpx flips the order: analyse first, then treat what the scalp actually needs.</p>
 <p class="rv" style="color:var(--mute);margin-bottom:28px">Our protocols are designed with textured and afro hair in mind, where tension, dryness and protective styling make scalp care essential.</p>
 <a class="btn btn-dark rv" href="book.html">Meet a specialist <i>{ARROW}</i></a></div>
</div></section>
<section class="dark-sec sec"><div class="wrap">
 {head_sec("How it works", "Four steps. One healthier scalp.", "A simple, repeatable journey from first look to lasting results.")}
 <div class="steps" style="--paper:#151515">
  {"".join(f'<div class="step rv glass-dark" style="--d:{i*.08}s"><div><h3>{t}</h3><p style="color:#a7a5a0">{d}</p></div></div>' for i,(t,d) in enumerate([("Analyse","Micro-imaging maps density, oil balance and follicle health."),("Plan","A personalised protocol built around your texture and goals."),("Treat","In-clinic therapies paired with a simple at-home routine."),("Maintain","Progress reviews and adjustments to protect results.")]))}
 </div>
</div></section>
<section class="sec"><div class="wrap">
 {head_sec("Principles", "What we stand for.", "")}
 <div class="tgrid">
  {"".join(f'<div class="tcard rv" style="--d:{i*.1}s"><div class="im"><img src="img/{im}.webp" alt="" loading="lazy"></div><div class="tx"><h3>{t}</h3><p>{d}</p></div></div>' for i,(im,t,d) in enumerate([("gold","Evidence-informed","We choose methods supported by dermatology and trichology research, and say so when evidence is limited."),("woman","Texture-respecting","Care designed for afro, curly and coily hair, never one-size-fits-all."),("helix","Honest outcomes","Hair cycles take months. We set clear expectations and track real progress.")]))}
 </div>
</div></section>
'''
page("about.html", "About Scalpx: Root-Cause Scalp & Hair Science",
     "Learn how Scalpx uses scalp analysis and personalised care for afro, curly and straight hair to support healthier, fuller hair growth.", about)

# ---------------------------------------------------------------- TREATMENTS
T = [("analysis","blue","Digital Scalp Analysis","Micro-imaging of density, sebum, flaking and follicle health to build your baseline.","45 min","First visit"),
     ("detox","twists","Deep Scalp Detox","Clarifying exfoliation and soothing care that lifts build-up without stripping coils.","60 min","Monthly"),
     ("growth","gold","Hair Growth Therapy","Nutrient serums and scalp stimulation to support the natural growth cycle.","60 min","12-week plan"),
     ("textured","woman","Textured Hair Ritual","Moisture-first routine for afro, curly and coily hair: scalp care, oiling and protective-style guidance.","75 min","Every 6 weeks"),
     ("dandruff","glow","Dandruff &amp; Itch Relief","Calm irritation, rebalance the microbiome and restore comfort.","45 min","4–6 sessions"),
     ("maintain","oil","Maintenance Plans","Check-ins and refills to protect your progress long-term.","30 min","Ongoing")]
treat = f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Treatments</span><h1>Care that<br><span class="dim">starts at the root.</span></h1>
<p>Six signature protocols, each beginning with analysis so you only get what your scalp needs.</p></div><div class="bgimg rvx"><img src="img/gold.webp" alt=""></div></section>
<section class="sec" style="padding-top:30px"><div class="wrap"><div class="tgrid">
{"".join(f'<article id="{i}" class="tcard rv" style="--d:{(n%3)*.1}s;scroll-margin-top:110px"><div class="im"><img src="img/{im}.webp" alt="{t}" loading="lazy"></div><div class="tx"><div class="meta"><span>{d}</span><span>{f}</span></div><h3>{t}</h3><p>{desc}</p><a class="btn btn-line btn-sm" style="align-self:flex-start" href="book.html">Book this <i>{ARROW}</i></a></div></article>' for n,(i,im,t,desc,d,f) in enumerate(T))}
</div></div></section>
<section class="dark-sec sec"><div class="wrap split">
 <div><span class="eyebrow">The process</span><h2 style="margin:16px 0 20px">Your first visit.</h2><p style="color:#a7a5a0;max-width:420px;margin-bottom:26px">Relaxed, unhurried and tailored. You leave with a clear plan and a routine you can actually follow.</p><a class="btn btn-acc" href="book.html">Book analysis <i>{ARROW}</i></a></div>
 <div class="steps" style="grid-template-columns:1fr 1fr">{"".join(f'<div class="step glass-dark rv" style="min-height:190px"><div><h3>{t}</h3><p style="color:#a7a5a0">{d}</p></div></div>' for t,d in [("Consult","Goals, history and lifestyle."),("Image","Scalp micro-imaging."),("Plan","Your protocol and timeline."),("Begin","First treatment and routine.")])}</div>
</div></section>
<section class="sec"><div class="wrap">{head_sec("FAQ","Good questions.","")}
<div class="faq">
 <details class="rv"><summary>Do you treat afro and textured hair?</summary><p>Yes, our protocols are built with coily, curly and protective-styled hair in mind, including tension and dryness concerns.</p></details>
 <details class="rv"><summary>How long until I see a difference?</summary><p>Scalp comfort can improve within weeks; visible hair changes follow the growth cycle and usually take 3–6 months.</p></details>
 <details class="rv"><summary>Is this medical treatment?</summary><p>Scalpx offers cosmetic and wellness scalp care. For suspected medical conditions we recommend seeing a dermatologist.</p></details>
 <details class="rv"><summary>Do I need an account?</summary><p>No, you can book as a guest. An account lets you track consultations and your routine in your dashboard.</p></details>
</div></div></section>'''
page("treatments.html", "Scalp Treatments: Analysis, Detox & Hair Growth | Scalpx",
     "Explore Scalpx treatments: digital scalp analysis, deep scalp detox, hair growth therapy and textured hair rituals for afro and curly hair.", treat)

# ---------------------------------------------------------------- RESULTS
res = f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Results</span><h1>What progress<br><span class="dim">looks like.</span></h1>
<p>An honest timeline of what most clients can expect on a consistent plan. Individual results vary.</p></div><div class="bgimg rvx"><img src="img/oil.webp" alt="" style="object-position:50% 20%"></div></section>
<section class="dark-sec sec"><div class="wrap split">
 <div><span class="eyebrow">Typical plan outcomes</span><h2 style="margin:16px 0 28px">Measured, not promised.</h2>
  <div class="bar"><div class="lab"><span>Scalp comfort &amp; flaking</span><span>4–6 wks</span></div><div class="tk"><i style="--w:82%"></i></div></div>
  <div class="bar"><div class="lab"><span>Shedding reduction</span><span>8–12 wks</span></div><div class="tk"><i style="--w:68%"></i></div></div>
  <div class="bar"><div class="lab"><span>Visible density &amp; thickness</span><span>3–6 mo</span></div><div class="tk"><i style="--w:55%"></i></div></div>
  <div class="bar"><div class="lab"><span>Long-term maintenance</span><span>6 mo +</span></div><div class="tk"><i style="--w:90%"></i></div></div>
  <p style="font-size:12px;color:#8d8b86;margin-top:20px">Illustrative demo data, replace with your clinic’s verified outcomes.</p></div>
 <div class="pic ratio-45 rvx"><img src="img/woman-cut.webp" alt="" style="object-fit:contain;background:radial-gradient(circle at 50% 40%,#ff5a1f55,transparent 70%),#111"></div>
</div></section>
<section class="sec"><div class="wrap">{head_sec("Client journeys","Three common paths.","")}
 <div class="tgrid">
  {"".join(f'<div class="tcard rv" style="--d:{i*.1}s"><div class="im"><img src="img/{im}.webp" alt="" loading="lazy"></div><div class="tx"><div class="meta"><span>{m}</span></div><h3>{t}</h3><p>{d}</p></div></div>' for i,(im,m,t,d) in enumerate([("twists","Protective styles","Tension &amp; dryness","Detox and oiling rituals to ease tight styles and keep the scalp comfortable."),("black","Thinning","Strength at the root","A growth plan pairing stimulation with nutrient-dense serums."),("oil","Daily routine","Simple &amp; sustainable","A short at-home routine reinforced with monthly check-ins.")]))}
 </div></div></section>
<section class="cta glass-dark"><img src="img/gold.webp" alt="" loading="lazy"><div><span class="eyebrow" style="color:#ddd">Ready?</span><h2>Start your own scalp journey.</h2><a class="btn btn-acc" href="book.html">Book Consultation <i>{ARROW}</i></a></div></section>'''
page("results.html", "Results & Timelines: Scalp Care That Works | Scalpx",
     "See what progress with Scalpx looks like: realistic timelines for scalp comfort, shedding, density and long-term hair health.", res)

# ---------------------------------------------------------------- BLOG
B = [("Hair growth","gold","How the hair growth cycle really works","Anagen, catagen, telogen, and why patience matters.","<p>Hair grows in cycles: a long growth phase (anagen), a brief transition (catagen) and a resting phase (telogen) before shedding.</p><p>Because every follicle runs on its own schedule, visible change takes months. Consistent scalp care supports the environment each follicle grows in.</p>"),
     ("Textured hair","woman","Afro hair & scalp care: a moisture-first guide","Why coils need a different routine.","<p>Natural oils travel slowly down tightly coiled strands, so dryness is common. A healthy scalp is the starting point.</p><p>Cleanse regularly, seal moisture and avoid prolonged tension from tight styles.</p>"),
     ("Scalp health","twists","Do you need a scalp detox?","Signs of build-up and how to clear it gently.","<p>Itch, flaking that returns quickly, or products that stop working can signal build-up.</p><p>A gentle clarifying treatment once a month is enough for most people.</p>"),
     ("Hair growth","oil","Oils, serums & the scalp: what to apply","Apply smart, not more.","<p>Lightweight oils or serums applied to a clean scalp with a dropper give control and avoid heavy residue.</p><p>Massage for a minute to support circulation.</p>"),
     ("Scalp health","blue","What scalp analysis reveals","Your scalp, magnified.","<p>Micro-imaging shows density, oil balance, and follicle openings, information you can’t see in a mirror.</p>"),
     ("Textured hair","helix","Protective styles without the damage","Keep the style, protect the scalp.","<p>Keep tension low, avoid styles that pull at the hairline and give your scalp rest between installs.</p>")]
blog = f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Journal</span><h1>Scalp notes<br><span class="dim">&amp; hair science.</span></h1>
<div class="chips" style="margin-top:26px">{"".join(f'<button class="chip{" on" if f=="all" else ""}" data-f="{f}">{l}</button>' for f,l in [("all","All"),("Hair growth","Hair growth"),("Textured hair","Textured hair"),("Scalp health","Scalp health")])}</div></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="posts">
{"".join(f'<article class="post rv" role="button" tabindex="0" data-cat="{c}" data-img="img/{im}.webp" style="--d:{(i%3)*.1}s"><div class="im"><img src="img/{im}.webp" alt="" loading="lazy"></div><div class="tx"><small>{c}</small><h3>{t}</h3><p>{d}</p><template>{body}</template></div></article>' for i,(c,im,t,d,body) in enumerate(B))}
</div></div></section>
<div class="modal" role="dialog" aria-modal="true"><div class="box glass" style="background:#fff"><button class="x-btn" aria-label="Close">✕</button><img src="" alt=""><div class="bd"><small class="acc" style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:11px"></small><h3></h3><div class="body"></div></div></div></div>'''
page("blog.html", "Scalp & Hair Blog: Afro Hair Care, Hair Growth Tips | Scalpx",
     "Practical scalp care and hair growth guidance for afro, curly and straight hair from the Scalpx journal.", blog)

# ---------------------------------------------------------------- LOGIN
login = f'''
<div class="auth">
 <aside class="auth-side"><img src="img/glow.webp" alt="">
  <a class="logo" href="index.html" style="color:#fff">{LOGO}<div>Scalpx</div></a>
  <div><h2>Your scalp journey, all in one place.</h2><p style="opacity:.8;margin-top:14px;max-width:380px">Track consultations, follow your personalised routine and keep your progress in sync.</p></div>
  <div class="glass-dark" style="padding:16px 20px;border-radius:22px;max-width:320px;font-size:13px">“Healthier hair starts at the scalp.”<br><span style="opacity:.6">The Scalpx philosophy</span></div></aside>
 <div class="auth-main"><div class="auth-card">
  <div class="tabs" role="tablist"><i></i><button type="button" data-m="in" class="on">Sign in</button><button type="button" data-m="reg">Create account</button></div>
  <h1 id="atitle">Welcome back</h1><p class="sub" id="asub"></p>
  <div id="amsg" class="formmsg" role="status"></div>
  <form id="authform" novalidate>
   <div class="field" data-only="reg"><label for="name">Full name</label><input id="name" name="name" autocomplete="name"><span class="err"></span></div>
   <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" placeholder="you@email.com"><span class="err"></span></div>
   <div class="field"><label for="password">Password</label><div class="pw"><input id="password" name="password" type="password" autocomplete="current-password" placeholder="At least 8 characters"><button type="button">Show</button></div><span class="err"></span></div>
   <div data-only="in" style="text-align:right;margin:-6px 0 16px"><a href="#" id="forgot" style="font-size:13px;color:var(--mute)">Forgot password?</a></div>
   <button id="submit" class="btn btn-dark" style="width:100%;justify-content:space-between" type="submit"><span>Sign in</span><i>{ARROW}</i></button>
  </form>
  <p style="font-size:12px;color:var(--mute);margin-top:22px">Demo mode: accounts are stored only in this browser. Connect a backend (e.g. Supabase) before taking real sign-ups.</p>
 </div></div>
</div>'''
page("login.html", "Log in or Create Account | Scalpx", "Sign in to your Scalpx account to manage consultations and your scalp care routine.", login, active="login.html", shell=False)
# login uses a lightweight shell (no nav) but keep a back link via logo.

# ---------------------------------------------------------------- DASHBOARD
dash = f'''
<section class="dash" id="dash"><div class="wrap">
 <span class="eyebrow">Your dashboard</span>
 <h1 style="font-size:clamp(40px,6vw,88px);margin:14px 0 4px">Hello, <span class="acc" data-name></span>.</h1>
 <p style="color:var(--mute)" data-email></p>
 <div class="dgrid">
  <div class="panel"><h3>Consultations</h3><div id="bookings"></div><a class="btn btn-dark btn-sm" style="margin-top:20px" href="book.html">Book a consultation <i>{ARROW}</i></a></div>
  <div class="panel dk"><h3>Your daily routine</h3><p id="prog" style="color:var(--acc);font-weight:600;margin:-6px 0 8px"></p>
   <label class="chk"><input type="checkbox" name="a"><span>Gentle scalp massage, 2 min</span></label>
   <label class="chk"><input type="checkbox" name="b"><span>Apply serum with dropper</span></label>
   <label class="chk"><input type="checkbox" name="c"><span>Drink 2L of water</span></label>
   <label class="chk"><input type="checkbox" name="d"><span>Protect scalp from tension</span></label>
  </div>
 </div>
 <button id="signout" class="btn btn-line" style="margin-top:28px">Sign out <i>{ARROW}</i></button>
</div></section>'''
page("dashboard.html", "Your Dashboard | Scalpx", "Manage your Scalpx consultations and daily scalp routine.", dash, active="dashboard.html")

# ---------------------------------------------------------------- BOOK
book = f'''
<section class="page-hero" style="padding-bottom:30px"><div class="wrap"><span class="eyebrow">Book consultation</span><h1>Let’s look at<br><span class="dim">your scalp.</span></h1></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap split" style="align-items:start">
 <div id="bookwrap"><form id="bookform" novalidate class="panel" style="padding:34px">
  <div class="two"><div class="field"><label for="n">Full name</label><input id="n" name="name" autocomplete="name"><span class="err"></span></div>
  <div class="field"><label for="e">Email</label><input id="e" name="email" type="email" autocomplete="email"><span class="err"></span></div></div>
  <div class="field"><label for="c">What would you like help with?</label><select id="c" name="concern"><option>Scalp analysis</option><option>Hair thinning / growth</option><option>Dandruff &amp; itch</option><option>Textured hair care</option><option>Scalp detox</option></select></div>
  <div class="two"><div class="field"><label for="d">Preferred date</label><input id="d" name="date" type="date"><span class="err"></span></div>
  <div class="field"><label for="t">Time</label><select id="t" name="time"><option>Morning</option><option>Afternoon</option><option>Evening</option></select></div></div>
  <div class="field"><label for="m">Notes (optional)</label><textarea id="m" name="notes" rows="3"></textarea></div>
  <button class="btn btn-acc" style="width:100%;justify-content:space-between" type="submit"><span>Request consultation</span><i>{ARROW}</i></button></form></div>
 <div id="booked" class="panel dk" style="display:none;padding:40px"><span class="eyebrow" style="color:#bbb">Request received</span><h2 style="margin:14px 0">You’re on the list.</h2><p id="bookedmsg" style="color:#bbb;margin-bottom:24px"></p><a class="btn btn-acc" href="index.html">Back home <i>{ARROW}</i></a></div>
 <div class="pic ratio-45 rvx" style="position:sticky;top:110px"><img src="img/helix.webp" alt=""></div>
</div></section>'''
page("book.html", "Book a Scalp Consultation | Scalpx", "Book your Scalpx consultation for scalp analysis, hair growth, dandruff or textured hair care.", book, active="book.html")

# ---------------------------------------------------------------- static extras
open(os.path.join(OUT, "favicon.svg"), "w").write(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" '))
pages = ["index", "about", "treatments", "results", "blog", "login", "book"]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}/{p}.html</loc></url>" for p in pages) + "</urlset>")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /dashboard.html\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(os.listdir(OUT)), "entries")
