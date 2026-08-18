"""Pull Savant spin-direction leaderboard (active spin %, measured vs movement-inferred axis) per
pitcher x pitch type x season, 2020-2026. Output data/derived/savant_spin.csv"""
import io, time, urllib.request, pandas as pd
UA={'User-Agent':'Mozilla/5.0'}
out=[]
for y in range(2020,2027):
    for t in ['FF','SI','FC','CH','FS','CU','KC','SL','ST','SV','FO','CS']:
        url=f"https://baseballsavant.mlb.com/leaderboard/spin-direction-pitches?year={y}&pitch_type={t}&min=25&csv=true"
        try:
            d=pd.read_csv(io.StringIO(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60).read().decode('utf-8-sig')))
            if len(d): out.append(d); print(y,t,len(d),flush=True)
        except Exception as e: print('fail',y,t,e,flush=True)
        time.sleep(0.6)
df=pd.concat(out,ignore_index=True)
df=df.rename(columns={'player_id':'pitcher','year':'game_year','api_pitch_type':'pitch_type'})
df.to_csv('data/derived/savant_spin.csv',index=False); print(df.shape)
