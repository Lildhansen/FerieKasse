from selenium.webdriver.common.by import By

import bs4, requests
import constants as const
import time
class Team:
    def __init__(self,name,league,country,player,webdriver):
        self.name = name
        self.league = league
        self.country = country
        self.player = player
        self.webdriver = webdriver
    def getTeamURL(self):
        self.webdriver.get(f"{const.LINK}/fodbold/{self.country}/{self.league}/tabeloversigt")
        self.acceptCookies()
        allTeamRows = self.webdriver.find_elements_by_css_selector("div.ui-table__row")
        self.addTeamToFile(allTeamRows)
        time.sleep(5)
    def acceptCookies(self):
        time.sleep(3)#wait for it to show up
        try:
            self.webdriver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
        except:
            pass
    def addTeamToFile(self,allTeamRows):
        if self.TeamInFile():
            return
        for row in allTeamRows:
            teamRow = row.find_element(By.CLASS_NAME, "tableCellParticipant__name")
            if teamRow.get_attribute("innerHTML").lower() == self.name.lower():
                file = open(r"./logs/teams.txt","a")
                file.write(f"{teamRow.get_attribute('innerHTML')},{teamRow.get_attribute('href')}\n")
                file.close()
                break
    def TeamInFile():
        #se om dette team er i teams.txt


    

