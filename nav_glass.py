"""Turns the top menu into a frosted-glass side panel (desktop) with a highlight that follows your scroll.
Run from ~/portfolio:   python3 nav_glass.py      Safe to re-run. To undo: python3 nav_glass.py --remove
"""
import re, sys

CSS = """/*glass-nav-css*/
:root{--glass:rgba(255,255,255,.58);--glass-line:rgba(26,36,51,.12);--glow:rgba(29,78,216,.22)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--glass:rgba(22,30,44,.55);--glass-line:rgba(255,255,255,.14);--glow:rgba(107,155,255,.28)}}
:root[data-theme="dark"]{--glass:rgba(22,30,44,.55);--glass-line:rgba(255,255,255,.14);--glow:rgba(107,155,255,.28)}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(420px 420px at 6% 18%,var(--glow),transparent 70%),radial-gradient(380px 380px at 4% 82%,var(--glow),transparent 70%)}
header.top{-webkit-backdrop-filter:blur(16px) saturate(160%);backdrop-filter:blur(16px) saturate(160%);background:var(--glass)}
nav a{padding:6px 10px;border-radius:8px;border-left:3px solid transparent}
nav a[aria-current="true"]{color:var(--ink);background:var(--glow);border-left-color:var(--accent)}
@media(prefers-reduced-motion:no-preference){nav a{transition:background .25s,color .25s,border-color .25s}}
@media (min-width:1000px){
body{padding-left:244px}
header.top{position:fixed;left:14px;top:14px;bottom:14px;width:208px;height:auto;border:1px solid var(--glass-line);border-radius:18px;box-shadow:0 10px 40px rgba(0,0,0,.12)}
header.top .wrap{height:100%;max-width:none;padding:26px 14px;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:26px}
.brand{font-size:17px;line-height:1.25;padding:0 10px}
nav{flex-direction:column;gap:4px;width:100%;overflow:visible;font-size:15px}
nav a{display:block}
}
/*end-glass-nav-css*/"""

JS = """<!--glass-nav-js--><script>(function(){var L=document.querySelectorAll('nav[aria-label="Sections"] a[href^="#"]');if(!L.length||!("IntersectionObserver" in window))return;
var m={};L.forEach(function(a){var s=document.querySelector(a.getAttribute("href"));if(s)m[s.id]=a;});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){L.forEach(function(a){a.removeAttribute("aria-current");});m[e.target.id].setAttribute("aria-current","true");}});},{rootMargin:"-40% 0px -55% 0px"});
Object.keys(m).forEach(function(id){io.observe(document.getElementById(id));});})();</script><!--end-glass-nav-js-->"""

html = open("index.html", encoding="utf-8").read()
html = re.sub(r"/\*glass-nav-css\*/.*?/\*end-glass-nav-css\*/", "", html, flags=re.S)
html = re.sub(r"<!--glass-nav-js-->.*?<!--end-glass-nav-js-->", "", html, flags=re.S)
if "--remove" not in sys.argv:
    if "</style>" not in html or "</body>" not in html:
        sys.exit("Could not find the expected spots in index.html. Are you in the portfolio folder?")
    html = html.replace("</style>", CSS + "\n</style>", 1)
    html = html.replace("</body>", JS + "\n</body>", 1)
open("index.html", "w", encoding="utf-8").write(html)
print("Removed glass menu." if "--remove" in sys.argv else "Done. Glass side menu added.")
