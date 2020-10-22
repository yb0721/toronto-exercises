import unittest
import puzzler_functions as pf

class TestPuzzler(unittest.TestCase):
    """测试puzzler内的函数"""

    def test_is_win(self):
        """测试函数is_win"""

        expected = False
        result = pf.is_win('apple', 'about')
        self.assertEqual(expected,result)

    def test_game_over(self):
        """测试函数game_over"""

        expected = False
        result = pf.game_over('water', '^^te^', pf.CONSONANT)
        self.assertEqual(expected,result)
        
unittest.main()