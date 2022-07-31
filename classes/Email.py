import smtplib
import configparser
import os
import ssl
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

from datetime import date 
import utilities.constants as const
  
class Email:
    def __init__(self,emailIniFile):
        self.sender = None
        self.password = None
        self.server = None
        self.port = None
        self.receivers = []
        self.setupEmailInformationFromConfigFile(emailIniFile)
    def setupEmailInformationFromConfigFile(self,emailIniFile):
        configSection = "email_config"
        config = configparser.ConfigParser()
        config.read(emailIniFile)
        self.sender = config.get(configSection,'sender')
        self.password = config.get(configSection,'password')
        self.server = config.get(configSection,'server')
        self.port = int(config.getint(configSection,'port'))
        self.receivers = config.get(configSection,'receivers').split(';')
    def sendInitialEmail(self):
        mailBody = "The feriekasse has been created and the teams picked by each player is visible in the attached excel file (.xlsx)."
        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = self.receivers
        message['Subject'] = f"feriekassen, {const.FERIEKASSE_NAME}, has been created"
        #add body
        message.set_content(mailBody)
        
        #attach the excel file
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        with open(excelFile, 'rb') as f:
            file_data = f.read()
        message.add_attachment(file_data, maintype="application", subtype="xlsx", filename=filename)
        
        #connect and send mail
        smtp = smtplib.SMTP_SSL(self.server)
        smtp.connect(self.server,self.port)
        smtp.login(self.sender,self.password)
        smtp.sendmail(to_addrs=self.receivers,msg=message.as_string(),from_addr=self.sender)
        smtp.quit()
    def sendMail(self):
        mailBody = f"Attached is an excel file (.xlsx) with the current standings of the feriekasse."


