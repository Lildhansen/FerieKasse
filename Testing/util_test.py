import pytest
from freezegun import freeze_time
from datetime import date, timedelta, datetime

import utilities.util as util

def test_parseIntOrNone_parses_int_correctly():
    assert util.parseIntOrNone("100")==100

@pytest.mark.parametrize("test_input", [("2.5"),("abcdef"),("")])
def test_parseIntOrNone_returns_None_if_input_cannnot_be_int(test_input):
    assert util.parseIntOrNone(test_input) == None
        
@pytest.mark.parametrize("test_input,expected", [("abcædefgæ", "abcdefg"), ("123-. Hej øå 123312''", "123-. Hej  123312''"),
                                                 ("æøå", ""),("æøåæøåæøå abc"," abc") ])
def test_removeInvalidLetters_removes_invalid_letters(test_input,expected):
    assert util.removeInvalidLetters(test_input) == expected

def test_removeInvalidLetters_keeps_string_intact_in_no_invalid_letters():
    validString = "Liverpool FC"
    assert util.removeInvalidLetters(validString) == validString

@pytest.mark.parametrize("test_input,expected", [(1, "A"), (26,"Z"),(27,"AA"),(53, "BA"),(14,"N"),(79,"CA"),(26*27,"ZZ")]) 
#ZZ is max value. for 3 digits it omits one of the digits (fx AAA is AA instead) 
# though it doesnt matter cause that many players will never play it
def test_numberToExcelColumn_returns_correct_columnstring(test_input,expected):
    assert util.numberToExcelColumn(test_input) == expected

def test_textToDate__converts_I_Dag_correctly():
    today = date.today()
    assert util.textToDate("I Dag") == today
    
def test_textToDate__converts_I_Går_correctly():
    yesterday = date.today() - timedelta(days=1)
    assert util.textToDate("I Går") == yesterday

@freeze_time("2022-01-01")
def test_textToDate_converts_month_day_and_weekdays_correctly_if_input_date_is_in_first_half_and_date_is_in_first_half():
    test_input = util.textToDate("Ons. 10.4")
    expected_date = date(datetime.now().year,4,10)
    
    actual = test_input.strftime("%Y") + test_input.strftime("%m") + test_input.strftime("%d")
    expected = expected_date.strftime("%Y") + expected_date.strftime("%m") + expected_date.strftime("%d")
    assert actual== expected

@freeze_time("2022-04-15")
def test_textToDate_converts_month_day_and_weekdays_correctly_if_input_date_is_in_second_half_and_date_is_in_first_half(): #special case - use freeze time
    test_input = util.textToDate("Fre. 10.10")
    expected_date = date(datetime.now().year-1,10,10)
    
    actual = test_input.strftime("%Y") + test_input.strftime("%m") + test_input.strftime("%d")
    expected = expected_date.strftime("%Y") + expected_date.strftime("%m") + expected_date.strftime("%d")
    assert actual== expected

@freeze_time("2022-10-15")
def test_textToDate_converts_month_day_and_weekdays_correctly_if_input_date_is_in_first_half_and_date_is_in_second_half():
    test_input = util.textToDate("Søn. 1.1")
    expected_date = date(datetime.now().year,1,1)
    
    actual = test_input.strftime("%Y") + test_input.strftime("%m") + test_input.strftime("%d")
    expected = expected_date.strftime("%Y") + expected_date.strftime("%m") + expected_date.strftime("%d")
    assert actual== expected
    
@freeze_time("2022-12-12")
def test_textToDate_converts_month_day_and_weekdays_correctly_if_input_date_is_in_second_half_and_date_is_in_second_half(): #use freeze time
    test_input = util.textToDate("Lør. 16.12")
    expected_date = date(datetime.now().year,12,16)
    
    actual = test_input.strftime("%Y") + test_input.strftime("%m") + test_input.strftime("%d")
    expected = expected_date.strftime("%Y") + expected_date.strftime("%m") + expected_date.strftime("%d")
    assert actual== expected
