from datetime import date
from classes.League import League
from classes.Team import Team
import utilities.util as util

import orjson
import codecs #for reading non-ascii chars

def getAllLeagues():
    leagues = []
    file = codecs.open(r"./logs/leaguesAndTeams.json","r",encoding='UTF-8')
    jsonData = orjson.loads(file.read())
    for leagueAndCountry in jsonData:
        league,country = leagueAndCountry.split(",")
        league = League(league,country)
        for teamName in jsonData[leagueAndCountry]:
            player = jsonData[leagueAndCountry][teamName]
            league.teams.append(Team(teamName,player))
        leagues.append(league)
    return leagues