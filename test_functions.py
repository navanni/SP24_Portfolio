from unittest.mock import patch
import pytest

from vigenere_cipher import generate_vigenere_table, format_key, remove_punctuation, vigenere_encrypt, input_vigenere_encrypt, vigenere_decrypt, input_vigenere_decrypt, find_vigenere_key, input_vigenere_key, get_encrypted_message, get_decrypted_message

def test_generate_vigenere_table():
    vigenere_table = generate_vigenere_table()
    assert len(vigenere_table) == 26, "vigenere table does not have 26 rows"
    
    for row in vigenere_table:
        assert len(row) == 26, "row in vigenere table does not have 26 columns"
        
    for i, row in enumerate(vigenere_table):
        for j, char in enumerate(row):
            expected_char = chr((i + j) % 26 + ord('A'))
            assert char == expected_char, f"unexpected character {char} at position ({i}, {j})"
    
    
def test_format_key():
    assert format_key("Hello", "KEY") == "KEYKE"
    assert format_key("Hello, World!", "KEY") == "KEYKEYKEYK"
    assert format_key("", "") == ""
    assert format_key("Giraffe") =="THEQUIC"

    
def test_remove_punctuation():
    assert remove_punctuation("Hello") == "Hello", "failed with alphabetic characters only"
    assert remove_punctuation("!@#$%^") == "", "failed with punctuation marks only"
    assert remove_punctuation("Hello, World!") == "HelloWorld", "failed on mixed characters"
    assert remove_punctuation("") == "", "failed on empty string"
    assert remove_punctuation("Hello world") == "Helloworld", "failed on spaces"    
    
def test_vigenere_encrypt():
    encrypted_message = get_encrypted_message("HELLO", "KEY")
    assert type(encrypted_message) == str
    assert vigenere_encrypt("HELLO, KEY") == "RIJVS", "failed on simple message and specified key"
    assert vigenere_encrypt("HELLO") == "ALPBI", "failed on simple message and default key"
    assert vigenere_encrypt("Hello, World!", "Vigenere") == "CMRPBAFVGL", "failed on mixed character message and specified key"
    assert vigenere_encrypt("", "") == "", "failed on empty message and key"
    assert vigenere_encrypt("%^&*()") == "", "failed on non-alphabetic message"
    
    
def test_input_vigenere_encrypt():
    with patch("getpass.getpass", side_effect=["Hello, World!", "Vigenere"]):
        assert input_vigenere_encrypt() == "CMRPBAFVGL", "test failed on message and specified key"
        
    with patch("getpass.getpass", side_effect=["", ""]):
        assert input_vigenere_encrypt() == "", "test failed on empty message and key"
        
    with patch("getpass.getpass", side_effect=["!@#$%", "Vigenere"]):
        assert input_vigenere_encrypt() == "", "test failed on non-alphabetic message and specified key"
        
        
def test_vigenere_decrypt():
    decrypted_message = get_decrypted_message("RIJVS", "KEY")
    assert type(decrypted_message) == str
    assert vigenere_decrypt("RIJVS", "KEY") == "HELLO", "failed on simple message and specified key"
    assert vigenere_decrypt("ALPBIEQBMU") == "HELLOWORLD", "failed on simple message and default key"
    assert vigenere_decrypt("", "") == "", "failed on empty message and key"
    

def test_input_vigenere_decrypt():
    with patch("getpass.getpass", side_effect=["CMRPBAFVGL", "VIGENERE"]):
        assert input_vigenere_decrypt() == "HELLOWORLD", "test failed on message and specified key"
        
    with patch("getpass.getpass", side_effect=["", ""]):
        assert input_vigenere_decrypt() == "", "test failed on empty message and key"
        
    with patch("getpass.getpass", side_effect=["!@#$%", ""]):
        assert input_vigenere_decrypt() == "!@#$%", "test failed on non-alphabetic characters and default key"

        
def test_find_vigenere_key():
    encrypted_message = get_encrypted_message("HELLO", "KEY")
    decrypted_message = get_decrypted_message("RIJVS", "KEY")
    assert type(encrypted_message and decrypted_message) == str
    assert len(encrypted_message) == len(decrypted_message)
    assert find_vigenere_key("AIDEHLWEESZXEPG", "HELLOHELLOHELLO") == "TEST"
    assert find_vigenere_key("!@#$%", "^&*()") == "", "failed on non-alphabetic messages"
    assert find_vigenere_key("", "") == "", "failed on empty messages"
    
    
def test_input_vigenere_key():
    with patch("builtins.input", side_effect=["CMRPBAFVGL", "HELLOWORLD"]):
        assert input_vigenere_key() == "VIGENEREVI"
        
    with patch("builtins.input", side_effect=["", ""]):
        assert input_vigenere_key() == "", "test failed on empty encrypted and decrypted messages"
        
    with patch("builtins.input", side_effect=["!@#$%", "^&*()"]):
        assert input_vigenere_key() == "", "test failed on non-aphabetic encrypted and decrypted messages"   
