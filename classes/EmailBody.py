"""
used for the body of the Email

"""

from abc import ABCMeta, abstractmethod, abstractproperty
import copy
from random import shuffle
from random import getrandbits
from random import choice

import utilities.util as util


class ExtraBodyPickers:
    def __init__(self):
        self.leadingExtraBodyPicker = None
        self.trailingExtraBodyPicker = None
        self.losingExtraBodyPicker = None
        self.highestScoreTeamExtraBodyPicker = None
        self.lowestScoreTeamExtraBodyPicker = None
        self.allExtraBodyPickers = [self.leadingExtraBodyPicker,self.trailingExtraBodyPicker,self.losingExtraBodyPicker,self.highestScoreTeamExtraBodyPicker,self.lowestScoreTeamExtraBodyPicker] 
        
#abstract class
class ExtraBodyPicker:
    @abstractmethod
    def condition(self):
        pass
    @abstractmethod
    def getText(self):
        pass

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
            util.getPlayerScoreFromExcelFile(player)
        players.sort(key=lambda player: player.totalPoints) #small -> big
        leastPointsPlayer = player[0]
        self.leastPointsPlayerName = leastPointsPlayer.name
        self.playerPoints = leastPointsPlayer.totalPoints
    
#Oh no! player2 is in the last place at a whopping 560 points
#Oh no! = initial expression
#mostPointsPlayer
#is in the last place = positionDescription
#at a whopping = pointsDescription
#points
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
            util.getPlayerScoreFromExcelFile(player)
        players.sort(key=lambda player: player.totalPoints, reverse=True) #big -> small
        mostPointsPlayer = player[0]
        self.mostPointsPlayerName = mostPointsPlayer.name
        self.playerPoints = mostPointsPlayer.totalPoints
#examples
#
#almost there! player2 leads player1 by just 30 points 
#So close! player1 is behind player2 by a mere 30 points
#so close = initial expression
#player 1 = trailing player
#is behind = comparison
#by a mere = pointDescription (in lack of better word)
#30 = pointDifference
#player1Points
#player2Points
#trailingPlayerFirst (true or false) (altså både a er foran b    og    b er bagved a)
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
        shuffle(players)
        for player in players:
            util.getPlayerScoreFromExcelFile(player) #should be made ----------------
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
        return f"{initialExpression} {self.mostPointsPlayerName}'s team, {self.mostPointsTeamName}, {pointDescription} {self.playerPoints} points"
    def getPlayerInformation(self,players):
        mostPointsTeam = util.getHighestScoreTeam()
        self.mostPointsTeamName = mostPointsTeam.name
        self.teamPoints = mostPointsTeam.points
        self.mostPointsTeamPlayerName = util.getPlayerThatHasTeam(self.mostPointsTeamName,players)
    
    
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
        return f"{initialExpression} {self.leastPointsPlayerName}'s team, {self.leastPointsTeamName}, {pointDescription} {self.playerPoints} points"
    def getPlayerInformation(self,players):
        leastPointsTeam = util.getHighestScoreTeam()
        self.leastPointsTeamName = leastPointsTeam.name
        self.teamPoints = leastPointsTeam.points
        self.leastPointsTeamPlayerName = util.getPlayerThatHasTeam(self.leastPointsTeamName,players)

        

#shoudl be called englishExtraBodyPickers
extraBodyPickers = ExtraBodyPickers()

positiveInitialExpressions = ["Nice one!","Damn!","Very good,"]
negativeInitialExpressions = ["Oh no!","Damn!","How unfortunate,"]

trailingExtraBody = TrailingExtraBodyPicker()
trailingExtraBody.initialExpressions = ["So close!","Almost There!","Come on!","Nearly there!","Oh my!"]
trailingExtraBody.leadingPlayerFirstComparisons = ["has a lead on","leads","only leads","has a small lead on","currently leads","is just ahead of"]
trailingExtraBody.trailingPlayerFirstComparisons = ["is behind","is just behind","is only behind","trails","trails by a hair on","is after","is at the heel of"]
trailingExtraBody.pointDescriptions = ["by a mere","by merely","by just","with merely","with a mere","with just","by nothing more than","with nothing more than"] 
extraBodyPickers.trailingExtraBodyPicker = trailingExtraBody

losingExtraBodyPicker = LosingExtraBodyPicker()
losingExtraBodyPicker.initialExpressions = negativeInitialExpressions
losingExtraBodyPicker.positionDescriptions = ["is in the last place","is last","has the most points"]
losingExtraBodyPicker.pointDescriptions = ["at a whopping","with","with a total of","with a whopping"]
extraBodyPickers.losingExtraBodyPicker = losingExtraBodyPicker

leadingExtraBodyPicker = LeadingExtraBodyPicker()
leadingExtraBodyPicker.initialExpressions = positiveInitialExpressions
leadingExtraBodyPicker.positionDescriptions = ["is in the first place","is first","has the least points"]
leadingExtraBodyPicker.pointDescriptions = ["at only","at","with","with a total of","with just"]
extraBodyPickers.leadingExtraBodyPicker = leadingExtraBodyPicker

lowestScoreTeamExtraBodyPicker = LowestScoreTeamExtraBodyPicker()
lowestScoreTeamExtraBodyPicker.initialExpressions = positiveInitialExpressions
lowestScoreTeamExtraBodyPicker.pointDescriptions = ["has the least points with","has the least points of all teams with","has scored the least total points","is the best team so far with"]
extraBodyPickers.lowestScoreTeamExtraBodyPicker = lowestScoreTeamExtraBodyPicker

highestScoreTeamExtraBodyPicker = HighestScoreTeamExtraBodyPicker()
highestScoreTeamExtraBodyPicker.initialExpressions = negativeInitialExpressions
highestScoreTeamExtraBodyPicker.pointDescriptions = ["has the most points with","has the most points of all teams with","has scored the most total points","is the worst team so far with"]
extraBodyPickers.highestScoreTeamExtraBodyPicker = highestScoreTeamExtraBodyPicker
