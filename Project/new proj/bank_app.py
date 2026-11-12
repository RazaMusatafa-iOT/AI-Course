import tkinter as tk
from tkinter import messagebox, ttk


BANK_NAME = "CS Banking System"
TRANSACTION_FEE = 20


class BankAccount:
    def __init__(self, title, acc_num, balance=0.0):
        self.title = title
        self.acc_num = acc_num
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True, "Deposit successful."
        return False, "Please enter a valid amount."

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Please enter a valid amount."
        if self._balance + TRANSACTION_FEE < amount:
            return False, "Insufficient funds (incl. transaction fee)."
        self._balance -= (amount + TRANSACTION_FEE)
        return True, f"Withdrawal successful. Fee: {TRANSACTION_FEE}"

    def transfer(self, amount, receiver):
        if amount <= 0:
            return False, "Please enter a valid amount."
        if self._balance + TRANSACTION_FEE < amount:
            return False, "Insufficient funds (incl. transaction fee)."
        self._balance -= (amount + TRANSACTION_FEE)
        receiver._balance += amount
        return True, f"Transferred {amount} to {receiver.title}. Fee: {TRANSACTION_FEE}"

    @property
    def balance(self):
        return self._balance

    def slip_text(self):
        line = "-" * 40
        return (
            f"{line}\n"
            f"Hello {self.title}, this is {BANK_NAME}\n"
            f"{line}\n"
            f"Account Number : {self.acc_num}\n"
            f"Balance        : {self.balance}\n"
            f"{line}"
        )


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(BANK_NAME)
        self.geometry("520x560")
        self.resizable(False, False)

        self.accounts = {}
        self.next_acc_num = 10001

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        create_frame = ttk.LabelFrame(self, text="Create Account")
        create_frame.pack(fill="x", **pad)

        ttk.Label(create_frame, text="Title:").grid(row=0, column=0, sticky="w", **pad)
        self.title_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.title_var, width=24).grid(row=0, column=1, **pad)

        ttk.Label(create_frame, text="Initial Deposit:").grid(row=1, column=0, sticky="w", **pad)
        self.init_dep_var = tk.StringVar(value="0")
        ttk.Entry(create_frame, textvariable=self.init_dep_var, width=24).grid(row=1, column=1, **pad)

        ttk.Button(create_frame, text="Create", command=self.create_account).grid(row=1, column=2, **pad)

        op_frame = ttk.LabelFrame(self, text="Operations")
        op_frame.pack(fill="x", **pad)

        ttk.Label(op_frame, text="Account:").grid(row=0, column=0, sticky="w", **pad)
        self.acc_combo = ttk.Combobox(op_frame, state="readonly", width=22)
        self.acc_combo.grid(row=0, column=1, **pad)

        ttk.Label(op_frame, text="Amount:").grid(row=1, column=0, sticky="w", **pad)
        self.amount_var = tk.StringVar()
        ttk.Entry(op_frame, textvariable=self.amount_var, width=24).grid(row=1, column=1, **pad)

        ttk.Button(op_frame, text="Deposit", command=self.do_deposit).grid(row=2, column=0, **pad)
        ttk.Button(op_frame, text="Withdraw", command=self.do_withdraw).grid(row=2, column=1, **pad)
        ttk.Button(op_frame, text="Check Balance", command=self.show_balance).grid(row=2, column=2, **pad)

        ttk.Label(op_frame, text="Transfer To:").grid(row=3, column=0, sticky="w", **pad)
        self.target_combo = ttk.Combobox(op_frame, state="readonly", width=22)
        self.target_combo.grid(row=3, column=1, **pad)
        ttk.Button(op_frame, text="Transfer", command=self.do_transfer).grid(row=3, column=2, **pad)

        ttk.Button(op_frame, text="Print Slip", command=self.print_slip).grid(row=4, column=0, columnspan=3, sticky="ew", **pad)

        log_frame = ttk.LabelFrame(self, text="Log")
        log_frame.pack(fill="both", expand=True, **pad)
        self.log_text = tk.Text(log_frame, height=10, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _refresh_combos(self):
        labels = [f"{a.acc_num} - {a.title}" for a in self.accounts.values()]
        self.acc_combo["values"] = labels
        self.target_combo["values"] = labels
        if labels:
            self.acc_combo.current(len(labels) - 1)
            self.target_combo.current(0)

    def _get_selected_account(self):
        sel = self.acc_combo.get()
        if not sel:
            messagebox.showwarning("Warning", "No account selected.")
            return None
        acc_num = int(sel.split(" - ")[0])
        return self.accounts.get(acc_num)

    def _get_amount(self):
        try:
            return float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return None

    def create_account(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Title is required.")
            return
        try:
            init_dep = float(self.init_dep_var.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Invalid initial deposit.")
            return
        acc = BankAccount(title, self.next_acc_num, init_dep)
        self.accounts[self.next_acc_num] = acc
        self.log(f"Created account {acc.acc_num} for '{title}' with balance {acc.balance}")
        self.next_acc_num += 1
        self._refresh_combos()
        self.title_var.set("")
        self.init_dep_var.set("0")

    def do_deposit(self):
        acc = self._get_selected_account()
        if not acc:
            return
        amount = self._get_amount()
        if amount is None:
            return
        ok, msg = acc.deposit(amount)
        self.log(f"[{acc.acc_num}] {msg} New balance: {acc.balance}")

    def do_withdraw(self):
        acc = self._get_selected_account()
        if not acc:
            return
        amount = self._get_amount()
        if amount is None:
            return
        ok, msg = acc.withdraw(amount)
        if ok:
            self.log(f"[{acc.acc_num}] {msg} New balance: {acc.balance}")
        else:
            messagebox.showerror("Failed", msg)
            self.log(f"[{acc.acc_num}] {msg}")

    def do_transfer(self):
        acc = self._get_selected_account()
        if not acc:
            return
        sel = self.target_combo.get()
        if not sel:
            messagebox.showwarning("Warning", "No target account selected.")
            return
        target_num = int(sel.split(" - ")[0])
        if target_num == acc.acc_num:
            messagebox.showwarning("Warning", "Cannot transfer to the same account.")
            return
        receiver = self.accounts.get(target_num)
        if not receiver:
            return
        amount = self._get_amount()
        if amount is None:
            return
        ok, msg = acc.transfer(amount, receiver)
        if ok:
            self.log(f"[{acc.acc_num}] {msg} New balance: {acc.balance}")
        else:
            messagebox.showerror("Failed", msg)
            self.log(f"[{acc.acc_num}] {msg}")

    def show_balance(self):
        acc = self._get_selected_account()
        if not acc:
            return
        messagebox.showinfo("Balance", f"{acc.title} ({acc.acc_num})\nBalance: {acc.balance}")

    def print_slip(self):
        acc = self._get_selected_account()
        if not acc:
            return
        self.log(acc.slip_text())


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()