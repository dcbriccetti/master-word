from random import choice
from typing import Optional, Iterator

from colorama import Fore
from words import words_from_file

WORD_LENGTH = 5

def play() -> None:
    hint_commands = ('h', 'hint')
    CountAndWord = tuple[int, str]

    def find_hint() -> Optional[str]:
        'Without any reference to the actual word to be guessed, but only considering hits and misses, return a hint'

        def words_with_hits() -> Iterator[CountAndWord]:
            'For every word with at least one hit and no mismatches, return the number of hits and the word'

            for word in common_words:
                letters = set(word)
                num_matches = len(letters & hits)
                mismatches = letters & misses
                if num_matches and not mismatches:
                    yield num_matches, word

        count_and_words = list(words_with_hits())
        count_and_words.sort(reverse=True)
        best_words: list[str] = [word for count, word in count_and_words
                                 if count == count_and_words[0][0]]
        return choice(best_words) if best_words else None

    def colored_alphabet(hits: set[str], misses: set[str]) -> str:
        'Return a string of the letters of the alphabet colored by hit, miss, unknown'
        def color_and_char(ascii_code: int) -> str:
            char = chr(ascii_code)
            color = Fore.GREEN if char in hits \
                else Fore.RED if char in misses \
                else Fore.LIGHTBLACK_EX
            return color + char

        return ''.join(color_and_char(ascii_code) for ascii_code in range(ord('a'), ord('z') + 1))

    def get_valid_answer() -> str:
        answer: Optional[str] = None
        while not answer:
            prompt = colored_alphabet(hits, misses) + Fore.LIGHTWHITE_EX + ' ➜ ' + Fore.WHITE
            response = input(prompt)
            if response in hint_commands:
                return response
            if len(response) != WORD_LENGTH:
                print(Fore.WHITE + f'Your answer must have {WORD_LENGTH} letters')
            elif response not in many_words:
                print(Fore.WHITE + 'Not in word list')
            else:
                answer = response
        return answer

    def show_output_pattern() -> None:
        for word_letter, answer_letter in zip(word, answer):
            [misses, hits][answer_letter in word].add(answer_letter)
            display_color, display_char = \
                (Fore.GREEN, word_letter) if word_letter == answer_letter \
                else (Fore.YELLOW, answer_letter) if answer_letter in word \
                else (Fore.WHITE, '*')
            print(display_color + display_char, end='')
        print()

    common_words, many_words = [list(words_from_file(f'resources/{name}.txt', word_length=WORD_LENGTH))
                                for name in ('common-words', 'many-words')]
    word = choice(common_words)
    print('Shhh... the word is', word)
    answer: Optional[str] = None
    hits: set[str] = set()
    misses: set[str] = set()

    while answer != word:
        answer = get_valid_answer()
        if answer in hint_commands:
            hint = find_hint()
            print(Fore.BLUE + hint if hint else 'No hints yet')
        else:
            show_output_pattern()

if __name__ == '__main__':
    play()
