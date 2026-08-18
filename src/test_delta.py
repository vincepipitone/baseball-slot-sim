"""Within-pitcher delta test: does OOS emulator pred(new shape) - pred(old shape) track realized ΔStf+?"""
import pandas as pd, numpy as np
o=pd.read_parquet('data/derived/emulator_oos.parquet')
t=pd.read_parquet('data/derived/emulator_table.parquet')[['pitcher','game_year','fg_type','arm_angle','n']]
o=o.merge(t,on=['pitcher','game_year','fg_type','n']); o=o[o.n>=100]
a=o.copy(); a['game_year']+=1
m=a.merge(o,on=['pitcher','fg_type','game_year'],suffixes=('_prev',''))
m['d_act']=m.stf-m.stf_prev; m['d_pred']=m.oos_pred-m.oos_pred_prev; m['d_slot']=m.arm_angle-m.arm_angle_prev
def rep(d,label):
    r=np.corrcoef(d.d_act,d.d_pred)[0,1]; b=np.polyfit(d.d_pred,d.d_act,1)[0]
    print(f"{label:34s} n={len(d):4d}  r(Δpred,Δact)={r:.3f}  slope={b:.2f}  sd Δact={d.d_act.std():.1f} sd Δpred={d.d_pred.std():.1f}")
rep(m,'all consecutive-season pitches'); rep(m[m.d_slot.abs()>=5],'|Δslot|>=5°'); rep(m[m.d_slot>=5],'  steeper >=5°'); rep(m[m.d_slot<=-5],'  flatter >=5°'); rep(m[m.d_slot.abs()<1],'|Δslot|<1°')
for ft,g in m.groupby('fg_type'):
    if len(g)>100: rep(g,f'  {ft}')
print(m[m.player_name_prev.str.contains('Palmquist')][['game_year','fg_type','stf_prev','stf','oos_pred_prev','oos_pred','d_slot']].round(1).to_string(index=False))
