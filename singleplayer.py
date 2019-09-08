from pathlib import Path
from backend import word_score, convert
from typing import List
import random


SIZE = 1000
LIMIT = 1000

def word_sample(size:int=SIZE, limit:int=LIMIT) -> List[str]:
    path = Path("words.txt")

    wordlist = []
    with path.open("r") as fo_r:
        for line in fo_r:
            if len(wordlist) < number:
                word = line.strip()
                score = word_score(word)
                r = int(random.random() * limit)
                if int(score) == r:
                    wordlist.append((word, score))

    wordlist.sort(key=lambda x: x[1], reverse=True)
    return wordlist


def game():
    score = 0
    sample = word_sample()

    for word in sample:
        score += game_round(word)
        answer = input("Do you want to continue [y,n]? ")
        if answer.lower() == "n":
            exit()
