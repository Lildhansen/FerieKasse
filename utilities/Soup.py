#libraries - standard or pip
import datetime
from datetime import date
import time
from pytest import skip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4, requests

#own libraries
from classes.Match import Match
import utilities.util as util


class Soup:
    def __init__(self):
        self.res = None
        self.soup = None
    #sets up services and options for the soup
    def setupDriver(self):
        self.res = None
        self.soup = None
    #gets the content of the links and saves it in self.soup
    def getLinkContent(self,link):
        time.sleep(2)
        with requests.Session() as req:
            self.res = req.get(link)
            while self.res.status_code == 429:
                #time.sleep(int(self.res.headers["Retry-After"]))
                time.sleep(.5)
                self.res = req.get(link)
            self.res.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.res.text,features="lxml")
    #takes the latest match that has been processed as input, and get all matches in that specific league between that match+1 and the last played match
    def getMatchesAfterLatestMatch(self,latestMatch):
        allMatches = []
        for rawMatch in self.soup.findAll('tr'):
            if len(rawMatch.text) == 0 or rawMatch.text == None:
                continue
            elif not rawMatch.text[0].isdigit(): 
                continue
            #then it is indeed a match
            currentMatch = self.rawMatchToMatchObject(rawMatch)
            if currentMatch.date <= latestMatch.date: #if we have already looked at this match earlier
                continue
            #not sure which one it is, but if it has no score, it is in progress or havent been played (and from there on the rest of the matches are the same)
            elif currentMatch.homeGoals == None or currentMatch.homeGoals == "": 
                break
            elif currentMatch.date == date.today(): #if it is today, we don't check it
                continue
            allMatches.append(currentMatch)
        return allMatches

    #Turns the data of a raw match into a match object, and returns it
    def rawMatchToMatchObject(self,rawMatchData):
        match = Match()
        for info in rawMatchData:
            if info.get('data-stat') == "date":
                match.date = util.textToDate(info.text)
            elif info.get('data-stat') == "squad_a":
                match.homeTeam = info.text
            elif info.get('data-stat') == "squad_b":
                match.awayTeam = info.text
            elif info.get('data-stat') == "score":
                match.homeGoals,match.awayGoals = util.splitAndConvertToInt(info.text,"–")#for some reason this is not a dash (-), but instead – (which is not a dash)
        return match