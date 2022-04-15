from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import re

#consts
INVALID_LETTERS = "æøå"

#parses input into an int if possible - otherwise returns None (rather than throwing an exception)
def parseIntOrNone(input,minValue=0,maxValue=0):
    output = None
    try:
        output = int(input)
    except ValueError:
        return None
    if minValue != 0 or maxValue != 0:
        if output > maxValue or output < minValue:
            return None
    return output

#.txt files have issues reading æøå so these are simply removed when used for comparison and URL generation fx
def removeInvalidLetters(myStr):
    for letter in INVALID_LETTERS:
        if (letter in myStr.lower()):
            myStr = myStr.replace(letter,"")
    return myStr
        
#for excelfile
#number is always at least 1
#max working output = ZZ
def numberToExcelColumn(number):
    result = ""
    chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ" #first blank space is intended
    while number > len(chars)-1:
        if result != "":
            nextLetterIndex = chars.index(result[-1])+1
            if nextLetterIndex == len(chars):
                nextLetterIndex = 1
            result = result[1:-1] + chars[nextLetterIndex]
            number -= len(chars)-1
        else:
            result += chars[1]
            number -= len(chars)-1
    if (number != 0):
        result += chars[number]
    return result

#expects input in the form "Søn. 10.4" or "10.4" or either "I Går" or "I Dag"
def textToDate(text):
    if text != "I Dag" and text != "I Går":
        if (re.search('[a-zA-Z]',text) != None):
            onlyDate = text.split(" ")[1]
        else:
            onlyDate = text
        dayAndMonth = onlyDate.split(".")
        day = parseIntOrNone(dayAndMonth[0])
        month = parseIntOrNone(dayAndMonth[1])
        #print(day,"-----",month)
        if (parseIntOrNone(dayAndMonth[1]) > 7) and (datetime.now().month < 7):
            return date(datetime.now().year-1,month,day) #if last game counted was in second half and it is the first half
        return date(datetime.now().year,month,day)

    if text == "I Dag":
        return date.today()
    else:
        return date.today() - timedelta(days=1)
    