import getpass
from huepy import red, green, yellow, bold
from backend import convert, score, word_score, word_sample
from typing import Dict


SIZE = 1000
LIMIT = 1000


def get_gamemode() -> str:
    print()
    print("-"*80)
    print("Choose between 'PvC' and 'PvP' mode.".center(80))
    print("PvC mode:")
    print("\tYou play against the computer in 'classic' mode.")
    print()
    print("PvP mode: ")
    print("\tYou play against other local players in two different modes.")
    print()
    gamemode = convert(input(": "))
    if gamemode == "pvp":
        return "pvp"
    else:
        return "pvc"


def pvc_round(secret):
    guess_limit = 20
    print()
    print(bold(green("Player 1".center(80))))
    print(f"Try to guess the word: {len(secret)*'*'} ({len(secret)} letters).")
    print(f"The secret word has a score of {word_score(secret)}")
    print()

    right = set()
    wrong = set()
    counter = 0
    while counter < guess_limit:
        counter += 1
        guess = input(f"guess {counter}/{guess_limit}: ")
        
        # commands
        if guess == "/true":
            print()
            print("The secret word contains:")
            print(green(", ".join(list(sorted(right)))))
            print()
            continue

        elif guess == "/false":
            print()
            print("The secret word does not contain:")
            print(red(", ".join(list(sorted(wrong)))))
            print()
            continue

        elif guess == "/solve":
            print(str(green("The word was: ") + secret).center(80))
            print()
            return 0
        
        guess = convert(guess)
        
        if guess == secret:
            print()
            print(green("Congratulations, you guessed it.".center(80)))
            print(str(green("The word was: ") + secret).center(80))
            print()
            return word_score(secret)
            
        if len(guess) == 1:
            guess = guess.upper()
            if guess in secret.upper():
                right.add(guess)
            else:
                wrong.add(guess)
        else:
            print(red("Sorry, but that was wrong.".center(80)))
            continue

        if right == set(secret.upper()):
            print()
            print(green("Congratulations, you guessed it.".center(80)))
            print(str(green("The word was: ") + secret).center(80))
            print()
            return word_score(secret)

        result = "".join([char if char in right else "*" for char in secret.upper()])
        print()
        print(result)
        print()     
        


def pvp_round(player1: str, player2:str):
    
    # player 2 phase
    print(bold(red(player2.center(80))))
    print("-"*80)
    print("Input your secret word.")
    secret = convert(getpass.getpass(": "))
    
    # choose mode
    print()
    print(bold(green(player1)))
    print("-"*80)
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
        
    else:
        mode = "classic"
        SINGLE_CHARS_ALLOWED = False
        LIMIT = None
        
    print(f"You choosed '{mode}' mode.")
    print()

    # player 1 guess phase

    print()
    print()
    print(bold(green(player1.ljust(40) + mode.rjust(40))))
    print(f"Try to guess the word: {len(secret)*'*'} ({len(secret)} letters).")
    print(f"You choosed the '{mode}' mode.")
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
            return 0
            
        elif guess == "/reset_counter":
            counter = 1
            continue
        
        guess = convert(guess)
        
        if guess == secret:
            print()
            print(green("Congratulations, you guessed it.".center(80)))
            print(str(green("The word was: ") + secret).center(80))
            print()
            return word_score(secret)
            
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
            return 0
        else:
            counter += 1


def PvP():
    player1 = input("Player 1: ").capitalize()
    player2 = input("Player 2: ").capitalize()
    while True:
        pvp_round(player1, player2)
        if input("new round [y/n]?").lower() == "n":
            break
        player1, player2 = player2, player1

def PvC():
    sample = word_sample(SIZE, LIMIT)
    word_counter = 0
    win_counter = 0
    total_score = 0
    for word, score in sample:
        word_counter += 1
        del score
        print()
        print(f"Your current score is: {total_score:.2f}%.")
        print()
        win_counter += bool(pvc_round(word))
        total_score = (win_counter / word_counter) * 100
        if input("new round [y/n]?").lower() == "n":
            return
        
        
def main():
    game_mode = get_gamemode()
    if game_mode == "pvc":
        PvC()
    elif game_mode == "pvp":
        PvP()
    else:
        raise Exception("Wrong input!")


if __name__ == "__main__":
    main()