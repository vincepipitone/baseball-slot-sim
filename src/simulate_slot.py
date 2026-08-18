"""Slot counterfactual engine. For each pitcher-season: shift arm angle by δ ∈ [-10,+10], transform every pitch's
shape with the fitted per-family transfer slopes (release z, rx, VRA, HRA, IVB, HB, measured axis, VAA_AA_pt),
carry active spin / dead-zone / velo unchanged (no slot dependence found), rescore with the own Stuff model (B),
aggregate usage-weighted. Validation: on actual slot changers, predicted ΔStuff at their realized Δslot vs realized ΔStuff."""
import numpy as np, pandas as pd, sys, warnings
sys.path.insert(0,'src'); import stuff_model as SM
warnings.filterwarnings('ignore')
FG={'ST':'SL','SV':'SL','SL':'SL','CS':'CU','CU':'CU','KC':'KC','FF':'FF','SI':'SI','FC':'FC','FS':'FS','CH':'CH','FO':'FO'}
fits=pd.read_csv('data/derived/transfer_fits.csv')
SLOPE={(r.fam,r['var']):r.slope_per_deg for _,r in fits.iterrows()}
def slope(fam,var):
    if (fam,var) in SLOPE: return SLOPE[(fam,var)]
    return fits[fits['var']==var].slope_per_deg.median()
TRANSFORM=['release_pos_z','rx_arm','VRA','HRA','IVB','HB_arm','axis_m','VAA_AA_pt']
def transform(p,delta):
    q=p.copy()
    q['arm_angle']=q.arm_angle+delta
    for v in TRANSFORM:
        s=q.fg_type.map(lambda f: slope(f,v)); q[v]=q[v]+s*delta
    # recompute differentials vs primary fastball after transform
    fb=q[q.is_primary_fb==1].groupby(['pitcher','game_year']).agg(fb_velo=('release_speed','mean'),fb_IVB=('IVB','mean'),fb_HB=('HB_arm','mean')).reset_index()
    q=q.drop(columns=['fb_velo','fb_IVB','fb_HB']).merge(fb,on=['pitcher','game_year'],how='left')
    q['d_velo']=q.release_speed-q.fb_velo; q['d_IVB']=q.IVB-q.fb_IVB; q['d_HB']=q.HB_arm-q.fb_HB
    return q
if __name__=='__main__':
    m,scale=SM.load()
    p=SM.engineer(SM.load_pitches()); p['fg_type']=p.pitch_type.map(FG); p=p[p.fg_type.notna()&p.arm_angle.notna()]
    p=p[p.game_year>=2020]
    # cap per pitcher-season for speed
    p=p.sample(frac=1,random_state=1); p['_r']=p.groupby(['pitcher','game_year']).cumcount(); p=p[p._r<400].drop(columns='_r')
    deltas=list(range(-10,11,1))
    out=[]
    for d in deltas:
        q=transform(p,d) if d!=0 else p
        s=SM.score(m,scale,q)
        agg=pd.DataFrame({'pitcher':q.pitcher.values,'game_year':q.game_year.values,'stuff':s}).groupby(['pitcher','game_year']).stuff.mean().rename(f'stuff_{d:+d}')
        out.append(agg); print('delta',d,flush=True)
    R=pd.concat(out,axis=1).reset_index()
    names=p.groupby(['pitcher','game_year']).agg(player_name=('player_name','first'),arm_angle=('arm_angle','mean'),n=('pitch_type','size')).reset_index()
    R=R.merge(names,on=['pitcher','game_year'])
    cols=[f'stuff_{d:+d}' for d in deltas]
    R['best_delta']=R[cols].idxmax(axis=1).str.replace('stuff_','').astype(int)
    R['stuff_now']=R['stuff_+0']; R['stuff_best']=R[cols].max(axis=1); R['gain']=R.stuff_best-R.stuff_now
    R.to_parquet('data/derived/slot_sim.parquet',index=False)
    print(R[['best_delta']].value_counts().sort_index().to_string())
    print('mean gain %.2f | median %.2f | p90 %.2f' % (R.gain.mean(),R.gain.median(),R.gain.quantile(.9)))
    for nm in ['Palmquist','Yesavage']:
        r=R[R.player_name.str.contains(nm)]
        print(r[['player_name','game_year','arm_angle','stuff_now','stuff_-5','stuff_+5','best_delta','stuff_best','gain']].round(1).to_string(index=False))
    # validation on slot changers: predicted Δ at realized Δslot vs realized Δ (own model, and FG)
    ch=pd.read_csv('data/derived/slot_changers.csv')
    own=pd.read_parquet('data/derived/stuff_rv_pitcher_season.parquet')[['pitcher','game_year','stuff_B_plus_oos','sp_stuff']]
    v=ch.merge(R,on=['pitcher','game_year'],suffixes=('','_sim'))
    def pick(r):
        d=int(np.clip(round(r.d_slot),-10,10)); return r[f'stuff_{d:+d}']-r['stuff_+0']
    v['pred_d']=v.apply(pick,axis=1)
    o1=own.copy(); o2=own.copy(); o2['game_year']-=1
    v=v.merge(o1,on=['pitcher','game_year'],how='left').merge(o2,on=['pitcher','game_year'],how='left',suffixes=('','_next'))
    v['d_own']=v.stuff_B_plus_oos_next-v.stuff_B_plus_oos; v['d_fg']=v.stuff_next-v.stuff
    for lab,col in [('own-model ΔStuff','d_own'),('FG ΔStuff+','d_fg')]:
        d=v[[col,'pred_d','d_slot']].dropna(); r=np.corrcoef(d[col],d.pred_d)[0,1]; b=np.polyfit(d.pred_d,d[col],1)[0]
        print(f"changers ≥5°: r(pred Δ, realized {lab}) = {r:.3f}, slope {b:.2f}, n={len(d)} | steeper r {np.corrcoef(d[d.d_slot>0][col],d[d.d_slot>0].pred_d)[0,1]:.3f} flatter r {np.corrcoef(d[d.d_slot<0][col],d[d.d_slot<0].pred_d)[0,1]:.3f}")
    print(v[v.player_name.str.contains('Palmquist|Hancock')][['player_name','game_year','d_slot','pred_d','d_own','d_fg']].round(1).to_string(index=False))
