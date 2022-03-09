from utilities.util import removeInvalidLetters
import pytest


@pytest.mark.parametrize("test_input,expected", [("abcædefgæ", "abcdefg"), ("123-. Hej øå 123312''", "123-. Hej  123312''"),
                                                 ("æøå", ""),("æøåæøåæøå abc"," abc") ])
def test_removeInvalidLetters_RemovesInvalidLetters(test_input,expected):
    assert removeInvalidLetters(test_input) == expected


        