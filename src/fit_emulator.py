"""Stuff+ emulator: FG per-pitch Stf+ ~ Statcast shape. Eval per leakage protocol:
in-sample vs grouped K-fold (pitcher_id) vs temporal (2024-25 -> 2026); ablations."""
import numpy as np, pandas as pd, lightgbm as lgb, warnings, sys
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
MIN_N=int(sys.argv[1]) if len(sys.argv)>1 else 50
t=pd.read_parquet('data/derived/emulator_table.parquet')
t=t[(t.n>=MIN_N)&t.stf.notna()&t.arm_angle.notna()].copy()
t['rx_arm']=np.where(t.p_throws=='R',-t.release_pos_x,t.release_pos_x)
t['fg_type_c']=t.fg_type.astype('category'); t['hand']=(t.p_throws=='R').astype(int)
BASE=['release_speed','IVB','HB_arm','VAA','VAA_AA_pt','HAA','HAA_AA_pt','VRA','HRA','arm_angle','release_extension',
      'release_pos_z','rx_arm','release_spin_rate','bauer','spin_axis','AzOE','AxOE','PythagOE','move_axis','axis_minus_slot',
      'd_velo','d_IVB','d_HB','is_primary_fb','fg_type_c','hand','sd_IVB','sd_HB','sd_velo','sd_release_x','sd_release_z']
P=dict(objective='regression',learning_rate=0.03,num_leaves=15,min_data_in_leaf=40,feature_fraction=0.8,bagging_fraction=0.8,bagging_freq=1,lambda_l2=5,verbose=-1,seed=1)
def fit(X,y,w): return lgb.train(P,lgb.Dataset(X,y,weight=w),num_boost_round=600)
def r2(y,p,w): return 1-np.average((y-p)**2,weights=w)/np.average((y-np.average(y,weights=w))**2,weights=w)
def evaluate(feats,label):
    X=t[feats]; y=t.stf.values; w=t.n.values; g=t.pitcher.values
    m=fit(X,y,w); ins=r2(y,m.predict(X),w)
    oos=np.zeros(len(y))
    for tr,te in GroupKFold(10).split(X,y,g):
        oos[te]=fit(X.iloc[tr],y[tr],w[tr]).predict(X.iloc[te])
    grp=r2(y,oos,w)
    tr=(t.game_year<=2025).values; te=~tr
    tmp=r2(y[te],fit(X[tr],y[tr],w[tr]).predict(X[te]),w[te])
    # temporal AND grouped: 2026 pitchers not seen in 2024-25
    seen=set(t.pitcher[tr]); te2=te&(~t.pitcher.isin(seen)).values
    tmp2=r2(y[te2],fit(X[tr],y[tr],w[tr]).predict(X[te2]),w[te2]) if te2.sum()>50 else np.nan
    print(f"{label:28s} in-sample {ins:.3f} | grouped-OOS {grp:.3f} | gap {ins-grp:+.3f} | temporal26 {tmp:.3f} | temporal26 new pitchers {tmp2:.3f} (n={te2.sum()})",flush=True)
    return oos
print(f"rows {len(t)}  pitchers {t.pitcher.nunique()}  min_n {MIN_N}")
oos=evaluate(BASE,'baseline')
t['oos_pred']=oos
for drop in [['rx_arm'],['release_pos_z'],['release_extension'],['sd_release_x','sd_release_z'],['AzOE','AxOE','PythagOE'],
             ['rx_arm','release_pos_z','release_extension','sd_release_x','sd_release_z']]:
    evaluate([f for f in BASE if f not in drop],'drop '+'+'.join(drop))
# per-pitch-type OOS r2 and Palmquist/Yesavage
for ft,g in t.groupby('fg_type'):
    if len(g)>100: print(f"  {ft}: grouped-OOS r2 {r2(g.stf.values,g.oos_pred.values,g.n.values):.3f} (rows {len(g)})")
for nm in ['Palmquist','Yesavage']:
    print(t[t.player_name.str.contains(nm)][['player_name','game_year','fg_type','n','stf','oos_pred']].round(1).to_string(index=False))
t[['pitcher','player_name','game_year','fg_type','n','stf','oos_pred']].to_parquet('data/derived/emulator_oos.parquet',index=False)
