"""Phrase Puzzler: functions"""

# Phrase Puzzler constants 常量

# Name of file containing puzzles 拼图文件名
DATA_FILE = 'puzzles_small.txt'

# Letter values 字母值
CONSONANT_POINTS = 1
VOWEL_PRICE = 1
CONSONANT_BONUS = 2

# Players' names 玩家名
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# Menu options - includes letter types 菜单选项——包括字母类型
CONSONANT = 'C'
VOWEL = 'V'
SOLVE = 'S'
QUIT = 'Q'


# Define your functions here.

def is_win(puzzle: str, view: str) -> bool:
    """Return True if and only if puzzle is the same as view.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('apple', 'a^^le')
    False
    """
    # put the function body here
    return puzzle == view

def game_over(puzzle: str, view: str, selection: str) -> bool:
    """Return True if and only if the puzzle is the same as view
       or the current selection is QUIT
    """

    return puzzle == view or selection == 'Q'

def bonus_letter(puzzle: str, view: str, letter: str) -> bool:
    """Return True if and only if the letter appears in the puzzle
       but not in its view
    """

    return letter in puzzle and letter not in view

def update_letter_view(puzzle: str, view: str, index: int, letter: str) -> str:
    """ 
       if puzzle[index] == letter, return puzzle[index],else,return view[index]
    """

    if puzzle[index] == letter:
        return puzzle[index]
    return view[index]

def calculate_score(score: int, number: int, letter: str) -> int:
    """if letter == consonant，return new score，the new score is the adding from CONSONANT_POINTS
       if letter == vowel，return new score，the new score is the deducting score from VOWEL_PRICE
       the first 1 is CONSONANT_POINTS,the second 1 is VOWEL_PRICE
    """
    if letter == 'C':
        score = score + 1 * number
        return score
    elif letter == 'V':
        score = score - 1 * number
        return score

def next_player(player: str, number: int) -> str:
    """if and only if the number of occurrences is greater than zero, the current player plays again.
        return the next player.
    """
    if player == 'Player One':
        if number > 0 :
            return 'Player One'
        return 'Player Two'
    elif player == 'Player Two':
        if number > 0:
            return 'Player Two'
        return 'Player One'