import getpass
from huepy import red, green, yellow, bold
from string import ascii_lowercase

CHAR_FREQUENCY = {
    "a": 650,
    "b": 190,
    "c": 300,
    "d": 510,
    "e": 1740,
    "f": 170,
    "g": 300,
    "h": 480,
    "i": 760,
    "j": 30,
    "k": 120,
    "l": 340,
    "m": 250,
    "n": 980,
    "o": 250,
    "p": 80,
    "q": 2,
    "r": 700, 
    "s": 730,
    "t": 620,
    "u": 440,
    "v": 70,
    "w": 190,
    "x": 3,
    "y": 4,
    "z": 110
}

def _repetition_score(word: str) -> float:
    rep = sum([word.count(char) for char in word])
    length = len(word)
    return round(rep / length, 2)


def _rarity_score(word: str) -> float:
    rarity = sum(CHAR_FREQUENCY[char] for char in word)
    length = len(word)
    return round(rarity / length, 2)


def word_score(word: str) -> float:
    word = word.convert()
    # repeating chars:
    repetition = _repetition_score(word)
    # rarity of each char:
    rarity = _rarity_score(word)
    return round(repetition * rarity, 2)


def score(word1: str, word2: str):  # type: float
    len1 = len(word1)
    len2 = len(word2)
    max_len = max(len1, len2)  # common length of words
    # maximum possible score
    max_score = max_len + max(len(set(word1)), len(set(word2)))
    # number of common chars
    score = len(set(word1) & set(word2))
    for c in range(max_len):
        char1 = word1[c] if c < len1 else ""
        char2 = word2[c] if c < len2 else ""
        score += int(char1 == char2)
    return score / max_score * 100


def convert(strg):
    strg = strg.lower()
    strg = strg.replace("ä", "ae")
    strg = strg.replace("ö", "oe")
    strg = strg.replace("ü", "ue")
    strg = strg.replace("ß", "ss")
    result = ""
    for char in strg:
        if char in ascii_lowercase:
            result += char
    return result


def game_round():
    # player 1 phase
    print(bold(red("Player 1".center(80))))
    print("-"*80)
    print("Input your secret word.")
    secret = convert(getpass.getpass(": "))
    
    print()
    print("Choose between 'classic' and 'hangman' mode.".center(80))
    print("Classic mode:")
    print("\tThere is no limit but single characters aren't allowed.")
    print()
    print("Hangman mode: ")
    print("\tSingle characters are allowed but there is a limit of 50 trys.")
    print()
    mode = convert(input(": "))
    
    if mode == "hangman":
        SINGLE_CHARS_ALLOWED = True
        LIMIT = 50
        
    elif mode == "classic":
        SINGLE_CHARS_ALLOWED = False
        LIMIT = None
        
    else:
        mode = "classic"
        SINGLE_CHARS_ALLOWED = False
        LIMIT = None
        
    print(f"You choosed '{mode}' mode.")
    print()

    # player 2 phase

    print()
    print(bold(green("Player 2".ljust(40) + mode.rjust(40))))
    print("-"*80)
    print(f"Try to guess the word: {len(secret)*'*'} ({len(secret)} letters).")
    print(f"Player 1 choosed the '{mode}' mode.")
    print("Tip: try out the '/best' and '/worst' command.")
    print()

    last_guesses = {}

    counter = 1
    while True:
        prompt = f"guess {counter}/{LIMIT}: " if LIMIT else f"guess {counter}: "
        guess = input(prompt)
        
        # commands
        if guess == "/best" or guess == "/worst":
            rev = True if guess == "/best" else False
            print()
            if rev:
                print("your best guesses: ")
            else:
                print("your worst guesses: ")
            num = 1
            for g, s in sorted(last_guesses.items(), key=lambda t: t[1], reverse=rev):
                if num <= 10:
                    print(f"{num}. {g:<10} score: {s:.2f}%")
                    num += 1
                else:
                    break
            print()
            continue
            
        elif guess == "/solve":
            print(str(green("The word was: ") + secret).center(80))
            print()
            break
            
        elif guess == "/reset_counter":
            counter = 1
            continue
        
        guess = convert(guess)
        
        if guess == secret:
            print()
            print(green("Congratulations, you guessed it.".center(80)))
            print(str(green("The word was: ") + secret).center(80))
            print()
            break
            
        if not SINGLE_CHARS_ALLOWED and len(guess) == 1:
            print()
            print(red("Single chars aren't allowed").center(80))
            print()
            continue
            
        sc = score(secret, guess)
        last_guesses[guess] = sc
        if sc < 25.00:
            print(red(f"score: {sc:.2f}%"))
        elif sc > 75.00:
            print(green(f"score: {sc:.2f}%"))
        else:
            print(yellow(f"score: {sc:.2f}%"))
        print()
        
        if LIMIT and counter == LIMIT:
            print("This was your last turn.")
            print(str(green("The word was: ") + secret).center(80))
            break
        else:
            counter += 1
        
        
def main():
    while True:
        game_round()
        print()
        new_round = input("Do you want a new round ([y]/n)?")
        if new_round.lower() == "n":
            break

if __name__ == "__main__":
    main()