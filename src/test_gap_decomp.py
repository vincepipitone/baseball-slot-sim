"""Decompose existing-pitch gap: for pitcher x family x season (n>=50), comps' mean shape and Stf+ (same neighborhood as precedent);
shape distance = z-distance of (velo, IVB, HB_arm) from comps' mean. Test at pitch level: next-season Stf+ ~ own + comps + gap x shape-distance."""
import numpy as np, pandas as pd, statsmodels.api as sm
from sklearn.neighbors import NearestNeighbors
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[(t.n>=50)&t.stf.notna()&t.arm_angle.notna()]
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4','axis_res','suppro_class']].drop_duplicates(['pitcher','game_year']); t=t.merge(sp,how='left')
G={'pronator':'P','lean_pronator':'P','supinator':'S','lean_supinator':'S'}; t['grp']=t.suppro_class.map(G).fillna('H')
fb=t[t.is_primary_fb==1][['pitcher','game_year','arm_angle','VAA_AA_pt','release_pos_z','release_speed','release_spin_rate','eff4','axis_res','p_throws','grp']].rename(columns={'arm_angle':'aa','VAA_AA_pt':'hv','release_pos_z':'rz','release_speed':'fv','release_spin_rate':'fs'})
fb=fb.drop_duplicates(['pitcher','game_year']); fb['bauer']=fb.fs/fb.fv
X=fb[['aa','hv','rz','fv','bauer','eff4','axis_res']].fillna(fb[['aa','hv','rz','fv','bauer','eff4','axis_res']].median()); Z=((X-X.mean())/X.std()).values; Z[:,0]*=1.5
fb=fb.reset_index(drop=True)
rows=[]
for hand in ['R','L']:
    idx=np.where(fb.p_throws.values==hand)[0]; nn=NearestNeighbors(n_neighbors=120).fit(Z[idx]); _,nb=nn.kneighbors(Z[idx])
    for i,row in enumerate(idx):
        me=fb.iloc[row]; cand=[idx[j] for j in nb[i] if fb.pitcher.values[idx[j]]!=me.pitcher and (me.grp=='H' or fb.grp.values[idx[j]] in (me.grp,'H'))][:40]
        keys=set(zip(fb.pitcher.values[cand],fb.game_year.values[cand]))
        pool=t[t.set_index(['pitcher','game_year']).index.isin(keys)] if False else None
        rows.append((me.pitcher,me.game_year,cand))
# build comps table per pitcher-season-family
tt=t.set_index(['pitcher','game_year'])
comp_rows=[]
for pid,yr,cand in rows:
    keys=list(zip(fb.pitcher.values[cand],fb.game_year.values[cand]))
    pool=tt.loc[tt.index.isin(keys)]
    for f in FAM:
        g=pool[(pool.fg_type==f)&(pool.usage>=0.10)]
        if len(g)<5: continue
        w=g.n.values
        comp_rows.append(dict(pitcher=pid,game_year=yr,fg_type=f,c_stf=np.average(g.stf,weights=w),c_velo=np.average(g.release_speed,weights=w),c_ivb=np.average(g.IVB,weights=w),c_hb=np.average(g.HB_arm,weights=w),
                              s_velo=g.release_speed.std(),s_ivb=g.IVB.std(),s_hb=g.HB_arm.std(),n_comp=len(g)))
C=pd.DataFrame(comp_rows)
m=t.merge(C,on=['pitcher','game_year','fg_type'])
m['dist']=np.sqrt(((m.release_speed-m.c_velo)/m.s_velo)**2+((m.IVB-m.c_ivb)/m.s_ivb)**2+((m.HB_arm-m.c_hb)/m.s_hb)**2)
m['gap']=m.c_stf-m.stf
nx=m[['pitcher','game_year','fg_type','stf','n']].copy(); nx['game_year']-=1
p=m.merge(nx,on=['pitcher','game_year','fg_type'],suffixes=('','_next')); p=p[(p.n>=100)&(p.n_next>=100)&(p.usage>=0.08)]
p['d']=p.stf_next-p.stf
print(f"pitch-level pairs {len(p)}; corr(gap, dist) {np.corrcoef(p.gap,p.dist)[0,1]:.2f}")
p['far']=(p.dist>p.dist.median()).astype(int)
Xr=sm.add_constant(pd.DataFrame({'stf':p.stf,'gap':p.gap,'gap_x_far':p.gap*p.far,'far':p.far}))
f=sm.OLS(p.d,Xr).fit(); print(f.summary().tables[1])
# simpler: split
for lab,g in [('shape-similar (dist<=median)',p[p.far==0]),('shape-different (dist>median)',p[p.far==1])]:
    ff=sm.OLS(g.d,sm.add_constant(g[['stf','gap']])).fit(); print(f"{lab}: n={len(g)}  gap coef {ff.params.gap:+.3f} (t={ff.tvalues.gap:.1f})  stf coef {ff.params.stf:+.3f}")
# does gap predict beyond own-pitch mean reversion + comps' Stf+ as prior?
ff=sm.OLS(p.d,sm.add_constant(p[['stf','c_stf']])).fit(); print(f"\nnext-season Δ ~ own stf {ff.params.stf:+.3f} + comps stf {ff.params.c_stf:+.3f} (t={ff.tvalues.c_stf:.1f})  → shrinkage weight toward comps ≈ {ff.params.c_stf/(-ff.params.stf):.2f}")
# by dist tercile
p['dq']=pd.qcut(p.dist,3,labels=['near','mid','far'])
for q,g in p.groupby('dq',observed=True):
    ff=sm.OLS(g.d,sm.add_constant(g[['stf','c_stf']])).fit(); print(f"  {q}: n={len(g)} comps coef {ff.params.c_stf:+.3f} (t={ff.tvalues.c_stf:.1f}), mean gap {g.gap.mean():+.1f}, mean Δ {g.d.mean():+.2f}")
m.to_parquet('data/derived/gap_decomp.parquet',index=False)
# Dobnak / SWR / Palmquist 2025 view
for nm in ['Dobnak','Woods Richardson','Palmquist']:
    x=m[(m.player_name.str.contains(nm))&(m.game_year.isin([2025,2026]))][['player_name','game_year','fg_type','usage','release_speed','IVB','HB_arm','stf','c_stf','c_velo','c_ivb','c_hb','dist','gap']].round(1)
    print(x.to_string(index=False))
