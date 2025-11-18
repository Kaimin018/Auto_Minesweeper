# 測試說明

本目錄包含踩地雷遊戲的單元測試。

## 測試結構

- `test_board.py` - 測試遊戲板 (Board) 的基本功能
- `test_game_engine.py` - 測試遊戲引擎 (GameEngine) 的基本功能
- `test_game_logic.py` - 測試遊戲邏輯和完整流程
- `test_ui_integration.py` - 測試 UI 與遊戲引擎的整合，確保返回字典完整性

## 執行測試

### 執行所有測試

```bash
# 在專案根目錄執行
python -m pytest testcases/

# 或使用 unittest
python -m unittest discover testcases
```

### 執行特定測試文件

```bash
# 測試遊戲板
python -m pytest testcases/test_board.py

# 測試遊戲引擎
python -m pytest testcases/test_game_engine.py

# 測試遊戲邏輯
python -m pytest testcases/test_game_logic.py
```

### 執行特定測試類別

```bash
python -m pytest testcases/test_board.py::TestBoard
```

### 執行特定測試方法

```bash
python -m pytest testcases/test_board.py::TestBoard::test_board_initialization
```

## 測試覆蓋範圍

### test_board.py (13 個測試)
- ✅ 遊戲板初始化
- ✅ 第一次點擊安全保證
- ✅ 地雷數量驗證
- ✅ 數字格子計算
- ✅ 揭開格子功能
- ✅ 揭開地雷處理
- ✅ 空白區域自動展開
- ✅ 標記/取消標記功能
- ✅ 不能標記已揭開的格子
- ✅ 鄰居格子取得
- ✅ 勝利判斷
- ✅ 標記和揭開計數

### test_game_engine.py (15 個測試)
- ✅ 遊戲引擎初始化
- ✅ 開始新遊戲
- ✅ 第一次點擊安全
- ✅ 點擊格子功能
- ✅ 點擊已標記的格子
- ✅ 點擊已揭開的格子
- ✅ 標記格子功能
- ✅ 取消標記功能
- ✅ 不能標記已揭開的格子
- ✅ 剩餘地雷數計算
- ✅ 移動次數統計
- ✅ 計時功能
- ✅ 遊戲狀態管理
- ✅ 遊戲板狀態取得
- ✅ 格子值取得
- ✅ 揭開所有地雷功能

### test_game_logic.py (9 個測試)
- ✅ 完整遊戲流程
- ✅ 勝利條件
- ✅ 失敗條件
- ✅ 標記數量一致性
- ✅ 多次遊戲
- ✅ 邊界情況
- ✅ 自動展開功能
- ✅ 狀態一致性

### test_ui_integration.py (6 個測試)
- ✅ click_cell 所有返回路徑都包含 'exploded' 鍵
- ✅ 返回字典結構完整性驗證
- ✅ 所有點擊場景的返回完整性
- ✅ 'exploded' 鍵的值正確性
- ✅ 遊戲狀態與 exploded 鍵的一致性
- ✅ 錯誤處理時返回字典的完整性

**總計：43 個測試，全部通過 ✅**

## 測試最佳實踐

1. **獨立性**：每個測試應該獨立，不依賴其他測試的結果
2. **可重現性**：使用固定種子 (`random.seed(42)`) 確保測試可重現
3. **覆蓋率**：盡量覆蓋所有主要功能和邊界情況
4. **清晰性**：測試名稱應該清楚描述測試的內容

## 添加新測試

當添加新功能時，應該同時添加相應的測試：

1. 在適當的測試文件中添加測試方法
2. 測試應該包含：
   - 正常情況
   - 邊界情況
   - 錯誤情況
3. 確保測試通過後再提交

## 持續整合

建議在 CI/CD 流程中自動執行這些測試，確保程式碼品質。

