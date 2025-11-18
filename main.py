"""
主入口 - AI 輔助踩地雷教學遊戲
"""
import sys
import os

# 添加專案根目錄到路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from ui.main_menu import MainMenu


def main():
    """主函數"""
    app = QApplication(sys.argv)
    
    # 設定應用程式樣式
    app.setStyle('Fusion')
    
    # 建立並顯示主選單
    menu = MainMenu()
    menu.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

