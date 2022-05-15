class MenuItem:
    __undermenu = None
    def __init__(self,title):
        self.title = title
        self.teams = []
        self.isUnderMenu = False
    def Select(self):
        if self.__undermenu != None:
            self.__undermenu.Start()
