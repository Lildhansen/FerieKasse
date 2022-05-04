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
    #navigates the webdriver to the url for that specific league
    def findLeagueUrl(self,searchText,isScoreTable):
        self.driver.get('http://www.google.com')
        self.acceptCookies()
        searchField = self.driver.find_element(By.NAME, 'q')
        searchField.send_keys(searchText + " ")
        searchField.submit()
        if (isScoreTable):
            self.driver.find_element(By.CSS_SELECTOR,"#sports-app > div > div:nth-child(2) > div > div > div > ol > li:nth-child(3)").click() 
        else:
            self.driver.find_element(By.CSS_SELECTOR,"#sports-app > div > div.imso-ft.duf-h > div.imso-loa.imso-ani > div > g-immersive-footer > g-fab > span").click() 
    #accepts cookies when using the selenium webdriver
    def acceptCookies(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#L2AGLb > div"))).click()
        except:
            pass
    #takes the latest match that has been processed as input, and get all matches in that specific league between that match+1 and the last played match
    def getMatchesAfterLatestMatch(self,latestMatch,league):
        time.sleep(1) #wait for page to load
        # for testing ----------
        # latestMatch.date = datetime.date(2022, month=4, day=8)
        # latestMatch.homeTeam = "Newcastle"
        # latestMatch.awayTeam = "Wolves"
        # latestMatch.homeGoals = 1
        # latestMatch.awayGoals = 0
        
        # latestMatch.date = datetime.date(2021, month=12, day=30)
        # latestMatch.homeTeam = "Man Utd"
        # latestMatch.awayTeam = "Burnley"
        # latestMatch.homeGoals = 3
        # latestMatch.awayGoals = 1
        
        #_---------------------------
        allMatches = []
        rawMatchesData = None
        firstRun = True
        while (True):
            #is used to check if top of page has been reached
            if rawMatchesData == None: 
                previousTopMatchData = None
            else:
                previousTopMatchData = rawMatchesData[0]

            rawMatchesData = self.loadDataForAllMatches()
            allMatches = self.rawMatchesToMatchObjects(rawMatchesData)
            currentMatch = self.rawMatchToMatchObject([rawMatchesData[2].text,rawMatchesData[4].text,rawMatchesData[5].text])
            print(f"current match: {currentMatch.date} latestMatch: {latestMatch.date}")
            if firstRun:
                league.newLatestMatch = allMatches[-1]
            if currentMatch.date > latestMatch.date:
                print("here")
                TopMatchData = rawMatchesData[0]
                if (previousTopMatchData == TopMatchData): #has reached the top - meaning all matches must be checked
                    break
                self.scrollToTop(TopMatchData)
                time.sleep(1) #wait for matches to load
            else: #currentMatch.date <= latestMatch.date
                i = 2
                while (currentMatch != latestMatch):
                    currentMatch = self.rawMatchToMatchObject([rawMatchesData[i].text,rawMatchesData[i+2].text,rawMatchesData[i+3].text])
                    i += 8
                allMatches = allMatches[allMatches.index(currentMatch)+1::] #removes all older matches than currentMatch 
                                                                            #(as they have already been calculated in an earlier iteration of the program)
                break
        return allMatches

    #loads the data for all matches visible on the page at that time. Only saves the matches that have finished.
    #returns the raw data for these matches
    def loadDataForAllMatches(self):
        matchElements = self.driver.find_elements(By.XPATH,"//*[@class='KAIX8d']/tbody//tr") ##finds all <tr>'s in all matches
        i = 2
        while i <= len(matchElements): #removes all non-finished matches
            if (not "FT" in matchElements[i].text):
                matchElements = matchElements[:i-2:]
                break
            i += 8
        return matchElements      
    
    #scroll to the top of the result page, by finding the first match element (which is the one highest up) and moving to that element.
    #moving to that element will either spawn a new top element, which can be jumped to again, or put the page to the top
    def scrollToTop(self,topElement):
        action = ActionChains(self.driver)
        action.move_to_element(topElement).perform()
        
    #turns a list of raw matches into a list of match objects, and returns the list
    def rawMatchesToMatchObjects(self,rawMatches):
        allMatches = []
        i = 2
        while i <= len(rawMatches):
            print(i)
            match = self.rawMatchToMatchObject([rawMatches[i].text,rawMatches[i+2].text,rawMatches[i+3].text])
            allMatches.append(match)
            i += 8
        return allMatches
    #Turns the data of a raw match into a match object, and returns it
    def rawMatchToMatchObject(self,rawMatchData):
        matchData = []
        
        #data (date and state of match)
        for data in rawMatchData:
            data = data.strip()
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