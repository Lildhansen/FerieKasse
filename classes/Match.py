class Match:
    def __init__(self,homeTeam,homeGoals,awayTeam,awayGoals):
        self.homeTeam = homeTeam
        self.homeGoals = homeGoals
        self.awayTeam = awayTeam
        self.awayGoals = awayGoals
    #should add more attributes

class IndbyrdesMatch(Match): ##what is this called in english??
    def __init__(self, homeTeam, homeGoals, awayTeam, awayGoals):
        super().__init__(homeTeam, homeGoals, awayTeam, awayGoals)
##match kunne have en subclass - indbyrdesMatch - som så beregnede på samme måde - men med x2
#på den måde kunne alt beregningen ske i match objekterne    