select
	me.gameid
	,me.goals + tm.goals as teamGoals
	,o1.goals + o2.goals as opponentGoals
    ,me.shots + tm.shots as teamShots
	,o1.shots + o2.shots as opponentShots
    ,me.saves + tm.saves as teamSaves
    ,o1.saves + o2.saves as opponentSaves
	,me.assists + tm.assists as teamAssists
    ,o1.assists + o2.assists as opponentAssists
	,case when (me.goals + tm.goals) > (o1.goals + o2.goals) then 1 else 0 end as win
	,(me.goals + tm.goals) - (o1.goals + o2.goals) as goalDiff
	,sum((me.goals + tm.goals) - (o1.goals + o2.goals)) over (order by me.gameid) as runningGoalDiff
	,round(avg((me.goals + tm.goals)) over (order by me.gameid), 2) as teamRunningGoalAvg
	,round(avg((o1.goals + o2.goals)) over (order by o1.gameid), 2) as opponentRunningGoalAvg
	,(me.goals + tm.goals + o1.saves + o2.saves) / (me.shots + tm.shots) as shotsOnGoalPercent
	--,(me.saves + tm.saves) / case when (o1.shots + o2.shots)::int = 0::int then null end as savePercent
	,gd.overtime
	,gd.comms
from doubles.mystats me
inner join doubles.teammate1 tm
	on tm.gameid = me.gameid
inner join doubles.opponent1 o1
	on o1.gameid = me.gameid
inner join doubles.opponent2 o2
	on o2.gameid = me.gameid
inner join doubles.gamedetails gd
	on gd.gameid = me.gameid
order by me.gameid asc;