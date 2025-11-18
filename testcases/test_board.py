"""
測試遊戲板 (Board) 的基本功能
"""
import unittest
from core.board import Board


class TestBoard(unittest.TestCase):
    """測試 Board 類別"""
    
    def setUp(self):
        """每個測試前的設置"""
        # 使用固定種子以便測試可重現
        import random
        random.seed(42)
    
    def test_board_initialization(self):
        """測試遊戲板初始化"""
        board = Board(9, 9, 10)
        
        self.assertEqual(board.rows, 9)
        self.assertEqual(board.cols, 9)
        self.assertEqual(board.num_mines, 10)
        self.assertIsNotNone(board.mine_grid)
        self.assertIsNotNone(board.state_grid)
    
    def test_first_click_safety(self):
        """測試第一次點擊不會是地雷"""
        # 測試多次，確保第一次點擊位置不會是地雷
        for _ in range(10):
            board = Board(9, 9, 10, first_click=(4, 4))
            self.assertFalse(board.is_mine(4, 4), "第一次點擊位置不應該是地雷")
    
    def test_mine_count(self):
        """測試地雷數量正確"""
        board = Board(9, 9, 10)
        mine_count = sum(1 for r in range(9) for c in range(9) if board.is_mine(r, c))
        self.assertEqual(mine_count, 10, f"地雷數量應該是 10，實際是 {mine_count}")
    
    def test_cell_numbers(self):
        """測試數字格子的計算"""
        board = Board(9, 9, 10)
        
        # 檢查所有非地雷格子的數字是否正確
        for r in range(9):
            for c in range(9):
                if not board.is_mine(r, c):
                    value = board.get_cell_value(r, c)
                    self.assertGreaterEqual(value, 0)
                    self.assertLessEqual(value, 8)
    
    def test_reveal_cell(self):
        """測試揭開格子"""
        board = Board(9, 9, 10, first_click=(0, 0))
        
        # 揭開一個格子
        result = board.reveal_cell(0, 0)
        self.assertTrue(result, "應該成功揭開格子")
        self.assertTrue(board.is_revealed(0, 0), "格子應該被標記為已揭開")
    
    def test_reveal_mine(self):
        """測試揭開地雷"""
        board = Board(9, 9, 10, first_click=(0, 0))
        
        # 找到一個地雷（不是第一次點擊的位置）
        mine_found = False
        for r in range(9):
            for c in range(9):
                if (r, c) != (0, 0) and board.is_mine(r, c):
                    result = board.reveal_cell(r, c)
                    self.assertFalse(result, "揭開地雷應該返回 False")
                    self.assertTrue(board.is_revealed(r, c), "地雷應該被標記為已揭開")
                    mine_found = True
                    break
            if mine_found:
                break
        
        self.assertTrue(mine_found, "應該能找到地雷")
    
    def test_reveal_empty_auto_expand(self):
        """測試揭開空白格子時自動展開"""
        # 建立一個小棋盤，確保有空白區域
        board = Board(5, 5, 2, first_click=(2, 2))
        
        # 揭開中心位置（通常是空白）
        board.reveal_cell(2, 2)
        
        # 檢查周圍是否也被自動揭開（如果是空白）
        revealed_count = sum(1 for r in range(5) for c in range(5) if board.is_revealed(r, c))
        self.assertGreater(revealed_count, 1, "空白區域應該自動展開")
    
    def test_flag_cell(self):
        """測試標記格子"""
        board = Board(9, 9, 10)
        
        # 標記一個格子
        result = board.toggle_flag(0, 0)
        self.assertTrue(result, "應該成功標記")
        self.assertTrue(board.is_flagged(0, 0), "格子應該被標記")
        
        # 取消標記
        result = board.toggle_flag(0, 0)
        self.assertFalse(result, "應該成功取消標記")
        self.assertFalse(board.is_flagged(0, 0), "格子應該不再被標記")
    
    def test_flag_revealed_cell(self):
        """測試不能標記已揭開的格子"""
        board = Board(9, 9, 10, first_click=(0, 0))
        
        # 先揭開格子
        board.reveal_cell(0, 0)
        self.assertTrue(board.is_revealed(0, 0))
        
        # 嘗試標記已揭開的格子（應該失敗）
        initial_state = board.state_grid[0][0]
        board.toggle_flag(0, 0)
        # 狀態不應該改變
        self.assertEqual(board.state_grid[0][0], initial_state)
    
    def test_get_neighbors(self):
        """測試取得鄰居格子"""
        board = Board(9, 9, 10)
        
        # 中心位置的鄰居應該有 8 個
        neighbors = board.get_neighbors(4, 4)
        self.assertEqual(len(neighbors), 8)
        
        # 角落位置的鄰居應該有 3 個
        neighbors = board.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 3)
        
        # 邊緣位置的鄰居應該有 5 個
        neighbors = board.get_neighbors(0, 4)
        self.assertEqual(len(neighbors), 5)
    
    def test_check_win(self):
        """測試勝利判斷"""
        board = Board(3, 3, 2, first_click=(0, 0))
        
        # 揭開所有非地雷格子
        for r in range(3):
            for c in range(3):
                if not board.is_mine(r, c):
                    board.reveal_cell(r, c)
        
        self.assertTrue(board.check_win(), "應該判斷為勝利")
    
    def test_get_flagged_count(self):
        """測試取得標記數量"""
        board = Board(9, 9, 10)
        
        # 標記幾個格子
        board.toggle_flag(0, 0)
        board.toggle_flag(0, 1)
        board.toggle_flag(0, 2)
        
        self.assertEqual(board.get_flagged_count(), 3)
    
    def test_get_revealed_count(self):
        """測試取得已揭開數量"""
        board = Board(9, 9, 10, first_click=(0, 0))
        
        # 揭開幾個格子
        board.reveal_cell(0, 0)
        board.reveal_cell(0, 1)
        
        revealed = board.get_revealed_count()
        self.assertGreaterEqual(revealed, 2)


if __name__ == '__main__':
    unittest.main()

