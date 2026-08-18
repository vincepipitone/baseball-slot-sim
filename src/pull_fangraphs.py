"""Pull FanGraphs Stuff+/Location+/Pitching+ (overall + per pitch) per pitcher-season.
Output: data/derived/fg_stuff.csv  (one row per pitcher-season, ind=0 → totals across teams)"""
import json, sys, time, urllib.request, pandas as pd
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'
def pull(season):
    url=(f"https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=pit&lg=all&qual=0"
         f"&season={season}&season1={season}&startdate=&enddate=&month=0&hand=&team=0&pageitems=5000&pagenum=1"
         f"&ind=0&rost=0&players=&type=36")
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json','Referer':'https://www.fangraphs.com/leaders/major-league'})
    d=json.load(urllib.request.urlopen(req,timeout=60))
    rows=d['data']; print(season,len(rows),'rows',flush=True); return rows
seasons=[int(x) for x in sys.argv[1:]] or list(range(2020,2027))
out=[]
for s in seasons:
    out+=pull(s); time.sleep(1.5)
keep=['Season','xMLBAMID','playerid','PlayerName','Team','IP','Pitches','sp_stuff','sp_location','sp_pitching']+\
     [f'sp_{k}_{p}' for p in ['FF','SI','FC','FS','SL','CU','KC','CH','FO'] for k in 'slp']
df=pd.DataFrame(out)[keep].rename(columns={'Season':'game_year','xMLBAMID':'pitcher'})
df.to_csv('data/derived/fg_stuff.csv',index=False); print(df.shape, df.game_year.value_counts().sort_index().to_dict())
