"""Levers that would have found Palmquist:
 (A) mix optimization: reweight the pitcher's own per-pitch Stf+ toward his better pitches under constraints
     (primary FB family >= 30% total fastball usage; no pitch > 45%; keep >=3 pitches; move at most 20 pts of usage total).
     gain_mix = optimized usage-weighted Stf+ - current usage-weighted Stf+.
 (B) existing-pitch gap: for pitches thrown >=8%, gap_f = usage_f * (precedent Stf+ of family in his neighborhood - own Stf+_f)^+ ;
     gain_gap = sum. (value-signed 'unrealized pitch')
 (C) Coors: road-only own-model Stuff for pitchers with >=25% of pitches at COL, minus overall.
Backtest 2020-25 (own gain at t vs realized ΔStuff+ t+1, mean-reversion controlled); as-of-2025 look at Palmquist; who ranks top."""
import numpy as np, pandas as pd, sys, os
sys.path.insert(0,'src')
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[(t.n>=30)&t.stf.notna()]
pr=pd.read_parquet('data/derived/precedent.parquet').drop_duplicates(['pitcher','game_year'])
fg=pd.read_csv('data/derived/fg_stuff.csv').drop_duplicates(['pitcher','game_year'])[['pitcher','game_year','sp_stuff','sp_location','sp_pitching']]
# ---- (A) mix optimization on per-pitch PITCHING+ (owner: optimize on Pit+), after CLUSTER-BASED identity:
#      merge labels within a pitcher-season that are the same pitch (same role, |Δvelo|<2.5 mph, movement distance<4.5"):
#      merged usage = sum, grades = usage-weighted. Kills CU/KC, CH/FS, FF/SI label splits of one physical pitch.
ROLE={'FF':'ride','SI':'run','FC':'cut','FS':'offspeed','CH':'offspeed','SL':'slider','CU':'curve','KC':'curve'}
SAME_ROLE_MERGE={('CU','KC'),('KC','CU'),('CH','FS'),('FS','CH'),('FF','SI'),('SI','FF'),('FC','SL'),('SL','FC')}
def merge_labels(g):
    g=g[g.n>=20].copy().sort_values('usage',ascending=False)
    rows=[r for _,r in g.iterrows()]; merged=[]
    while rows:
        a=rows.pop(0); keep=[]
        for b in rows:
            same=(a.fg_type,b.fg_type) in SAME_ROLE_MERGE or a.fg_type==b.fg_type
            close=abs(a.release_speed-b.release_speed)<2.5 and np.hypot(a.IVB-b.IVB,a.HB_arm-b.HB_arm)<4.5
            if same and close:
                w=a.usage+b.usage
                for c_ in ['stf','loc','pit','release_speed','IVB','HB_arm']: a[c_]=(a[c_]*a.usage+b[c_]*b.usage)/w
                a['n']=a.n+b.n; a['usage']=w; a['merged_from']=(a.get('merged_from','') or '')+'+'+b.fg_type
            else: keep.append(b)
        merged.append(a); rows=keep
    return pd.DataFrame(merged)
def optimize(g,col='pit'):
    g=g.sort_values(col,ascending=False); u=g.usage.values.copy(); s=g[col].values; fam=g.fg_type.values
    isfb=np.isin(fam,['FF','SI','FC']); u=u/u.sum(); base=(u*s).sum(); budget=0.20; u2=u.copy()
    for w in np.argsort(s):
        for b in np.argsort(-s):
            if b==w or budget<=0: continue
            take=min(u2[w],0.45-u2[b],budget)
            if take<=0: continue
            trial=u2.copy(); trial[w]-=take; trial[b]+=take
            if trial[isfb].sum()<0.30: continue
            u2=trial; budget-=take
    return base,(u2*s).sum(),u2
rows=[]
for (pid,yr),g in t.groupby(['pitcher','game_year']):
    if g.n.sum()<300: continue
    gm=merge_labels(g)
    if len(gm)<2 or gm.pit.isna().any(): continue
    gm['blend']=0.5*gm.stf+0.5*gm.pit
    base_p,opt_p,u2=optimize(gm,'blend'); base_s,opt_s,_=optimize(gm,'stf')
    worst=gm.sort_values('blend').iloc[0]; best=gm.sort_values('blend').iloc[-1]
    rows.append(dict(pitcher=pid,game_year=yr,mix_base=base_s,mix_opt=opt_s,gain_mix=opt_s-base_s,mix_pit=opt_p-base_p,n_pitches_merged=len(gm),
        merged=' '.join(f"{r_.fg_type}{r_['merged_from']}" for _,r_ in gm.iterrows() if isinstance(r_.get('merged_from',None),str) and r_['merged_from']),
        worst_fam=worst.fg_type,worst_use=worst.usage,worst_stf=worst.stf,worst_pit=worst.pit,best_fam=best.fg_type,best_use=best.usage,best_stf=best.stf,best_pit=best.pit,
        mix_plan=', '.join(f"{f} {a*100:.0f}→{b*100:.0f}%" for f,a,b in zip(gm.sort_values('blend',ascending=False).fg_type,gm.sort_values('blend',ascending=False).usage/gm.usage.sum(),u2) if abs(a-b)>0.005)))
M=pd.DataFrame(rows)
# ---- (B) existing-pitch precedent gap
G=[]
for _,r in pr.iterrows():
    own=t[(t.pitcher==r.pitcher)&(t.game_year==r.game_year)]
    tot=0; parts=[]
    for _,x in own.iterrows():
        if x.usage<0.08: continue
        p=r.get(f'pstf_{x.fg_type}',np.nan)
        if pd.notna(p) and p>x.stf: tot+=x.usage*(p-x.stf); parts.append(f"{x.fg_type} {x.stf:.0f}→{p:.0f}")
    G.append(dict(pitcher=r.pitcher,game_year=r.game_year,gain_gap=tot,gap_parts=' | '.join(parts)))
G=pd.DataFrame(G)
# ---- (C) Coors road-only via own model
import stuff_model as SM
m,scale=SM.load()
gh=pd.read_parquet('data/derived/game_home.parquet')
raw=pd.read_parquet('data/derived/pitches.parquet',columns=['pitcher','game_year','game_pk']).merge(gh,on='game_pk',how='left')
# simpler: recompute home_team share per pitcher-season from raw and score road-only subset by excluding COL home games
col_share=raw.groupby(['pitcher','game_year']).home_team.apply(lambda s:(s=='COL').mean()).rename('col_share').reset_index()
cands=col_share[col_share.col_share>=0.25]
raw2=pd.read_parquet('data/derived/pitches.parquet',columns=SM.COLS+['game_pk']).merge(gh,on='game_pk',how='left')
raw2=raw2[raw2.pitcher.isin(cands.pitcher)]
raw2=raw2[raw2.release_speed.notna()&raw2.IVB.notna()&raw2.release_pos_z.notna()&raw2.release_extension.notna()]
q=SM.engineer(raw2); q=q[q.arm_angle.notna()]
q['stuff']=SM.score(m,scale,q)
allst=q.groupby(['pitcher','game_year']).stuff.mean().rename('own_all'); road=q[q.home_team!='COL'].groupby(['pitcher','game_year']).stuff.mean().rename('own_road'); home=q[q.home_team=='COL'].groupby(['pitcher','game_year']).stuff.mean().rename('own_home')
Cc=pd.concat([allst,road,home],axis=1).reset_index().merge(cands,on=['pitcher','game_year']); Cc['coors_adj']=Cc.own_road-Cc.own_all
print(f"Coors: pitcher-seasons with >=25% pitches at COL: {len(Cc)}; mean own-model stuff home {Cc.own_home.mean():.1f} vs road {Cc.own_road.mean():.1f} (Δ {Cc.own_road.mean()-Cc.own_home.mean():+.1f}); mean road-minus-all {Cc.coors_adj.mean():+.2f}")
# ---- assemble + backtest
A=fg.merge(M,how='left').merge(G,how='left').merge(Cc[['pitcher','game_year','col_share','coors_adj']],how='left')
A['coors_adj']=A.coors_adj.fillna(0); A['gain_gap']=A.gain_gap.fillna(0)
nm=t.groupby(['pitcher','game_year']).player_name.first().reset_index(); A=A.merge(nm,how='left')
nx=A[['pitcher','game_year','sp_stuff','sp_pitching']].copy(); nx['game_year']-=1
b=A.merge(nx,on=['pitcher','game_year'],suffixes=('','_next')).dropna(subset=['sp_stuff_next','gain_mix'])
b['d']=b.sp_stuff_next-b.sp_stuff; b['dp']=b.sp_pitching_next-b.sp_pitching
import statsmodels.api as sm
res=sm.OLS(b.d,sm.add_constant(b.sp_stuff)).fit().resid
def r(a,c): k=np.isfinite(a)&np.isfinite(c); return np.corrcoef(a[k],c[k])[0,1]
print(f"\nbacktest n={len(b)} (2020-25 → next season):")
for lab,col in [('mix gain','gain_mix'),('existing-pitch gap','gain_gap'),('coors adj','coors_adj')]:
    print(f"  {lab:20s} r(ΔStuff+) {r(b[col],b.d):+.3f} | after mean-reversion {r(b[col],res):+.3f} | r(ΔPit+) {r(b[col],b.dp):+.3f} | mean {b[col].mean():.2f} p90 {b[col].quantile(.9):.2f}")
X=sm.add_constant(b[['sp_stuff','gain_mix','gain_gap','coors_adj']]); f=sm.OLS(b.d,X).fit(); print(f.summary().tables[1])
b['comb']=f.params.gain_mix*b.gain_mix+f.params.gain_gap*b.gain_gap+f.params.coors_adj*b.coors_adj
b['q']=pd.qcut(b.comb.rank(method='first'),5,labels=False); print(b.groupby('q').agg(n=('d','size'),comb=('comb','mean'),d_stuff=('d','mean'),resid=('d',lambda s:res[s.index].mean())).round(2).T.to_string())
A.to_parquet('data/derived/levers_v2.parquet',index=False)
# as-of-2025 look
c=A[A.game_year==2025].copy(); c['score']=f.params.gain_mix*c.gain_mix+f.params.gain_gap*c.gain_gap+f.params.coors_adj*c.coors_adj
c['rank']=c.score.rank(ascending=False,method='min')
n26=fg[fg.game_year==2026][['pitcher','sp_stuff']].rename(columns={'sp_stuff':'stuff26'}); c=c.merge(n26,how='left'); c['d26']=c.stuff26-c.sp_stuff
print("\nas-of-2025:"); print(c[c.player_name.str.contains('Palmquist|Hancock|Dollander|Senzatela',na=False)][['player_name','sp_stuff','gain_mix','worst_fam','worst_use','worst_stf','best_fam','best_use','best_stf','gain_gap','gap_parts','col_share','coors_adj','score','rank','stuff26','d26']].round(2).to_string(index=False))
v=c.dropna(subset=['d26']); top=v[v['rank']<=40]; rest=v[v['rank']>40]
exp=[rest[(rest.sp_stuff-s).abs()<=3].d26.mean() for s in top.sp_stuff]
print(f"as-of-2025 top-40 by combined score: realized 2026 ΔStuff+ {top.d26.mean():+.2f} vs stuff-matched {np.nanmean(exp):+.2f} → excess {top.d26.mean()-np.nanmean(exp):+.2f} (n={len(top)})")
print(c.sort_values('score',ascending=False).head(20)[['player_name','sp_stuff','gain_mix','gain_gap','coors_adj','score','stuff26','d26']].round(2).to_string(index=False))
