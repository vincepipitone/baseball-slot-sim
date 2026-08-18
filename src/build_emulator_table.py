"""Join Statcast shape aggregates (FG pitch typing) to FanGraphs per-pitch Stuff+/Location+/Pitching+.
Output: data/derived/emulator_table.parquet — one row per pitcher-season-fgtype with shape + targets."""
import numpy as np, pandas as pd
FG_MAP={'ST':'SL','SV':'SL','SL':'SL','CS':'CU','CU':'CU','KC':'KC','FF':'FF','SI':'SI','FC':'FC','FS':'FS','CH':'CH','FO':'FO'}
p=pd.read_parquet('data/derived/pitches.parquet')
p['fg_type']=p.pitch_type.map(FG_MAP)
p=p[p.fg_type.notna()].copy()
# canonical name per pitcher id (source has truncated variants like 'Woods Richardson, Sime')
canon=p.groupby('pitcher').player_name.agg(lambda s:s.value_counts().idxmax()); p['player_name']=p.pitcher.map(canon)
key=['pitcher','player_name','p_throws','game_year','fg_type']
means=['release_speed','IVB','HB','VAA','HAA','VRA','HRA','VAA_AA_pt','VAA_AA_velo','VAA_AA_all','HAA_AA_pt','HAA_AA_all',
       'AzOE','AxOE','PythagOE','arm_angle','release_pos_x','release_pos_z','release_extension','release_spin_rate','spin_axis',
       'plate_z','plate_x','delta_run_exp','t_flight','ax','az']
agg=p.groupby(key).agg(n=('pitch_type','size'),**{m:(m,'mean') for m in means},
    sd_release_x=('release_pos_x','std'),sd_release_z=('release_pos_z','std'),sd_arm_angle=('arm_angle','std'),
    sd_spin_axis=('spin_axis','std'),sd_IVB=('IVB','std'),sd_HB=('HB','std'),sd_velo=('release_speed','std'),
    sweeper_share=('pitch_type',lambda s:(s=='ST').mean())).reset_index()
tot=agg.groupby(['pitcher','game_year'])['n'].transform('sum'); agg['usage']=agg.n/tot
agg['rv100']=-agg.delta_run_exp*100
# spin-based movement proxies: Bauer units, total break, movement axis (deg, 0=pure ride, +=arm side for RHP)
agg['bauer']=agg.release_spin_rate/agg.release_speed
agg['total_break']=np.sqrt(agg.IVB**2+agg.HB**2)
hb_arm=np.where(agg.p_throws=='R',-agg.HB,agg.HB)   # arm-side positive for both hands
agg['HB_arm']=hb_arm
agg['move_axis']=np.degrees(np.arctan2(hb_arm,agg.IVB))
agg['axis_minus_slot']=agg.move_axis-agg.arm_angle   # tell: movement axis more horizontal than the slot implies (+)
# primary fastball + differentials
fbs=agg[agg.fg_type.isin(['FF','SI','FC'])].sort_values('n',ascending=False).drop_duplicates(['pitcher','game_year'])
fbs=fbs[['pitcher','game_year','fg_type','release_speed','IVB','HB_arm','VAA','arm_angle','release_pos_z']].rename(columns={
    'fg_type':'primary_fb','release_speed':'fb_velo','IVB':'fb_IVB','HB_arm':'fb_HB_arm','VAA':'fb_VAA','arm_angle':'fb_arm_angle','release_pos_z':'fb_release_z'})
agg=agg.merge(fbs,on=['pitcher','game_year'],how='left')
agg['d_velo']=agg.release_speed-agg.fb_velo; agg['d_IVB']=agg.IVB-agg.fb_IVB; agg['d_HB']=agg.HB_arm-agg.fb_HB_arm
agg['is_primary_fb']=(agg.fg_type==agg.primary_fb).astype(int)
# FG join
fg=pd.read_csv('data/derived/fg_stuff.csv')
long=[]
for t in ['FF','SI','FC','FS','SL','CU','KC','CH','FO']:
    d=fg[['pitcher','game_year','IP','Pitches','sp_stuff','sp_location','sp_pitching',f'sp_s_{t}',f'sp_l_{t}',f'sp_p_{t}']].copy()
    d.columns=['pitcher','game_year','IP','fg_pitches','sp_stuff','sp_location','sp_pitching','stf','loc','pit']; d['fg_type']=t
    long.append(d[d.stf.notna()])
long=pd.concat(long)
tab=agg.merge(long,on=['pitcher','game_year','fg_type'],how='left')
tab.to_parquet('data/derived/emulator_table.parquet',index=False)
m=tab[tab.game_year<=2026]
print('rows',len(tab),'| with FG target',tab.stf.notna().sum(),'| n>=50 & target',((tab.n>=50)&tab.stf.notna()).sum())
print('unmatched pitcher-seasons (n>=200 pitches):', tab[(tab.n>=200)&tab.sp_stuff.isna()][['player_name','game_year']].drop_duplicates().shape[0])
print(tab[tab.n>=50].groupby('fg_type').apply(lambda g: pd.Series({'rows':len(g),'has_stf':g.stf.notna().mean().round(2),'r_rv_stf':g[['rv100','stf']].corr().iloc[0,1].round(2)})))
