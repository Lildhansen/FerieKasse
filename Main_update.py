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
    for league in leagues:
        ##kunne godt bruge threads her
        match = getLatestMatchCovered(league)
        if match == None:
            league.getMatchesAfterLatestMatch()
        else:
            league.getMatchesAfterLatestMatch(match)
        league.calculatePointsForMatches()
        return

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
    


if __name__ == "__main__":
    UpdateFerieKasse()

