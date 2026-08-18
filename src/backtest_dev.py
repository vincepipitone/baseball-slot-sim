"""Rolling-origin backtest of the development engine (Dev ΔStf+): for each season t in 2021..2025, train on seasons < t
(strict), predict ΔStuff+ for t→t+1, compare to realized. Reports per-year r, top-k excess vs stuff-matched controls,
calibration by predicted bucket (ungated and gated), and a calibration map to shrink raw predictions."""
import numpy as np, pandas as pd, lightgbm as lgb, warnings
warnings.filterwarnings('ignore')
src=open('src/palmquist_model_variants.py').read().split("run('V1 GBM base")[0]; exec(src)
gate=lambda x:(x.pp_stf>=105)&(x.stuff.between(88,104))
P2={**P}
out=[]
for yr in [2021,2022,2023,2024,2025]:
    tr=d5[(d5.game_year<yr)&d5.d_stuff.notna()].dropna(subset=ARCH); te=d5[(d5.game_year==yr)&d5.d_stuff.notna()].dropna(subset=ARCH).copy()
    if len(tr)<300: continue
    pred=np.zeros(len(te))
    for sd in (1,2,3): pred+=lgb.train({**P2,'seed':sd},lgb.Dataset(tr[ARCH],tr.d_stuff),400).predict(te[ARCH])/3
    te['pred']=pred; te['yr']=yr; out.append(te)
    g=te[gate(te)]
    def exc(df,k):
        df=df.copy(); df['rk']=df.pred.rank(ascending=False,method='min'); top=df[df.rk<=k]; rest=df[df.rk>k]
        e=[rest[(rest.stuff-s).abs()<=3].d_stuff.mean() for s in top.stuff]; return top.d_stuff.mean()-np.nanmean(e), top.pred.mean(), top.d_stuff.mean()
    a=exc(te,25); b=exc(g,10)
    print(f"{yr}→{yr+1}: train {len(tr)} test {len(te)} | r(pred,Δ) {np.corrcoef(te.pred,te.d_stuff)[0,1]:.3f} | ungated top-25: pred {a[1]:+.1f}, realized {a[2]:+.1f}, excess vs matched {a[0]:+.2f} | gated (n={len(g)}) top-10: pred {b[1]:+.1f}, realized {b[2]:+.1f}, excess {b[0]:+.2f}")
A=pd.concat(out)
print(f"\nALL YEARS pooled (n={len(A)}): r {np.corrcoef(A.pred,A.d_stuff)[0,1]:.3f}")
A['bucket']=pd.cut(A.pred,[-99,-4,-2,0,2,4,6,8,99])
print("calibration by predicted bucket (ungated):"); print(A.groupby('bucket',observed=True).agg(n=('d_stuff','size'),pred=('pred','mean'),realized=('d_stuff','mean'),sd=('d_stuff','std'),p_gain5=('d_stuff',lambda s:(s>=5).mean())).round(2).to_string())
G=A[gate(A)]; print(f"\ngated pooled (n={len(G)}): r {np.corrcoef(G.pred,G.d_stuff)[0,1]:.3f}"); print(G.groupby('bucket',observed=True).agg(n=('d_stuff','size'),pred=('pred','mean'),realized=('d_stuff','mean'),sd=('d_stuff','std'),p_gain5=('d_stuff',lambda s:(s>=5).mean())).round(2).to_string())
# calibration line: realized = a + b*pred
import statsmodels.api as sm
f=sm.OLS(A.d_stuff,sm.add_constant(A.pred)).fit(); print(f"\ncalibration (all): realized ≈ {f.params.const:+.2f} + {f.params.pred:.2f}×pred  (R² {f.rsquared:.3f})")
fg_=sm.OLS(G.d_stuff,sm.add_constant(G.pred)).fit(); print(f"calibration (gated): realized ≈ {fg_.params.const:+.2f} + {fg_.params.pred:.2f}×pred  (R² {fg_.rsquared:.3f})")
A.drop(columns=['bucket']).to_parquet('data/derived/dev_backtest.parquet',index=False)
# Blewett
b=A[A.PlayerName.str.contains('Blewett',na=False)][['yr','stuff','pred','d_stuff','fb_liability','gain_gap','own_minus_fg','pp_stf','pp_use','Age']].round(2); print("\nBlewett across years:"); print(b.to_string(index=False))
# top-10 predicted each year with realized
for yr,g in A.groupby('yr'):
    top=g.sort_values('pred',ascending=False).head(8)
    print(f"\n{yr} top-8 predicted:", ', '.join(f"{n} {p:+.1f}→{d:+.1f}" for n,p,d in zip(top.PlayerName,top.pred,top.d_stuff)))
