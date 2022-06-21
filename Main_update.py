#libraries - standard or pip
import codecs
import json
from collections import namedtuple

#own modules
from Excel import Excel
import utilities.util as util
import helperMain

def setupLinks(leagues):
    for league in leagues:
        if league.name == "superliga":
            league.link = "https://fbref.com/en/comps/50/schedule/Superliga-Scores-and-Fixtures"
        elif league.name == "premier-league":
            league.link = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
        elif league.name == "bundesliga":
            league.link = "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures"
        elif league.name == "serie-a":
            league.link = "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures"
        elif league.name == "laliga":
            league.link = "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures"

def UpdateFerieKasse():
    leagues = helperMain.getAllLeagues()
    setupLinks(leagues)
    players = util.getPlayerObjectsFromFile()
    for league in leagues:
        print("working on",league.name)
        match = getLatestMatchCovered(league)
        if match == None:
            league.getMatchesAfterLatestMatch()
        else:
            league.getMatchesAfterLatestMatch(match)
        league.calculatePointsForMatches()
        league.removeMatchesYielding0Points()
        for match in league.matches:
            assignMatchToPlayers(match,players)
    myExcel = Excel(leagues)
    myExcel.updateExcelFile(players)
    

def getLatestMatchCovered(league):
    file = codecs.open(r"./logs/latestMatchCovered.json","r")
    fileJson = json.loads(file.read())
    fileDict = fileJson[f"{league.name},{league.country}"]
    if fileDict == {}: #if no latest match was covered - ie it is the first time we run main_update
        return None
    match = json.loads(fileDict)
    matchJson = json.dumps(match)
    matchTuple = json.loads(matchJson, object_hook = lambda d : namedtuple('Match', d.keys())(*d.values()))
    file.close()
    return util.matchTupleToMatchObject(matchTuple)

#assigns a specific match to a player depending on if one of the player's team is in the match (will only assign match to player if the player loses point for that match)
#can be assigned to 2 players, if it is a draw with 2 different players' teams
def assignMatchToPlayers(match,players):
    homePlayer, awayPlayer = None,None
    if match.homeTeamIsPlayerTeam:
        homePlayer = getPlayerThatHasTeam(match.homeTeam,players)
    if match.awayTeamIsPlayerTeam:
        awayPlayer = getPlayerThatHasTeam(match.awayTeam,players)
    if match.homeTeamIsWinner or match.draw:
        tryAppendMatch(awayPlayer,match)
    if not match.homeTeamIsWinner or match.draw:
        tryAppendMatch(homePlayer,match)

def tryAppendMatch(player,match):
    if player == None:
        return
    player.matches.append(match)
          
#returns the player that has the team with the given name from a list of players 
def getPlayerThatHasTeam(teamName,players):
    for player in players:
        for team in player.teams:
            if team == teamName:
                return player
    return None
    
if __name__ == "__main__":
    UpdateFerieKasse()
