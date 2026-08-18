"""The Carson Palmquist Model: predict next-season ΔStuff+ / ΔPit+ from STRUCTURAL arsenal features.
Features (all as-of season t): stuff level, age, role, plus-pitch under-usage (PPU), fastball liability vs comps, regress-to-comps
(all pitches), mix gain (blend, label-merged), reachable-add gain, add EV, drop-recipe, eff4, sup/pro class, Coors share, precedent pool,
own-vs-FG disagreement, Loc+, velo. Fit OLS (interpretable) and LightGBM (ceiling) with grouped CV; strict temporal test train<=2024
→ predict 2025→26. Report Palmquist-2025 rank, Way-2026 rank, and prospective excess."""
import numpy as np, pandas as pd, lightgbm as lgb, statsmodels.api as sm, warnings, os
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']
tc=pd.read_parquet('data/derived/target_cards.parquet')          # all years, precedent as-of-2026 pools (used for 2026 scoring)
tc5=pd.read_parquet('data/derived/target_cards_asof2025.parquet') # strict pools ≤2025 (used for fitting/testing)
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[(t.n>=30)&t.stf.notna()]
fg=pd.read_csv('data/derived/fg_stuff.csv').drop_duplicates(['pitcher','game_year'])[['pitcher','game_year','sp_stuff','sp_pitching','sp_location']]
gs=pd.read_parquet('data/derived/gap_decomp.parquet')
def structural(base):
    d=base.copy()
    # plus-pitch under-usage: best pitch (blend grade, n>=40) minus arsenal, times how far below 35% usage it is
    rows=[]
    for (pid,yr),g in t[t.pitcher.isin(d.pitcher)].groupby(['pitcher','game_year']):
        g=g[g.n>=40]
        if len(g)<2: continue
        g=g.assign(blend=0.5*g.stf+0.5*g.pit.fillna(g.stf)); ars=np.average(g.blend,weights=g.usage); b=g.sort_values('blend').iloc[-1]
        fb=g[g.fg_type.isin(['FF','SI','FC'])]
        rows.append(dict(pitcher=pid,game_year=yr,ppu=max(b.blend-ars,0)*max(0.35-b.usage,0),best_grade=b.blend,best_usage=b.usage,best_minus_ars=b.blend-ars,
                         fb_usage=fb.usage.sum(),fb_grade=np.average(fb.stf,weights=fb.usage) if len(fb) else np.nan,n_pitches=len(g)))
    d=d.merge(pd.DataFrame(rows),on=['pitcher','game_year'],how='left')
    # fastball liability vs comps: usage-weighted (comps' Stf+ - own) on FF/SI/FC
    g2=gs[gs.fg_type.isin(['FF','SI','FC'])&(gs.usage>=0.08)].assign(x=lambda z:z.usage*z.gap.clip(lower=0)).groupby(['pitcher','game_year']).x.sum().rename('fb_liability').reset_index()
    d=d.merge(g2,how='left'); d['fb_liability']=d.fb_liability.fillna(0)
    d['own_minus_fg']=d.stuff_B_plus_oos-d.stuff
    d['is_sp']=(d.role=='SP').astype(int); d['cls_S']=d.suppro_class.isin(['supinator','lean_supinator']).astype(int); d['cls_P']=d.suppro_class.isin(['pronator','lean_pronator']).astype(int)
    d['col_share']=d.col_share.fillna(0)
    return d
F=['stuff','Age','is_sp','ppu','best_minus_ars','fb_liability','gain_gap','mix_pit','add_act','sum_ev','drop_recipe','eff4','cls_S','cls_P','col_share','own_minus_fg','sp_location','fb_velo','n_precedent_pool']
d5=structural(tc5[tc5.n_tot>=300]); d6=structural(tc[(tc.n_tot>=300)&(tc.game_year==2026)])
nx=fg.copy(); nx['game_year']-=1
d5=d5.merge(nx,on=['pitcher','game_year'],how='left',suffixes=('','_next')); d5['d_stuff']=d5.sp_stuff_next-d5.stuff; d5['d_pit']=d5.sp_pitching_next-d5.sp_pitching
train=d5[(d5.game_year<=2024)&d5.d_stuff.notna()].dropna(subset=F); test=d5[(d5.game_year==2025)&d5.d_stuff.notna()].dropna(subset=F)
print(f"train {len(train)} (2020-24 → next) | test {len(test)} (2025 → 2026)")
# OLS
X=sm.add_constant(train[F].astype(float)); ols=sm.OLS(train.d_stuff.astype(float),X).fit()
print(ols.summary().tables[1])
test=test.assign(pred_ols=ols.predict(sm.add_constant(test[F].astype(float))))
# GBM
P=dict(objective='regression',learning_rate=0.03,num_leaves=7,min_data_in_leaf=40,feature_fraction=0.8,bagging_fraction=0.8,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1)
gbm=lgb.train(P,lgb.Dataset(train[F],train.d_stuff),400); test=test.assign(pred_gbm=gbm.predict(test[F]))
# also a Pit+ target OLS
olsp=sm.OLS(train.d_pit.astype(float),X).fit(); test=test.assign(pred_pit=olsp.predict(sm.add_constant(test[F].astype(float))))
def r(a,b): k=np.isfinite(a)&np.isfinite(b); return np.corrcoef(a[k],b[k])[0,1]
def excess(df,col,k,tgt='d_stuff',lvl='stuff'):
    df=df.copy(); df['rk']=df[col].rank(ascending=False,method='min'); top=df[df.rk<=k]; rest=df[df.rk>k]
    e=[rest[(rest[lvl]-s).abs()<=3][tgt].mean() for s in top[lvl]]; return top[tgt].mean(),np.nanmean(e),len(top)
print(f"\nTEST 2025→26: r(pred_ols, ΔStuff+) {r(test.pred_ols,test.d_stuff):.3f} | r(pred_gbm, ΔStuff+) {r(test.pred_gbm,test.d_stuff):.3f} | r(pred_pit, ΔPit+) {r(test.pred_pit,test.d_pit):.3f} | baseline r(−stuff, Δ) {r(-test.stuff,test.d_stuff):.3f}")
for col in ['pred_ols','pred_gbm']:
    for k in [10,25,40]:
        a,e,n=excess(test,col,k); print(f"  {col} top-{k}: realized {a:+.2f} vs matched {e:+.2f} → excess {a-e:+.2f} (n={n})")
test['rk_ols']=test.pred_ols.rank(ascending=False,method='min'); test['rk_gbm']=test.pred_gbm.rank(ascending=False,method='min')
print("\n2025 ranks (going into 2026):")
for nm in ['Palmquist','Hancock','Dollander','Senzatela','Beck Way','Sasaki']:
    x=test[test.PlayerName.str.contains(nm,na=False)]
    if len(x): x=x.iloc[0]; print(f"  {x.PlayerName:20s} OLS #{x.rk_ols:.0f} (pred {x.pred_ols:+.1f}) GBM #{x.rk_gbm:.0f} | realized Δ {x.d_stuff:+.1f} | ppu {x.ppu:.2f} best {x.best_grade:.0f}@{x.best_usage*100:.0f}% fb_liab {x.fb_liability:.1f} gap {x.gain_gap:.1f} mix {x.mix_pit:.1f} age {x.Age:.0f} coors {x.col_share:.2f} drop {x.drop_recipe}")
print("\n2025 OLS top-15:"); print(test.sort_values('pred_ols',ascending=False).head(15)[['PlayerName','Team','Age','stuff','ppu','fb_liability','gain_gap','mix_pit','col_share','drop_recipe','pred_ols','d_stuff']].round(2).to_string(index=False))
# score 2026 with model refit on all ≤2025
full=d5[d5.d_stuff.notna()].dropna(subset=F); ols2=sm.OLS(full.d_stuff.astype(float),sm.add_constant(full[F].astype(float))).fit()
d6=d6.dropna(subset=F); d6['pred']=ols2.predict(sm.add_constant(d6[F].astype(float))); d6['rk']=d6.pred.rank(ascending=False,method='min')
print("\n2026 ranks (refit ≤2025):")
for nm in ['Beck Way','Palmquist','Yesavage','Glasnow','Iglesias','Hancock','Woods Richardson']:
    x=d6[d6.PlayerName.str.contains(nm,na=False)]
    if len(x): x=x.iloc[0]; print(f"  {x.PlayerName:24s} #{x.rk:.0f} pred {x.pred:+.1f} | ppu {x.ppu:.2f} best {x.best_grade:.0f}@{x.best_usage*100:.0f}% fb_liab {x.fb_liability:.1f} gap {x.gain_gap:.1f} mix {x.mix_pit:.1f} age {x.Age:.0f} drop {x.drop_recipe}")
print("\n2026 top-20:"); print(d6.sort_values('pred',ascending=False).head(20)[['PlayerName','Team','Age','role','stuff','sp_pitching','ppu','best_grade','best_usage','fb_liability','gain_gap','mix_pit','drop_recipe','pred']].round(2).to_string(index=False))
d6.to_parquet('data/derived/palmquist_model_2026.parquet',index=False); test.to_parquet('data/derived/palmquist_model_test2025.parquet',index=False)
