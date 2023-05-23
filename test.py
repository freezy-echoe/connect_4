import unittest
from main import Player
from main import Disc
from main import Board
import main


class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(1, main.RED)
        self.player2 = Player(2, main.YELLOW)
        self.disc1 = Disc(self.player1)
        self.disc2 = Disc(self.player2)
        self.board = Board(main.ROW_COUNT, main.COLUMN_COUNT)

    def test_player_creation(self):
        self.assertEqual(self.player1.id, 1)
        self.assertEqual(self.player1.color, main.RED)
        self.assertEqual(self.player2.id, 2)
        self.assertEqual(self.player2.color, main.YELLOW)

    def test_disc_creation(self):
        self.assertEqual(self.disc1.player, self.player1)
        self.assertEqual(self.disc2.player, self.player2)

    def test_board_creation(self):
        self.assertEqual(self.board.row_count, main.ROW_COUNT)
        self.assertEqual(self.board.column_count, main.COLUMN_COUNT)


if __name__ == "__main__":
    unittest.main()
# reference for unit test https://youtu.be/tIrcxwLqzjQ
