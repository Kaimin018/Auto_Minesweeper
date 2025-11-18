"""
主選單視窗
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QMessageBox, QDialog, QLineEdit, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
from typing import Optional

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.game_window import GameWindow
from ui.leaderboard import LeaderboardWindow
from utils.database import Database
import config


class MainMenu(QMainWindow):
    """主選單視窗"""
    
    def __init__(self):
        super().__init__()
        self.database = Database(config.DATABASE_PATH)
        self.init_ui()
    
    def init_ui(self):
        """初始化使用者介面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 標題
        title = QLabel("踩地雷 AI 教學遊戲")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)
        
        subtitle = QLabel("選擇遊戲模式")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 14))
        layout.addWidget(subtitle)
        
        layout.addStretch()
        
        # 模式按鈕
        speed_mode_btn = QPushButton("計時模式")
        speed_mode_btn.setFont(QFont("Arial", 16))
        speed_mode_btn.setMinimumHeight(50)
        speed_mode_btn.clicked.connect(self.start_speed_mode)
        layout.addWidget(speed_mode_btn)
        
        tutorial_mode_btn = QPushButton("教學模式（開發中）")
        tutorial_mode_btn.setFont(QFont("Arial", 16))
        tutorial_mode_btn.setMinimumHeight(50)
        tutorial_mode_btn.setEnabled(False)
        layout.addWidget(tutorial_mode_btn)
        
        vs_ai_mode_btn = QPushButton("與 AI 對戰（開發中）")
        vs_ai_mode_btn.setFont(QFont("Arial", 16))
        vs_ai_mode_btn.setMinimumHeight(50)
        vs_ai_mode_btn.setEnabled(False)
        layout.addWidget(vs_ai_mode_btn)
        
        layout.addStretch()
        
        # 其他按鈕
        leaderboard_btn = QPushButton("排行榜")
        leaderboard_btn.setFont(QFont("Arial", 14))
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        layout.addWidget(leaderboard_btn)
        
        exit_btn = QPushButton("離開")
        exit_btn.setFont(QFont("Arial", 14))
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
        
        # 設定視窗
        self.setWindowTitle("踩地雷 AI 教學遊戲")
        self.setFixedSize(400, 500)
    
    def start_speed_mode(self):
        """開始計時模式"""
        # 選擇難度
        difficulty = self.select_difficulty()
        if not difficulty:
            return
        
        # 開啟遊戲視窗
        game_window = GameWindow(difficulty=difficulty)
        game_window.game_won.connect(
            lambda time, moves: self.on_game_won(difficulty, time, moves)
        )
        game_window.show()
    
    def select_difficulty(self) -> Optional[str]:
        """選擇難度對話框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("選擇難度")
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        beginner_btn = QPushButton("初級 (9x9, 10 地雷)")
        beginner_btn.clicked.connect(lambda: dialog.done(1))
        layout.addWidget(beginner_btn)
        
        intermediate_btn = QPushButton("中級 (16x16, 40 地雷)")
        intermediate_btn.clicked.connect(lambda: dialog.done(2))
        layout.addWidget(intermediate_btn)
        
        expert_btn = QPushButton("專家級 (30x16, 99 地雷)")
        expert_btn.clicked.connect(lambda: dialog.done(3))
        layout.addWidget(expert_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)
        layout.addWidget(cancel_btn)
        
        result = dialog.exec_()
        
        if result == 1:
            return 'beginner'
        elif result == 2:
            return 'intermediate'
        elif result == 3:
            return 'expert'
        return None
    
    def on_game_won(self, difficulty: str, elapsed_time: float, moves: int):
        """遊戲勝利時處理"""
        # 詢問玩家名稱
        name, ok = self.get_player_name()
        if not ok or not name:
            return
        
        # 儲存到排行榜
        settings = config.DIFFICULTY_SETTINGS[difficulty]
        self.database.save_record(
            player_name=name,
            difficulty=difficulty,
            time_seconds=elapsed_time,
            board_size=settings['board_size'],
            moves_count=moves
        )
        
        QMessageBox.information(
            self, 
            "記錄已儲存", 
            f"你的成績已儲存到排行榜！\n時間: {int(elapsed_time // 60):02d}:{int(elapsed_time % 60):02d}"
        )
    
    def get_player_name(self) -> tuple:
        """取得玩家名稱"""
        dialog = QDialog(self)
        dialog.setWindowTitle("輸入名稱")
        dialog.setFixedSize(300, 100)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        form_layout = QFormLayout()
        name_input = QLineEdit()
        name_input.setPlaceholderText("請輸入你的名稱")
        form_layout.addRow("名稱:", name_input)
        layout.addLayout(form_layout)
        
        button_layout = QVBoxLayout()
        ok_btn = QPushButton("確定")
        ok_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_input.text().strip()
            return (name if name else "匿名", True)
        return ("", False)
    
    def show_leaderboard(self):
        """顯示排行榜"""
        leaderboard_window = LeaderboardWindow(self.database, self)
        leaderboard_window.show()

