#libraries - standard or pip
import random
import os
#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.League import League
from Excel import Excel
from utilities.Webdriver import Webdriver
import helperMain
import utilities.constants as const


leagues = []

#terminal prompting the user the selection of players, then initiating the menu for selecting teams
# def setupMenuInitiation():
#     numOfPlayers = ""
#     while (util.parseIntOrNone(numOfPlayers,1,8) == None):
#         numOfPlayers = input("number of players: ")
#     numOfPlayers = int(numOfPlayers)
#     print(f"write the {numOfPlayers} players (seperated by enter)")
#     while len(players) < numOfPlayers:
#         players.append(input())
#     random.shuffle(players)
#     myMenu = Menu(players,"Select a league/country",driver)
#     myMenu.run()


def setupLatestMatchCoveredForEachLeagueFile():
    file = open("./logs/latestMatchCovered.json","w+")
    file.write("{")
    i = 0
    for country,league in const.LeagueNationsDict.items():
        if i != 0:
            file.write(",\n")
        file.write('"'+country+','+league+'":{}')
        i += 1
    file.write("}")
    file.close() 

#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    if (os.path.isfile(r"./logs/leaguesAndTeams.txt") and os.path.getsize(r"./logs/leaguesAndTeams.txt") > 0):
        helperMain.getAllLeagues()
    else:
        pass
        #setupMenuInitiation()
    myExcel = Excel(leagues)
    myExcel.deleteExcelFile() #should not do this in the end
    myExcel.setupExcelFile()
    setupLatestMatchCoveredForEachLeagueFile()
    



if __name__ == "__main__":
    #if (not) excel sheet er tom - eller slettet:
        #print "a round has already been started" - or something
        #return
    initiateFerieKasse()