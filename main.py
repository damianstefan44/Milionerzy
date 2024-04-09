import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import openpyxl
import random


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
        self.current_question = 0
        self.current_money = 0
        self.guaranteed = 0
        self.question_list = []
        self.questions_path = 'data/questions.xlsx'
        self.already_asked_path = 'data/already_asked.xlsx'

        # DO TESTOWANIA
        self.question_label = None
        self.switch_button = None

    def start(self):
        self.menu_frame.pack_forget()
        # Create a frame for asking questions

        self.canvas = tk.Canvas(self.root,
                                width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(),
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,
                         expand=True)

        image = Image.open("photos/milionerzy_studio3.png")
        resized_image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(resized_image)

        self.canvas.create_image(0, 0,
                                 anchor=tk.NW,
                                 image=self.background_image)

        # Here you can add widgets for asking questions
        # For example:
        self.question_label = tk.Label(self.canvas, text="What is the capital of France?", font="Helvetica 18",
                                       fg="white", bg="#080E43")
        self.question_label.pack()

        # Create a button to switch back to the menu
        self.switch_button = tk.Button(self.canvas, text="Switch to Menu", command=self.next_question)
        self.switch_button.pack()

        self.create_prize_buttons()

        self.game_frame = tk.Frame(self.canvas, background="#080E43")
        self.game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def end_game(self):
        print("Game has ended")
        self.switch_to_menu()

    def switch_to_menu(self):
        self.canvas.destroy()
        self.game_frame.pack_forget()
        self.game_frame.destroy()
        self.menu_frame.pack()

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

        prize_button_0 = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                   outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_0_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                         text="0",
                                                         font='Helvetica 15 bold',
                                                         fill="orange")
        self.prize_button_list.append(prize_button_0)
        self.prize_button_text_list.append(prize_button_0_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_100 = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                    outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_100_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                      text="100",
                                                      font='Helvetica 15 bold',
                                                      fill="orange")
        self.prize_button_list.append(prize_button_100)
        self.prize_button_text_list.append(prize_button_100_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_200 = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                    outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_200_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                      text="200",
                                                      font='Helvetica 15 bold',
                                                      fill="orange")
        self.prize_button_list.append(prize_button_200)
        self.prize_button_text_list.append(prize_button_200_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_300 = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                    outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_300_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                      text="300",
                                                      font='Helvetica 15 bold',
                                                      fill="orange")
        self.prize_button_list.append(prize_button_300)
        self.prize_button_text_list.append(prize_button_300_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_500 = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                    outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_500_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                      text="500",
                                                      font='Helvetica 15 bold',
                                                      fill="orange")
        self.prize_button_list.append(prize_button_500)
        self.prize_button_text_list.append(prize_button_500_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_1k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                    outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_1k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                      text="1000",
                                                      font='Helvetica 15 bold',
                                                      fill="white")
        self.prize_button_list.append(prize_button_1k)
        self.prize_button_text_list.append(prize_button_1k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_2k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                     outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_2k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                       text="2000",
                                                       font='Helvetica 15 bold',
                                                       fill="orange")
        self.prize_button_list.append(prize_button_2k)
        self.prize_button_text_list.append(prize_button_2k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_5k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                     outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_5k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                       text="5000",
                                                       font='Helvetica 15 bold',
                                                       fill="orange")
        self.prize_button_list.append(prize_button_5k)
        self.prize_button_text_list.append(prize_button_5k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_10k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                     outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_10k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                       text="10000",
                                                       font='Helvetica 15 bold',
                                                       fill="orange")
        self.prize_button_list.append(prize_button_10k)
        self.prize_button_text_list.append(prize_button_10k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_20k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_20k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="20000",
                                                        font='Helvetica 15 bold',
                                                        fill="orange")
        self.prize_button_list.append(prize_button_20k)
        self.prize_button_text_list.append(prize_button_20k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_40k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_40k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="40000",
                                                        font='Helvetica 15 bold',
                                                        fill="white")
        self.prize_button_list.append(prize_button_40k)
        self.prize_button_text_list.append(prize_button_40k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_75k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_75k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="75000",
                                                        font='Helvetica 15 bold',
                                                        fill="orange")
        self.prize_button_list.append(prize_button_75k)
        self.prize_button_text_list.append(prize_button_75k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_125k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_125k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="125000",
                                                        font='Helvetica 15 bold',
                                                        fill="orange")
        self.prize_button_list.append(prize_button_125k)
        self.prize_button_text_list.append(prize_button_125k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_250k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_250k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="250000",
                                                        font='Helvetica 15 bold',
                                                        fill="orange")
        self.prize_button_list.append(prize_button_250k)
        self.prize_button_text_list.append(prize_button_250k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_500k = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_500k_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="500000",
                                                        font='Helvetica 15 bold',
                                                        fill="orange")
        self.prize_button_list.append(prize_button_500k)
        self.prize_button_text_list.append(prize_button_500k_text)
        y1 -= (40 + padding)
        y2 -= (40 + padding)
        y3 -= (40 + padding)
        y4 -= (40 + padding)
        prize_button_1m = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
        prize_button_1m_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text="1000000",
                                                        font='Helvetica 15 bold',
                                                        fill="white")
        self.prize_button_list.append(prize_button_1m)
        self.prize_button_text_list.append(prize_button_1m_text)

    def next_question(self):
        if self.current_question != 15:
            self.current_question = self.current_question + 1
            self.load_new_question()
            self.current_money = self.question_prize_list[self.current_question]
            if self.current_money in self.guaranteed_list:
                self.guaranteed = self.current_money
            self.update_prize_buttons()
            print(f"Current question: {self.current_question}")
            print(f"Current money: {self.current_money}")
            print(f"Guaranteed: {self.guaranteed}")
        else:
            self.end_game()

    def update_prize_buttons(self):
        for i in range(len(self.prize_button_list)):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#4D5CDC')
        self.canvas.itemconfig(self.prize_button_list[self.current_question], outline='#080E43', fill='yellow')

    def load_new_question(self):
        print("New question loaded")

    def pick_random_question(self, prize):
        result = [q for q in self.question_list if q.prize == prize]
        print(random.sample(result, 1)[0].question)
        return random.sample(result, 1)[0].question

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
        # game.next_question()
        game.start()
        game.update_prize_buttons()

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
