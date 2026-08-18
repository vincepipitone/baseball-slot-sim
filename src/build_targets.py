"""Target cards. For every pitcher-season (n_tot>=300):
 - repertoire lever: for each unthrown family (usage<2%) with precedent share>=.20 in the sup/pro-compatible neighborhood,
   possible gain = u_add(0.14) x (precedent Stf+ of family - current Stuff+)^+; best family = max gain.
   add-propensity P(add f next yr) from a binary LightGBM (grouped CV) over ALL pitcher-season x family rows; EV = P x gain.
 - slot flag: Driveline drop recipe (below-avg FF IVB & eff4>=.93 & slot>=25) ; precedent pool count.
 - projection: proj Stuff+ = Stuff+ + gain ; proj Pit+ = -74.8+.850*Stf+ +.897*Loc+ (Loc+ mean-reverted 50%);
   ΔWAR/180 = .098 (SP) / .074 (RP) x ΔPit+ ; IP = last-season IP (min 60 SP / 40 RP) ; $ at $8M/WAR.
 - backtest (years<=2025): gain/EV vs realized ΔStuff+ / ΔPit+ next season; P(add) calibration.
Outputs data/derived/target_cards.parquet, docs/targets_2026.md"""
import numpy as np, pandas as pd, lightgbm as lgb, warnings, os
ASOF=int(os.environ.get('ASOF','2026')); SUF='' if ASOF==2026 else f'_asof{ASOF}'
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
FAM=['FF','SI','FC','FS','SL','CU','KC','CH']; ROLE={'FF':'ride','SI':'run','FC':'cut','FS':'offspeed','CH':'offspeed','SL':'slider','CU':'curve','KC':'curve'}
U_ADD=0.14; A,B,C=-74.8,0.850,0.897; WAR_SP,WAR_RP=0.098,0.074; DPW=8.0
pr=pd.read_parquet(f'data/derived/precedent{SUF}.parquet').drop_duplicates(['pitcher','game_year'])
fg=pd.read_csv('data/derived/fg_stuff.csv')[['pitcher','game_year','sp_stuff','sp_location','sp_pitching','Pitches']].drop_duplicates(['pitcher','game_year'])
st=pd.read_csv('data/derived/fg_std.csv')[['pitcher','game_year','PlayerName','Team','Age','G','GS','IP','ERA','FIP','xERA','WAR','K%','BB%']].drop_duplicates(['pitcher','game_year'])
st['Team']=st.Team.astype(str).str.replace(r'<[^>]+>','',regex=True).str.strip()
own=pd.read_parquet('data/derived/stuff_rv_pitcher_season.parquet')[['pitcher','game_year','stuff_B_plus_oos','stuff_A_fglike_oos']].drop_duplicates(['pitcher','game_year'])
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4','axis_res','si_dev','sweep_cap','pro_pts','sup_pts','suppro_class']].drop_duplicates(['pitcher','game_year'])
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[t.game_year<=ASOF]
ff=t[(t.fg_type=='FF')&(t.n>=50)][['pitcher','game_year','IVB']].rename(columns={'IVB':'ff_ivb'}); ff=ff.merge(ff.groupby('game_year').ff_ivb.mean().rename('lg_ivb').reset_index()); ff['ivb_rel']=ff.ff_ivb-ff.lg_ivb; ff=ff.drop_duplicates(['pitcher','game_year'])
d=pr.drop(columns=['eff4','axis_res','si_dev','suppro_class'],errors='ignore').merge(fg,on=['pitcher','game_year'],how='left',suffixes=('','_fg')).merge(st,on=['pitcher','game_year'],how='left').merge(own,how='left').merge(sp,how='left').merge(ff[['pitcher','game_year','ivb_rel']],how='left')
d=d[(d.n_tot>=300)&(d.game_year<=ASOF)].reset_index(drop=True)
d['stuff']=d.sp_stuff.fillna(d.sp_stuff_fg) if 'sp_stuff_fg' in d else d.sp_stuff
d['role']=np.where(d.GS.fillna(0)/d.G.fillna(1)>=0.5,'SP','RP')
# ---- add-propensity model over pitcher-season x family (unthrown)
nxt=t.pivot_table(index=['pitcher','game_year'],columns='fg_type',values='usage',aggfunc='first').reindex(columns=FAM).fillna(0)
nxt.index=pd.MultiIndex.from_arrays([nxt.index.get_level_values(0),nxt.index.get_level_values(1)-1],names=['pitcher','game_year'])
has_next=set(zip(d.pitcher+0,d.game_year-1))  # pitcher-seasons that exist next year (need n_tot>=300 next yr for label validity)
valid_next=set(zip(d.pitcher,d.game_year-1))
rows=[]
for i,r in d.iterrows():
    role_use={}
    for g_ in FAM: role_use[ROLE[g_]]=role_use.get(ROLE[g_],0)+r[f'use_{g_}']
    for f in FAM:
        if r[f'use_{f}']>=0.02: continue
        if role_use[ROLE[f]]>=0.05: continue   # role already occupied (CU vs KC, CH vs FS): not an addition
        key=(r.pitcher,r.game_year)
        label=np.nan
        if key in valid_next:
            try: label=float(nxt.loc[key,f]>=0.08)
            except KeyError: label=np.nan
        rows.append(dict(idx=i,pitcher=r.pitcher,game_year=r.game_year,fam=f,label=label,prec=r[f'prec_{f}'],pstf=r[f'pstf_{f}'],gain_raw=r[f'pstf_{f}']-r.stuff,
                         arm_angle=r.arm_angle,fb_havaa=r.fb_havaa,fb_velo=r.fb_velo,bauer_fb=r.bauer_fb,eff4=r.eff4,axis_res=r.axis_res,si_dev=r.si_dev,sweep_cap=r.sweep_cap,
                         pro_pts=r.pro_pts,sup_pts=r.sup_pts,hand=int(r.p_throws=='R'),stuff=r.stuff,role_sp=int(r.role=='SP'),
                         **{f'use_{g}':r[f'use_{g}'] for g in FAM}))
L=pd.DataFrame(rows); L['fam_c']=L.fam.astype('category')
for c_ in ['prec','pstf','gain_raw','arm_angle','fb_havaa','fb_velo','bauer_fb','eff4','axis_res','si_dev','sweep_cap','pro_pts','sup_pts','stuff']+[f'use_{g}' for g in FAM]: L[c_]=pd.to_numeric(L[c_],errors='coerce')
F=['fam_c','prec','pstf','gain_raw','arm_angle','fb_havaa','fb_velo','bauer_fb','eff4','axis_res','si_dev','sweep_cap','pro_pts','sup_pts','hand','stuff','role_sp']+[f'use_{g}' for g in FAM]
P=dict(objective='binary',learning_rate=0.03,num_leaves=15,min_data_in_leaf=50,feature_fraction=0.7,bagging_fraction=0.8,bagging_freq=1,lambda_l2=10,verbose=-1,seed=1)
lab=L[L.label.notna()]; X=lab[F]; y=lab.label.values; g=lab.pitcher.values
oof=np.zeros(len(lab))
for tr,te in GroupKFold(5).split(X,y,g): oof[te]=lgb.train(P,lgb.Dataset(X.iloc[tr],y[tr]),400).predict(X.iloc[te])
lab=lab.assign(p_add=oof)
from sklearn.metrics import roc_auc_score
print(f"add-propensity: rows {len(lab)}, base rate {y.mean():.3f}, grouped-OOF AUC {roc_auc_score(y,oof):.3f}")
# calibration deciles
lab['dec']=pd.qcut(lab.p_add,10,labels=False,duplicates='drop'); print(lab.groupby('dec').agg(p=('p_add','mean'),obs=('label','mean'),n=('label','size')).round(3).T.to_string())
m_all=lgb.train(P,lgb.Dataset(X,y),400)
L['p_add']=np.nan; L.loc[lab.index,'p_add']=oof
L.loc[L.label.isna(),'p_add']=m_all.predict(L.loc[L.label.isna(),F])   # 2026 rows scored by model trained on ≤2025 labels
# ---- reachable + gains
L['reach']=(L.prec>=0.20)&L.pstf.notna()
L['gain']=np.where(L.reach,U_ADD*np.clip(L.gain_raw,0,None),0.0); L['ev']=L.p_add*L.gain
best=L.sort_values('gain',ascending=False).drop_duplicates('idx').set_index('idx')
bestev=L.sort_values('ev',ascending=False).drop_duplicates('idx').set_index('idx')
d['best_add']=best.fam; d['best_add_pstf']=best.pstf; d['best_add_prec']=best.prec; d['best_add_padd']=best.p_add; d['gain']=best.gain.fillna(0)
nog=(d.gain<=0)|d.best_add.isna(); d.loc[nog,'best_add']='—'; d.loc[nog,['best_add_pstf','best_add_prec','best_add_padd']]=np.nan
d['ev_add']=bestev.fam; d['ev']=bestev.ev.fillna(0)
d['n_reachable']=L[L.reach].groupby('idx').size().reindex(d.index).fillna(0)
d['sum_ev']=L.groupby('idx').ev.sum().reindex(d.index).fillna(0)
# ---- slot flag
d['drop_recipe']=((d.ivb_rel<0)&(d.eff4>=0.93)&(d.arm_angle>=15)).fillna(False).astype(int)
# ---- projection & value
d['loc_proj']=100+0.5*(d.sp_location-100)
d['proj_stuff']=d.stuff+d.gain
d['pit_now_fit']=A+B*d.stuff+C*d.sp_location; d['proj_pit']=A+B*d.proj_stuff+C*d.loc_proj; d['d_pit']=B*d.gain  # lever only; Loc+ reversion shown via proj_pit
d['ip_assume']=np.where(d.role=='SP',np.clip(d.IP.fillna(0),60,200),np.clip(d.IP.fillna(0),40,80))
d['d_war']=np.where(d.role=='SP',WAR_SP,WAR_RP)*d.d_pit*d.ip_assume/180; d['d_dollars_M']=d.d_war*DPW
d['ev_war']=np.where(d.role=='SP',WAR_SP,WAR_RP)*(B*d.ev)*d.ip_assume/180
d.to_parquet(f'data/derived/target_cards{SUF}.parquet',index=False)
d.to_parquet(f'data/derived/target_cards{SUF}.parquet',index=False)
L[['pitcher','game_year','fam','prec','pstf','gain_raw','p_add','reach','gain','ev']].to_parquet(f'data/derived/target_fams{SUF}.parquet',index=False)
# ---- levers v2 (mix, existing-pitch gap, Coors) + combined opportunity score
lv=pd.read_parquet('data/derived/levers_v2.parquet')[['pitcher','game_year','gain_mix','worst_fam','worst_use','worst_stf','best_fam','best_use','best_stf','gain_gap','gap_parts','col_share','coors_adj']].drop_duplicates(['pitcher','game_year'])
d=d.merge(lv,on=['pitcher','game_year'],how='left'); d[['gain_mix','gain_gap','coors_adj']]=d[['gain_mix','gain_gap','coors_adj']].fillna(0)
import statsmodels.api as sm
_nx=d[['pitcher','game_year','stuff']].copy(); _nx['game_year']-=1
_b=d.merge(_nx,on=['pitcher','game_year'],suffixes=('','_next')).dropna(subset=['stuff_next'])
_b=_b[_b.game_year<=ASOF-1]
_f=sm.OLS(_b.stuff_next-_b.stuff,sm.add_constant(_b[['stuff','sum_ev','gain_mix','gain_gap','coors_adj']])).fit()
print('combined-score weights (ΔStuff+ ~ level + levers, years<=%d):'%(ASOF-1)); print(_f.params.round(3).to_dict(), {k:round(v,3) for k,v in _f.pvalues.items()})
W={k:max(_f.params[k],0) for k in ['sum_ev','gain_mix','gain_gap','coors_adj']}
d['opportunity']=sum(W[k]*d[k] for k in W)
# ACTIONABLE UPSIDE (what an org could do, not what drifts on its own): mix gain in full + best reachable role-unoccupied add
# valued at precedent Stf+ (no P(add) multiplier; feasibility = precedent share ≥.20 in the sup/pro-compatible neighborhood)
# + drop-recipe bonus (+1.4, our replicated Driveline effect). Regress-to-comps EXCLUDED.
d['add_act']=np.where(d.gain>0,d.gain,0.0)
d['drop_bonus']=1.4*d.drop_recipe
d['actionable']=d.gain_mix.clip(lower=0)+d.add_act+d.drop_bonus
d['proj_stuff_act']=d.stuff+d.actionable
d['proj_stuff_all']=d.stuff+d.opportunity
# ---- backtest on years <=2025
nx=d[['pitcher','game_year','stuff','sp_pitching','sp_location']].copy(); nx['game_year']-=1
b=d.merge(nx,on=['pitcher','game_year'],suffixes=('','_next')); b['d_stuff']=b.stuff_next-b.stuff; b['d_pitp']=b.sp_pitching_next-b.sp_pitching
b=b.dropna(subset=['d_stuff'])
def r(a,c): k=np.isfinite(a)&np.isfinite(c); return np.corrcoef(a[k],c[k])[0,1]
print(f"opportunity: r(opp, ΔStuff+) {r(b.opportunity,b.d_stuff):.3f} | after mean reversion {r(b.opportunity,sm.OLS(b.d_stuff,sm.add_constant(b.stuff)).fit().resid):.3f}")
print(f"\nbacktest n={len(b)}: r(gain, ΔStuff+) {r(b.gain,b.d_stuff):.3f} | r(EV, ΔStuff+) {r(b.ev,b.d_stuff):.3f} | r(sum_EV, ΔStuff+) {r(b.sum_ev,b.d_stuff):.3f} | r(EV, ΔPit+) {r(b.ev,b.d_pitp):.3f} | r(stuff level, ΔStuff+) {r(b.stuff,b.d_stuff):.3f}")
# controlling for mean reversion: residualize ΔStuff+ on stuff level
import statsmodels.api as sm
res=sm.OLS(b.d_stuff,sm.add_constant(b.stuff)).fit().resid
print(f"after removing mean reversion: r(gain, resid) {r(b.gain,res):.3f} | r(EV, resid) {r(b.ev,res):.3f} | r(sum_EV, resid) {r(b.sum_ev,res):.3f}")
b['q']=pd.qcut(b.sum_ev.rank(method='first'),5,labels=False); print(b.groupby('q').agg(n=('d_stuff','size'),sum_ev=('sum_ev','mean'),d_stuff=('d_stuff','mean'),resid=('d_stuff',lambda s: res[s.index].mean())).round(2).T.to_string())
# ---- 2026 cards
c=d[(d.game_year==ASOF)].copy()
cols=['PlayerName','Team','Age','role','IP','arm_angle','eff4','suppro_class','stuff','stuff_B_plus_oos','sp_location','sp_pitching','best_add','best_add_pstf','best_add_prec','best_add_padd','gain','sum_ev','n_reachable','npit0' if 'npit0' in c else 'n_precedent_pool','drop_recipe','proj_stuff','proj_pit','d_pit','d_war','d_dollars_M']
cols=[x for x in cols if x in c.columns]
top=c.sort_values('actionable',ascending=False)
lines=[f"# {ASOF} target cards (as of end of {ASOF} data) — repertoire lever, precedent-valued\n",
"Method: for each family the pitcher does not throw (<2%), precedent = same-hand, sup/pro-compatible pitchers within the trait neighborhood; "
"reachable if ≥20% of them throw it ≥10%; gain = 0.14 usage × (precedent Stf+ − current Stuff+)+; P(add) from a grouped-CV binary model; "
"EV = P(add) × gain summed over reachable families. Projection: Pit+ = −74.8 + .85·Stf+ + .90·Loc+ (Loc+ half mean-reverted); "
"ΔWAR = .098 (SP)/.074 (RP) per Pit+ per 180 IP at last-season IP; $8M/WAR. `own` = our run-value Stuff model (grouped-OOS). "
"`drop_recipe` = below-avg FF IVB & eff4≥.93 & slot≥25 (Driveline recipe; feasibility flag only). Slot change is NOT projected as gain.\n",
"Backtest (2020–25, n=2315): possible-gain vs next-season ΔStuff+ r=.22 raw, ≈.04 after removing mean reversion → these are REACHABILITY cards with conditional value, not forecasts. Validated pieces: P(add) grouped-OOF AUC .79 (calibrated by decile); precedent Stf+ of an added pitch vs realized r≈.5.\n","## Top 40 by expected value of reachable additions\n","| # | Pitcher | Tm | Age | Role | IP | Slot | eff4 | Class | Stuff+ | own | Loc+ | Pit+ | Best add (prec Stf+, share, P) | Gain | ΣEV | Reach | Pool | Drop? | Proj Stf+ | ΔPit+ | ΔWAR | Δ$M |","|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
poolcol='n_precedent_pool' if 'n_precedent_pool' in c.columns else None
for i,(_,r) in enumerate(top.head(40).iterrows(),1):
    lines.append(f"| {i} | {r.PlayerName} | {r.Team} | {r.Age:.0f} | {r.role} | {r.IP:.0f} | {r.arm_angle:.0f}° | {r.eff4:.2f} | {r.suppro_class} | {r.stuff:.0f} | {r.stuff_B_plus_oos:.0f} | {r.sp_location:.0f} | {r.sp_pitching:.0f} | {r.best_add} ({r.best_add_pstf:.0f}, {r.best_add_prec:.2f}, {r.best_add_padd:.2f}) | {r.gain:+.1f} | {r.sum_ev:.2f} | {r.n_reachable:.0f} | {r[poolcol]:.0f} | {'Y' if r.drop_recipe else ''} | {r.proj_stuff:.0f} | {r.d_pit:+.1f} | {r.d_war:+.2f} | {r.d_dollars_M:+.1f} |")
lines+=["\n## Top 25 by raw possible gain (best single add, regardless of P(add))\n","| # | Pitcher | Tm | Role | Slot | Class | Stuff+ | Best add | prec Stf+ | share | P(add) | Gain | Proj Stf+ | ΔWAR |","|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for i,(_,r) in enumerate(c.sort_values('gain',ascending=False).head(25).iterrows(),1):
    lines.append(f"| {i} | {r.PlayerName} | {r.Team} | {r.role} | {r.arm_angle:.0f}° | {r.suppro_class} | {r.stuff:.0f} | {r.best_add} | {r.best_add_pstf:.0f} | {r.best_add_prec:.2f} | {r.best_add_padd:.2f} | {r.gain:+.1f} | {r.proj_stuff:.0f} | {r.d_war:+.2f} |")
lines+=["\n## Named checks\n"]
for nm in ['Yesavage','Palmquist','Hancock']:
    for _,r in c[c.PlayerName.str.contains(nm,na=False)].iterrows():
        lines.append(f"- **{r.PlayerName}** ({r.Team}, {r.role}): slot {r.arm_angle:.0f}°, eff4 {r.eff4:.2f}, {r.suppro_class}; Stuff+ {r.stuff:.0f} (own {r.stuff_B_plus_oos:.0f}), Loc+ {r.sp_location:.0f}; reachable {r.n_reachable:.0f}, best add {r.best_add} (prec Stf+ {r.best_add_pstf:.0f}, share {r.best_add_prec:.2f}, P {r.best_add_padd:.2f}), gain {r.gain:+.1f}, ΣEV {r.sum_ev:.2f}, pool n={r[poolcol]:.0f}, drop-recipe {'Y' if r.drop_recipe else 'N'} → proj Stf+ {r.proj_stuff:.0f}, ΔWAR {r.d_war:+.2f}")
open(f'docs/targets_{ASOF}.md','w').write('\n'.join(lines))
print('\nwrote docs/targets_2026.md; 2026 pitchers:',len(c))
print(c.sort_values('sum_ev',ascending=False)[['PlayerName','Team','role','stuff','best_add','best_add_pstf','best_add_padd','gain','sum_ev','d_war']].head(15).round(2).to_string(index=False))

d.to_parquet(f'data/derived/target_cards{SUF}.parquet',index=False)
