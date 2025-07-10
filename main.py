import customtkinter as ctk
import logging

from string import ascii_uppercase
from collections import defaultdict
from networking import Networking




logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", filename="Hangman.log", filemode="a")


root = ctk.CTk()
root.geometry("1000x563")
ctk.set_appearance_mode("dark")

letter_buttons: list = []
word_characters: dict = defaultdict(list)


def reset_buttons():
    for button in letter_buttons:
        button.reset()


word = Networking.fetch_word()


class LetterButton(ctk.CTkButton):
    def __init__(self, master, letter, command=None, **kwargs):
        super().__init__(
            master,
            text=letter.upper(),
            width=40,
            height=40,
            corner_radius=5,
            font=("Arial", 16),
            command=self.on_click,
            **kwargs
        )
        self.letter = letter.upper()
        self.user_command = command

    def on_click(self) -> None:
        self.configure(state="disabled")
        if self.user_command:
            self.user_command(self.letter)

    def reset(self) -> None:
        self.configure(state="Normal")

# Create buttons A-Z
resetBtn = ctk.CTkButton(root, text="Reset", command=reset_buttons)
resetBtn.grid(column = 10, row=5)

for i, letter in enumerate(word):
    word_characters[letter].append(i)

print(word_characters)
print(word_characters.keys())


for i, letter in enumerate(ascii_uppercase):
    btn = LetterButton(root, letter)
    btn.grid(row=i // 9, column=i % 9, padx=5, pady=5)
    letter_buttons.append(btn)

root.mainloop()