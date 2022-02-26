#libraries - standard or pip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#own modules
from classes.Team import Team
from classes.Player import Player
import utilities.util as util

service = Service("./chromedriver.exe")
options = Options()
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service,options=options)
driver.close


    
def UpdateFerieKasse():
    pass



