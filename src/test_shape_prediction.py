"""For slot changers (|Δ|>=5): predict year-t+1 per-family shape (IVB, HB_arm) three ways and compare error vs realized:
 (a) no change (carry year t), (b) transfer slopes, (c) precedent: mean shape of same-hand pitchers with slot within ±3° of the
 NEW slot, same family, similar 4S efficiency (±0.05), excluding the pitcher. Also (d) blend of b and c."""
import numpy as np, pandas as pd
m=pd.read_parquet('data/derived/transfer_pairs.parquet')
fits=pd.read_csv('data/derived/transfer_fits.csv'); S={(r.fam,r['var']):r.slope_per_deg for _,r in fits.iterrows()}
t=pd.read_parquet('data/derived/emulator_table.parquet'); t=t[(t.n>=50)&t.arm_angle.notna()]
sp=pd.read_parquet('data/derived/suppro.parquet')[['pitcher','game_year','eff4']]
t=t.merge(sp,on=['pitcher','game_year'],how='left'); m=m.merge(sp.rename(columns={'eff4':'eff4_0'}).assign(game_year=lambda d:d.game_year+1),on=['pitcher','game_year'],how='left')
big=m[m.d_slot.abs()>=5].copy()
def precedent(r,var):
    pool=t[(t.p_throws==r.p_throws0)&(t.fg_type==r.fg_type)&(t.pitcher!=r.pitcher)&((t.arm_angle-r.arm_angle).abs()<=3)]
    if pd.notna(r.eff4_0): pool2=pool[(pool.eff4-r.eff4_0).abs()<=0.05]; pool=pool2 if len(pool2)>=8 else pool
    return np.average(pool[var],weights=pool.n) if len(pool)>=5 else np.nan
rows=[]
for var in ['IVB','HB_arm','release_pos_z']:
    big['p_none']=big[var+'0']; big['p_slope']=big[var+'0']+big.fg_type.map(lambda f:S.get((f,var),0))*big.d_slot
    big['p_prec']=big.apply(lambda r:precedent(r,var),axis=1)
    # precedent applied as a shift: keep pitcher's own offset vs his OLD-slot comps
    big['p_prec_rel']=big[var+'0']+(big.p_prec-big.apply(lambda r:precedent(pd.Series({**r.to_dict(),'arm_angle':r.arm_angle0}),var),axis=1))
    d=big.dropna(subset=['p_prec','p_prec_rel'])
    for fam in ['FF','SI','SL','CH','CU','FC']:
        g=d[d.fg_type==fam]
        if len(g)<25: continue
        y=g[var]
        mae=lambda c: np.mean(np.abs(y-g[c]))
        rows.append(dict(var=var,fam=fam,n=len(g),mae_none=mae('p_none'),mae_slope=mae('p_slope'),mae_prec=mae('p_prec'),mae_prec_rel=mae('p_prec_rel'),
                         mae_blend=np.mean(np.abs(y-(0.5*g.p_slope+0.5*g.p_prec_rel)))))
R=pd.DataFrame(rows).round(2); pd.set_option('display.width',200); print(R.to_string(index=False))
