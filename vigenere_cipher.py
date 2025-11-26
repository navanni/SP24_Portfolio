import getpass
import string

def generate_vigenere_table():
    """
    Create Vigenère table (26 x 26 table) where each row is a Caesar-shift cipher. 
    As you increase row number, the cipher is shifted one more to the right. The first row has no shift 
    
    Returns
    -------
    table: list of list of str
        26 x 26 matrix where each row represents a shifted alphabet
    """
    table = []
    
    for i in range(26):
        row = []
        for j in range(26):
            row.append(chr((i + j) % 26 + ord('A')))
        table.append(row)
            
    return table


def format_key(message, key='THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'):
    """
    Takes input message and key, formats the key so it is all caps, has no spaces,  and is the same length as the message. 
    If the key is shorter than the message, it repeats until they are the same length or truncates if longer than the message
    
    Parameters
    ----------
    message: str 
        message to be encrypted/decrypted using Vigenère cipher
    key: str, optional 
        used to determine which Caesar shift cipher is used to encrypt/decript that particular character. 
        Can be set to anything but has a defualt that is used if nothing is provided
        
    """
    key = key.upper()
    formatted_key = ""
    key_index = 0
    for i in range(len(message)):
        if message[i].isalpha():
            formatted_key += key[key_index % len(key)]
            key_index += 1

    return formatted_key


def remove_punctuation(message):
    """
    removes punctuation from the message
    
    Parameter
    --------
    message: str
        message in which punctuation is removed
        
    Returns 
    ------
    message: str
        message without any punctuation marks
    """
    return ''.join(char for char in message if char.isalpha())


def vigenere_encrypt(message, key='THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'):
    """
    Encrypts a message using the Vigenère cipher. 
    This function removes punctuation and spaces from the message, converts it to uppercase. 
    Uses the Vigenère cipher to encrypt with either the default key or a provided key.
    
    Paramteters
    ----------
    message: str
        message to be encrypted
    key: str (optional)
        key used to determine which Caesar shift cipher to use for each letter in the message
        
    Returns
    -------
    encrypted_message: str
        encrypted message
        
   Example
   -------
   >>> message = "Hello, World!"
   >>> key = "VIGENERE"
   >>> vigenere_encrypt(message, key)
   'CMRPBAFVGL'
    """
    message = remove_punctuation(message).upper()
    # format key to match length of the modified message
    key = format_key(message, key)
    encrypted_message = ''
    vigenere_table = generate_vigenere_table()
    
    for i in range(len(message)):
        if message[i].isalpha():
            # find the row and column indicies for the table
            row = ord(key[i]) - ord('A')
            col = ord(message[i]) - ord('A')
            
            if 0 <= row < 26 and 0 <= col < 26:
                encrypted_message += vigenere_table[row][col]
            else:
                raise ValueError(f"Invalid character in message or key: {message[i]} or {key[i]}")
                                 
        else:
            encrypted_message += message[i]

    return encrypted_message


def input_vigenere_encrypt():
    """
    Prompts the user for a message and a key, encrypts the message using the Vigenère cipher with the given key 
    (or default if none is given), and returns the encrypted message. Inputs are obscured
    
    Returns
    -------
    encrypted_message = str
        the encrypted message
    """
    message = getpass.getpass("please enter your message: ")
    key = getpass.getpass("please enter the key: ")
    
    if not key:
        key = 'THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'
        
    encrypted_message = vigenere_encrypt(message, key)
    return encrypted_message


def vigenere_decrypt(encryption, key='THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'):
    """
    Decrypts a message encoded using a Vigenère cipher
    
    Parameters
    ----------
    encryption: str
        message that has been encrypted with the cipher to be decrypted
    key: str (optional)
        key used to determine which Caesar shift cipher in the Vigenère table to use to decrypt. 
        Must match the key used to encrypt. 
       
    Returns
    -------
    decrypted_message: str
        decrypted message
        
    Example
    -------
    >>> encryption = "CMRPBAFVGL"
    >>> key = "VIGENERE"
    >>> vigenere_decrypt(encryption, key)
    'HELLOWORLD'
    """
    encryption = encryption.upper()
    key = key.upper()
    decrypted_message = ''
    vigenere_table = generate_vigenere_table()
    key = format_key(encryption, key)
    
    for j in range(len(encryption)):
        if encryption[j].isalpha():  # Only decrypt alphabetic characters
            # Find row in Vigenère table corresponding to character in the key
            row = ord(key[j]) - ord('A')
            # Find column in that row corresponding to encrypted character
            col = vigenere_table[row].index(encryption[j])
            decrypted_message += chr(col + ord('A'))
        else:
            decrypted_message += encryption[j]  # Non-alphabetic characters remain the same

    return decrypted_message


def input_vigenere_decrypt():
    """
    Prompts the user for a message and the key, encrypts the message using the Vigenère cipher with the provided key 
    (or default if none is given), and returns the encrypted message. Inputs are obscured
    
    Returns
    -------
    encrypted_message: str
        the encrypted message
    """
    encryption = getpass.getpass("please enter your encrypted message: ")
    key = getpass.getpass("please enter the key (press enter to use default key): ")
    
    if not key:
        key = 'THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG'
        
    decrypted_message = vigenere_decrypt(encryption, key)
    return decrypted_message


def find_vigenere_key(encrypted_message, decrypted_message):
    """
    Determine the key used for the Vigenère cipher given the encrypted and decrypted messages.

    Parameters
    ----------
    encrypted_message: str
        The encrypted message.
    decrypted_message: str
        The original (decrypted) message.

    Returns
    -------
    key: str
        The determined key.
    """
    key = ''
    key_length = len(decrypted_message)
    for enc_char, dec_char in zip(encrypted_message, decrypted_message):
        if enc_char.isalpha() and dec_char.isalpha():
            enc_val = ord(enc_char) - ord('A')
            dec_val = ord(dec_char) - ord('A')
            key_char = chr((enc_val - dec_val + 26) % 26 + ord('A'))
            key += key_char
    
    # identifies if there is a repeating pattern in the key
    # assume that key loops if the message is longer than the key
    for i in range(1, len(key)):
        if key[:i] == key[i:i+i]:
            key = key[:i]
            break
            
    return key


def input_vigenere_key():
    """
    Prompts the user for the encrypted and decrypted messages, then returns the key that was used to encrypt the message.
    
    Returns
    -------
    vigenere_key: str
        the key
    """
    encrypted_message = input("please enter the encrypted message: ")
    decrypted_message = input("please enter the decrypted message: ")
    
    vigenere_key = find_vigenere_key(encrypted_message, decrypted_message)
    return vigenere_key