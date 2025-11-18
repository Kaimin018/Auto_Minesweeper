"""
機率計算引擎 - 計算每個格子的地雷機率
"""
from typing import List, Tuple, Dict, Optional
import copy


class ProbabilityCalculator:
    """計算踩地雷遊戲中每個格子的地雷機率"""
    
    def __init__(self, board_state: List[List[int]], rows: int, cols: int, total_mines: int):
        """
        初始化機率計算器
        
        Args:
            board_state: 遊戲板狀態（0=未揭開, 1-8=數字, 9=標記）
            rows: 行數
            cols: 列數
            total_mines: 總地雷數
        """
        self.board_state = board_state
        self.rows = rows
        self.cols = cols
        self.total_mines = total_mines
        self.probabilities: Dict[Tuple[int, int], float] = {}
        self.flagged_count = 0
        
        # 計算已標記的數量
        for r in range(rows):
            for c in range(cols):
                if board_state[r][c] == 9:
                    self.flagged_count += 1
    
    def calculate_probabilities(self) -> Dict[Tuple[int, int], float]:
        """
        計算所有未知格子的地雷機率
        
        Returns:
            字典：{(row, col): probability}
        """
        self.probabilities = {}
        
        # 找出所有未揭開且未標記的格子
        unknown_cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board_state[r][c] == 0:
                    unknown_cells.append((r, c))
        
        if not unknown_cells:
            return self.probabilities
        
        # 計算剩餘地雷數
        remaining_mines = self.total_mines - self.flagged_count
        
        if remaining_mines <= 0:
            # 所有地雷都已標記，剩餘格子都是安全的
            for cell in unknown_cells:
                self.probabilities[cell] = 0.0
            return self.probabilities
        
        # 策略1: 使用約束傳播找出確定是地雷或安全的格子
        safe_cells, mine_cells = self._find_deterministic_cells()
        
        # 標記確定安全的格子
        for cell in safe_cells:
            self.probabilities[cell] = 0.0
        
        # 標記確定是地雷的格子
        for cell in mine_cells:
            self.probabilities[cell] = 1.0
        
        # 策略2: 對於其他未知格子，使用約束滿足問題計算機率
        remaining_unknown = [cell for cell in unknown_cells 
                            if cell not in safe_cells and cell not in mine_cells]
        
        if remaining_unknown:
            # 使用簡化的機率計算
            # 考慮所有數字方塊的約束條件
            constraints = self._extract_constraints()
            
            # 對於每個未知格子，計算在所有可能配置中它是地雷的機率
            for cell in remaining_unknown:
                prob = self._calculate_cell_probability(cell, constraints, remaining_unknown, remaining_mines)
                self.probabilities[cell] = prob
        
        return self.probabilities
    
    def _find_deterministic_cells(self) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        """
        使用約束傳播找出確定安全或確定是地雷的格子
        
        Returns:
            (safe_cells, mine_cells)
        """
        safe_cells = []
        mine_cells = []
        
        # 遍歷所有數字方塊
        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.board_state[r][c]
                if 1 <= cell_value <= 8:
                    neighbors = self._get_neighbors(r, c)
                    
                    # 找出未揭開且未標記的鄰居
                    unknown_neighbors = []
                    flagged_count = 0
                    
                    for nr, nc in neighbors:
                        state = self.board_state[nr][nc]
                        if state == 0:  # 未揭開
                            unknown_neighbors.append((nr, nc))
                        elif state == 9:  # 已標記
                            flagged_count += 1
                    
                    # 如果數字等於已標記的數量，所有未揭開的鄰居都是安全的
                    if cell_value == flagged_count and unknown_neighbors:
                        safe_cells.extend(unknown_neighbors)
                    
                    # 如果數字等於未揭開鄰居數 + 已標記數，所有未揭開的鄰居都是地雷
                    if cell_value == len(unknown_neighbors) + flagged_count and unknown_neighbors:
                        mine_cells.extend(unknown_neighbors)
        
        # 去重
        safe_cells = list(set(safe_cells))
        mine_cells = list(set(mine_cells))
        
        return safe_cells, mine_cells
    
    def _extract_constraints(self) -> List[Dict]:
        """
        提取所有約束條件
        
        Returns:
            約束列表，每個約束包含：
            {
                'center': (row, col),
                'value': int,  # 數字值
                'unknown_neighbors': List[Tuple[int, int]],
                'flagged_count': int
            }
        """
        constraints = []
        
        for r in range(self.rows):
            for c in range(self.cols):
                cell_value = self.board_state[r][c]
                if 1 <= cell_value <= 8:
                    neighbors = self._get_neighbors(r, c)
                    unknown_neighbors = []
                    flagged_count = 0
                    
                    for nr, nc in neighbors:
                        state = self.board_state[nr][nc]
                        if state == 0:
                            unknown_neighbors.append((nr, nc))
                        elif state == 9:
                            flagged_count += 1
                    
                    if unknown_neighbors:  # 如果有未知鄰居，才需要這個約束
                        constraints.append({
                            'center': (r, c),
                            'value': cell_value,
                            'unknown_neighbors': unknown_neighbors,
                            'flagged_count': flagged_count
                        })
        
        return constraints
    
    def _calculate_cell_probability(
        self, 
        cell: Tuple[int, int], 
        constraints: List[Dict],
        unknown_cells: List[Tuple[int, int]],
        remaining_mines: int
    ) -> float:
        """
        計算特定格子的地雷機率
        
        使用簡化的方法：考慮該格子相關的所有約束條件
        """
        # 找出與該格子相關的約束
        relevant_constraints = []
        for constraint in constraints:
            if cell in constraint['unknown_neighbors']:
                relevant_constraints.append(constraint)
        
        if not relevant_constraints:
            # 沒有相關約束，使用全局機率
            if len(unknown_cells) > 0:
                return remaining_mines / len(unknown_cells)
            return 0.0
        
        # 計算該格子必須是地雷的最小約束
        min_required = 0
        for constraint in relevant_constraints:
            # 如果該約束要求至少 N 個地雷在未知鄰居中
            # 且該格子是唯一可能的候選，則機率為 1
            required = constraint['value'] - constraint['flagged_count']
            unknown_in_constraint = constraint['unknown_neighbors']
            
            if required == len(unknown_in_constraint) and len(unknown_in_constraint) == 1:
                return 1.0
            
            if required > 0:
                min_required = max(min_required, required / len(unknown_in_constraint))
        
        # 如果有多個約束，取平均值
        if relevant_constraints:
            total_prob = 0.0
            for constraint in relevant_constraints:
                required = constraint['value'] - constraint['flagged_count']
                unknown_in_constraint = constraint['unknown_neighbors']
                if len(unknown_in_constraint) > 0:
                    total_prob += required / len(unknown_in_constraint)
            
            avg_prob = total_prob / len(relevant_constraints)
            
            # 結合全局機率（加權平均）
            global_prob = remaining_mines / len(unknown_cells) if unknown_cells else 0.0
            return min(1.0, (avg_prob * 0.7 + global_prob * 0.3))
        
        # 回退到全局機率
        if len(unknown_cells) > 0:
            return remaining_mines / len(unknown_cells)
        return 0.0
    
    def _get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """取得所有鄰居格子的座標"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors
    
    def get_cell_probability(self, row: int, col: int) -> float:
        """取得特定格子的機率"""
        return self.probabilities.get((row, col), 0.5)  # 預設 0.5
    
    def find_safe_cells(self) -> List[Tuple[int, int]]:
        """找出機率為 0 的安全格子"""
        return [cell for cell, prob in self.probabilities.items() if prob == 0.0]
    
    def find_mine_cells(self) -> List[Tuple[int, int]]:
        """找出機率為 1 的地雷格子"""
        return [cell for cell, prob in self.probabilities.items() if prob == 1.0]
    
    def find_best_move(self) -> Optional[Tuple[int, int]]:
        """
        找出最佳下一步（機率最低的格子）
        
        Returns:
            (row, col) 或 None
        """
        if not self.probabilities:
            return None
        
        # 找出機率最低的格子
        min_prob = min(self.probabilities.values())
        if min_prob >= 1.0:
            return None  # 沒有安全的格子
        
        best_cells = [cell for cell, prob in self.probabilities.items() if prob == min_prob]
        return best_cells[0] if best_cells else None

