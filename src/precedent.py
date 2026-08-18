"""Module 3b: precedent / comps for pitch additions at current slot.
For each pitcher-season: neighborhood of same-hand pitcher-seasons on physical traits
(arm angle, FB HAVAA, release height, FB velo, FB Bauer units, sup/pro proxy = FB axis-minus-slot, extension).
For each pitch family: precedent share (neighbors throwing it >=10%), neighbors' mean Stf+ on it.
Backtest: on the addition corpus, does precedent rank the pitch actually added? (top-1/top-2 vs slot-bucket base rate)
Also computes ARSENAL OPTIONALITY per pitcher-season."""
import numpy as np, pandas as pd, sys
from sklearn.neighbors import NearestNeighbors
K=int(sys.argv[1]) if len(sys.argv)>1 else 40
import os; ASOF=int(os.environ.get('ASOF','2026')); SUF='' if ASOF==2026 else f'_asof{ASOF}'
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
t=pd.read_parquet('data/derived/emulator_table.parquet')
t=t[(t.n>0)&(t.game_year<=ASOF)]
# pitcher-season trait vector from primary fastball rows
fb=t[t.is_primary_fb==1].copy()
fb['bauer_fb']=fb.release_spin_rate/fb.release_speed
tr=fb[['pitcher','player_name','p_throws','game_year','arm_angle','VAA_AA_pt','release_pos_z','release_speed','bauer_fb','axis_minus_slot','release_extension','sp_stuff']].rename(
    columns={'VAA_AA_pt':'fb_havaa','release_speed':'fb_velo','axis_minus_slot':'suppro'})
tot=t.groupby(['pitcher','game_year']).n.sum().rename('n_tot').reset_index()
tr=tr.merge(tot,on=['pitcher','game_year']); tr=tr[(tr.n_tot>=200)&tr.arm_angle.notna()].reset_index(drop=True)
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4','axis_res','si_dev','suppro_class']]
tr=tr.merge(sp,on=['pitcher','game_year'],how='left'); tr['suppro_class']=tr.suppro_class.fillna('unknown')
GROUP={'pronator':'P','lean_pronator':'P','supinator':'S','lean_supinator':'S','hybrid':'H','unknown':'H'}
tr['grp']=tr.suppro_class.map(GROUP)
U=t.pivot_table(index=['pitcher','game_year'],columns='fg_type',values='usage',aggfunc='first').reindex(columns=FAM).fillna(0)
S=t.pivot_table(index=['pitcher','game_year'],columns='fg_type',values='stf',aggfunc='first').reindex(columns=FAM)
U=U.reindex(pd.MultiIndex.from_frame(tr[['pitcher','game_year']])).fillna(0).values
S=S.reindex(pd.MultiIndex.from_frame(tr[['pitcher','game_year']])).values
FEATS=['arm_angle','fb_havaa','release_pos_z','fb_velo','bauer_fb','eff4','axis_res','release_extension']
X=tr[FEATS].fillna(tr[FEATS].median()); Z=((X-X.mean())/X.std()).values
Z[:,0]*=1.5  # weight slot a bit more
prec=np.zeros((len(tr),len(FAM))); pstf=np.full((len(tr),len(FAM)),np.nan)
for hand in ['R','L']:
    idx=np.where(tr.p_throws.values==hand)[0]
    nn=NearestNeighbors(n_neighbors=min(3*K,len(idx))).fit(Z[idx])
    d,nb=nn.kneighbors(Z[idx])
    for i,row in enumerate(idx):
        # exclude self AND same pitcher other seasons (leakage)
        # exclude self/same pitcher; require compatible sup/pro group (hybrids match anyone)
        g0=tr.grp.values[row]
        cand=[idx[j] for j in nb[i] if tr.pitcher.values[idx[j]]!=tr.pitcher.values[row] and (g0=='H' or tr.grp.values[idx[j]] in (g0,'H'))][:K]
        uu=U[cand]; ss=S[cand]
        thr=(uu>=0.10)
        prec[row]=thr.mean(0)
        for f in range(len(FAM)):
            m=thr[:,f]&~np.isnan(ss[:,f])
            if m.sum()>=3: pstf[row,f]=np.average(ss[m,f],weights=uu[m,f])
P=pd.DataFrame(prec,columns=[f'prec_{f}' for f in FAM]); Q=pd.DataFrame(pstf,columns=[f'pstf_{f}' for f in FAM])
out=pd.concat([tr,P,Q],axis=1)
own=pd.DataFrame(U,columns=[f'use_{f}' for f in FAM]); out=pd.concat([out,own],axis=1)
# functional roles: a family only counts as an option if its ROLE is unoccupied (<5% usage in role)
ROLE={'FF':'ride','SI':'run','FC':'cut','FS':'offspeed','CH':'offspeed','SL':'slider','CU':'curve','KC':'curve'}
role_use={r:np.zeros(len(out)) for r in set(ROLE.values())}
for f_i,f in enumerate(FAM): role_use[ROLE[f]]+=U[:,f_i]
opt=np.zeros(len(out)); breadth=np.zeros(len(out)); best_gain=np.zeros(len(out)); best_fam=np.array(['']*len(out),dtype=object)
for f_i,f in enumerate(FAM):
    unocc=role_use[ROLE[f]]<0.05
    gain=np.nan_to_num(pstf[:,f_i]-out.sp_stuff.values,nan=0)
    contrib=unocc*prec[:,f_i]*np.maximum(gain,0)
    opt+=contrib; breadth+=unocc*(prec[:,f_i]>=0.25)
    better=contrib>best_gain; best_gain[better]=contrib[better]; best_fam[better]=f
out['optionality']=opt; out['reachable_families']=breadth; out['best_add']=best_fam
# precedent thinness: how many same-hand pitcher-seasons within ±5° slot and ±0.5 HAVAA (excluding own pitcher)
thin=np.zeros(len(out))
for i in range(len(out)):
    m=(tr.p_throws.values==tr.p_throws.values[i])&(np.abs(tr.arm_angle.values-tr.arm_angle.values[i])<=5)&(np.abs(X.fb_havaa.values-X.fb_havaa.values[i])<=0.5)&(tr.pitcher.values!=tr.pitcher.values[i])
    thin[i]=m.sum()
out['n_precedent_pool']=thin
out.to_parquet(f'data/derived/precedent{SUF}.parquet',index=False)
# ---- backtest on additions
ad=pd.read_csv('data/derived/pitch_additions.csv')
m=ad.merge(out,on=['pitcher','game_year'],how='inner',suffixes=('','_p'))
def rank_hit(r,k):
    cand=[(r[f'prec_{f}'],f) for f in FAM if r[f'use_{f}']<0.02]
    cand.sort(reverse=True); return r.fg_type in [f for _,f in cand[:k]]
top1=m.apply(lambda r:rank_hit(r,1),axis=1).mean(); top2=m.apply(lambda r:rank_hit(r,2),axis=1).mean()
# base rate: same but using league-wide add frequency by slot tercile
tr['slot_bin']=pd.qcut(tr.arm_angle,3,labels=['low','mid','high']); m=m.merge(tr[['pitcher','game_year','slot_bin']],on=['pitcher','game_year'])
base=m.groupby('slot_bin',observed=True).fg_type.value_counts(normalize=True)
def base_hit(r,k):
    order=[f for f in base[r.slot_bin].index if r[f'use_{f}']<0.02]; return r.fg_type in order[:k]
b1=m.apply(lambda r:base_hit(r,1),axis=1).mean(); b2=m.apply(lambda r:base_hit(r,2),axis=1).mean()
print(f"additions matched {len(m)} | precedent top1 {top1:.2f} top2 {top2:.2f} | slot-bucket base top1 {b1:.2f} top2 {b2:.2f}")
# quality: precedent Stf+ of the added family vs realized
q=m.apply(lambda r:r[f"pstf_{r.fg_type}"],axis=1); ok=q.notna()&m.stf_next.notna()
print(f"added-pitch quality: r(precedent Stf+, realized Stf+) = {np.corrcoef(q[ok],m.stf_next[ok])[0,1]:.3f} (n={ok.sum()})")
for nm in ['Yesavage','Palmquist']:
    r=out[out.player_name.str.contains(nm)].sort_values('game_year').iloc[-1]
    print(f"\n{r.player_name} {int(r.game_year)}: slot {r.arm_angle:.1f}, HAVAA {r.fb_havaa:+.2f}, eff4 {r.eff4:.2f}, class {r.suppro_class}, Stuff+ {r.sp_stuff:.0f}, optionality {r.optionality:.1f}, reachable roles {int(r.reachable_families)}, best add {r.best_add or '-'}, precedent pool n={int(r.n_precedent_pool)}")
    print('  '+' | '.join(f"{f}: use {r[f'use_{f}']*100:.0f}% prec {r[f'prec_{f}']:.2f} pStf {r[f'pstf_{f}']:.0f}" for f in FAM))
print('\noptionality by slot quintile:'); out['q']=pd.qcut(out.arm_angle,5); print(out.groupby('q',observed=True)[['optionality','reachable_families','n_precedent_pool']].mean().round(2))
