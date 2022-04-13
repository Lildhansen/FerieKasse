from datetime import date


class Match:
    def __init__(self,matchData=[None,None,None,None,None]):
        self.date = matchData[0]
        self.homeTeam = matchData[1]
        self.homeGoals = matchData[2]
        self.awayTeam = matchData[3]
        self.awayGoals = matchData[4]
        self.homeTeamIsPlayerTeam = False
        self.awayTeamIsPlayerTeam = False
        self.homeTeamIsWinner = None
        self.points = 0
    #calculate points for match and saves it in the points property
    def calculatePoints(self):
        pass
    def __eq__(self, other):
        return self.date == other.date and self.homeTeam == other.homeTeam
            
    #should add more attributes

#match skal beregnes og i player skal vi derefter - måske - gange med 0 eller 2. not sure hvor vi ganger med 2 henne - burde nok gøres i
#main_update
