import sys
sys.path.insert(0, 'pyta')

print("================= Start: checking coding style =================")

# import python_ta
# python_ta.check_all('puzzler_functions.py', config='pyta/a1_pyta.txt')

# print("================= End: checking coding style =================\n")


# print("================= Start: checking parameter and return types =================")

import puzzler_functions as pf

# Get the initial values of the constants
constants_before = [pf.DATA_FILE, pf.VOWEL_PRICE, pf.CONSONANT_BONUS,  
                   pf.CONSONANT_POINTS, pf.PLAYER_ONE, pf.PLAYER_TWO, pf.CONSONANT,
                   pf.VOWEL, pf.SOLVE, pf.QUIT]

# Type check puzzler_functions.is_win
print('Checking is_win...')
result = pf.is_win('apple', 'about')
assert isinstance(result, bool), \
       """puzzler_functions.is_win should return a bool, but returned {0}
       .""".format(type(result))
print('  check complete')


# Type check puzzler_functions.game_over
print('Checking game_over...')
result = pf.game_over('water', '^^te^', pf.CONSONANT)
assert isinstance(result, bool), \
       """puzzler_functions.game_over should return a bool, but returned {0}.""" \
       .format(type(result))
print('  check complete')


# Type check puzzler_functions.bonus_letter
print('Checking bonus_letter...')
result = pf.bonus_letter('water', '^^te^', 'w')
assert isinstance(result, bool), \
       """puzzler_functions.bonus_letter should return a bool, but returned {0}.""" \
       .format(type(result))
print('  check complete')


# Type check puzzler_functions.update_letter_view
print('Checking update_letter_view...')
result = pf.update_letter_view('apple', 'a^^l^', 2, 'x')
assert isinstance(result, str), \
       """puzzler_functions.update_letter_view should return a str, but returned {0}.""" \
       .format(type(result))
print('  check complete')


# Type check pf.calculate_score
print('Checking calculate_score...')
result = pf.calculate_score(4, 2, pf.CONSONANT)
assert isinstance(result, int), \
       """pf.calculate_score should return an int, but returned {0}.""" \
       .format(type(result))
print('  check complete')


# Type check pf.next_player
print('Checking next_player...')
result = pf.next_player(pf.PLAYER_ONE, 2)
assert isinstance(result, str), \
       """pf.next_player should return a str, but returned {0}.""" \
       .format(type(result))
print('  check complete')
print("================= End: checking parameter and return types =================\n")


print("================= Start: checking whether constants are unchanged =================")

# Get the final values of the constants
constants_after = [pf.DATA_FILE, pf.VOWEL_PRICE, pf.CONSONANT_BONUS,  
                   pf.CONSONANT_POINTS, pf.PLAYER_ONE, pf.PLAYER_TWO, pf.CONSONANT,
                   pf.VOWEL, pf.SOLVE, pf.QUIT]

# Check whether the constants are unchanged.
print('Checking constants...')
assert constants_before == constants_after, \
       """Your function(s) modified the value of a constant(s). Edit your code
        so that the values of constants are unchanged by your functions."""
print('  check complete')    
print("================= End: checking whether constants are unchanged =================")

