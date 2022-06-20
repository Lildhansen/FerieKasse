import utilities.constants as const

class Match:
    def __init__(self,date=None,homeTeam=None,homeGoals=None,awayTeam=None,awayGoals=None):
        self.date = date
        self.homeTeam = homeTeam
        self.homeGoals = homeGoals
        self.awayTeam = awayTeam
        self.awayGoals = awayGoals
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
            #if it is not an indbyrdes match
            if not (self.awayTeamIsPlayerTeam and self.homeTeamIsPlayerTeam):
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
        if other == None:
            return False
        return self.date == other.date and self.homeTeam == other.homeTeam


