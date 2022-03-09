#libraries - standard or pip
import random
import os
#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.Player import Player
from classes.Team import Team
from Excel import Excel
from utilities.Webdriver import Webdriver

driver = Webdriver()

players = []

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
    file = open(r"./logs/PlayerAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        if ":" in line.lower():
            players.append(Player((line.rstrip()).strip(":"),[]))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            players[-1].addTeam(Team(strippedSplitLine[0],strippedSplitLine[1],strippedSplitLine[2],driver))  
    driver.quit()
    file = open(r"./logs/playersTeamsAndLinks.txt","a+") #this is not unreachable lol- dunno why it says so
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