import pyautogui
import cv2
import numpy as np
import time
import os

# --- 設定參數 (您需要根據您的遊戲介面進行調整) ---

# 遊戲板的左上角座標 (X, Y) 和單個方塊的邊長 (像素)
# 您可以手動截圖後，使用繪圖工具測量這些值。
# 例如：(100, 200, 30) 表示遊戲板左上角在螢幕 (100, 200) 處，每個方塊是 30x30 像素。
BOARD_TOP_LEFT_X = 100
BOARD_TOP_LEFT_Y = 200
CELL_SIZE = 30 # 每個方塊的寬度和高度 (假設是正方形)

# 遊戲板的行數和列數 (例如 9x9, 16x16 等)
BOARD_ROWS = 9
BOARD_COLS = 9

# 範本圖片路徑 (您需要自行截圖並建立這些圖片)
# 將這些圖片放在與您的 Python 腳本相同的目錄中。
# 這些圖片應該是單個方塊的精確截圖。
TEMPLATES = {
    'unopened': cv2.imread('templates/unopened.png', cv2.IMREAD_GRAYSCALE),
    'flagged': cv2.imread('templates/flagged.png', cv2.IMREAD_GRAYSCALE),
    'mine': cv2.imread('templates/mine.png', cv2.IMREAD_GRAYSCALE),
    'open_empty': cv2.imread('templates/open_empty.png', cv2.IMREAD_GRAYSCALE), # 打開的空白方塊
    'num_1': cv2.imread('templates/num_1.png', cv2.IMREAD_GRAYSCALE),
    'num_2': cv2.imread('templates/num_2.png', cv2.IMREAD_GRAYSCALE),
    'num_3': cv2.imread('templates/num_3.png', cv2.IMREAD_GRAYSCALE),
    'num_4': cv2.imread('templates/num_4.png', cv2.IMREAD_GRAYSCALE),
    'num_5': cv2.imread('templates/num_5.png', cv2.IMREAD_GRAYSCALE),
    'num_6': cv2.imread('templates/num_6.png', cv2.IMREAD_GRAYSCALE),
    'num_7': cv2.imread('templates/num_7.png', cv2.IMREAD_GRAYSCALE),
    'num_8': cv2.imread('templates/num_8.png', cv2.IMREAD_GRAYSCALE),
}

# 範本比對的閾值 (0.0 到 1.0, 越接近 1.0 越精確)
# 您可能需要根據實際測試調整這個值。
TEMPLATE_MATCH_THRESHOLD = 0.85

# 自動遊玩時每次動作之間的延遲 (秒)
AUTO_PLAY_DELAY = 0.1

# --- 內部遊戲板狀態定義 ---
# 0: 未知/未打開
# 1-8: 已打開的數字
# 9: 旗子
# -1: 地雷 (僅在遊戲結束時顯示或內部推斷)
# -2: 已打開的空白方塊 (mineCount = 0)

# --- 輔助函數 ---

def capture_board_image():
    """
    截取踩地雷遊戲板區域的螢幕畫面。
    """
    # pyautogui.screenshot 返回 PIL Image 對象
    # .convert('RGB') 確保是 RGB 格式，OpenCV 通常處理 BGR 或灰度
    # np.array() 轉換為 NumPy 陣列
    # cv2.cvtColor() 轉換為灰度圖，有利於範本比對
    screenshot = pyautogui.screenshot(region=(
        BOARD_TOP_LEFT_X,
        BOARD_TOP_LEFT_Y,
        BOARD_COLS * CELL_SIZE,
        BOARD_ROWS * CELL_SIZE
    ))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

def get_cell_image(board_image, r, c):
    """
    從遊戲板截圖中提取單個方塊的圖像。
    """
    x = c * CELL_SIZE
    y = r * CELL_SIZE
    return board_image[y : y + CELL_SIZE, x : x + CELL_SIZE]

def recognize_cell_state(cell_image):
    """
    辨識單個方塊的狀態。
    返回: 'unopened', 'flagged', 'mine', 'open_empty', 'num_1'...'num_8', 或 'unknown'
    """
    for state, template in TEMPLATES.items():
        if template is None:
            print(f"警告: 範本 '{state}.png' 未載入，請檢查路徑。")
            continue

        # 確保範本和圖像大小匹配，或者進行縮放
        # 這裡假設範本已經是 CELL_SIZE x CELL_SIZE
        if template.shape[0] != CELL_SIZE or template.shape[1] != CELL_SIZE:
             # 如果範本大小不對，則縮放範本以匹配單元格大小
            template = cv2.resize(template, (CELL_SIZE, CELL_SIZE))

        # 使用 OpenCV 進行範本比對
        res = cv2.matchTemplate(cell_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= TEMPLATE_MATCH_THRESHOLD:
            return state
    return 'unknown'

def get_cell_center_coords(r, c):
    """
    計算螢幕上指定方塊的中心座標，用於滑鼠點擊。
    """
    center_x = BOARD_TOP_LEFT_X + c * CELL_SIZE + CELL_SIZE // 2
    center_y = BOARD_TOP_LEFT_Y + r * CELL_SIZE + CELL_SIZE // 2
    return center_x, center_y

def click_cell(r, c):
    """
    模擬滑鼠左鍵點擊指定方塊。
    """
    x, y = get_cell_center_coords(r, c)
    pyautogui.click(x, y)
    time.sleep(AUTO_PLAY_DELAY) # 點擊後稍作延遲，等待遊戲響應

def right_click_cell(r, c):
    """
    模擬滑鼠右鍵點擊指定方塊 (標記旗子)。
    """
    x, y = get_cell_center_coords(r, c)
    pyautogui.rightClick(x, y)
    time.sleep(AUTO_PLAY_DELAY) # 點擊後稍作延遲

# --- 遊戲板狀態更新與辨識 ---

def update_internal_board(current_board_state):
    """
    掃描螢幕並更新內部遊戲板的狀態。
    """
    board_image = capture_board_image()
    # 為了調試，可以保存截圖
    # cv2.imwrite("debug_board_capture.png", board_image)

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cell_img = get_cell_image(board_image, r, c)
            state = recognize_cell_state(cell_img)

            # 根據辨識結果更新內部板
            if state == 'unopened':
                current_board_state[r][c] = 0
            elif state == 'flagged':
                current_board_state[r][c] = 9
            elif state == 'open_empty':
                current_board_state[r][c] = -2 # 用 -2 表示已打開的空白
            elif state.startswith('num_'):
                current_board_state[r][c] = int(state.split('_')[1])
            elif state == 'mine':
                # 如果辨識到地雷，表示遊戲可能已經結束或點錯了
                current_board_state[r][c] = -1
                print(f"偵測到地雷在 ({r}, {c})。遊戲可能結束。")
            else:
                # 如果無法辨識，保持原狀或標記為未知
                # print(f"無法辨識方塊 ({r}, {c}) 的狀態: {state}")
                pass # 保持原狀，等待下次掃描

    return current_board_state

# --- 踩地雷 AI 邏輯 ---

def get_neighbors(r, c):
    """
    獲取指定方塊的所有鄰居座標。
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < BOARD_ROWS and 0 <= nc < BOARD_COLS:
                neighbors.append((nr, nc))
    return neighbors

def find_next_move(board_state):
    """
    根據當前遊戲板狀態，找出下一步行動。
    返回 (action, r, c) 或 None
    action: 'click' 或 'flag'
    """
    # 策略 1: 找出安全的點擊 (數字方塊周圍的旗子數等於數字，則其餘未開方塊安全)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cell_value = board_state[r][c]
            if 1 <= cell_value <= 8: # 是一個數字方塊
                neighbors = get_neighbors(r, c)
                flagged_neighbors = 0
                unopened_neighbors = []

                for nr, nc in neighbors:
                    neighbor_state = board_state[nr][nc]
                    if neighbor_state == 9: # 旗子
                        flagged_neighbors += 1
                    elif neighbor_state == 0: # 未打開
                        unopened_neighbors.append((nr, nc))

                # 如果數字方塊周圍的旗子數量等於數字本身，則所有未打開的鄰居都是安全的
                if cell_value == flagged_neighbors and unopened_neighbors:
                    print(f"策略1: 發現安全點擊在 ({unopened_neighbors[0][0]}, {unopened_neighbors[0][1]})")
                    return 'click', unopened_neighbors[0][0], unopened_neighbors[0][1]

    # 策略 2: 找出地雷並標記 (數字方塊周圍的未開方塊數等於數字，則這些未開方塊是地雷)
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cell_value = board_state[r][c]
            if 1 <= cell_value <= 8: # 是一個數字方塊
                neighbors = get_neighbors(r, c)
                unopened_and_unflagged_neighbors = []
                flagged_count = 0

                for nr, nc in neighbors:
                    neighbor_state = board_state[nr][nc]
                    if neighbor_state == 0: # 未打開且未標記
                        unopened_and_unflagged_neighbors.append((nr, nc))
                    elif neighbor_state == 9: # 已標記旗子
                        flagged_count += 1

                # 如果數字方塊周圍的未打開且未標記的方塊數量 + 已標記旗子的數量 等於數字本身
                # 則所有未打開且未標記的方塊都是地雷
                if cell_value == (len(unopened_and_unflagged_neighbors) + flagged_count) and unopened_and_unflagged_neighbors:
                    print(f"策略2: 發現地雷並標記在 ({unopened_and_unflagged_neighbors[0][0]}, {unopened_and_unflagged_neighbors[0][1]})")
                    return 'flag', unopened_and_unflagged_neighbors[0][0], unopened_and_unflagged_neighbors[0][1]

    # 策略 3: 如果沒有明確的動作，隨機點擊一個未開的方塊
    unopened_cells = []
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board_state[r][c] == 0: # 未打開的方塊
                unopened_cells.append((r, c))

    if unopened_cells:
        # 為了避免一開始就隨機點擊地雷，可以優先點擊角落或邊緣的方塊
        # 或者簡單地隨機選擇一個
        r_rand, c_rand = unopened_cells[np.random.randint(len(unopened_cells))]
        print(f"策略3: 隨機點擊在 ({r_rand}, {c_rand})")
        return 'click', r_rand, c_rand

    return None # 沒有可行的動作

def check_game_status(board_state):
    """
    檢查遊戲是否結束 (勝利或失敗)。
    這需要觀察遊戲介面上的特定文字或圖案。
    此函數為概念性，您需要根據遊戲實際情況實現。
    例如：
    - 尋找螢幕上的 "You Win!" 或 "Game Over!" 文字。
    - 檢查所有非地雷方塊是否都已打開。
    - 檢查是否點擊到地雷 (內部板狀態為 -1)。
    """
    # 簡單檢查：如果內部板中有地雷被打開，則遊戲失敗
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board_state[r][c] == -1:
                return 'lose'

    # 檢查是否勝利：所有非地雷方塊都已打開，且沒有未打開的方塊
    unopened_count = 0
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board_state[r][c] == 0 or board_state[r][c] == 9: # 未打開或旗子
                unopened_count += 1
    
    # 這裡需要知道總地雷數來判斷是否所有安全方塊都已打開
    # 由於我們無法直接從螢幕讀取總地雷數，這部分判斷會比較困難。
    # 一個簡單的判斷是，如果所有方塊都被識別為已打開或旗子，且沒有地雷被點開，則可能勝利。
    # 或者，您可以尋找遊戲介面上的勝利訊息。
    # 暫時簡化為：如果沒有未打開或旗子的方塊，則認為勝利
    if unopened_count == 0:
        return 'win'

    return 'playing'

# --- 主程式 ---

def main():
    print("踩地雷自動遊玩程式已啟動。")
    print("請確保踩地雷遊戲已開啟並位於螢幕上可見位置。")
    print("程式將在 5 秒後開始掃描。")
    time.sleep(5) # 給用戶時間切換到遊戲視窗

    # 創建範本圖片目錄 (如果不存在)
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("請在 'templates/' 目錄中放置範本圖片 (unopened.png, flagged.png, mine.png, open_empty.png, num_1.png ... num_8.png)。")
        print("您需要手動截取遊戲中的這些方塊圖像並保存為灰度圖。")
        print("程式將退出，請準備好範本後重新運行。")
        return

    # 檢查所有範本是否都已載入
    for state, template in TEMPLATES.items():
        if template is None:
            print(f"錯誤: 範本 '{state}.png' 未載入。請檢查 'templates/' 目錄和圖片名稱。")
            print("程式將退出。")
            return

    # 初始化內部遊戲板狀態
    internal_board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    
    # 首次掃描以填充初始板狀態
    print("首次掃描遊戲板...")
    internal_board = update_internal_board(internal_board)
    print("初始遊戲板狀態:")
    for row in internal_board:
        print(row)

    while True:
        game_status = check_game_status(internal_board)
        if game_status == 'win':
            print("🎉 遊戲勝利！")
            break
        elif game_status == 'lose':
            print("💥 遊戲失敗！")
            break

        next_move = find_next_move(internal_board)

        if next_move:
            action, r, c = next_move
            if action == 'click':
                print(f"執行: 左鍵點擊 ({r}, {c})")
                click_cell(r, c)
            elif action == 'flag':
                print(f"執行: 右鍵標記 ({r}, {c})")
                right_click_cell(r, c)
            
            # 執行動作後，重新掃描並更新內部板狀態
            internal_board = update_internal_board(internal_board)
            # print("更新後的遊戲板狀態:")
            # for row in internal_board:
            #     print(row)
        else:
            print("沒有明確的下一步動作。可能遊戲已陷入僵局或已完成。")
            # 如果沒有下一步動作，可以考慮等待一段時間或結束程式
            time.sleep(1) 
            # 為了避免無限循環，如果長時間沒有動作，可以手動停止或加入計數器
            break

        time.sleep(AUTO_PLAY_DELAY) # 每次動作之間稍作延遲

if __name__ == "__main__":
    main()
