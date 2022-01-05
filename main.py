from io import StringIO
from random import choice
from colorama import Fore
from words import words_from_file

WORD_LENGTH = 5

def letter_status() -> str:
    buf = StringIO()
    for ascii_code in range(ord('a'), ord('z') + 1):
        char = chr(ascii_code)
        color = Fore.GREEN if char in hits \
            else Fore.RED if char in misses \
            else Fore.WHITE
        buf.write(color)
        buf.write(char)
    return buf.getvalue()

common5, all5 = [list(words_from_file(fn, word_length=WORD_LENGTH))
                 for fn in ('resources/common-words.txt',
                            'resources/many-words.txt')]
word = choice(common5)
print('Shhh... the word is', word)
answer: None | str = None
hits: set[str] = set()
misses: set[str] = set()

while answer != word:
    letter_status()
    print(Fore.WHITE, end='')
    answer = input(letter_status() + Fore.LIGHTWHITE_EX + ' ➜ ' + Fore.WHITE)
    if len(answer) == WORD_LENGTH:
        if answer not in all5:
            print(Fore.RED + 'Not in word list')
        else:
            for word_letter, answer_letter in zip(word, answer):
                display_color, display_char = (Fore.GREEN, word_letter) if word_letter == answer_letter \
                    else (Fore.YELLOW, answer_letter) if answer_letter in word \
                    else (Fore.WHITE, '*')
                if answer_letter in word:
                    hits.add(answer_letter)
                else:
                    misses.add(answer_letter)
                print(display_color + display_char, end='')
            print()
