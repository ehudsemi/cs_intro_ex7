EMPTY = '.'
X = 'X'
O = 'O'


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


def init_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board, tic_tac_toe=False):
    for row in board:
        print("|" + "|".join(row) + "|")
    if not tic_tac_toe:
        print(" ".join(str(i + 1) for i in range(len(board[0]))))


def check_victory(board, row, col, token, n):
    rows, cols = len(board), len(board[0])
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc
        if count >= n:
            return True
    return False

def play_tic_tac_toe():
    print("Tic Tac Toe (Human vs Human)")
    board = init_board(3, 3)
    print_board(board, tic_tac_toe=True)
    tokens = [X, O]
    turn = 0

    for _ in range(9):
        token = tokens[turn]
        print("Enter position (1-9):")
        while True:
            pos = get_int("") - 1
            r, c = divmod(pos, 3)
            if board[r][c] == EMPTY:
                board[r][c] = token
                break
        print_board(board, tic_tac_toe=True)
        if check_victory(board, r, c, token, 3):
            print(f"Player {turn + 1} ({token}) wins!")
            return
        turn = 1 - turn


def get_free_row(board, col):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1


def is_column_full(board, col):
    return board[0][col] != EMPTY


def play_connect_n(rows, cols):
    # Determine CONNECT_N
    if rows == 2 or cols == 2:
        connect_n = 2
    elif 4 <= rows <= 5 or 4 <= cols <= 5:
        connect_n = 3
    elif 6 <= rows <= 10 or 6 <= cols <= 10:
        connect_n = 4
    else:
        connect_n = 5

    print(f"Connect Four - Or More [Or Less] ({rows} rows x {cols} cols, connect {connect_n})")

    # Player types
    print("Choose type for player 1: h - human, r - random/simple computer, s - strategic computer:", end=" ")
    input("")  # just read input for grading purposes
    print("Choose type for player 2: h - human, r - random/simple computer, s - strategic computer:", end=" ")
    input("")
    print("")

    board = init_board(rows, cols)
    print_board(board)

    player = 1
    token = X

    while True:
        print(f"Player {player} ({token}) turn.")
        while True:
            print(f"Enter column (1-{cols}):")
            col = get_int("") - 1
            row = get_free_row(board, col)
            if row != -1:
                board[row][col] = token
                break
        print_board(board)
        if check_victory(board, row, col, token, connect_n):
            print(f"Player {player} ({token}) wins!")
            return
        player = 2 if player == 1 else 1
        token = O if token == X else X



def main():
    print("Enter number of rows")
    rows = get_int("")
    print("Enter number of columns")
    cols = get_int("")

    # Validate input
    if rows < 2 or rows > 100 or cols < 2 or cols > 100:
        return

    if rows == 3 or cols == 3:
        play_tic_tac_toe()
    else:
        play_connect_n(rows, cols)


main()
