"""FanGraphs standard pitching dashboard (type=8): IP, ERA, FIP, xFIP, SIERA, WAR, K%, BB%, GS/G per pitcher-season 2020-26."""
import json,time,urllib.request,pandas as pd
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'
out=[]
for s in range(2020,2027):
    url=(f"https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=pit&lg=all&qual=0&season={s}&season1={s}"
         f"&startdate=&enddate=&month=0&hand=&team=0&pageitems=5000&pagenum=1&ind=0&rost=0&players=&type=8")
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json','Referer':'https://www.fangraphs.com/leaders/major-league'})
    d=json.load(urllib.request.urlopen(req,timeout=60))['data']; out+=d; print(s,len(d),flush=True); time.sleep(1.5)
df=pd.DataFrame(out)
keep=[c for c in ['Season','xMLBAMID','playerid','PlayerName','Team','Age','G','GS','IP','ERA','FIP','xFIP','SIERA','WAR','K%','BB%','xERA','WHIP','HR/9','K-BB%'] if c in df.columns]
df=df[keep].rename(columns={'Season':'game_year','xMLBAMID':'pitcher'})
df.to_csv('data/derived/fg_std.csv',index=False); print(df.shape, list(df.columns))
