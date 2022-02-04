class SimpleMenu:
    def __init__(self,players,webDriver):
        self.players = players;
        self.playerCount = len(players)
        self.webDriver = webDriver
    #hent fra resultat.dk