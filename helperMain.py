from classes.League import League
from classes.Team import Team
import utilities.util as util

def getAllLeagues():
    leagues = []
    file = open(r"./logs/leaguesAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        strippedSplitLine = ""
        if ":" in line:
            strippedSplitLine = (line.rstrip()).strip(":").split(",") #strips white space and then strips the ":". finally the string is splitted into name and country by ","
            leagues.append(League(strippedSplitLine[0],strippedSplitLine[1])) #league is then created
        else: #if it is not a league, it is a team,player
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",") #removes whitespace and invalid letters of the team - then split the string into name and playername
            leagues[-1].teams.append(Team(strippedSplitLine[0],strippedSplitLine[1]))
    return leagues