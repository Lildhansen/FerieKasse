
class Player:
    def __init__(self,name):
        self.name = name
        self.teams = []
        self.matches = []
        self.points = []
        self.totalPoints = 0 #used for Email
        self.availableLeagues = [] #used for menu
        self.pickedLeagues = [] #used for menu
    def __eq__(self, other):
        if other == None:
            return False
        return self.name == other.name


