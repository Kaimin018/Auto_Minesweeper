"""
遊戲視窗 - 顯示遊戲板和處理使用者輸入
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QMessageBox, QDialog, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QMouseEvent
from typing import Optional
import sys
import os

# 添加專案根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from core.game_engine import GameEngine


class CellButton(QPushButton):
    """自定義格子按鈕，支援右鍵點擊"""
    
    right_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_clicked.emit)
    
    def mousePressEvent(self, event: QMouseEvent):
        """處理滑鼠點擊"""
        if event.button() == Qt.RightButton:
            self.right_clicked.emit()
        else:
            super().mousePressEvent(event)


class GameWindow(QMainWindow):
    """遊戲主視窗"""
    
    game_won = pyqtSignal(float, int)  # 遊戲勝利信號 (time, moves)
    game_lost = pyqtSignal()  # 遊戲失敗信號
    
    def __init__(self, difficulty: str = 'beginner', parent=None):
        super().__init__(parent)
        self.difficulty = difficulty
        self.settings = config.DIFFICULTY_SETTINGS[difficulty]
        
        # 初始化遊戲引擎
        self.game_engine = GameEngine(
            rows=self.settings['rows'],
            cols=self.settings['cols'],
            num_mines=self.settings['mines']
        )
        self.game_engine.start_new_game()
        
        # UI 元件
        self.cell_buttons = []
        self.timer_label = None
        self.mines_label = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.init_ui()
        self.update_display()
    
    def init_ui(self):
        """初始化使用者介面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 頂部資訊欄
        info_layout = QHBoxLayout()
        
        # 計時器
        self.timer_label = QLabel("時間: 00:00")
        self.timer_label.setFont(QFont("Arial", 14, QFont.Bold))
        info_layout.addWidget(self.timer_label)
        
        info_layout.addStretch()
        
        # 剩餘地雷數
        self.mines_label = QLabel(f"地雷: {self.settings['mines']}")
        self.mines_label.setFont(QFont("Arial", 14, QFont.Bold))
        info_layout.addWidget(self.mines_label)
        
        main_layout.addLayout(info_layout)
        
        # 遊戲板
        board_widget = QWidget()
        board_layout = QGridLayout()
        board_layout.setSpacing(2)
        board_widget.setLayout(board_layout)
        
        self.cell_buttons = []
        for r in range(self.settings['rows']):
            row = []
            for c in range(self.settings['cols']):
                btn = CellButton()
                btn.setFixedSize(config.CELL_SIZE, config.CELL_SIZE)
                btn.setFont(QFont("Arial", 12, QFont.Bold))
                
                # 連接信號
                btn.clicked.connect(lambda checked, row=r, col=c: self.handle_cell_click(row, col))
                btn.right_clicked.connect(lambda row=r, col=c: self.handle_cell_right_click(row, col))
                
                row.append(btn)
                board_layout.addWidget(btn, r, c)
            self.cell_buttons.append(row)
        
        main_layout.addWidget(board_widget)
        
        # 底部按鈕
        button_layout = QHBoxLayout()
        
        new_game_btn = QPushButton("新遊戲")
        new_game_btn.clicked.connect(self.new_game)
        button_layout.addWidget(new_game_btn)
        
        button_layout.addStretch()
        
        back_btn = QPushButton("返回主選單")
        back_btn.clicked.connect(self.close)
        button_layout.addWidget(back_btn)
        
        main_layout.addLayout(button_layout)
        
        # 設定視窗
        self.setWindowTitle(f"踩地雷 - {self.settings['name']}")
        self.setFixedSize(
            self.settings['cols'] * (config.CELL_SIZE + 4) + 40,
            self.settings['rows'] * (config.CELL_SIZE + 4) + 120
        )
    
    def handle_cell_click(self, row: int, col: int):
        """處理格子點擊"""
        if self.game_engine.get_game_status() != GameEngine.STATUS_PLAYING:
            return
        
        # 開始計時（第一次點擊時）
        if not self.timer.isActive():
            self.timer.start(100)  # 每 100ms 更新一次
        
        result = self.game_engine.click_cell(row, col)
        
        if result['exploded']:
            # 踩到地雷
            self.timer.stop()
            self.reveal_all_cells()
            self.game_lost.emit()
            QMessageBox.critical(self, "遊戲結束", "你踩到地雷了！")
        elif result['game_status'] == GameEngine.STATUS_WON:
            # 勝利
            self.timer.stop()
            elapsed_time = self.game_engine.get_elapsed_time()
            moves = self.game_engine.get_moves_count()
            self.game_won.emit(elapsed_time, moves)
            self.show_win_dialog(elapsed_time, moves)
        
        self.update_display()
    
    def handle_cell_right_click(self, row: int, col: int):
        """處理格子右鍵點擊（標記）"""
        if self.game_engine.get_game_status() != GameEngine.STATUS_PLAYING:
            return
        
        result = self.game_engine.flag_cell(row, col)
        if result['success']:
            self.update_display()
    
    def update_display(self):
        """更新顯示"""
        board_state = self.game_engine.get_board_state()
        
        for r in range(self.settings['rows']):
            for c in range(self.settings['cols']):
                btn = self.cell_buttons[r][c]
                cell_state = board_state[r][c]
                
                if cell_state == 0:  # 未揭開
                    btn.setText("")
                    btn.setStyleSheet("background-color: #C0C0C0; border: 2px solid #808080;")
                elif cell_state == 9:  # 已標記
                    btn.setText("🚩")
                    btn.setStyleSheet("background-color: #FFC8C8; border: 2px solid #808080;")
                elif cell_state == -1:  # 地雷（遊戲結束時）
                    btn.setText("💣")
                    btn.setStyleSheet("background-color: #FF0000; border: 2px solid #808080;")
                else:  # 數字 1-8
                    btn.setText(str(cell_state))
                    color = config.COLORS['numbers'].get(cell_state, (0, 0, 0))
                    btn.setStyleSheet(
                        f"background-color: #F0F0F0; "
                        f"border: 1px solid #808080; "
                        f"color: rgb({color[0]}, {color[1]}, {color[2]});"
                    )
        
        # 更新剩餘地雷數
        remaining = self.game_engine.get_remaining_mines()
        self.mines_label.setText(f"地雷: {remaining}")
    
    def update_timer(self):
        """更新計時器顯示"""
        elapsed = self.game_engine.get_elapsed_time()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        self.timer_label.setText(f"時間: {minutes:02d}:{seconds:02d}")
    
    def reveal_all_cells(self):
        """揭開所有格子（遊戲結束時）"""
        self.game_engine.reveal_all_mines()
        self.update_display()
    
    def new_game(self):
        """開始新遊戲"""
        self.timer.stop()
        self.game_engine.start_new_game()
        self.update_display()
        self.timer_label.setText("時間: 00:00")
    
    def show_win_dialog(self, elapsed_time: float, moves: int):
        """顯示勝利對話框"""
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        msg = QMessageBox(self)
        msg.setWindowTitle("恭喜！")
        msg.setText(f"🎉 你贏了！\n\n時間: {minutes:02d}:{seconds:02d}\n移動次數: {moves}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def closeEvent(self, event):
        """關閉視窗時停止計時器"""
        self.timer.stop()
        event.accept()

