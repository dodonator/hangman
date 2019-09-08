from pathlib import Path
from backend import word_score
import random


def word_sample(number=1000, limit=1000):
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
