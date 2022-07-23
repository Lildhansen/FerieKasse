import smtplib
import configparser
import os

from datetime import date 
import utilities.constants as const
  
class Email:
    def __init__(self):
        self.sender = None
        self.password = None
        self.server = None
        self.port = None
        self.receivers = []
        self.setupEmailInformationFromConfigFile()
    def setupEmailInformationFromConfigFile(self):
        configSection = "email_config"
        config = configparser.ConfigParser()
        config.read(os.path.join(fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx", (os.path.join(os.path.dirname(os.path.dirname(__file__)),'Email.ini'))))
        self.sender = config.get(configSection,'sender')
        self.password = config.get(configSection,'password')
        self.server = config.get(configSection,'server')
        self.port = int(config.getint(configSection,'port'))
        self.receivers = config.get(configSection,'receivers').split(';')
        
a = Email()


