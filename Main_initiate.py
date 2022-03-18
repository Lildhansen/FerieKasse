#libraries - standard or pip
import random
import os
#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.League import League
from classes.Team import Team
from Excel import Excel
from utilities.Webdriver import Webdriver

driver = Webdriver()

leagues = []

#terminal prompting the user the selection of players, then initiating the menu for selecting teams
def setupMenuInitiation():
    numOfPlayers = ""
    while (util.parseIntOrNone(numOfPlayers,1,8) == None):
        numOfPlayers = input("number of players: ")
    numOfPlayers = int(numOfPlayers)
    print(f"write the {numOfPlayers} players (seperated by enter)")
    while len(players) < numOfPlayers:
        players.append(input())
    random.shuffle(players)
    myMenu = Menu(players,"Select a league/country",driver)
    myMenu.run()

#setting up the feriekasse with the existence of a PlayerAndTeams.txt-file 
def setupFileInitiation():
    file = open(r"./logs/leaguesAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        strippedSplitLine = ""
        if ":" in line.lower():
            strippedSplitLine = (line.rstrip()).strip(":").split(",")
            leagues.append(leagues(strippedSplitLine[0],strippedSplitLine[1],[],None))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            leagues[-1].teams.append(Team(strippedSplitLine[0],strippedSplitLine[1]))
    driver.quit()
    file = open(r"./logs/leaguesTeamsAndLinks.txt","a+")
    file.truncate(0)
    file.close
    for player in players:
        player.addToPlayersTeamsAndLinksFile()

def setupWeeksCoveredFile():
    file = open("./logs/WeeksCovered.txt","w+")
    file.close() 


#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    if (os.path.isfile(r"./logs/PlayerAndTeams.txt") and os.path.getsize(r"./logs/PlayerAndTeams.txt") > 0):
        setupFileInitiation()
    else:
        setupMenuInitiation()
    myExcel = Excel(players)
    myExcel.deleteExcelFile() #should not to this in the end - or maybe
    myExcel.setupExcelFile()
    setupWeeksCoveredFile()
    


driver.quit()


if __name__ == "__main__":
    #if (not) excel sheet er tom - eller slettet:
        #print "a round has already been started" - or something
        #return
    initiateFerieKasse()