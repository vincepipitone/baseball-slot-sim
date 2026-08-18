"""Reusable pieces of the own run-value Stuff model: feature engineering, training on all data, scoring."""
import numpy as np, pandas as pd, xgboost as xgb, json, os
COLS=['pitcher','player_name','p_throws','stand','game_year','pitch_type','release_speed','IVB','HB','release_pos_x','release_pos_z','release_extension',
      'release_spin_rate','spin_axis','arm_angle','VRA','HRA','VAA_AA_pt','AzOE','AxOE','delta_run_exp','woba_value']
FEATS_B=['release_speed','IVB','HB_arm','release_pos_z','rx_arm','release_extension','release_spin_rate','d_velo','d_IVB','d_HB','is_primary_fb',
         'arm_angle','VAA_AA_pt','axis_m','VRA','HRA','AzOE','AxOE','active_spin','alan_active_spin_pct','diff_measured_inferred']
PARAMS=dict(objective='reg:squarederror',tree_method='hist',max_depth=7,eta=0.03,subsample=0.8,colsample_bytree=0.8,min_child_weight=200,reg_lambda=10,nthread=8)
ROUNDS=900
def load_pitches():
    p=pd.read_parquet('data/derived/pitches.parquet',columns=COLS)
    p=p[p.release_speed.notna()&p.IVB.notna()&p.release_pos_z.notna()&p.release_extension.notna()].copy()
    return p
def engineer(p):
    """Add derived + pitcher-season context features. p must have the COLS columns."""
    p=p.copy()
    p['HB_arm']=np.where(p.p_throws=='R',-p.HB,p.HB); p['rx_arm']=np.where(p.p_throws=='R',-p.release_pos_x,p.release_pos_x)
    p['axis_m']=np.where(p.p_throws=='R',p.spin_axis,360-p.spin_axis)
    fbm=p[p.pitch_type.isin(['FF','SI','FC'])].groupby(['pitcher','game_year','pitch_type']).size().reset_index(name='k').sort_values('k',ascending=False).drop_duplicates(['pitcher','game_year'])
    fbm=fbm.rename(columns={'pitch_type':'primary_fb'})[['pitcher','game_year','primary_fb']]
    p=p.merge(fbm,on=['pitcher','game_year'],how='left')
    fbstats=p[p.pitch_type==p.primary_fb].groupby(['pitcher','game_year']).agg(fb_velo=('release_speed','mean'),fb_IVB=('IVB','mean'),fb_HB=('HB_arm','mean')).reset_index()
    p=p.merge(fbstats,on=['pitcher','game_year'],how='left')
    p['d_velo']=p.release_speed-p.fb_velo; p['d_IVB']=p.IVB-p.fb_IVB; p['d_HB']=p.HB_arm-p.fb_HB
    p['is_primary_fb']=(p.pitch_type==p.primary_fb).astype(int)
    sv=pd.read_csv('data/derived/savant_spin.csv')[['pitcher','game_year','pitch_type','active_spin','alan_active_spin_pct','diff_measured_inferred']]
    p=p.merge(sv,on=['pitcher','game_year','pitch_type'],how='left')
    return p
def target(p):
    rv=-p.delta_run_exp
    return rv-rv.groupby([p.p_throws,p.stand,p.game_year]).transform('mean')
def train_and_save(path='data/derived/stuff_model_B.json', years=None):
    p=engineer(load_pitches()); p=p[p.delta_run_exp.notna()]
    if years is not None: p=p[p.game_year.isin(years)]
    y=target(p).values
    m=xgb.train(PARAMS,xgb.DMatrix(p[FEATS_B],y),ROUNDS); m.save_model(path)
    pred=m.predict(xgb.DMatrix(p[FEATS_B]))
    scale=pd.DataFrame({'y':p.game_year.values,'pred':pred}).groupby('y').pred.agg(['mean','std'])
    scale.to_json(path.replace('.json','_scale.json'))
    return m,scale
def load(path='data/derived/stuff_model_B.json'):
    m=xgb.Booster(); m.load_model(path); scale=pd.read_json(path.replace('.json','_scale.json'))
    return m,scale
def score(m,scale,df,year_col='game_year'):
    """Return Stuff index (100/10 per season scaling) for engineered rows."""
    pred=m.predict(xgb.DMatrix(df[FEATS_B]))
    mu=df[year_col].map(scale['mean']).values; sd=df[year_col].map(scale['std']).values
    return 100+10*(pred-mu)/sd
if __name__=='__main__':
    m,scale=train_and_save(); print('saved; scale:\n',scale.round(4))
