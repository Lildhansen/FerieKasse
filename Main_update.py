from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from Team import Team
from Player import Player
import util
import random

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome( options=options)
    #service=service,

#testing purposes
players = []

def readFromPlayerAndTeamsFile():
    file = open(r"./logs/PlayerAndTeams.txt","r")
    for line in file.readlines(): 
        print(line)
        if ":" in line.lower():
            players.append(Player(line.strip(":")))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            players[-1].addTeam(Team(strippedSplitLine[0],strippedSplitLine[1],strippedSplitLine[2],driver))
            

readFromPlayerAndTeamsFile()
#for x in players:
#   for y in x.teams:
#       print(f"{x.name} {y.Url}")

def UpdateFerieKasse():
    pass


