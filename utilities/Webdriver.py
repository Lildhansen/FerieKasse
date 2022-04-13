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
    def getMatchesAfterDateAndMatch(self,date,homeTeam,awayTeam,league):
        
        time.sleep(1)
        # for testin ----------
        date = datetime.date(2022, 1, 23)
        homeTeam = "Crystal Palace"
        awayTeam = "Liverpool"
        #_---------------------------
        #check date for first match - if date is earlier than date of the match, more matches needs to be loaded in.
        doWhileFlag = True
        allMatches = []
        currentMatch = Match()
        rawMatchesData = None
        
        #gets the first match
        while (doWhileFlag or util.compareDates(currentMatch.date,date)):
            doWhileFlag = False
            #used to check if top has been reached
            if rawMatchesData == None: 
                previousTopMatchData = None
            else:
                previousTopMatchData = rawMatchesData[0]
            rawMatchesData = self.loadDataForAllMatches()
            print("(",rawMatchesData[2].text,") (",rawMatchesData[4].text,") (",rawMatchesData[5].text,")")
            currentMatch = self.rawMatchToMatchObject([rawMatchesData[2].text,rawMatchesData[4].text,rawMatchesData[5].text])
            print("currentmatch date: ",currentMatch.date)
            print("date: ",date)
            if currentMatch.date == date: 
                i = 2
                while (currentMatch.homeTeam != homeTeam and currentMatch.awayTeam != awayTeam):
                    currentMatch = self.rawMatchToMatchObject([rawMatchesData[i].text,rawMatchesData[i+2].text,rawMatchesData[i+3].text])
                    print(i,currentMatch.homeTeam,currentMatch.awayTeam)
                    i += 8
            else:
                TopMatchData = rawMatchesData[0]
                if (previousTopMatchData == TopMatchData): #has reached the top - meaning all matches must be checked
                    break
                self.scrollToTop(TopMatchData)
                time.sleep(1)
        #rawMatchesData.index()
        #allMatches = rawMatchesData[]
        print("done")
        i = 2
        while i <= len(rawMatchesData):
            if (not "FT" in rawMatchesData[i].text):
                break
            match = self.rawMatchToMatchObject([rawMatchesData[i].text,rawMatchesData[i+2].text,rawMatchesData[i+3].text])
            if (match.date == date):
                pass
                #check the teams
            #else if
            i += 8
    def loadDataForAllMatches(self):
        return self.driver.find_elements(By.XPATH,"//*[@class='KAIX8d']/tbody//tr") ##finds all <tr>'s in all matches
    def scrollToTop(self,topElement):
        action = ActionChains(self.driver)
        action.move_to_element(topElement).perform()
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
            goals = teamAndGoals[0]
            team = teamAndGoals[1]
            matchData.append(team)
            matchData.append(goals)
            i += 1
        return Match(matchData)
        
        
        
         
        #this does not work:
        # finishedMatches = self.driver.find_elements(By.CLASS_NAME,"KAIX8d") #KAIX8d = the box with a match, L5Kkcd = the 2 teams
        # for match in finishedMatches:
            
        #     matchStatus = match.find_elements(By.CLASS_NAME,"BhSGD imspo_mt__ndl-p imso-medium-font imspo_mt__match-status") #FT stuff here
        #     if (len(matchStatus) > 0):
        #         print("match been played: ",matchStatus[0].text)
        #     ms = match.find_elements(By.CLASS_NAME,"imspo_mt__pm-inf imspo_mt__pm-infc imspo_mt__date imso-medium-font") #if match has not been
        #     if (len(ms) > 0):
        #         print("match not been played: ",ms[0].text)
        #allmatchesRow = self.driver.find_elements_by_css_selector("div.event__match event__match--static event__match--twoLine")
        #a = self.driver.find_elements(By.ID,"live-table") #den kan ikke finde mere end denne...
        #b = a[0].find_elements(By.CSS_SELECTOR,"div.event__match event__match--static event__match--twoLine")
        #print(len(b))
        #print(len(allmatchesRow))
    #closes the webdriver
    def quit(self):
        self.driver.quit()