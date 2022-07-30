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
        mail_body = f"Attached is an excel file (.xlsx) with the current standings of the feriekasse."
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receivers
        message['Subject'] = f"feriekassen, {const.FERIEKASSE_NAME}, has been created"
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx"
        #add body
        message.attach(MIMEText(mail_body))
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(excelFile, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=excelFile')
        message.attach(part)
        
        
        # #attach the excel file
        # excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        # with open(excelFile, 'rb') as f:
        #     file_data = f.read()
        # message.add_attachment(file_data, maintype="application", subtype="xlsx", filename=excelFile) #this doesnt work
        #establish connection
        
        context = ssl.create_default_context()
        
        print("0")
        smtp = smtplib.SMTP_SSL(self.server, self.port,context=context)
        print("2")
        smtp.ehlo()
        smtp.login(self.sender,self.password)
        print("3")
        smtp.sendmail(message)
        print("4")
        smtp.quit()
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(self.server, self.port) as session:
        #     session.ehlo()
        #     #session.starttls() #enable security
        #     session.login(self.sender, self.password)
        #     #send mail
        #     session.send(message)
        #     print("initial mail has been sent")

#turn off LESS SECURE APPS to make this work on your gmail


