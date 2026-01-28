import sys
import random

# Constants
EMPTY = '.'
TOKEN_P1 = 'X'
TOKEN_P2 = 'O'
HUMAN = 1
RANDOM_COMP = 2
STRATEGIC_COMP = 3

def get_column_by_order(cols, i):
    """Priority for strategic computer: Center -> Left -> Right."""
    center = (cols - 1) // 2
    if i == 0: return center
    offset = (i + 1) // 2
    if i % 2 == 1: return center - offset
    else: return center + offset

def check_victory(board, rows, cols, r, c, token, n):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            nr, nc = r + (dr * step), c + (dc * step)
            while 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == token:
                count += 1
                nr += (dr * step)
                nc += (dc * step)
        if count >= n: return True
    return False

def computer_choose(board, rows, cols, token, opp_token, n, strategy):
    if strategy == RANDOM_COMP:
        # True random: pick any non-full column
        available = [c for c in range(cols) if board[0][c] == EMPTY]
        return random.choice(available)
    
    # Strategic (s): Priorities 1-5
    for p in range(1, 6):
        for i in range(cols):
            c = get_column_by_order(cols, i)
            if board[0][c] == EMPTY:
                r_idx = -1
                for r in range(rows - 1, -1, -1):
                    if board[r][c] == EMPTY:
                        r_idx = r; break
                if p == 1:
                    board[r_idx][c] = token
                    if check_victory(board, rows, cols, r_idx, c, token, n):
                        board[r_idx][c] = EMPTY; return c
                elif p == 2:
                    board[r_idx][c] = opp_token
                    if check_victory(board, rows, cols, r_idx, c, opp_token, n):
                        board[r_idx][c] = EMPTY; return c
                elif p == 3:
                    board[r_idx][c] = token
                    if check_victory(board, rows, cols, r_idx, c, token, 3):
                        board[r_idx][c] = EMPTY; return c
                elif p == 4:
                    board[r_idx][c] = opp_token
                    if check_victory(board, rows, cols, r_idx, c, opp_token, 3):
                        board[r_idx][c] = EMPTY; return c
                elif p == 5:
                    board[r_idx][c] = EMPTY; return c
                board[r_idx][c] = EMPTY
    return 0

def print_board(board, rows, cols, is_ttt):
    print()
    for r in range(rows):
        print("|", end="")
        for c in range(cols):
            print(board[r][c], end="|")
        print()
    if not is_ttt:
        for c in range(1, cols + 1):
            print(f" {c % 10}", end="")
        print()

def main():
    print("Enter number of rows")
    rows = int(input().strip())
    print("Enter number of columns")
    cols = int(input().strip())

    is_ttt = (rows == 3 or cols == 3)
    if is_ttt:
        rows, cols, n = 3, 3, 3
        print("\nTic Tac Toe (Human vs Human)")
        p1_t, p2_t = HUMAN, HUMAN
    else:
        if rows == 2 or cols == 2: n = 2
        elif 4 <= max(rows, cols) <= 5: n = 3
        elif 6 <= max(rows, cols) <= 10: n = 4
        else: n = 5
        print(f"Connect Four - Or More [Or Less] ({rows} rows x {cols} cols, connect {n})")
        
        print("\nChoose type for player 1: h - human, r - random/simple computer, s - strategic computer: ", end="")
        c1 = input().strip().lower()
        p1_t = HUMAN if c1 == 'h' else (RANDOM_COMP if c1 == 'r' else STRATEGIC_COMP)
        print("Choose type for player 2: h - human, r - random/simple computer, s - strategic computer: ", end="")
        c2 = input().strip().lower()
        p2_t = HUMAN if c2 == 'h' else (RANDOM_COMP if c2 == 'r' else STRATEGIC_COMP)

    board = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    print_board(board, rows, cols, is_ttt)
    
    curr_p, curr_token, curr_type = 1, TOKEN_P1, p1_t
    
    while True:
        print(f"\nPlayer {curr_p} ({curr_token}) turn.")
        if curr_type == HUMAN:
            while True:
                msg = "Enter position (1-9): " if is_ttt else f"Enter column (1-{cols}): "
                raw = input(msg).strip()
                if not raw: continue
                val = int(raw)
                if is_ttt:
                    r, c = (val-1)//3, (val-1)%3
                    if board[r][c] == EMPTY: break
                    print(f"Position {val} is full.")
                else:
                    if 1 <= val <= cols:
                        c = val - 1
                        if board[0][c] == EMPTY: break
                        print(f"Column {val} is full. Choose another column.")
                    else: print(f"Invalid column. Choose between 1 and {cols}.")
        else:
            opp = TOKEN_P2 if curr_token == TOKEN_P1 else TOKEN_P1
            c = computer_choose(board, rows, cols, curr_token, opp, n, curr_type)
            print(f"Computer chose column {c + 1}")

        for row_idx in range(rows - 1, -1, -1):
            if board[row_idx][c] == EMPTY:
                r = row_idx; break
        
        board[r][c] = curr_token
        print_board(board, rows, cols, is_ttt)

        if check_victory(board, rows, cols, r, c, curr_token, n):
            print(f"Player {curr_p} ({curr_token}) wins!")
            break
        if not any(board[0][col_idx] == EMPTY for col_idx in range(cols)):
            print("Board full and no winner. It's a tie!")
            break
        curr_p, curr_token, curr_type = (2, TOKEN_P2, p2_t) if curr_p == 1 else (1, TOKEN_P1, p1_t)

if __name__ == "__main__":
    main()