#libraries - standard or pip
from selenium.webdriver.common.by import By
import os

#own modules
import utilities.webdriverHelper as wdHelper
import utilities.util as util
import utilities.constants as const

class Team:
    def __init__(self,name,league,country,webdriver=None):
        self.name = util.removeInvalidLetters(name)
        self.league = league
        self.country = country.lower()
        self.webdriver = webdriver
        self.url = self.getTeamURL()
    #get URL for a team - either from the team.txt or with the webdriver
    def getTeamURL(self):
        url = self.getURLFromFile()
        if url == None:
            self.webdriver.get(f"{const.LINK}/fodbold/{self.country}/{self.league}/tabeloversigt")
            wdHelper.acceptCookies(self.webdriver)
            allTeamRows = self.webdriver.find_elements_by_css_selector("div.ui-table__row")
            url = self.addTeamAndUrlToFileAndReturnURL(allTeamRows)
        return url
    #gets the team's URL from "teams.txt"
    def getURLFromFile(self):
        if not os.path.isfile(r"./logs/teams.txt"):
            return None
        file = open(r"./logs/teams.txt","r")
        for line in file.readlines():
            if self.name.lower() in line.lower():
                return line[line.index(",")+1:line.index("\n"):]
        return None
    #adds the "team,URL" to the "teams.txt"-file for later use
    #this teams.txt serves as a database for the teams already used, making it easier
    # when a new iteration is run - avoiding that every team is recovered with the driver again
    def addTeamAndUrlToFileAndReturnURL(self,allTeamRows):
        for row in allTeamRows:
            teamRow = row.find_element(By.CLASS_NAME, "tableCellParticipant__name")
            if util.removeInvalidLetters(teamRow.get_attribute("innerHTML").lower()) == self.name.lower():
                file = open(r"./logs/teams.txt","a+")
                file.write(f"{self.name.lower()},{teamRow.get_attribute('href')}\n")
                file.close()
                return teamRow.get_attribute('href')


    

