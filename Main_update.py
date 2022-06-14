#libraries - standard or pip
import json
import orjson
from collections import namedtuple

#own modules
from classes.Player import Player
from Excel import Excel
from classes.Match import Match
import utilities.util as util
from utilities.Webdriver import Webdriver as wd
import helperMain

def setupLinks(leagues):
    for league in leagues:
        if league.name == "Superliga":
            league.link = "https://www.google.com/search?q=superliagetable&sxsrf=ALiCzsbrRcpPR73yMygkacEmQt88qS6qSQ%3A1655221225444&ei=6auoYoHeGobRqwG91JaoBg&ved=0ahUKEwjB9qrJo634AhWG6CoKHT2qBWUQ4dUDCA4&uact=5&oq=superliagetable&gs_lcp=Cgdnd3Mtd2l6EAMyBAgAEA0yBAgAEA0yBAgAEA0yCAgAEB4QBxAKMgQIABANMgQILhANMgQIABANMgYIABAeEA0yBggAEB4QDTIGCAAQHhANOgcIIxCwAxAnOgcIABBHELADOgcIABCwAxBDOgwILhDIAxCwAxBDGAE6BggAEB4QBzoECAAQEzoICAAQHhAHEBM6CggAEB4QBxAKEBM6CAguEB4QBxATOggIABAeEA0QCjoICAAQHhANEBM6CggAEB4QDRAFEBNKBAhBGABKBAhGGAFQ8QxYyytgvi9oBXABeACAAWyIAakIkgEEMTEuMZgBAKABAcgBFMABAdoBBggBEAEYCA&sclient=gws-wiz#sie=lg;/g/11nmr_75gx;2;/m/06bxjb;mt;fp;1;;"
        elif league.name == "premier-league":
            league.link = "https://www.google.com/search?q=premier+league+table#sie=lg;/g/11p44qhs93;2;/m/02_tc;mt;fp;1;;"
        elif league.name == "Bundesliga":
            league.link = "https://www.google.com/search?q=bundesliga+1+table&sxsrf=ALiCzsZkk_XyHAIj70_EmJr_WlhI6SKIQw%3A1655222309694&ei=JbCoYq2FKovMrgTmuonYAQ&ved=0ahUKEwjtq6zOp634AhULposKHWZdAhsQ4dUDCA4&uact=5&oq=bundesliga+1+table&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEB4QBzIGCAAQHhAHMgYIABAeEAcyBggAEB4QBzIGCAAQHhAHMgYIABAeEAcyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgcIABBHELADOgcIABCwAxBDOgwILhDIAxCwAxBDGAE6DwguENQCEMgDELADEEMYAToECCMQJzoICAAQHhAHEAo6CAgAEB4QBxATOgoIABAeEAcQChATSgQIQRgASgQIRhgBUOITWLwaYMcbaANwAXgAgAFQiAGcApIBATSYAQCgAQHIARTAAQHaAQYIARABGAg&sclient=gws-wiz#sie=lg;/g/11m__0kr76;2;/m/037169;mt;fp;1;;"
        elif league.name == "serie-a":
            league.link = "https://www.google.com/search?q=serie+a+table&oq=serie+a+table&aqs=chrome.0.69i59j0i512l9.6906j0j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11n0vx7n5d;2;/m/03zv9;mt;fp;1;;"
        elif league.name == "laliga":
            league.link = "https://www.google.com/search?q=laliga+table&oq=la&aqs=chrome.1.69i57j35i19i39j69i59j35i19i39j0i131i433j69i60l3.1694j0j9&sourceid=chrome&ie=UTF-8#sie=lg;/g/11mqlmppsd;2;/m/09gqx;mt;fp;1;;"
            

def UpdateFerieKasse():
    leagues = helperMain.getAllLeagues()
    setupLinks(leagues) ##remove this when in midst of season
    players = util.getPlayerObjectsFromFile()
    for league in leagues:
        print("working on",league.name) #for some reason league.name starts with a space??
        ##kunne godt bruge threads her
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
    
    #skriv til excel
    

def getLatestMatchCovered(league):
    file = open(r"./logs/latestMatchCovered.json","r")
    fileJson = json.loads(file.read())
    fileDict = fileJson[f"{league.name},{league.country}"]
    if fileDict == {}: #if no latest match was covered - ie it is the first time we run main_update
        return None
    match = json.loads(fileDict)
    matchJson = json.dumps(match)
    matchTuple = json.loads(matchJson, object_hook = lambda d : namedtuple('Match', d.keys())(*d.values()))
    
    file.close()
    return util.matchTupleToMatchObject(matchTuple)

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
           
def getPlayerThatHasTeam(teamName,players):
    for player in players:
        for team in player.teams:
            if team == teamName:
                return player
    return None

def tryAddPoints(player,points):
    if player == None:
        return
    player.points.append(points)
    
if __name__ == "__main__":
    UpdateFerieKasse()

