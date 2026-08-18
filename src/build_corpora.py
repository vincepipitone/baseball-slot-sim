"""Natural-experiment corpora from emulator_table.parquet:
 (1) slot changers: pitcher-season pairs with |Δ pitch-weighted arm angle| >= THRESH (both directions)
 (2) pitch additions: fg_type usage <2% in year t (>=200 pitches) and >=8% in year t+1; also abandoned adds
     (present >=8% in t+1 but <2% in t+2) flagged. Writes data/derived/slot_changers.csv, pitch_additions.csv"""
import numpy as np, pandas as pd, sys
TH=float(sys.argv[1]) if len(sys.argv)>1 else 5.0
t=pd.read_parquet('data/derived/emulator_table.parquet')
ps=t.groupby(['pitcher','player_name','game_year']).apply(lambda g: pd.Series({
    'n':g.n.sum(),'arm_angle':np.average(g.arm_angle.fillna(g.arm_angle.mean()),weights=g.n) if g.arm_angle.notna().any() else np.nan,
    'release_z':np.average(g.release_pos_z,weights=g.n),'stuff':g.sp_stuff.iloc[0],'locp':g.sp_location.iloc[0],'pit':g.sp_pitching.iloc[0],
    'fb_VAA':g.fb_VAA.iloc[0]})).reset_index()
ps=ps[ps.n>=200]
nxt=ps.copy(); nxt['game_year']-=1
pair=ps.merge(nxt,on=['pitcher','player_name','game_year'],suffixes=('','_next'))
pair['d_slot']=pair.arm_angle_next-pair.arm_angle; pair['d_stuff']=pair.stuff_next-pair.stuff
pair['d_loc']=pair.locp_next-pair.locp; pair['d_pit']=pair.pit_next-pair.pit; pair['d_fb_VAA']=pair.fb_VAA_next-pair.fb_VAA
ch=pair[pair.d_slot.abs()>=TH].sort_values('d_slot')
ch.to_csv('data/derived/slot_changers.csv',index=False)
print(f"pairs {len(pair)} | slot changers |Δ|>={TH}°: {len(ch)} (steeper {(ch.d_slot>0).sum()}, flatter {(ch.d_slot<0).sum()})")
print(ch.groupby('game_year').size().to_dict())
print('mean ΔStuff+ steeper %.1f flatter %.1f | mean ΔLoc+ steeper %.1f flatter %.1f' % (
    ch[ch.d_slot>0].d_stuff.mean(),ch[ch.d_slot<0].d_stuff.mean(),ch[ch.d_slot>0].d_loc.mean(),ch[ch.d_slot<0].d_loc.mean()))
# additions
u=t.pivot_table(index=['pitcher','player_name'],columns=['game_year','fg_type'],values='usage',aggfunc='first').fillna(0)
st=t.pivot_table(index=['pitcher','player_name'],columns=['game_year','fg_type'],values='stf',aggfunc='first')
years=sorted(t.game_year.unique()); okpairs=set(zip(pair.pitcher,pair.game_year))
rows=[]
for y in years[:-1]:
    for ft in ['FF','SI','FC','FS','SL','CU','KC','CH']:
        if (y,ft) not in u or (y+1,ft) not in u: continue
        m=(u[(y,ft)]<0.02)&(u[(y+1,ft)]>=0.08)
        for (pid,name) in u.index[m]:
            if (pid,y) not in okpairs: continue
            aband = ((y+2,ft) in u) and (u.loc[(pid,name),(y+2,ft)]<0.02) and ((pid,y+1) in okpairs)
            rows.append(dict(pitcher=pid,player_name=name,game_year=y,fg_type=ft,usage_next=u.loc[(pid,name),(y+1,ft)],
                stf_next=st.loc[(pid,name),(y+1,ft)] if (y+1,ft) in st else np.nan,abandoned=bool(aband)))
ad=pd.DataFrame(rows).merge(pair[['pitcher','game_year','arm_angle','stuff','stuff_next','d_stuff','d_loc','d_pit']],on=['pitcher','game_year'],how='left')
ad.to_csv('data/derived/pitch_additions.csv',index=False)
print('additions:',len(ad),'| by type:',ad.fg_type.value_counts().to_dict(),'| abandoned:',int(ad.abandoned.sum()))
print('mean ΔStuff+ for adders %.1f vs all pairs %.1f' % (ad.d_stuff.mean(),pair.d_stuff.mean()))
