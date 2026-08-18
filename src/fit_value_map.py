"""Stage 2/3 pieces: (a) ΔLocation+ cost of slot changes / pitch additions from the corpora; (b) Pitching+ ≈ f(Stuff+, Location+);
(c) Pitching+ (and Stuff+/Loc+) -> NEXT-season ERA/FIP/xERA and WAR per 180 IP; per-role IP assumptions."""
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
fg=pd.read_csv('data/derived/fg_stuff.csv'); st=pd.read_csv('data/derived/fg_std.csv')
d=fg.drop(columns=['IP']).merge(st.drop(columns=['playerid','PlayerName','Team']),on=['pitcher','game_year'])
d=d[d.Pitches>=300]
# (a) command cost
ch=pd.read_csv('data/derived/slot_changers.csv'); ad=pd.read_csv('data/derived/pitch_additions.csv')
pairs=[]
allp=d[['pitcher','game_year','sp_location','sp_stuff','sp_pitching']].copy(); nx=allp.copy(); nx['game_year']-=1
pp=allp.merge(nx,on=['pitcher','game_year'],suffixes=('','_next')); pp['d_loc']=pp.sp_location_next-pp.sp_location; pp['d_stf']=pp.sp_stuff_next-pp.sp_stuff; pp['d_pit']=pp.sp_pitching_next-pp.sp_pitching
print("ΔLoc+ next season — all pairs %.2f (n=%d) | slot changers ≥5°: %.2f (n=%d) steeper %.2f flatter %.2f | ≥8°: %.2f (n=%d) | pitch adders: %.2f (n=%d)" % (
  pp.d_loc.mean(),len(pp),ch.d_loc.mean(),len(ch),ch[ch.d_slot>0].d_loc.mean(),ch[ch.d_slot<0].d_loc.mean(),ch[ch.d_slot.abs()>=8].d_loc.mean(),(ch.d_slot.abs()>=8).sum(),ad.d_loc.mean(),ad.d_loc.notna().sum()))
print("ΔStuff+ next season — all %.2f | changers %.2f | ≥8° %.2f | adders %.2f ;  ΔPit+ — all %.2f | changers %.2f | adders %.2f" % (
  pp.d_stf.mean(),ch.d_stuff.mean(),ch[ch.d_slot.abs()>=8].d_stuff.mean(),ad.d_stuff.mean(),pp.d_pit.mean(),ch.d_pit.mean(),ad.d_pit.mean()))
# regression: ΔLoc+ on |Δslot| controlling for mean reversion (Loc+ level)
cc=ch.dropna(subset=["d_loc","locp"]); X=np.c_[cc.d_slot.abs(),cc.locp-100]; y=cc.d_loc; lr=LinearRegression().fit(X,y); print("ΔLoc+ = %.2f + %.2f*|Δslot| + %.2f*(Loc+ - 100)  [changers]" % (lr.intercept_,*lr.coef_))
# (b) Pitching+ ~ Stuff+ + Location+
m=d.dropna(subset=['sp_pitching','sp_stuff','sp_location']); lr=LinearRegression().fit(m[['sp_stuff','sp_location']],m.sp_pitching)
r2=lr.score(m[['sp_stuff','sp_location']],m.sp_pitching); print("Pitching+ ≈ %.1f + %.3f*Stuff+ + %.3f*Location+   R² %.3f (n=%d)" % (lr.intercept_,*lr.coef_,r2,len(m)))
# (c) value map: same-season and next-season outcomes
def wr(a,b,w): a,b,w=np.asarray(a,float),np.asarray(b,float),np.asarray(w,float); k=np.isfinite(a)&np.isfinite(b); a,b,w=a[k],b[k],w[k]; ma,mb=np.average(a,weights=w),np.average(b,weights=w); return np.average((a-ma)*(b-mb),weights=w)/np.sqrt(np.average((a-ma)**2,weights=w)*np.average((b-mb)**2,weights=w))
nx=d[['pitcher','game_year','ERA','FIP','xERA','xFIP','SIERA','WAR','IP','GS','G']].copy(); nx['game_year']-=1
q=d.merge(nx,on=['pitcher','game_year'],suffixes=('','_next')); q=q[q.IP_next>=40]
q['war180_next']=q.WAR_next/q.IP_next*180
print(f"\nnext-season (IP_next>=40, n={len(q)}), IP-weighted r:")
for tgt in ['ERA_next','FIP_next','xERA_next','SIERA_next','war180_next']:
    print(f"  {tgt:12s} Stuff+ {wr(q.sp_stuff,q[tgt],q.IP_next):+.3f} | Loc+ {wr(q.sp_location,q[tgt],q.IP_next):+.3f} | Pitching+ {wr(q.sp_pitching,q[tgt],q.IP_next):+.3f} | same-season ERA {wr(q.ERA,q[tgt],q.IP_next):+.3f} | SIERA {wr(q.SIERA,q[tgt],q.IP_next):+.3f}")
# Pitching+ -> next-season ERA and WAR/180 (linear, IP-weighted), by role
q['role']=np.where(q.GS_next/q.G_next>=0.5,'SP','RP')
for role,g in q.groupby('role'):
    w=g.IP_next
    b=np.polyfit(g.sp_pitching,g.ERA_next,1,w=np.sqrt(w)); c=np.polyfit(g.sp_pitching,g.war180_next,1,w=np.sqrt(w))
    print(f"{role}: next ERA = {b[1]:.2f} {b[0]:+.3f}*Pit+ ; next WAR/180 = {c[1]:.2f} {c[0]:+.3f}*Pit+  (n={len(g)}, median IP_next {g.IP_next.median():.0f})  → 1 Pit+ ≈ {c[0]:.3f} WAR/180 ≈ {c[0]*g.IP_next.median()/180:.3f} WAR at median IP")
pd.DataFrame({'note':['see stdout']}).to_csv('data/derived/value_map_ran.csv',index=False)
