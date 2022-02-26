#libraries - standard or pip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import os
#own modules
from menuStuff.Menu import Menu
import util
from Player import Player
from Team import Team

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service,options=options)

#terminal prompting the user the selection of players, then initiating the menu for selecting teams
def setupMenuInitiation():
    numOfPlayers = ""
    players = []
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
    players = []
    file = open(r"./logs/PlayerAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        if ":" in line.lower():
            players.append(Player((line.rstrip()).strip(":"),[]))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            players[-1].addTeam(Team(strippedSplitLine[0],strippedSplitLine[1],strippedSplitLine[2],driver))  
    driver.quit()
    for player in players:
        player.addToPlayersTeamsAndLinksFile()

#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    if (os.path.isfile(r"./logs/PlayerAndTeams.txt") and os.path.getsize(r"./logs/PlayerAndTeams.txt") > 0):
        setupFileInitiation()
    else:
        setupMenuInitiation()

driver.quit()


if __name__ == "__main__":
    initiateFerieKasse()