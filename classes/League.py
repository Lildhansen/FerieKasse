#libraries - standard or pip
import codecs
import datetime
import json
from classes.myJsonEncoder import MyJsonEncoder as Encoder
import copy
import os

#own libraries
from classes.Match import Match
from utilities.Soup import Soup
import utilities.constants as const
import utilities.util as util

class League:
    def __init__(self,name,country):
        self.name = name
        self.country = country.lower()
        self.soup = None
        self.teams = []
        self.matches = []
        self.link = None
    #will update "matches" with all matches after date of latest match covered (if any)
    def getMatchesAfterLatestMatch(self,match=Match()):
        if match.date == None:
            if datetime.datetime.now().month > 7: #if we are in the first half of the season we must get all matches from this year till now
                match.date = datetime.date(datetime.datetime.now().year,7,15)
            else: #if we are in the final half of the season, we must get all matches from last year's season start till now
                match.date = datetime.date(datetime.datetime.now().year-1,7,15)
        self.soup = Soup()
        self.soup.getLinkContent(self.link)
        self.matches = self.soup.getMatchesAfterLatestMatch(match)
        self.saveLatestMatchCovered()
        self.filterMatches()

    def getMatchesAfterLatestMatchForSuperliga(self,match=Match()):
        if match.date == None:
            if datetime.datetime.now().month > 7:
                match.date = datetime.date(datetime.datetime.now().year,7,15)
            else:
                match.date = datetime.date(datetime.datetime.now().year-1,7,15)
        self.soup = Soup()
        self.soup.getLinkContent(self.link)
        self.matches = self.soup.getMatchesAfterLatestMatchForSuperliga(match)
        self.saveLatestMatchCovered()
        self.filterMatches()
        

    #saves the latest match covered for each league in a temporary json file (which will later replace the latestMatchCovered file)
    def saveLatestMatchCovered(self):
        if len(self.matches) == 0:
            return
        latestMatch = copy.deepcopy(self.matches[-1])
        latestMatch.date = latestMatch.date.isoformat()
        latestMatchJSON = json.dumps(latestMatch, cls=Encoder)

        # reading
        leaguesAndCountries = {}
        if os.path.exists(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCoveredToUpdate.json"):
            with codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCoveredToUpdate.json", "r") as file:
                leaguesAndCountries = json.load(file)

        # updating
        leaguesAndCountries[f"{self.name},{self.country}"] = latestMatchJSON

        # Writing
        with codecs.open(fr"./data/{const.FERIEKASSE_NAME}/latestMatchCoveredToUpdate.json", "w") as file:
            json.dump(leaguesAndCountries, file)



    #removes the matches that does not involve any of the teams (that is players' teams) in that league,
    def filterMatches(self):
        originalMatchList = self.matches.copy() #creates a copy of the list as to no alter the list mid-loop
        for match in originalMatchList:                  
            TeamInMatch = False            
            for team in self.teams:
                if (match.homeTeam == team.name):
                    match.homeTeamIsPlayerTeam = True
                    TeamInMatch = True
                if (match.awayTeam == team.name):
                    match.awayTeamIsPlayerTeam = True
                    TeamInMatch = True
                continue #needs to go all the way through the list (even if one team is player team) - to make sure we check for if both teams are player teams
            if not TeamInMatch:
                self.matches.remove(match)
    #remove matches, where the losing team is not one of the players' teams
    def removeMatchesYielding0Points(self):
        originalMatchList = self.matches.copy() #creates a copy of the list as to no alter the list mid-loop
        for match in originalMatchList:
            if (not match.draw):
                #if (match.homeTeamIsWinner and not match.awayTeamIsPlayerTeam) or (not match.homeTeamIsWinner and not match.homeTeamIsPlayerTeam):
                if match.points == 0 and match.bonusPoints == 0:
                    self.matches.remove(match)           
    #calculates the points for all matches and saves the points in the match objects
    def calculatePointsForMatches(self):
        for match in self.matches:
            match.calculatePoints()
            self.applyMatchMultipliers(match)
            if const.FOUR_GOAL_WIN_RULE:
                self.applyFourGoalWinBonus(match)
            #nice debugging line if something goes wrong:
            # print(f"{match.homeTeam} {match.homeGoals} - {match.awayGoals} {match.awayTeam} : {match.points} points")
    #apply possible multipliers for the match - if it was an "indbyrdes" match
    def applyMatchMultipliers(self,match):
        if (match.homeTeamIsPlayerTeam and match.awayTeamIsPlayerTeam): #if it is an indbyrdes match
            homeTeam = util.findTeamByTeamName(self.teams,match.homeTeam)
            awayTeam = util.findTeamByTeamName(self.teams,match.awayTeam)
            if homeTeam.playerName == awayTeam.playerName:
                match.points *= 0
            elif self.isSlutspilMatch(match) and match.homeTeamIsWinner:
                return
            else:
                match.points *= const.INDBYRDES_MULTIPLIER
    #returns true if the match is a slutspil match (this is only relevant for superliga matches)
    #Returns false if it is not - also if the league is not the superliga
    def isSlutspilMatch(self,match):
        if self.name.lower() != "superliga":
            return False
        if match.date.month >= 7 and match.date.day > 1: #if we are in the first half of the season the slutspil begins next year (otherwise it is the current year)
            return match.date >= datetime.date(datetime.datetime.now().year+1,4,1)
        return match.date >= datetime.date(datetime.datetime.now().year,4,1)
        
    #calculates the bonus points for the extra rule - that is if a team wins by 4 goals or more
    def applyFourGoalWinBonus(self,match):
        if (match.homeTeamIsWinner and match.homeTeamIsPlayerTeam) and (match.homeGoals - match.awayGoals) >= 4: #home win by 4+ goals
            match.bonusPoints += const.FOUR_GOAL_WIN_BONUS_POINTS
        elif (not match.homeTeamIsWinner and match.awayTeamIsPlayerTeam) and (match.awayGoals - match.homeGoals) >= 4: #away win with 4+ goals
            match.bonusPoints += const.FOUR_GOAL_WIN_BONUS_POINTS
    
           