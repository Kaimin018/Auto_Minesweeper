# 開發環境設置

本指南幫助開發者設置開發環境。

## 前置需求

- Python 3.8+
- Git
- 文字編輯器或 IDE（推薦 VS Code 或 PyCharm）

## 設置步驟

### 1. 克隆專案

```bash
git clone <repository-url>
cd 10_auto_minesweeper
```

### 2. 建立虛擬環境

```bash
python -m venv myenv

# Windows
myenv\Scripts\activate

# Linux/Mac
source myenv/bin/activate
```

### 3. 安裝開發依賴

```bash
pip install -r requirements.txt

# 如果需要開發工具
pip install pytest black flake8 mypy
```

### 4. 設置 IDE

#### VS Code

1. 安裝 Python 擴展
2. 選擇虛擬環境作為 Python 解釋器
3. 設置 `.vscode/settings.json`：

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/myenv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

#### PyCharm

1. 開啟專案
2. File → Settings → Project → Python Interpreter
3. 選擇虛擬環境的 Python 解釋器

## 專案結構

```
10_auto_minesweeper/
├── main.py              # 主入口
├── config.py            # 配置設定
├── requirements.txt      # 依賴套件
├── architecture.md      # 架構文件
│
├── core/                # 核心遊戲邏輯
│   ├── game_engine.py
│   └── board.py
│
├── ai/                  # AI 模組
│   ├── probability_calculator.py
│   └── strategies.py
│
├── ui/                  # 使用者介面
│   ├── main_menu.py
│   ├── game_window.py
│   └── leaderboard.py
│
├── utils/               # 工具函數
│   └── database.py
│
├── modes/               # 遊戲模式
│   └── (未來擴展)
│
├── data/                # 資料儲存
│   └── leaderboard.db
│
└── guidance/            # 文檔
    └── (各種指南)
```

## 開發工作流程

### 1. 建立新功能分支

```bash
git checkout -b feature/new-feature
```

### 2. 開發和測試

```bash
# 執行遊戲測試
python main.py

# 執行單元測試（如果有）
pytest tests/
```

### 3. 提交變更

```bash
git add .
git commit -m "描述變更"
git push origin feature/new-feature
```

### 4. 建立 Pull Request

在 GitHub 上建立 PR，等待審查。

## 程式碼規範

### Python 風格

- 遵循 PEP 8
- 使用 4 個空格縮排
- 行長度限制 100 字元
- 使用類型提示（Type Hints）

### 命名規範

- **類別**：PascalCase（如 `GameEngine`）
- **函數/變數**：snake_case（如 `get_cell_value`）
- **常數**：UPPER_SNAKE_CASE（如 `STATUS_PLAYING`）

### 文檔字串

所有公開的類別和函數都應該有文檔字串：

```python
def function_name(param1: int, param2: str) -> bool:
    """
    函數描述
    
    Args:
        param1: 參數1的描述
        param2: 參數2的描述
    
    Returns:
        返回值的描述
    """
    pass
```

## 測試

### 執行測試

```bash
pytest tests/
```

### 撰寫測試

在 `tests/` 目錄下建立測試檔案：

```python
import pytest
from core.game_engine import GameEngine

def test_game_engine_initialization():
    engine = GameEngine(9, 9, 10)
    assert engine.rows == 9
    assert engine.cols == 9
    assert engine.num_mines == 10
```

## 除錯技巧

### 使用 print 除錯

```python
print(f"Debug: value = {value}")
```

### 使用斷點

在 IDE 中設置斷點進行除錯。

### 使用日誌

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## 常見開發任務

### 添加新功能

1. 在適當的模組中實作功能
2. 更新相關文檔
3. 添加測試
4. 更新 `architecture.md`（如果需要）

### 修改 UI

1. 編輯 `ui/` 目錄下的檔案
2. 測試不同解析度和作業系統
3. 確保響應式設計

### 修改遊戲邏輯

1. 編輯 `core/` 目錄下的檔案
2. 確保不破壞現有功能
3. 添加測試覆蓋

## 工具推薦

### 程式碼格式化

```bash
black .
```

### 程式碼檢查

```bash
flake8 .
```

### 類型檢查

```bash
mypy .
```

## 取得幫助

- 查看[架構文件](../architecture.md)了解程式碼結構和系統架構
- 查看[貢獻指南](contributing.md)

