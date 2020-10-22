"""Phrase Puzzler main program"""

import random
from typing import Tuple
from puzzler_functions import DATA_FILE, PLAYER_ONE, PLAYER_TWO, CONSONANT, \
 VOWEL_PRICE, CONSONANT_BONUS, VOWEL, SOLVE, QUIT
import puzzler_functions as pf

# Phrase Puzzler constants

# Hidden character symbol
HIDDEN = '^'

# Game types
HUMAN = '1'
HUMAN_HUMAN = '2'
HUMAN_COMPUTER = '3'

# Computer difficulty levels
EASY = 'E'
HARD = 'H'

# Consonant and vowel sets
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'

# The order in which a computer player, hard difficulty, will guess consonants.
PRIORITY_CONSONANTS = 'tnrslhdcmpfygbwvkqxjz'


def get_puzzle() -> str:
    """Return a randomly chosen line from the file named DATA_FILE.

    Docstring examples not given since result depends on input data.
    """

    data_file = open(DATA_FILE)

    phrases = []
    for line in data_file:
        phrases.append(line.strip())

    data_file.close()
    return phrases[random.randint(0, len(phrases) - 1)]


def get_view(puzzle: str) -> str:
    """Return a string that is based on puzzle, with each alphabetic character
    replaced by the HIDDEN character.

    >>> get_view('apple cake is great!')
    '^^^^^ ^^^^ ^^ ^^^^^!'
    >>> get_view('108@#$&!')
    '108@#$&!'
    """

    view = ''
    for char in puzzle:
        if char.isalpha():
            view = view + HIDDEN
        else:
            view = view + char
    return view


def update_view(puzzle: str, view: str, guessed_letter: str) -> str:
    """Return a string that gives a new view of the puzzle. Each occurrence in
    the puzzle of the guessed_letter is revealed.

    >>> update_view('apple', '^^^le', 'a')
    'a^^le'
    >>> update_view('apple', '^^^le', 'z')
    '^^^le'
    """

    new_view = ''
    for i in range(len(puzzle)):
        new_view = new_view \
         + pf.update_letter_view(puzzle, view, i, guessed_letter)
    return new_view

def make_guessed(consonants: str, vowels: str, letter: str) -> Tuple[str]:
    """Return a tuple containing consonants and vowels with letter removed
    from one of them.

    >>> make_guessed('bcd', 'aei', 'c')
    ('bd', 'aei')
    >>> make_guessed('bcd', 'aei', 'a')
    ('bcd', 'ei')
    """

    new_consonants = ''
    for c in consonants:
        if c != letter:
            new_consonants = new_consonants + c

    new_vowels = ''
    for v in vowels:
        if v != letter:
            new_vowels = new_vowels + v

    return (new_consonants, new_vowels)

def finalize_score(puzzle: str, view: str, unguessed_consonants: str, \
    current_score: int) -> int:
    """Return the final score, which is calculated by adding CONSONANT_BONUS
    points to the current_score for each occurrence of each item from 
    unguessed_consonants in puzzle that appears as HIDDEN in view.

    >>> finalize_score('apple pies', '^^^le ^^e^', 'dfkpqstz', 0)
    8
    """

    final_score = current_score
    for letter in unguessed_consonants:
        if pf.bonus_letter(puzzle, view, letter):
            final_score = final_score + CONSONANT_BONUS * puzzle.count(letter)
    return final_score


def update_score(p1_score: int, p2_score: int, new_score: int, \
    current_player: str) -> Tuple[int]:
    """Return player one and player two's updated scores, replacing the score of
    the current_player with new_score.

    >>> update_score(3, 4, 5, PLAYER_ONE)
    (5, 4)
    >>> update_score(3, 4, 3, PLAYER_TWO)
    (3, 3)
    """

    if current_player == PLAYER_ONE:
        return (new_score, p2_score)
    elif current_player == PLAYER_TWO:
        return (p1_score, new_score)


def guess_letter(unguessed_consonants: str, difficulty_level: str) -> str:
    """Return a letter from unguessed_consonants (this function will never 
    return a vowel). If difficulty is EASY, the letter is randomly selected. If
    difficulty is HARD, the letter is the first one from PRIORITY_CONSONANTS 
    that occurs in unguessed_letters.

    Precondition: there is a consonant to return.

    >>> guess_letter('bcdfg', HARD)
    'd'
    """

    if difficulty_level == EASY:
        return random.choice(unguessed_consonants)
    else:
        for c in PRIORITY_CONSONANTS:
            if c in unguessed_consonants:
                return c


def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic characters in
    view are revealed.

    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_alphabetic = 0
    num_revealed = 0
    for char in view:
        if char == HIDDEN or char.isalpha():
            num_alphabetic = num_alphabetic + 1
            if char.isalpha():
                num_revealed = num_revealed + 1
    return (num_revealed * 2) >= num_alphabetic


def is_match(puzzle: str, view: str) -> bool:
    """Return True if and only if view could be a puzzle-view of puzzle.

    >>> is_match('abcde', 'ab^^e')
    True
    >>> is_match('axyzb', 'ab^^e')
    False
    >>> is_match('abcdefg', 'ab^^e')
    False
    >>> is_match('bb', 'b^')
    False
    """

    if len(view) != len(puzzle):
        return False

    hidden = ''
    revealed = ''

    for i in range(len(view)):
        if view[i] != puzzle[i] and view[i] != HIDDEN:
            return False
        if view[i] == puzzle[i] and view[i] not in revealed:
            revealed += view[i]
        if view[i] == HIDDEN and puzzle[i] not in hidden:
            hidden += puzzle[i]

    # if any characters are in both hidden and revealed then return False
    for char in hidden:
        if char in revealed:
            return False

    return True


def prompt_for_game_type() -> str:
    """Prompt for and return the game type.

    Docstring examples not given since result depends on input data.
    """

    game_type = input("""Choose the game type:
     [1] - One Player
     [2] - Two player (human opponent)
     [3] - Two player (computer opponent)\n""").strip()

    while not (game_type == HUMAN \
          or game_type == HUMAN_HUMAN \
          or game_type == HUMAN_COMPUTER):
        game_type = input('Invalid choice.  Enter [1], [2] or [3]: ').strip()
    return game_type


def select_computer_difficulty(game_type: str) -> str:
    """If game_type is HUMAN_COMPUTER, prompt the user to enter the difficulty
    and return it. Otherwise, return None because there is no computer player.

    Docstring examples not given since result depends on input data.
    """

    if game_type == HUMAN_COMPUTER:
        difficulty = input(
            "Enter the game difficulty ([E]asy or [H]ard):  ").strip().upper()

        while difficulty != EASY and difficulty != HARD:
            difficulty = input(
                "Enter the game difficulty ([E]asy or [H]ard):  ")
            difficulty = difficulty.strip().upper()

    else:
        difficulty = None

    return difficulty


def get_player_letter(unguessed_consonants: str, unguessed_vowels: str, \
    move_type: str, _difficulty: str) -> str:
    """Prompt the user to enter either an unguessed consonant or an unguesssed
    vowel based on the move_type, and return the letter. difficulty is
    ignored; it is supplied only because this function must have the same type
    contract as get_computer_letter.

    This function must have the same type contract as get_computer_letter.

    Docstring examples not given since result depends on input data.
    """

    if move_type == CONSONANT:
        letter = input(
            'Please enter a consonant [{0}]: '.format(unguessed_consonants))
        while len(letter) != 1 or letter not in unguessed_consonants:
            letter = input("Invalid choice.  Please enter a consonant: ")
    else:
        letter = input("Please enter a vowel [{0}]: ".format(unguessed_vowels))
        while len(letter) != 1 or letter not in unguessed_vowels:
            letter = input("Invalid choice.  Please enter a vowel: ")

    return letter


def get_computer_letter(unguessed_consonants: str, _unguessed_vowels: str, \
    _move_type: str, difficulty: str) -> str:
    """Return the letter the computer selects from unguessed_consonants based on
    difficulty, which is one of EASY and HARD. unguessed_vowels and
    move_type are ignored; they are supplied only because this function must
    have the same type contract as get_player_letter.

    This function must have the same type contract as get_player_letter.

    Docstring examples not given since result depends on input data.
    """

    return guess_letter(unguessed_consonants, difficulty)


def move_type_is_valid(move_type: str, score: int, unguessed_consonants: str, \
    unguessed_vowels: str) -> bool:
    """Return whether move_type is one of CONSONANT, VOWEL, SOLVE, or
    QUIT. If it's VOWEL, also check whether the player has a high
    enough score to buy a vowel and print a message if they do not.
    For pf.consonant and pf.vowel, ensure that there is something to guess.

    >>> move_type_is_valid(CONSONANT, 2, 'bcdfghjklmnpqstvwxyz', 'aeiou')
    True
    >>> move_type_is_valid(VOWEL, 1, 'bcdfghjklmnpqstvwxyz', 'aeiou')
    True
    """

    valid = move_type == CONSONANT or move_type == VOWEL or \
        move_type == SOLVE or move_type == QUIT

    if move_type == VOWEL and score < VOWEL_PRICE:
        print('You do not have enough points to reveal a vowel. ' \
            'Vowels cost {0} point.'.format(VOWEL_PRICE))
        valid = False

    elif move_type == VOWEL and unguessed_vowels == '':
        print('You do not have any more vowels to guess!')
        valid = False

    elif move_type == CONSONANT and unguessed_consonants == '':
        print('You do not have any more consonants to guess!')
        valid = False

    return valid


def is_human(current_player: str, game_type: str) -> bool:
    """Return True iff current_player represents a human in a game of type
    game_type.

    >>> is_human(PLAYER_ONE, HUMAN_COMPUTER)
    True
    >>> is_human(PLAYER_TWO, HUMAN_HUMAN)
    True
    """

    return current_player == PLAYER_ONE or game_type != HUMAN_COMPUTER


def get_player_move(current_player: int, view: str, _difficulty: str, \
    score: int, unguessed_consonants: str, unguessed_vowels: str) -> str:
    """Prompt current_player to choose the kind of move (CONSONANT, VOWEL,
    SOLVE or QUIT) and return it.

    view is the current state of the puzzle, difficulty and game_type are
    unused (and supplied only because of get_computer_move), score is provided
    for display to the player, and the unguessed_ parameters are the letters
    that have not yet been guessed.

    This function and get_computer_move must have the same type contract.

    Docstring examples not given since result depends on input data.
    """

    print('=' * 50)
    print('{0}, it\'s your turn. You have {1} points.'.format(
        current_player, score))
    print('\n' + view + '\n')
    move_type = input(
        '[C]onsonant, [V]owel, [S]olve, [Q]uit: ').strip().upper()
    while not move_type_is_valid(move_type, score, unguessed_consonants, \
        unguessed_vowels):
        print('Invalid input.')
        move_type = input(
            '[C]onsonant, [V]owel, [S]olve, [Q]uit: ').strip().upper()

    return move_type


def get_computer_move(_current_player: int, view: str, difficulty: str, \
    score: int, unguessed_consonants: str, _unguessed_vowels: str) -> str:
    """ Return the computer's next move, which will be either to guess a
    CONSONANT or to SOLVE. The computer chooses to solve when difficulty
    is HARD, at least half of the letters in the puzzle have been revealed
    and there is a valid guess (according to guess_puzzle), otherwise the
    computer opts to guess a CONSONANT.

    This function and get_player_move must have the same type contract.
    current_player and unguessed_vowels are unused.
    """

    print('=' * 50)
    print('Computer, it\'s your turn. You have {0} points.'.format(
        score))
    print('\n' + view + '\n')
    print('[C]onsonant, [V]owel, [S]olve, [Q]uit: ')
    guess = get_computer_guess(view)
    if (difficulty == HARD and half_revealed(view) \
       and guess != '') or unguessed_consonants == '':
        print('The Computer chooses to try to solve.')
        print('The computer guesses "{0}"'.format(guess))
        return SOLVE

    return CONSONANT


def get_player_guess(_view: str) -> str:
    """Ask the player for a guess and return it. view is ignored (and is 
    supplied because get_computer_guess requires it).

    This function and get_computer_guess must have the same type contract.

    Docstring examples not given since result depends on input data.
    """

    return input("Please enter your guess: ")


def get_computer_guess(view: str) -> str:
    """Return a line from the file named DATA_FILE that contains string that
    could be represented by view, or, if no such line exists, the empty
    string.

    This function and get_player_guess must have the same type contract.
    """

    data_file = open(DATA_FILE)
    for line in data_file:
        if is_match(line.strip(), view):
            return line.strip()

    return ''


def play_game(puzzle: str, view: str, game_type: str) -> None:
    """Prompt the player(s) to try to guess the puzzle. game_type is one of
    HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.
    Return whether there was a winner and the final score.
    """

    player_one_score = 0
    player_two_score = 0
    current_player = PLAYER_ONE

    # The player move choice; will be one of CONSONANT, VOWEL,
    # SOLVE and QUIT.
    move_type = ''

    # The letters that have not yet been guessed.
    unguessed_consonants = CONSONANTS
    unguessed_vowels = VOWELS

    # This is None if there is no computer player.
    difficulty = select_computer_difficulty(game_type)

    # Note: you may find it helpful to display the solution while you
    # are testing. To do this, uncomment the following line:
    #print('Solution: {0}'.format(puzzle))

    while not pf.game_over(puzzle, view, move_type):
        quantity = 0
        if current_player == PLAYER_ONE:
            score = player_one_score
        else:
            score = player_two_score

        # Set up function aliases based on whether it's a human's turn or a
        # computer's turn.
        if is_human(current_player, game_type):
            get_move = get_player_move
            get_guess = get_player_guess
            get_letter = get_player_letter
        else:
            get_move = get_computer_move
            get_guess = get_computer_guess
            get_letter = get_computer_letter

        move_type = get_move(current_player, view, difficulty, \
            score, unguessed_consonants, unguessed_vowels)

        if move_type == SOLVE:

            guess = get_guess(view)
            if guess == puzzle:
                score = finalize_score(puzzle, view, \
                    unguessed_consonants, score)
                view = puzzle
            else:
                print("The guess '{0}' is Incorrect :-(".format(guess))

        elif move_type == CONSONANT or move_type == VOWEL:

            letter = get_letter(
                unguessed_consonants, unguessed_vowels, move_type, difficulty)

            quantity = puzzle.count(letter)
            view = update_view(puzzle, view, letter)
            score = pf.calculate_score(score, quantity, move_type)
            unguessed_consonants, unguessed_vowels = make_guessed(
                unguessed_consonants, unguessed_vowels, letter)

            print('The guess was {0}, which occurs {1} time(s).  '\
                  .format(letter, quantity), end='')
            print('Your score is {0}.'.format(score))

            player_one_score, player_two_score = update_score(player_one_score,\
             player_two_score, score, current_player)

        if game_type != HUMAN:
            current_player = pf.next_player(current_player, quantity)

    # The game is over.
    display_outcome(pf.is_win(view, puzzle), score)


def display_outcome(won: bool, score: int) -> None:
    """Display a message indicating whether the player won and, if so, their
    score.

    >>> display_outcome(True, 4)
    Winner! You scored 4 point(s).
    """

    if won:
        print("Winner! You scored {0} point(s).".format(score))
    else:
        print("Better luck next time!")


if __name__ == '__main__':

    ## The main Phrase Puzzler program
    phrase_puzzle = get_puzzle()
    phrase_view = get_view(phrase_puzzle)

    print('Welcome to Phrase Puzzler!')
    phrase_game = prompt_for_game_type()
    play_game(phrase_puzzle, phrase_view, phrase_game)
