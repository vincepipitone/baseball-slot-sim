"""Build pitch-level and pitcher-season-pitch feature tables from the
Chamberlain Pitch Leaderboard v8 Tableau extract (raw Statcast, 2024-).

Reproduces his calculated fields:
  VAA/HAA  (approach angles at plate front, y = 17/12 ft)
  VRA/HRA  (release angles at y = 60.5 - extension)
  VAA AA (pitch type / velo band / all), HAA AA (pitch type / all)
  Dynamic Dead Zone: AzOE, AxOE (FF/SI/FC; over expected given VRA/HRA),
  Pythag OE (total accel over expected given release z, ext, arm angle)
Deviation from source: "velo band" uses round(release_speed) rather than his
flight-time proxy round(t_f + t_s, 2).

Usage: python3.11 src/build_pitch_features.py [path/to.hyper]
"""
import glob, sys, numpy as np, pandas as pd
from tableauhyperapi import HyperProcess, Telemetry, Connection

HYPER = sys.argv[1] if len(sys.argv) > 1 else glob.glob('data/raw/Data/TableauTemp/*.hyper')[0]
COLS = ['pitch_type','pitch_name','game_date','game_year','game_pk','at_bat_number','pitch_number',
        'pitcher','player_name','p_throws','stand','SP_RP','release_speed','release_pos_x','release_pos_z',
        'release_extension','release_spin_rate','spin_axis','arm_angle','pfx_x','pfx_z','plate_x','plate_z',
        'vx0','vy0','vz0','ax','ay','az','zone','description','events','delta_run_exp','woba_value',
        'estimated_woba_using_speedangle','launch_speed','launch_angle','bat_speed','swing_length']

def load():
    with HyperProcess(Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hp, Connection(hp.endpoint, HYPER) as c:
        q = 'select ' + ','.join(('cast("game_date" as text) as "game_date"' if x=='game_date' else f'"{x}"') for x in COLS) + ' from "Extract"."Extract"'
        rows = c.execute_list_query(q)
    df = pd.DataFrame(rows, columns=COLS)
    df['game_year'] = df['game_year'].astype(int)
    df['src'] = 'hyper'
    # pybaseball backfill (2020-23; anything outside the extract's years)
    parts = []
    for f in sorted(glob.glob('data/raw/statcast_*.parquet')):
        d = pd.read_parquet(f)
        d['SP_RP'] = None
        d = d.reindex(columns=COLS); parts.append(d)
    if parts:
        b = pd.concat(parts, ignore_index=True)
        b['game_year'] = b['game_year'].astype(int)
        b = b[~b.game_year.isin(df.game_year.unique())]
        b['src'] = 'pybaseball'
        for c in ['pitcher','game_pk','at_bat_number','pitch_number','zone']:
            b[c] = pd.to_numeric(b[c], errors='coerce')
        df = pd.concat([df, b], ignore_index=True)
    return df

def angles(df):
    y_plate = 17/12
    vy_f = -np.sqrt(df.vy0**2 - 2*df.ay*(50 - y_plate))
    t_f = (vy_f - df.vy0)/df.ay
    vz_f = df.vz0 + df.az*t_f
    vx_f = df.vx0 + df.ax*t_f
    df['VAA'] = -np.degrees(np.arctan(vz_f/vy_f))
    df['HAA'] = -np.degrees(np.arctan(vx_f/vy_f))
    y_rel = 60.5 - df.release_extension
    vy_r = -np.sqrt(df.vy0**2 - 2*df.ay*(50 - y_rel))
    t_s = (vy_r - df.vy0)/df.ay
    vz_r = df.vz0 + df.az*t_s
    vx_r = df.vx0 + df.ax*t_s
    df['VRA'] = -np.degrees(np.arctan(vz_r/vy_r))
    df['HRA'] = -np.degrees(np.arctan(vx_r/vy_r))
    df['t_flight'] = t_f - t_s
    df['IVB'] = df.pfx_z*12
    df['HB'] = df.pfx_x*12
    return df

def abbrev(pt):
    return pt.replace({'ST':'SW','CS':'CU','KC':'CU'}).fillna('(unk)')

def over_expected(df, col, keys, mask=None):
    g = df[col] - df.groupby(keys)[col].transform('mean')
    if mask is not None: g = g.where(mask)
    return g

def add_aa(df):
    df['abbrev'] = abbrev(df.pitch_type)
    df['pz_r'] = df.plate_z.round(1); df['px_r'] = df.plate_x.round(1)
    df['rx_c'] = df.release_pos_x.clip(-4,4).round(1)
    df['velo_r'] = df.release_speed.round(0)
    df['VAA_AA_pt']   = over_expected(df,'VAA',['game_year','p_throws','pz_r','abbrev'])
    df['VAA_AA_velo'] = over_expected(df,'VAA',['game_year','p_throws','pz_r','velo_r'])
    df['VAA_AA_all']  = over_expected(df,'VAA',['game_year','p_throws','pz_r'])
    df['HAA_AA_pt']   = over_expected(df,'HAA',['game_year','px_r','rx_c','abbrev'])
    df['HAA_AA_all']  = over_expected(df,'HAA',['game_year','px_r','rx_c'])
    fb = df.abbrev.isin(['FF','SI','FC'])
    df['VRA_r'] = df.VRA.round(1); df['HRA_r'] = df.HRA.round(1)
    df['AzOE'] = over_expected(df,'az',['game_year','abbrev','VRA_r'], fb)
    df['AxOE'] = over_expected(df,'ax',['game_year','p_throws','abbrev','HRA_r'], fb)
    rz = df.release_pos_z.where(df.release_pos_z.between(0.75,7.5)).round(1)
    keys = pd.DataFrame({'y':df.game_year,'h':df.p_throws,'a':df.abbrev,'rz':rz,
                         'ext':df.release_extension.round(1),'aa':(2*df.arm_angle).round()/2})
    kk = [keys[c] for c in keys]
    ez = df.groupby(kk)['az'].transform('mean'); ex = df.groupby(kk)['ax'].transform('mean')
    df['PythagOE'] = np.sqrt(df.az**2+df.ax**2) - np.sqrt(ez**2+ex**2)
    df.drop(columns=['pz_r','px_r','rx_c','velo_r','VRA_r','HRA_r'], inplace=True)
    return df

def aggregate(df):
    df['is_fb'] = df.abbrev.isin(['FF','SI','FC'])
    key = ['pitcher','player_name','p_throws','game_year','abbrev']
    means = ['release_speed','IVB','HB','VAA','HAA','VRA','HRA','VAA_AA_pt','VAA_AA_velo','VAA_AA_all',
             'HAA_AA_pt','HAA_AA_all','AzOE','AxOE','PythagOE','arm_angle','release_pos_x','release_pos_z',
             'release_extension','release_spin_rate','spin_axis','plate_z','plate_x','delta_run_exp','t_flight']
    agg = df.groupby(key).agg(n=('pitch_type','size'), **{m:(m,'mean') for m in means},
                              sd_release_x=('release_pos_x','std'), sd_release_z=('release_pos_z','std'),
                              sd_arm_angle=('arm_angle','std'), sd_spin_axis=('spin_axis','std'),
                              sd_IVB=('IVB','std'), sd_HB=('HB','std'), sd_velo=('release_speed','std'),
                              sp_share=('SP_RP', lambda s: (s=='SP').mean())).reset_index()
    tot = agg.groupby(['pitcher','game_year'])['n'].transform('sum')
    agg['usage'] = agg.n/tot
    agg['rv100'] = -agg.delta_run_exp*100  # pitcher perspective: positive = good
    # primary fastball per pitcher-season (most-used among FF/SI/FC) and differentials
    fbs = agg[agg.abbrev.isin(['FF','SI','FC'])].sort_values('n',ascending=False).drop_duplicates(['pitcher','game_year'])
    fbs = fbs[['pitcher','game_year','abbrev','release_speed','IVB','HB','VAA']].rename(
        columns={'abbrev':'primary_fb','release_speed':'fb_velo','IVB':'fb_IVB','HB':'fb_HB','VAA':'fb_VAA'})
    agg = agg.merge(fbs, on=['pitcher','game_year'], how='left')
    agg['d_velo'] = agg.release_speed - agg.fb_velo
    agg['d_IVB'] = agg.IVB - agg.fb_IVB
    agg['d_HB'] = agg.HB - agg.fb_HB
    return agg

if __name__ == '__main__':
    df = load(); print('loaded', len(df))
    df = angles(df); df = add_aa(df)
    df.to_parquet('data/derived/pitches.parquet', index=False); print('wrote pitches.parquet')
    agg = aggregate(df)
    agg.to_parquet('data/derived/pitcher_season_pitch.parquet', index=False)
    agg.to_csv('data/derived/pitcher_season_pitch.csv', index=False)
    print('wrote pitcher_season_pitch', agg.shape)
