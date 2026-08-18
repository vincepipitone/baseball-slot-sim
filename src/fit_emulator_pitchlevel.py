"""Pitch-level Stuff+ emulator: each pitch gets its pitcher-season-fgtype Stf+ as target;
predictions averaged back to pitcher-season-fgtype and scored (grouped by pitcher / temporal)."""
import numpy as np, pandas as pd, lightgbm as lgb, warnings
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
FG_MAP={'ST':'SL','SV':'SL','SL':'SL','CS':'CU','CU':'CU','KC':'KC','FF':'FF','SI':'SI','FC':'FC','FS':'FS','CH':'CH','FO':'FO'}
p=pd.read_parquet('data/derived/pitches.parquet',columns=['pitcher','player_name','p_throws','game_year','pitch_type','release_speed','IVB','HB','VAA','HAA','VRA','HRA','VAA_AA_pt','HAA_AA_pt','arm_angle','release_extension','release_pos_x','release_pos_z','release_spin_rate','spin_axis','AzOE','AxOE','PythagOE','ax','az','plate_z'])
p['fg_type']=p.pitch_type.map(FG_MAP); p=p[p.fg_type.notna()&p.arm_angle.notna()&p.release_speed.notna()]
tab=pd.read_parquet('data/derived/emulator_table.parquet')
tab=tab[(tab.n>=50)&tab.stf.notna()]
fb=tab[['pitcher','game_year','fb_velo','fb_IVB','fb_HB_arm','primary_fb']].drop_duplicates(['pitcher','game_year'])
p=p.merge(tab[['pitcher','game_year','fg_type','stf','n']],on=['pitcher','game_year','fg_type']).merge(fb,on=['pitcher','game_year'],how='left')
# cap pitches per row so big samples don't dominate
p=p.sample(frac=1,random_state=1); p['_r']=p.groupby(['pitcher','game_year','fg_type']).cumcount(); p=p[p._r<250].drop(columns='_r')
p['HB_arm']=np.where(p.p_throws=='R',-p.HB,p.HB); p['rx_arm']=np.where(p.p_throws=='R',-p.release_pos_x,p.release_pos_x)
p['d_velo']=p.release_speed-p.fb_velo; p['d_IVB']=p.IVB-p.fb_IVB; p['d_HB']=p.HB_arm-p.fb_HB_arm
p['is_primary_fb']=(p.fg_type==p.primary_fb).astype(int); p['hand']=(p.p_throws=='R').astype(int)
p['move_axis']=np.degrees(np.arctan2(p.HB_arm,p.IVB)); p['axis_minus_slot']=p.move_axis-p.arm_angle
p['fg_type_c']=p.fg_type.astype('category')
F=['release_speed','IVB','HB_arm','VAA','VAA_AA_pt','HAA','HAA_AA_pt','VRA','HRA','arm_angle','release_extension','release_pos_z','rx_arm',
   'release_spin_rate','spin_axis','AzOE','AxOE','PythagOE','move_axis','axis_minus_slot','d_velo','d_IVB','d_HB','is_primary_fb','fg_type_c','hand']
P=dict(objective='regression',learning_rate=0.05,num_leaves=63,min_data_in_leaf=200,feature_fraction=0.8,bagging_fraction=0.7,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1,num_threads=8)
def r2(y,pr,w): return 1-np.average((y-pr)**2,weights=w)/np.average((y-np.average(y,weights=w))**2,weights=w)
def score(mask_te,pred,label):
    d=p.loc[mask_te,['pitcher','game_year','fg_type','stf','n']].copy(); d['pred']=pred
    a=d.groupby(['pitcher','game_year','fg_type']).agg(stf=('stf','first'),n=('n','first'),pred=('pred','mean')).reset_index()
    print(f"{label}: r2 {r2(a.stf.values,a.pred.values,a.n.values):.3f} (rows {len(a)})",flush=True); return a
X=p[F]; y=p.stf.values; g=p.pitcher.values
print('pitches',len(p))
oos=np.zeros(len(p))
for tr,te in GroupKFold(5).split(X,y,g):
    oos[te]=lgb.train(P,lgb.Dataset(X.iloc[tr],y[tr]),400).predict(X.iloc[te])
a=score(np.ones(len(p),bool),oos,'grouped-OOS (5-fold by pitcher)')
tr=(p.game_year<=2025).values; m=lgb.train(P,lgb.Dataset(X[tr],y[tr]),400)
score(~tr,m.predict(X[~tr]),'temporal 2026')
seen=set(p.pitcher[tr]); te2=(~tr)&(~p.pitcher.isin(seen)).values
score(te2,m.predict(X[te2]),'temporal 2026 new pitchers')
a.to_parquet('data/derived/emulator_pitchlevel_oos.parquet',index=False)
imp=pd.Series(m.feature_importance('gain'),index=F).sort_values(ascending=False); print((imp/imp.sum()).round(3).head(12).to_string())
