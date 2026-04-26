import tkinter as tk

# IBK 기업은행 CI 색상
IBK_NAVY = "#003478"
IBK_BLUE = "#00A0E0"
IBK_WHITE = "#FFFFFF"
IBK_LIGHT = "#E8F4FD"
IBK_DARK_TEXT = "#002255"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("IBK 계산기")
        self.window.configure(bg=IBK_NAVY)
        self.window.resizable(False, False)

        self.expression = ""

        # 디스플레이
        self.display = tk.Entry(self.window, font=("Arial", 24), justify="right",
                                bd=0, relief="flat",
                                bg=IBK_WHITE, fg=IBK_NAVY,
                                insertbackground=IBK_NAVY)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew",
                          padx=8, pady=(8, 4), ipady=10)

        # 버튼 배치
        buttons = [
            ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0, 2), (".", 5, 2), ("=", 5, 3),
        ]

        operators = {"/", "*", "-", "+", "(", ")"}

        for btn in buttons:
            text, row, col = btn[0], btn[1], btn[2]
            colspan = btn[3] if len(btn) > 3 else 1

            if text == "=":
                bg, fg, abg = IBK_BLUE, IBK_WHITE, "#0080B8"
            elif text == "C":
                bg, fg, abg = "#FF6B6B", IBK_WHITE, "#E05555"
            elif text in operators:
                bg, fg, abg = IBK_LIGHT, IBK_NAVY, "#D0E8F5"
            else:
                bg, fg, abg = IBK_WHITE, IBK_DARK_TEXT, "#F0F0F0"

            b = tk.Button(self.window, text=text, font=("Arial", 18, "bold"),
                          width=4, height=2, bd=0, relief="flat",
                          bg=bg, fg=fg, activebackground=abg, activeforeground=fg,
                          command=lambda t=text: self.on_click(t))
            b.grid(row=row, column=col, columnspan=colspan, sticky="nsew",
                   padx=3, pady=3)

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.expression = result
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "오류")
                self.expression = ""
        else:
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Calculator().run()
