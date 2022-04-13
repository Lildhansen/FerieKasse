#libraries - standard or pip
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#own libraries
from classes.Match import Match
import utilities.util as util

class Webdriver:
    def __init__(self):
        self.setupDriver()
        self.driver = webdriver.Chrome(service=self.__service,options=self.__options) #service=self.__service,
    #sets up services and options for the webdriver
    def setupDriver(self):
        self.__service = Service("./chromedriver.exe")
        self.__options = Options()
        #self.__options.headless = True
        self.__options.add_experimental_option("excludeSwitches", ["enable-logging"])
    def findLeagueUrl(self,searchText):
        self.driver.get('http://www.google.com')
        self.acceptCookies()
        searchField = self.driver.find_element(By.NAME, 'q')
        searchField.send_keys(searchText + " ")
        searchField.submit()
        self.driver.find_element(By.CSS_SELECTOR,"#sports-app > div > div.imso-ft.duf-h > div.imso-loa.imso-ani > div > g-immersive-footer > g-fab > span").click()   
        #soccerway
    #accepts cookies when using the selenium webdriver - not sure if it is neccessary
    def acceptCookies(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#L2AGLb > div"))).click()
        except:
            pass
    #clicks the "vis flere kampe"-button on flash score until all matches are shown
    def showAllMatches(self):
        while True:
            showMoreButton = []
            i = 0
            while i < 10 and showMoreButton == []:
                time.sleep(0.3)
                i += 1
                showMoreButton = self.driver.find_elements_by_css_selector("#live-table > div.event.event--results > div > div > a")
            if showMoreButton == []:
                return
            actions = ActionChains(self.driver)
            actions.move_to_element(showMoreButton[0]).perform()
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            showMoreButton[0].click()
    def getMatchesAfterLatestMatch(self,latestMatch):
        time.sleep(1)
        # for testing ----------
        latestMatch.date = datetime.date(2022, month=4, day=10)
        latestMatch.homeTeam = "Brentford"
        latestMatch.awayTeam = "West Ham"
        latestMatch.homeGoals = 2
        latestMatch.awayGoals = 0
        #_---------------------------
        #check date for first match - if date is earlier than date of the match, more matches needs to be loaded in.
        allMatches = []
        currentMatch = Match()
        rawMatchesData = None
        while (True):
            #used to check if top of page has been reached
            if rawMatchesData == None: 
                previousTopMatchData = None
            else:
                previousTopMatchData = rawMatchesData[0]

            rawMatchesData = self.loadDataForAllMatches()
            allMatches = self.rawMatchesToMatchObjects(rawMatchesData)
            currentMatch = self.rawMatchToMatchObject([rawMatchesData[2].text,rawMatchesData[4].text,rawMatchesData[5].text])
            if util.compareDates(currentMatch.date,latestMatch.date): #currentMatch.date > latestMatch.date
                TopMatchData = rawMatchesData[0]
                if (previousTopMatchData == TopMatchData): #has reached the top - meaning all matches must be checked
                    break
                self.scrollToTop(TopMatchData)
                time.sleep(1)
            else: #currentMatch.date =< latestMatch.date ##det virker vist ikke helt
                i = 2
                while (currentMatch != latestMatch):
                    print(currentMatch.date,currentMatch.homeTeam,currentMatch.homeGoals,currentMatch.awayTeam,currentMatch.awayGoals,"=",latestMatch.date,latestMatch.homeTeam,latestMatch.homeGoals,latestMatch.awayTeam,latestMatch.awayGoals)
                    currentMatch = self.rawMatchToMatchObject([rawMatchesData[i].text,rawMatchesData[i+2].text,rawMatchesData[i+3].text])
                    i += 8
                allMatches = allMatches[allMatches.index(currentMatch)+1::]
                break
        return allMatches
    
    def loadDataForAllMatches(self):
        matchElements = self.driver.find_elements(By.XPATH,"//*[@class='KAIX8d']/tbody//tr") ##finds all <tr>'s in all matches
        i = 2
        while i <= len(matchElements): #removes all non-finished matches
            if (not "FT" in matchElements[i].text):
                matchElements = matchElements[:i-2:]
                break
            i += 8
        return matchElements      
            
    def scrollToTop(self,topElement):
        action = ActionChains(self.driver)
        action.move_to_element(topElement).perform()
    def rawMatchesToMatchObjects(self,rawMatches):
        allMatches = []
        i = 2
        while i <= len(rawMatches):
            match = self.rawMatchToMatchObject([rawMatches[i].text,rawMatches[i+2].text,rawMatches[i+3].text])
            ##test to see if match is valid - ie if any "teams" in that "league" is their home/away team
            allMatches.append(match)
            i += 8
        return allMatches
    def rawMatchToMatchObject(self,rawMatchData):
        matchData = []
        for data in rawMatchData:
            data = data.strip()
        #date
        rawDate = rawMatchData[0].split("\n")[1]
        matchData.append(util.textToDate(rawDate))
     
        #teams and goal
        i = 1
        while i < len(rawMatchData):
            teamAndGoals = rawMatchData[i].split("\n")
            goals = util.parseIntOrNone(teamAndGoals[0])
            team = teamAndGoals[1]
            matchData.append(team)
            matchData.append(goals)
            i += 1
        return Match(matchData)
    #closes the webdriver
    def quit(self):
        self.driver.quit()