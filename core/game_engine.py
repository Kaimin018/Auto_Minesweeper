"""
遊戲引擎 - 管理遊戲狀態和邏輯
"""
from typing import Optional, Tuple, List
from .board import Board


class GameEngine:
    """遊戲引擎類別，管理遊戲的整體狀態"""
    
    # 遊戲狀態
    STATUS_PLAYING = "playing"
    STATUS_WON = "won"
    STATUS_LOST = "lost"
    
    def __init__(self, rows: int = 9, cols: int = 9, num_mines: int = 10):
        """
        初始化遊戲引擎
        
        Args:
            rows: 行數
            cols: 列數
            num_mines: 地雷數量
        """
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board: Optional[Board] = None
        self.status = self.STATUS_PLAYING
        self.first_click = True
        self.moves_count = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def start_new_game(self, first_click: Optional[Tuple[int, int]] = None):
        """開始新遊戲"""
        self.board = Board(self.rows, self.cols, self.num_mines, first_click)
        self.status = self.STATUS_PLAYING
        self.first_click = True
        self.moves_count = 0
        self.start_time = None
        self.end_time = None
    
    def click_cell(self, row: int, col: int) -> dict:
        """
        點擊格子
        
        Returns:
            包含結果資訊的字典：
            {
                'success': bool,
                'game_status': str,
                'exploded': bool,  # 是否踩到地雷
                'revealed_cells': List[Tuple[int, int]]  # 被揭開的格子列表
            }
        """
        if not self.board or self.status != self.STATUS_PLAYING:
            return {'success': False, 'game_status': self.status, 'exploded': False}
        
        # 如果已標記，不能點擊
        if self.board.is_flagged(row, col):
            return {'success': False, 'game_status': self.status, 'message': '格子已標記', 'exploded': False}
        
        # 如果已揭開，不需要處理
        if self.board.is_revealed(row, col):
            return {'success': True, 'game_status': self.status, 'exploded': False}
        
        # 第一次點擊時，確保不會是地雷，並記錄開始時間
        if self.first_click:
            import time
            self.board = Board(self.rows, self.cols, self.num_mines, (row, col))
            self.start_time = time.time()
            self.first_click = False
        
        # 揭開格子
        revealed_cells = []
        success = self.board.reveal_cell(row, col)
        
        if not success:
            # 踩到地雷
            self.status = self.STATUS_LOST
            import time
            self.end_time = time.time()
            return {
                'success': False,
                'game_status': self.STATUS_LOST,
                'exploded': True,
                'revealed_cells': [(row, col)]
            }
        
        # 收集所有被揭開的格子
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board.is_revealed(r, c):
                    revealed_cells.append((r, c))
        
        self.moves_count += 1
        
        # 檢查是否勝利
        if self.board.check_win():
            self.status = self.STATUS_WON
            import time
            self.end_time = time.time()
        
        return {
            'success': True,
            'game_status': self.status,
            'exploded': False,
            'revealed_cells': revealed_cells
        }
    
    def flag_cell(self, row: int, col: int) -> dict:
        """
        標記/取消標記格子
        
        Returns:
            包含結果資訊的字典：
            {
                'success': bool,
                'flagged': bool,  # True 表示標記，False 表示取消標記
                'remaining_mines': int
            }
        """
        if not self.board or self.status != self.STATUS_PLAYING:
            return {'success': False}
        
        if self.board.is_revealed(row, col):
            return {'success': False, 'message': '已揭開的格子不能標記'}
        
        flagged = self.board.toggle_flag(row, col)
        remaining = self.num_mines - self.board.get_flagged_count()
        
        return {
            'success': True,
            'flagged': flagged,
            'remaining_mines': max(0, remaining)
        }
    
    def get_board_state(self) -> List[List[int]]:
        """取得當前遊戲板狀態（供 UI 顯示用）"""
        if not self.board:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return self.board.get_board_state_for_ai()
    
    def get_cell_value(self, row: int, col: int) -> int:
        """取得格子的值（僅在已揭開時有效）"""
        if not self.board:
            return 0
        if self.board.is_revealed(row, col):
            return self.board.get_cell_value(row, col)
        return 0
    
    def is_cell_revealed(self, row: int, col: int) -> bool:
        """檢查格子是否已揭開"""
        if not self.board:
            return False
        return self.board.is_revealed(row, col)
    
    def is_cell_flagged(self, row: int, col: int) -> bool:
        """檢查格子是否已標記"""
        if not self.board:
            return False
        return self.board.is_flagged(row, col)
    
    def get_game_status(self) -> str:
        """取得遊戲狀態"""
        return self.status
    
    def get_elapsed_time(self) -> float:
        """取得經過的時間（秒）"""
        import time
        if self.start_time is None:
            return 0.0
        if self.end_time is not None:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def get_remaining_mines(self) -> int:
        """取得剩餘地雷數"""
        if not self.board:
            return self.num_mines
        return max(0, self.num_mines - self.board.get_flagged_count())
    
    def get_moves_count(self) -> int:
        """取得移動次數"""
        return self.moves_count
    
    def reveal_all_mines(self):
        """揭開所有地雷（遊戲結束時使用）"""
        if not self.board:
            return
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board.is_mine(r, c) and not self.board.is_flagged(r, c):
                    self.board.state_grid[r][c] = Board.REVEALED

