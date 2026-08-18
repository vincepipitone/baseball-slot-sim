"""Render docs/targets_2026.html (standalone) and an artifact fragment. Both years embedded (2026 today; 2025 with realized)."""
import json, numpy as np, pandas as pd, sys, os
pool='n_precedent_pool'
def f(x,nd=0):
    try:
        if x is None or (isinstance(x,float) and not np.isfinite(x)) or pd.isna(x): return None
    except Exception: pass
    return round(float(x),nd)
def build_rows(year):
    suf='' if year==2026 else f'_asof{year}'
    d=pd.read_parquet(f'data/derived/target_cards{suf}.parquet'); d=d[d.game_year==year].copy()
    L=pd.read_parquet(f'data/derived/target_fams{suf}.parquet'); L=L[L.game_year==year]
    dev=pd.read_parquet('data/derived/dev_all_2026.parquet' if year==2026 else 'data/derived/dev_all_2025.parquet')[['pitcher','pred','pred_cal','pp_stf','pp_use','fb_liability']]
    cpm=pd.read_parquet('data/derived/cpm_2026.parquet' if year==2026 else 'data/derived/cpm_test2025.parquet')[['pitcher','z_dev','z_act','cpm']]
    d=d.merge(dev,on='pitcher',how='left').merge(cpm,on='pitcher',how='left')
    import json as _j; CAL=_j.load(open('data/derived/dev_calibration.json'))
    _t=pd.read_parquet('data/derived/emulator_table.parquet'); _t=_t[(_t.game_year==year)&(_t.n>=40)]
    _raw=_t.sort_values('stf',ascending=False).drop_duplicates('pitcher')[['pitcher','fg_type','stf','usage']].rename(columns={'fg_type':'pp_fam','stf':'pp_raw','usage':'pp_raw_use'})
    d=d.merge(_raw,on='pitcher',how='left')
    if year<2026:
        fg=pd.read_csv('data/derived/fg_stuff.csv').drop_duplicates(['pitcher','game_year']); nx=fg[fg.game_year==year+1][['pitcher','sp_stuff','sp_pitching','sp_location']].rename(columns={'sp_stuff':'stuff_n','sp_pitching':'pit_n','sp_location':'loc_n'})
        d=d.merge(nx,on='pitcher',how='left'); d['d_stuff']=d.stuff_n-d.stuff; d['d_pit']=d.pit_n-d.sp_pitching
    else: d['d_stuff']=np.nan; d['d_pit']=np.nan
    rows=[]
    for _,r in d.iterrows():
        fams=L[L.pitcher==r.pitcher].sort_values('ev',ascending=False)
        rows.append(dict(name=r.PlayerName,team=r.Team if isinstance(r.Team,str) else '',age=f(r.Age),role=r.role,ip=f(r.IP),slot=f(r.arm_angle),eff4=f(r.eff4,2),
            cls=r.suppro_class if isinstance(r.suppro_class,str) else 'unknown',stuff=f(r.stuff),loc=f(r.sp_location),pit=f(r.sp_pitching),
            gate=int(pd.notna(r.cpm)),cpm=f(r.cpm,2),dev=f(r.pred_cal,1) if pd.notna(r.pred_cal) else None,devraw=f(r.pred,1),zdev=f(r.z_dev,2),zact=f(r.z_act,2),ppstf=f(r.pp_stf),ppuse=f(r.pp_use*100) if pd.notna(r.pp_use) else None,ppfam=(r.pp_fam if isinstance(r.pp_fam,str) else ''),ppraw=f(r.pp_raw),fbliab=f(r.fb_liability,1),
            opp=f(r.opportunity,2),act=f(r.actionable,1),projact=f(r.proj_stuff_act),dropb=f(r.drop_bonus,1),addact=f(r.add_act,1),mixplan=(r.mix_plan if isinstance(r.mix_plan,str) else ''),merged=(r.merged if isinstance(r.merged,str) else ''),mixb=f(r.mix_pit,1),
            mix=f(r.gain_mix,1),gap=f(r.gain_gap,1),gapexp=f(0.2*r.gain_gap,1),gapp=(r.gap_parts if isinstance(r.gap_parts,str) else ''),coors=f(r.coors_adj,1),colshare=f(r.col_share,2) if pd.notna(r.col_share) else None,
            worst=f'{r.worst_fam} {r.worst_stf:.0f} @ {r.worst_use*100:.0f}%' if isinstance(r.worst_fam,str) else '',bestp=f'{r.best_fam} {r.best_stf:.0f} @ {r.best_use*100:.0f}%' if isinstance(r.best_fam,str) else '',
            best=r.best_add if isinstance(r.best_add,str) else '—',bpstf=f(r.best_add_pstf),bprec=f(r.best_add_prec,2),bp=f(r.best_add_padd,2),gain=f(r.gain,1),ev=f(r.sum_ev,2),reach=f(r.n_reachable),
            pool=f(r[pool]),drop=int(r.drop_recipe),proj=f(r.proj_stuff),dpit=f(r.d_pit_lever if 'd_pit_lever' in r else r.d_pit,1) if year==2026 else None,dwar=f(r.d_war,2),dm=f(r.d_dollars_M,1),era=f(r.ERA,2),xera=f(r.xERA,2),
            bb=f(r['BB%']*100,1) if pd.notna(r['BB%']) else None,k=f(r['K%']*100,1) if pd.notna(r['K%']) else None,
            rstf=f(r.d_stuff,1) if year<2026 else None,rpit=f(r.d_pit,1) if year<2026 else None,
            fams=[dict(fam=x.fam,prec=f(x.prec,2),pstf=f(x.pstf),p=f(x.p_add,2),gain=f(x.gain,1),ev=f(x.ev,2),reach=bool(x.reach)) for _,x in fams.iterrows()]))
    return rows,d
rows26,d=build_rows(2026); rows25,_=build_rows(2025)
data=json.dumps({'2026':rows26,'2025':rows25},separators=(',',':'))
n=len(rows26); n25=len(rows25); ASOF=2026
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
button.yr{font:inherit;padding:7px 12px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:2px;cursor:pointer}
button.yr[aria-pressed="true"]{background:var(--accent);color:#fff;border-color:var(--accent)}
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
const ALL=__DATA__;let YEAR='2026';let D=ALL[YEAR];const FAMN={FF:'4-seam',SI:'sinker',FC:'cutter',FS:'splitter',SL:'slider/sweeper',CU:'curve',KC:'knuckle-curve',CH:'changeup'};
const CLSG={pronator:'P',lean_pronator:'P',supinator:'S',lean_supinator:'S',hybrid:'H',unknown:'H'};
let sortKey='cpm',sortDir=-1,filt={q:'',role:'',cls:'',reach:false,drop:false,gate:true};
const COLS26=[['name','Pitcher','l'],['team','Tm','l'],['age','Age'],['role','Role','l'],['ip','IP'],['slot','Slot°'],['eff4','4S eff'],['cls','Class','l'],['stuff','Stuff+'],['loc','Loc+'],['pit','Pit+'],['ppstf','Plus pitch (raw→shrunk @ use)'],['dev','Dev ΔStf+ (cal.)'],['act','Actionable'],['cpm','CPM score'],['mixb','Mix'],['best','Best add','l'],['bpstf','Prec Stf+'],['addact','Add gain'],['dropb','Drop'],['projact','Proj Stf+'],['opp','Drift'],['gap','Gap vs comps → exp.'],['pool','Pool']];const COLS25=COLS26.concat([['rstf','ΔStf+ next'],['rpit','ΔPit+ next']]);let cols=COLS26;
function fmt(v,k){if(v===null||v===undefined)return '<span style="color:var(--muted)">·</span>';if(k==='cls'){const g=CLSG[v]||'H';return `<span class="chip ${g}">${v.replace('_',' ')}</span>`}
 if(k==='gain'||k==='dwar'||k==='dm'||k==='gap'||k==='mix'||k==='mixb'||k==='coors'){const s=(v>0?'+':'')+v.toFixed(k==='dwar'?2:1);return v>0?`<span class="pos">${s}</span>`:v<0?`<span class="neg">${s}</span>`:s}
 if(k==='cpm'){return `<span class="bar" style="width:${Math.max(0,Math.min(70,(v+1)*20))}px"></span>${v.toFixed(2)}`}if(k==='act')return v.toFixed(1);if(k==='gate')return v?'<span class="chip P">in</span>':'<span style="color:var(--muted)">·</span>';if(k==='ppstf'){const u=this&&this.ppuse;return v}if(k==='dev'||k==='rstf'||k==='rpit'){const s=(v>0?'+':'')+v.toFixed(1);return v>0?`<span class="pos">${s}</span>`:v<0?`<span class="neg">${s}</span>`:s}if(k==='opp')return v.toFixed(2);if(k==='dropb'||k==='addact')return v>0?`<span class="pos">+${v.toFixed(1)}</span>`:'0';if(k==='ev')return v.toFixed(2);
 if(k==='eff4'||k==='bprec'||k==='bp')return v.toFixed(2);if(k==='name')return v;return typeof v==='number'?v:v}
function header(){document.querySelector('thead tr').innerHTML='<th class="l">#</th>'+cols.map(([k,lab,c])=>`<th data-k="${k}" class="${c||''}">${lab}</th>`).join('');document.querySelectorAll('th[data-k]').forEach(th=>th.addEventListener('click',()=>{const k=th.dataset.k;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=['name','team','role','cls','best'].includes(k)?1:-1}render()}));}
function setYear(y){YEAR=y;D=ALL[y];cols=y==='2025'?COLS25:COLS26;header();document.querySelectorAll('button.yr').forEach(b=>b.setAttribute('aria-pressed',b.dataset.y===y?'true':'false'));document.getElementById('yrnote').textContent=y==='2025'?'As of end-2025: models trained on seasons before 2025; last two columns are what actually happened in 2026.':'As of 2026-08-16.';render();}
function render(){const tb=document.getElementById('tb');const q=filt.q.toLowerCase();
 let rows=D.filter(r=>(!q||r.name.toLowerCase().includes(q)||(r.team||'').toLowerCase().includes(q))&&(!filt.role||r.role===filt.role)&&(!filt.cls||CLSG[r.cls]===filt.cls)&&(!filt.reach||r.reach>0)&&(!filt.drop||r.drop===1)&&(!filt.gate||r.gate===1));
 rows.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];const nx=(x===null||x===undefined),ny=(y===null||y===undefined);if(nx&&ny)return 0;if(nx)return 1;if(ny)return -1;if(typeof x==='string')return sortDir*x.localeCompare(y);return sortDir*(x-y)});
 document.getElementById('cnt').textContent=rows.length+' of '+D.length+' pitchers';
 tb.innerHTML=rows.map((r,i)=>`<tr class="row" tabindex="0" data-i="${D.indexOf(r)}"><td class="l" style="color:var(--muted)">${i+1}</td>`+cols.map(([k,,c])=>`<td class="${c||''}">${k==='ppstf'&&r.ppstf!==null?`${r.ppfam} ${r.ppraw}→${r.ppstf} @ ${r.ppuse}%`:k==='gap'&&r.gap!==null?`${r.gap.toFixed(1)} → <span class="pos">+${r.gapexp.toFixed(1)}</span>`:fmt(r[k],k)}${k==='slot'&&r.drop?'<span class="flag" title="Driveline drop recipe: below-avg IVB, eff≥.93"></span>':''}</td>`).join('')+'</tr>').join('');
 document.querySelectorAll('th[data-k]').forEach(th=>th.classList.toggle('sorted',th.dataset.k===sortKey));}
function detail(r){const fams=r.fams.map(x=>`<div class="fam ${x.reach?'reach':'off'}"><div class="h">${x.fam} <span style="font-weight:400;color:var(--muted)">${FAMN[x.fam]}</span></div><div class="m">prec Stf+ ${x.pstf??'·'} · share ${x.prec??'·'} · P(add) ${x.p??'·'}</div><div class="m">gain ${x.gain>0?'+'+x.gain:'0'} · EV ${x.ev??0}</div></div>`).join('');
 return `<td colspan="${cols.length+1}"><div><strong>${r.name}</strong> — ${r.role}, ${r.ip} IP, ERA ${r.era??'·'} / xERA ${r.xera??'·'}, K% ${r.k??'·'} · BB% ${r.bb??'·'} · slot ${r.slot}°, 4S efficiency ${r.eff4}, ${r.cls.replace('_',' ')}, precedent pool ${r.pool} same-hand pitcher-seasons within ±5°/similar VAA${r.drop?' · <span style="color:var(--flag)">drop-recipe profile</span>':''}.<br>Families not thrown (&lt;2%). Outlined = reachable (≥20% of sup/pro-compatible comps throw it ≥10%). Gain = 0.14 × (precedent Stf+ − ${r.stuff})⁺; EV = P(add) × gain.</div><div class="fams">${fams||'<em>No unthrown families with precedent data.</em>'}</div><div style="margin-top:10px">${r.dev!==null?`<strong>Development engine</strong>: raw ${r.devraw>0?'+':''}${r.devraw}, calibrated ${r.dev>0?'+':''}${r.dev} next-season Stuff+ (five rolling backtests 2021–25: realized ≈ −0.29 + 0.67×raw, pooled r .29; calibrated +1–3 realized +2.0 (26% chance of ≥5, 38% decline), +3–5 realized +3.3 (39% / 27%); sd ≈ 6 in every bucket; scored for every pitcher, not just the archetype). `:''}<strong>Actionable ${r.act}</strong> = 0.5×mix ${r.mixb>0?'+'+r.mixb:'0'} (${r.mixplan||'no reallocation'}${r.merged?'; merged labels: '+r.merged:''}) + add ${r.addact>0?'+'+r.addact:'0'} + drop ${r.dropb>0?'+'+r.dropb:'0'} → projected Stuff+ ${r.projact}. <strong>Regress-to-comps</strong> ${r.gap>0?'+'+r.gap:'0'} — ${r.gapp||'no pitch grades below its comps'}. <strong>Mix</strong> ${r.mix>0?'+'+r.mix:r.mix} — worst pitch ${r.worst||'·'}, best ${r.bestp||'·'}; reweighting up to 20 pts of usage toward better pitches (FB ≥30%, cap 45%). <strong>Drift</strong> ${r.opp} = fitted weights on gap-vs-comps, add-EV and mix (2020–25 next-season ΔStuff+).</div><div class="legend">Projected Stuff+ ${r.proj} → ΔPit+ ${r.dpit>0?'+':''}${r.dpit} → ΔWAR ${r.dwar>0?'+':''}${r.dwar} at ${r.ip} IP (${r.role} rate) → ${r.dm>0?'+':''}$${r.dm}M at $8M/WAR. Conditional on the add happening; not a forecast.</div></td>`}
document.getElementById('tb').addEventListener('click',e=>{const tr=e.target.closest('tr.row');if(!tr)return;const nx=tr.nextElementSibling;if(nx&&nx.classList.contains('detail')){nx.remove();return}const r=D[+tr.dataset.i];const d=document.createElement('tr');d.className='detail';d.innerHTML=detail(r);tr.after(d)});
document.getElementById('tb').addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.classList.contains('row'))e.target.click()});
document.getElementById('q').addEventListener('input',e=>{filt.q=e.target.value;render()});
document.getElementById('role').addEventListener('change',e=>{filt.role=e.target.value;render()});
document.getElementById('cls').addEventListener('change',e=>{filt.cls=e.target.value;render()});
document.getElementById('reach').addEventListener('change',e=>{filt.reach=e.target.checked;render()});
document.getElementById('gate').addEventListener('change',e=>{filt.gate=e.target.checked;render()});
document.getElementById('drop').addEventListener('change',e=>{filt.drop=e.target.checked;render()});
document.querySelectorAll('button.yr').forEach(b=>b.addEventListener('click',()=>setYear(b.dataset.y)));
setYear('2026');
"""
ths=''.join(f'<th data-k="{k}" class="{c if len(x)>2 else ""}">{lab}</th>' for x in [['name','Pitcher','l'],['team','Tm','l'],['age','Age'],['role','Role','l'],['ip','IP'],['slot','Slot°'],['eff4','4S eff'],['cls','Class','l'],['stuff','Stuff+'],['loc','Loc+'],['act','Actionable'],['mixb','Mix'],['best','Best add','l'],['bpstf','Prec Stf+'],['addact','Add gain'],['dropb','Drop'],['projact','Proj Stf+'],['opp','Drift'],['gap','Gap vs comps → exp.'],['ev','Add ΣEV'],['bp','P(add)'],['pool','Pool']] for k,lab,*c in [x] for c in [c[0] if c else ''])
def check(nm):
    r=d[d.PlayerName.str.contains(nm,na=False)]
    if not len(r): return ''
    r=r.iloc[0]; ba=r.best_add if isinstance(r.best_add,str) else '—'
    cpmtxt=('%.2f'%r.cpm) if ('cpm' in r.index and pd.notna(r.cpm)) else 'out of gate'
    gp=(' (' + r.gap_parts + ')') if isinstance(r.gap_parts,str) and r.gap_parts else ''
    return f'<div class="check"><div class="h">{r.PlayerName} <span style="color:var(--muted);font-weight:400">{r.Team} · {r.role}</span></div><div>Slot {r.arm_angle:.0f}°, 4S efficiency {r.eff4:.2f}, {str(r.suppro_class).replace("_"," ")}. Stuff+ {r.stuff:.0f}, Loc+ {r.sp_location:.0f}.</div><div style="margin-top:6px">Reachable roles {r.n_reachable:.0f}; best add {ba}{"" if ba=="—" else f" (prec Stf+ {r.best_add_pstf:.0f}, share {r.best_add_prec:.2f}, P {r.best_add_padd:.2f})"}; gain <span class="{ "pos" if r.gain>0 else ""}">{r.gain:+.1f}</span>; pool n={r[pool]:.0f}.</div><div style="margin-top:6px">Gap vs comps {r.gain_gap:+.1f}{gp}; mix {r.gain_mix:+.1f}; <strong>CPM {cpmtxt}</strong>; <strong>actionable {r.actionable:.1f}</strong> (mix {r.gain_mix:+.1f}, add {r.add_act:+.1f}, drop {r.drop_bonus:+.1f} → proj {r.proj_stuff_act:.0f}); drift {r.opportunity:.2f}.</div></div>'
checks=''.join(check(n) for n in ['Beck Way','Yesavage','Palmquist','Hancock'])
try:
    def cpm_table(path,realized):
        cpm=pd.read_parquet(path).sort_values('cpm',ascending=False)
        rows=''
        for i,(_,x) in enumerate(cpm.head(40).iterrows(),1):
            real=f"<td class='{'pos' if x.d_stuff>0 else 'neg'}'>{x.d_stuff:+.1f}</td><td class='{'pos' if x.d_pit>0 else 'neg'}'>{x.d_pit:+.1f}</td>" if realized else ''
            hl=" style='background:var(--gain-bg)'" if ('Palmquist' in str(x.PlayerName) or 'Beck Way' in str(x.PlayerName)) else ''
            rows+=f"<tr{hl}><td class='l' style='color:var(--muted)'>{i}</td><td class='l'>{x.PlayerName}</td><td class='l'>{x.Team}</td><td>{x.Age:.0f}</td><td class='l'>{x.role}</td><td>{x.stuff:.0f}</td><td>{x.sp_pitching:.0f}</td><td>{x.pp_stf:.0f} @ {x.pp_use*100:.0f}%</td><td>{x.fb_liability:.1f}</td><td>{x.gain_gap:.1f}</td><td>{x.mix_pit:+.1f}</td><td>{'Y' if x.drop_recipe else ''}</td><td>{x.pred:+.1f}</td><td>{x.actionable:.1f}</td><td><strong>{x.cpm:.2f}</strong></td>{real}</tr>"
        rh="<th>2026 ΔStf+</th><th>2026 ΔPit+</th>" if realized else ''
        return f'<div class="tbl"><table style="min-width:900px"><thead><tr><th class="l">#</th><th class="l">Pitcher</th><th class="l">Tm</th><th>Age</th><th class="l">Role</th><th>Stuff+</th><th>Pit+</th><th>Plus pitch</th><th>FB liab.</th><th>Regress</th><th>Mix</th><th>Drop</th><th>Dev ΔStf+</th><th>Actionable</th><th>Score</th>{rh}</tr></thead><tbody>{rows}</tbody></table></div>', len(cpm)
    t26,n26=cpm_table('data/derived/cpm_2026.parquet',False); t25,n25=cpm_table('data/derived/cpm_test2025.parquet',True)
    cpm_html=f'''<h2>The Carson Palmquist Model</h2><p class="sub" style="max-width:100ch">Gate: owns a plus pitch (any offering Stf+ ≥105) inside an ordinary arsenal (Stuff+ 88–104). Score = z(development engine: GBM-predicted next-season ΔStuff+ from structural features, trained on seasons before the one shown) + z(reconfiguration engine: the Actionable score). Ranks are within the gate: {n25} pitchers in 2025, {n26} in 2026. Highlighted rows: Palmquist, Way. Full spec: docs/CARSON-PALMQUIST-MODEL.md.</p>
<div class="controls" style="margin-top:6px"><button class="yr" data-y="2026" aria-pressed="true">2026 · today</button><button class="yr" data-y="2025" aria-pressed="false">2025 · going into 2026, with what happened</button></div>
<div id="cpm2026">{t26}</div><div id="cpm2025" hidden>{t25}</div>'''
except Exception as e:
    cpm_html=''
head=f"""<title>Reachable Arsenal Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>"""
body=f"""<div class="wrap">
<div class="eyebrow">MLB pitchers · 2026 through Aug 16 ({n} with ≥300 pitches) · 2025 full season ({n25})</div>
<h1>Reachable Arsenal Board</h1>
<p class="sub">What each pitcher could add from his current arm slot, what precedent says it would grade, and what that is worth. Sort any column; click a row for every family and the math.</p>
<div class="stats">
<div class="stat"><div class="v">#11 · #29</div><div class="l">Palmquist going into 2026 · Way today, on the CPM composite within the gate (development engine alone: Palmquist #4)</div></div><div class="stat"><div class="v">+2.9 / +1.9</div><div class="l">2026 Stuff+ / Pitching+ excess of the as-of-2025 CPM top-10 vs matched controls (top-40 +1.3 / +2.0)</div></div>
<div class="stat"><div class="v">r ≈ .5</div><div class="l">precedent grade of an added pitch vs its realized Stf+</div></div>
<div class="stat"><div class="v">+3.3</div><div class="l">same for the DRIFT top-40 (n=21; top-80 +1.4)</div></div>
<div class="stat"><div class="v">t = 5.9</div><div class="l">regress-to-comps on next-season ΔStuff+ after mean reversion — a valuation prior, not a lever</div></div>
</div>
<div class="method">
<p><strong>Method.</strong> For each family a pitcher throws under 2%, precedent is the same-hand, supination/pronation-compatible pitchers in his trait neighborhood (arm angle, height-adjusted VAA, release height, velo, spin, 4-seam efficiency, axis residual). Reachable if at least 20% of them throw it at 10%+. Gain = 0.14 usage × (precedent Stf+ − current Stuff+)⁺. P(add) comes from a grouped-CV model over every pitcher-season × unthrown family. EV = P(add) × gain, summed. Value: Pit+ = −74.8 + .85·Stf+ + .90·Loc+; ΔWAR = .098 (SP) / .074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR.</p>
<p><strong>Dev ΔStf+</strong> is the development engine's forecast of next-season change in overall Stuff+, scored for <em>every</em> pitcher (not just the archetype) and shown <em>calibrated</em>: five rolling-origin backtests (train on seasons before t, predict t→t+1, 2021–2025) give realized ≈ −0.29 + 0.67×raw, pooled r .29, top-25 beating stuff-matched controls in 5/5 years; calibrated +3–5 realized +3.3 with a 39% chance of a 5+ gain and 27% chance of decline; sd ≈ 6. Features are structural only (stuff level, age, velo, plus-pitch grade/usage, fastball liability vs comps, gap vs comps, efficiency/class, drop flag, Coors share, precedent pool, Loc+, mix/add gains). <strong>Gap vs comps</strong> is the raw usage-weighted shortfall of his pitches vs comps' — its <em>expected</em> regression is ~0.2 per point, shown after the arrow; it is a valuation prior, not a projection.</p><p><strong>CPM score</strong> (default sort) = <em>The Carson Palmquist Model</em>: for pitchers in the gate (a plus pitch, any offering Stf+ ≥105, inside an ordinary arsenal, Stuff+ 88–104), z(development engine: GBM-predicted next-season ΔStuff+ from structural features, trained only on seasons before the one shown) + z(Actionable). Out of the gate: no score, sorted last. Strict 2025→26 test: gated top-10 +3.9 Stuff+ over matched controls; Per-pitch grades are shrunk toward comps by sample (K=80 pitches, FG's stabilization point) before mix and plus-pitch. Palmquist #11 going into 2026 (development engine alone #4), Way #29 today.</p><p><strong>Actionable</strong> = what an org could do on day one: <em>mix</em> gain (move ≤20 pts of usage toward his better pitches, graded on a 50/50 blend of per-pitch Stuff+ and Pitching+ so results-good pitches like a plus changeup aren't cut; labels that are the same physical pitch — CU/KC, CH/FS, FF/SI, FC/SL within 2.5 mph and 4.5" — are merged first; fastballs ≥30%, no pitch >45%) + best reachable role-unoccupied <em>add</em> valued at comps' Stf+ × 0.14 usage (feasibility = ≥20% of sup/pro-compatible comps throw it; no P(add) discount) + <em>drop-recipe</em> bonus of +1.4 (the replicated Driveline effect for below-average ride + efficiency ≥.93). Regress-to-comps is deliberately excluded. <strong>Drift</strong> is the passive counterpart — what tends to happen on its own — and combines four levers, weighted by a regression of next-season ΔStuff+ on each (2020–25, mean reversion controlled): <em>regress-to-comps</em> = usage × (comps' Stf+ on the same family − his)⁺ over pitches he throws ≥8% — a shrinkage prior (persistent gaps regress ~.16/pt, transient ~.26/pt; Dobnak is the counterexample); <em>reachable additions</em> as EV; <em>mix</em> = usage-weighted Stuff+ gain from moving ≤20 pts of usage toward his better pitches; </p><p><strong>Read the addition columns as reachability with a conditional price.</strong> Backtest 2020–25: possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after mean reversion. Slot change is a feasibility flag only (<span class="flag"></span> = below-average four-seam ride with efficiency ≥.93 — the profile that gained on dropping in Driveline's data and ours); no slot gain is projected. </p>
</div>
<div class="controls"><button class="yr" data-y="2026" aria-pressed="true">2026 · today</button><button class="yr" data-y="2025" aria-pressed="false">2025 · going into 2026</button><span id="yrnote" class="legend" style="margin:0 6px"></span></div>
<div class="controls"><input id="q" type="search" placeholder="Search pitcher or team" aria-label="Search">
<select id="role" aria-label="Role"><option value="">All roles</option><option>SP</option><option>RP</option></select>
<select id="cls" aria-label="Class"><option value="">All classes</option><option value="P">Pronator-leaning</option><option value="S">Supinator-leaning</option><option value="H">Hybrid / unknown</option></select>
<label><input id="gate" type="checkbox" checked> Palmquist archetype only — a plus pitch (Stf+ ≥ 105) inside an ordinary arsenal (Stuff+ 88–104)</label>
<label><input id="reach" type="checkbox"> reachable add only</label>
<label><input id="drop" type="checkbox"> drop-recipe profile</label>
<span class="n" id="cnt"></span></div>
<div class="tbl"><table><thead><tr></tr></thead><tbody id="tb"></tbody></table></div>
<p class="legend">Stuff+/Loc+/Pit+ = FanGraphs. Pitch families follow FanGraphs typing: sweepers live inside SL (FG has no ST column), knuckle-curves are KC. Per-pitch grades used by mix / plus-pitch are shrunk toward comps by sample: (n·own + 80·comps)/(n+80); the plus-pitch column shows raw → shrunk. Prec Stf+ = usage-weighted FG Stf+ of comps on that family. Share = fraction of comps throwing it 10%+. Pool = same-hand pitcher-seasons within ±5° and similar VAA (thin pools mean thin precedent).</p>
<h2>Named checks</h2>
<div class="checks">{checks}</div>
<h2>Was it findable a year early?</h2>
<p class="sub" style="max-width:100ch">Rebuilt strictly as of end-2025 (precedent, P(add), and weights restricted to ≤2025 data): the opportunity top-40 gained +3.1 Stuff+ in 2026 vs −0.2 for stuff-matched controls (n=20 with ≥300 pitches; top-80 +1.6). On the actionable score, Beck Way is #1 in 2026 (128 slider thrown 15%, 84 four-seam 14%; curve reachable at 103; drop-recipe profile); Glasnow falls to ~#47 once his CU/KC labels are merged; Iglesias to ~#28 once the mix is graded on the Stf+/Pit+ blend. As of 2025 the actionable top-40 gained +2.5 Stuff+ and +2.5 Pit+ over matched controls; Palmquist ranked #94 actionable (his gain was pitch quality, which lives on the drift list, where he was #27) and Hancock #51. On drift, Palmquist ranked #27 (mix +5.4: threw his 86 four-seam 42%; pitch gap +9.2: FF 86 → comps 101, FC 75 → 93), Senzatela #26, Dollander #29, Hancock #101 (#1 by raw addition gain — card said curve; he dropped 8° and added a sweeper/cutter). Caveat: several top-ranked 2025 relievers had no 2026 sample, so the excess is measured among survivors.</p>
<p class="foot">Data: Statcast 2020–2026 (Chamberlain Pitch Leaderboard v8 extract + pybaseball backfill), Baseball Savant spin-direction leaderboard, FanGraphs Stuff+/Location+/Pitching+ and standard leaderboards. Code and derived tables: github.com/vincepipitone/baseball-slot-sim.</p>
</div>
<script>{JS.replace('__DATA__',data)}</script>"""
frag=head+body
open(f'docs/targets_{ASOF}.html','w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+head+'</head><body>'+body+'</body></html>')
os.makedirs('/Users/vincepipitone/.claude/jobs/aa656eb5/tmp',exist_ok=True)
open('/Users/vincepipitone/.claude/jobs/aa656eb5/tmp/reachable-arsenal-board.html','w').write(frag)
print('wrote', len(frag)//1024,'KB', n,'rows')
