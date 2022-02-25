import constants as const
from selenium.webdriver.common.by import By
import webdriverHelper as wdHelper
import os
from .MenuItem import MenuItem
import keyboard
import time
#from collections import defaultdict
class Menu:
    
    def __init__(self,players,title,webDriver):
        self.players = players;
        self.playerCount = len(players)
        self.title = title
        self.webDriver = webDriver
        self.options = self.getOptions()
        self.__selectedIndex = 0
        #self.addUnderMenus()
        self.running = False
    def getOptions(self):
        options = []
        i = 0
        for country,league in const.LeagueNationsDict.items():
            options.append(MenuItem(f"{country}-{league}"))
            self.addUnderMenu(country,league,i)
            i+=1
        return options
    def addUnderMenu(self,country,league,i):
        self.webDriver.get(f"{const.LINK}/fodbold/{country}/{league}/tabeloversigt")
        wdHelper.acceptCookies(self.webDriver)
        allTeamRows = self.webDriver.find_elements_by_css_selector("div.ui-table__row")
        for row in allTeamRows:
            teamRow = row.find_element(By.CLASS_NAME, "tableCellParticipant__name")
            #options[f"{country}-{league}"].append(teamRow.get_attribute("innerHTML"))
    def run(self):
        self.running = True
        os.system("cls")
        while self.running:
            self.displayMenu()
            self.readInput()
    def displayMenu(self):
        os.system("cls")
        print(self.title)
        for i in range(len(self.options)):
            if (i == self.__selectedIndex):
                print("  >",end="")
            print(self.options[i].title)
        #for option in self.options:
        #    print(option.title)
    def readInput(self):
        i = 0
        while True:
            key = keyboard.read_key()
            if (key=="pil op"):
                self.moveUp()
                return
            elif (key =="pil ned"):
                self.moveDown()
                return
            elif (key == "enter"):
                print(key)
                return
    def moveUp(self):
        time.sleep(.1)
        if (self.__selectedIndex - 1 < 0):
            self.__selectedIndex = len(self.options)-1
        else:
            self.__selectedIndex -= 1
    def moveDown(self):
        time.sleep(.1)
        if (self.__selectedIndex + 1 >= len(self.options)):
            self.__selectedIndex = 0
        else:
            self.__selectedIndex += 1
    ####arbejd på at gøre menus mere dynamiske, så den indeholder en anden menu. - stjæl fra c# opgave