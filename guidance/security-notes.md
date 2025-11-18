# 安全注意事項

本文檔說明如何保護敏感資訊，避免意外提交到 Git 倉庫。

## 已保護的敏感資訊類型

### 1. 環境變數和配置

以下檔案類型會被自動忽略：
- `.env` 和 `.env.*` 檔案
- `*.local` 配置檔案
- `config.local.py`、`settings.local.py`

**建議做法**：
- 使用 `.env.example` 作為範本（此檔案會被追蹤）
- 在 `.env.example` 中只包含變數名稱，不包含實際值
- 每個開發者建立自己的 `.env` 檔案

### 2. 憑證和密鑰

以下檔案類型會被自動忽略：
- `*.key`、`*.pem`、`*.p12`、`*.pfx`
- `*.crt`、`*.cer`、`*.jks`
- `secrets/` 目錄
- `credentials/` 目錄
- `*.credentials`、`*.secret`、`*.token`
- `api_keys.txt`、`secrets.json`

**建議做法**：
- 永遠不要將真實的 API 金鑰或密碼提交到 Git
- 使用環境變數或配置管理工具
- 如果必須追蹤範本，使用 `*.example` 或 `*.template` 後綴

### 3. 資料庫文件

以下檔案會被自動忽略：
- `data/*.db`、`data/*.sqlite`、`data/*.sqlite3`
- 資料庫日誌文件（`*.db-journal`、`*.db-wal`、`*.db-shm`）

**注意**：
- `data/` 目錄結構會被保留（通過 `.gitkeep`）
- 每個開發者會有自己的本地資料庫
- 生產環境的資料庫應該使用外部服務

### 4. 日誌文件

以下檔案會被自動忽略：
- `*.log`、`*.log.*`
- `logs/` 目錄
- `*.out`

### 5. 本地開發文件

以下會被自動忽略：
- `test_data/`、`dev_data/`、`sample_data/`、`mock_data/`
- `*.test.db`、`*.dev.db`
- `notes/`、`personal/`、`scratch/` 目錄
- `TODO.local.md`、`NOTES.md`

## 檢查清單

在提交程式碼前，請確認：

- [ ] 沒有包含真實的 API 金鑰或密碼
- [ ] 沒有包含 `.env` 檔案（只有 `.env.example`）
- [ ] 沒有包含資料庫文件
- [ ] 沒有包含個人筆記或敏感資訊
- [ ] 沒有包含日誌文件

## 如果意外提交了敏感資訊

### 立即處理步驟

1. **立即撤銷提交**（如果還沒推送）：
   ```bash
   git reset HEAD~1
   ```

2. **如果已經推送**：
   - 立即更改所有暴露的密鑰和憑證
   - 從 Git 歷史中移除敏感資訊（使用 `git filter-branch` 或 BFG Repo-Cleaner）
   - 通知團隊成員更新本地倉庫

3. **檢查 Git 歷史**：
   ```bash
   git log --all --full-history -- <敏感檔案路徑>
   ```

## 最佳實踐

### 使用環境變數

```python
import os
from dotenv import load_dotenv

load_dotenv()  # 載入 .env 檔案

API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
```

### 使用配置範本

建立 `config.example.py`：

```python
# config.example.py
DATABASE_PATH = "data/leaderboard.db"
API_KEY = "your-api-key-here"  # 替換為實際值
```

然後在 `.gitignore` 中忽略 `config.py`，只追蹤 `config.example.py`。

### 使用 secrets 管理

對於生產環境，考慮使用：
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- 環境變數（在部署平台設定）

## 相關文件

- [.gitignore](../.gitignore) - 完整的忽略規則
- [開發環境設置](development-setup.md) - 開發環境配置
- [故障排除](troubleshooting.md) - 問題診斷

---

**重要提醒**：一旦敏感資訊被提交到 Git 並推送到遠端，即使後來刪除，歷史記錄中仍然存在。務必在提交前仔細檢查！

