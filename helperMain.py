from classes.League import League
from classes.Team import Team
import utilities.constants as const

import orjson
import codecs #for reading non-ascii chars

def getAllLeagues():
    leagues = []
    file = codecs.open(fr"./data/{const.FERIEKASSE_NAME}/leaguesAndTeams.json","r",encoding='UTF-8')
    jsonData = orjson.loads(file.read())
    for leagueAndCountry in jsonData:
        league,country = leagueAndCountry.split(",")
        league = League(league,country)
        for teamName in jsonData[leagueAndCountry]:
            player = jsonData[leagueAndCountry][teamName]
            league.teams.append(Team(teamName,player,league.name))
        leagues.append(league)
    return leagues