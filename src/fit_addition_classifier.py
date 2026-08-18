"""Which pitch family does a pitcher add next season? Multiclass on the addition corpus, features = physical traits
+ sup/pro classifier + current arsenal usage + precedent shares. Grouped K-fold by pitcher; base rate computed OUT OF FOLD
(training-fold add frequencies, restricted to families the pitcher doesn't throw)."""
import numpy as np, pandas as pd, lightgbm as lgb, warnings
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
ad=pd.read_csv('data/derived/pitch_additions.csv')
pr=pd.read_parquet('data/derived/precedent.parquet')
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4','eff4_mb','axis_res','si_dev','ch_dev','sweep_cap','pro_pts','sup_pts','suppro_class','ff_spin']]
d=ad.merge(pr,on=['pitcher','game_year'],suffixes=('','_p')).merge(sp,on=['pitcher','game_year'],how='left')
d['cls']=d.suppro_class.astype('category'); d['hand']=(d.p_throws=='R').astype(int)
F=['arm_angle','fb_havaa','release_pos_z','fb_velo','bauer_fb','suppro','release_extension','hand','eff4','eff4_mb','axis_res','si_dev','sweep_cap','pro_pts','sup_pts','ff_spin','cls']+[f'use_{f}' for f in FAM]+[f'prec_{f}' for f in FAM]
y=pd.Categorical(d.fg_type,categories=FAM).codes; X=d[F]; g=d.pitcher.values
P=dict(objective='multiclass',num_class=len(FAM),learning_rate=0.03,num_leaves=7,min_data_in_leaf=15,feature_fraction=0.7,bagging_fraction=0.8,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1)
prob=np.zeros((len(d),len(FAM))); base=np.zeros((len(d),len(FAM)))
for tr,te in GroupKFold(10).split(X,y,g):
    m=lgb.train(P,lgb.Dataset(X.iloc[tr],y[tr]),300); prob[te]=m.predict(X.iloc[te])
    freq=np.bincount(y[tr],minlength=len(FAM))/len(tr); base[te]=freq
use=d[[f'use_{f}' for f in FAM]].values
mask=(use<0.02)  # only families not currently thrown are eligible
def topk(P_,k):
    P_=np.where(mask,P_,-1); order=np.argsort(-P_,axis=1)[:,:k]; return np.mean([y[i] in order[i] for i in range(len(y))])
print(f"n={len(d)} | model top1 {topk(prob,1):.3f} top2 {topk(prob,2):.3f} | OOF base-rate top1 {topk(base,1):.3f} top2 {topk(base,2):.3f} | precedent-only top1 {topk(d[[f'prec_{f}' for f in FAM]].values,1):.3f}")
# log-loss vs base
def ll(P_):
    P_=np.where(mask,P_,1e-9); P_=P_/P_.sum(1,keepdims=True); return -np.mean(np.log(P_[np.arange(len(y)),y]+1e-9))
print(f"log-loss model {ll(prob):.3f} vs base {ll(base):.3f}")
# by class: what gets added
print(pd.crosstab(d.suppro_class,d.fg_type,normalize='index').round(2))
imp=pd.Series(lgb.train(P,lgb.Dataset(X,y),300).feature_importance('gain'),index=F).sort_values(ascending=False); print((imp/imp.sum()).round(3).head(12).to_string())
