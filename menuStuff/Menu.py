import constants as const
from selenium.webdriver.common.by import By
import webdriverHelper as wdHelper
import os
from MenuItem import MenuItem
#from collections import defaultdict

class Menu:
    def __init__(self,players,title,webDriver):
        self.players = players;
        self.playerCount = len(players)
        self.title = title
        self.webDriver = webDriver
        self.options = self.getOptions()
        self.addUnderMenus()
        self.running = False
    def getOptions(self):
        options = []
        i = 0
        for country,league in const.LeagueNationsDict.items():
            options.append(MenuItem(f"{country}-{league}"))
            self.addUnderMenu(country,league,i)
            i+=1
        return options
    def addUnderMenu(self,country,league):
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
        pass
    def readInput(self):
        pass
    ####arbejd på at gøre menus mere dynamiske, så den indeholder en anden menu. - stjæl fra c# opgave