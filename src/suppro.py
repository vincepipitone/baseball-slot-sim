"""Supination/pronation classifier per pitcher-season from Savant spin-direction data + Statcast shape.
Rules from docs/RESEARCH-supination-pronation.md (Rosen thresholds, Tread sweeper tell, SSW deviation, slot residual).
Output data/derived/suppro.parquet: eff4, eff4_mb, axis_res, si_dev, ch_dev, sweeper_cap, pro_pts, sup_pts, suppro_class"""
import numpy as np, pandas as pd
sv=pd.read_csv('data/derived/savant_spin.csv')
t=pd.read_parquet('data/derived/emulator_table.parquet')
ps=t.groupby(['pitcher','game_year']).apply(lambda g: pd.Series({'p_throws':g.p_throws.iloc[0],'player_name':g.player_name.iloc[0],
    'arm_angle':np.average(g.arm_angle.fillna(g.arm_angle.mean()),weights=g.n) if g.arm_angle.notna().any() else np.nan,
    'n_tot':g.n.sum()})).reset_index()
def get(pt,col,name):
    d=sv[sv.pitch_type==pt][['pitcher','game_year',col]].rename(columns={col:name}); return d
ps=ps.merge(get('FF','active_spin','eff4'),how='left').merge(get('FF','alan_active_spin_pct','eff4_mb'),how='left')\
     .merge(get('FF','hawkeye_measured','ff_axis'),how='left').merge(get('FF','spin_rate','ff_spin'),how='left')\
     .merge(get('SI','diff_measured_inferred','si_dev'),how='left').merge(get('CH','diff_measured_inferred','ch_dev'),how='left')\
     .merge(get('SI','active_spin','effsi'),how='left')
# expected 4S axis by slot: RHP 180+(90-slot) (12:00 over top → 3:00 sidearm), LHP mirrored; residual signed so + = more run than slot implies
# data-driven expected 4S axis given slot, per hand (Savant clock convention differs from naive); residual signed so + = more RUN than slot implies
ps['axis_res']=np.nan
for h in ['R','L']:
    m=(ps.p_throws==h)&ps.ff_axis.notna()&ps.arm_angle.notna()&(ps.n_tot>=200)
    b,a=np.polyfit(ps.arm_angle[m],ps.ff_axis[m],1)
    r=ps.ff_axis-(a+b*ps.arm_angle)
    # as slot drops (more sidearm) the axis moves toward run: run direction = -sign(b)
    ps.loc[ps.p_throws==h,'axis_res']=(r*(-np.sign(b)))[ps.p_throws==h]
    print(f'hand {h}: axis = {a:.1f} + {b:.2f}*arm_angle  (run direction sign {-np.sign(b):+.0f})')
# sweeper capability from shape table: SL/ST family with |HB|>=12 and velo gap <=10 vs FB
sl=t[t.fg_type=='SL'].copy(); sl['sweep_cap']=((sl.HB_arm.abs()>=12)&(sl.d_velo.abs()<=10)&(sl.n>=50)).astype(int)
ps=ps.merge(sl.groupby(['pitcher','game_year']).sweep_cap.max().reset_index(),how='left'); ps['sweep_cap']=ps.sweep_cap.fillna(0)
# also which families thrown
use=t.pivot_table(index=['pitcher','game_year'],columns='fg_type',values='usage',aggfunc='first').fillna(0)
for f in ['FS','CH','FC','CU','KC','SI','SL']:
    ps=ps.merge(use[f].rename(f'use_{f}').reset_index(),how='left') if f in use else ps
e=ps.eff4
pro=(e>=0.95).astype(int)+(ps.axis_res>10).astype(int)+((ps.use_CH.fillna(0)+ps.use_FS.fillna(0)>=0.08)&(ps.sweep_cap==0)).astype(int)
sup=(e<0.90).astype(int)+(ps.axis_res<-10).astype(int)+(ps.si_dev.abs()>=15).astype(int)+((ps.sweep_cap==1)|(ps.use_FC.fillna(0)>=0.08)|(ps.use_CU.fillna(0)+ps.use_KC.fillna(0)>=0.08)).astype(int)
ps['pro_pts']=pro; ps['sup_pts']=sup
def cls(r):
    if pd.isna(r.eff4): return 'unknown'
    if r.eff4>=0.95 and r.pro_pts>=r.sup_pts: return 'pronator'
    if r.eff4<0.90 and r.sup_pts>=r.pro_pts: return 'supinator'
    if 0.80<=r.eff4<0.90 and (r.ff_spin or 0)>=2350: return 'hybrid'
    if r.pro_pts>r.sup_pts: return 'lean_pronator'
    if r.sup_pts>r.pro_pts: return 'lean_supinator'
    return 'hybrid'
ps['suppro_class']=ps.apply(cls,axis=1)
ps.to_parquet('data/derived/suppro.parquet',index=False)
q=ps[ps.n_tot>=200]
print(q.suppro_class.value_counts().to_dict())
print(q.groupby('suppro_class')[['eff4','axis_res','si_dev','sweep_cap','arm_angle']].mean().round(2))
# stability y2y of eff4 and class
prev=q[['pitcher','game_year','eff4','suppro_class']].copy(); prev['game_year']+=1
m=q.merge(prev,on=['pitcher','game_year'],suffixes=('','_prev'))
print('eff4 Y2Y r² %.2f | class same-next-year %.2f (n=%d)' % (m[['eff4','eff4_prev']].corr().iloc[0,1]**2,(m.suppro_class==m.suppro_class_prev).mean(),len(m)))
print(q[q.player_name.str.contains('Palmquist|Yesavage|Hancock, Emerson')][['player_name','game_year','arm_angle','eff4','eff4_mb','axis_res','si_dev','sweep_cap','pro_pts','sup_pts','suppro_class']].round(2).sort_values(['player_name','game_year']).to_string(index=False))
