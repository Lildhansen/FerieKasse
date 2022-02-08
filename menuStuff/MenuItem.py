from Menu import Menu

class MenuItem:
    __undermenu = None
    def __init__(self,title):
        self.title = title
        #self.__undermenu = None
    def Select(self):
        if self.__undermenu != None:
            self.__undermenu.Start()
