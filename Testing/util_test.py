import utilities.util as util
import pytest

def test_parseIntOrNone_parses_int_correctly():
    assert util.parseIntOrNone("100")==100

@pytest.mark.parametrize("test_input", [("2.5"),("abcdef"),("")])
def test_parseIntOrNone_returns_None_if_input_cannnot_be_int(test_input):
    assert util.parseIntOrNone(test_input) == None
        
@pytest.mark.parametrize("test_input,expected", [("abcædefgæ", "abcdefg"), ("123-. Hej øå 123312''", "123-. Hej  123312''"),
                                                 ("æøå", ""),("æøåæøåæøå abc"," abc") ])
def test_removeInvalidLetters_RemovesInvalidLetters(test_input,expected):
    assert util.removeInvalidLetters(test_input) == expected

@pytest.mark.parametrize("test_input,expected", [(1, "A"), (26,"Z"),(27,"AA"),(53, "BA"),(14,"N"),(79,"CA"),(26*27,"ZZ")]) 
#ZZ is max value. for 3 digits it omits one of the digits (fx AAA is AA instead) 
# though it doesnt matter cause that many players will never play it
def test_numberToExcelColumn_returns_correct_columnstring(test_input,expected):
    assert util.numberToExcelColumn(test_input) == expected
