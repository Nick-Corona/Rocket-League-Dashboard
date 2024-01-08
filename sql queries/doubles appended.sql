select
	gameid
	,score
	,goals
	,assists
	,saves
	,shots
	,'Me' as player
from doubles.mystats

union all

select
	gameid
	,score
	,goals
	,assists
	,saves
	,shots
	,'Teammate1' as player
from doubles.teammate1

union all

select
	gameid
	,score
	,goals
	,assists
	,saves
	,shots
	,'Opponent1' as player
from doubles.opponent1

union all

select
	gameid
	,score
	,goals
	,assists
	,saves
	,shots
	,'Opponent2' as player
from doubles.opponent2;