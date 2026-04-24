#----Import Python Packages----#
import json
import base64
import os
import codecs
import random
import time
import sys
import termios
import tty

#----Colours----#
class Colours:
    '''colours for texts'''
    BLACK = '\033[38;5;0m'
    RED = '\033[38;5;1m'
    GREEN = '\033[38;5;2m'
    YELLOW = '\033[38;5;3m'
    BLUE = '\033[38;5;4m'
    MAGENTA = '\033[38;5;5m'
    CYAN = '\033[38;5;6m'
    WHITE = '\033[38;5;7m'
    GOLD = '\033[38;5;220m'
    
    BG_RED = '\033[48;5;196m'
    BG_GREEN = '\033[48;5;46m'
    BG_YELLOW = '\033[48;5;226m'
    BG_BLUE = '\033[48;5;21m'
    BG_WHITE = '\033[48;5;15m'
    BG_BLACK = '\033[48;5;0m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    
    RESET = '\033[0m'
#----Colours----#

#----Precode Variables----#
CDC0 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) # Card Deck Completion representing none with 0

#----Save File Money----#

def to_binary_str(s):
    '''binary encoder'''
    return ''.join(format(ord(c), '08b') for c in s)

def from_binary_str(b):
    '''binary decoder'''
    # Validate binary string
    if len(b) % 8 != 0:
        raise ValueError("Binary string length must be divisible by 8")
    if not all(c in '01' for c in b):
        raise ValueError("Binary string must only contain 0s and 1s")
    
    chars = [chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)]
    return ''.join(chars)

def encode_save(json_str):
    '''encodes using method under'''
    # Base64 encode
    b64 = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    # Reverse
    rev = b64[::-1]
    # ROT13 encode
    rot = codecs.encode(rev, 'rot_13')
    # Binary encode
    binary = to_binary_str(rot)
    return binary.encode('utf-8')  # Write as bytes

def decode_save(encoded_bytes):
    '''decodes using method under'''
    # grabs code
    binary_str = encoded_bytes.decode('utf-8')
    # Binary decode
    rot = from_binary_str(binary_str)
    # ROT13 decode
    rev = codecs.decode(rot, 'rot_13')
    # Reverse
    b64 = rev[::-1]
    # Base64 decode
    json_str = base64.b64decode(b64).decode('utf-8')
    return json_str


def get_config_dir():
    '''Return platform-appropriate config directory'''
    return os.path.expanduser("~/.config/guess-the-duck")

def load_game(): # access save file -JSON
    '''loading save file - returns both money and name'''
    config_dir = get_config_dir()
    save_path = os.path.join(config_dir, "Guess-the-Duck.bin")
    try:
        with open(save_path, "rb") as f:
            encoded_bytes = f.read()
            json_str = decode_save(encoded_bytes)
            data = json.loads(json_str)
            print("Save file loaded")
            return (data.get("wins", 0),
                    data.get("name", None),
                    data.get("Scards", CDC0),
                    data.get("Ccards", CDC0),
                    data.get("Dcards", CDC0),
                    data.get("Hcards", CDC0))
    except FileNotFoundError:
        print("New player - no save file found")
        return 0, None, CDC0, CDC0, CDC0, CDC0
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Corrupted save file - using defaults. Error: {error}")
        return 0, None, CDC0, CDC0, CDC0, CDC0

def save_game(wins=None, name=None, Scards=None, Ccards=None, Dcards=None, Hcards=None):
    '''saving game data'''
    if wins is None:
        wins = WINS
    if name is None:
        name = USER_NAME
    if Scards is None:
        Scards = SCARDS
    if Ccards is None:
        Ccards = CCARDS
    if Dcards is None:
        Dcards = DCARDS
    if Hcards is None:
        Hcards = HCARDS

    data = {
        "wins": wins,
        "name": name,
        "Scards": Scards,
        "Ccards": Ccards,
        "Dcards": Dcards,
        "Hcards": Hcards,
    }
    json_str = json.dumps(data)
    encoded_bytes = encode_save(json_str)
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    save_path = os.path.join(config_dir, "Guess-the-Duck.bin")
    with open(save_path, "wb") as f:
        f.write(encoded_bytes)

#----Save File Money----#