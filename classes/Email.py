from msilib.schema import Condition
import smtplib
import configparser
from email.message import EmailMessage
from random import shuffle


from datetime import date
import utilities.constants as const
import classes.EmailBody as EmailBody
  
class Email:
    def __init__(self,emailIniFile):
        self.sender = None
        self.password = None
        self.server = None
        self.port = None
        self.language = None
        self.receivers = []
        self.mailBody = None #what should be the body of the email
        self.subject = None
        self.emailBody = EmailBody #a reference to the module EmailBody
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
        self.language = config.get(configSection,'language')
    def sendInitialEmail(self):
        message = EmailMessage()
        if self.language == "english":
            self.subject = self.emailBody.englishInitialSubject
            self.mailBody = self.emailBody.englishInitialEmailBody
        elif self.language == "danish":
            self.subject = self.emailBody.danishInitialSubject
            self.mailBody = self.emailBody.danishInitialEmailBody
        
        
        self.setupMailInfo(message,self.sender,self.receivers,self.subject,self.mailBody)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachExcelFile(message,excelFile,filename)
        
        self.connectToSmtpAndSendMail(message)
        
    def sendPeriodicMail(self,players):
        message = EmailMessage()
        self.mailBody = f"Attached is an excel file (.xlsx) with the current standings of the feriekasse.\n"
        self.mailBody += self.getExtraBody(players)
        print(self.mailBody)
        quit() #should be removed
        self.subject = f"feriekassen, {const.FERIEKASSE_NAME}, has been updated"
        self.setupMailInfo(message,self.sender,self.receivers,self.subject,self.mailBody)
        
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
    
    def getExtraBody(self,players):
        if self.language == "english":
            allExtraBodyPickers = self.emailBody.englishExtraBodyPickers.allExtraBodyPickers
        elif self.language == "danish":
            allExtraBodyPickers = self.emailBody.danishExtraBodyPickers.allExtraBodyPickers
        shuffle(allExtraBodyPickers)
        for extraBodyPicker in allExtraBodyPickers:
            if not extraBodyPicker.condition(players):
                continue
            return extraBodyPicker.getText() + "\n"
  


