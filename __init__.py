from unittest.mock import patch
import pytest

from my_module import vigenere_cipher

def test_generate_vigenere_table():
    vigenere_table = vigenere_cipher.generate_vigenere_table()
    assert len(vigenere_table) == 26, "vigenere table does not have 26 rows"
    
    for row in vigenere_table:
        assert len(row) == 26, "row in vigenere table does not have 26 columns"
        
    for i, row in enumerate(vigenere_table):
        for j, char in enumerate(row):
            expected_char = chr((i + j) % 26 + ord('A'))
            assert char == expected_char, f"unexpected character {char} at position ({i}, {j})"
    
    
def test_format_key():
    assert vigenere_cipher.format_key("Hello", "KEY") == "KEYKE"
    assert vigenere_cipher.format_key("Hello, World", "KEY") == "KEYKE, EYKEY!"
    assert vigenere_cipher.format_key("", "") == ""
    assert vigenere_cipher.format_key("Giraffe") =="THEQUIC"

    
def test_remove_punctuation():
    assert vigenere_cipher.remove_punctuation("Hello") == "Hello", "failed with alphabetic characters only"
    assert vigenere_cipher.remove_punctuation("!@#$%^") == "", "failed with punctuation marks only"
    assert vigenere_cipher.remove_punctuation("Hello, World!") == "HelloWorld", "failed on mixed characters"
    assert vigenere_cipher.remove_punctuation("") == "", "failed on empty string"
    assert vigenere_cipher.remove_punctuation("Hello world") == "Helloworld", "failed on spaces"
    assert vigenere_cipher.remove_punctuation("你好, world!") == "world", "failed on non-ASCII characters"
    
    
def test_vigenere_encrypt():
    assert type(encrypted_message) == 'str'
    assert vigenere_cipher.vigenere_encrypt("HELLO, KEY") == "RIJVS", "failed on simple message and specified key"
    assert vigenere_cipher.vigenere_encrypt("HELLO") == "ALPBI", "failed on simple message and default key"
    assert vigenere_cipher.vignere_encrypt("Hello, World!", "Vigenere") == "CMRPBAFVGL", "failed on mixed character message and specified key"
    assert vigenere_cipher.vigenere_encrypt("", "") == "", "failed on empty message and key"
    assert vigenere_cipher.vigenere_encrypt("%^&*()") == "", "failed on non-alphabetic message"
    assert vigenere_cipher.vigenere_encrypt("你好, world!", "KEY") == "UYVJN", "failed on non-ASCII characters"
    
    
def test_input_vigenere_encrypt():
    with patch("getpass.getpass", side_effect=["Hello, World!", "Vigenere"]):
        assert input_vigenere_encrypt() == "CMRPBAFVGL", "test failed on message and specified key"
        
    with patch("getpass.getpass", side_effect=["", ""]):
        assert input_vigenere_encrypt() == "", "test failed on empty message and key"
        
    with patch("getpass.getpass", side_effect=["!@#$%", "Vigenere"]):
        assert input_vigenere_encrypt() == "", "test failed on non-alphabetic message and specified key"
        
        
def test_vigenere_decrypt():
    assert type(decrypted_message) == 'str'
    assert vigenere_cipher.vigenere_decrypt("RIJVS", "KEY") == "HELLO", "failed on simple message and specified key"
    assert vigenere_cipher.vigenere_decrypt("ALPBIEQBMU") == "HELLOWORLD", "failed on simple message and default key"
    assert vigenere_cipher.vigenere_decrypt("", "") == "", "failed on empty message and key"
    
    
def test_input_vigenere_decrypt():
    with patch("getpass.getpass", side_effect=["CMRPBAFVGL", "Vigenere"]):
        assert input_vigenere_decrypt() == "HELLOWORLD", "test failed on message and specified key"
        
    with patch("getpass.getpass", side_effect=["", ""]):
        assert input_vigenere_decrypt() == "", "test failed on empty message and key"
        
    with patch("getpass.getpass", side_effect=["!@#$%"]):
        assert input_vigenere_decrypt() == "", "test failed on non-alphabetic characters and default key"
        
        
def test_find_vigenere_key():
    assert type(encrypted_message and decrypted_message) == "str"
    assert len(encrypted_message) == len(decrypted_message)
    assert vigenere_cipher.find_vigenere_key("NQXLKPZFNVHL", "HELLOHELLOHELLO") == "TEST"
    assert vigenere_cipher.find_vigenere_key("!@#$%", "^&*()") == "", "failed on non-alphabetic messages"
    assert vigenere_cipher.find_vigenere_key("", "") == "", "failed on empty messages"
    
    
def test_input_vigenere_key():
    with patch("builtins.input", side_effect=["CMRPBAFVGL", "HELLOWORLD"]):
        assert input_vigenere_key() == "VIGENERE"
        
    with patch("builtins.input", side_effect=["", ""]):
        assert input_vigenere_key() == "", "test failed on empty encrypted and decrypted messages"
        
    with patch("builtins.input", side_effect=["!@#$%", "^&*()"]):
        assert input_vigenere_key() == "", "test failed on non-aphabetic encrypted and decrypted messages"   