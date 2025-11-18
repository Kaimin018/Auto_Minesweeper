# 踩地雷 AI 教學遊戲 - 架構文件

## 專案概述

這是一個 AI 輔助的踩地雷教學遊戲，旨在幫助玩家學習踩地雷的策略和機率判斷技巧。

## 系統架構

### 目錄結構

```
10_auto_minesweeper/
├── main.py                    # 主入口（模式選擇選單）
├── config.py                  # 全域配置設定
├── requirements.txt           # Python 依賴套件
├── architecture.md            # 本架構文件
├── How-to.md                  # 快速指令參考
├── README.md                  # 專案說明
│
├── core/                      # 核心遊戲邏輯
│   ├── __init__.py
│   ├── game_engine.py        # 遊戲引擎（生成、狀態管理）
│   └── board.py              # 遊戲板類別
│
├── ai/                        # AI 相關模組
│   ├── __init__.py
│   ├── probability_calculator.py  # 機率計算引擎
│   ├── teacher.py            # 教學模式 AI（未來實作）
│   ├── opponent.py           # 對戰模式 AI（未來實作）
│   └── strategies.py         # 各種求解策略
│
├── modes/                     # 三種遊戲模式
│   ├── __init__.py
│   ├── tutorial_mode.py      # 教學模式（未來實作）
│   ├── vs_ai_mode.py         # 對戰模式（未來實作）
│   └── speed_mode.py         # 計時模式（階段一）
│
├── ui/                        # 使用者介面
│   ├── __init__.py
│   ├── main_menu.py          # 主選單視窗
│   ├── game_window.py        # 遊戲視窗（階段一）
│   └── leaderboard.py        # 排行榜顯示（階段一）
│
├── data/                      # 資料儲存
│   ├── leaderboard.db        # SQLite 排行榜資料庫
│   └── ai_models/            # 訓練好的 AI 模型（未來）
│
├── utils/                     # 工具函數
│   ├── __init__.py
│   ├── database.py           # 資料庫操作
│   └── helpers.py            # 輔助函數
│
├── guidance/                  # 使用指南
│   ├── installation.md
│   ├── quick-start.md
│   ├── game-guide.md
│   ├── features.md
│   ├── faq.md
│   ├── troubleshooting.md
│   ├── development-setup.md
│   ├── contributing.md
│   ├── security-notes.md
│   └── migration-log.md
│
├── testcases/                 # 測試檔案
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_game_engine.py
│   ├── test_game_logic.py
│   └── README.md
│
└── data/                      # 資料儲存
    ├── leaderboard.db        # SQLite 資料庫
    └── .gitkeep              # 保持目錄結構
```

## 核心模組設計

### 1. core/board.py - 遊戲板類別

**職責：** 管理遊戲板的資料結構和基本操作

**主要類別：**
```python
class Board:
    - __init__(rows, cols, mines, first_click)  # 初始化遊戲板，生成地雷
    - get_cell_value(row, col)  # 取得格子值
    - is_mine(row, col)  # 是否為地雷
    - is_revealed(row, col)  # 是否已揭開
    - is_flagged(row, col)  # 是否已標記
    - is_unrevealed(row, col)  # 是否未揭開且未標記
    - reveal_cell(row, col)  # 揭開格子（自動展開空白區域）
    - toggle_flag(row, col)  # 標記/取消標記
    - get_neighbors(row, col)  # 取得鄰居格子
    - check_win()  # 檢查是否勝利
    - get_flagged_count()  # 取得標記數量
    - get_revealed_count()  # 取得已揭開數量
    - get_board_state_for_ai()  # 取得供 AI 使用的狀態
```

**關鍵方法：**
- `_generate_mines()`: 生成地雷配置（確保第一次點擊位置不是地雷）
- `_calculate_numbers()`: 計算每個格子的數字（周圍地雷數）

### 2. core/game_engine.py - 遊戲引擎

**職責：** 管理遊戲的整體狀態和邏輯

**主要類別：**
```python
class GameEngine:
    - __init__(rows, cols, num_mines)  # 初始化遊戲引擎
    - start_new_game(first_click)  # 開始新遊戲
    - click_cell(row, col)  # 點擊格子，返回結果字典
    - flag_cell(row, col)  # 標記/取消標記
    - get_board_state()  # 取得當前遊戲狀態（供 UI 顯示）
    - get_game_status()  # 取得遊戲狀態（playing/won/lost）
    - get_cell_value(row, col)  # 取得格子值（僅已揭開時有效）
    - is_cell_revealed(row, col)  # 檢查格子是否已揭開
    - is_cell_flagged(row, col)  # 檢查格子是否已標記
    - get_elapsed_time()  # 取得經過時間（秒）
    - get_remaining_mines()  # 取得剩餘地雷數
    - get_moves_count()  # 取得移動次數
    - reveal_all_mines()  # 揭開所有地雷（遊戲結束時）
```

**狀態管理：**
- `STATUS_PLAYING`: 遊戲進行中
- `STATUS_WON`: 遊戲勝利
- `STATUS_LOST`: 遊戲失敗

### 3. ai/probability_calculator.py - 機率計算引擎

**職責：** 計算每個未知格子的地雷機率，考慮多個約束條件

**主要類別：**
```python
class ProbabilityCalculator:
    - __init__(board_state, rows, cols, total_mines)  # 初始化機率計算器
    - calculate_probabilities()  # 計算所有格子的機率
    - get_cell_probability(row, col)  # 取得特定格子的機率
    - find_safe_cells()  # 找出機率為 0 的安全格子
    - find_mine_cells()  # 找出機率為 1 的地雷格子
    - find_best_move()  # 找出最佳下一步（機率最低的格子）
```

**關鍵方法：**
- `_find_deterministic_cells()`: 使用約束傳播找出確定安全或確定是地雷的格子
- `_extract_constraints()`: 提取所有約束條件
- `_calculate_cell_probability()`: 計算特定格子的地雷機率

**演算法：**
1. **約束傳播**：從已知數字推導鄰居的機率
2. **多約束整合**：考慮多個數字方塊的共同約束
3. **機率計算**：使用約束滿足問題（CSP）方法，結合全局機率

### 4. ai/strategies.py - 基礎求解策略

**職責：** 基礎求解邏輯，從原 main.py 提取

**主要類別：**
```python
class BasicSolver:
    - __init__(board)  # 初始化求解器
    - find_next_move()  # 找出下一步行動（'click' 或 'flag'）
```

**策略：**
- 策略 1：找出安全的點擊（數字方塊周圍的旗子數等於數字）
- 策略 2：找出地雷並標記（數字方塊周圍的未開方塊數等於數字）

### 5. ui/main_menu.py - 主選單視窗

**職責：** 主選單視窗，提供模式選擇和難度選擇

**主要類別：**
```python
class MainMenu(QMainWindow):
    - __init__()  # 初始化主選單
    - start_speed_mode()  # 開始計時模式
    - select_difficulty()  # 選擇難度對話框
    - on_game_won()  # 遊戲勝利時處理（儲存到排行榜）
    - get_player_name()  # 取得玩家名稱
    - show_leaderboard()  # 顯示排行榜
```

### 6. ui/game_window.py - 遊戲視窗

**職責：** 顯示遊戲板，處理使用者輸入，顯示計時器和剩餘地雷數

**主要類別：**
```python
class CellButton(QPushButton):
    # 自定義格子按鈕，支援右鍵點擊
    - right_clicked  # 右鍵點擊信號

class GameWindow(QMainWindow):
    - __init__(difficulty, parent)  # 初始化遊戲視窗
    - handle_cell_click(row, col)  # 處理格子點擊
    - handle_cell_right_click(row, col)  # 處理格子右鍵（標記）
    - update_display()  # 更新顯示
    - update_timer()  # 更新計時器
    - reveal_all_cells()  # 揭開所有格子（遊戲結束時）
    - new_game()  # 開始新遊戲
    - show_win_dialog()  # 顯示勝利對話框
```

**信號：**
- `game_won`: 遊戲勝利信號（time, moves）
- `game_lost`: 遊戲失敗信號

### 7. ui/leaderboard.py - 排行榜視窗

**職責：** 顯示排行榜記錄，支援按難度篩選

**主要類別：**
```python
class LeaderboardWindow(QMainWindow):
    - __init__(database, parent)  # 初始化排行榜視窗
    - load_leaderboard()  # 載入排行榜資料
    - on_difficulty_changed()  # 難度選擇改變處理
```

### 8. utils/database.py - 資料庫操作

**職責：** 管理 SQLite 資料庫，提供排行榜的 CRUD 操作

**主要類別：**
```python
class Database:
    - __init__(db_path)  # 初始化資料庫（自動建立表結構）
    - save_record(name, difficulty, time_seconds, board_size, moves_count)  # 儲存記錄
    - get_leaderboard(difficulty, limit)  # 取得排行榜
    - get_best_time(difficulty)  # 取得特定難度的最佳時間
    - get_player_stats(player_name)  # 取得玩家統計
    - clear_leaderboard(difficulty)  # 清空排行榜（可選）
```

## 資料庫設計

### leaderboard 表結構

```sql
CREATE TABLE leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    difficulty TEXT NOT NULL,      -- 'beginner', 'intermediate', 'expert'
    time_seconds REAL NOT NULL,
    board_size TEXT NOT NULL,      -- '9x9', '16x16', '30x16'
    moves_count INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_difficulty_time ON leaderboard(difficulty, time_seconds);
```

## 遊戲難度設定

| 難度 | 棋盤大小 | 地雷數 | 說明 |
|------|---------|--------|------|
| beginner | 9x9 | 10 | 初學者 |
| intermediate | 16x16 | 40 | 中級 |
| expert | 30x16 | 99 | 專家級 |

## 實作階段

### 階段一：基礎架構（當前）
- ✅ 建立架構文件
- ⏳ 重構現有代碼，分離遊戲引擎
- ⏳ 實作機率計算引擎
- ⏳ 建立基本 UI 框架
- ⏳ 實作單人計時模式

### 階段二：教學模式（未來）
- 實作教學模式 UI
- 整合機率計算與視覺化
- 實作推理過程展示

### 階段三：對戰模式（未來）
- 實作對戰模式
- 優化 AI 策略
- 實作 AI 訓練（可選）

### 階段四：優化與擴展（未來）
- 更多難度與自訂選項
- 統計與分析功能
- 效能優化

## 技術棧

- **語言：** Python 3.8+
- **UI 框架：** PyQt5
- **資料庫：** SQLite3
- **圖像處理：** OpenCV（保留原功能，未來可選）
- **其他：** NumPy（用於機率計算）

## 資料流和設計模式

### 遊戲流程

```
main.py
  └─> MainMenu
       └─> GameWindow
            └─> GameEngine
                 └─> Board
```

### 資料流

```
User Input → GameWindow → GameEngine → Board
                                      ↓
                              Update Display
```

### MVC 架構

- **Model**: `core/board.py`, `core/game_engine.py`
- **View**: `ui/` 目錄下的所有檔案
- **Controller**: `GameEngine` 作為控制器

### 觀察者模式

- PyQt5 的信號槽機制實現觀察者模式（如 `game_won`、`game_lost` 信號）

## 擴展點

### 添加新遊戲模式

1. 在 `modes/` 目錄下建立新檔案
2. 實作模式類別
3. 在 `MainMenu` 中添加按鈕

### 添加新 AI 策略

1. 在 `ai/strategies.py` 中添加新策略類別
2. 或建立新的策略檔案

### 修改 UI 主題

1. 修改 `config.py` 中的顏色設定
2. 或建立新的主題配置檔案

## 依賴關係

```
main.py
  ├─> ui/main_menu.py
  │     ├─> ui/game_window.py
  │     │     ├─> core/game_engine.py
  │     │     │     └─> core/board.py
  │     │     └─> config.py
  │     └─> ui/leaderboard.py
  │           └─> utils/database.py
  └─> config.py
```

## API 設計原則

1. **模組化：** 每個模組職責單一明確
2. **可擴展：** 易於添加新功能和新模式
3. **可測試：** 核心邏輯與 UI 分離，便於單元測試
4. **一致性：** 統一的命名規範和錯誤處理
5. **文檔化：** 所有公開 API 都有文檔字串

## 測試

專案包含完整的單元測試，位於 `testcases/` 目錄：

- `test_board.py` - 測試遊戲板功能（13 個測試）
- `test_game_engine.py` - 測試遊戲引擎（15 個測試）
- `test_game_logic.py` - 測試遊戲邏輯（9 個測試）

**總計：37 個測試，全部通過 ✅**

執行測試：
```bash
python -m unittest discover testcases
# 或
python -m pytest testcases/
```

## 未來擴展方向

1. **AI 訓練：** 使用強化學習訓練更強的 AI
2. **多人在線：** 實作多人對戰功能
3. **自訂主題：** 支援多種視覺主題
4. **教學內容：** 添加詳細的策略教學內容
5. **統計分析：** 分析玩家的遊戲數據和進步曲線

