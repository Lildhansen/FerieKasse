import soccerdata as sd

leagues = ['ENG-Premier League',
 'ESP-La Liga',
 'FRA-Ligue 1',
 'GER-Bundesliga',
 'ITA-Serie A']


for league in leagues:
    sofascore = sd.Sofascore(leagues=league, seasons="2025/2026")
    league_table = sofascore.read_league_table()
    league_table.head() 