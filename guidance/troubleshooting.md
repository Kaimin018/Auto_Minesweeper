# 故障排除

本指南幫助你診斷和解決常見問題。

## 安裝問題

### 問題：`python: command not found`

**原因**：Python 未安裝或未加入 PATH

**解決方案**：
1. 安裝 Python 從 [python.org](https://www.python.org/downloads/)
2. 安裝時勾選「Add Python to PATH」
3. 或手動將 Python 加入系統 PATH

### 問題：`pip: command not found`

**原因**：pip 未安裝或未加入 PATH

**解決方案**：
```bash
python -m ensurepip --upgrade
```

### 問題：`No module named 'PyQt5'`

**原因**：PyQt5 未安裝

**解決方案**：
```bash
pip install PyQt5
```

如果仍然失敗，請參考[安裝指南](installation.md)中的 PyQt5 安裝說明。

### 問題：虛擬環境無法建立

**原因**：可能是 Python 版本問題或權限問題

**解決方案**：
1. 檢查 Python 版本：`python --version`
2. 確保有寫入權限
3. 嘗試使用完整路徑：`python -m venv C:\path\to\myenv`

## 執行問題

### 問題：`ModuleNotFoundError: No module named 'xxx'`

**原因**：模組未安裝或路徑問題

**解決方案**：
1. 確保虛擬環境已啟動
2. 安裝缺失的模組：`pip install <module-name>`
3. 重新安裝所有依賴：`pip install -r requirements.txt`

### 問題：遊戲視窗無法開啟

**原因**：可能是 PyQt5 問題或顯示驅動問題

**解決方案**：
1. 檢查錯誤訊息
2. 更新 PyQt5：`pip install --upgrade PyQt5`
3. 更新顯示驅動程式
4. 嘗試在終端機執行以查看詳細錯誤

### 問題：遊戲執行緩慢

**原因**：可能是系統資源不足或程式碼問題

**解決方案**：
1. 關閉其他應用程式釋放記憶體
2. 檢查是否有背景程式占用資源
3. 對於大型棋盤（30x16），這是正常的

### 問題：資料庫錯誤

**原因**：資料庫檔案損壞或權限問題

**解決方案**：
1. 刪除 `data/leaderboard.db` 讓程式重新建立
2. 確保 `data/` 目錄有寫入權限
3. 檢查磁碟空間是否充足

## 遊戲問題

### 問題：點擊沒有反應

**原因**：可能是 UI 事件處理問題

**解決方案**：
1. 重新啟動遊戲
2. 檢查是否有錯誤訊息
3. 確保遊戲視窗處於活動狀態

### 問題：排行榜無法顯示

**原因**：資料庫問題或 UI 問題

**解決方案**：
1. 檢查 `data/leaderboard.db` 是否存在
2. 嘗試重新啟動遊戲
3. 檢查資料庫是否有記錄

### 問題：計時器不準確

**原因**：可能是系統時間問題

**解決方案**：
1. 檢查系統時間是否正確
2. 重新啟動遊戲
3. 這通常是正常的，計時器精度為 0.1 秒

## 開發問題

### 問題：導入模組失敗

**原因**：路徑問題或模組未安裝

**解決方案**：
1. 確保在專案根目錄執行
2. 檢查 `sys.path` 是否包含專案目錄
3. 使用相對導入或絕對導入

### 問題：Git 相關問題

**原因**：可能是 .gitignore 或版本控制問題

**解決方案**：
1. 檢查 `.gitignore` 是否正確
2. 確保不提交虛擬環境和資料庫檔案
3. 使用 `git status` 檢查檔案狀態

## 系統特定問題

### Windows

**問題**：PowerShell 執行策略錯誤

**解決方案**：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**問題**：路徑包含空格

**解決方案**：使用引號包圍路徑，或避免在路徑中使用空格

### macOS

**問題**：權限問題

**解決方案**：
```bash
chmod +x myenv/bin/activate
```

### Linux

**問題**：缺少系統依賴

**解決方案**：
```bash
sudo apt-get install python3-pyqt5 python3-dev
```

## 診斷步驟

如果遇到問題，請按以下步驟診斷：

1. **檢查 Python 版本**
   ```bash
   python --version
   ```

2. **檢查虛擬環境**
   ```bash
   which python  # 應該指向 myenv
   ```

3. **檢查已安裝套件**
   ```bash
   pip list
   ```

4. **檢查專案結構**
   ```bash
   ls -la  # 確認所有檔案都在
   ```

5. **查看錯誤訊息**
   - 在終端機執行以查看完整錯誤
   - 檢查是否有堆疊追蹤

## 取得幫助

如果以上方法都無法解決問題：

1. 查看[常見問題](faq.md)
2. 查看[GitHub Issues](https://github.com/your-repo/issues)
3. 建立新的 Issue，包含：
   - 作業系統和版本
   - Python 版本
   - 完整錯誤訊息
   - 重現步驟

## 預防措施

為了避免問題：

1. **使用虛擬環境**：隔離依賴
2. **定期更新**：保持 Python 和套件最新
3. **備份資料**：定期備份 `data/` 目錄
4. **閱讀文檔**：查看[安裝指南](installation.md)和[使用指南](game-guide.md)

