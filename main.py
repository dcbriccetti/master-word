from random import choice
from colorama import Fore
from words import words_from_file

WORD_LENGTH = 5

def play() -> None:
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
        answer: str | None = None
        while not answer:
            prompt = colored_alphabet(hits, misses) + Fore.LIGHTWHITE_EX + ' ➜ ' + Fore.WHITE
            response = input(prompt)
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
    answer: None | str = None
    hits: set[str] = set()
    misses: set[str] = set()

    while answer != word:
        answer = get_valid_answer()
        show_output_pattern()

if __name__ == '__main__':
    play()
