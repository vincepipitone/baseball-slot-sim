"""Slot lever v2: value of the PRECEDENT ARSENAL available at slot (current + δ), same hand, similar 4S efficiency.
For each family: precedent shape + precedent Stf+ (usage-weighted FG Stf+ of comps throwing it >=10%). Pitcher keeps his own
pitch when his Stf+ >= precedent (his outlier stuff), else the precedent pitch is 'available'. Arsenal value at slot s =
usage-weighted over top families by (precedent share x value). Reports gain vs current, best δ, and the 'unrealized pitch'
distance (own shape vs precedent shape at own slot). Validation on slot changers."""
import numpy as np, pandas as pd, sys
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
ROLE={'FF':'ride','SI':'run','FC':'cut','FS':'offspeed','CH':'offspeed','SL':'slider','CU':'curve','KC':'curve'}
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[(t.n>=50)&t.arm_angle.notna()&t.stf.notna()]
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4','suppro_class']]; t=t.merge(sp,how='left')
GROUP={'pronator':'P','lean_pronator':'P','supinator':'S','lean_supinator':'S','hybrid':'H','unknown':'H'}; t['grp']=t.suppro_class.fillna('unknown').map(GROUP)
ps=t.groupby(['pitcher','game_year']).agg(player_name=('player_name','first'),p_throws=('p_throws','first'),arm_angle=('arm_angle',lambda s: np.average(s,weights=t.loc[s.index,'n'])),
    n_tot=('n','sum'),eff4=('eff4','first'),grp=('grp','first'),stuff=('sp_stuff','first')).reset_index()
ps=ps[ps.n_tot>=300].reset_index(drop=True)
own=t.pivot_table(index=['pitcher','game_year'],columns='fg_type',values=['stf','usage','IVB','HB_arm'],aggfunc='first')
def prec_table(hand,slot,eff,grp,exclude):
    pool=t[(t.p_throws==hand)&(t.pitcher!=exclude)&((t.arm_angle-slot).abs()<=3)]
    if pd.notna(eff):
        p2=pool[(pool.eff4-eff).abs()<=0.06]; pool=p2 if p2.pitcher.nunique()>=8 else pool
    if grp!='H':
        p3=pool[pool.grp.isin([grp,'H'])]; pool=p3 if p3.pitcher.nunique()>=8 else pool
    npit=pool.pitcher.nunique()
    out={}
    for f in FAM:
        g=pool[(pool.fg_type==f)&(pool.usage>=0.10)]
        share=g.pitcher.nunique()/max(npit,1)
        out[f]=(share, np.average(g.stf,weights=g.n) if len(g)>=3 else np.nan, np.average(g.IVB,weights=g.n) if len(g)>=3 else np.nan, np.average(g.HB_arm,weights=g.n) if len(g)>=3 else np.nan)
    return out,npit
def arsenal_value(r,slot):
    tab,npit=prec_table(r.p_throws,slot,r.eff4,r.grp,r.pitcher)
    vals=[]
    for f in FAM:
        share,pstf,_,_=tab[f]
        try: ostf=own.loc[(r.pitcher,r.game_year),('stf',f)]; ouse=own.loc[(r.pitcher,r.game_year),('usage',f)]
        except KeyError: ostf,ouse=np.nan,0
        keep=(pd.notna(ostf) and ouse>=0.05)
        v=np.nanmax([ostf if keep else np.nan, pstf if share>=0.20 else np.nan])
        if np.isfinite(v): vals.append((f,v,share,keep))
    if not vals: return np.nan,npit,[]
    # take best pitch per role, up to 4 pitches, weight by value rank (simple usage-optimizer: 40/30/20/10)
    best={}
    for f,v,share,keep in vals:
        if ROLE[f] not in best or v>best[ROLE[f]][1]: best[ROLE[f]]=(f,v,share,keep)
    top=sorted(best.values(),key=lambda x:-x[1])[:4]; w=[0.4,0.3,0.2,0.1][:len(top)]
    return float(np.average([x[1] for x in top],weights=w)),npit,top
rows=[]
deltas=list(range(-10,11,2))
for i,r in ps.iterrows():
    res={}
    for d in deltas:
        v,npit,top=arsenal_value(r,r.arm_angle+d); res[d]=v
        if d==0: res['npit0']=npit; res['top0']=' '.join(f"{f}:{v:.0f}{'*' if k else ''}" for f,v,s,k in top)
    # unrealized-pitch distance at own slot: for pitches he throws >=5%, |own IVB - precedent IVB| + |own HB - precedent HB|
    tab,_=prec_table(r.p_throws,r.arm_angle,r.eff4,r.grp,r.pitcher); dist=[]
    for f in FAM:
        try: u=own.loc[(r.pitcher,r.game_year),('usage',f)]
        except KeyError: continue
        if u>=0.05 and pd.notna(tab[f][2]):
            dist.append((f,abs(own.loc[(r.pitcher,r.game_year),('IVB',f)]-tab[f][2])+abs(own.loc[(r.pitcher,r.game_year),('HB_arm',f)]-tab[f][3])))
    res['max_unrealized']=max([d for f,d in dist]) if dist else np.nan; res['unrealized_pitch']=max(dist,key=lambda x:x[1])[0] if dist else ''
    rows.append({**r.to_dict(),**res})
    if i%300==0: print(i,len(ps),flush=True)
R=pd.DataFrame(rows)
cols=[d for d in deltas]
R['value_now']=R[0]; R['best_delta']=R[cols].idxmax(axis=1); R['value_best']=R[cols].max(axis=1); R['gain']=R.value_best-R.value_now
R.to_parquet('data/derived/precedent_at_slot.parquet',index=False)
print(R.best_delta.value_counts().sort_index().to_dict())
print('gain: mean %.2f median %.2f p90 %.2f' % (R.gain.mean(),R.gain.median(),R.gain.quantile(.9)))
for nm in ['Palmquist','Yesavage','Hancock, Emerson']:
    print(R[R.player_name.str.contains(nm)][['player_name','game_year','arm_angle','eff4','grp','stuff','value_now','best_delta','value_best','gain','npit0','top0','unrealized_pitch','max_unrealized']].round(1).to_string(index=False))
# validation: changers — did realized ΔStuff+ correlate with predicted value at realized new slot minus value now?
ch=pd.read_csv('data/derived/slot_changers.csv')[['pitcher','game_year','d_slot','d_stuff','stuff','stuff_next']]
v=ch.merge(R,on=['pitcher','game_year'],suffixes=('_ch',''))
def at(r):
    d=int(2*round(np.clip(r.d_slot,-10,10)/2)); return r[d]-r[0]
v['pred']=v.apply(at,axis=1); d=v.dropna(subset=['pred','d_stuff'])
print(f"changers ≥5°: r(pred Δvalue at realized slot, realized FG ΔStuff+) = {np.corrcoef(d.pred,d.d_stuff)[0,1]:.3f} n={len(d)} | steeper {np.corrcoef(d[d.d_slot>0].pred,d[d.d_slot>0].d_stuff)[0,1]:.3f} flatter {np.corrcoef(d[d.d_slot<0].pred,d[d.d_slot<0].d_stuff)[0,1]:.3f}")
# does 'unrealized pitch distance' predict next-season ΔStuff+ in general?
nx=ps[['pitcher','game_year','stuff']].copy(); nx['game_year']-=1; nx.columns=['pitcher','game_year','stuff_next']
g=R.merge(nx,on=['pitcher','game_year']); g['d']=g.stuff_next-g.stuff; g=g.dropna(subset=['d','max_unrealized'])
print(f"all pitchers: r(max_unrealized, next-season ΔStuff+) = {np.corrcoef(g.max_unrealized,g.d)[0,1]:.3f} n={len(g)}; r(gain, ΔStuff+) = {np.corrcoef(g.gain,g.d)[0,1]:.3f}")
