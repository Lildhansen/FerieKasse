from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import Team

service = Service("./chromedriver.exe")
options = Options()
#options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service, options=options)

aTeam = Team.Team("Liverpool","premier-League","england","Mads",driver)
aTeam.getTeamURL()
