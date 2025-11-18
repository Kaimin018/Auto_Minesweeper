# 專案結構遷移記錄

本文檔記錄了將專案從 `Auto_Minesweeper/` 子目錄遷移到根目錄 `10_auto_minesweeper/` 的完整過程。

## 遷移日期

2025-11-19

## 遷移原因

1. **GitHub 檔案連結**：GitHub 的檔案連結指向專案根目錄，為了讓連結正確指向檔案，需要將所有檔案移到根目錄
2. **專案結構簡化**：減少不必要的目錄層級，讓專案結構更清晰
3. **使用便利性**：檔案在根目錄更容易訪問和管理

## 遷移步驟

### 1. Git 倉庫遷移

將 Git 倉庫從 `Auto_Minesweeper/.git/` 移到根目錄：

```bash
# 移動 .git 目錄到根目錄
Move-Item -Path "Auto_Minesweeper\.git" -Destination ".git" -Force
```

**結果**：
- ✅ Git 倉庫現在在根目錄 `10_auto_minesweeper/.git/`
- ✅ 保留所有 Git 歷史記錄
- ✅ 遠端倉庫設定保持不變：`https://github.com/Kaimin018/Auto_Minesweeper.git`
- ✅ 當前分支：`main`

### 2. 檔案移動

將 `Auto_Minesweeper/` 目錄下的所有檔案和資料夾（除了 `myenv/` 虛擬環境）移動到根目錄：

**移動的檔案和資料夾**：
- `main.py` → 根目錄
- `config.py` → 根目錄
- `requirements.txt` → 根目錄
- `architecture.md` → 根目錄
- `How-to.md` → 根目錄
- `README.md` → 根目錄
- `STAGE1_COMPLETE.md` → 根目錄
- `.gitignore` → 根目錄
- `core/` → 根目錄
- `ai/` → 根目錄
- `ui/` → 根目錄
- `utils/` → 根目錄
- `modes/` → 根目錄

**保留在原位置**：
- `Auto_Minesweeper/myenv/` - 虛擬環境（不需要移動）

### 2. 建立 guidance 資料夾

在根目錄建立 `guidance/` 資料夾，包含以下文件：

- `README.md` - 指南總覽
- `installation.md` - 安裝指南
- `quick-start.md` - 快速開始
- `game-guide.md` - 遊戲說明
- `features.md` - 功能介紹
- `faq.md` - 常見問題
- `troubleshooting.md` - 故障排除
- `development-setup.md` - 開發環境設置
- 程式碼結構說明已整合到 `architecture.md`
- `contributing.md` - 貢獻指南
- `migration-log.md` - 本遷移記錄

### 3. 路徑修正

修正所有文件中的路徑引用：

#### README.md
- ✅ 將 `Auto_Minesweeper/` 改為 `10_auto_minesweeper/`
- ✅ 將 `main_new.py` 改為 `main.py`
- ✅ 更新專案結構圖
- ✅ 添加 `guidance/` 資料夾到結構圖
- ✅ 更新注意事項，移除舊的 `main_new.py` 引用

#### architecture.md
- ✅ 將 `Auto_Minesweeper/` 改為 `10_auto_minesweeper/`
- ✅ 更新專案結構圖
- ✅ 添加 `guidance/` 資料夾到結構圖

#### STAGE1_COMPLETE.md
- ✅ 將 `Auto_Minesweeper/` 改為 `10_auto_minesweeper/`
- ✅ 將 `main_new.py` 改為 `main.py`
- ✅ 更新專案結構圖
- ✅ 添加 `guidance/` 資料夾到結構圖

#### How-to.md
- ✅ 移除 `cd Auto_Minesweeper` 指令（檔案已在根目錄）
- ✅ 添加指向 `guidance/` 資料夾的說明

### 5. Git 狀態檢查

遷移後的 Git 狀態：

```bash
# 檢查 Git 狀態
git status

# 檢查遠端設定
git remote -v

# 檢查當前分支
git branch
```

**注意**：遷移後會顯示大量檔案變更（移動、新增等），需要提交這些變更。

### 6. 檔案名稱統一

- ✅ `main_new.py` → `main.py`（已在遷移前完成）
- ✅ 所有引用 `main_new.py` 的地方都已更新為 `main.py`

## 遷移後的專案結構

```
10_auto_minesweeper/          # GitHub 根目錄
├── main.py                   # 主入口
├── config.py                 # 配置設定
├── requirements.txt          # 依賴套件
├── architecture.md          # 架構文件
├── How-to.md                # 快速指令參考
├── README.md                # 專案說明
├── STAGE1_COMPLETE.md       # 階段一完成報告
│
├── core/                    # 核心遊戲邏輯
│   ├── __init__.py
│   ├── game_engine.py
│   └── board.py
│
├── ai/                      # AI 模組
│   ├── __init__.py
│   ├── probability_calculator.py
│   └── strategies.py
│
├── ui/                      # 使用者介面
│   ├── __init__.py
│   ├── main_menu.py
│   ├── game_window.py
│   └── leaderboard.py
│
├── utils/                   # 工具函數
│   ├── __init__.py
│   └── database.py
│
├── modes/                   # 遊戲模式（未來擴展）
│   └── __init__.py
│
├── data/                    # 資料儲存
│   └── leaderboard.db       # SQLite 資料庫（自動建立）
│
├── guidance/                # 使用指南（新增）
│   ├── README.md
│   ├── installation.md
│   ├── quick-start.md
│   ├── game-guide.md
│   ├── features.md
│   ├── faq.md
│   ├── troubleshooting.md
│   ├── development-setup.md
│   ├── (code-structure.md 已整合到 architecture.md)
│   ├── contributing.md
│   └── migration-log.md      # 本文件
│
└── Auto_Minesweeper/        # 僅保留 myenv
    └── myenv/               # 虛擬環境（不需要移動）
```

## 影響範圍

### 使用者影響

- ✅ **正面影響**：檔案路徑更清晰，GitHub 連結正確
- ✅ **無負面影響**：所有功能保持不變，只是檔案位置改變

### 開發者影響

- ✅ **需要更新**：如果本地有舊的專案結構，需要重新克隆或更新
- ✅ **路徑引用**：所有程式碼中的路徑引用已自動更新（使用相對路徑）

### Git 影響

- ✅ **檔案狀態**：所有檔案顯示為移動（Moved）而非刪除和新增
- ✅ **歷史保留**：Git 歷史完整保留
- ✅ **.gitignore**：已更新，包含 `.python-version`

## 驗證清單

- [x] Git 倉庫已移動到根目錄
- [x] 所有檔案已移動到根目錄
- [x] 所有路徑引用已更新
- [x] `guidance/` 資料夾已建立並包含所有指南文件
- [x] `README.md` 已更新
- [x] `architecture.md` 已更新
- [x] `STAGE1_COMPLETE.md` 已更新
- [x] `How-to.md` 已更新
- [x] 所有 `main_new.py` 引用已改為 `main.py`
- [x] `.gitignore` 已更新
- [x] 專案結構圖已更新
- [x] Git 狀態正常，可以追蹤變更

## 後續工作

### 已完成
- ✅ 檔案移動
- ✅ 路徑修正
- ✅ 文檔更新
- ✅ guidance 資料夾建立

### 建議
- [ ] 更新 GitHub 專案描述（如果有）
- [ ] 通知協作者專案結構變更
- [ ] 更新任何外部文檔或連結

## 注意事項

1. **虛擬環境**：`Auto_Minesweeper/myenv/` 保留在原位置，如果需要可以重新建立
2. **資料庫**：`data/leaderboard.db` 會自動在根目錄建立，不影響現有資料
3. **Git 歷史**：所有檔案移動都保留了 Git 歷史，可以使用 `git log --follow` 查看
4. **Git 倉庫位置**：`.git/` 目錄已從 `Auto_Minesweeper/` 移到根目錄，現在可以在根目錄使用所有 Git 指令
5. **遠端倉庫**：遠端 URL 保持不變，仍指向 `https://github.com/Kaimin018/Auto_Minesweeper.git`

## 回滾方案

如果需要回滾到舊的結構：

1. 使用 Git 回滾到遷移前的提交
2. 或手動將檔案移回 `Auto_Minesweeper/` 目錄
3. 更新所有路徑引用

## 相關文件

- [專案架構](../architecture.md)
- [快速開始](quick-start.md)
- [開發環境設置](development-setup.md)
- [架構文件](../architecture.md)（包含程式碼結構說明）

---

**遷移完成日期**：2025-11-19  
**遷移狀態**：✅ 已完成  
**驗證狀態**：✅ 已驗證

