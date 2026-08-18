"""Module 2: slot -> shape transfer function, fit on consecutive-season pitcher x pitch-family pairs.
Targets: Δ of IVB, HB_arm, release_pos_z, rx_arm, VRA, HRA, VAA, spin_axis (measured, mirrored), release_speed, active_spin.
Models: (a) per-family linear in Δslot (+ Δslot×slot0), (b) physics rotation for movement: (IVB,HB) rotated by k·Δslot with
magnitude preserved. Grouped-by-pitcher 10-fold OOS r² on |Δslot|>=3° pairs, both directions."""
import numpy as np, pandas as pd, warnings
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
warnings.filterwarnings('ignore')
t=pd.read_parquet('data/derived/emulator_table.parquet')
sv=pd.read_csv('data/derived/savant_spin.csv')
FG={'ST':'SL','SV':'SL','SL':'SL','CS':'CU','CU':'CU','KC':'KC','FF':'FF','SI':'SI','FC':'FC','FS':'FS','CH':'CH','FO':'FO'}
sv['fg_type']=sv.pitch_type.map(FG); sv=sv[sv.fg_type.notna()]
sv=sv.sort_values('n_pitches',ascending=False).drop_duplicates(['pitcher','game_year','fg_type'])[['pitcher','game_year','fg_type','active_spin','hawkeye_measured','diff_measured_inferred']]
t=t.merge(sv,on=['pitcher','game_year','fg_type'],how='left')
t['axis_m']=np.where(t.p_throws=='R',t.hawkeye_measured,360-t.hawkeye_measured)
t['rx_arm']=np.where(t.p_throws=='R',-t.release_pos_x,t.release_pos_x)
t=t[(t.n>=50)&t.arm_angle.notna()]
V=['IVB','HB_arm','release_pos_z','rx_arm','VRA','HRA','VAA','VAA_AA_pt','axis_m','release_speed','active_spin','release_extension','AzOE','AxOE']
a=t.copy(); a['game_year']+=1
m=a.merge(t,on=['pitcher','fg_type','game_year'],suffixes=('0',''))
m['d_slot']=m.arm_angle-m.arm_angle0
for v in V: m['d_'+v]=m[v]-m[v+'0']
m['hand']=(m.p_throws0=='R').astype(int)
print(f"pairs {len(m)} | |Δslot|>=3: {(m.d_slot.abs()>=3).sum()} | >=5: {(m.d_slot.abs()>=5).sum()}")
def r2(y,p): return 1-np.sum((y-p)**2)/np.sum((y-y.mean())**2)
rows=[]
for fam,g in m.groupby('fg_type'):
    if len(g)<150: continue
    for v in V:
        d=g[['d_slot','arm_angle0','hand','pitcher','d_'+v,v+'0']].dropna()
        if len(d)<120: continue
        X=np.c_[d.d_slot,d.d_slot*d.arm_angle0,d.d_slot*d.hand,d.hand,d.arm_angle0]
        y=d['d_'+v].values; oos=np.zeros(len(d))
        for tr,te in GroupKFold(10).split(X,y,d.pitcher):
            oos[te]=Ridge(alpha=1.0).fit(X[tr],y[tr]).predict(X[te])
        big=(d.d_slot.abs()>=3).values
        slope=Ridge(alpha=1.0).fit(X,y).coef_[0]
        rows.append(dict(fam=fam,var=v,n=len(d),n_big=int(big.sum()),slope_per_deg=slope,r2_all=r2(y,oos),r2_big=r2(y[big],oos[big]) if big.sum()>30 else np.nan,
                         r2_flatter=r2(y[big&(d.d_slot.values<0)],oos[big&(d.d_slot.values<0)]) if (big&(d.d_slot.values<0)).sum()>20 else np.nan,
                         r2_steeper=r2(y[big&(d.d_slot.values>0)],oos[big&(d.d_slot.values>0)]) if (big&(d.d_slot.values>0)).sum()>20 else np.nan))
R=pd.DataFrame(rows); R.to_csv('data/derived/transfer_fits.csv',index=False)
pd.set_option('display.width',200)
print(R[R['var'].isin(['IVB','HB_arm','release_pos_z','VRA','VAA','axis_m','active_spin','release_speed'])].pivot(index='var',columns='fam',values='r2_big').round(2))
print('\nslope per degree of slot (units per °):'); print(R[R['var'].isin(['IVB','HB_arm','release_pos_z','VRA','VAA','axis_m','active_spin','release_speed'])].pivot(index='var',columns='fam',values='slope_per_deg').round(3))
# physics rotation model for movement (all families pooled): rotate (IVB, HB_arm) by k*Δslot degrees, keep magnitude
d=m[['d_slot','IVB0','HB_arm0','IVB','HB_arm','pitcher','fg_type']].dropna(); big=d.d_slot.abs()>=3
def rot_pred(k,dd):
    th=np.radians(k*dd.d_slot.values); c,s=np.cos(th),np.sin(th)
    # movement axis angle from vertical: atan2(HB_arm, IVB); flatter slot (Δ<0) → axis toward horizontal (HB up, IVB down)
    ivb=dd.IVB0.values*c + dd.HB_arm0.values*s*(-1)*(-1)  # rotate toward run when Δslot<0
    hb =dd.HB_arm0.values*c - dd.IVB0.values*s
    return ivb,hb
best=None
for k in np.arange(0.2,1.61,0.1):
    ivb,hb=rot_pred(k,d[big]); e=np.mean((d.IVB[big]-ivb)**2+(d.HB_arm[big]-hb)**2)
    if best is None or e<best[1]: best=(k,e)
k=best[0]; ivb,hb=rot_pred(k,d[big])
print(f"\nrotation model: best k={k:.1f} (axis rotates {k:.1f}° per 1° slot) | ΔIVB r² {r2(d.IVB[big]-d.IVB0[big],ivb-d.IVB0[big]):.2f} | ΔHB r² {r2(d.HB_arm[big]-d.HB_arm0[big],hb-d.HB_arm0[big]):.2f} (|Δslot|>=3, n={big.sum()})")
m.to_parquet('data/derived/transfer_pairs.parquet',index=False)
