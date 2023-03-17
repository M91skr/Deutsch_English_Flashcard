"""---------------------------------------- Deutsch/ English Flashcard ----------------------------------------
In this code, In this code, a German to English flashcard is designed to help the user remember 2000 frequently used
German words.
This flash card stores a list of all the words that the user has not learned so far, so that the user does not see
the words that he has learned in the next performances.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import random
from tkinter import *
import  pandas

# ---------------------------------------- Add Parameters ----------------------------------------

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_card = {}
to_learn = {}

""" ---------------------------------------- Education Source Determination ----------------------------------------

If the current run is the first run. Our educational resource is the main source of words containing 2000 words.
But if the current execution is not the first execution, our data source will be the words_to_learn.csv file,
which does not contain the words that the user has learned in previous executions.
"""
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/Deutsch_words.csv")
finally:
    to_learn = data.to_dict(orient="records")

# ---------------------------------------- Word Selection ----------------------------------------


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(language_name, text="Deutsch", fill="black")
    canvas.itemconfig(word, text=current_card["Deutsch"], fill="black")
    flip_timer = window.after(7500, func=flip_card)


def right_answer():
    try:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", header=True, index=False)
        next_card()
    except ValueError:
        next_card()

# ---------------------------------------- Change Card ----------------------------------------


def flip_card():
    canvas.itemconfig(language_name, text="Englisch", fill="white")
    canvas.itemconfig(word, text=current_card["Englisch"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

# ---------------------------------------- GUI Creation ----------------------------------------


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(10000, func=next_card)

# ---------------------------------------- Card Front Design ----------------------------------------


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
language_name = canvas.create_text(400, 150, text="Welcome to German/English flashcards", fill="black", font=(FONT_NAME, 20, "italic"))
word = canvas.create_text(400, 263, text="ok let's start!", fill="black", font=(FONT_NAME, 40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# ---------------------------------------- Card Back Design ----------------------------------------

card_back_img = PhotoImage(file="images/card_back.png")

# ---------------------------------------- Button Design ----------------------------------------

image_right = PhotoImage(file="./images/right.png")
image_wrong = PhotoImage(file="./images/wrong.png")
button_right = Button(image=image_right, bg=BACKGROUND_COLOR, highlightthickness=0, command=right_answer)
button_wrong = Button(image=image_wrong, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
button_right.grid(column=1, row=1)
button_wrong.grid(column=0, row=1)

window.mainloop()