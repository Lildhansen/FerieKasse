"""
used for the body of the Email

"""

from abc import abstractmethod
import copy
from random import shuffle
from random import getrandbits
from random import choice

import utilities.util as util
from Excel import Excel

excel = Excel()

class ExtraBodyPickers:
    def __init__(self,leadingExtraBodyPicker,trailingExtraBodyPicker,losingExtraBodyPicker,highestScoreTeamExtraBodyPicker,lowestScoreTeamExtraBodyPicker):
        self.leadingExtraBodyPicker = leadingExtraBodyPicker
        self.trailingExtraBodyPicker = trailingExtraBodyPicker
        self.losingExtraBodyPicker = losingExtraBodyPicker
        self.highestScoreTeamExtraBodyPicker = highestScoreTeamExtraBodyPicker
        self.lowestScoreTeamExtraBodyPicker = lowestScoreTeamExtraBodyPicker
        self.allExtraBodyPickers = [self.leadingExtraBodyPicker,self.trailingExtraBodyPicker,self.losingExtraBodyPicker,self.highestScoreTeamExtraBodyPicker,self.lowestScoreTeamExtraBodyPicker] 
        
#abstract class
class ExtraBodyPicker:
    @abstractmethod
    def condition(self):
        pass
    @abstractmethod
    def getText(self):
        pass

#almost there! player2 leads player1 by just 30 points 
#So close! player1 is behind player2 by a mere 30 points
class TrailingExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.leadingPlayerFirstComparisons = []
        self.trailingPlayerFirstComparisons = []
        self.pointDescriptions = []
        self.pointDifference = None
        self.leadingPlayerName = None
        self.trailingPlayerName = None
    def condition(self,players):
        if len(players) == 1:
            return False
        shuffle(players)
        for player in players:
            player.totalPoints = excel.getPlayerScoreFromExcelFile(player).totalPoints #dont understand how this is not pass by reference
        players.sort(key=lambda player: player.totalPoints, reverse=True) #big -> small
        previousPlayer = None
        for player in players:
            previousPlayer = copy.deepcopy(player)
            if previousPlayer == None:
                continue
            #value used to make the threshold scale by number of points they have rather than by a constant
            deltaThreshold = (player.totalPoints + previousPlayer.totalPoints) / 20 #divided by 2 (since there are 2 teams) and then by 10
            pointDifference = abs(player.totalPoints - previousPlayer.totalPoints)
            if pointDifference <= deltaThreshold:
                self.pointDifference = pointDifference
                self.leadingPlayerName = previousPlayer.name
                self.trailingPlayerName = player.name
                return True
        return False
    def getText(self):
        trailingPlayerFirst = getrandbits(1) #getting a random bit (0 or 1) (faster than getting a bool)
        firstPlayerName = self.trailingPlayerName if trailingPlayerFirst else self.leadingPlayerName
        secondPlayerName = self.leadingPlayerName if trailingPlayerFirst else self.trailingPlayerName
        initialExpression = choice(self.initialExpressions)
        comparison = choice(self.trailingPlayerFirstComparisons) if trailingPlayerFirst else choice(self.leadingPlayerFirstComparisons)
        pointDescription = choice(self.pointDescriptions)
        return f"{initialExpression} {firstPlayerName} {comparison} {secondPlayerName} {pointDescription} {self.pointDifference} points"

#Oh no! player2 is in the last place at a whopping 560 points
class LosingExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.positionDescriptions = []
        self.pointDescriptions = []
        self.mostPointsPlayerName = None
        self.playerPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self):
        initialExpression = choice(self.initialExpressions)
        positionDescription = choice(self.positionDescriptions)
        pointDescription = choice(self.pointDescriptions)
        return f"{initialExpression} {self.mostPointsPlayerName} {positionDescription} {pointDescription} {self.playerPoints} points"
    def getPlayerInformation(self,players):
        for player in players:
            player.totalPoints = excel.getPlayerScoreFromExcelFile(player).totalPoints #dont understand how this is not pass by reference
        players.sort(key=lambda player: player.totalPoints, reverse=True) #big -> small
        mostPointsPlayer = players[0]
        self.mostPointsPlayerName = mostPointsPlayer.name
        self.playerPoints = mostPointsPlayer.totalPoints

#Holy Cow! player1 is in the lead with just 165 points
class LeadingExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.positionDescriptions = []
        self.pointDescriptions = []
        self.leastPointsPlayerName = None
        self.playerPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self):
        initialExpression = choice(self.initialExpressions)
        positionDescription = choice(self.positionDescriptions)
        pointDescription = choice(self.pointDescriptions)
        return f"{initialExpression} {self.leastPointsPlayerName} {positionDescription} {pointDescription} {self.playerPoints} points"
    def getPlayerInformation(self,players):
        for player in players:
            player.totalPoints = excel.getPlayerScoreFromExcelFile(player).totalPoints #dont understand how this is not pass by reference
        players.sort(key=lambda player: player.totalPoints) #small -> big
        leastPointsPlayer = players[0]
        self.leastPointsPlayerName = leastPointsPlayer.name
        self.playerPoints = leastPointsPlayer.totalPoints
                               
#Oh no! player1's FCK has the most points of all teams with 200 points         
class HighestScoreTeamExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.pointDescriptions = []
        self.mostPointsTeamName = None
        self.mostPointsTeamPlayerName = None
        self.teamPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self):
        initialExpression = choice(self.initialExpressions)
        pointDescription = choice(self.pointDescriptions)
        return f"{initialExpression} {self.mostPointsTeamPlayerName}'s team, {self.mostPointsTeamName}, {pointDescription} {self.teamPoints} points"
    def getPlayerInformation(self,players):
        mostPointsTeam = excel.getHighestScoreTeam()
        self.mostPointsTeamName = mostPointsTeam.name
        self.teamPoints = mostPointsTeam.points
        self.mostPointsTeamPlayerName = util.getPlayerThatHasTeam(self.mostPointsTeamName,players).name
     
#Nice one! player1's Liverpool has the least points of all teams with 35 points
class LowestScoreTeamExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.pointDescriptions = []
        self.leastPointsTeamName = None
        self.leastPointsTeamPlayerName = None
        self.teamPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self):
        initialExpression = choice(self.initialExpressions)
        pointDescription = choice(self.pointDescriptions)
        return f"{initialExpression} {self.leastPointsTeamPlayerName}'s team, {self.leastPointsTeamName}, {pointDescription} {self.teamPoints} points"
    def getPlayerInformation(self,players):
        leastPointsTeam = excel.getLowestScoreTeam()
        self.leastPointsTeamName = leastPointsTeam.name
        self.teamPoints = leastPointsTeam.points
        self.leastPointsTeamPlayerName = util.getPlayerThatHasTeam(self.leastPointsTeamName,players).name

englishPositiveInitialExpressions = ["Nice one!","Damn!","Very good,"]
englishNegativeInitialExpressions = ["Oh no!","Damn!","How unfortunate,"]

englishTrailingExtraBody = TrailingExtraBodyPicker()
englishTrailingExtraBody.initialExpressions = ["So close!","Almost There!","Come on!","Nearly there!","Oh my!"]
englishTrailingExtraBody.leadingPlayerFirstComparisons = ["has a lead on","leads","only leads","has a small lead on","currently leads","is just ahead of"]
englishTrailingExtraBody.trailingPlayerFirstComparisons = ["is behind","is just behind","is only behind","trails","trails by a hair on","is after","is at the heel of"]
englishTrailingExtraBody.pointDescriptions = ["by a mere","by merely","by just","with merely","with a mere","with just","by nothing more than","with nothing more than"] 

englishLosingExtraBodyPicker = LosingExtraBodyPicker()
englishLosingExtraBodyPicker.initialExpressions = englishNegativeInitialExpressions
englishLosingExtraBodyPicker.positionDescriptions = ["is in the last place","is last","has the most points"]
englishLosingExtraBodyPicker.pointDescriptions = ["at a whopping","with","with a total of","with a whopping"]

englishLeadingExtraBodyPicker = LeadingExtraBodyPicker()
englishLeadingExtraBodyPicker.initialExpressions = englishPositiveInitialExpressions
englishLeadingExtraBodyPicker.positionDescriptions = ["is in the first place","is first","has the least points"]
englishLeadingExtraBodyPicker.pointDescriptions = ["at only","at","with","with a total of","with just"]

englishLowestScoreTeamExtraBodyPicker = LowestScoreTeamExtraBodyPicker()
englishLowestScoreTeamExtraBodyPicker.initialExpressions = englishPositiveInitialExpressions
englishLowestScoreTeamExtraBodyPicker.pointDescriptions = ["has the least points with","has the least points of all teams with","has scored the least total points with","is the best team so far with"]

englishHighestScoreTeamExtraBodyPicker = HighestScoreTeamExtraBodyPicker()
englishHighestScoreTeamExtraBodyPicker.initialExpressions = englishNegativeInitialExpressions
englishHighestScoreTeamExtraBodyPicker.pointDescriptions = ["has the most points with","has the most points of all teams with","has scored the most total points with","is the worst team so far with"]

englishExtraBodyPickers = ExtraBodyPickers(englishTrailingExtraBody,englishLosingExtraBodyPicker,englishLeadingExtraBodyPicker,englishLowestScoreTeamExtraBodyPicker,englishHighestScoreTeamExtraBodyPicker)