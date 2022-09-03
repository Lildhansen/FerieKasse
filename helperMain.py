from classes.League import League
from classes.Team import Team
import utilities.constants as const

import os
import orjson
import codecs #for reading non-ascii chars

#Get all leagues with all their teams from the JSON file
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

#List the name of all feriekasser in the data folder
def listAllFeriekasser():
    for feriekasse in os.listdir("data"):
        feriekasseDirectory = os.path.join("data", feriekasse)
        if os.path.isdir(feriekasseDirectory):
            print(feriekasse)
            
#handles the case where the user inputs multiple feriekasser, and return a list of all the feriekasser
def handleMultipleArgumentsForFeriekasser(userInput):
    feriekasser = []
    feriekasseArguments = userInput.split(",")
    for feriekasse in feriekasseArguments:
        if not os.path.exists(fr"data/{feriekasse}"):
            raise Exception(f"feriekasse {feriekasse} does not exist")
        if feriekasse == "" or feriekasse.isspace():
            continue
        feriekasser.append(feriekasse.strip())
    return feriekasser