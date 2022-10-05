from datetime import date
import os
import configparser
from email.message import EmailMessage

from classes.Email import Email

#how to handle directories with github actions
iniFileLocation = os.path.join(os.path.join(os.path.dirname(__file__),"EmailTestMocks"),'EmailTest.ini')
iniFileLocation = "Testing/EmailTestMocks/EmailTest.ini"
def test_data_is_setup_correct_from_ini_file():
    email = Email(iniFileLocation)
    assert email.sender == "me"
    assert email.password == "pword"
    assert email.server == "192.168.0.1"
    assert email.port == 123
    assert email.language == "danish"
    assert len(email.receivers) == 2
    assert email.receivers[0] == "a"
    assert email.receivers[1] == "b"

def test_setupMailInfo_sets_up_correct_info_for_message():
    email = Email(iniFileLocation)
    message = EmailMessage()
    email.mailBody = "this is the body"
    email.subject = "this is the subject"
    email.setupMailInfo(message)
    assert message["From"] == email.sender
    assert message['To'] == ", ". join(email.receivers) #receivers are stored as a string, like "a, b, c"
    assert message['Subject'] == email.subject
    assert message.get_content() == email.mailBody + "\n" #body of the mail always ends on newline
   

def test_attachExcelFile_adds_excel_file_to_message():
    email = Email(iniFileLocation)
    message = EmailMessage()
    email.attachExcelFile(message,os.path.join(os.path.join(os.path.dirname(__file__),"EmailTestMocks"),'Feriekasse.xlsx'),"feriekasse.xlsx")
    assert len(message.get_payload()) == 1
    assert message.get_payload()[0].get_content_type() == "application/xlsx"
    assert message.get_payload()[0].get_filename() == "feriekasse.xlsx"

def test_attachExcelFileScreenshot_adds_image_to_message():
    email = Email(iniFileLocation)
    message = EmailMessage()
    email.attachExcelFileScreenshot(message,os.path.join(os.path.join(os.path.dirname(__file__),"EmailTestMocks"),'Feriekasse.xlsx'),'Feriekasse.png')
    assert len(message.get_payload()) == 1
    assert message.get_payload()[0].get_content_type() == "image/png" 
    assert os.path.basename(message.get_payload()[0].get_filename()) == "Feriekasse.png"
 
#integration test 
def test_attachFiles_adds_excel_file_and_image_to_message():
    email = Email(iniFileLocation)
    message = EmailMessage()
    email.attachFiles(message,os.path.join(os.path.join(os.path.dirname(__file__),"EmailTestMocks"),'Feriekasse.xlsx'),"feriekasse.xlsx",os.path.join(os.path.join(os.path.dirname(__file__),"EmailTestMocks"),'Feriekasse.png'))
    assert len(message.get_payload()) == 2
    assert message.get_payload()[0].get_content_type() == "application/xlsx"
    assert message.get_payload()[0].get_filename() == "feriekasse.xlsx"
    assert message.get_payload()[1].get_content_type() == "image/png" 
    assert os.path.basename(message.get_payload()[1].get_filename()) == "Feriekasse.png" #for some reason this is the full directory - though it still works fine
    
def test_updateLastMailSentValue_updates_last_mail_sent_value_to_todays_date_in_ini_file():
    email = Email(iniFileLocation)
    config = configparser.ConfigParser()
    
    email.updateLastMailSentValue(iniFileLocation)
    config.read(iniFileLocation)
    lastDateSent = config.get("email_config","lastdatesent")
    assert lastDateSent == date.today().isoformat()