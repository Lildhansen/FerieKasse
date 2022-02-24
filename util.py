invalidLetters = "æøå"

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

def removeInvalidLetters(myStr):
    for letter in invalidLetters:
        if (letter in myStr.lower()):
            myStr = myStr.replace(letter,"")
    return myStr
        
