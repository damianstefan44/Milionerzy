import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import openpyxl


# ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Game:
    def __init__(self, nickname):
        self.nickname = nickname
        self.question_type_list = [100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000,
                                   40000, 75000, 125000, 250000, 500000, 1000000]
        self.guaranteed_list = [1000, 40000]
        self.current_question = 0
        self.current_money = 0
        self.guaranteed = 0
        self.question_list = []
        self.questions_path = 'data/questions.xlsx'
        self.already_asked_path = 'data/already_asked.xlsx'

    def read_questions(self):
        excel_questions = pd.read_excel(self.questions_path)
        excel_already_asked = pd.read_excel(self.already_asked_path)
        questions = np.array(excel_questions)
        already_asked = np.array(excel_already_asked)
        for q in questions:
            if q[0] not in already_asked:
                question = Question(q[0], q[1], q[2], q[3], q[4], q[5], q[6], q[7])
                self.question_list.append(question)

        for i in self.question_list:
            print(i.question)

        for i in self.question_list:
            if i.question == "Magnes przyciągnie które z poniższych?":
                self.add_to_already_asked(i)

        # print(questions)

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
        self.menu_image = None

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

        canvas = tk.Canvas(self.root,
                           width=self.root.winfo_screenwidth(),
                           height=self.root.winfo_screenheight(),
                           highlightthickness=0)
        canvas.pack(fill=tk.BOTH,
                    expand=True)

        image = Image.open("photos/milionerzy2.png")
        resized_image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.menu_image = ImageTk.PhotoImage(resized_image)

        canvas.create_image(0, 0,
                            anchor=tk.NW,
                            image=self.menu_image)

        start_button_width = 300
        start_button_height = 80
        start_button_edge = 20

        x1 = canvas.winfo_screenwidth() / 2 - start_button_width / 2
        x2 = canvas.winfo_screenwidth() / 2 + start_button_width / 2
        x3 = x1 - start_button_edge
        x4 = x2 + start_button_edge
        y1 = canvas.winfo_screenheight() / 2 - start_button_height / 2
        y2 = canvas.winfo_screenheight() / 2 + start_button_height / 2
        y3 = y4 = canvas.winfo_screenheight() / 2

        start_button = canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                             outline='#4D5CDC',
                                             fill='#080E43',
                                             width=4)
        start_button_text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                               text="START",
                                               font='Helvetica 26 bold',
                                               fill="white")

        canvas.tag_bind(start_button, "<ButtonRelease-1>", self.start_game)
        canvas.tag_bind(start_button_text, "<ButtonRelease-1>", self.start_game)

    def mainloop(self):
        self.root.mainloop()

    def start_game(self, event):
        print("Game started")


def main():
    # menu = Menu()
    # menu.start_menu()
    # menu.mainloop()
    game = Game("Damian")
    game.read_questions()


if __name__ == '__main__':
    main()
