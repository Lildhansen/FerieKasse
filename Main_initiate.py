#libraries - standard or pip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
#own modules
from menuStuff.Menu import Menu
import util

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service,options=options)
#terminal prompting the user the selection of players, then initiating the menu for selecting teams
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



#the main function of the file - sets up the feriekasse
def initiateFerieKasse():
    setupPlayers()

driver.quit()


if __name__ == "__main__":
    initiateFerieKasse()