"""Adds the interactive "Try the ensemble" widget to the end of the Dashboard demo section.

Run from ~/portfolio:   python3 add_widget.py        Safe to re-run.  To undo: python3 add_widget.py --remove
NOTE: if you ever re-run add_demo.py it rebuilds the demo section and removes this widget,
so run add_widget.py again afterwards.
"""
import re, sys

ANCHOR = "</div></section><!--demo-end-->"

CSS = r"""/*ens-css*/
.ens{border:1px solid var(--line);border-radius:10px;padding:24px;background:var(--alt);margin-top:24px}
.ens h3{margin:0 0 4px}
.ens .note{font-size:14px;color:var(--mute);margin:0 0 16px;max-width:68ch}
.ens .row{display:flex;gap:10px 14px;flex-wrap:wrap;align-items:center;margin:10px 0}
.ens .lab{font-size:13px;font-weight:600;color:var(--mute);min-width:110px}
.ens .grp{display:inline-flex;gap:10px;flex-wrap:wrap}
.ens button{font:inherit;font-size:14px;font-weight:600;padding:8px 14px;border-radius:6px;border:1px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer}
.ens button:hover{border-color:var(--accent)}
.ens button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.ens button[aria-pressed="true"]{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.ens button[aria-pressed="true"]::before{content:"\2713\00a0"}
.ens .out{margin:16px 0 0;padding:12px 14px;border-radius:8px;border:1px solid var(--line);border-left-width:5px;background:var(--bg);max-width:68ch}
.ens .out.alert{border-left-color:#b42318}
.ens .out.clear{border-left-color:#067647}
.ens .out strong{display:block;margin-bottom:2px}
/*end-ens-css*/"""

HTML = r"""<!--ens-start--><div class="ens" id="ens"><h3>Try the ensemble</h3>
<p class="note">Choose what each model says about one network flow, then switch the decision rule. This illustrates the voting logic only; it is not live model output.</p>
<div class="row"><span class="lab" id="ens-l1">Random Forest says</span><span class="grp" role="group" aria-labelledby="ens-l1"><button type="button" data-m="rf" data-v="1" aria-pressed="true">Malicious</button><button type="button" data-m="rf" data-v="0" aria-pressed="false">Benign</button></span></div>
<div class="row"><span class="lab" id="ens-l2">XGBoost says</span><span class="grp" role="group" aria-labelledby="ens-l2"><button type="button" data-m="xgb" data-v="1" aria-pressed="false">Malicious</button><button type="button" data-m="xgb" data-v="0" aria-pressed="true">Benign</button></span></div>
<div class="row"><span class="lab" id="ens-l3">Decision rule</span><span class="grp" role="group" aria-labelledby="ens-l3"><button type="button" data-rule="and" aria-pressed="true">Both must agree (dashboard)</button><button type="button" data-rule="or" aria-pressed="false">Either can flag</button></span></div>
<p class="out" id="ens-out" role="status" aria-live="polite"></p></div>
<script>(function(){var root=document.getElementById("ens");if(!root)return;
var s={rf:1,xgb:0,rule:"and"},out=document.getElementById("ens-out");
function render(){var a=s.rf===1,b=s.xgb===1,hit=s.rule==="and"?(a&&b):(a||b),t,d;
if(hit){t="Alert: flow flagged as malicious";d=s.rule==="and"?"Both models agree, so the ensemble raises an alert.":(a&&b?"Both models flagged it.":"One model flagged it, and this looser rule is enough to raise an alert.");}
else{t="No alert: flow treated as benign";d=(!a&&!b)?"Neither model flagged it.":"The models disagree, so the stricter rule stays quiet. That cuts false alarms but can miss some attacks.";}
out.className="out "+(hit?"alert":"clear");out.innerHTML="<strong></strong><span></span>";out.firstChild.textContent=t;out.lastChild.textContent=d;
root.querySelectorAll("button").forEach(function(x){var on=x.dataset.m?(s[x.dataset.m]===+x.dataset.v):(s.rule===x.dataset.rule);x.setAttribute("aria-pressed",on?"true":"false");});}
root.addEventListener("click",function(e){var x=e.target.closest("button");if(!x||!root.contains(x))return;
if(x.dataset.m){s[x.dataset.m]=+x.dataset.v;}else if(x.dataset.rule){s.rule=x.dataset.rule;}render();});
render();})();</script><!--ens-end-->"""

html = open("index.html", encoding="utf-8").read()
html = re.sub(r"/\*ens-css\*/.*?/\*end-ens-css\*/\n?", "", html, flags=re.S)
html = re.sub(r"<!--ens-start-->.*?<!--ens-end-->", "", html, flags=re.S)

if "--remove" not in sys.argv:
    if ANCHOR not in html:
        sys.exit("Could not find the end of the Dashboard demo section in index.html. Are you in the portfolio folder?")
    if "</style>" not in html:
        sys.exit("Could not find </style> in index.html.")
    html = html.replace(ANCHOR, HTML + ANCHOR, 1)
    html = html.replace("</style>", CSS + "\n</style>", 1)

open("index.html", "w", encoding="utf-8").write(html)
print("Removed ensemble widget." if "--remove" in sys.argv else "Done. Ensemble widget added.")
