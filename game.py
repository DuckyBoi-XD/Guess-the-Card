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
import shutil

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
CARD_SUITS = ("♠", "♦", "♥", "♣")

temp_CardDeck = []
CardDeck = None
savefile_value = 0

temp_SuitNumbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "BACK"]

#----Card Deck----#

for suit in CARD_SUITS:
    for value_card in range(2, 11):
        temp_CardDeck.append(f"{value_card}{suit}")

for suit in CARD_SUITS:
    temp_CardDeck.append(f"J{suit}")
    temp_CardDeck.append(f"Q{suit}")
    temp_CardDeck.append(f"K{suit}")
    temp_CardDeck.append(f"A{suit}")

#----Card Deck----#

#----Save File----#

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
    '''loading save file - returns pat game data'''
    global savefile_value
    config_dir = get_config_dir()
    save_path = os.path.join(config_dir, "Guess-the-Duck.bin")
    try:
        with open(save_path, "rb") as f:
            encoded_bytes = f.read()
            json_str = decode_save(encoded_bytes)
            data = json.loads(json_str)
            savefile_value = 1
            return (data.get("deckscomplete", 0),
                    data.get("carddeck", temp_CardDeck),
                    data.get("guessamount", 0),
                    data.get("Scards", temp_SuitNumbers),
                    data.get("Ccards", temp_SuitNumbers),
                    data.get("Dcards", temp_SuitNumbers),
                    data.get("Hcards", temp_SuitNumbers))
    except FileNotFoundError:
        print("New player - no save file found")
        savefile_value = 2
        return 0, temp_CardDeck, 0, temp_SuitNumbers, temp_SuitNumbers, temp_SuitNumbers, temp_SuitNumbers
    except (ValueError, json.JSONDecodeError) as error:
        print(f"Corrupted save file - using defaults. Error: {error}")
        savefile_value = 3
        return 0, temp_CardDeck, 0, temp_SuitNumbers, temp_SuitNumbers, temp_SuitNumbers, temp_SuitNumbers

def save_game(deckscomplete=None, carddeck=None, guessnumber=None, Sscards=None, Cscards=None, Dscards=None, Hscards=None):
    '''saving game data'''
    if deckscomplete is None:
        deckscomplete = DECKS_COMPLETE
    if carddeck is None:
        carddeck = CardDeck
    if guessnumber is None:
        guessnumber = GUESS_PROGRESS
    if Sscards is None:
        Sscards = sSuitNumbers
    if Cscards is None:
        Cscards = cSuitNumbers
    if Dscards is None:
        Dscards = dSuitNumbers
    if Hscards is None:
        Hscards = hSuitNumbers

    data = {
        "deckscomplete": deckscomplete,
        "carddeck": carddeck,
        "guessamount" : guessnumber,
        "Scards": Sscards,
        "Ccards": Cscards,
        "Dcards": Dscards,
        "Hcards": Hscards,
    }
    json_str = json.dumps(data)
    encoded_bytes = encode_save(json_str)
    config_dir = get_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    save_path = os.path.join(config_dir, "Guess-the-Duck.bin")
    with open(save_path, "wb") as f:
        f.write(encoded_bytes)

#----Save File Money----#

#----Variable----#

DECKS_COMPLETE, CardDeck, GUESS_PROGRESS, sSuitNumbers, cSuitNumbers, dSuitNumbers, hSuitNumbers = load_game()
if savefile_value == 1:
    pass
elif savefile_value == 2 or savefile_value == 3:
    random.shuffle(CardDeck)

CARD_SUITS = ("♠", "♦", "♥", "♣")
CARD_IN_DECK = len(CardDeck) # How much carss is left in the deck counter
space_temp = None

GUESS_DECK_NUMBER = GUESS_PROGRESS / 52
GUESS_DECK_PERCENT = round(GUESS_DECK_NUMBER * 100, 2)

cardSuits = [f"{Colours.BLACK}♠ - Spades{Colours.RESET}", f"{Colours.RED}♦ - Diamonds{Colours.RESET}", f"{Colours.BLACK}♣ - Clubs{Colours.RESET}", f"{Colours.RED}♥ - Hearts{Colours.RESET}" ]
Confirm_Redo = ["✅ Confirm", "🔄 Redo"]

#----Variable----#

#----Function Variables----#

def LINE():
    ''''creates line spacing'''
    print(f"{Colours.BOLD}{Colours.MAGENTA}|====================--------------------==========--------==========--------------------====================|{Colours.RESET}")

def clear_screen():
    ''''clear screen function'''
    os.system('clear')  # Unix/Linux/macOS only

def flush_clear_screen():
    ''''clear screen function but with flushing'''
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def is_float(variable):
    '''check if value is a float'''
    try:
        float(variable)
        return True
    except ValueError:
        return False

def print_tw(sentence, type_delay=0.01):
    '''creates a type writer effect'''
    for char in sentence:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(type_delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

def CLI_SW():
    '''Command Line Interface Size Warning'''

    while True:
        global width
        global height
        width, height = shutil.get_terminal_size()
        if width < 110 or height < 30:
            clear_screen()
            if width < 110:
                ColourSWW = Colours.RED
            elif width >= 110:
                ColourSWW = Colours.GREEN
            else:
                ColourSWW = Colours.WHITE
            if height < 30:
                ColourSWH = Colours.RED
            elif height >= 30:
                ColourSWH = Colours.GREEN
            else:
                ColourSWH = Colours.WHITE

            height_top_bottom = 12 * "\n"
            spaces_TS = 43 * " "
            spaces_WH = 45 * " "
            spaces_RS = 48 * " "
            spaces_WH2 = 44 * " "
            print(f"{height_top_bottom}{spaces_TS}{Colours.BOLD}Terminal size too small:{Colours.RESET}\n"
                  f"{spaces_WH}Width: {ColourSWW}{width}{Colours.RESET} | Height: {ColourSWH}{height}{Colours.RESET}\n\n"
                  f"{spaces_RS}Required size:\n"
                  f"{spaces_WH2}Width: {Colours.BOLD}110{Colours.RESET} | Height: {Colours.BOLD}30{Colours.RESET}{height_top_bottom} ")
            while True:
                width2, height2 = shutil.get_terminal_size()
                if width != width2 or height != height2:
                    clear_screen()
                    break
                elif width == width2 and height == height2:
                    time.sleep(0.25)
                    continue
        elif width >= 110 and height >= 30:
            break

def card_loading(countvalue):
    '''function that create animation'''
    clear_screen()
    count = 0
    while count < countvalue:
        LINE()
        sys.stdout.write("Drawing card")
        print_tw(" ...", 0.2)
        count += 1
        time.sleep(0.2)
        clear_screen()

def get_title():
    "Prev: GuessTheDuckTitle"
    return f"{Colours.CYAN}{Colours.BOLD}❓ Guess The Duck 🃏\n{Colours.YELLOW}Decks Completed: {DECKS_COMPLETE} | % of Deck Guessed: {GUESS_DECK_PERCENT}% | Amount of card left : {CARD_IN_DECK}"

#----Function Variables----#

#----Single Key Track----#
def key_press(option):
    '''single key tracking - Unix/macOS'''
    try:
        if option == 0:
            print(f"{Colours.RED}Press any key to continue{Colours.RESET}")
        elif option == 1:
            print(f"{Colours.YELLOW}🔄 Press any key to guess another card{Colours.RESET}")
        elif option == 2:
            print(f"{Colours.YELLOW}🔄 Press any key to start another deck{Colours.RESET}")
        CLI_SW()
        # Unix/Linux/macOS with termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return True
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Guess the Duck{Colours.RESET}")
        sys.exit()

#----Single Key Track----#

#----Arrow Key Track----#
def arrow_key():
    '''reads and looks for arrow press - Unix/macOS'''
    try:
        # Unix/Linux/macOS
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            
            # Check for CTRL-C and CTRL-D in raw mode
            if ord(key) == 3:  # CTRL-C
                print(f"\n{Colours.RED}Thanks for playing Guess the Duck{Colours.RESET}")
                sys.exit()
            elif ord(key) == 4:  # CTRL-D
                print(f"\n{Colours.RED}Thanks for playing Guess the Duck{Colours.RESET}")
                sys.exit()
            
            # Check for escape sequence (arrow keys)
            if ord(key) == 27:  # ESC
                key += sys.stdin.read(2)  # Read the next 2 characters (for arrows)
                
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Guess the Duck{Colours.RESET}")
        sys.exit()
#----Arrow Key Track----#

#----Arrow Key Menu System----#

def arrow_menu(title, text, options, menu_orientation):
    """generic arrow key menu system"""
    try:
        global space_temp
        card_numbers_menu = "|"
        selected = 0
        arrow_space = None
        menu_orientation_selection = False
        while True:
            flush_clear_screen()
            clear_screen()
            LINE()
            print(f"{Colours.BOLD}{Colours.CYAN}{title}")
            LINE()
            if text is not None:
                print(text + "\n")
            else:
                pass
            # Display menu options
            if menu_orientation == 0:
                if menu_orientation_selection is False:
                    selected = 0
                    menu_orientation_selection = True
                for i, option in enumerate(options):
                    if i == selected:
                        print(f"{Colours.BOLD}{Colours.YELLOW}► {option}{Colours.RESET}")
                    else:
                        print(f"{Colours.WHITE}  {option}{Colours.RESET}")
            elif menu_orientation == 1:
                if menu_orientation_selection is False:
                    selected = 1
                    menu_orientation_selection = True
                card_numbers_menu = "|"
                for i, option in enumerate(options, start=1):
                    if option == "BACK":
                        card_number = f" {Colours.RED}{option}{Colours.RESET} |"
                    else:
                        card_number = f" {option} |"

                    if i == selected:
                        card_number = f" {Colours.RESET}{Colours.YELLOW}{option}{Colours.RESET} |"
                        space_temp = option
                    if space_temp == "10":
                        arrow_space = " " * (selected * 4 - 1)
                    
                    elif "10" in options:
                            if space_temp == "J" or space_temp == "Q" or space_temp == "K" or space_temp == "A" or space_temp =="BACK":
                                arrow_space = " " * ((selected - 1) * 4 - 2 + (1 * 4 + 1))
                            else:
                                arrow_space = " " * (selected * 4 - 2)
                    else:
                        arrow_space = " " * (selected * 4 - 2)
                        
                    card_numbers_menu += card_number

                print(card_numbers_menu)
                print(f"{arrow_space}{Colours.BOLD}{Colours.YELLOW}▲{Colours.RESET}")

            LINE()
            key = arrow_key()
            CLI_SW()
            # Handle arrow keys and other inputs for Unix/macOS
            if menu_orientation == 1:
                if len(key) > 1:
                    n = len(options)
                    if key == '\x1b[C':  # right arrow
                        selected = (selected % n) + 1
                    elif key == '\x1b[D':  # left arrow
                        selected = ((selected - 2) % n) + 1
                    elif ord(key[0]) == 13:  # Enter
                        return selected
                    elif len(key) == 1 and ord(key) == 27:  # ESC alone
                        return -1
                elif len(key) == 1:
                    n = len(options)
                    if key.lower() == 'd':  # d key - right
                        selected = (selected % n) + 1
                    elif key.lower() == 'a':  # a key - left
                        selected = ((selected - 2) % n) + 1
                    elif key == '\r' or key == '\n':  # Enter
                        return selected
            else:
                if len(key) > 1:
                    if key == '\x1b[A':  # up arrow
                        selected = (selected - 1) % len(options)
                    elif key == '\x1b[B':  # down arrow
                        selected = (selected + 1) % len(options)
                    elif ord(key[0]) == 13:  # Enter
                        return selected
                    elif len(key) == 1 and ord(key) == 27:  # ESC alone
                        return -1
                elif len(key) == 1:
                    if key.lower() == 'w':  # w key - up
                        selected = (selected - 1) % len(options)
                    elif key.lower() == 's':  # s key - down
                        selected = (selected + 1) % len(options)
                    elif key == '\r' or key == '\n':  # Enter
                        return selected
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colours.RED}Thanks for playing Guess the Duck{Colours.RESET}")
        sys.exit()

#----Arrow Key Menu System----#

#------------------------------------#
#============GAME FUNCTIONS==========#
#------------------------------------#

#----Starting Game----#

def start():
    '''Starting game function'''
    clear_screen()
    LINE()
    sys.stdout.write(47 * " ")
    print_tw(f"{Colours.BOLD}Welcome to....\n{Colours.RESET}", 0.05)
    sys.stdout.write(47 * " ")
    print("")
    time.sleep(1)
    print_tw(" ██████╗ ██╗   ██╗███████╗███████╗███████╗    ████████╗██╗  ██╗███████╗    ██████╗ ██╗   ██╗ ██████╗██╗  ██╗\n"
          "██╔════╝ ██║   ██║██╔════╝██╔════╝██╔════╝    ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██║   ██║██╔════╝██║ ██╔╝\n" 
          "██║  ███╗██║   ██║█████╗  ███████╗███████╗       ██║   ███████║█████╗      ██║  ██║██║   ██║██║     █████╔╝ \n" \
          "██║   ██║██║   ██║██╔══╝  ╚════██║╚════██║       ██║   ██╔══██║██╔══╝      ██║  ██║██║   ██║██║     ██╔═██╗ \n" \
          "╚██████╔╝╚██████╔╝███████╗███████║███████║       ██║   ██║  ██║███████╗    ██████╔╝╚██████╔╝╚██████╗██║  ██╗\n" \
          " ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝", 0.001)
    sys.stdout.write(44 * " ")
    print_tw(f"{Colours.BLUE}Created by Duckyboi_XD{Colours.RESET}", 0.001)
    sys.stdout.write(40 * " ")
    print_tw("Created for Hackclub Macondo\n", 0.001)

    print_tw(f"{Colours.BOLD}{Colours.YELLOW}A CLI Python game about guessing every single card in a regular playing card deck.\n"
          f"When you successfully guess a card, it will be removed from the deck{Colours.RESET}\n\n"
          f"No, you are not guessing ducks. Yes, the title is misleading\nI just like ducks and I name every project with 'duck'\n"
          , 0.0005)
    if savefile_value == 0:
        print(f"{Colours.RED}ERRROR=UNASSIGNED SAVEFILE VALUE{Colours.RESET}")
    elif savefile_value == 1:
        print(f"{Colours.GREEN}Save File Loaded{Colours.RESET}")
    elif savefile_value == 2:
        print(f"{Colours.YELLOW}No Save File Loaded - Creating New Save File{Colours.RESET}")
    elif savefile_value == 3:
        print(f"{Colours.RED}Save File Corrupted - Creating New Save File{Colours.RESET}")
    LINE()
    key_press(0)

#----Game Function----#

def guessingcard():
    '''guessing game function'''
    global suit_number_cards
    global number_choice
    global suit_logo_track

    global gc_top
    global gc_top_mid
    global gc_mid
    global gc_bottom_mid
    global gc_bottom
    global GuessCard
    while True:
        suit_choice = arrow_menu(get_title(), 
                f"{Colours.BLACK}♠{Colours.RESET}{Colours.RED}♦{Colours.RESET} Pick the card suit {Colours.BLACK}♣{Colours.RESET}{Colours.RED}♥{Colours.RESET}",
                cardSuits, 0)
        if suit_choice == 0:
            suit_logo = f"{Colours.BLACK}♠{Colours.RESET}"
            suit_number_cards = sSuitNumbers
            card_colour = Colours.BLACK
            suit_logo_track = "♠"
        elif suit_choice == 1:
            suit_logo = f"{Colours.RED}♦{Colours.RESET}"
            suit_number_cards = dSuitNumbers
            card_colour = Colours.RED
            suit_logo_track = "♦"
        elif suit_choice == 2:
            suit_logo = f"{Colours.BLACK}♣{Colours.RESET}"
            suit_number_cards = cSuitNumbers
            card_colour = Colours.BLACK
            suit_logo_track = "♣"
        elif suit_choice == 3:
            suit_logo = f"{Colours.RED}♥{Colours.RESET}"
            suit_number_cards = hSuitNumbers
            card_colour = Colours.RED
            suit_logo_track = "♥"
        else:
            suit_logo = "ERRORRRRRRR!!!^&$#^@*$&^##*@%$@&!&@"
            suit_number_cards = "EERRROORRORO#($&@^%^&*(@*&^%$#*#))"
            card_colour = Colours.BLACK
            suit_logo_track = "ERRRORRORR*&^&*(*&^%$%^&(^@@2134"
            CLI_SW()
        while True:
            number_choice = arrow_menu(get_title(), 
                f"{suit_logo} Pick the card value {suit_logo}",
                suit_number_cards, 1)
            
            number_choice -= 1
            number_choice = suit_number_cards[int(number_choice)]
            if "BACK" in number_choice:
                break

            gc_top = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}╭─────╮{Colours.RESET}"
            if number_choice == "10":
                gc_top_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│ {number_choice}  │{Colours.RESET}"
            else:
                gc_top_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│ {number_choice}   │{Colours.RESET}"
            gc_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│     │{Colours.RESET}"
            gc_bottom_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│   {suit_logo}{Colours.BG_WHITE}{Colours.BOLD}{card_colour} │{Colours.RESET}"
            gc_bottom = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}╰─────╯{Colours.RESET}"

            card_output = f"{gc_top}\n{gc_top_mid}\n{gc_mid}\n{gc_bottom_mid}\n{gc_bottom}"

            confirmation = arrow_menu(get_title(), f"You chose:\n{card_output}", Confirm_Redo, 0 )
            CLI_SW()
            if confirmation == 0:
                GuessCard = f"{number_choice}{suit_logo_track}"
                return
            elif confirmation == 1:
                break

def guess_resolution():
    '''function to check if your guess was correct'''
    global GUESS_PROGRESS
    global CARD_IN_DECK
    global GUESS_DECK_NUMBER
    global GUESS_DECK_PERCENT
    global DECKS_COMPLETE
    global CardDeck
    global suit_number_cards
    global sSuitNumbers
    global cSuitNumbers
    global dSuitNumbers
    global hSuitNumbers


    drawn_card = CardDeck[0]
    if "♠" in drawn_card or "♣" in drawn_card:
        card_colour = Colours.BLACK
    else:
        card_colour = Colours.RED
    
    drawn_card_rank = drawn_card[:-1] # Everything but last character
    drawn_card_suit = drawn_card[-1] # last character (suit
    dc_top = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}╭─────╮{Colours.RESET}"
    if len(drawn_card_rank) == 2:
        dc_top_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│ {drawn_card_rank}  │{Colours.RESET}"
    else:
        dc_top_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│ {drawn_card_rank}   │{Colours.RESET}"
    dc_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│     │{Colours.RESET}"
    dc_bottom_mid = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}│   {drawn_card_suit}{Colours.BG_WHITE}{Colours.BOLD}{card_colour} │{Colours.RESET}"
    dc_bottom = f"{Colours.BG_WHITE}{Colours.BOLD}{card_colour}╰─────╯{Colours.RESET}"

    output_top = f"Card Drawn: {dc_top} │ Card Picked: {gc_top}"
    output_top_mid = f"            {dc_top_mid} │              {gc_top_mid}"
    output_mid = f"            {dc_mid} │              {gc_mid}"
    output_bottom_mid = f"            {dc_bottom_mid} │              {gc_bottom_mid}"
    output_bottom = f"            {dc_bottom} │              {gc_bottom}"

    CardOutput = f"{output_top}\n{output_top_mid}\n{output_mid}\n{output_bottom_mid}\n{output_bottom}\n"

    if str(GuessCard) == str(drawn_card):
        GUESS_PROGRESS += 1
        GUESS_DECK_NUMBER = GUESS_PROGRESS / 52
        CardDeck.remove(str(drawn_card))
        suit_number_cards.remove(str(number_choice))
        GUESS_DECK_PERCENT = round(GUESS_DECK_NUMBER * 100, 2)
        CARD_IN_DECK = len(CardDeck)
        output_print = f"✅{Colours.BOLD}{Colours.GREEN}CONGRATS, you guessed correct{Colours.RESET} ✅"
        keypress_value = 1
    else:
        output_print = f"❌ {Colours.RED}{Colours.BOLD}Sorry, but you guessed wrong{Colours.RESET} ❌"
        CardDeck.append(CardDeck.pop(0))
        keypress_value = 1

    if len(CardDeck) == 0:
        keypress_value = 2
        output_print = f"🎉 {Colours.GREEN}{Colours.BOLD}Congratulations, you have successfully guessed the entire deck of playing card{Colours.RESET} 🎉"
    clear_screen()
    card_loading(2)
    CLI_SW()
    clear_screen()
    LINE()
    print(get_title())
    LINE()
    print(CardOutput)
    print(output_print)
    LINE()
    save_game()
    key_press(keypress_value)
    if len(CardDeck) == 0:
        DECKS_COMPLETE += 1
        CardDeck = temp_CardDeck.copy()
        random.shuffle(CardDeck)
        CARD_IN_DECK = len(CardDeck)
        GUESS_PROGRESS = 0
        GUESS_DECK_NUMBER = GUESS_PROGRESS / 52
        GUESS_DECK_PERCENT = round(GUESS_DECK_NUMBER * 100, 2)
        sSuitNumbers = temp_SuitNumbers.copy()
        cSuitNumbers = temp_SuitNumbers.copy()
        dSuitNumbers = temp_SuitNumbers.copy()
        hSuitNumbers = temp_SuitNumbers.copy()
#----Main Game----#

def main():
    '''main game function'''
    global CARD_IN_DECK
    global GUESS_DECK_NUMBER
    global GUESS_DECK_PERCENT
    clear_screen()
    CLI_SW()
    start()
    CARD_IN_DECK = len(CardDeck)
    GUESS_DECK_NUMBER = GUESS_PROGRESS / 52
    GUESS_DECK_PERCENT = round(GUESS_DECK_NUMBER * 100, 2)
    save_game()
    while True:
        CLI_SW()
        clear_screen()
        guessingcard()
        CLI_SW()
        clear_screen()
        guess_resolution()

#----Main Game----#
main()
