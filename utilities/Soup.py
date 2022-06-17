#libraries - standard or pip
import datetime
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

#mangler check for om kampen er i gang

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
        self.res = requests.get(link)
        self.res.raise_for_status()
        self.soup = bs4.BeautifulSoup(self.res.text,features="lxml")
    #takes the latest match that has been processed as input, and get all matches in that specific league between that match+1 and the last played match
    def getMatchesAfterLatestMatch(self,latestMatch,league):
        allMatches = []
        for rawMatch in self.soup.findAll('tr'):
            if len(rawMatch.text) == 0 or rawMatch.text == None:
                continue
            if not rawMatch.text[0].isdigit(): 
                continue
            #then it is indeed a match
            currentMatch = self.rawMatchToMatchObject(rawMatch)
            
            allMatches.append(currentMatch)
    
        
        
        
        
        
        
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
            if firstRun:
                league.newLatestMatch = allMatches[-1]
            if currentMatch.date > latestMatch.date:
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
            # if info.get('data-stat') == "time": #kan eventuel bruges hvis der er en igangværende kamp (tjek om klokken er 2 timer + tidspunktet) 
            #kunne også gemmes sammen med dato for også at sammenligne tidspunkt
        return match