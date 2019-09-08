from pathlib import Path
from backend import word_score, convert
from typing import List
import random

def game():
    score = 0
    sample = word_sample()

    for word in sample:
        score += game_round(word)
        answer = input("Do you want to continue [y,n]? ")
        if answer.lower() == "n":
            exit()
