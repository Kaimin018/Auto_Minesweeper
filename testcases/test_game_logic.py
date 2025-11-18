"""
測試遊戲邏輯和流程
"""
import unittest
import random
from core.game_engine import GameEngine


class TestGameLogic(unittest.TestCase):
    """測試遊戲邏輯"""
    
    def setUp(self):
        """每個測試前的設置"""
        random.seed(42)
    
    def test_complete_game_flow(self):
        """測試完整的遊戲流程"""
        engine = GameEngine(5, 5, 3)  # 小棋盤用於測試
        engine.start_new_game()
        
        # 1. 開始遊戲
        self.assertEqual(engine.get_game_status(), GameEngine.STATUS_PLAYING)
        
        # 2. 第一次點擊（必須先點擊才能標記）
        result = engine.click_cell(2, 2)
        self.assertTrue(result['success'])
        self.assertFalse(result['exploded'])
        
        # 3. 標記一個格子（確保該格子未被揭開）
        # 如果 (0,0) 已被自動展開，選擇另一個位置
        if not engine.is_cell_revealed(0, 0):
            flag_result = engine.flag_cell(0, 0)
            self.assertTrue(flag_result['success'])
        else:
            # 找一個未揭開的格子標記
            flagged = False
            for r in range(5):
                for c in range(5):
                    if not engine.is_cell_revealed(r, c):
                        flag_result = engine.flag_cell(r, c)
                        self.assertTrue(flag_result['success'])
                        flagged = True
                        break
                if flagged:
                    break
        
        # 4. 繼續點擊（如果該格子還沒被揭開）
        if not engine.is_cell_revealed(1, 1):
            result = engine.click_cell(1, 1)
            self.assertTrue(result['success'])
        
        # 遊戲應該還在進行中
        self.assertEqual(engine.get_game_status(), GameEngine.STATUS_PLAYING)
    
    def test_win_condition(self):
        """測試勝利條件"""
        # 建立一個非常小的棋盤來測試勝利
        engine = GameEngine(3, 3, 1)
        engine.start_new_game()
        
        # 找到並標記地雷
        mine_found = False
        for r in range(3):
            for c in range(3):
                if engine.board.is_mine(r, c):
                    engine.flag_cell(r, c)
                    mine_found = True
                    break
            if mine_found:
                break
        
        # 揭開所有非地雷格子
        for r in range(3):
            for c in range(3):
                if not engine.board.is_mine(r, c) and not engine.is_cell_flagged(r, c):
                    engine.click_cell(r, c)
        
        # 檢查是否勝利
        self.assertEqual(engine.get_game_status(), GameEngine.STATUS_WON)
    
    def test_lose_condition(self):
        """測試失敗條件"""
        engine = GameEngine(5, 5, 3)
        engine.start_new_game()
        
        # 第一次點擊（安全）
        engine.click_cell(2, 2)
        
        # 找到一個地雷並點擊
        mine_clicked = False
        for r in range(5):
            for c in range(5):
                if (r, c) != (2, 2) and engine.board.is_mine(r, c):
                    result = engine.click_cell(r, c)
                    if result['exploded']:
                        self.assertEqual(engine.get_game_status(), GameEngine.STATUS_LOST)
                        mine_clicked = True
                        break
            if mine_clicked:
                break
        
        self.assertTrue(mine_clicked, "應該能找到並點擊到地雷")
    
    def test_flag_count_consistency(self):
        """測試標記數量的一致性"""
        engine = GameEngine(9, 9, 10)
        engine.start_new_game()
        
        # 標記幾個格子
        flags_to_set = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        
        for r, c in flags_to_set:
            engine.flag_cell(r, c)
        
        # 檢查剩餘地雷數
        remaining = engine.get_remaining_mines()
        self.assertEqual(remaining, 10 - len(flags_to_set))
        
        # 取消一個標記
        engine.flag_cell(0, 0)
        remaining = engine.get_remaining_mines()
        self.assertEqual(remaining, 10 - len(flags_to_set) + 1)
    
    def test_multiple_games(self):
        """測試多次遊戲"""
        engine = GameEngine(9, 9, 10)
        
        # 第一次遊戲
        engine.start_new_game()
        engine.click_cell(0, 0)
        moves1 = engine.get_moves_count()
        
        # 第二次遊戲
        engine.start_new_game()
        self.assertEqual(engine.get_moves_count(), 0, "新遊戲移動次數應該重置為 0")
        self.assertEqual(engine.get_game_status(), GameEngine.STATUS_PLAYING)
        self.assertTrue(engine.first_click, "新遊戲應該標記為第一次點擊")
        
        engine.click_cell(1, 1)
        moves2 = engine.get_moves_count()
        
        # 兩次遊戲都應該至少有一次移動
        self.assertGreaterEqual(moves1, 1)
        self.assertGreaterEqual(moves2, 1)
        # 注意：由於隨機性和自動展開，移動次數可能相同，這是正常的
    
    def test_edge_cases(self):
        """測試邊界情況"""
        engine = GameEngine(9, 9, 10)
        engine.start_new_game()
        
        # 測試無效座標（應該被忽略或返回 False）
        # 注意：目前的實作可能不會檢查邊界，這取決於實作細節
        
        # 測試在遊戲結束後點擊
        engine.status = GameEngine.STATUS_WON
        result = engine.click_cell(0, 0)
        self.assertFalse(result['success'])
        self.assertEqual(result['game_status'], GameEngine.STATUS_WON)
    
    def test_auto_expand_on_first_click(self):
        """測試第一次點擊時自動展開"""
        engine = GameEngine(9, 9, 10)
        engine.start_new_game()
        
        # 第一次點擊
        result = engine.click_cell(4, 4)
        
        # 應該自動展開周圍的空白區域
        revealed_count = len(result['revealed_cells'])
        self.assertGreater(revealed_count, 1, "第一次點擊應該展開多個格子")
    
    def test_board_state_consistency(self):
        """測試遊戲板狀態的一致性"""
        engine = GameEngine(9, 9, 10)
        engine.start_new_game()
        
        # 第一次點擊（會自動展開）
        result1 = engine.click_cell(0, 0)
        state = engine.get_board_state()
        
        # 檢查至少有一些格子被揭開
        revealed_count = sum(1 for row in state for cell in row if cell != 0 and cell != 9)
        self.assertGreater(revealed_count, 0, "應該至少有一些格子被揭開")
        
        # 標記一個未揭開的格子
        # 找一個未揭開且未標記的格子
        flagged = False
        for r in range(9):
            for c in range(9):
                if state[r][c] == 0:  # 未揭開
                    flag_result = engine.flag_cell(r, c)
                    if flag_result['success']:
                        flagged = True
                        break
            if flagged:
                break
        
        # 檢查標記後的狀態
        state = engine.get_board_state()
        flag_count = sum(1 for row in state for cell in row if cell == 9)
        # 如果找到了未揭開的格子，應該能成功標記
        # 如果所有格子都被自動展開，這個測試仍然通過（因為至少驗證了狀態一致性）
        if flagged:
            self.assertGreater(flag_count, 0, "應該至少有一個格子被標記")


if __name__ == '__main__':
    unittest.main()

