# 安裝指南

本指南將幫助你安裝和設置踩地雷 AI 教學遊戲。

## 系統需求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows, macOS, 或 Linux
- **記憶體**: 至少 512MB 可用記憶體
- **硬碟空間**: 約 100MB

## 安裝步驟

### 1. 檢查 Python 版本

```bash
python --version
```

如果沒有安裝 Python 或版本過舊，請從 [python.org](https://www.python.org/downloads/) 下載安裝。

### 2. 克隆或下載專案

如果你使用 Git：

```bash
git clone <repository-url>
cd 10_auto_minesweeper
```

或者直接下載 ZIP 檔案並解壓縮。

### 3. 建立虛擬環境（建議）

```bash
# 建立虛擬環境
python -m venv myenv

# 啟動虛擬環境
# Windows:
myenv\Scripts\activate
# Linux/Mac:
source myenv/bin/activate
```

### 4. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 5. 驗證安裝

```bash
python main.py
```

如果遊戲視窗正常開啟，表示安裝成功！

## 使用 pyenv（可選）

如果你使用 pyenv 管理 Python 版本：

```bash
# 安裝指定版本的 Python（如果尚未安裝）
pyenv install 3.12.10

# 在專案目錄設置本地版本
pyenv local 3.12.10
```

## 故障排除

### 問題：找不到 requirements.txt

**解決方案**：確保你在專案根目錄（`10_auto_minesweeper`）執行指令。

### 問題：PyQt5 安裝失敗

**解決方案**：
- Windows: 可能需要安裝 Visual C++ Redistributable
- Linux: 可能需要安裝系統依賴：`sudo apt-get install python3-pyqt5`
- macOS: 使用 Homebrew：`brew install pyqt5`

### 問題：虛擬環境無法啟動

**解決方案**：
- 檢查 Python 是否正確安裝
- 確保使用正確的啟動指令（Windows 使用 `\`，Linux/Mac 使用 `/`）

## 下一步

安裝完成後，請查看：
- [快速開始指南](quick-start.md)
- [遊戲說明](game-guide.md)

