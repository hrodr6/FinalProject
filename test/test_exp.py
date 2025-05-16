import pytest
from src.exp import Exp, classify_old_new, calculate_accuracy

#i was confused by what was meant as pytest, so Chat GPT helped to explain and formulate some aspects of this code
def test_is_response_correct():
    exp = Exp(None)  
    assert exp.is_response_correct("u", "u") == True
    assert exp.is_response_correct("i", "u") == False

def test_classify_old_new():
    familizarization_list = ["word1", "word2", "word3"]  # use  actual familiarization list items
    assert classify_old_new("word1", fam_list) == "old"  
    assert classify_old_new("wordX", fam_list) == "new"  

def test_calculate_accuracy():
    assert calculate_accuracy(8, 10) == 80.0
    assert calculate_accuracy(0, 10) == 0.0

