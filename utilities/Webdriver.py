#libraries - standard or pip
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


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
    def goToUrl(self,url):
        self.driver.get(url)
    #accepts cookies when using the selenium webdriver - not sure if it is neccessary
    #on slower machines this might require time.sleep() - for some time (not more than half a second - otherwise it is slow af)
    def acceptCookies(self):
        try:
            self.driver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
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
    def getMatchesAfterDateAndMatch(self,date,hometeam,awayTeam):
        #allmatchesRow = self.driver.find_elements_by_css_selector("div.event__match event__match--static event__match--twoLine")
        a = self.driver.find_elements(By.ID,"live-table") #den kan ikke finde mere end denne...
        b = a[0].find_elements(By.CSS_SELECTOR,"div.event__match event__match--static event__match--twoLine")
        print(len(b))
        #print(len(allmatchesRow))
    #closes the webdriver
    def quit(self):
        self.driver.quit()

