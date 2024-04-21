import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import openpyxl
import random
from time import sleep


class Game:
    def __init__(self, nickname, menu_frame, root):
        self.nickname = nickname
        self.root = root
        self.menu_frame = menu_frame
        self.game_frame = None
        self.background_image = None
        self.canvas = None
        self.prize_button_list = []
        self.prize_button_text_list = []
        self.question_prize_list = [0, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000,
                                    40000, 75000, 125000, 250000, 500000, 1000000]
        self.guaranteed_list = [1000, 40000, 1000000]
        self.current_question_number = 0
        self.current_money = 0
        self.guaranteed = 0
        self.question_list = []
        self.questions_path = 'data/questions.xlsx'
        self.already_asked_path = 'data/already_asked.xlsx'
        self.current_question = None
        self.currently_clicked = None

        self.question_button_A = None
        self.question_button_A_text = None
        self.question_button_B = None
        self.question_button_B_text = None
        self.question_button_C = None
        self.question_button_C_text = None
        self.question_button_D = None
        self.question_button_D_text = None
        self.question_button_Q = None
        self.question_button_Q_text = None

        # DO TESTOWANIA
        self.question_label = None
        self.switch_button = None

    def start(self):
        self.menu_frame.pack_forget()

        self.init_canvas()  # Initialize canvas
        self.init_buttons()  # Initialize buttons

        self.game_frame = tk.Frame(self.canvas, background="#080E43")
        self.game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def init_canvas(self):
        self.canvas = tk.Canvas(self.root,
                                width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(),
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        image = Image.open("photos/milionerzy_studio3.png")
        resized_image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(0, 0,
                                 anchor=tk.NW,
                                 image=self.background_image)

    def init_buttons(self):
        # Initialize buttons here
        self.question_label = tk.Label(self.canvas, text="What is the capital of France?", font="Helvetica 18",
                                       fg="white", bg="#080E43")
        self.question_label.pack()

        # Create a button to switch back to the menu
        self.switch_button = tk.Button(self.canvas, text="Switch to Menu", command=self.update_after_answer)
        self.switch_button.pack()

        self.create_prize_buttons()
        self.create_question_buttons()

    def end_game(self):
        print("Game has ended")
        self.switch_to_menu()

    def switch_to_menu(self):
        self.canvas.destroy()
        self.game_frame.pack_forget()
        self.game_frame.destroy()
        self.menu_frame.pack()

    def create_question_buttons(self):
        start_button_width = 300
        start_button_height = 80
        start_button_edge = 40
        padding = 5

        x1 = self.canvas.winfo_screenwidth() / 100 * 37.5 - start_button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 100 * 37.5 + start_button_width / 2
        x3 = x1 - start_button_edge
        x4 = x2 + start_button_edge
        y1 = self.canvas.winfo_screenheight() * 16 / 20 - start_button_height / 2
        y2 = self.canvas.winfo_screenheight() * 16 / 20 + start_button_height / 2
        y3 = y4 = self.canvas.winfo_screenheight() * 16 / 20

        qx1 = x1
        qy1 = y2 - (start_button_height + padding)
        qx2 = x3
        qy2 = y3 - (start_button_height + padding)
        qx3 = x1
        qy3 = y1 - (start_button_height + padding)

        self.question_button_A = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_A_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                              text="A",
                                                              font='Helvetica 10 bold',
                                                              fill="orange")

        x1 += (start_button_width + padding + 2 * start_button_edge)
        x2 += (start_button_width + padding + 2 * start_button_edge)
        x3 += (start_button_width + padding + 2 * start_button_edge)
        x4 += (start_button_width + padding + 2 * start_button_edge)

        qx4 = x2
        qy4 = y1 - (start_button_height + padding)
        qx5 = x4
        qy5 = y4 - (start_button_height + padding)
        qx6 = x2
        qy6 = y2 - (start_button_height + padding)

        self.question_button_Q = self.canvas.create_polygon(
            [qx1, qy1, qx2, qy2, qx3, qy3, qx4, qy4, qx5, qy5, qx6, qy6],
            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_Q_text = self.canvas.create_text((qx1 + qx6) / 2, qy2,
                                                              text="",
                                                              font='Helvetica 12 bold',
                                                              fill="orange")

        self.question_button_B = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_B_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                              text="B",
                                                              font='Helvetica 10 bold',
                                                              fill="orange")
        y1 += (start_button_height + padding)
        y2 += (start_button_height + padding)
        y3 += (start_button_height + padding)
        y4 += (start_button_height + padding)
        self.question_button_D = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_D_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                              text="D",
                                                              font='Helvetica 10 bold',
                                                              fill="orange")

        x1 -= (start_button_width + padding + 2 * start_button_edge)
        x2 -= (start_button_width + padding + 2 * start_button_edge)
        x3 -= (start_button_width + padding + 2 * start_button_edge)
        x4 -= (start_button_width + padding + 2 * start_button_edge)
        self.question_button_C = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_C_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                              text="C",
                                                              font='Helvetica 10 bold',
                                                              fill="orange")
        self.bind_buttons()

    def bind_buttons(self):
        buttons = [self.question_button_A, self.question_button_A_text,
                   self.question_button_B, self.question_button_B_text,
                   self.question_button_C, self.question_button_C_text,
                   self.question_button_D, self.question_button_D_text]
        params = ["A", "A", "B", "B", "C", "C", "D", "D"]
        for i in range(8):
            self.canvas.tag_bind(buttons[i], "<ButtonRelease-1>",
                                 lambda event, param1=params[i]: self.click_answer(event, param1))
            self.canvas.tag_bind(buttons[i], "<Enter>",
                                 lambda event, param1=params[i]: self.on_hover(event, param1))
            self.canvas.tag_bind(buttons[i], "<Leave>",
                                 lambda event, param1=params[i]: self.on_stop_hover(event, param1))

    def unbind_button(self, button):
        actions = ["<ButtonRelease-1>", "<Enter>", "<Leave>"]
        for a in actions:
            self.canvas.tag_unbind(button, a)

    def unbind_all(self):
        buttons = [self.question_button_A, self.question_button_A_text,
                   self.question_button_B, self.question_button_B_text,
                   self.question_button_C, self.question_button_C_text,
                   self.question_button_D, self.question_button_D_text]
        actions = ["<ButtonRelease-1>", "<Enter>", "<Leave>"]
        for b in buttons:
            for a in actions:
                self.canvas.tag_unbind(b, a)

    def reset_buttons(self):
        self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_button_B, outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_button_C, outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_button_D, outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_button_A_text, fill="orange")
        self.canvas.itemconfig(self.question_button_B_text, fill="orange")
        self.canvas.itemconfig(self.question_button_C_text, fill="orange")
        self.canvas.itemconfig(self.question_button_D_text, fill="orange")

    def reset_attributes(self):
        self.current_question = None
        self.currently_clicked = None

    def printTest(self, event):
        print("działa")

    def next_question(self):
        if self.current_question_number < 15:
            self.reset_attributes()
            self.reset_buttons()
            self.bind_buttons()
            self.update_after_answer()
            self.load_new_question()
        else:
            print("Gratulację - wygrałeś MILION")

    def show_answer(self, answer):
        correct_answer = self.current_question.correct_answer
        correct_button = None
        correct_button_text = None

        if correct_answer == "A":
            correct_button = self.question_button_A
            correct_button_text = self.question_button_A_text
        elif correct_answer == "B":
            correct_button = self.question_button_B
            correct_button_text = self.question_button_B_text
        elif correct_answer == "C":
            correct_button = self.question_button_C
            correct_button_text = self.question_button_C_text
        elif correct_answer == "D":
            correct_button = self.question_button_D
            correct_button_text = self.question_button_D_text
        else:
            print(f"Odpowiedzia powinno byc A, B, C, lub D, a nie: {correct_answer}")

        if answer == "A":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#00FF00')
                self.root.after(3000, lambda: self.next_question())
            else:
                self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.root.after(5000, lambda: self.end_game())
        elif answer == "B":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#00FF00')
                self.root.after(3000, lambda: self.next_question())
            else:
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.root.after(5000, lambda: self.end_game())
        elif answer == "C":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#00FF00')
                self.root.after(3000, lambda: self.next_question())
            else:
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.root.after(5000, lambda: self.end_game())
        elif answer == "D":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#00FF00')
                self.root.after(3000, lambda: self.next_question())
            else:
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.root.after(5000, lambda: self.end_game())
        else:
            print(f"Odpowiedzia powinno byc A, B, C, lub D, a nie: {answer}")

    def check_answer(self, answer):
        print(f"Sprawdzam {answer}")
        if self.current_question_number in [0, 1, 2, 3]:
            self.root.after(2000, lambda: self.show_answer(answer))
        elif self.current_question_number in [5, 6, 7, 8]:
            self.root.after(3000, lambda: self.show_answer(answer))
        elif self.current_question_number in [10, 11, 12, 13]:
            self.root.after(4000, lambda: self.show_answer(answer))
        elif self.current_question_number in [4, 9, 14]:
            self.root.after(6000, lambda: self.show_answer(answer))
        else:
            print("Bledny numer pytania")

    def click_answer(self, event, answer):
        if answer == "A":
            if self.currently_clicked == "A":
                self.unbind_all()
                self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#F75B11')
                self.canvas.itemconfig(self.question_button_A_text, fill='#FFFFFF')
                self.check_answer(answer)
            else:
                self.currently_clicked = "A"
                self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#4D5CDC')
                self.canvas.itemconfig(self.question_button_B, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_C, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_D, outline='#4D5CDC', fill='#080E43')
                self.canvas.tag_unbind(self.question_button_A, "<Enter>")
                self.canvas.tag_unbind(self.question_button_A_text, "<Enter>")
                self.canvas.tag_unbind(self.question_button_A, "<Leave>")
                self.canvas.tag_unbind(self.question_button_A_text, "<Leave>")
                self.canvas.tag_bind(self.question_button_B, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
        elif answer == "B":
            if self.currently_clicked == "B":
                self.unbind_all()
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#F75B11')
                self.canvas.itemconfig(self.question_button_B_text, fill='#ffffff')
                self.check_answer(answer)
            else:
                self.currently_clicked = "B"
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#4D5CDC')
                self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_C, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_D, outline='#4D5CDC', fill='#080E43')
                self.canvas.tag_unbind(self.question_button_B, "<Enter>")
                self.canvas.tag_unbind(self.question_button_B_text, "<Enter>")
                self.canvas.tag_unbind(self.question_button_B, "<Leave>")
                self.canvas.tag_unbind(self.question_button_B_text, "<Leave>")
                self.canvas.tag_bind(self.question_button_A, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
        elif answer == "C":
            if self.currently_clicked == "C":
                self.unbind_all()
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#F75B11')
                self.canvas.itemconfig(self.question_button_C_text, fill='#ffffff')
                self.check_answer(answer)
            else:
                self.currently_clicked = "C"
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#4D5CDC')
                self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_B, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_D, outline='#4D5CDC', fill='#080E43')
                self.canvas.tag_unbind(self.question_button_C, "<Enter>")
                self.canvas.tag_unbind(self.question_button_C_text, "<Enter>")
                self.canvas.tag_unbind(self.question_button_C, "<Leave>")
                self.canvas.tag_unbind(self.question_button_C_text, "<Leave>")
                self.canvas.tag_bind(self.question_button_B, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Enter>",
                                     lambda e, param1="D": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_D_text, "<Leave>",
                                     lambda e, param1="D": self.on_stop_hover(e, param1))
        elif answer == "D":
            if self.currently_clicked == "D":
                self.unbind_all()
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#F75B11')
                self.canvas.itemconfig(self.question_button_D_text, fill='#ffffff')
                self.check_answer(answer)
            else:
                self.currently_clicked = "D"
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#4D5CDC')
                self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_B, outline='#4D5CDC', fill='#080E43')
                self.canvas.itemconfig(self.question_button_C, outline='#4D5CDC', fill='#080E43')
                self.canvas.tag_unbind(self.question_button_D, "<Enter>")
                self.canvas.tag_unbind(self.question_button_D_text, "<Enter>")
                self.canvas.tag_unbind(self.question_button_D, "<Leave>")
                self.canvas.tag_unbind(self.question_button_D_text, "<Leave>")
                self.canvas.tag_bind(self.question_button_B, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Enter>",
                                     lambda e, param1="B": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_B_text, "<Leave>",
                                     lambda e, param1="B": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Enter>",
                                     lambda e, param1="C": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_C_text, "<Leave>",
                                     lambda e, param1="C": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Enter>",
                                     lambda e, param1="A": self.on_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
                self.canvas.tag_bind(self.question_button_A_text, "<Leave>",
                                     lambda e, param1="A": self.on_stop_hover(e, param1))
        else:
            print("Bad argument - button")

    def create_prize_buttons(self):
        start_button_width = 180
        start_button_height = 40
        start_button_edge = 15
        padding = 5

        x1 = self.canvas.winfo_screenwidth() / 100 * 92 - start_button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 100 * 92 + start_button_width / 2
        x3 = x1 - start_button_edge
        x4 = x2 + start_button_edge
        y1 = self.canvas.winfo_screenheight() * 19 / 20 - start_button_height / 2
        y2 = self.canvas.winfo_screenheight() * 19 / 20 + start_button_height / 2
        y3 = y4 = self.canvas.winfo_screenheight() * 19 / 20

        prize_values = ["0 zł", "100 zł", "200 zł", "300 zł", "500 zł", "1000 zł", "2000 zł", "5000 zł", "10 000 zł", "20 000 zł", "40 000 zł", "75 000 zł", "125 000 zł", "250 000 zł", "500 000 zł",
                        "1 000 000 zł"]
        text_colors = ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 + ["white"]

        for prize_value, text_color in zip(prize_values, text_colors):
            prize_button = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
            prize_button_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text=str(prize_value),
                                                        font='Helvetica 15 bold',
                                                        fill=text_color)
            self.prize_button_list.append(prize_button)
            self.prize_button_text_list.append(prize_button_text)
            y1 -= (40 + padding)
            y2 -= (40 + padding)
            y3 -= (40 + padding)
            y4 -= (40 + padding)

    def update_after_answer(self):
        if self.current_question_number != 14:
            self.current_question_number = self.current_question_number + 1
            print(self.current_question_number)
            self.current_money = self.question_prize_list[self.current_question_number]
            print(f"Masz aktualnie: {self.current_money}")
            if self.current_money in self.guaranteed_list:
                self.guaranteed = self.current_money
            self.update_prize_buttons()
            # print(f"Current question: {self.current_question_number}")
            # print(f"Current money: {self.current_money}")
            # print(f"Guaranteed: {self.guaranteed}")
        else:
            self.root.after(5000, lambda: self.end_game())

    def update_prize_buttons(self):
        for i in range(len(self.prize_button_list)):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#4D5CDC')
        for i in range(self.current_question_number + 1):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#00FF00')
        self.canvas.itemconfig(self.prize_button_list[self.current_question_number + 1], outline='#080E43', fill='yellow')

    def load_new_question(self):
        prize = self.question_prize_list[self.current_question_number + 1]
        print(prize)
        self.current_question = self.pick_random_question(prize)
        # self.add_to_already_asked(self.current_question)
        print("New question loaded")
        self.canvas.itemconfigure(self.question_button_Q_text, text=self.current_question.question)
        self.canvas.itemconfigure(self.question_button_A_text, text=self.current_question.answer_A)
        self.canvas.itemconfigure(self.question_button_B_text, text=self.current_question.answer_B)
        self.canvas.itemconfigure(self.question_button_C_text, text=self.current_question.answer_C)
        self.canvas.itemconfigure(self.question_button_D_text, text=self.current_question.answer_D)
        print(self.current_question.question)

    def pick_random_question(self, prize):
        result = [q for q in self.question_list if q.prize == prize]
        #print(result)
        #print(random.sample(result, 1)[0].question)
        return random.sample(result, 1)[0]

    def read_questions(self):
        excel_questions = pd.read_excel(self.questions_path)
        excel_already_asked = pd.read_excel(self.already_asked_path)
        questions = np.array(excel_questions)
        already_asked = np.array(excel_already_asked)

        for q in questions:
            if q[0] not in already_asked:
                question = Question(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7])
                self.question_list.append(question)

    def add_to_already_asked(self, question):
        excel_already_asked = pd.read_excel(self.already_asked_path, )
        question_df = pd.DataFrame({"question": [question.question]})
        merged_df = pd.concat([excel_already_asked, question_df], ignore_index=True)
        merged_df.to_excel(self.already_asked_path, index=False)

        self.question_list = [q for q in self.question_list if q.question != question.question]
        # remove from current question list in case of question swap

    def on_hover(self, event, button):
        if button == "A":
            self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#4D5CDC')
        elif button == "B":
            self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#4D5CDC')
        elif button == "C":
            self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#4D5CDC')
        elif button == "D":
            self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#4D5CDC')
        else:
            print("Bad argument - button")

    def on_stop_hover(self, event, button):
        if button == "A":
            self.canvas.itemconfig(self.question_button_A, outline='#4D5CDC', fill='#080E43')
        elif button == "B":
            self.canvas.itemconfig(self.question_button_B, outline='#4D5CDC', fill='#080E43')
        elif button == "C":
            self.canvas.itemconfig(self.question_button_C, outline='#4D5CDC', fill='#080E43')
        elif button == "D":
            self.canvas.itemconfig(self.question_button_D, outline='#4D5CDC', fill='#080E43')
        else:
            print("Bad argument - button")


class Question:
    def __init__(self, question, correct_answer, answer_A, answer_B, answer_C, answer_D, category, prize):
        self.question = question
        self.correct_answer = correct_answer
        self.answer_A = answer_A
        self.answer_B = answer_B
        self.answer_C = answer_C
        self.answer_D = answer_D
        self.category = category
        self.prize = prize


class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.background_image = None
        self.start_button = None
        self.start_button_text = None
        self.canvas = None
        self.menu_frame = None

    def end_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

    def switch_fullscreen(self, event):
        if self.root.attributes('-fullscreen') == 1:
            self.end_fullscreen(self)
        else:
            self.root.attributes('-fullscreen', True)

    def start_menu(self):
        self.root.title("Milionerzy")
        self.root.attributes('-fullscreen', True)
        self.root.pack_propagate(False)
        self.root.configure(background='#080E43')

        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind("<F11>", self.switch_fullscreen)

        self.canvas = tk.Canvas(self.root,
                                width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(),
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,
                         expand=True)

        image = Image.open("photos/milionerzy2.png")
        resized_image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(0, 0,
                                 anchor=tk.NW,
                                 image=self.background_image)

        start_button_width = 300
        start_button_height = 80
        start_button_edge = 20

        x1 = self.canvas.winfo_screenwidth() / 2 - start_button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 2 + start_button_width / 2
        x3 = x1 - start_button_edge
        x4 = x2 + start_button_edge
        y1 = self.canvas.winfo_screenheight() / 2 - start_button_height / 2
        y2 = self.canvas.winfo_screenheight() / 2 + start_button_height / 2
        y3 = y4 = self.canvas.winfo_screenheight() / 2

        self.start_button = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                       outline='#4D5CDC',
                                                       fill='#080E43',
                                                       width=4)
        self.start_button_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                         text="START",
                                                         font='Helvetica 26 bold',
                                                         fill="white")

        self.canvas.tag_bind(self.start_button, "<ButtonRelease-1>", self.start_game)
        self.canvas.tag_bind(self.start_button_text, "<ButtonRelease-1>", self.start_game)
        self.canvas.tag_bind(self.start_button, "<Enter>", self.on_hover)
        self.canvas.tag_bind(self.start_button_text, "<Enter>", self.on_hover)
        self.canvas.tag_bind(self.start_button, "<Leave>", self.on_stop_hover)
        self.canvas.tag_bind(self.start_button_text, "<Leave>", self.on_stop_hover)

        self.menu_frame = tk.Frame(self.canvas, background="#080E43")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.menu_frame.lower()

    def mainloop(self):
        self.root.mainloop()

    def start_game(self, event):
        print("Game started")
        # Hide the menu frame
        self.menu_frame.pack_forget()
        game = Game("Test", self.canvas, self.root)
        game.read_questions()
        game.start()
        game.update_prize_buttons()
        game.load_new_question()

    def on_hover(self, event):
        self.canvas.itemconfig(self.start_button, outline='#080E43', fill='#4D5CDC')

    def on_stop_hover(self, event):
        self.canvas.itemconfig(self.start_button, outline='#4D5CDC', fill='#080E43')


def main():
    menu = Menu()
    menu.start_menu()
    menu.mainloop()
    # game = Game("Damian")
    # game.read_questions()
    # game.pick_random_question(100)


if __name__ == '__main__':
    main()
