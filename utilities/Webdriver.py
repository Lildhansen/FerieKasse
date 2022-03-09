#libraries - standard or pip
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



class Webdriver:
    def __init__(self):
        self.setupDriver()
        self.driver = webdriver.Chrome(service=self.__service,options=self.__options)
    #sets up services and options for the webdriver
    def setupDriver(self):
        self.__service = Service("./chromedriver.exe")
        self.__options = Options()
        self.__options.headless = True
        self.__options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #accepts cookies when using the selenium webdriver - not sure if it is neccessary
    #on slower machines this might require time.sleep() - for some time (not more than half a second - otherwise it is slow af)
    def acceptCookies(self):
        try:
            self.driver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
        except:
            pass
    #closes the webdriver
    def quit(self):
        self.driver.quit()

