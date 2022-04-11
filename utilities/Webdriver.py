#libraries - standard or pip
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    def getMatchesAfterDateAndMatch(self,date,teams):
        time.sleep(1)
        x = self.driver.find_elements(By.XPATH,"//*[@class='KAIX8d']/tbody//tr") ##finds all <tr>'s in that the match
            
            
        for y in range(len(x)):
            if (y % 8 == 2): #the date and match status
                if (not "FT" in x[y].text):
                    break
                print("date: ",x[y].text,"\n")
            elif (y % 8 == 4): #homegoals and hometeam
                print("team1: ",x[y].text,"\n")
            elif (y % 8 == 5): #awaygoals and awayteam
                print("team2: ",x[y].text,"\n")
                
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