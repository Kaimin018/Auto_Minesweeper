"""
排行榜視窗
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import Database
import config


class LeaderboardWindow(QMainWindow):
    """排行榜視窗"""
    
    def __init__(self, database: Database, parent=None):
        super().__init__(parent)
        self.database = database
        self.current_difficulty = None
        self.init_ui()
        self.load_leaderboard()
    
    def init_ui(self):
        """初始化使用者介面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 標題
        title = QLabel("排行榜")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title)
        
        # 難度選擇
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("難度:"))
        
        difficulty_combo = QComboBox()
        difficulty_combo.addItem("全部", None)
        for key, value in config.DIFFICULTY_SETTINGS.items():
            difficulty_combo.addItem(value['name'], key)
        difficulty_combo.currentIndexChanged.connect(
            lambda idx: self.on_difficulty_changed(difficulty_combo.itemData(idx))
        )
        filter_layout.addWidget(difficulty_combo)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # 排行榜表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["排名", "玩家名稱", "時間", "移動次數", "日期"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)
        
        # 按鈕
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("重新整理")
        refresh_btn.clicked.connect(self.load_leaderboard)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("關閉")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # 設定視窗
        self.setWindowTitle("排行榜")
        self.setFixedSize(600, 500)
    
    def on_difficulty_changed(self, difficulty):
        """難度選擇改變時"""
        self.current_difficulty = difficulty
        self.load_leaderboard()
    
    def load_leaderboard(self):
        """載入排行榜資料"""
        records = self.database.get_leaderboard(
            difficulty=self.current_difficulty,
            limit=50
        )
        
        self.table.setRowCount(len(records))
        
        for idx, record in enumerate(records):
            # 排名
            self.table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            
            # 玩家名稱
            self.table.setItem(idx, 1, QTableWidgetItem(record['player_name']))
            
            # 時間
            time_seconds = record['time_seconds']
            minutes = int(time_seconds // 60)
            seconds = int(time_seconds % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.table.setItem(idx, 2, QTableWidgetItem(time_str))
            
            # 移動次數
            moves = record['moves_count'] if record['moves_count'] else "N/A"
            self.table.setItem(idx, 3, QTableWidgetItem(str(moves)))
            
            # 日期
            date_str = record['date'][:19] if record['date'] else "N/A"
            self.table.setItem(idx, 4, QTableWidgetItem(date_str))
        
        # 調整欄寬
        self.table.resizeColumnsToContents()

