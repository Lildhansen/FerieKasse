#libraries - standard or pip
import json
from collections import namedtuple

#own modules
from classes.Player import Player
from classes.Match import Match
import utilities.util as util
from utilities.Webdriver import Webdriver as wd
import helperMain


 
def UpdateFerieKasse():
    leagues = helperMain.getAllLeagues()
    players = util.getPlayerObjectsFromFile()
    for league in leagues:
        ##kunne godt bruge threads her
        match = getLatestMatchCovered(league)
        if match == None:
            league.getMatchesAfterLatestMatch()
        else:
            league.getMatchesAfterLatestMatch(match)
        league.calculatePointsForMatches()
        for match in league.matches:
            awardPointsToPlayers(match,players,league)
        return
    #skriv til excel
    

def getLatestMatchCovered(league):
    file = open(r"./logs/latestMatchCovered.json","r")
    fileJson = json.loads(file.read())
    fileDict = fileJson[f"{league.country},{league.name}"]
    if fileDict == {}: #if no latest match was covered - ie it is the first time we run main_update
        return None
    match = json.loads(fileDict)
    matchJson = json.dumps(match)
    matchTuple = json.loads(matchJson, object_hook = lambda d : namedtuple('Match', d.keys())(*d.values()))
    file.close()
    return util.matchTupleToMatchObject(matchTuple)
    
def awardPointsToPlayers(match,players,league):
    if match.homeTeamIsPlayerTeam:
        homePlayer = getPlayerThatHasTeam(match.homeTeam,players)
    if match.awayTeamIsPlayerTeam:
        awayPlayer = getPlayerThatHasTeam(match.awayTeam,players)
    if match.homeTeamIsWinner:
        tryAddPoints(awayPlayer,match.points)
    elif not match.homeTeamIsWinner:
        tryAddPoints(homePlayer,match.points)
    elif match.draw:
        tryAddPoints(awayPlayer,match.points)
        tryAddPoints(homePlayer,match.points)
           
def getPlayerThatHasTeam(teamName,players):
    for player in players:
        for team in player.teams:
            if team.name == teamName:
                return player
    return None

def tryAddPoints(player,points):
    if player == None:
        return
    player.points.append(points)
    
if __name__ == "__main__":
    UpdateFerieKasse()

