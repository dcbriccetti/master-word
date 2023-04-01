from random import choice
from string import ascii_lowercase
from typing import Optional, Iterator

from colorama import Fore
from words import words_from_file

WORD_LENGTH = 5

def play() -> None:
    hint_commands = ('h', 'hint')
    CountAndWord = tuple[int, str]

    def find_hint() -> Optional[str]:
        'Return a hint based on the hits and misses without considering the actual word to be guessed.'

        def words_with_hits() -> Iterator[CountAndWord]:
            'Yield the number of hits and the corresponding word for each word with at least one hit and no mismatches.'

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
        'Return a string of the alphabet’s letters colored according to their status in hits, misses, or unknown.'

        def colored_char(char: str) -> str:
            'Return the input character with an appropriate color based on its presence in hits or misses.'
            color = (
                Fore.GREEN if char in hits
                else Fore.RED if char in misses
                else Fore.LIGHTBLACK_EX
            )
            return color + char

        return ''.join(colored_char(char) for char in ascii_lowercase)

    def get_valid_answer() -> str:
        'Get a valid answer from the user, ensuring it has the correct length and is in the word list.'

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
        'Display the output pattern with the appropriate colors for matched and unmatched letters.'

        for word_letter, answer_letter in zip(word, answer):
            (hits if answer_letter in word else misses).add(answer_letter)
            colored_char = (
                Fore.GREEN + word_letter if word_letter == answer_letter
                else Fore.YELLOW + answer_letter if answer_letter in word
                else Fore.WHITE + '*'
            )
            print(colored_char, end='')
        print()

    # Create lists of common and many words by reading from respective files
    common_words, many_words = [list(words_from_file(f'resources/{name}.txt', word_length=WORD_LENGTH))
                                for name in ['common-words', 'many-words']]

    # Choose a random word from common_words as the target word
    word = choice(common_words)

    # Print the chosen word (for debugging purposes)
    print('Shhh... the word is', word)

    # Initialize the answer, hits, and misses
    answer: Optional[str] = None
    hits: set[str] = set()
    misses: set[str] = set()

    # Keep playing until the user guesses the correct word
    while answer != word:
        # Get a valid answer from the user
        answer = get_valid_answer()

        # If the user requested a hint, display it
        if answer in hint_commands:
            hint = find_hint()
            print(Fore.BLUE + hint if hint else 'No hints yet')
        else:
            # Show the output pattern with the appropriate colors for matched and unmatched letters
            show_output_pattern()

if __name__ == '__main__':
    play()
