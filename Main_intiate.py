#æøå skal fjernes når de tilføjes til txt-filer samt når de skal bruges i flashscore link(her skal de erstattes af -)
#landene må ikke stå med stort

#optimeringsmuligheder:
    #når den skal finde holdene, skal den samle dem alle i lande, så den laver minimal søgninger til chrome

#initiate skal kunne gøres enten gennem en fil - eller gennem en menu

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from Team import Team
from Player import Player
from menuStuff.Menu import Menu
import util
import random

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service,options=options)
def setupPlayers():
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
    #menu kunne være lidt federe her
    #den skal dog stadig hente data fra resultat - og skrive holdene, og fjerne de hold som er taget. måske menu alligvel
def selectTeams(): 
    setupPlayers()
    #kunne laves så man kunne lave en sorteringfunktion - fx kun klubber med danskere - og så vil værdierne ændres
def IntiateFerieKasse():
    pass



#selectTeams()
#Menu(["1","2","3","4"],"Select a league/country",driver).run()

