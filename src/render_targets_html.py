"""Render docs/targets_2026.html (standalone) and an artifact fragment from target_cards.parquet + target_fams.parquet."""
import json, numpy as np, pandas as pd, sys, os
ASOF=int(os.environ.get('ASOF','2026')); SUF='' if ASOF==2026 else f'_asof{ASOF}'
d=pd.read_parquet(f'data/derived/target_cards{SUF}.parquet'); d=d[d.game_year==ASOF].copy()
L=pd.read_parquet(f'data/derived/target_fams{SUF}.parquet'); L=L[L.game_year==ASOF]
pool='n_precedent_pool'
def f(x,nd=0):
    return None if x is None or (isinstance(x,float) and not np.isfinite(x)) else round(float(x),nd)
rows=[]
for _,r in d.iterrows():
    fams=L[L.pitcher==r.pitcher].sort_values('ev',ascending=False)
    rows.append(dict(name=r.PlayerName,team=r.Team if isinstance(r.Team,str) else '',age=f(r.Age),role=r.role,ip=f(r.IP),slot=f(r.arm_angle),eff4=f(r.eff4,2),
        cls=r.suppro_class if isinstance(r.suppro_class,str) else 'unknown',stuff=f(r.stuff),own=f(r.stuff_B_plus_oos),loc=f(r.sp_location),pit=f(r.sp_pitching),
        best=r.best_add,bpstf=f(r.best_add_pstf),bprec=f(r.best_add_prec,2),bp=f(r.best_add_padd,2),gain=f(r.gain,1),ev=f(r.sum_ev,2),reach=f(r.n_reachable),
        pool=f(r[pool]),drop=int(r.drop_recipe),proj=f(r.proj_stuff),dpit=f(r.d_pit,1),dwar=f(r.d_war,2),dm=f(r.d_dollars_M,1),era=f(r.ERA,2),xera=f(r.xERA,2),bb=f(r['BB%']*100,1) if pd.notna(r['BB%']) else None,k=f(r['K%']*100,1) if pd.notna(r['K%']) else None,
        fams=[dict(fam=x.fam,prec=f(x.prec,2),pstf=f(x.pstf),p=f(x.p_add,2),gain=f(x.gain,1),ev=f(x.ev,2),reach=bool(x.reach)) for _,x in fams.iterrows()]))
data=json.dumps(rows,separators=(',',':'))
n=len(rows)
CSS="""
:root{--paper:#EEF1F4;--panel:#FFFFFF;--ink:#14202B;--muted:#5B6B78;--line:#D5DCE2;--accent:#0F6E68;--accent-ink:#0B4F4B;--flag:#B9741A;--flag-bg:#F6ECD9;--gain:#1B7F5A;--loss:#A83A2E;--gain-bg:#DDF0E7;--hover:#E5EBEF;--chip:#E3E9ED;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#0F1519;--panel:#161D23;--ink:#E4E9EE;--muted:#93A2AE;--line:#2A343D;--accent:#3FB3AA;--accent-ink:#8FE0D8;--flag:#E0A54D;--flag-bg:#3A2E18;--gain:#4FC08D;--loss:#E07A6A;--gain-bg:#173428;--hover:#1D262E;--chip:#232D36;}}
:root[data-theme="dark"]{--paper:#0F1519;--panel:#161D23;--ink:#E4E9EE;--muted:#93A2AE;--line:#2A343D;--accent:#3FB3AA;--accent-ink:#8FE0D8;--flag:#E0A54D;--flag-bg:#3A2E18;--gain:#4FC08D;--loss:#E07A6A;--gain-bg:#173428;--hover:#1D262E;--chip:#232D36;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,sans-serif;font-size:14px;line-height:1.5}
.wrap{max-width:1380px;margin:0 auto;padding:28px 24px 60px}
h1,h2,h3,.disp{font-family:"Barlow Condensed","Arial Narrow",Impact,sans-serif;text-wrap:balance;letter-spacing:.01em}
h1{font-size:44px;font-weight:600;line-height:1;margin:0 0 6px}
h2{font-size:24px;font-weight:600;margin:34px 0 10px}
.sub{color:var(--muted);max-width:72ch;margin:0}
.eyebrow{font-family:"Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:var(--accent);font-weight:600}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:22px 0 8px}
.stat{background:var(--panel);border:1px solid var(--line);padding:14px 16px}
.stat .v{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:26px;font-weight:500;font-variant-numeric:tabular-nums;color:var(--accent-ink)}
.stat .l{font-size:12px;color:var(--muted);margin-top:2px}
.method{background:var(--panel);border:1px solid var(--line);padding:14px 18px;margin-top:14px;max-width:none}
.method p{margin:6px 0;max-width:110ch}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:18px 0 10px}
.controls input,.controls select{font:inherit;padding:7px 10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:2px}
.controls input:focus,.controls select:focus,button:focus,tr.row:focus{outline:2px solid var(--accent);outline-offset:1px}
.controls .n{color:var(--muted);margin-left:auto;font-variant-numeric:tabular-nums}
.tbl{overflow-x:auto;border:1px solid var(--line);background:var(--panel)}
table{border-collapse:collapse;width:100%;min-width:1180px}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}
th{position:sticky;top:0;background:var(--panel);z-index:1;font-family:"Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.08em;font-size:12px;font-weight:600;color:var(--muted);cursor:pointer;user-select:none}
th.sorted{color:var(--accent-ink)}
th:first-child,td:first-child,th.l,td.l{text-align:left}
td{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:13px}
td.l{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:14px}
tr.row{cursor:pointer}tr.row:hover{background:var(--hover)}
tr.detail td{background:var(--paper);white-space:normal;font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:13px}
.chip{display:inline-block;padding:1px 7px;border-radius:2px;background:var(--chip);font-family:"IBM Plex Sans",sans-serif;font-size:11px;letter-spacing:.04em;text-transform:uppercase}
.chip.P{background:var(--gain-bg);color:var(--gain)}.chip.S{background:var(--flag-bg);color:var(--flag)}
.flag{display:inline-block;width:9px;height:9px;background:var(--flag);border-radius:50%;vertical-align:middle;margin-left:4px}
.pos{color:var(--gain);font-weight:500}.neg{color:var(--loss)}
.bar{display:inline-block;height:8px;background:var(--accent);vertical-align:middle;margin-right:6px;opacity:.85}
.fams{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:8px 0 4px}
.fam{border:1px solid var(--line);background:var(--panel);padding:8px 10px}
.fam .h{font-family:"Barlow Condensed",sans-serif;font-size:16px;font-weight:600;letter-spacing:.04em}
.fam .m{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted)}
.fam.reach{border-color:var(--accent)}
.fam.off{opacity:.55}
.checks{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.check{background:var(--panel);border:1px solid var(--line);padding:14px 16px}
.check .h{font-family:"Barlow Condensed",sans-serif;font-size:20px;font-weight:600}
.foot{color:var(--muted);font-size:12px;margin-top:30px;max-width:90ch}
.legend{color:var(--muted);font-size:12px;margin:8px 0 0}
@media (prefers-reduced-motion: no-preference){tr.row{transition:background .12s}}
"""
JS=r"""
const D=__DATA__;const FAMN={FF:'4-seam',SI:'sinker',FC:'cutter',FS:'splitter',SL:'slider/sweeper',CU:'curve',KC:'knuckle-curve',CH:'changeup'};
const CLSG={pronator:'P',lean_pronator:'P',supinator:'S',lean_supinator:'S',hybrid:'H',unknown:'H'};
let sortKey='ev',sortDir=-1,filt={q:'',role:'',cls:'',reach:false,drop:false};
const cols=[['name','Pitcher','l'],['team','Tm','l'],['age','Age'],['role','Role','l'],['ip','IP'],['slot','Slot°'],['eff4','4S eff'],['cls','Class','l'],['stuff','Stuff+'],['own','Own'],['loc','Loc+'],['pit','Pit+'],['best','Best add','l'],['bpstf','Prec Stf+'],['bprec','Share'],['bp','P(add)'],['gain','Gain'],['ev','ΣEV'],['reach','Reach'],['pool','Pool'],['proj','Proj Stf+'],['dwar','ΔWAR'],['dm','Δ$M']];
function fmt(v,k){if(v===null||v===undefined)return '<span style="color:var(--muted)">·</span>';if(k==='cls'){const g=CLSG[v]||'H';return `<span class="chip ${g}">${v.replace('_',' ')}</span>`}
 if(k==='gain'||k==='dwar'||k==='dm'){const s=(v>0?'+':'')+v.toFixed(k==='gain'?1:k==='dwar'?2:1);return v>0?`<span class="pos">${s}</span>`:v<0?`<span class="neg">${s}</span>`:s}
 if(k==='ev'){return `<span class="bar" style="width:${Math.min(60,v*40)}px"></span>${v.toFixed(2)}`}
 if(k==='eff4'||k==='bprec'||k==='bp')return v.toFixed(2);if(k==='name')return v;return typeof v==='number'?v:v}
function render(){const tb=document.getElementById('tb');const q=filt.q.toLowerCase();
 let rows=D.filter(r=>(!q||r.name.toLowerCase().includes(q)||(r.team||'').toLowerCase().includes(q))&&(!filt.role||r.role===filt.role)&&(!filt.cls||CLSG[r.cls]===filt.cls)&&(!filt.reach||r.reach>0)&&(!filt.drop||r.drop===1));
 rows.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];if(x===null||x===undefined)x=-1e9*sortDir;if(y===null||y===undefined)y=-1e9*sortDir;if(typeof x==='string')return sortDir*x.localeCompare(y);return sortDir*(x-y)});
 document.getElementById('cnt').textContent=rows.length+' of '+D.length+' pitchers';
 tb.innerHTML=rows.map((r,i)=>`<tr class="row" tabindex="0" data-i="${D.indexOf(r)}"><td class="l" style="color:var(--muted)">${i+1}</td>`+cols.map(([k,,c])=>`<td class="${c||''}">${fmt(r[k],k)}${k==='slot'&&r.drop?'<span class="flag" title="Driveline drop recipe: below-avg IVB, eff≥.93"></span>':''}</td>`).join('')+'</tr>').join('');
 document.querySelectorAll('th[data-k]').forEach(th=>th.classList.toggle('sorted',th.dataset.k===sortKey));}
function detail(r){const fams=r.fams.map(x=>`<div class="fam ${x.reach?'reach':'off'}"><div class="h">${x.fam} <span style="font-weight:400;color:var(--muted)">${FAMN[x.fam]}</span></div><div class="m">prec Stf+ ${x.pstf??'·'} · share ${x.prec??'·'} · P(add) ${x.p??'·'}</div><div class="m">gain ${x.gain>0?'+'+x.gain:'0'} · EV ${x.ev??0}</div></div>`).join('');
 return `<td colspan="${cols.length+1}"><div><strong>${r.name}</strong> — ${r.role}, ${r.ip} IP, ERA ${r.era??'·'} / xERA ${r.xera??'·'}, K% ${r.k??'·'} · BB% ${r.bb??'·'} · slot ${r.slot}°, 4S efficiency ${r.eff4}, ${r.cls.replace('_',' ')}, precedent pool ${r.pool} same-hand pitcher-seasons within ±5°/similar VAA${r.drop?' · <span style="color:var(--flag)">drop-recipe profile</span>':''}.<br>Families not thrown (&lt;2%). Outlined = reachable (≥20% of sup/pro-compatible comps throw it ≥10%). Gain = 0.14 × (precedent Stf+ − ${r.stuff})⁺; EV = P(add) × gain.</div><div class="fams">${fams||'<em>No unthrown families with precedent data.</em>'}</div><div class="legend">Projected Stuff+ ${r.proj} → ΔPit+ ${r.dpit>0?'+':''}${r.dpit} → ΔWAR ${r.dwar>0?'+':''}${r.dwar} at ${r.ip} IP (${r.role} rate) → ${r.dm>0?'+':''}$${r.dm}M at $8M/WAR. Conditional on the add happening; not a forecast.</div></td>`}
document.getElementById('tb').addEventListener('click',e=>{const tr=e.target.closest('tr.row');if(!tr)return;const nx=tr.nextElementSibling;if(nx&&nx.classList.contains('detail')){nx.remove();return}const r=D[+tr.dataset.i];const d=document.createElement('tr');d.className='detail';d.innerHTML=detail(r);tr.after(d)});
document.getElementById('tb').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.classList.contains('row'))e.target.click()});
document.querySelectorAll('th[data-k]').forEach(th=>th.addEventListener('click',()=>{const k=th.dataset.k;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=['name','team','role','cls','best'].includes(k)?1:-1}render()}));
document.getElementById('q').addEventListener('input',e=>{filt.q=e.target.value;render()});
document.getElementById('role').addEventListener('change',e=>{filt.role=e.target.value;render()});
document.getElementById('cls').addEventListener('change',e=>{filt.cls=e.target.value;render()});
document.getElementById('reach').addEventListener('change',e=>{filt.reach=e.target.checked;render()});
document.getElementById('drop').addEventListener('change',e=>{filt.drop=e.target.checked;render()});
render();
"""
ths=''.join(f'<th data-k="{k}" class="{c if len(x)>2 else ""}">{lab}</th>' for x in [['name','Pitcher','l'],['team','Tm','l'],['age','Age'],['role','Role','l'],['ip','IP'],['slot','Slot°'],['eff4','4S eff'],['cls','Class','l'],['stuff','Stuff+'],['own','Own'],['loc','Loc+'],['pit','Pit+'],['best','Best add','l'],['bpstf','Prec Stf+'],['bprec','Share'],['bp','P(add)'],['gain','Gain'],['ev','ΣEV'],['reach','Reach'],['pool','Pool'],['proj','Proj Stf+'],['dwar','ΔWAR'],['dm','Δ$M']] for k,lab,*c in [x] for c in [c[0] if c else ''])
def check(nm):
    r=d[d.PlayerName.str.contains(nm,na=False)]
    if not len(r): return ''
    r=r.iloc[0]; ba=r.best_add if isinstance(r.best_add,str) else '—'
    return f'<div class="check"><div class="h">{r.PlayerName} <span style="color:var(--muted);font-weight:400">{r.Team} · {r.role}</span></div><div>Slot {r.arm_angle:.0f}°, 4S efficiency {r.eff4:.2f}, {str(r.suppro_class).replace("_"," ")}. Stuff+ {r.stuff:.0f} (own {r.stuff_B_plus_oos:.0f}), Loc+ {r.sp_location:.0f}.</div><div style="margin-top:6px">Reachable roles {r.n_reachable:.0f}; best add {ba}{"" if ba=="—" else f" (prec Stf+ {r.best_add_pstf:.0f}, share {r.best_add_prec:.2f}, P {r.best_add_padd:.2f})"}; gain <span class="{ "pos" if r.gain>0 else ""}">{r.gain:+.1f}</span>; pool n={r[pool]:.0f}.</div></div>'
checks=''.join(check(n) for n in ['Yesavage','Palmquist','Hancock'])
head=f"""<title>Reachable Arsenal Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>"""
body=f"""<div class="wrap">
<div class="eyebrow">MLB pitchers · {ASOF} through Aug 16 · {n} with ≥300 pitches</div>
<h1>Reachable Arsenal Board</h1>
<p class="sub">What each pitcher could add from his current arm slot, what precedent says it would grade, and what that is worth. Sort any column; click a row for every family and the math.</p>
<div class="stats">
<div class="stat"><div class="v">.785</div><div class="l">P(add) grouped-OOF AUC, calibrated by decile</div></div>
<div class="stat"><div class="v">r ≈ .5</div><div class="l">precedent grade of an added pitch vs its realized Stf+</div></div>
<div class="stat"><div class="v">+2.7</div><div class="l">2026 Stuff+ gain of the as-of-2025 EV top-40 vs matched controls (n=19)</div></div>
<div class="stat"><div class="v">≈ 0</div><div class="l">forward signal of possible-gain across all pitchers beyond mean reversion</div></div>
</div>
<div class="method">
<p><strong>Method.</strong> For each family a pitcher throws under 2%, precedent is the same-hand, supination/pronation-compatible pitchers in his trait neighborhood (arm angle, height-adjusted VAA, release height, velo, spin, 4-seam efficiency, axis residual). Reachable if at least 20% of them throw it at 10%+. Gain = 0.14 usage × (precedent Stf+ − current Stuff+)⁺. P(add) comes from a grouped-CV model over every pitcher-season × unthrown family. EV = P(add) × gain, summed. Value: Pit+ = −74.8 + .85·Stf+ + .90·Loc+; ΔWAR = .098 (SP) / .074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR.</p>
<p><strong>Read it as reachability with a conditional price, not a forecast.</strong> Backtest 2020–25: possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after mean reversion. Slot change is a feasibility flag only (<span class="flag"></span> = below-average four-seam ride with efficiency ≥.93 — the profile that gained on dropping in Driveline's data and ours); no slot gain is projected. <em>Own</em> = our run-value Stuff model (XGBoost, physical features only, scored on unseen pitchers).</p>
</div>
<div class="controls"><input id="q" type="search" placeholder="Search pitcher or team" aria-label="Search">
<select id="role" aria-label="Role"><option value="">All roles</option><option>SP</option><option>RP</option></select>
<select id="cls" aria-label="Class"><option value="">All classes</option><option value="P">Pronator-leaning</option><option value="S">Supinator-leaning</option><option value="H">Hybrid / unknown</option></select>
<label><input id="reach" type="checkbox"> reachable add only</label>
<label><input id="drop" type="checkbox"> drop-recipe profile</label>
<span class="n" id="cnt"></span></div>
<div class="tbl"><table><thead><tr><th class="l">#</th>{ths}</tr></thead><tbody id="tb"></tbody></table></div>
<p class="legend">Stuff+/Loc+/Pit+ = FanGraphs. Own = our model. Prec Stf+ = usage-weighted FG Stf+ of comps on that family. Share = fraction of comps throwing it 10%+. Pool = same-hand pitcher-seasons within ±5° and similar VAA (thin pools mean thin precedent).</p>
<h2>Named checks</h2>
<div class="checks">{checks}</div>
<h2>Was it findable a year early?</h2>
<p class="sub" style="max-width:100ch">Rebuilt strictly as of end-2025 (precedent and P(add) restricted to ≤2025 data): the EV top-40 gained +2.7 Stuff+ in 2026 vs −0.1 for stuff-matched controls; the raw-gain top-40 +2.2. Hancock ranked #1 by raw gain (card said curve; he dropped 8° and added a sweeper/cutter instead). Palmquist was not findable — his gain came from turning a running four-seam into a real sinker, which this lever does not model. Dollander (#2), Senzatela (#7), Sasaki (#36) were on the list.</p>
<p class="foot">Data: Statcast 2020–2026 (Chamberlain Pitch Leaderboard v8 extract + pybaseball backfill), Baseball Savant spin-direction leaderboard, FanGraphs Stuff+/Location+/Pitching+ and standard leaderboards. Code and derived tables: github.com/vincepipitone/baseball-slot-sim.</p>
</div>
<script>{JS.replace('__DATA__',data)}</script>"""
frag=head+body
open(f'docs/targets_{ASOF}.html','w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+head+'</head><body>'+body+'</body></html>')
os.makedirs('/Users/vincepipitone/.claude/jobs/aa656eb5/tmp',exist_ok=True)
open('/Users/vincepipitone/.claude/jobs/aa656eb5/tmp/reachable-arsenal-board.html','w').write(frag)
print('wrote', len(frag)//1024,'KB', n,'rows')
