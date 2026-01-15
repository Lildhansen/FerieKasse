SEARCH_BAR_ICON = "#search-window"
LeagueNationsDict = {"eng.1": {},
    "ger.1": {},
    "esp.1": {},
    "ita.1": {},
    "den.1": {}}
global POINTS_PER_GOAL
POINTS_PER_GOAL = 5
global DRAW_POINTS
DRAW_POINTS = 5
global LOSE_POINTS
LOSE_POINTS = 5
global INDBYRDES_MULTIPLIER
INDBYRDES_MULTIPLIER = 2
global TEAMS_PER_PLAYER
TEAMS_PER_PLAYER = 6 #EXTRA_TEAMS_PER_PLAYER is included in this
global EXTRA_TEAMS_PER_PLAYER
EXTRA_TEAMS_PER_PLAYER = 1 
global FOUR_GOAL_WIN_BONUS_POINTS
FOUR_GOAL_WIN_BONUS_POINTS = -10
global SKIP_POSTPONED_MATCHES
SKIP_POSTPONED_MATCHES = True

global FERIEKASSE_NAME
FERIEKASSE_NAME = ""

global FOUR_GOAL_WIN_RULE
FOUR_GOAL_WIN_RULE = False

SEND_MAIL_INTERVAL_DAYS = 14
TRAILING_PERCENTAGE_THRESHOLD = 10 #as in, in order for 2 players to be trailing each other there must be no more than 10% point difference

AVAILABLE_COLORS = ["ff0000","00ff00","0000ff","ff9933","000000","ff00ff"]

ESPN_LEAGUE_NAME_TO_PRETTY_LEAGUE_NAME = {
    "eng.1":"Premier League (England)",
    "ger.1":"Bundesliga (Germany)",
    "esp.1":"La Liga (Spain)",
    "ita.1":"Serie A (Italy)",
    "den.1":"Superliga (Denmark)"
    }

PRETTY_LEAGUE_NAME_TO_ESPN_LEAGUE_NAME = {
    "Premier League (England)":"eng.1",
    "Bundesliga (Germany)":"ger.1",
    "La Liga (Spain)":"esp.1",
    "Serie A (Italy)":"ita.1",
    "Superliga (Denmark)":"den.1"
}
