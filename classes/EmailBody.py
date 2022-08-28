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
    def __init__(self,leadingExtraBodyPicker,trailingExtraBodyPicker,losingExtraBodyPicker,highestScoreTeamExtraBodyPicker,lowestScoreTeamExtraBodyPicker,emptyExtraBodyPicker):
        self.leadingExtraBodyPicker = leadingExtraBodyPicker
        self.trailingExtraBodyPicker = trailingExtraBodyPicker
        self.losingExtraBodyPicker = losingExtraBodyPicker
        self.highestScoreTeamExtraBodyPicker = highestScoreTeamExtraBodyPicker
        self.lowestScoreTeamExtraBodyPicker = lowestScoreTeamExtraBodyPicker
        self.emptyExtraBodyPicker = emptyExtraBodyPicker
        self.allExtraBodyPickers = [self.leadingExtraBodyPicker,self.trailingExtraBodyPicker,self.losingExtraBodyPicker,self.highestScoreTeamExtraBodyPicker,self.lowestScoreTeamExtraBodyPicker,self.emptyExtraBodyPicker] 
        
#abstract class
class ExtraBodyPicker:
    @abstractmethod
    def condition(self):
        pass
    @abstractmethod
    def getText(self,language):
        pass

#almost there! player2 leads player1 by just 30 points 
#So close! player1 is behind player2 by a mere 30 points

#Nøj hvor tæt! Player 2 fører over player1 med kun 30 point
#Ej hvor tæt på! Player1 er kun 30 point bag player2
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
            if previousPlayer == None:
                continue
            previousPlayer = copy.deepcopy(player)
            #value used to make the threshold scale by number of points they have rather than by a constant
            deltaThreshold = (player.totalPoints + previousPlayer.totalPoints) / 20 #divided by 2 (since there are 2 teams) and then by 10
            pointDifference = abs(player.totalPoints - previousPlayer.totalPoints)
            if pointDifference <= deltaThreshold:
                self.pointDifference = pointDifference
                self.leadingPlayerName = previousPlayer.name
                self.trailingPlayerName = player.name
                return True
        return False
    def getText(self,language):
        trailingPlayerFirst = getrandbits(1) #getting a random bit (0 or 1) (faster than getting a bool)
        firstPlayerName = self.trailingPlayerName if trailingPlayerFirst else self.leadingPlayerName
        secondPlayerName = self.leadingPlayerName if trailingPlayerFirst else self.trailingPlayerName
        initialExpression = choice(self.initialExpressions)
        comparison = choice(self.trailingPlayerFirstComparisons) if trailingPlayerFirst else choice(self.leadingPlayerFirstComparisons)
        pointDescription = choice(self.pointDescriptions)
        if language.lower() == "english":
            return f"{initialExpression} {firstPlayerName} {comparison} {secondPlayerName} {pointDescription} {self.pointDifference} points"
        #danish
        if trailingPlayerFirst:
            return f"{initialExpression} {firstPlayerName} er {pointDescription} {self.pointDifference} point {comparison} {secondPlayerName}"
        return f"{initialExpression} {firstPlayerName} {comparison} {secondPlayerName} med {pointDescription} {self.pointDifference} point"
            
#Oh no! player2 is in the last place at a whopping 560 points
#Åh nej! player2 ligger på sidste pladsen med hele 560 point
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
    def getText(self,language):
        initialExpression = choice(self.initialExpressions)
        positionDescription = choice(self.positionDescriptions)
        pointDescription = choice(self.pointDescriptions)
        if language.lower() == "english":
            return f"{initialExpression} {self.mostPointsPlayerName} {positionDescription} {pointDescription} {self.playerPoints} points"
        return f"{initialExpression} {self.mostPointsPlayerName} {positionDescription} med {pointDescription} {self.playerPoints} point"
    def getPlayerInformation(self,players):
        for player in players:
            player.totalPoints = excel.getPlayerScoreFromExcelFile(player).totalPoints #dont understand how this is not pass by reference
        players.sort(key=lambda player: player.totalPoints, reverse=True) #big -> small
        mostPointsPlayer = players[0]
        self.mostPointsPlayerName = mostPointsPlayer.name
        self.playerPoints = mostPointsPlayer.totalPoints

#Holy Cow! player1 is in the lead with just 165 points
#Hold da op! player1 er på første pladsen med kun 165 point
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
    def getText(self,language):
        initialExpression = choice(self.initialExpressions)
        positionDescription = choice(self.positionDescriptions)
        pointDescription = choice(self.pointDescriptions)
        if language.lower == "english":
            return f"{initialExpression} {self.leastPointsPlayerName} {positionDescription} {pointDescription} {self.playerPoints} points"
        return f"{initialExpression} {self.leastPointsPlayerName} {positionDescription} med {pointDescription} {self.playerPoints} point"
    def getPlayerInformation(self,players):
        for player in players:
            player.totalPoints = excel.getPlayerScoreFromExcelFile(player).totalPoints #dont understand how this is not pass by reference
        players.sort(key=lambda player: player.totalPoints) #small -> big
        leastPointsPlayer = players[0]
        self.leastPointsPlayerName = leastPointsPlayer.name
        self.playerPoints = leastPointsPlayer.totalPoints
                               
#Oh no! player1's FCK has the most points of all teams with 200 points
#For dælen! player1s FCK har med 200 point mest point af alle hold
class HighestScoreTeamExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.pointDescriptions = []
        self.pointComparisons = []
        self.mostPointsTeamName = None
        self.mostPointsTeamPlayerName = None
        self.teamPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self,language):
        initialExpression = choice(self.initialExpressions)
        pointDescription = choice(self.pointDescriptions)
        if language.lower() == "english":
            return f"{initialExpression} {self.mostPointsTeamPlayerName}'s team, {self.mostPointsTeamName}, {pointDescription} {self.teamPoints} points"
        pointComparison = choice(self.pointComparisons)
        return f"{initialExpression} {self.mostPointsTeamPlayerName}s hold, {self.mostPointsTeamName}, har med {pointDescription} {self.teamPoints} point {pointComparison}"
    def getPlayerInformation(self,players):
        mostPointsTeam = excel.getHighestScoreTeam()
        self.mostPointsTeamName = mostPointsTeam.name
        self.teamPoints = mostPointsTeam.points
        self.mostPointsTeamPlayerName = util.getPlayerThatHasTeam(self.mostPointsTeamName,players).name
     
#Nice one! player1's Liverpool has the least points of all teams with 35 points
#Sådan! player1s liverpool har med 35 point fået færrest point af alle hold
class LowestScoreTeamExtraBodyPicker(ExtraBodyPicker):
    def __init__(self):
        self.initialExpressions = []
        self.pointDescriptions = []
        self.pointComparisons = []
        self.leastPointsTeamName = None
        self.leastPointsTeamPlayerName = None
        self.teamPoints = None
    def condition(self,players):
        self.getPlayerInformation(players)
        return True
    def getText(self,language):
        initialExpression = choice(self.initialExpressions)
        pointDescription = choice(self.pointDescriptions)
        if language.lower() == "english":
            return f"{initialExpression} {self.leastPointsTeamPlayerName}'s team, {self.leastPointsTeamName}, {pointDescription} {self.teamPoints} points"
        pointComparison = choice(self.pointComparisons) #this is empty somehow?
        return f"{initialExpression} {self.leastPointsTeamPlayerName}s hold, {self.leastPointsTeamName}, har med {pointDescription} {self.teamPoints} point {pointComparison}"
    def getPlayerInformation(self,players):
        leastPointsTeam = excel.getLowestScoreTeam()
        self.leastPointsTeamName = leastPointsTeam.name
        self.teamPoints = leastPointsTeam.points
        self.leastPointsTeamPlayerName = util.getPlayerThatHasTeam(self.leastPointsTeamName,players).name

#tied for the most points with player1 and player2

class EmptyExtraBodyPicker(ExtraBodyPicker):
    def condition(self,players):
        return True
    def getText(self,language):
        return ""

emptyExtraBodyPicker = EmptyExtraBodyPicker()

#english

englishInitialSubject = "The feriekasse has been created"
englishInitialEmailBody = "The feriekasse has been created and the teams picked by each player is visible in the attached excel file (.xlsx)."


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

englishExtraBodyPickers = ExtraBodyPickers(englishTrailingExtraBody,englishLosingExtraBodyPicker,englishLeadingExtraBodyPicker,englishLowestScoreTeamExtraBodyPicker,englishHighestScoreTeamExtraBodyPicker,emptyExtraBodyPicker)

#danish
danishInitialSubject = "feriekassen er blevet oprettet"
danishInitialEmailBody = "feriekassen er blevet oprettet og holdene er blevet valgt for hver spiller og er synlig i den vedhæftede excel fil (.xlsx)."
danishLowPointDescriptions = ["kun","kun lige","egentlig kun","sådan set kun",""]
danishHighPointDescriptions = ["hele","noget så meget som","","intet mindre end","sådan set intet mindre end"]
                        
danishPositiveInitialExpressions = ["Flot klaret!","Hold da op","Wow!","Sådan!","Godt klaret!","Hold nu op!"]
danishNegativeInitialExpressions = ["Åh nej!","For dælen da!","Hvor ærgeligt!","For dælen!"]

danishTrailingExtraBody = TrailingExtraBodyPicker()
danishTrailingExtraBody.initialExpressions = ["Så tæt på","Nøj hvor tæt!","Ej hvor tæt på!","Kom nu!","Næsten!","Hold da op!"]
danishTrailingExtraBody.leadingPlayerFirstComparisons = ["fører over","er foran","har en lille føring over","er et hår foran","er kun lige foran","er med en lille føring foran"]
danishTrailingExtraBody.trailingPlayerFirstComparisons = ["bag","bagved","efter"]
danishTrailingExtraBody.pointDescriptions = danishLowPointDescriptions

danishLosingExtraBodyPicker = LosingExtraBodyPicker()
danishLosingExtraBodyPicker.initialExpressions = danishNegativeInitialExpressions
danishLosingExtraBodyPicker.positionDescriptions = ["ligger sidst","er sidst","har flest point","ligger på sidste pladsen"]
danishLosingExtraBodyPicker.pointDescriptions = danishHighPointDescriptions

danishLeadingExtraBodyPicker = LeadingExtraBodyPicker()
danishLeadingExtraBodyPicker.initialExpressions = danishPositiveInitialExpressions
danishLeadingExtraBodyPicker.positionDescriptions = ["fører","er først","er på første pladsen","ligger først","ligger på første pladsen","har færrest point","er bedst"]
danishLeadingExtraBodyPicker.pointDescriptions = danishLowPointDescriptions

danishLowestScoreTeamExtraBodyPicker = LowestScoreTeamExtraBodyPicker()
danishLowestScoreTeamExtraBodyPicker.initialExpressions = danishPositiveInitialExpressions
danishLowestScoreTeamExtraBodyPicker.pointDescriptions = danishLowPointDescriptions
danishLowestScoreTeamExtraBodyPicker.pointComparisons = ["færrest point","fået færrest point af alle hold","færrest point af alle hold","fået færrest point","scoret færrest point","scoret færrest point af alle hold"]

danishHighestScoreTeamExtraBodyPicker = HighestScoreTeamExtraBodyPicker()
danishHighestScoreTeamExtraBodyPicker.initialExpressions = danishNegativeInitialExpressions
danishHighestScoreTeamExtraBodyPicker.pointDescriptions = danishHighPointDescriptions
danishHighestScoreTeamExtraBodyPicker.pointComparisons = ["flest point","fået flest point af alle hold","flest point af alle hold","fået flest point","scoret flest point","scoret flest point af alle hold"]


danishExtraBodyPickers = ExtraBodyPickers(danishTrailingExtraBody,danishLosingExtraBodyPicker,danishLeadingExtraBodyPicker,danishLowestScoreTeamExtraBodyPicker,danishHighestScoreTeamExtraBodyPicker,emptyExtraBodyPicker)
