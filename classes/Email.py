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
        message = EmailMessage()
        mailBody = "The feriekasse has been created and the teams picked by each player is visible in the attached excel file (.xlsx)."
        subject = f"feriekassen, {const.FERIEKASSE_NAME}, has been created"
        
        self.setupMailInfo(message,self.sender,self.receivers,subject,mailBody)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachExcelFile(message,excelFile,filename)
        
        self.connectToSmtpAndSendMail(message)
        
    def sendPeriodicMail(self):
        message = EmailMessage()
        mailBody = f"Attached is an excel file (.xlsx) with the current standings of the feriekasse."
        #tilføj evt. extra til mailBody
        subject = f"feriekassen, {const.FERIEKASSE_NAME}, has been updated"
        self.setupMailInfo(message,self.sender,self.receivers,subject,mailBody)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachExcelFile(message,excelFile,filename)
        
        self.connectToSmtpAndSendMail(message)
        
    def setupMailInfo(self,message,sender,receivers,subject,body):
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = subject
        message.set_content(body)
    
    def attachExcelFile(self,message,excelFile,newFileName):
        with open(excelFile, 'rb') as f:
            file_data = f.read()
        message.add_attachment(file_data, maintype="application", subtype="xlsx", filename=newFileName)

    def connectToSmtpAndSendMail(self,message):
        smtp = smtplib.SMTP_SSL(self.server)
        smtp.connect(self.server,self.port)
        smtp.login(self.sender,self.password)
        smtp.sendmail(to_addrs=self.receivers,msg=message.as_string(),from_addr=self.sender)
        smtp.quit()

