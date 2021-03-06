from string import ascii_lowercase
from typing import List
from pathlib import Path
from tqdm import tqdm
import random

__all__ = [
    "word_sample",
    "word_score",
    "compare_score",
    "delete_words",
    "convert"
    ]

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
    word = convert(word)
    # repeating chars:
    repetition = _repetition_score(word)
    # rarity of each char:
    rarity = _rarity_score(word)
    return round(repetition * rarity, 2)


def compare_score(word1: str, word2: str) -> float:
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


def word_sample(size: int, limit: int) -> List:
    path = Path("words.txt")

    wordlist: List = []
    with path.open("r") as fo:
        for line in tqdm(fo):
            if len(wordlist) < size:
                word = line.strip()
                word = convert(word)
                score = word_score(word)
                r = int(random.random() * limit)
                if int(score) == r:
                    wordlist.append((word, score))

    wordlist.sort(key=lambda x: x[1], reverse=True)
    return wordlist


def delete_words(wordlist: List) -> None:
    path = Path("wordlist.txt")
    path_tmp = Path("tmp.txt")
    path_tmp.touch()

    wordlist.sort()

    counter = 0
    with path.open("r") as fo_r:
        with path_tmp.open("w") as fo_w:
            step = 0
            while wordlist:
                pos = fo_r.tell()
                current = wordlist[0].lower()
                line = fo_r.readline().lower().strip()
                if line == current:
                    word = wordlist.pop(0)
                    print(f"{counter:<5} deleting: {word.strip()} @ {pos}")
                    counter += 1
                    continue
                else:
                    fo_w.write(line)
                    print(f"pos: {pos}")
                step = (ord(current[0]) - ord(line[0].lower())) * 10
                # skip some lines
                for i in range(step):
                    fo_r.readline()

    print(f"deleted {counter} lines")
    path_tmp.replace(path)
