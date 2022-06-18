#libraries - standard or pip
import codecs
import os
import time
import orjson

#own modules
from menuStuff.Menu import Menu
import utilities.util as util
from classes.League import League
from classes.Player import Player
from Excel import Excel
import helperMain
import utilities.constants as const
import random


leagues = []
players = []

#terminal prompting the user the selection of players, then initiating the menu for selecting teams
def setupMenuInitiation():
    numOfPlayers = ""
    while (util.parseIntOrNone(numOfPlayers,1,8) == None):
        numOfPlayers = input("number of players: ")
    numOfPlayers = int(numOfPlayers)
    print(f"write the {numOfPlayers} players (seperated by enter):")
    while len(players) < numOfPlayers:
        players.append(Player(input()))
    random.shuffle(players)
    myMenu = Menu(players,"Select a league/country")
    myMenu.setupMenu()
    myMenu.run()
    myMenu.saveInJson()

#orjson
def setupLatestMatchCoveredForEachLeagueFile():
    with codecs.open("./logs/latestMatchCovered.json","wb") as file:
        file.write(orjson.dumps(const.LeagueNationsDict))

#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    if not (os.path.isfile(r"./logs/leaguesAndTeams.json") and os.path.getsize(r"./logs/leaguesAndTeams.json") > 0):
        setupMenuInitiation()
    helperMain.getAllLeagues()
    myExcel = Excel(leagues)
    myExcel.deleteExcelFile() #should not do this in the end
    myExcel.setupExcelFile()
    setupLatestMatchCoveredForEachLeagueFile()
    



if __name__ == "__main__":
    if os.path.isfile("Feriekasse.xlsx"):
        print("A round has already been started.")
        print("if you want to start a new round, do 'make reset' first")
        input("press enter to continue ...")
    else:
        initiateFerieKasse()