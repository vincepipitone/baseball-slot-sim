"""Backfill raw Statcast pitch data 2020-2023 (extract only covers 2024+) via pybaseball, one month at a time,
cached to data/raw/statcast_YYYY_MM.parquet. Columns trimmed to what build_pitch_features needs."""
import os, sys, time, calendar, pandas as pd
from pybaseball import statcast, cache
cache.enable()
COLS=['pitch_type','game_date','release_speed','release_pos_x','release_pos_z','player_name','batter','pitcher','events','description','zone','des','stand','p_throws','home_team','away_team','type','bb_type','balls','strikes','game_year','pfx_x','pfx_z','on_3b','on_2b','on_1b','outs_when_up','inning','inning_topbot','hc_x','hc_y','vx0','vy0','vz0','ax','ay','az','launch_speed','launch_angle','release_spin_rate','release_extension','game_pk','estimated_ba_using_speedangle','estimated_woba_using_speedangle','woba_value','launch_speed_angle','at_bat_number','pitch_number','pitch_name','home_score','away_score','post_away_score','post_home_score','spin_axis','delta_run_exp','bat_speed','swing_length','estimated_slg_using_speedangle','arm_angle','attack_angle','attack_direction','swing_path_tilt','intercept_ball_minus_batter_pos','plate_x','plate_z']
years=[int(y) for y in sys.argv[1:]] or [2023,2022,2021,2020]
for y in years:
    for m in range(3,12):
        out=f'data/raw/statcast_{y}_{m:02d}.parquet'
        if os.path.exists(out): continue
        start=f'{y}-{m:02d}-01'; end=f'{y}-{m:02d}-{calendar.monthrange(y,m)[1]:02d}' if m!=11 else f'{y}-11-15'
        for attempt in range(3):
            try:
                df=statcast(start_dt=start,end_dt=end,verbose=False); break
            except Exception as e:
                print('retry',y,m,e,flush=True); time.sleep(30)
        else: continue
        if df is None or len(df)==0: print('empty',y,m,flush=True); continue
        keep=[c for c in COLS if c in df.columns]; df=df[keep]
        df['game_date']=df['game_date'].astype(str)
        df.to_parquet(out,index=False); print(y,m,len(df),flush=True)
print('done')
