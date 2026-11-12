import tkinter as tk
from tkinter import messagebox

WINNING_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.current = "X"
        self.board = [" "] * 9
        self.buttons = []
        self.status = tk.Label(root, text="Player X's turn",
                               font=("Arial", 16), pady=10)
        self.status.grid(row=0, column=0, columnspan=3)
        self.build_grid()
        reset = tk.Button(root, text="Reset", font=("Arial", 12),
                          command=self.reset)
        reset.grid(row=1, column=0, columnspan=3, sticky="we", pady=(5, 0))

    def build_grid(self):
        frame = tk.Frame(self.root)
        frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        for i in range(9):
            btn = tk.Button(frame, text=" ", font=("Arial", 32),
                            width=3, height=1,
                            command=lambda idx=i: self.click(idx))
            btn.grid(row=i // 3, column=i % 3, sticky="nsew")
            self.buttons.append(btn)
        for i in range(3):
            frame.grid_rowconfigure(i, minsize=90)
            frame.grid_columnconfigure(i, minsize=90)

    def click(self, idx):
        if self.board[idx] != " ":
            return
        self.board[idx] = self.current
        self.buttons[idx].config(text=self.current,
                                 disabledforeground="black")
        if self.check_winner(self.current):
            messagebox.showinfo("Game Over", f"Player {self.current} wins!")
            self.disable_all()
            self.status.config(text=f"Player {self.current} wins!")
            return
        if " " not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.status.config(text="It's a draw!")
            return
        self.current = "O" if self.current == "X" else "X"
        self.status.config(text=f"Player {self.current}'s turn")

    def check_winner(self, player):
        return any(all(self.board[p] == player for p in line)
                   for line in WINNING_LINES)

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset(self):
        self.current = "X"
        self.board = [" "] * 9
        self.status.config(text="Player X's turn")
        for btn in self.buttons:
            btn.config(text=" ", state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()