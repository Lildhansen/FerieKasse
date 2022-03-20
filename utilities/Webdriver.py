#libraries - standard or pip
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



class Webdriver:
    def __init__(self):
        self.setupDriver()
        self.driver = webdriver.Chrome(options=self.__options) #service=self.__service,
    #sets up services and options for the webdriver
    def setupDriver(self):
        self.__service = Service("./chromedriver.exe")
        self.__options = Options()
        self.__options.headless = True
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
    #closes the webdriver
    def showAllMatches(self):
        while True:
            time.sleep(2)
            showMoreButton = self.driver.find_element_by_css_selector("#live-table > div.event.event--results > div > div > a")
            print(showMoreButton)
            #den skal se om den kan finde den fucking knap
            #if showMoreButton
        
    def quit(self):
        self.driver.quit()

