import smtplib
import configparser
from email.message import EmailMessage
from random import shuffle
import excel2img
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
        self.emailBody = EmailBody #a reference to the EmailBody module
        self.__setupEmailInformationFromConfigFile(emailIniFile)
        
    #sets the attributes of the current Email object up based on a .ini file (directory of that file is the parameter of the method)
    # this method is only called when instantiating an Email object
    def __setupEmailInformationFromConfigFile(self,emailIniFile):
        configSection = "email_config"
        config = configparser.ConfigParser()
        config.read(emailIniFile)
        self.sender = config.get(configSection,'sender')
        self.password = config.get(configSection,'password')
        self.server = config.get(configSection,'server')
        self.port = int(config.getint(configSection,'port'))
        self.receivers = config.get(configSection,'receivers').split(';')
        self.language = config.get(configSection,'language')
        
    #sends the initial email with the initial standings in the excel file through SMTP
    def sendInitialEmail(self):
        message = EmailMessage()
        if self.language == "english":
            self.subject = self.emailBody.englishInitialSubject
            self.mailBody = self.emailBody.englishInitialEmailBody
        elif self.language == "danish":
            self.subject = self.emailBody.danishInitialSubject
            self.mailBody = self.emailBody.danishInitialEmailBody
        
        
        self.setupMailInfo(message)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachFiles(message,excelFile,filename,fr"data/{const.FERIEKASSE_NAME}/Feriekasse.png")
        
        self.connectToSmtpAndSendMail(message)
        
    #sends the periodic email with attached image and excel file through smtp
    def sendPeriodicMail(self,players):
        message = EmailMessage()
        if self.language == "english":
            self.mailBody = f"Attached is an excel file (.xlsx) and a picture with the current standings of the feriekasse.\n"
            self.subject = f"feriekassen has been updated"
        elif self.language == "danish":
            self.mailBody = f"En excel fil (.xlsx) samt et billede med pointfordelingen for feriekassen er vedhæftet\n"
            self.subject = f"feriekassen er blevet opdateret"
        self.mailBody += self.getExtraBody(players)
        print("Body of the email:",self.mailBody)
        self.setupMailInfo(message)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachFiles(message,excelFile,filename,fr"data/{const.FERIEKASSE_NAME}/Feriekasse.png")
        
        self.connectToSmtpAndSendMail(message)
    
    #sets up the basic information of the email
    def setupMailInfo(self,message):
        message['From'] = self.sender
        message['To'] = self.receivers
        message['Subject'] = self.subject
        message.set_content(self.mailBody)
        
    
    #attach the files (that is excelfile and screenshot thereof) to the email
    def attachFiles(self,message,excelFile,newFileName,screenshotName):
        self.attachExcelFile(message,excelFile,newFileName)
        self.attachExcelFileScreenshot(message,excelFile,screenshotName)
        
    #attach the excel file to the email
    def attachExcelFile(self,message,excelFile,newFileName):
        with open(excelFile, 'rb') as f:
            fileData = f.read()
        message.add_attachment(fileData, maintype="application", subtype="xlsx", filename=newFileName)
        
    #take screenshot of the excel file and attach it to the email
    def attachExcelFileScreenshot(self,message,excelFile,screenshotName):
        excel2img.export_img(excelFile,screenshotName, "Feriekasse", None) #"Feriekasse" = sheetname
        with open(screenshotName, 'rb') as f:
            imgData = f.read()
        message.add_attachment(imgData, maintype="image", subtype="png", filename=screenshotName)
        
    #connect to smtp server and send the email
    def connectToSmtpAndSendMail(self,message):
        smtp = smtplib.SMTP_SSL(self.server)
        smtp.connect(self.server,self.port)
        smtp.login(self.sender,self.password)
        smtp.sendmail(to_addrs=self.receivers,msg=message.as_string(),from_addr=self.sender)
        smtp.quit()
        print("Email sent")
    
    #get the extra body of the email (the part that is not the same for every email)
    def getExtraBody(self,players):
        if self.language == "english":
            allExtraBodyPickers = self.emailBody.englishExtraBodyPickers.allExtraBodyPickers
        elif self.language == "danish":
            allExtraBodyPickers = self.emailBody.danishExtraBodyPickers.allExtraBodyPickers
        shuffle(allExtraBodyPickers)
        for extraBodyPicker in allExtraBodyPickers:
            if not extraBodyPicker.condition(players):
                continue
            return extraBodyPicker.getText(self.language) + "\n"
    
    #Updates the last mail sent value in the email.ini file
    def updateLastMailSentValue(self,emailIniFileLocation):
        config = configparser.ConfigParser()
        config.read(emailIniFileLocation)
        try:
            config.add_section("email_config")
        except configparser.DuplicateSectionError:
            pass
        config.set("email_config", "lastDateSent", date.today().isoformat())
        with open(emailIniFileLocation, "w") as config_file:
            config.write(config_file)


