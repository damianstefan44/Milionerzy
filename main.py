import textwrap
import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import openpyxl
import random
import pygame.mixer


def cut_question(question, width=20):
    # Split the question into lines
    lines = question.split('\n')

    # Cut each line to fit within the specified width
    cut_lines = []
    for line in lines:
        if len(line) <= width:
            cut_lines.append(line)
        else:
            # Split the line into words
            words = line.split()

            # Cut the line into lines of the specified width
            cut_line = ''
            for word in words:
                if len(cut_line) + len(word) + 1 <= width:
                    cut_line += word + ' '
                else:
                    cut_lines.append(cut_line.strip())
                    cut_line = word + ' '

            # Add the remaining line
            if cut_line.strip():
                cut_lines.append(cut_line.strip())

    # Join the cut lines back into a single string
    return '\n'.join(cut_lines)


class Game:
    def __init__(self, nickname, menu_frame, root):
        self.nickname = nickname
        self.root = root
        self.menu_frame = menu_frame
        self.game_frame = None
        self.background_image = None
        self.option_menu = None
        self.lifeline_specialist_image = None
        self.lifeline_specialist = None
        self.lifeline_50_image = None
        self.lifeline_50 = None
        self.lifeline_phone_image = None
        self.lifeline_phone = None
        self.lifeline_swap_image = None
        self.lifeline_swap = None
        self.lifeline_exit_image = None
        self.lifeline_exit = None
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
        self.questions_path = 'data/questions2.xlsx'
        self.already_asked_path = 'data/already_asked.xlsx'
        self.current_question = None
        self.currently_clicked = None
        self.timer_time_left = 0
        self.timer_start_button = None
        self.timer_stop_button = None
        self.timer_start_button_text = ""
        self.timer_stop_button_text = ""
        self.timer_text = ""
        self.end_prize_text = None
        self.start_button_clicked = None
        self.bad_answer = False
        self.end_prize = 0
        self.answer_clicked = False

        self.audio_event = None
        self.audio_channel_1 = None
        self.audio_channel_2 = None
        self.audio_next_question = pygame.mixer.Sound("audio/next_question.wav")
        self.audio_background = pygame.mixer.Sound("audio/background1.wav")
        self.audio_menu = pygame.mixer.Sound("audio/menu.wav")
        self.audio_wrong_answer = pygame.mixer.Sound("audio/wrong_answer.wav")
        self.audio_right_answer = pygame.mixer.Sound("audio/right_answer.wav")
        self.audio_right_answer_guaranteed = pygame.mixer.Sound("audio/right_answer_guaranteed.wav")
        self.audio_million = pygame.mixer.Sound("audio/million.wav")
        self.audio_phone = pygame.mixer.Sound("audio/phone.wav")
        self.audio_end_prize = pygame.mixer.Sound("audio/end_prize.wav")
        self.audio_click_answer = pygame.mixer.Sound("audio/click_answer.wav")
        self.audio_lifeline = pygame.mixer.Sound("audio/lifeline.wav")

        self.question_button_A = None
        self.question_button_A_text = None
        self.A_text = None
        self.question_button_B = None
        self.question_button_B_text = None
        self.B_text = None
        self.question_button_C = None
        self.question_button_C_text = None
        self.C_text = None
        self.question_button_D = None
        self.question_button_D_text = None
        self.D_text = None
        self.question_button_Q = None
        self.question_button_Q_text = None

        # DO TESTOWANIA
        self.question_label = None
        self.switch_button = None

    def start(self):
        self.menu_frame.pack_forget()
        self.init_canvas()  # Initialize canvas
        self.init_buttons()  # Initialize buttons
        self.game_frame.update()
        self.game_frame.update_idletasks()
        pygame.mixer.music.stop()
        #self.reset_channels()
        self.audio_next_question.fadeout(4000)
        self.audio_channel_1 = self.audio_next_question.play()
        self.root.after(2500, lambda: self.play_background_music())

    def reset_channels(self):
        pygame.mixer.music.stop()
        if self.audio_channel_1:
            self.audio_channel_1.stop()
            print("zastopowalem 1")
        if self.audio_channel_2:
            self.audio_channel_2.stop()
            print("zastopowalem 2")

    def play_sound(self, path, fade=0, duration=0, callback=None):
        pygame.mixer.music.load(path)
        if fade > 0:
            pygame.mixer.music.fadeout(fade * 1000)

        if duration > 0:
            self.root.after(duration * 1000, self.stop_music)
        if callback:
            self.audio_event = self.root.after(duration * 1000, callback)

        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_menu_music(self):
        self.reset_channels()
        self.audio_channel_2 = self.audio_menu.play(loops=-1, fade_ms=1000)

    def play_background_music(self):
        if self.audio_channel_2:
            self.audio_channel_2.stop()
        self.audio_channel_2 = self.audio_background.play(loops=-1, fade_ms=1000)
        self.root.after(2000, self.audio_channel_1.stop)

    def create_black_rectangle(self, width):
        rectangle = self.canvas.create_rectangle(0, 0, width, self.canvas.winfo_screenheight(), fill="#06070C")
        self.option_menu = rectangle

    def put_image_in_object(self, image_path, object_label, x, y):
        image = Image.open(image_path)
        resized_image = image.resize((146, 101))
        lifeline_image = ImageTk.PhotoImage(resized_image)
        lifeline = self.canvas.create_image(x, y,
                                            anchor=tk.NW,
                                            image=lifeline_image)
        if object_label == "specialist":
            self.lifeline_specialist_image = lifeline_image
            self.lifeline_specialist = lifeline
        elif object_label == "50":
            self.lifeline_50_image = lifeline_image
            self.lifeline_50 = lifeline
        elif object_label == "phone":
            self.lifeline_phone_image = lifeline_image
            self.lifeline_phone = lifeline
        elif object_label == "swap":
            self.lifeline_swap_image = lifeline_image
            self.lifeline_swap = lifeline
        elif object_label == "exit":
            self.lifeline_exit_image = lifeline_image
            self.lifeline_exit = lifeline
        else:
            print("Bad argument - object_label")

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
        self.create_black_rectangle(200)

        start_position = 50
        padding = self.root.winfo_screenheight() / 6

        self.put_image_in_object("photos/lifeline_specialist_black.png", "specialist", 25, start_position)
        self.put_image_in_object("photos/lifeline_50_black.png", "50", 25, start_position + padding)
        self.put_image_in_object("photos/lifeline_phone_black.png", "phone", 25, start_position + 2 * padding)
        self.put_image_in_object("photos/lifeline_swap_black.png", "swap", 25, start_position + 3 * padding)
        self.put_image_in_object("photos/lifeline_exit_black.png", "exit", 25,
                                 self.root.winfo_screenheight() - 3 * start_position)

        self.game_frame = tk.Frame(self.canvas, background="#080E43")
        self.game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.canvas.tag_bind(self.lifeline_specialist, "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, "specialist"))
        self.canvas.tag_bind(self.lifeline_specialist, "<Enter>",
                             lambda event: self.on_lifeline_hover(event, "specialist"))
        self.canvas.tag_bind(self.lifeline_specialist, "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, "specialist"))
        self.canvas.tag_bind(self.lifeline_50, "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, "50"))
        self.canvas.tag_bind(self.lifeline_50, "<Enter>",
                             lambda event: self.on_lifeline_hover(event, "50"))
        self.canvas.tag_bind(self.lifeline_50, "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, "50"))
        self.canvas.tag_bind(self.lifeline_phone, "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, "phone"))
        self.canvas.tag_bind(self.lifeline_phone, "<Enter>",
                             lambda event: self.on_lifeline_hover(event, "phone"))
        self.canvas.tag_bind(self.lifeline_phone, "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, "phone"))
        self.canvas.tag_bind(self.lifeline_swap, "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, "swap"))
        self.canvas.tag_bind(self.lifeline_swap, "<Enter>",
                             lambda event: self.on_lifeline_hover(event, "swap"))
        self.canvas.tag_bind(self.lifeline_swap, "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, "swap"))
        self.canvas.tag_bind(self.lifeline_exit, "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, "exit"))
        self.canvas.tag_bind(self.lifeline_exit, "<Enter>",
                             lambda event: self.on_lifeline_hover(event, "exit"))
        self.canvas.tag_bind(self.lifeline_exit, "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, "exit"))

    def on_lifeline_hover(self, event, lifeline):
        if lifeline == "specialist":
            image = Image.open("photos/lifeline_specialist_blue.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_specialist, image=lifeline_image)
            self.lifeline_specialist_image = lifeline_image
        elif lifeline == "50":
            image = Image.open("photos/lifeline_50_blue.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_50, image=lifeline_image)
            self.lifeline_50_image = lifeline_image
        elif lifeline == "phone":
            image = Image.open("photos/lifeline_phone_blue.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_phone, image=lifeline_image)
            self.lifeline_phone_image = lifeline_image
        elif lifeline == "swap":
            image = Image.open("photos/lifeline_swap_blue.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_swap, image=lifeline_image)
            self.lifeline_swap_image = lifeline_image
        elif lifeline == "exit":
            image = Image.open("photos/lifeline_exit_blue.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_exit, image=lifeline_image)
            self.lifeline_exit_image = lifeline_image
        else:
            print("Bad argument - lifeline - on_lifeline_hover")

    def on_lifeline_stop_hover(self, event, lifeline):
        if lifeline == "specialist":
            image = Image.open("photos/lifeline_specialist_black.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_specialist, image=lifeline_image)
            self.lifeline_specialist_image = lifeline_image
        elif lifeline == "50":
            image = Image.open("photos/lifeline_50_black.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_50, image=lifeline_image)
            self.lifeline_50_image = lifeline_image
        elif lifeline == "phone":
            image = Image.open("photos/lifeline_phone_black.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_phone, image=lifeline_image)
            self.lifeline_phone_image = lifeline_image
        elif lifeline == "swap":
            image = Image.open("photos/lifeline_swap_black.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_swap, image=lifeline_image)
            self.lifeline_swap_image = lifeline_image
        elif lifeline == "exit":
            image = Image.open("photos/lifeline_exit_black.png")
            resized_image = image.resize((146, 101))
            lifeline_image = ImageTk.PhotoImage(resized_image)
            self.canvas.itemconfig(self.lifeline_exit, image=lifeline_image)
            self.lifeline_exit_image = lifeline_image
        else:
            print("Bad argument - lifeline - on_lifeline_stop_hover")

    def on_lifeline_click(self, event, lifeline):
        if lifeline == "specialist":
            if not self.answer_clicked and not self.start_button_clicked:
                image = Image.open("photos/lifeline_specialist_red.png")
                resized_image = image.resize((146, 101))
                lifeline_image = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.lifeline_specialist, image=lifeline_image)
                self.lifeline_specialist_image = lifeline_image
                self.unbind_button(self.lifeline_specialist)
                self.audio_channel_1.stop()
                self.audio_channel_1.play(self.audio_lifeline)
                self.phone_a_friend()
        elif lifeline == "50":
            if not self.answer_clicked and not self.start_button_clicked:
                image = Image.open("photos/lifeline_50_red.png")
                resized_image = image.resize((146, 101))
                lifeline_image = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.lifeline_50, image=lifeline_image)
                self.lifeline_50_image = lifeline_image
                self.unbind_button(self.lifeline_50)
                self.audio_channel_1.stop()
                self.audio_channel_1.play(self.audio_lifeline)
                self.fifty_fifty()
        elif lifeline == "phone":
            if not self.answer_clicked and not self.start_button_clicked:
                image = Image.open("photos/lifeline_phone_red.png")
                resized_image = image.resize((146, 101))
                lifeline_image = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.lifeline_phone, image=lifeline_image)
                self.lifeline_phone_image = lifeline_image
                self.unbind_button(self.lifeline_phone)
                self.audio_channel_1.stop()
                self.audio_channel_1.play(self.audio_lifeline)
                self.phone_a_friend()
        elif lifeline == "swap":
            if not self.answer_clicked and not self.start_button_clicked:
                image = Image.open("photos/lifeline_swap_red.png")
                resized_image = image.resize((146, 101))
                lifeline_image = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.lifeline_swap, image=lifeline_image)
                self.lifeline_swap_image = lifeline_image
                self.unbind_button(self.lifeline_swap)
                self.audio_channel_1.stop()
                self.audio_channel_1.play(self.audio_lifeline)
                self.swap_question()
        elif lifeline == "exit":
            if not self.answer_clicked and not self.start_button_clicked:
                image = Image.open("photos/lifeline_exit_red.png")
                resized_image = image.resize((146, 101))
                lifeline_image = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.lifeline_exit, image=lifeline_image)
                self.lifeline_exit_image = lifeline_image
                self.unbind_button(self.lifeline_exit)
                self.audio_channel_1.stop()
                self.audio_channel_1.play(self.audio_lifeline)
                self.end_game()
        else:
            print("Bad argument - lifeline - on_lifeline_hover")

    def fifty_fifty(self):
        answers = ["A", "B", "C", "D"]
        answers_text_dict = {"A": self.question_button_A_text, "B": self.question_button_B_text,
                             "C": self.question_button_C_text, "D": self.question_button_D_text}
        answers_dict = {"A": self.question_button_A, "B": self.question_button_B,
                        "C": self.question_button_C, "D": self.question_button_D}

        answers.remove(self.current_question.correct_answer)
        random_answer = random.choice(answers)
        answers.remove(random_answer)

        for answer in answers:
            self.canvas.itemconfig(answers_text_dict[answer], text="")
            self.unbind_button(answers_dict[answer])

    def swap_question(self):
        self.current_question_number = self.current_question_number - 1
        self.current_money = self.question_prize_list[self.current_question_number]
        self.next_question(swap=True)

    def phone_a_friend(self):
        self.reset_phone_lifeline()
        self.start_button_clicked = False
        start_button_width = 180
        start_button_height = 40
        start_button_edge = 15
        padding = 5
        to_top = 80

        x1 = self.canvas.winfo_screenwidth() / 100 * 92 - start_button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 100 * 92 + start_button_width / 2
        x3 = x1 - start_button_edge
        x4 = x2 + start_button_edge
        y1 = self.canvas.winfo_screenheight() * 1 / 20 - start_button_height / 2
        y2 = self.canvas.winfo_screenheight() * 1 / 20 + start_button_height / 2
        y3 = y4 = self.canvas.winfo_screenheight() * 1 / 20

        self.timer_start_button = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                             outline='#4D5CDC', fill='#080E43', width=0)
        self.timer_start_button_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                               text="START",
                                                               font='Helvetica 15 bold',
                                                               fill="white")
        y1 += (40 + padding)
        y2 += (40 + padding)
        y3 += (40 + padding)
        y4 += (40 + padding)

        self.timer_stop_button = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.timer_stop_button_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                              text="STOP",
                                                              font='Helvetica 15 bold',
                                                              fill="white")

        self.timer_text = self.canvas.create_text(self.canvas.winfo_screenwidth() / 2,
                                                  self.canvas.winfo_screenheight() / 2 - to_top,
                                                  text="",
                                                  font='Helvetica 80 bold',
                                                  fill="white")

        self.canvas.tag_bind(self.timer_start_button, "<Enter>",
                             lambda e, param1="start": self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer_start_button, "<Leave>",
                             lambda e, param1="start": self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer_start_button, "<Double-Button-1>", self.start_timer)
        self.canvas.tag_bind(self.timer_start_button_text, "<Enter>",
                             lambda e, param1="start": self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer_start_button_text, "<Leave>",
                             lambda e, param1="start": self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer_start_button_text, "<Double-Button-1>", self.start_timer)
        self.canvas.tag_bind(self.timer_stop_button, "<Enter>",
                             lambda e, param1="stop": self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer_stop_button, "<Leave>",
                             lambda e, param1="stop": self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer_stop_button, "<Double-Button-1>", self.stop_timer)
        self.canvas.tag_bind(self.timer_stop_button_text, "<Enter>",
                             lambda e, param1="stop": self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer_stop_button_text, "<Leave>",
                             lambda e, param1="stop": self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer_stop_button_text, "<Double-Button-1>", self.stop_timer)

    def start_timer(self, event):
        if not self.start_button_clicked:
            if self.audio_channel_2:
                self.audio_channel_2.stop()
            if self.audio_channel_1:
                self.audio_channel_1.stop()
            self.audio_channel_1.play(self.audio_phone)
            self.timer_time_left = 30
            self.start_button_clicked = True
            self.countdown()

    def countdown(self):
        if self.timer_time_left <= -1:
            self.canvas.after(1000, self.canvas.itemconfig(self.timer_text, text=""))
            self.audio_channel_1.stop()
            self.audio_channel_2.play(self.audio_background)
            self.start_button_clicked = False
        else:
            self.canvas.itemconfig(self.timer_text, text=f"{self.timer_time_left}")
            self.timer_time_left -= 1
            self.root.after(1000, self.countdown)

    def stop_timer(self, event):
        if self.start_button_clicked:
            self.timer_time_left = 0
            self.start_button_clicked = False

    def init_buttons(self):
        self.create_prize_buttons()
        self.create_question_buttons()

    def create_end_prize_text(self):
        to_top = 80
        if self.bad_answer:
            self.end_prize = self.guaranteed
        else:
            self.end_prize = self.current_money

        self.end_prize_text = self.canvas.create_text(self.canvas.winfo_screenwidth() / 2,
                                                      self.canvas.winfo_screenheight() / 2 - to_top,
                                                      text=f"Wygrałeś {self.end_prize} zł!",
                                                      font='Helvetica 80 bold',
                                                      fill="white")

    def end_game(self):
        print("Game has ended")
        self.reset_phone_lifeline()
        self.root.after(2000, lambda: self.create_end_prize_text())
        self.root.after(4000, lambda: self.switch_to_menu())

    def switch_to_menu(self):
        self.canvas.destroy()
        self.game_frame.pack_forget()
        self.game_frame.destroy()
        self.menu_frame.pack()
        # self.root.after_cancel(self.audio_event)
        self.reset_channels()
        pygame.mixer.music.load("audio/menu.wav")
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    def create_question_buttons(self):
        start_button_width = 300
        start_button_height = 80
        start_button_edge = 40
        padding = 5
        answer_text_padding = 5
        to_left = 130
        left_padding = 20

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
        self.question_button_A_text = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="A",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.A_text = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="A:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')

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
                                                              fill="white",
                                                              anchor='center',
                                                              justify='center')

        self.question_button_B = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_B_text = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="B",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.B_text = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="B:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')
        y1 += (start_button_height + padding)
        y2 += (start_button_height + padding)
        y3 += (start_button_height + padding)
        y4 += (start_button_height + padding)
        self.question_button_D = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_D_text = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="D",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.D_text = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="D:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')

        x1 -= (start_button_width + padding + 2 * start_button_edge)
        x2 -= (start_button_width + padding + 2 * start_button_edge)
        x3 -= (start_button_width + padding + 2 * start_button_edge)
        x4 -= (start_button_width + padding + 2 * start_button_edge)

        self.question_button_C = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_button_C_text = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="C",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.C_text = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="C:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')
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
        actions = ["<ButtonRelease-1>", "<Enter>", "<Leave>", "<Double-Button-1>"]
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
        self.canvas.itemconfig(self.question_button_A_text, fill="white")
        self.canvas.itemconfig(self.question_button_B_text, fill="white")
        self.canvas.itemconfig(self.question_button_C_text, fill="white")
        self.canvas.itemconfig(self.question_button_D_text, fill="white")

    def reset_attributes(self):
        self.current_question = None
        self.currently_clicked = None

    def reset_phone_lifeline(self):
        self.canvas.delete(self.timer_start_button)
        self.canvas.delete(self.timer_start_button_text)
        self.canvas.delete(self.timer_stop_button)
        self.canvas.delete(self.timer_stop_button_text)
        self.canvas.delete(self.timer_text)

    def printTest(self, event):
        print("działa")

    def next_question(self, swap=False):
        if self.current_question_number < 14:
            self.reset_attributes()
            self.reset_buttons()
            self.reset_phone_lifeline()
            self.bind_buttons()
            self.update_after_answer()
            self.start_button_clicked = False
            self.answer_clicked = False
            if not swap:
                self.audio_next_question.fadeout(4000)
                self.audio_channel_1.stop()
                self.audio_channel_1 = self.audio_next_question.play()
                self.root.after(2500, lambda: self.play_background_music())
            self.load_new_question()
        else:
            print("Gratulację - wygrałeś MILION")

    def play_wrong_answer(self):
        self.audio_channel_1.stop()
        self.audio_channel_1 = self.audio_wrong_answer.play()
        self.root.after(3000, lambda: self.end_game())

    def play_right_answer(self):
        if self.current_question_number in [4, 9, 14]:
            self.audio_channel_1.stop()
            self.audio_channel_1 = self.audio_right_answer_guaranteed.play()
            self.root.after(4000, lambda: self.next_question())
        else:
            self.audio_channel_1.stop()
            self.audio_channel_1 = self.audio_right_answer.play()
            self.root.after(4000, lambda: self.next_question())

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
                self.play_right_answer()
            else:
                self.canvas.itemconfig(self.question_button_A, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.bad_answer = True
                self.play_wrong_answer()
        elif answer == "B":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#00FF00')
                self.play_right_answer()
            else:
                self.canvas.itemconfig(self.question_button_B, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.bad_answer = True
                self.play_wrong_answer()
        elif answer == "C":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#00FF00')
                self.play_right_answer()
            else:
                self.canvas.itemconfig(self.question_button_C, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.bad_answer = True
                self.play_wrong_answer()
        elif answer == "D":
            if answer == correct_answer:
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#00FF00')
                self.play_right_answer()
            else:
                self.canvas.itemconfig(self.question_button_D, outline='#080E43', fill='#FB1111')
                self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
                self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
                self.bad_answer = True
                self.play_wrong_answer()
        else:
            print(f"Odpowiedzia powinno byc A, B, C, lub D, a nie: {answer}")

    def check_answer(self, answer):
        print(f"Sprawdzam {answer}")
        self.answer_clicked = True
        if self.current_question_number in [0, 1, 2, 3]:
            self.root.after(4000, lambda: self.show_answer(answer))
        elif self.current_question_number in [5, 6, 7, 8]:
            self.root.after(4000, lambda: self.show_answer(answer))
        elif self.current_question_number in [10, 11, 12, 13]:
            self.root.after(5000, lambda: self.show_answer(answer))
        elif self.current_question_number in [4, 9, 14]:
            self.root.after(6000, lambda: self.show_answer(answer))
        else:
            print("Bledny numer pytania")

    def click_answer(self, event, answer):
        if answer == "A":
            if self.currently_clicked == "A":
                self.reset_channels()
                self.audio_channel_1 = self.audio_click_answer.play()
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
                self.reset_channels()
                self.audio_channel_1 = self.audio_click_answer.play()
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
                self.reset_channels()
                self.audio_channel_1 = self.audio_click_answer.play()
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
                self.reset_channels()
                self.audio_channel_1 = self.audio_click_answer.play()
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

        prize_values = ["0 zł", "100 zł", "200 zł", "300 zł", "500 zł", "1000 zł", "2000 zł", "5000 zł", "10 000 zł",
                        "20 000 zł", "40 000 zł", "75 000 zł", "125 000 zł", "250 000 zł", "500 000 zł",
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
            self.end_game()

    def update_prize_buttons(self):
        for i in range(len(self.prize_button_list)):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#4D5CDC')
        for i in range(self.current_question_number + 1):
            self.canvas.itemconfig(self.prize_button_list[i], outline='#080E43', fill='#00FF00')
        self.canvas.itemconfig(self.prize_button_list[self.current_question_number + 1], outline='#080E43',
                               fill='yellow')

    def load_new_question(self):
        prize = self.question_prize_list[self.current_question_number + 1]
        print(prize)
        self.current_question = self.pick_random_question(prize)
        # self.add_to_already_asked(self.current_question)
        print("New question loaded")

        self.canvas.itemconfigure(self.question_button_Q_text,
                                  text=cut_question(f"{self.current_question.question}", width=85))
        self.canvas.itemconfigure(self.question_button_A_text,
                                  text=cut_question(f"{self.current_question.answer_A}", width=38))
        self.canvas.itemconfigure(self.question_button_B_text,
                                  text=cut_question(f"{self.current_question.answer_B}", width=38))
        self.canvas.itemconfigure(self.question_button_C_text,
                                  text=cut_question(f"{self.current_question.answer_C}", width=38))
        self.canvas.itemconfigure(self.question_button_D_text,
                                  text=cut_question(f"{self.current_question.answer_D}", width=38))

        print(self.current_question.question)

    def pick_random_question(self, prize):
        result = [q for q in self.question_list if q.prize == prize]
        # print(result)
        # print(random.sample(result, 1)[0].question)
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
        elif button == "start":
            self.canvas.itemconfig(self.timer_start_button, outline='#080E43', fill='#4D5CDC')
        elif button == "stop":
            self.canvas.itemconfig(self.timer_stop_button, outline='#080E43', fill='#4D5CDC')
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
        elif button == "start":
            self.canvas.itemconfig(self.timer_start_button, outline='#4D5CDC', fill='#080E43')
        elif button == "stop":
            self.canvas.itemconfig(self.timer_stop_button, outline='#4D5CDC', fill='#080E43')
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
        pygame.mixer.init()

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

        pygame.mixer.music.load("audio/menu.wav")
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

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
