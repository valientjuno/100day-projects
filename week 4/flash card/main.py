import pandas as pd
import random
from tkinter import *
from pathlib import Path

# ---------------------------- PATH SETUP ------------------------------- #
# Get the directory where this script is located
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"

# ---------------------------- DATA ------------------------------- #
# Try to load words_to_learn.csv; if it doesn't exist, use french_words.csv
try:
    data = pd.read_csv(DATA_DIR / "words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv(DATA_DIR / "french_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}

# ---------------------------- FLASH CARD LOGIC ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data_frame = pd.DataFrame(to_learn)
    data_frame.to_csv(DATA_DIR / "words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg="#B1DDC6")

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file=IMAGES_DIR / "card_front.png")
card_back_img = PhotoImage(file=IMAGES_DIR / "card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg="#B1DDC6", highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file=IMAGES_DIR / "wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

right_image = PhotoImage(file=IMAGES_DIR / "right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()

