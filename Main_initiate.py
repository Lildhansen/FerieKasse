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
import helperMain


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
    leagues = helperMain.getAllLeagues()
    file = open(r"./logs/leaguesTeamsAndLinks.txt","a+")
    file.truncate(0)
    file.close
    for league in leagues:
        league.addToLeaguesTeamsAndLinksFile()

def setupWeeksCoveredForEachLeagueFile():
    file = open("./logs/WeeksCovered.txt","w+")
    file.close() 


#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    if (os.path.isfile(r"./logs/leaguesAndTeams.txt") and os.path.getsize(r"./logs/leaguesAndTeams.txt") > 0):
        setupFileInitiation()
    else:
        pass
        #setupMenuInitiation()
    myExcel = Excel(leagues)
    myExcel.deleteExcelFile() #should not to this in the end - or maybe
    myExcel.setupExcelFile()
    setupWeeksCoveredForEachLeagueFile()
    



if __name__ == "__main__":
    #if (not) excel sheet er tom - eller slettet:
        #print "a round has already been started" - or something
        #return
    initiateFerieKasse()