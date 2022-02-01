import random
import re

from argparse import ArgumentParser

def check_match(word, target):
    exact_match = [char_w if char_w == char_t else None for char_w, char_t in zip(word, target)]
    offset_match = [char if char in target else None for char in word]
    return exact_match, offset_match

def check_valid(next_word, exact_match, offset_match):
    for char_w, char_e, char_o in zip(next_word, exact_match, offset_match):
        if char_e != None and char_e != char_w:
            return False
        if char_o != None and char_o not in next_word:
            return False
    return True

def get_vocab(path, word_len):
    vocab_list = []
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not re.match("^\[.*\]$|^##", line) and len(line) == word_len:
                vocab_list.append(line)
    return vocab_list

def wordle(vocab_list, num_guesses, target):
    vocab_size = len(vocab_list)
    selected_word = []
    for i in range(num_guesses):
        word = random.choice(vocab_list)
        selected_word.append(word)

        exact_match, offset_match = check_match(word, target)
        vocab_list = [next_word  for next_word in vocab_list if check_valid(next_word, exact_match, offset_match) and next_word not in selected_word]        

        if word == target:
            print(f"Guessed from {vocab_size} words and succeeded in {i+1} guess(es). Guessed words: {selected_word}. Remaining words: {vocab_list}.")
            return True
    
    print(f"Guessed from {vocab_size} words and failed in {num_guesses} guess(es). Guessed words: {selected_word}. Remaining words: {vocab_list}.")
    return False

def main(args):
    vocab_list = get_vocab(args.vocab_path, args.num_chars)
    
    successes = sum([wordle(vocab_list, args.num_guesses, args.target) for _ in range(args.num_runs)])
    print(f"{successes}/{args.num_runs} succeeded!")
    
if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("--target", type=str, required=True)
    parser.add_argument("--num_chars", type=int, default=5)
    parser.add_argument("--num_guesses", type=int, default=6)
    parser.add_argument("--num_runs", type=int, default=1)
    parser.add_argument("--vocab_path", type=str, default="vocab.txt")

    args = parser.parse_args()
    main(args)