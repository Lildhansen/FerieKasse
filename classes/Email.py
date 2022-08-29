import email
from msilib.schema import Condition
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
        self.attachFiles(message,excelFile,filename,"Feriekasse.png")
        
        self.connectToSmtpAndSendMail(message)
        
    def sendPeriodicMail(self,players):
        message = EmailMessage()
        if self.language == "english":
            self.mailBody = f"Attached is an excel file (.xlsx) with the current standings of the feriekasse.\n"
            self.subject = f"feriekassen has been updated"
        elif self.language == "danish":
            self.mailBody = f"En excel fil (.xlsx) med pointfordelingen for feriekassen er vedhæftet\n"
            self.subject = f"feriekassen er blevet opdateret"
        self.mailBody += self.getExtraBody(players)
        print(self.mailBody)
        #quit() #should be removed
        self.setupMailInfo(message,self.sender,self.receivers,self.subject,self.mailBody)
        
        excelFile = fr"data/{const.FERIEKASSE_NAME}/Feriekasse.xlsx" 
        filename = "feriekasse (" + date.today().strftime("%d-%m-%Y") + ").xlsx"
        self.attachFiles(message,excelFile,filename,"Feriekasse.png")
        
        self.connectToSmtpAndSendMail(message)
        
    def setupMailInfo(self,message,sender,receivers,subject,body):
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = subject
        message.set_content(body)
    
    def attachFiles(self,message,excelFile,newFileName,screenshotName):
        self.attachExcelFiles(message,excelFile,newFileName)
        self.attachExcelFileScreenshot(message,excelFile,screenshotName)
    def attachExcelFiles(self,message,excelFile,newFileName):
        with open(excelFile, 'rb') as f:
            fileData = f.read()
        message.add_attachment(fileData, maintype="application", subtype="xlsx", filename=newFileName)
    def attachExcelFileScreenshot(self,message,excelFile,screenshotName):
        excel2img.export_img(excelFile,screenshotName, "Feriekasse", None) #"Feriekasse" = sheetname
        with open(screenshotName, 'rb') as f:
            imgData = f.read()
        message.add_attachment(imgData, maintype="image", subtype="png", filename=screenshotName)
        
    def connectToSmtpAndSendMail(self,message):
        smtp = smtplib.SMTP_SSL(self.server)
        smtp.connect(self.server,self.port)
        smtp.login(self.sender,self.password)
        smtp.sendmail(to_addrs=self.receivers,msg=message.as_string(),from_addr=self.sender)
        smtp.quit()
        print("Email sent")
    
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
    def updateLastMailSentValue(self):
        emailIniFile = fr"data/{const.FERIEKASSE_NAME}/email.ini"
        config = configparser.ConfigParser()
        config.read(emailIniFile)
        try:
            config.add_section("email_config")
        except configparser.DuplicateSectionError:
            pass
        config.set("email_config", "lastDateSent", date.today().isoformat())
        with open(emailIniFile, "w") as config_file:
            config.write(config_file)


