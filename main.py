import customtkinter as ctk
import logging

from string import ascii_uppercase
from collections import defaultdict
from networking import Networking




logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s   (Line: %(lineno)d [%(filename)s])", 
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    filename="hangman.log", 
                    encoding="utf-8", 
                    filemode="w", 
                    level=logging.INFO)


root = ctk.CTk()
root.geometry("1000x563")
ctk.set_appearance_mode("dark")

letter_buttons: list = []
letter_placeholders: list = []
word_characters: dict = defaultdict(list)


def guess_letter(letter: str) -> None:
    letter = letter.lower()
    if letter in word_characters:
        letter_positions = word_characters[letter]
        for position in letter_positions:
            letter_placeholders[position].configure(text=word[position].upper())


def reset_buttons():
    for button in letter_buttons:
        button.reset()

def get_new_word() -> str:
    new_word = Networking.fetch_word()
    if new_word == None:
        logging.CRITICAL("Word was not obtained successfully!")
        raise ValueError("Word was not obtained successfully!")
    else:
        logging.info("Word api request successful.")
        logging.info(f"The word is {new_word}.")
        return new_word

word = get_new_word()
guesses: int = len(word) + 2

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
            logging.info(f"Letter {self.letter} guessed.")

    def reset(self) -> None:
        self.configure(state="Normal")

# Create buttons A-Z
resetBtn = ctk.CTkButton(root, text="Reset", command=reset_buttons)
resetBtn.grid(column = 10, row=5)

for i, letter in enumerate(word):
    word_characters[letter].append(i)

print(word_characters)
print(list(word_characters.keys()))


for i, letter in enumerate(ascii_uppercase):
    btn = LetterButton(master=root, letter=letter, command=guess_letter)
    btn.grid(row=i // 9, column=i % 9, padx=5, pady=5)
    letter_buttons.append(btn)



for i in range(len(word)):
    lbl = ctk.CTkLabel(root, text="_", font=("Arial", 24))
    lbl.grid(row=6, column=i, padx=5, pady=10)
    letter_placeholders.append(lbl)


root.mainloop()