import getpass
from huepy import red, green, yellow, bold
from backend import convert, score


def game_round_old():
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


def game_round(player1: str, player2:str="JARVIS"):
    # player1 chooses the mode and guesses
    # player2 chooses the word
    if player2 == "JARVIS":
        pass
    else:
        # player 2 phase
        print(bold(red(player2.center(80))))
        print("-"*80)
        print("Input your secret word.")
        secret = convert(getpass.getpass(": "))
    
    # choose mode
    print()
    print(bold(green(player1.ljust(40))))
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
        
    elif mode == "classic":
        SINGLE_CHARS_ALLOWED = False
        LIMIT = None
        
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

        
def main():
    while True:
        game_round()
        print()
        new_round = input("Do you want a new round ([y]/n)?")
        if new_round.lower() == "n":
            break

if __name__ == "__main__":
    main()