from classes.League import League
import utilities.util as util

def getAllLeagues():
    leagues = []
    file = open(r"./logs/leaguesAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        strippedSplitLine = ""
        if ":" in line.lower():
            strippedSplitLine = (line.rstrip()).strip(":").split(",")
            leagues.append(League(strippedSplitLine[0],strippedSplitLine[1]))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            leagues[-1].teams.append(Team(strippedSplitLine[0],strippedSplitLine[1]))
    return leagues