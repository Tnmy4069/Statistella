we have a lot of data 

1. teams.csv
LEAGUE_ID,TEAM_ID,MIN_YEAR,MAX_YEAR,ABBREVIATION,NICKNAME,YEARFOUNDED,CITY,ARENA,ARENACAPACITY,OWNER,GENERALMANAGER,HEADCOACH,DLEAGUEAFFILIATION
00,1610612737,1949,2019,ATL,Hawks,1949,Atlanta,State Farm Arena,18729,Tony Ressler,Travis Schlenk,Lloyd Pierce,Erie Bayhawks
00,1610612738,1946,2019,BOS,Celtics,1946,Boston,TD Garden,18624,Wyc Grousbeck,Danny Ainge,Brad Stevens,Maine Red Claws
00,1610612740,2002,2019,NOP,Pelicans,2002,New Orleans,Smoothie King Center,,Tom Benson,Trajan Langdon,Alvin Gentry,No Affiliate
00,1610612741,1966,2019,CHI,Bulls,1966,Chicago,United Center,21711,Jerry Reinsdorf,Gar Forman,Jim Boylen,Windy City Bulls
and so On....

2. player.csv
PLAYER_NAME,TEAM_ID,PLAYER_ID,SEASON
Royce O'Neale,1610612762,1626220,2019
Bojan Bogdanovic,1610612762,202711,2019
Rudy Gobert,1610612762,203497,2019
Donovan Mitchell,1610612762,1628378,2019
Mike Conley,1610612762,201144,2019
Joe Ingles,1610612762,204060,2019
Ed Davis,1610612762,202334,2019
Jeff Green,1610612762,201145,2019
Dante Exum,1610612762,203957,2019
Emmanuel Mudiay,1610612762,1626144,2019
Georges Niang,1610612762,1627777,2019
Tony Bradley,1610612762,1628396,2019
Nigel Williams-Goss,1610612762,1628430,2019
Tobias Harris,1610612755,202699,2019
And so on....

3.ranking.csv
TEAM_ID,LEAGUE_ID,SEASON_ID,STANDINGSDATE,CONFERENCE,TEAM,G,W,L,W_PCT,HOME_RECORD,ROAD_RECORD,RETURNTOPLAY
1610612743,00,22022,2022-12-22,West,Denver,30,19,11,0.633,10-3,9-8,
1610612763,00,22022,2022-12-22,West,Memphis,30,19,11,0.633,13-2,6-9,
1610612740,00,22022,2022-12-22,West,New Orleans,31,19,12,0.613,13-4,6-8,
1610612756,00,22022,2022-12-22,West,Phoenix,32,19,13,0.594,14-4,5-9,
1610612746,00,22022,2022-12-22,West,LA Clippers,33,19,14,0.576,11-7,8-7,
1610612758,00,22022,2022-12-22,West,Sacramento,30,17,13,0.567,9-5,8-8,
1610612762,00,22022,2022-12-22,West,Utah,35,19,16,0.543,12-5,7-11,
1610612757,00,22022,2022-12-22,West,Portland,32,17,15,0.531,7-6,10-9,
1610612742,00,22022,2022-12-22,West,Dallas,32,16,16,0.5,12-5,4-11,
and so on...

4. games.csv
GAME_DATE_EST,GAME_ID,GAME_STATUS_TEXT,HOME_TEAM_ID,VISITOR_TEAM_ID,SEASON,TEAM_ID_home,PTS_home,FG_PCT_home,FT_PCT_home,FG3_PCT_home,AST_home,REB_home,TEAM_ID_away,PTS_away,FG_PCT_away,FT_PCT_away,FG3_PCT_away,AST_away,REB_away,HOME_TEAM_WINS
2022-12-22,22200477,Final,1610612740,1610612759,2022,1610612740,126,0.484,0.926,0.382,25,46,1610612759,117,0.478,0.815,0.321,23,44,1
2022-12-22,22200478,Final,1610612762,1610612764,2022,1610612762,120,0.488,0.952,0.457,16,40,1610612764,112,0.561,0.765,0.333,20,37,1
2022-12-21,22200466,Final,1610612739,1610612749,2022,1610612739,114,0.482,0.786,0.313,22,37,1610612749,106,0.47,0.682,0.433,20,46,1
2022-12-21,22200467,Final,1610612755,1610612765,2022,1610612755,113,0.441,0.909,0.297,27,49,1610612765,93,0.392,0.735,0.261,15,46,1
2022-12-21,22200468,Final,1610612737,1610612741,2022,1610612737,108,0.429,1.0,0.378,22,47,1610612741,110,0.5,0.773,0.292,20,47,0
ans so on...

5. games_details.csv
GAME_DATE_EST,GAME_ID,GAME_STATUS_TEXT,HOME_TEAM_ID,VISITOR_TEAM_ID,SEASON,TEAM_ID_home,PTS_home,FG_PCT_home,FT_PCT_home,FG3_PCT_home,AST_home,REB_home,TEAM_ID_away,PTS_away,FG_PCT_away,FT_PCT_away,FG3_PCT_away,AST_away,REB_away,HOME_TEAM_WINS
2022-12-22,22200477,Final,1610612740,1610612759,2022,1610612740,126,0.484,0.926,0.382,25,46,1610612759,117,0.478,0.815,0.321,23,44,1
2022-12-22,22200478,Final,1610612762,1610612764,2022,1610612762,120,0.488,0.952,0.457,16,40,1610612764,112,0.561,0.765,0.333,20,37,1
2022-12-21,22200466,Final,1610612739,1610612749,2022,1610612739,114,0.482,0.786,0.313,22,37,1610612749,106,0.47,0.682,0.433,20,46,1
2022-12-21,22200467,Final,1610612755,1610612765,2022,1610612755,113,0.441,0.909,0.297,27,49,1610612765,93,0.392,0.735,0.261,15,46,1
2022-12-21,22200468,Final,1610612737,1610612741,2022,1610612737,108,0.429,1.0,0.378,22,47,1610612741,110,0.5,0.773,0.292,20,47,0
and so on....

### **Problem Statement (Clear & Refined)**

Basketball generates a massive amount of data every season, including team details, player rosters, game results, and league rankings. While this data is rich, it is fragmented across multiple datasets such as teams, players, games, game details, and rankings. In raw form, this data is difficult to interpret and does not directly provide actionable insights for fans, analysts, or decision-makers.

The challenge is to transform this large, multi-table NBA dataset (spanning from the 2004 season to the latest available season) into meaningful insights using data visualization. The dataset contains game-level outcomes, player participation, team metadata, home vs away performance, and conference-wise standings across seasons.

Participants are required to analyze, clean, and integrate these datasets to build an **interactive analytics dashboard** that clearly explains trends, comparisons, and performance patterns in the NBA over time. The goal is not just to show numbers, but to tell a clear data-driven story about how teams, players, and the league have evolved.

---

### **Key Focus Areas**

* Season-wise and team-wise scoring trends
* Player performance, contribution, and efficiency analysis
* Team consistency and win–loss patterns
* Home vs Away performance comparison
* Eastern vs Western Conference performance dynamics

---

### **Task**

Build an **interactive NBA analytics dashboard** using **Python** that enables intuitive exploration of the data.

---

### **Dashboard Must Include**

* **Trends:** Season-wise and game-wise scoring and performance trends
* **Team & Conference Analysis:** Team comparisons and East vs West insights
* **Player Insights:** Key player statistics, consistency, and standout performances
* **Rankings:** Team rankings and win–loss patterns over time
* **Interactivity:** Filters by season, team, and player with short explanatory insights

also show USP
Highlight best and worst seasons, turning points, and outlier games
Insight cards update dynamically based on selected filters

---

### **Outcome**

The final dashboard should help users easily explore NBA data, compare teams and players, and understand long-term trends through clear visuals and structured storytelling.

