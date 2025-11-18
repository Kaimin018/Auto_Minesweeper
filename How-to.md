# 建立虛擬環境和安裝依賴

# 重要：所有指令都需要在專案根目錄（10_auto_minesweeper）下執行
# 更多詳細指南請查看 guidance/ 資料夾

# 0. 如果使用 pyenv 管理 Python 版本（可選）
# 如果遇到 "No global/local python version has been set yet" 錯誤：
# pyenv install 3.12.10  # 或你使用的 Python 版本

# 1. 建立虛擬環境
python -m venv myenv

# 2. 啟動虛擬環境
# Windows:
myenv\Scripts\activate
# Linux/Mac:
# source myenv/bin/activate

# 3. 安裝依賴套件
pip install -r requirements.txt

# 開始遊戲

# 確保虛擬環境已啟動後，執行：
python main.py

# 其他指令

# 建立 requirement 檔案（如果需要）
pip freeze > requirement.txt

# 執行測試
pytest tests
