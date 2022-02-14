from logging import exception
from selenium.webdriver.common.by import By
import os
import webdriverHelper as wdHelper

import constants as const
import time
class Team:
    def __init__(self,name,league,country,player,webdriver):
        self.name = name
        self.league = league
        self.country = country
        self.player = player
        self.webdriver = webdriver
        self.Url = self.getTeamURL()
    def getTeamURL(self):
        url = self.GetURLFromFile()
        if url == None:
            self.webdriver.get(f"{const.LINK}/fodbold/{self.country}/{self.league}/tabeloversigt")
            wdHelper.acceptCookies(self.webdriver)
            allTeamRows = self.webdriver.find_elements_by_css_selector("div.ui-table__row")
            url = self.addTeamAndUrlToFileAndReturnURL(allTeamRows)
        return url
    def addTeamAndUrlToFileAndReturnURL(self,allTeamRows):
        for row in allTeamRows:
            teamRow = row.find_element(By.CLASS_NAME, "tableCellParticipant__name")
            if teamRow.get_attribute("innerHTML").lower() == self.name.lower():
                file = open(r"./logs/teams.txt","a+")
                file.write(f"{teamRow.get_attribute('innerHTML')},{teamRow.get_attribute('href')}\n")
                file.close()
                return teamRow.get_attribute('href')
    def GetURLFromFile(self):
        if not os.path.isfile(r"./logs/teams.txt"):
            return None
        file = open(r"./logs/teams.txt","r")
        for line in file.readlines():
            if self.name.lower() in line.lower():
                return line[line.index(",")+1:line.index("\n"):]
        return None


    

