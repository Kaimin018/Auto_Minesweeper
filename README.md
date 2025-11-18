# 踩地雷 AI 教學遊戲

一個 AI 輔助的踩地雷教學遊戲，旨在幫助玩家學習踩地雷的策略和機率判斷技巧。

## 功能特色

### 階段一：基礎架構（已完成）
- ✅ **遊戲引擎**：完整的踩地雷遊戲邏輯
- ✅ **機率計算引擎**：計算每個格子的地雷機率
- ✅ **計時模式**：單人計時遊戲，記錄完成時間
- ✅ **排行榜系統**：SQLite 資料庫儲存最佳成績
- ✅ **現代化 UI**：使用 PyQt5 建立的使用者介面

### 未來功能（開發中）
- ⏳ **教學模式**：AI 即時教學，顯示機率和推理過程
- ⏳ **與 AI 對戰**：與 AI 輪流操作，比較決策品質

## 安裝與執行

### 1. 安裝依賴

```bash
# 使用虛擬環境（建議）
python -m venv myenv
myenv\Scripts\activate  # Windows
# 或
source myenv/bin/activate  # Linux/Mac

# 安裝套件
pip install -r requirements.txt
```

### 2. 執行遊戲

```bash
python main.py
```

## 遊戲說明

### 操作方式
- **左鍵點擊**：揭開格子
- **右鍵點擊**：標記/取消標記地雷
- **新遊戲**：重新開始遊戲
- **返回主選單**：回到主選單

### 難度等級
- **初級**：9x9 棋盤，10 個地雷
- **中級**：16x16 棋盤，40 個地雷
- **專家級**：30x16 棋盤，99 個地雷

### 排行榜
- 遊戲勝利後可以輸入名稱儲存成績
- 在主選單可以查看排行榜
- 支援按難度篩選

## 專案結構

```
10_auto_minesweeper/
├── main.py                 # 主入口
├── config.py               # 配置設定
├── requirements.txt        # 依賴套件
├── architecture.md         # 架構文件
├── How-to.md              # 快速指令參考
├── README.md              # 專案說明
│
├── core/                   # 核心遊戲邏輯
│   ├── game_engine.py     # 遊戲引擎
│   └── board.py           # 遊戲板類別
│
├── ai/                     # AI 模組
│   ├── probability_calculator.py  # 機率計算
│   └── strategies.py      # 求解策略
│
├── ui/                     # 使用者介面
│   ├── main_menu.py       # 主選單
│   ├── game_window.py     # 遊戲視窗
│   └── leaderboard.py     # 排行榜
│
├── utils/                  # 工具函數
│   └── database.py        # 資料庫操作
│
├── modes/                  # 遊戲模式（未來擴展）
│
├── data/                   # 資料儲存
│   └── leaderboard.db     # SQLite 資料庫
│
└── guidance/               # 使用指南
    ├── README.md
    ├── installation.md
    ├── quick-start.md
    ├── game-guide.md
    └── ... (更多指南文件)
```

## 技術棧

- **Python 3.8+**
- **PyQt5**：使用者介面框架
- **SQLite3**：排行榜資料庫
- **NumPy**：數值計算（未來擴展用）

## 開發狀態

### 階段一：基礎架構 ✅
- [x] 重構現有代碼，分離遊戲引擎
- [x] 實作機率計算引擎
- [x] 建立基本 UI 框架
- [x] 實作單人計時模式
- [x] 建立資料庫系統

### 階段二：教學模式（規劃中）
- [ ] 實作教學模式 UI
- [ ] 整合機率計算與視覺化
- [ ] 實作推理過程展示

### 階段三：對戰模式（規劃中）
- [ ] 實作對戰模式
- [ ] 優化 AI 策略
- [ ] 實作 AI 訓練（可選）

## 使用指南

本專案提供完整的使用和開發指南，位於 `guidance/` 資料夾：

### 快速開始
- [安裝指南](guidance/installation.md) - 如何安裝和設置專案
- [快速開始](guidance/quick-start.md) - 快速上手遊戲

### 使用指南
- [遊戲說明](guidance/game-guide.md) - 遊戲規則和操作說明
- [功能介紹](guidance/features.md) - 各項功能詳細介紹

### 開發指南
- [開發環境設置](guidance/development-setup.md) - 開發者環境配置
- [貢獻指南](guidance/contributing.md) - 如何貢獻程式碼

### 其他
- [常見問題](guidance/faq.md) - 常見問題解答
- [故障排除](guidance/troubleshooting.md) - 問題診斷和解決
- [安全注意事項](guidance/security-notes.md) - 保護敏感資訊指南
- [專案遷移記錄](guidance/migration-log.md) - 專案結構遷移詳細記錄

## 注意事項

- 資料庫會自動在 `data/` 目錄下建立
- 快速指令參考請查看 `How-to.md`
- 詳細的程式碼結構和架構說明請查看 `architecture.md`

## 授權

本專案僅供學習使用。

