from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Team import Team
from Player import Player
import util
import random

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service,options=options)
driver.close


#testing purposes
players = []
def readFromPlayerAndTeamsFile(): # dette burde nok også være i initiate
    file = open(r"./logs/PlayerAndTeams.txt","r",encoding="utf-8")
    for line in file.readlines(): 
        if ":" in line.lower():
            players.append(Player(line.strip(":"),[]))
        else:
            strippedSplitLine = util.removeInvalidLetters(line.rstrip()).split(",")
            players[-1].addTeam(Team(strippedSplitLine[0],strippedSplitLine[1],strippedSplitLine[2],driver))         

readFromPlayerAndTeamsFile()
def printTeams():
    for x in players:
        for y in x.teams:
            print(f"{x.name} {y.Url}")
printTeams()


def UpdateFerieKasse():
    pass



driver.quit() #sørg for at brug den oftere

