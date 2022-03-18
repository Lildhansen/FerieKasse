class League:
    def __init__(self,name,country,url):
        self.name = name
        self.country = country.lower()
        self.teams = []
        self.url = url#getUrl now probably
        #self.webdriver = webdriver