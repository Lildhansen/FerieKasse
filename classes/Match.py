import utilities.constants as const

class Match:
    def __init__(self,matchData=[None,None,None,None,None]):
        self.date = matchData[0]
        self.homeTeam = matchData[1]
        self.homeGoals = matchData[2]
        self.awayTeam = matchData[3]
        self.awayGoals = matchData[4]
        self.homeTeamIsPlayerTeam = False
        self.awayTeamIsPlayerTeam = False
        self.homeTeamIsWinner = None #will remain none if it is a draw
        self.draw = False
        self.points = 0
    #calculate points for match and saves it in the points property
    def calculatePoints(self):
        self.setupPointCalculation()
        self.points = self.calculate()
    #set the bools for point calculation
    def setupPointCalculation(self):
        if self.homeGoals > self.awayGoals:
            self.homeTeamIsWinner = True
        elif self.homeGoals < self.awayGoals:
            self.homeTeamIsWinner = False
        else:
            self.draw = True
    #calculate the points and return them    
    def calculate(self):
        if not self.draw:
            #if the player team won
            if (not self.homeTeamIsWinner and self.awayTeamIsPlayerTeam) or (self.homeTeamIsWinner and self.homeTeamIsPlayerTeam):
                return 0
            return self.calculateLoss()
        #draw
        else:
            return const.DRAW_POINTS
    #calculates the points for a loss
    def calculateLoss(self):
        return const.LOSE_POINTS + abs(self.awayGoals - self.homeGoals) * const.POINTS_PER_GOAL            
       
        
    def __eq__(self, other):
        return self.date == other.date and self.homeTeam == other.homeTeam

