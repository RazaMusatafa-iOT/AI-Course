def print_board(board):
    print()
    for i in range(3):
        row = " | ".join(board[i * 3:(i + 1) * 3])
        print(f" {row} ")
        if i < 2:
            print("---+---+---")
    print()


def check_winner(board, player):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    return any(all(board[p] == player for p in line) for line in wins)


def get_move(board, player):
    while True:
        try:
            pos = int(input(f"Player {player}, enter position (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if pos < 1 or pos > 9:
            print("Position out of range. Choose 1-9.")
            continue
        if board[pos - 1] != " ":
            print("That spot is taken. Try again.")
            continue
        return pos - 1


def play():
    board = [" "] * 9
    current = "X"
    print("Welcome to Tic-Tac-Toe!")
    print("Positions are numbered 1-9, left-to-right, top-to-bottom.")
    print_board(board)

    for turn in range(9):
        move = get_move(board, current)
        board[move] = current
        print_board(board)
        if check_winner(board, current):
            print(f"Player {current} wins!")
            return
        current = "O" if current == "X" else "X"

    print("It's a draw!")


if __name__ == "__main__":
    play()