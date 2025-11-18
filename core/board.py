"""
遊戲板類別 - 封裝遊戲板的資料結構和基本操作
"""
import random
from typing import List, Tuple, Optional


class Board:
    """遊戲板類別，管理地雷配置和格子狀態"""
    
    # 格子狀態常數
    UNREVEALED = 0  # 未揭開
    REVEALED = 1    # 已揭開
    FLAGGED = 2     # 已標記
    
    def __init__(self, rows: int, cols: int, num_mines: int, first_click: Optional[Tuple[int, int]] = None):
        """
        初始化遊戲板
        
        Args:
            rows: 行數
            cols: 列數
            num_mines: 地雷數量
            first_click: 第一次點擊的位置 (row, col)，確保第一次點擊不會是地雷
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        
        # 內部地雷配置：-1 表示地雷，0-8 表示周圍地雷數
        self.mine_grid: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # 格子狀態：UNREVEALED, REVEALED, FLAGGED
        self.state_grid: List[List[int]] = [[self.UNREVEALED for _ in range(cols)] for _ in range(rows)]
        
        # 生成地雷配置
        self._generate_mines(first_click)
        
        # 計算每個格子的數字（周圍地雷數）
        self._calculate_numbers()
    
    def _generate_mines(self, first_click: Optional[Tuple[int, int]] = None):
        """隨機生成地雷位置"""
        mine_positions = []
        safe_positions = set()
        
        # 確保第一次點擊的位置及其鄰居不會是地雷
        if first_click:
            r, c = first_click
            safe_positions.add((r, c))
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        safe_positions.add((nr, nc))
        
        # 生成所有可能的位置
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        available_positions = [pos for pos in all_positions if pos not in safe_positions]
        
        # 隨機選擇地雷位置
        if len(available_positions) < self.num_mines:
            self.num_mines = len(available_positions)
        
        mine_positions = random.sample(available_positions, self.num_mines)
        
        # 放置地雷
        for r, c in mine_positions:
            self.mine_grid[r][c] = -1
    
    def _calculate_numbers(self):
        """計算每個格子周圍的地雷數"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_grid[r][c] == -1:
                    continue  # 地雷本身不需要計算
                
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.mine_grid[nr][nc] == -1:
                                count += 1
                
                self.mine_grid[r][c] = count
    
    def get_cell_value(self, row: int, col: int) -> int:
        """
        取得格子的值
        -1: 地雷
        0-8: 周圍地雷數
        """
        if not self.is_valid_position(row, col):
            return 0
        return self.mine_grid[row][col]
    
    def is_mine(self, row: int, col: int) -> bool:
        """檢查是否為地雷"""
        if not self.is_valid_position(row, col):
            return False
        return self.mine_grid[row][col] == -1
    
    def is_revealed(self, row: int, col: int) -> bool:
        """檢查是否已揭開"""
        if not self.is_valid_position(row, col):
            return False
        return self.state_grid[row][col] == self.REVEALED
    
    def is_flagged(self, row: int, col: int) -> bool:
        """檢查是否已標記"""
        if not self.is_valid_position(row, col):
            return False
        return self.state_grid[row][col] == self.FLAGGED
    
    def is_unrevealed(self, row: int, col: int) -> bool:
        """檢查是否未揭開且未標記"""
        if not self.is_valid_position(row, col):
            return False
        return self.state_grid[row][col] == self.UNREVEALED
    
    def reveal_cell(self, row: int, col: int) -> bool:
        """
        揭開格子
        
        Returns:
            True 如果成功揭開，False 如果是地雷
        """
        if not self.is_valid_position(row, col):
            return False
        
        if self.state_grid[row][col] != self.UNREVEALED:
            return True  # 已經揭開或標記，不需要處理
        
        self.state_grid[row][col] = self.REVEALED
        
        # 如果是地雷，返回 False
        if self.is_mine(row, col):
            return False
        
        # 如果是空白格子（數字為0），自動揭開周圍的格子
        if self.mine_grid[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if self.is_valid_position(nr, nc) and self.state_grid[nr][nc] == self.UNREVEALED:
                        self.reveal_cell(nr, nc)
        
        return True
    
    def toggle_flag(self, row: int, col: int) -> bool:
        """
        切換標記狀態
        
        Returns:
            True 如果標記，False 如果取消標記
        """
        if not self.is_valid_position(row, col):
            return False
        
        if self.state_grid[row][col] == self.REVEALED:
            return False  # 已揭開的格子不能標記
        
        if self.state_grid[row][col] == self.FLAGGED:
            self.state_grid[row][col] = self.UNREVEALED
            return False  # 取消標記
        else:
            self.state_grid[row][col] = self.FLAGGED
            return True  # 標記
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """取得所有鄰居格子的座標"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.is_valid_position(nr, nc):
                    neighbors.append((nr, nc))
        return neighbors
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """檢查座標是否有效"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_flagged_count(self) -> int:
        """取得已標記的格子數量"""
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.state_grid[r][c] == self.FLAGGED:
                    count += 1
        return count
    
    def get_revealed_count(self) -> int:
        """取得已揭開的格子數量"""
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.state_grid[r][c] == self.REVEALED:
                    count += 1
        return count
    
    def check_win(self) -> bool:
        """檢查是否勝利（所有非地雷格子都已揭開）"""
        total_cells = self.rows * self.cols
        revealed_count = self.get_revealed_count()
        return revealed_count == (total_cells - self.num_mines)
    
    def get_board_state_for_ai(self) -> List[List[int]]:
        """
        取得供 AI 使用的遊戲板狀態
        返回一個 2D 列表：
        - 0: 未揭開
        - 1-8: 已揭開的數字
        - 9: 已標記
        - -1: 已揭開的地雷（遊戲結束時）
        """
        state = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if self.state_grid[r][c] == self.FLAGGED:
                    row.append(9)
                elif self.state_grid[r][c] == self.REVEALED:
                    row.append(self.mine_grid[r][c])
                else:
                    row.append(0)
            state.append(row)
        return state

