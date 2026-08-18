"""Build the Carson Palmquist Model outputs: gated composite (CPM) and ungated development prediction for ALL pitchers,
for 2026 (models trained ≤2025) and the strict 2025 view (trained ≤2024). Also rolling-origin calibration of the ungated dev engine.
Writes data/derived/cpm_2026.parquet, cpm_test2025.parquet, dev_all_2026.parquet, dev_all_2025.parquet, dev_calibration.json"""
import numpy as np, pandas as pd, lightgbm as lgb, json, warnings
warnings.filterwarnings('ignore')
src=open('src/palmquist_model_variants.py').read().split("run('V1 GBM base")[0]; exec(src)
gate=lambda x:(x.pp_stf>=105)&(x.stuff.between(88,104))
def fitpred(tr,te,F,tgt='d_stuff'):
    p=np.zeros(len(te))
    for sd in (1,2,3): p+=lgb.train({**P,'seed':sd},lgb.Dataset(tr[F],tr[tgt]),400).predict(te[F])/3
    return p
# rolling calibration (ungated)
rows=[]
for yr in [2021,2022,2023,2024,2025]:
    tr=d5[(d5.game_year<yr)&d5.d_stuff.notna()]; te=d5[(d5.game_year==yr)&d5.d_stuff.notna()].copy()
    if len(tr)<300: continue
    te['pred']=fitpred(tr,te,ARCH); te['yr']=yr; rows.append(te)
A=pd.concat(rows)
import statsmodels.api as sm
cal=sm.OLS(A.d_stuff,sm.add_constant(A.pred)).fit(); a,b=cal.params.const,cal.params.pred
A['cal']=a+b*A.pred; A['bucket']=pd.cut(A.cal,[-99,-3,-1,1,3,5,99])
tab=A.groupby('bucket',observed=True).agg(n=('d_stuff','size'),pred_cal=('cal','mean'),realized=('d_stuff','mean'),sd=('d_stuff','std'),p5=('d_stuff',lambda s:(s>=5).mean()),pdown=('d_stuff',lambda s:(s<0).mean()))
print('rolling calibration (ungated, no own model):', {'a':round(a,3),'b':round(b,3),'r_pooled':round(np.corrcoef(A.pred,A.d_stuff)[0,1],3)}); print(tab.round(2).to_string())
byyr={int(y):{'r':round(np.corrcoef(g.pred,g.d_stuff)[0,1],3)} for y,g in A.groupby('yr')}
json.dump({'a':a,'b':b,'r_pooled':float(np.corrcoef(A.pred,A.d_stuff)[0,1]),'by_year':byyr,'buckets':{str(k):{'n':int(v.n),'pred_cal':float(v.pred_cal),'realized':float(v.realized),'sd':float(v.sd),'p_gain5':float(v.p5),'p_decline':float(v.pdown)} for k,v in tab.iterrows()}},open('data/derived/dev_calibration.json','w'),indent=1)
A.drop(columns=['bucket']).to_parquet('data/derived/dev_backtest.parquet',index=False)
# ungated dev for everyone
tr25=d5[(d5.game_year<=2024)&d5.d_stuff.notna()]; te25=d5[d5.game_year==2025].copy(); te25['pred']=fitpred(tr25,te25,ARCH)
full=d5[d5.d_stuff.notna()]; s26=d6.copy(); s26['pred']=fitpred(full,s26,ARCH)
for df in (te25,s26): df['pred_cal']=a+b*df.pred
te25.to_parquet('data/derived/dev_all_2025.parquet',index=False); s26.to_parquet('data/derived/dev_all_2026.parquet',index=False)
# gated composite = z(dev) + z(actionable) within gate
def combine(df):
    df=df.copy(); z=lambda s:(s-s.mean())/s.std(); df['z_dev']=z(df.pred); df['z_act']=z(df.actionable.fillna(0).clip(lower=0)); df['cpm']=df.z_dev+df.z_act
    df['in_gate']=gate(df).astype(int); df['rk']=df.cpm.rank(ascending=False,method='min'); df['rk_gate']=df[df.in_gate==1].cpm.rank(ascending=False,method='min'); return df
g25=combine(te25); g26=combine(s26)
g25.to_parquet('data/derived/cpm_test2025.parquet',index=False); g26.to_parquet('data/derived/cpm_2026.parquet',index=False)
def excess(df,col,k,tgt,lvl):
    df=df.copy(); df['rk']=df[col].rank(ascending=False,method='min'); top=df[df.rk<=k]; rest=df[df.rk>k]
    e=[rest[(rest[lvl]-s).abs()<=3][tgt].mean() for s in top[lvl]]; return top[tgt].mean()-np.nanmean(e)
v=g25.dropna(subset=['d_stuff']); vg=v[v.in_gate==1]
print(f"2025→26 CPM ALL: top-10 excess ΔStuff+ {excess(v,'cpm',10,'d_stuff','stuff'):+.2f} ΔPit+ {excess(v,'cpm',10,'d_pit','sp_pitching'):+.2f} | top-25 {excess(v,'cpm',25,'d_stuff','stuff'):+.2f} | top-40 {excess(v,'cpm',40,'d_stuff','stuff'):+.2f}")
print(f"2025→26 CPM within gate: top-10 excess ΔStuff+ {excess(vg,'cpm',10,'d_stuff','stuff'):+.2f} | top-25 {excess(vg,'cpm',25,'d_stuff','stuff'):+.2f}")
print(f"2025→26 ungated dev: top-25 excess {excess(te25.dropna(subset=['d_stuff']),'pred',25,'d_stuff','stuff'):+.2f} | top-10 {excess(te25.dropna(subset=['d_stuff']),'pred',10,'d_stuff','stuff'):+.2f}")
for nm in ['Palmquist','Hancock','Dollander','Kyle Harrison','Sasaki']:
    x=g25[g25.PlayerName.str.contains(nm,na=False)]
    if len(x): x=x.iloc[0]; print(f"  2025 {nm}: CPM all #{x.rk:.0f}/{len(g25)} (gate {'#%.0f'%x.rk_gate if x.in_gate else 'out'}) | dev cal {x.pred_cal:+.1f} realized {x.d_stuff:+.1f}")
for nm in ['Beck Way','Mason Black','Kyle Harrison']:
    x=g26[g26.PlayerName.str.contains(nm,na=False)]
    if len(x): x=x.iloc[0]; print(f"  2026 {nm}: CPM all #{x.rk:.0f}/{len(g26)} (gate {'#%.0f'%x.rk_gate if x.in_gate else 'out'}) | dev cal {x.pred_cal:+.1f}")
