class Match:
    def __init__(self,matchData):
        self.date = matchData[0]
        self.homeTeam = matchData[1]
        self.homeGoals = matchData[2]
        self.awayTeam = matchData[3]
        self.awayGoals = matchData[4]
    #should add more attributes

#match skal beregnes og i player skal vi derefter - måske - gange med 0 eller 2. not sure hvor vi ganger med 2 henne - burde nok gøres i
#main_update
