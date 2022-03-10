#libraries - standard or pip

#own modules
from classes.Team import Team
from classes.Player import Player
import utilities.util as util
from utilities.Webdriver import Webdriver as wd

driver = wd()

def getAllPlayers():
    currentplayers = []
    file = open(r"./logs/playersTeamsAndLinks.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        if not ("," in line.lower()):
            currentplayers.append(Player((line.rstrip()).strip(":"),[]))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",") #remove invalid letters burde ikke være nødvendig, men ig
            currentplayers[-1].addTeam(Team(strippedSplitLine[0],url=strippedSplitLine[1],webdriver=driver))  
    return currentplayers

 
def UpdateFerieKasse():
    players = getAllPlayers()
    for player in players:
        player.updateTeamPoints()

if __name__ == "__main__":
    UpdateFerieKasse()

