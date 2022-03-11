#libraries - standard or pip
from selenium.webdriver.common.by import By
import os

#own modules
import utilities.util as util
import utilities.constants as const
from classes.Match import Match
from classes.Match import IndbyrdesMatch
class Team:
    def __init__(self,name,league=None,country="",webdriver=None,url=None):
        self.name = util.removeInvalidLetters(name)
        self.league = league
        self.country = country.lower()
        self.webdriver = webdriver
        if url == None:
            self.url = self.getTeamURL()
        else:
            self.url = url
        self.points = 0 #this will be changed with the main_update
        self.currentMatches = []
    #get URL for a team - either from the team.txt or with the webdriver
    def getTeamURL(self):
        url = self.getURLFromFile()
        if url == None:
            url = self.getURLWithWebdriver()
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
    #gets the team's URL with the webdriver
    def getURLWithWebdriver(self):
        self.webdriver.get(f"{const.LINK}/fodbold/{self.country}/{self.league}/tabeloversigt")
        self.webdriver.acceptCookies()
        allTeamRows = self.webdriver.find_elements_by_css_selector("div.ui-table__row")
        return self.addTeamAndUrlToFileAndReturnURL(allTeamRows)
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
    def updatePointsForMatches():
        
        ##her skal der findes alle matches i denne uge - og på den måde sørge for at få alle med - og ingen duplicates
        
        

    

