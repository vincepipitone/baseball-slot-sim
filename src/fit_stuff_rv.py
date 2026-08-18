"""Own Stuff model: XGBoost on pitch-level physical shape -> run value (pitcher perspective), all pitches pooled,
no pitch-type label. Variants: A = FG-like features; B = A + arm angle, HAVAA, active spin, SSW deviation.
Indexed 100/10 per season. Eval at pitcher-season level: grouped-by-pitcher OOS, temporal; head-to-head vs FG Stuff+
predicting same-season and NEXT-season RV/100 and wOBA."""
import numpy as np, pandas as pd, xgboost as xgb, sys, warnings
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
COLS=['pitcher','player_name','p_throws','stand','game_year','pitch_type','release_speed','IVB','HB','release_pos_x','release_pos_z','release_extension',
      'release_spin_rate','spin_axis','arm_angle','VRA','HRA','VAA_AA_pt','AzOE','AxOE','delta_run_exp','woba_value','description','events']
p=pd.read_parquet('data/derived/pitches.parquet',columns=COLS)
p=p[p.delta_run_exp.notna()&p.release_speed.notna()&p.IVB.notna()&p.release_pos_z.notna()&p.release_extension.notna()].copy()
p['rv']=-p.delta_run_exp  # + = good for pitcher
# platoon/season adjustment: remove league mean RV by (pitcher hand, batter hand, year) so 'hand' isn't a stuff feature
p['rv']=p.rv-p.groupby(['p_throws','stand','game_year']).rv.transform('mean')
p['HB_arm']=np.where(p.p_throws=='R',-p.HB,p.HB); p['rx_arm']=np.where(p.p_throws=='R',-p.release_pos_x,p.release_pos_x)
p['axis_m']=np.where(p.p_throws=='R',p.spin_axis,360-p.spin_axis)  # mirror lefties
p['hand']=(p.p_throws=='R').astype(int)
# primary fastball per pitcher-season (most-used of FF/SI/FC) → differentials
fbm=p[p.pitch_type.isin(['FF','SI','FC'])].groupby(['pitcher','game_year','pitch_type']).size().reset_index(name='k').sort_values('k',ascending=False).drop_duplicates(['pitcher','game_year'])
fbm=fbm.rename(columns={'pitch_type':'primary_fb'})[['pitcher','game_year','primary_fb']]
p=p.merge(fbm,on=['pitcher','game_year'],how='left')
fbstats=p[p.pitch_type==p.primary_fb].groupby(['pitcher','game_year']).agg(fb_velo=('release_speed','mean'),fb_IVB=('IVB','mean'),fb_HB=('HB_arm','mean')).reset_index()
p=p.merge(fbstats,on=['pitcher','game_year'],how='left')
p['d_velo']=p.release_speed-p.fb_velo; p['d_IVB']=p.IVB-p.fb_IVB; p['d_HB']=p.HB_arm-p.fb_HB
p['is_primary_fb']=(p.pitch_type==p.primary_fb).astype(int)
# Savant active spin / SSW per pitcher-season-pitchtype
sv=pd.read_csv('data/derived/savant_spin.csv')[['pitcher','game_year','pitch_type','active_spin','alan_active_spin_pct','diff_measured_inferred']]
p=p.merge(sv,on=['pitcher','game_year','pitch_type'],how='left')
A=['release_speed','IVB','HB_arm','release_pos_z','rx_arm','release_extension','release_spin_rate','d_velo','d_IVB','d_HB','is_primary_fb']
B=A+['arm_angle','VAA_AA_pt','axis_m','VRA','HRA','AzOE','AxOE','active_spin','alan_active_spin_pct','diff_measured_inferred']
PARAMS=dict(objective='reg:squarederror',tree_method='hist',max_depth=7,eta=0.03,subsample=0.8,colsample_bytree=0.8,min_child_weight=200,reg_lambda=10,nthread=8)
ROUNDS=900
def fitpred(Xtr,ytr,Xte):
    m=xgb.train(PARAMS,xgb.DMatrix(Xtr,ytr),ROUNDS); return m.predict(xgb.DMatrix(Xte)),m
def index(pred,year):
    s=pd.Series(pred); mu=s.groupby(year).transform('mean'); sd=s.groupby(year).transform('std'); return (100+10*(s-mu)/sd).values
y=p.rv.values; g=p.pitcher.values; yr=p.game_year.values
res={}
for name,F in [('A_fglike',A),('B_plus',B)]:
    X=p[F]
    oos=np.zeros(len(p))
    for tr,te in GroupKFold(5).split(X,y,g):
        oos[te],_=fitpred(X.iloc[tr],y[tr],X.iloc[te])
    p[f'stuff_{name}_oos']=index(oos,yr)
    tr=yr<=2023; pt,m=fitpred(X[tr],y[tr],X); p[f'stuff_{name}_t23']=index(pt,yr)  # temporal: trained ≤2023, applied everywhere
    imp=pd.Series(m.get_score(importance_type='gain')).sort_values(ascending=False); res[name]=imp
    print(name,'done',flush=True)
# pitcher-season aggregation
agg=p.groupby(['pitcher','player_name','game_year']).agg(n=('rv','size'),rv100=('rv',lambda s:s.mean()*100),
    woba=('woba_value','mean'),**{c:(c,'mean') for c in p.columns if c.startswith('stuff_')}).reset_index()
fg=pd.read_csv('data/derived/fg_stuff.csv')[['pitcher','game_year','sp_stuff','sp_location','sp_pitching','IP']]
agg=agg.merge(fg,on=['pitcher','game_year'],how='left')
nxt=agg[['pitcher','game_year','rv100','woba','n']].copy(); nxt['game_year']-=1; nxt.columns=['pitcher','game_year','rv100_next','woba_next','n_next']
agg=agg.merge(nxt,on=['pitcher','game_year'],how='left')
agg.to_parquet('data/derived/stuff_rv_pitcher_season.parquet',index=False)
def wr(a,b,w): a,b,w=np.asarray(a),np.asarray(b),np.asarray(w); m=np.isfinite(a)&np.isfinite(b); a,b,w=a[m],b[m],w[m]; ma,mb=np.average(a,weights=w),np.average(b,weights=w); return np.average((a-ma)*(b-mb),weights=w)/np.sqrt(np.average((a-ma)**2,weights=w)*np.average((b-mb)**2,weights=w))
q=agg[(agg.n>=300)]
print(f"\npitcher-seasons n>=300: {len(q)}")
print("corr with FG Stuff+ (grouped-OOS ours): A %.3f  B %.3f" % (wr(q.stuff_A_fglike_oos,q.sp_stuff,q.n),wr(q.stuff_B_plus_oos,q.sp_stuff,q.n)))
print("\nSAME-season RV/100 (weights n):   FG %.3f | A_oos %.3f | B_oos %.3f" % (wr(q.sp_stuff,q.rv100,q.n),wr(q.stuff_A_fglike_oos,q.rv100,q.n),wr(q.stuff_B_plus_oos,q.rv100,q.n)))
qq=q[q.n_next>=300]
print(f"NEXT-season RV/100 (n={len(qq)}):      FG %.3f | A_oos %.3f | B_oos %.3f | A_t23 %.3f | B_t23 %.3f" % (wr(qq.sp_stuff,qq.rv100_next,qq.n_next),wr(qq.stuff_A_fglike_oos,qq.rv100_next,qq.n_next),wr(qq.stuff_B_plus_oos,qq.rv100_next,qq.n_next),wr(qq.stuff_A_fglike_t23,qq.rv100_next,qq.n_next),wr(qq.stuff_B_plus_t23,qq.rv100_next,qq.n_next)))
qf=qq[qq.game_year>=2024]  # strictly forward for the t23 models
print(f"NEXT-season RV/100, 2024-25 seasons only (t23 models are true forward, n={len(qf)}): FG %.3f | A_t23 %.3f | B_t23 %.3f | Pitching+ %.3f" % (wr(qf.sp_stuff,qf.rv100_next,qf.n_next),wr(qf.stuff_A_fglike_t23,qf.rv100_next,qf.n_next),wr(qf.stuff_B_plus_t23,qf.rv100_next,qf.n_next),wr(qf.sp_pitching,qf.rv100_next,qf.n_next)))
print(f"NEXT-season wOBA (n={len(qq)}):        FG %.3f | A_oos %.3f | B_oos %.3f" % (wr(qq.sp_stuff,-qq.woba_next,qq.n_next),wr(qq.stuff_A_fglike_oos,-qq.woba_next,qq.n_next),wr(qq.stuff_B_plus_oos,-qq.woba_next,qq.n_next)))
# stability year-to-year of the metric itself
prev=agg[['pitcher','game_year','stuff_A_fglike_oos','stuff_B_plus_oos','sp_stuff','n']].copy(); prev['game_year']+=1
st=q.merge(prev,on=['pitcher','game_year'],suffixes=('','_prev')); st=st[st.n_prev>=300]
print(f"Y2Y stability (n={len(st)}): FG %.3f | A %.3f | B %.3f" % (wr(st.sp_stuff,st.sp_stuff_prev,st.n),wr(st.stuff_A_fglike_oos,st.stuff_A_fglike_oos_prev,st.n),wr(st.stuff_B_plus_oos,st.stuff_B_plus_oos_prev,st.n)))
print("\nB feature importance (gain share):"); imp=res['B_plus']; print((imp/imp.sum()).round(3).head(14).to_string())
for nm in ['Palmquist','Yesavage']:
    print(agg[agg.player_name.str.contains(nm)][['player_name','game_year','n','sp_stuff','stuff_A_fglike_oos','stuff_B_plus_oos','rv100']].round(1).to_string(index=False))
