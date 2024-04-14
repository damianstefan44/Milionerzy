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

        x1 += (start_button_width + padding + 2*start_button_edge)
        x2 += (start_button_width + padding + 2*start_button_edge)
        x3 += (start_button_width + padding + 2*start_button_edge)
        x4 += (start_button_width + padding + 2*start_button_edge)

        qx4 = x2
        qy4 = y1 - (start_button_height + padding)
        qx5 = x4
        qy5 = y4 - (start_button_height + padding)
        qx6 = x2
        qy6 = y2 - (start_button_height + padding)

        self.question_button_Q = self.canvas.create_polygon([qx1, qy1, qx2, qy2, qx3, qy3, qx4, qy4, qx5, qy5, qx6, qy6],
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

        # self.canvas.tag_bind(self.start_button, "<ButtonRelease-1>", self.start_game)
        # self.canvas.tag_bind(self.start_button_text, "<ButtonRelease-1>", self.start_game)
        # self.canvas.tag_bind(self.start_button, "<Enter>", self.on_hover)
        # self.canvas.tag_bind(self.start_button_text, "<Enter>", self.on_hover)
        # self.canvas.tag_bind(self.start_button, "<Leave>", self.on_stop_hover)
        # self.canvas.tag_bind(self.start_button_text, "<Leave>", self.on_stop_hover)

        # TODO PRZEROBIC NA AKCJE DLA ZAZNACZANIA ODPOWIEDZI


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

        prize_values = [0, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 40000, 75000, 125000, 250000, 500000,
                        1000000]
        text_colors = ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 +["white"]

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
        if self.current_question != 14:
            self.current_question = self.current_question + 1
            print(self.current_question)
            self.current_money = self.question_prize_list[self.current_question]
            if self.current_money in self.guaranteed_list:
                self.guaranteed = self.current_money
            self.update_prize_buttons()
            #print(f"Current question: {self.current_question}")
            #print(f"Current money: {self.current_money}")
            #print(f"Guaranteed: {self.guaranteed}")
        else:
            self.end_game()

    def update_prize_buttons(self):
        for i in range(len(self.prize_button_list)):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#4D5CDC')
        self.canvas.itemconfig(self.prize_button_list[self.current_question], outline='#080E43', fill='yellow')

    def load_new_question(self):
        prize = self.question_prize_list[self.current_question + 1]
        question = self.pick_random_question(prize)
        print("New question loaded")
        self.canvas.itemconfigure(self.question_button_Q_text, text=question.question)
        self.canvas.itemconfigure(self.question_button_A_text, text=question.answer_A)
        self.canvas.itemconfigure(self.question_button_B_text, text=question.answer_B)
        self.canvas.itemconfigure(self.question_button_C_text, text=question.answer_C)
        self.canvas.itemconfigure(self.question_button_D_text, text=question.answer_D)
        print(question.question)

        #NWM CZEMU NIE ŁADUJE PYTANIA DO BUTTONA

    def pick_random_question(self, prize):
        result = [q for q in self.question_list if q.prize == prize]
        print(random.sample(result, 1)[0].question)
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

    def on_hover(self, button, event):
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

            #TODO DO PRZETESTOWANIA


    def on_stop_hover(self, button, event):
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

            # TODO DO PRZETESTOWANIA


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
