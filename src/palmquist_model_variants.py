import numpy as np, pandas as pd, lightgbm as lgb, warnings
warnings.filterwarnings('ignore')
exec(open('src/palmquist_model.py').read().split("F=['stuff'")[0])   # loads data + structural()
d5=structural(tc5[tc5.n_tot>=300]); d6=structural(tc[(tc.n_tot>=300)&(tc.game_year==2026)])
# Stuff-based plus-pitch features (best pitch by Stf+, n>=40)
def plus_feats(base):
    rows=[]
    for (pid,yr),g in t[t.pitcher.isin(base.pitcher)].groupby(['pitcher','game_year']):
        g=g[g.n>=40]
        if len(g)<2: continue
        ars=np.average(g.stf,weights=g.usage); b=g.sort_values('stf').iloc[-1]
        rows.append(dict(pitcher=pid,game_year=yr,pp_stf=b.stf,pp_use=b.usage,ppu_stf=max(b.stf-ars,0)*max(0.35-b.usage,0),plus_pitch=int(b.stf>=105)))
    return base.merge(pd.DataFrame(rows),on=['pitcher','game_year'],how='left')
d5=plus_feats(d5); d6=plus_feats(d6)
nx=fg.copy(); nx['game_year']-=1
d5=d5.merge(nx,on=['pitcher','game_year'],how='left',suffixes=('','_next')); d5['d_stuff']=d5.sp_stuff_next-d5.stuff; d5['d_pit']=d5.sp_pitching_next-d5.sp_pitching
d5['young']=(d5.Age<=27).astype(int); d6['young']=(d6.Age<=27).astype(int)
d5['ppu_x_young']=d5.ppu_stf*d5.young; d6['ppu_x_young']=d6.ppu_stf*d6.young
BASE=['stuff','Age','is_sp','ppu','best_minus_ars','fb_liability','gain_gap','mix_pit','add_act','sum_ev','drop_recipe','eff4','cls_S','cls_P','col_share','own_minus_fg','sp_location','fb_velo','n_precedent_pool']
ARCH=BASE+['pp_stf','pp_use','ppu_stf','plus_pitch','young','ppu_x_young']
P=dict(objective='regression',learning_rate=0.03,num_leaves=7,min_data_in_leaf=40,feature_fraction=0.8,bagging_fraction=0.8,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1)
def excess(df,col,k,tgt,lvl):
    df=df.copy(); df['rk']=df[col].rank(ascending=False,method='min'); top=df[df.rk<=k]; rest=df[df.rk>k]
    e=[rest[(rest[lvl]-s).abs()<=3][tgt].mean() for s in top[lvl]]; return top[tgt].mean()-np.nanmean(e)
def run(name,F,tgt,gate=None,seeds=(1,2,3)):
    tr=d5[(d5.game_year<=2024)&d5[tgt].notna()].dropna(subset=F); te=d5[(d5.game_year==2025)&d5[tgt].notna()].dropna(subset=F).copy()
    full=d5[d5[tgt].notna()].dropna(subset=F); s6=d6.dropna(subset=F).copy()
    te['pred']=0; s6['pred']=0
    for sd in seeds:
        m=lgb.train({**P,'seed':sd},lgb.Dataset(tr[F],tr[tgt]),400); te['pred']+=m.predict(te[F])/len(seeds)
        m2=lgb.train({**P,'seed':sd},lgb.Dataset(full[F],full[tgt]),400); s6['pred']+=m2.predict(s6[F])/len(seeds)
    if gate is not None: te=te[gate(te)]; s6=s6[gate(s6)]
    lvl='stuff' if tgt=='d_stuff' else 'sp_pitching'
    te['rk']=te.pred.rank(ascending=False,method='min'); s6['rk']=s6.pred.rank(ascending=False,method='min')
    line=f"{name:34s} test n={len(te)} | excess top10 {excess(te,'pred',10,tgt,lvl):+.2f} top25 {excess(te,'pred',25,tgt,lvl):+.2f} top40 {excess(te,'pred',40,tgt,lvl):+.2f} | 2025→ "
    for nm in ['Palmquist','Hancock','Dollander','Sasaki']:
        x=te[te.PlayerName.str.contains(nm,na=False)]; line+=f"{nm[:4]} #{x.rk.iloc[0]:.0f} " if len(x) else f"{nm[:4]} — "
    line+="| 2026→ "
    for nm in ['Beck Way','Dobnak','Glasnow','Yesavage','Woods Richardson']:
        x=s6[s6.PlayerName.str.contains(nm,na=False)]; line+=f"{nm.split()[-1][:5]} #{x.rk.iloc[0]:.0f} " if len(x) else f"{nm[:4]} — "
    print(line,flush=True); return te,s6
run('V1 GBM base ΔStuff+',BASE,'d_stuff')
run('V2 GBM archetype ΔStuff+',ARCH,'d_stuff')
run('V3 GBM archetype ΔPit+',ARCH,'d_pit')
run('V4 V2 gated: plus pitch (best Stf+≥105)',ARCH,'d_stuff',gate=lambda x:x.pp_stf>=105)
run('V5 V2 gated: plus pitch & age≤27',ARCH,'d_stuff',gate=lambda x:(x.pp_stf>=105)&(x.Age<=27))
run('V6 V2 gated: plus & stuff 88-104',ARCH,'d_stuff',gate=lambda x:(x.pp_stf>=105)&(x.stuff.between(88,104)))
te,s6=run('V7 V3 gated: plus & stuff 88-104 (ΔPit+)',ARCH,'d_pit',gate=lambda x:(x.pp_stf>=105)&(x.stuff.between(88,104)))
print("\nV6 2026 top-15:")
te6,s66=run('V6 again',ARCH,'d_stuff',gate=lambda x:(x.pp_stf>=105)&(x.stuff.between(88,104)))
print(s66.sort_values('pred',ascending=False).head(15)[['PlayerName','Team','Age','role','stuff','sp_pitching','pp_stf','pp_use','ppu_stf','fb_liability','gain_gap','mix_pit','drop_recipe','pred']].round(2).to_string(index=False))
print("\nV6 2025 top-15 (with realized):"); print(te6.sort_values('pred',ascending=False).head(15)[['PlayerName','Team','Age','stuff','pp_stf','pp_use','ppu_stf','fb_liability','gain_gap','mix_pit','col_share','drop_recipe','pred','d_stuff']].round(2).to_string(index=False))
s66.to_parquet('data/derived/palmquist_model_v6_2026.parquet',index=False); te6.to_parquet('data/derived/palmquist_model_v6_test2025.parquet',index=False)
