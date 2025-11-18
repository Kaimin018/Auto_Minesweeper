"""
資料庫操作 - 管理排行榜資料
"""
import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime


class Database:
    """資料庫管理類別"""
    
    def __init__(self, db_path: str = "data/leaderboard.db"):
        """
        初始化資料庫
        
        Args:
            db_path: 資料庫檔案路徑
        """
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self):
        """確保 data 目錄存在"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _init_database(self):
        """初始化資料庫表結構"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立排行榜表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                time_seconds REAL NOT NULL,
                board_size TEXT NOT NULL,
                moves_count INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 建立索引以提升查詢效能
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_difficulty_time 
            ON leaderboard(difficulty, time_seconds)
        """)
        
        conn.commit()
        conn.close()
    
    def save_record(
        self, 
        player_name: str, 
        difficulty: str, 
        time_seconds: float, 
        board_size: str,
        moves_count: Optional[int] = None
    ) -> int:
        """
        儲存遊戲記錄
        
        Returns:
            記錄 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO leaderboard 
            (player_name, difficulty, time_seconds, board_size, moves_count)
            VALUES (?, ?, ?, ?, ?)
        """, (player_name, difficulty, time_seconds, board_size, moves_count))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_leaderboard(
        self, 
        difficulty: Optional[str] = None, 
        limit: int = 10
    ) -> List[Dict]:
        """
        取得排行榜
        
        Args:
            difficulty: 難度篩選（None 表示所有難度）
            limit: 返回記錄數量限制
        
        Returns:
            記錄列表，每個記錄包含：
            {
                'id': int,
                'player_name': str,
                'difficulty': str,
                'time_seconds': float,
                'board_size': str,
                'moves_count': int,
                'date': str
            }
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if difficulty:
            cursor.execute("""
                SELECT id, player_name, difficulty, time_seconds, board_size, moves_count, date
                FROM leaderboard
                WHERE difficulty = ?
                ORDER BY time_seconds ASC
                LIMIT ?
            """, (difficulty, limit))
        else:
            cursor.execute("""
                SELECT id, player_name, difficulty, time_seconds, board_size, moves_count, date
                FROM leaderboard
                ORDER BY time_seconds ASC
                LIMIT ?
            """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        for row in rows:
            records.append({
                'id': row[0],
                'player_name': row[1],
                'difficulty': row[2],
                'time_seconds': row[3],
                'board_size': row[4],
                'moves_count': row[5],
                'date': row[6]
            })
        
        return records
    
    def get_best_time(self, difficulty: str) -> Optional[float]:
        """取得特定難度的最佳時間"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MIN(time_seconds)
            FROM leaderboard
            WHERE difficulty = ?
        """, (difficulty,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result and result[0] is not None else None
    
    def clear_leaderboard(self, difficulty: Optional[str] = None):
        """
        清空排行榜
        
        Args:
            difficulty: 如果指定，只清空該難度的記錄
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if difficulty:
            cursor.execute("DELETE FROM leaderboard WHERE difficulty = ?", (difficulty,))
        else:
            cursor.execute("DELETE FROM leaderboard")
        
        conn.commit()
        conn.close()
    
    def get_player_stats(self, player_name: str) -> Dict:
        """取得玩家的統計資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_games,
                MIN(time_seconds) as best_time,
                AVG(time_seconds) as avg_time,
                difficulty
            FROM leaderboard
            WHERE player_name = ?
            GROUP BY difficulty
        """, (player_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {
            'total_games': 0,
            'by_difficulty': {}
        }
        
        for row in rows:
            difficulty = row[3]
            stats['by_difficulty'][difficulty] = {
                'count': row[0],
                'best_time': row[1],
                'avg_time': row[2]
            }
            stats['total_games'] += row[0]
        
        return stats

