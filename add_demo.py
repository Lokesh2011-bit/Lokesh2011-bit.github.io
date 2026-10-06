"""Adds a "Dashboard demo" section (video, screenshots, live link) to index.html.

Usage (in Terminal, from your portfolio folder):
    python3 add_demo.py

Fill in the three settings below first. Safe to re-run: it replaces its own section.
"""
import re, sys

# ---- SETTINGS ----------------------------------------------------------
YOUTUBE_ID = "LXvA4tBJYKg"      # e.g. "dQw4w9WgXcQ" from youtube.com/watch?v=dQw4w9WgXcQ (unlisted video)
DASHBOARD_URL = ""   # your live Streamlit dashboard address, or leave empty
SHOTS = [            # (file in the shots/ folder, caption)
    ("shots/overview.jpg", "Overview: traffic, anomaly scores and protocols on the held-out IoT-23 test set (21,533 flows, mostly attack traffic)."),
    ("shots/upload.jpg", "Upload and detect: a CSV is checked for format (IoT-23) before anomaly detection runs."),
]
# -------------------------------------------------------------------------

CSS = """
/*demo-css*/.demo-video{position:relative;padding-top:56.25%;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:24px;background:#000}
.demo-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-bottom:20px}
.shots figure{margin:0}.shots img{width:100%;height:auto;border:1px solid var(--line);border-radius:8px;display:block}
.shots a:focus-visible img,.shots a:hover img{outline:3px solid var(--accent);outline-offset:2px}
.shots figcaption{font-size:14px;color:var(--mute);margin-top:8px}
/*end-demo-css*/
"""

parts = ['<!--demo-start--><section id="demo"><div class="wrap"><h2>Dashboard demo</h2>']
if YOUTUBE_ID:
    parts.append('<div class="demo-video"><iframe src="https://www.youtube-nocookie.com/embed/%s" '
                 'title="PulseGuard dashboard walkthrough" loading="lazy" allowfullscreen></iframe></div>' % YOUTUBE_ID)
if SHOTS:
    parts.append('<div class="shots">')
    for f, cap in SHOTS:
        parts.append('<figure><a href="%s" target="_blank" rel="noopener"><img src="%s" alt="%s" loading="lazy"></a>'
                     '<figcaption>%s (click to enlarge)</figcaption></figure>' % (f, f, cap, cap))
    parts.append('</div>')
if DASHBOARD_URL:
    parts.append('<p><a class="btn p" href="%s" target="_blank" rel="noopener">Open the live dashboard</a></p>' % DASHBOARD_URL)
parts.append('</div></section><!--demo-end-->')
SECTION = "".join(parts)

html = open("index.html", encoding="utf-8").read()
html = re.sub(r"<!--demo-start-->.*?<!--demo-end-->", "", html, flags=re.S)
html = re.sub(r"/\*demo-css\*/.*?/\*end-demo-css\*/", "", html, flags=re.S)
if '<section id="projects">' not in html or "</style>" not in html:
    sys.exit("Could not find the expected spots in index.html. Is this the right file?")
html = html.replace("</style>", CSS + "</style>", 1)
m = re.search(r'</section>\s*<section id="skills"', html)
if not m:
    sys.exit("Could not find where to insert the demo section.")
html = html[:m.start()] + "</section>\n" + SECTION + "\n\n" + '<section id="skills"' + html[m.end():]
if 'href="#demo"' not in html:
    html = html.replace('<a href="#skills">', '<a href="#demo">Demo</a><a href="#skills">', 1)
open("index.html", "w", encoding="utf-8").write(html)
print("Done. Demo section added.")
