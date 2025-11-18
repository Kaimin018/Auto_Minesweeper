"""
求解策略 - 從原 main.py 提取的基礎求解邏輯
"""
from typing import Optional, Tuple, List
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.board import Board


class BasicSolver:
    """基礎求解器，使用簡單的邏輯規則"""
    
    def __init__(self, board: Board):
        self.board = board
    
    def find_next_move(self) -> Optional[Tuple[str, int, int]]:
        """
        找出下一步行動
        
        Returns:
            (action, row, col) 或 None
            action: 'click' 或 'flag'
        """
        # 策略 1: 找出安全的點擊
        safe_move = self._find_safe_click()
        if safe_move:
            return ('click', safe_move[0], safe_move[1])
        
        # 策略 2: 找出地雷並標記
        mine_move = self._find_mine_to_flag()
        if mine_move:
            return ('flag', mine_move[0], mine_move[1])
        
        return None
    
    def _find_safe_click(self) -> Optional[Tuple[int, int]]:
        """找出安全的點擊（數字方塊周圍的旗子數等於數字，則其餘未開方塊安全）"""
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if not self.board.is_revealed(r, c):
                    continue
                
                cell_value = self.board.get_cell_value(r, c)
                if 1 <= cell_value <= 8:
                    neighbors = self.board.get_neighbors(r, c)
                    flagged_count = 0
                    unopened_neighbors = []
                    
                    for nr, nc in neighbors:
                        if self.board.is_flagged(nr, nc):
                            flagged_count += 1
                        elif self.board.is_unrevealed(nr, nc):
                            unopened_neighbors.append((nr, nc))
                    
                    # 如果數字等於旗子數，剩餘未開方塊都是安全的
                    if cell_value == flagged_count and unopened_neighbors:
                        return unopened_neighbors[0]
        
        return None
    
    def _find_mine_to_flag(self) -> Optional[Tuple[int, int]]:
        """找出地雷並標記（數字方塊周圍的未開方塊數等於數字，則這些未開方塊是地雷）"""
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if not self.board.is_revealed(r, c):
                    continue
                
                cell_value = self.board.get_cell_value(r, c)
                if 1 <= cell_value <= 8:
                    neighbors = self.board.get_neighbors(r, c)
                    unopened_count = 0
                    flagged_count = 0
                    unopened_neighbors = []
                    
                    for nr, nc in neighbors:
                        if self.board.is_flagged(nr, nc):
                            flagged_count += 1
                        elif self.board.is_unrevealed(nr, nc):
                            unopened_count += 1
                            unopened_neighbors.append((nr, nc))
                    
                    # 如果數字等於未開方塊數 + 旗子數，所有未開方塊都是地雷
                    if cell_value == (unopened_count + flagged_count) and unopened_neighbors:
                        return unopened_neighbors[0]
        
        return None

