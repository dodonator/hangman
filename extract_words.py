from pathlib import Path
from backend import word_score

LIMIT = 1000
print(f"the limit is {LIMIT}")

path = Path("wordlist.txt")
path_filtered = Path("words.txt")
word_counter = 0
with path.open("r") as fo_r:
    with path_filtered.open("w") as fo_a:
        for line in fo_r:
            word = line.strip()
            score = word_score(word)
            if score <= LIMIT:
                print(f"{score:<8} : {word}")
                fo_a.write(word + "\n")
                word_counter += 1

print(f"\n{word_counter} words extracted")
