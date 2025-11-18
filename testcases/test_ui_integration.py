"""
測試 UI 與遊戲引擎的整合，確保返回字典的完整性
"""
import unittest
from core.game_engine import GameEngine


class TestUIIntegration(unittest.TestCase):
    """測試 UI 整合，確保所有返回字典都包含必要的鍵"""
    
    def setUp(self):
        """每個測試前的設置"""
        import random
        random.seed(42)
        self.engine = GameEngine(9, 9, 10)
        self.engine.start_new_game()
    
    def test_click_cell_always_has_exploded_key(self):
        """測試 click_cell 的所有返回路徑都包含 'exploded' 鍵"""
        # 測試 1: 遊戲未開始時
        engine = GameEngine(9, 9, 10)
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result, "遊戲未開始時應該包含 'exploded' 鍵")
        
        # 測試 2: 點擊已標記的格子
        engine.start_new_game()
        engine.flag_cell(0, 0)
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result, "點擊已標記格子時應該包含 'exploded' 鍵")
        
        # 測試 3: 點擊已揭開的格子
        engine.start_new_game()
        engine.click_cell(0, 0)
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result, "點擊已揭開格子時應該包含 'exploded' 鍵")
        
        # 測試 4: 正常點擊
        engine.start_new_game()
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result, "正常點擊時應該包含 'exploded' 鍵")
        
        # 測試 5: 遊戲已結束時
        engine.status = GameEngine.STATUS_WON
        result = engine.click_cell(0, 1)
        self.assertIn('exploded', result, "遊戲已結束時應該包含 'exploded' 鍵")
    
    def test_click_cell_result_structure(self):
        """測試 click_cell 返回字典的結構完整性"""
        result = self.engine.click_cell(0, 0)
        
        # 必須包含的鍵
        required_keys = ['success', 'game_status', 'exploded']
        for key in required_keys:
            self.assertIn(key, result, f"返回字典應該包含 '{key}' 鍵")
        
        # 驗證鍵的類型
        self.assertIsInstance(result['success'], bool)
        self.assertIsInstance(result['game_status'], str)
        self.assertIsInstance(result['exploded'], bool)
        
        # 如果成功，應該包含 revealed_cells
        if result['success']:
            self.assertIn('revealed_cells', result)
            self.assertIsInstance(result['revealed_cells'], list)
    
    def test_all_click_scenarios(self):
        """測試所有點擊場景的返回完整性"""
        scenarios = []
        
        # 場景 1: 第一次點擊
        engine = GameEngine(9, 9, 10)
        engine.start_new_game()
        result = engine.click_cell(4, 4)
        scenarios.append(('第一次點擊', result))
        
        # 場景 2: 點擊已標記的格子
        engine.start_new_game()
        engine.flag_cell(0, 0)
        result = engine.click_cell(0, 0)
        scenarios.append(('點擊已標記格子', result))
        
        # 場景 3: 點擊已揭開的格子
        engine.start_new_game()
        engine.click_cell(0, 0)
        result = engine.click_cell(0, 0)
        scenarios.append(('點擊已揭開格子', result))
        
        # 場景 4: 遊戲已結束
        engine.start_new_game()
        engine.status = GameEngine.STATUS_LOST
        result = engine.click_cell(0, 0)
        scenarios.append(('遊戲已結束', result))
        
        # 驗證所有場景
        for scenario_name, result in scenarios:
            with self.subTest(scenario=scenario_name):
                self.assertIn('exploded', result, 
                            f"{scenario_name} 應該包含 'exploded' 鍵")
                self.assertIn('game_status', result,
                            f"{scenario_name} 應該包含 'game_status' 鍵")
                self.assertIn('success', result,
                            f"{scenario_name} 應該包含 'success' 鍵")
    
    def test_exploded_key_values(self):
        """測試 'exploded' 鍵的值是否正確"""
        # 第一次點擊不應該是地雷
        result = self.engine.click_cell(0, 0)
        self.assertFalse(result['exploded'], "第一次點擊不應該踩到地雷")
        
        # 正常點擊不應該是地雷（除非真的踩到）
        # 注意：由於隨機性，我們無法確定是否會踩到地雷
        # 但至少第一次點擊是安全的
        
        # 測試已標記的格子
        self.engine.start_new_game()
        self.engine.flag_cell(0, 0)
        result = self.engine.click_cell(0, 0)
        self.assertFalse(result['exploded'], "點擊已標記格子不應該設置 exploded=True")
        
        # 測試已揭開的格子
        self.engine.start_new_game()
        self.engine.click_cell(0, 0)
        result = self.engine.click_cell(0, 0)
        self.assertFalse(result['exploded'], "點擊已揭開格子不應該設置 exploded=True")
    
    def test_game_status_consistency(self):
        """測試遊戲狀態與 exploded 鍵的一致性"""
        # 如果 exploded=True，game_status 應該是 LOST
        # 注意：由於隨機性，我們無法強制踩到地雷
        # 但我們可以測試其他情況
        
        # 正常點擊，不應該爆炸
        result = self.engine.click_cell(0, 0)
        if not result['exploded']:
            # 如果沒有爆炸，狀態應該是 PLAYING 或 WON
            self.assertIn(result['game_status'], 
                         [GameEngine.STATUS_PLAYING, GameEngine.STATUS_WON])
        
        # 如果狀態是 LOST，exploded 應該是 True
        # （這個測試需要實際踩到地雷，所以我們跳過）
    
    def test_error_handling(self):
        """測試錯誤處理時返回字典的完整性"""
        # 測試無效座標（如果有的話）
        # 目前實作可能不會檢查，但我們至少確保返回有 exploded 鍵
        
        # 測試遊戲未開始
        engine = GameEngine(9, 9, 10)
        # 不調用 start_new_game()
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result)
        
        # 測試遊戲已結束
        engine.start_new_game()
        engine.status = GameEngine.STATUS_WON
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result)
        
        engine.status = GameEngine.STATUS_LOST
        result = engine.click_cell(0, 0)
        self.assertIn('exploded', result)


if __name__ == '__main__':
    unittest.main()

