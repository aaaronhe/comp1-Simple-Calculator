import tkinter as tk
from tkinter import messagebox
import math


class CalculatorApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Desktop Calculator")
        self.resizable(False, False)

        self.expression = ""
        self.memory_value = 0.0

        self._build_ui()
        self._bind_keys()


    def _build_ui(self):
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Segoe UI", 18),
            justify="right",
            bd=8,
            relief="sunken",
            state="readonly",
            readonlybackground="white"
        )
        self.display.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=8, pady=8)
        self._update_display("0")

        buttons = [
            ("MC", 1, 0, self.memory_clear),
            ("MR", 1, 1, self.memory_recall),
            ("MS", 1, 2, self.memory_store),
            ("M+", 1, 3, self.memory_add),
            ("⌫", 1, 4, self.backspace),

            ("CE", 2, 0, self.clear_entry),
            ("C",  2, 1, self.clear_all),
            ("±",  2, 2, self.toggle_sign),
            ("%",  2, 3, self.percent),
            ("÷",  2, 4, lambda: self.append_operator("/")),

            ("7", 3, 0, lambda: self.append_char("7")),
            ("8", 3, 1, lambda: self.append_char("8")),
            ("9", 3, 2, lambda: self.append_char("9")),
            ("×", 3, 3, lambda: self.append_operator("*")),
            ("√", 3, 4, self.square_root),

            ("4", 4, 0, lambda: self.append_char("4")),
            ("5", 4, 1, lambda: self.append_char("5")),
            ("6", 4, 2, lambda: self.append_char("6")),
            ("-", 4, 3, lambda: self.append_operator("-")),
            ("(", 4, 4, lambda: self.append_char("(")),

            ("1", 5, 0, lambda: self.append_char("1")),
            ("2", 5, 1, lambda: self.append_char("2")),
            ("3", 5, 2, lambda: self.append_char("3")),
            ("+", 5, 3, lambda: self.append_operator("+")),
            (")", 5, 4, lambda: self.append_char(")")),

            ("0", 6, 0, lambda: self.append_char("0")),
            (".", 6, 1, lambda: self.append_decimal()),
            ("=", 6, 2, self.evaluate),
        ]

        for r in range(1, 7):
            self.rowconfigure(r, weight=1)
        for c in range(5):
            self.columnconfigure(c, weight=1)

        for label, row, col, cmd in buttons:
            span = 1
            if label == "0":
                span = 2  #
            btn = tk.Button(
                self,
                text=label,
                font=("Segoe UI", 14),
                command=cmd
            )
            btn.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=3, pady=3)

        self.equal_button = tk.Button(
            self,
            text="=",
            font=("Segoe UI", 16, "bold"),
            command=self.evaluate
        )
        self.equal_button.grid(row=6, column=2, columnspan=3, sticky="nsew", padx=3, pady=3)

    def _bind_keys(self):
        self.bind("<Key>", self._on_key)

    def _update_display(self, text):
        if text == "":
            text = "0"
        self.display_var.set(text)

    def _current_number_segment(self):
        """
        Returns the part of the expression after the last operator.
        Used for %, ±, etc.
        """
        last_op_index = -1
        for op in "+-*/":
            idx = self.expression.rfind(op)
            if idx > last_op_index:
                last_op_index = idx
        return self.expression[last_op_index + 1 :]

    def append_char(self, char):
        if self.expression == "0":
            self.expression = char
        else:
            self.expression += char
        self._update_display(self.expression)

    def append_operator(self, op):
        if not self.expression:
            if op == "-":
                self.expression = "-"
            else:
                return
        elif self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self._update_display(self.expression)

    def append_decimal(self):
        segment = self._current_number_segment()
        if "." in segment:
            return
        if not segment:
            self.expression += "0."
        else:
            self.expression += "."
        self._update_display(self.expression)

    def clear_entry(self):
        segment = self._current_number_segment()
        if segment:
            self.expression = self.expression[: -len(segment)]
        self._update_display(self.expression)

    def clear_all(self):
        self.expression = ""
        self._update_display("0")

    def backspace(self):
        self.expression = self.expression[:-1]
        self._update_display(self.expression)

    def toggle_sign(self):
        segment = self._current_number_segment()
        if not segment:
            return
        try:
            value = float(segment)
        except ValueError:
            return
        value = -value
        self.expression = self.expression[: -len(segment)] + str(value)
        self._update_display(self.expression)

    def percent(self):
        segment = self._current_number_segment()
        if not segment:
            return
        try:
            value = float(segment)
        except ValueError:
            return
        value = value / 100.0
        self.expression = self.expression[: -len(segment)] + str(value)
        self._update_display(self.expression)

    def square_root(self):
        segment = self._current_number_segment()
        if not segment:
            return
        try:
            value = float(segment)
            if value < 0:
                raise ValueError("negative")
        except Exception:
            messagebox.showerror("Math error", "Cannot take square root of that.")
            return
        result = math.sqrt(value)
        self.expression = self.expression[: -len(segment)] + str(result)
        self._update_display(self.expression)

    def memory_clear(self):
        self.memory_value = 0.0

    def memory_recall(self):
        self.expression += str(self.memory_value)
        self._update_display(self.expression)

    def memory_store(self):
        try:
            self.memory_value = float(self.display_var.get())
        except ValueError:
            self.memory_value = 0.0

    def memory_add(self):
        try:
            self.memory_value += float(self.display_var.get())
        except ValueError:
            pass

    def evaluate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression, {"__builtins__": None, "math": math}, {})
        except ZeroDivisionError:
            messagebox.showerror("Math error", "Division by zero.")
            self.clear_all()
            return
        except Exception:
            messagebox.showerror("Error", "Something went wrong with that expression.")
            self.clear_all()
            return
        self.expression = str(result)
        self._update_display(self.expression)

    def _on_key(self, event):
        ch = event.char
        if ch.isdigit():
            self.append_char(ch)
        elif ch in "+-*/":
            self.append_operator(ch)
        elif ch == ".":
            self.append_decimal()
        elif event.keysym in ("Return", "KP_Enter"):
            self.evaluate()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear_all()

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()