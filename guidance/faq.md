# 常見問題 (FAQ)

## 安裝相關

### Q: 如何安裝 Python？

A: 從 [python.org](https://www.python.org/downloads/) 下載並安裝最新版本的 Python（3.8 或更高）。

### Q: 虛擬環境是什麼？為什麼需要？

A: 虛擬環境可以隔離專案的依賴套件，避免與其他專案衝突。雖然不是必須的，但強烈建議使用。

### Q: 如何知道虛擬環境已啟動？

A: 在命令提示字元前面會顯示 `(myenv)` 或類似的標記。

### Q: PyQt5 安裝失敗怎麼辦？

A: 
- **Windows**: 可能需要安裝 Visual C++ Redistributable
- **Linux**: 執行 `sudo apt-get install python3-pyqt5` 或 `sudo yum install python3-qt5`
- **macOS**: 使用 Homebrew：`brew install pyqt5`

## 執行相關

### Q: 執行 `python main.py` 時出現模組找不到的錯誤？

A: 確保：
1. 你在專案根目錄執行指令
2. 虛擬環境已啟動
3. 已安裝所有依賴：`pip install -r requirements.txt`

### Q: 遊戲視窗無法顯示？

A: 
- 檢查是否有錯誤訊息
- 確保 PyQt5 正確安裝
- 嘗試更新顯示驅動程式

### Q: 如何關閉遊戲？

A: 點擊視窗右上角的關閉按鈕，或使用 Alt+F4（Windows）。

## 遊戲相關

### Q: 第一次點擊會是地雷嗎？

A: 不會！遊戲保證第一次點擊不會是地雷，並且會自動展開周圍的空白區域。

### Q: 如何標記地雷？

A: 右鍵點擊格子即可標記。再次右鍵點擊可以取消標記。

### Q: 可以暫停遊戲嗎？

A: 目前不支援暫停功能。你可以關閉視窗，下次開啟時會開始新遊戲。

### Q: 如何查看排行榜？

A: 在主選單點擊「排行榜」按鈕即可查看。

### Q: 排行榜資料儲存在哪裡？

A: 資料儲存在 `data/leaderboard.db` SQLite 資料庫中。

## 技術相關

### Q: 使用哪個 Python 版本？

A: 建議使用 Python 3.8 或更高版本。專案已測試過 Python 3.8, 3.9, 3.10, 3.11, 3.12。

### Q: 如何更新依賴套件？

A: 執行 `pip install --upgrade -r requirements.txt`

### Q: 可以修改遊戲設定嗎？

A: 可以！編輯 `config.py` 檔案可以修改難度設定、顏色等。

### Q: 如何貢獻程式碼？

A: 歡迎提交 Pull Request！請先查看[貢獻指南](contributing.md)。

## 其他問題

### Q: 遊戲有音效嗎？

A: 目前沒有，但未來可能會添加。

### Q: 可以自訂主題嗎？

A: 目前不支援，但可以通過修改 `config.py` 中的顏色設定來調整。

### Q: 支援多語言嗎？

A: 目前只有繁體中文，未來可能會添加其他語言。

### Q: 如何回報問題？

A: 請在 GitHub 上建立 Issue，詳細描述問題和重現步驟。

## 需要更多幫助？

- 查看[故障排除指南](troubleshooting.md)
- 查看[遊戲說明](game-guide.md)
- 查看[開發文檔](../architecture.md)

