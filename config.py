"""
全域配置設定
"""

# 遊戲難度設定
DIFFICULTY_SETTINGS = {
    'beginner': {
        'rows': 9,
        'cols': 9,
        'mines': 10,
        'name': '初級',
        'board_size': '9x9'
    },
    'intermediate': {
        'rows': 16,
        'cols': 16,
        'mines': 40,
        'name': '中級',
        'board_size': '16x16'
    },
    'expert': {
        'rows': 16,
        'cols': 30,
        'mines': 99,
        'name': '專家級',
        'board_size': '30x16'
    }
}

# UI 設定
CELL_SIZE = 30  # 每個格子的像素大小
CELL_MARGIN = 2  # 格子之間的間距

# 顏色設定（RGB）
COLORS = {
    'cell_unrevealed': (200, 200, 200),
    'cell_revealed': (240, 240, 240),
    'cell_flagged': (255, 200, 200),
    'cell_mine': (255, 0, 0),
    'numbers': {
        1: (0, 0, 255),      # 藍色
        2: (0, 128, 0),      # 綠色
        3: (255, 0, 0),      # 紅色
        4: (128, 0, 128),    # 紫色
        5: (128, 0, 0),      # 深紅色
        6: (0, 128, 128),    # 青色
        7: (0, 0, 0),        # 黑色
        8: (128, 128, 128),  # 灰色
    }
}

# 資料庫路徑
DATABASE_PATH = "data/leaderboard.db"

