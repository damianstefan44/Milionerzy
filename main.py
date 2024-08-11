import os
import tkinter as tk
from time import time_ns
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import random
import pygame.mixer
from operator import itemgetter


QUESTION_PRIZE_LIST = [0, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 20000, 
                       40000, 75000, 125000, 250000, 500000, 1000000]
GUARANTEED_LIST = [1000, 40000, 1000000]
PRIZE_VALUES = ["0 zł", "100 zł", "200 zł", "300 zł", "500 zł", "1000 zł", "2000 zł", "5000 zł", "10 000 zł",
                        "20 000 zł", "40 000 zł", "75 000 zł", "125 000 zł", "250 000 zł", "500 000 zł",
                        "1 000 000 zł"]
TEXT_COLORS = ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 + ["white"] + ["orange"] * 4 + ["white"]
pygame.mixer.init()
AUDIO_NEXT_QUESTION = pygame.mixer.Sound("audio/next_question.wav")
AUDIO_BACKGROUND = pygame.mixer.Sound("audio/background1.wav")
AUDIO_MENU = pygame.mixer.Sound("audio/menu.wav")
AUDIO_WRONG_ANSWER = pygame.mixer.Sound("audio/wrong_answer.wav")
AUDIO_RIGHT_ANSWER = pygame.mixer.Sound("audio/right_answer.wav")
AUDIO_RIGHT_ANSWER_GUARANTEED = pygame.mixer.Sound("audio/right_answer_guaranteed.wav")
AUDIO_MILLION = pygame.mixer.Sound("audio/million.wav")
AUDIO_PHONE = pygame.mixer.Sound("audio/phone.wav")
AUDIO_END_PRIZE = pygame.mixer.Sound("audio/end_prize.wav")
AUDIO_CLICK_ANSWER = pygame.mixer.Sound("audio/click_answer.wav")
AUDIO_LIFELINE = pygame.mixer.Sound("audio/lifeline.wav")


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
    def __init__(self, menu, nickname, menu_frame, root, menu_canvas, leader_button_text1, leader_button_text2,
                 leader_button_text3,
                 leader_button_text4, leader_button_text5, leader_button_text6, leader_button_text7,
                 leader_button_text8, leader_button_text9, leader_button_text10):
        self.time_of_load = None
        self.nickname = nickname
        self.root = root
        self.menu = menu
        self.menu_frame = menu_frame
        self.menu_canvas = menu_canvas
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
        self.banned_categories = []
        self.geography_counter = 0
        self.leader_button_text1 = leader_button_text1
        self.leader_button_text2 = leader_button_text2
        self.leader_button_text3 = leader_button_text3
        self.leader_button_text4 = leader_button_text4
        self.leader_button_text5 = leader_button_text5
        self.leader_button_text6 = leader_button_text6
        self.leader_button_text7 = leader_button_text7
        self.leader_button_text8 = leader_button_text8
        self.leader_button_text9 = leader_button_text9
        self.leader_button_text10 = leader_button_text10
        self.audio_event = None
        self.audio_channel_1 = None
        self.audio_channel_2 = None
        self.question_buttons = {
            'A': {'button': None, 'button_text': None, 'text': None},
            'B': {'button': None, 'button_text': None, 'text': None},
            'C': {'button': None, 'button_text': None, 'text': None},
            'D': {'button': None, 'button_text': None, 'text': None},
            'Q': {'button': None, 'button_text': None}
        }

    def start(self):
        self.menu_frame.pack_forget()
        self.init_canvas()
        self.init_buttons()
        self.game_frame.update()
        self.game_frame.update_idletasks()
        pygame.mixer.music.stop()
        AUDIO_NEXT_QUESTION.fadeout(4000)
        self.audio_channel_1 = AUDIO_NEXT_QUESTION.play()
        self.audio_event = self.root.after(2500, lambda: self.play_background_music())

    def reset_channels(self):
        pygame.mixer.music.stop()
        if self.audio_channel_1:
            self.audio_channel_1.stop()
            print("zastopowalem 1")
        if self.audio_channel_2:
            self.audio_channel_2.stop()
            print("zastopowalem 2")

    def play_menu_music(self):
        self.reset_channels()
        self.audio_channel_2 = AUDIO_MENU.play(loops=-1, fade_ms=1000)

    def play_background_music(self):
        if self.audio_channel_2:
            self.audio_channel_2.stop()
        self.audio_channel_2 = AUDIO_BACKGROUND.play(loops=-1, fade_ms=1000)
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
                self.audio_channel_1.play(AUDIO_LIFELINE)
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
                self.audio_channel_1.play(AUDIO_LIFELINE)
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
                self.audio_channel_1.play(AUDIO_LIFELINE)
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
                self.audio_channel_1.play(AUDIO_LIFELINE)
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
                self.audio_channel_1.play(AUDIO_LIFELINE)
                self.end_game()
        else:
            print("Bad argument - lifeline - on_lifeline_hover")

    def fifty_fifty(self):
        answers = ["A", "B", "C", "D"]
        answers_text_dict = {"A": self.question_buttons['A']['button_text'], "B": self.question_buttons['B']['button_text'],
                             "C": self.question_buttons['C']['button_text'], "D": self.question_buttons['D']['button_text']}
        answers_dict = {"A": self.question_buttons['A']['button'], "B": self.question_buttons['B']['button'],
                        "C": self.question_buttons['C']['button'], "D": self.question_buttons['D']['button']}

        answers.remove(self.current_question.correct_answer)
        random_answer = random.choice(answers)
        answers.remove(random_answer)

        for answer in answers:
            self.canvas.itemconfig(answers_text_dict[answer], text="")
            self.unbind_button(answers_dict[answer])

    def swap_question(self):
        self.current_question_number = self.current_question_number - 1
        self.current_money = QUESTION_PRIZE_LIST[self.current_question_number]
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

        y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, -(40 + padding))

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
            self.audio_channel_1.play(AUDIO_PHONE)
            self.timer_time_left = 30
            self.start_button_clicked = True
            self.countdown()

    def countdown(self):
        if self.timer_time_left <= -1:
            self.canvas.after(1000, self.canvas.itemconfig(self.timer_text, text=""))
            self.audio_channel_1.stop()
            self.audio_channel_2.play(AUDIO_BACKGROUND)
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
        self.end_prize_text = self.canvas.create_text(self.canvas.winfo_screenwidth() / 2,
                                                      self.canvas.winfo_screenheight() / 2 - 80,
                                                      text=f"Wygrałeś {self.end_prize} zł!",
                                                      font='Helvetica 80 bold',
                                                      fill="white")
        self.save_result()

    def save_result(self):
        f = open("data/wyniki.txt", "a", encoding="utf-8")
        current_time = int(time_ns() / 1000000)
        f.write(f"{self.nickname}, {self.end_prize}, {current_time}\n")

    def end_game(self):
        print("Game has ended")
        if self.bad_answer:
            self.end_prize = self.guaranteed
        else:
            self.end_prize = self.current_money
        if self.end_prize != 1000:
            self.reset_channels()
            self.audio_channel_1 = AUDIO_END_PRIZE.play()
            self.reset_phone_lifeline()
            self.root.after(2000, lambda: self.create_end_prize_text())
            self.root.after(8000, lambda: self.switch_to_menu())
        else:
            self.reset_channels()
            self.audio_channel_1 = AUDIO_MILLION.play()
            self.reset_phone_lifeline()
            self.root.after(2000, lambda: self.create_end_prize_text())
            self.root.after(20000, lambda: self.switch_to_menu())

    def switch_to_menu(self):
        self.canvas.destroy()
        self.game_frame.pack_forget()
        self.game_frame.destroy()
        self.menu_frame.pack()
        # self.root.after_cancel(self.audio_event)
        self.reset_channels()
        self.menu.load_leaderboard()

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

        self.question_buttons['A']['button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons['A']['button_text'] = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="A",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.question_buttons['A']['text'] = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
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

        self.question_buttons['Q']['button'] = self.canvas.create_polygon(
            [qx1, qy1, qx2, qy2, qx3, qy3, qx4, qy4, qx5, qy5, qx6, qy6],
            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons['Q']['button_text'] = self.canvas.create_text((qx1 + qx6) / 2, qy2,
                                                              text="",
                                                              font='Helvetica 12 bold',
                                                              fill="white",
                                                              anchor='center',
                                                              justify='center')

        self.question_buttons['B']['button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons['B']['button_text'] = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="B",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.question_buttons['B']['text'] = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="B:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')

        y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, -(start_button_height + padding))
        self.question_buttons['D']['button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons['D']['button_text'] = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="D",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.question_buttons['D']['text'] = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="D:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')

        x1, x2, x3, x4 = substract_leader_padding(x1, x2, x3, x4,
                                                  (start_button_width + padding + 2 * start_button_edge))

        self.question_buttons['C']['button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons['C']['button_text'] = self.canvas.create_text((x1 + x2) / 2 - to_left + answer_text_padding,
                                                              (y1 + y2) / 2,
                                                              text="C",
                                                              font='Helvetica 10 bold',
                                                              fill="white",
                                                              anchor='w')
        self.question_buttons['C']['text'] = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding, (y1 + y2) / 2,
                                              text="C:",
                                              font='Helvetica 16 bold',
                                              fill="orange",
                                              anchor='w')
        self.bind_question_buttons()

    def bind_question_buttons(self):
        buttons = [self.question_buttons['A']['button'], self.question_buttons['A']['button_text'],
                   self.question_buttons['B']['button'], self.question_buttons['B']['button_text'],
                   self.question_buttons['C']['button'], self.question_buttons['C']['button_text'],
                   self.question_buttons['D']['button'], self.question_buttons['D']['button_text']]
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

    def unbind_all_question_buttons(self):
        buttons = [self.question_buttons['A']['button'], self.question_buttons['A']['button_text'],
                   self.question_buttons['B']['button'], self.question_buttons['B']['button_text'],
                   self.question_buttons['C']['button'], self.question_buttons['C']['button_text'],
                   self.question_buttons['D']['button'], self.question_buttons['D']['button_text']]
        actions = ["<ButtonRelease-1>", "<Enter>", "<Leave>"]
        for b in buttons:
            for a in actions:
                self.canvas.tag_unbind(b, a)

    def reset_question_buttons(self):
        self.canvas.itemconfig(self.question_buttons['A']['button'], outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_buttons['B']['button'], outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_buttons['C']['button'], outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_buttons['D']['button'], outline='#4D5CDC', fill='#080E43')
        self.canvas.itemconfig(self.question_buttons['A']['button_text'], fill="white")
        self.canvas.itemconfig(self.question_buttons['B']['button_text'], fill="white")
        self.canvas.itemconfig(self.question_buttons['C']['button_text'], fill="white")
        self.canvas.itemconfig(self.question_buttons['D']['button_text'], fill="white")

    def reset_attributes(self):
        self.current_question = None
        self.currently_clicked = None

    def reset_phone_lifeline(self):
        self.canvas.delete(self.timer_start_button)
        self.canvas.delete(self.timer_start_button_text)
        self.canvas.delete(self.timer_stop_button)
        self.canvas.delete(self.timer_stop_button_text)
        self.canvas.delete(self.timer_text)

    def next_question(self, swap=False):
        if self.current_question_number < 14:
            self.reset_attributes()
            self.reset_question_buttons()
            self.reset_phone_lifeline()
            self.bind_question_buttons()
            self.update_after_answer()
            self.start_button_clicked = False
            self.answer_clicked = False
            if not swap:
                AUDIO_NEXT_QUESTION.fadeout(4000)
                self.audio_channel_1.stop()
                self.audio_channel_1 = AUDIO_NEXT_QUESTION.play()
                self.audio_event = self.root.after(2500, lambda: self.play_background_music())
            self.load_new_question()
        else:
            print("Gratulację - wygrałeś MILION")

    def reset_audio_event(self):
        if self.audio_event is not None:
            self.root.after_cancel(self.audio_event)
            self.audio_event = None

    def play_wrong_answer(self):
        self.audio_channel_1.stop()
        self.audio_channel_1 = AUDIO_WRONG_ANSWER.play()
        self.root.after(3000, lambda: self.end_game())

    def play_right_answer(self):
        if self.current_question_number in [4, 9, 14]:
            self.audio_channel_1.stop()
            self.audio_channel_1 = AUDIO_RIGHT_ANSWER_GUARANTEED.play()
            self.root.after(5000, lambda: self.next_question())
        else:
            self.audio_channel_1.stop()
            self.audio_channel_1 = AUDIO_RIGHT_ANSWER.play()
            self.root.after(5000, lambda: self.next_question())

    def show_answer(self, answer):
        correct_answer = self.current_question.correct_answer
        button_map = {
            "A": (self.question_buttons['A']['button'], self.question_buttons['A']['button_text']),
            "B": (self.question_buttons['B']['button'], self.question_buttons['B']['button_text']),
            "C": (self.question_buttons['C']['button'], self.question_buttons['C']['button_text']),
            "D": (self.question_buttons['D']['button'], self.question_buttons['D']['button_text']),
        }

        if correct_answer not in button_map:
            print(f"Odpowiedzia powinno byc A, B, C, lub D, a nie: {correct_answer}")
            return

        correct_button, correct_button_text = button_map[correct_answer]

        if answer not in button_map:
            print(f"Odpowiedzia powinno byc A, B, C, lub D, a nie: {answer}")
            return

        selected_button, _ = button_map[answer]

        if answer == correct_answer:
            self.canvas.itemconfig(selected_button, outline='#080E43', fill='#00FF00')
            self.play_right_answer()
        else:
            self.canvas.itemconfig(selected_button, outline='#080E43', fill='#FB1111')
            self.canvas.itemconfig(correct_button, outline='#080E43', fill='#00FF00')
            self.canvas.itemconfig(correct_button_text, fill='#FFFFFF')
            self.bad_answer = True
            self.play_wrong_answer()

    def check_answer(self, answer):
        print(f"Sprawdzam {answer}")
        self.answer_clicked = True
        delay_mapping = {
            (0, 1, 2, 3): 4000,
            (5, 6, 7, 8): 4000,
            (10, 11, 12, 13): 5000,
            (4, 9, 14): 6000
        }
        # Determine the delay based on the current question number
        delay = next((delay for questions, delay in delay_mapping.items() if self.current_question_number in questions),
                     None)
        if delay is not None:
            self.root.after(delay, lambda: self.show_answer(answer))
        else:
            print("Bledny numer pytania")

    def correct_time(self):
        current_time = time_ns() / 1000000
        if current_time - self.time_of_load > 5000:
            return True
        return False

    def click_answer(self, event, answer):
        if answer not in "ABCD":
            print("Bad argument - button")
            return

        button_config = {
            "A": (self.question_buttons['A']['button'], self.question_buttons['A']['button_text']),
            "B": (self.question_buttons['B']['button'], self.question_buttons['B']['button_text']),
            "C": (self.question_buttons['C']['button'], self.question_buttons['C']['button_text']),
            "D": (self.question_buttons['D']['button'], self.question_buttons['D']['button_text']),
        }

        # Perform actions based on the answer
        if self.currently_clicked == answer:
            if self.correct_time():
                self.handle_correct_answer(answer, button_config)
        else:
            self.currently_clicked = answer
            self.update_button_states(answer, button_config)
            self.bind_hover_events(button_config, answer)

    def handle_correct_answer(self, answer, button_config):
        self.reset_audio_event()
        self.reset_channels()
        self.audio_channel_1 = AUDIO_CLICK_ANSWER.play()
        self.unbind_all_question_buttons()
        button, text = button_config[answer]
        self.canvas.itemconfig(button, outline='#080E43', fill='#F75B11')
        self.canvas.itemconfig(text, fill='#ffffff')
        self.check_answer(answer)

    def update_button_states(self, answer, button_config):
        for key, (button, text) in button_config.items():
            if key == answer:
                self.canvas.itemconfig(button, outline='#080E43', fill='#4D5CDC')
            else:
                self.canvas.itemconfig(button, outline='#4D5CDC', fill='#080E43')

    def bind_hover_events(self, button_config, answer):
        for key, (button, text) in button_config.items():
            if key != answer:
                self.canvas.tag_unbind(button, "<Enter>")
                self.canvas.tag_unbind(text, "<Enter>")
                self.canvas.tag_unbind(button, "<Leave>")
                self.canvas.tag_unbind(text, "<Leave>")
                self.canvas.tag_bind(button, "<Enter>",
                                     lambda e, param1=key: self.on_hover(e, param1))
                self.canvas.tag_bind(text, "<Enter>",
                                     lambda e, param1=key: self.on_hover(e, param1))
                self.canvas.tag_bind(button, "<Leave>",
                                     lambda e, param1=key: self.on_stop_hover(e, param1))
                self.canvas.tag_bind(text, "<Leave>",
                                     lambda e, param1=key: self.on_stop_hover(e, param1))

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

        for prize_value, text_color in zip(PRIZE_VALUES, TEXT_COLORS):
            prize_button = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                      outline='#4D5CDC', fill='#080E43', width=0)
            prize_button_text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                        text=str(prize_value),
                                                        font='Helvetica 15 bold',
                                                        fill=text_color)
            self.prize_button_list.append(prize_button)
            self.prize_button_text_list.append(prize_button_text)
            y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, 40 + padding)

    def update_after_answer(self):
        if self.current_question_number != 14:
            self.current_question_number = self.current_question_number + 1
            print(self.current_question_number)
            self.current_money = QUESTION_PRIZE_LIST[self.current_question_number]
            print(f"Masz aktualnie: {self.current_money}")
            if self.current_money in GUARANTEED_LIST:
                self.guaranteed = self.current_money
            self.update_prize_buttons()
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
        self.time_of_load = time_ns() / 1000000
        prize = QUESTION_PRIZE_LIST[self.current_question_number + 1]
        print(prize)
        self.current_question = self.pick_random_question(prize)
        print("New question loaded")
        # Update question and answers
        self.update_question_texts()
        # Ban question category
        self.ban_question_category(self.current_question.category)
        print(self.current_question.question)

    def update_question_texts(self):
        # Update the question text
        self.canvas.itemconfigure(self.question_buttons['Q']['button_text'],
                                  text=cut_question(self.current_question.question, width=85))
        # Update answer texts using a loop
        answers = [
            (self.question_buttons['A']['button_text'], self.current_question.answer_A),
            (self.question_buttons['B']['button_text'], self.current_question.answer_B),
            (self.question_buttons['C']['button_text'], self.current_question.answer_C),
            (self.question_buttons['D']['button_text'], self.current_question.answer_D)
        ]

        for text_widget, answer in answers:
            self.canvas.itemconfigure(text_widget, text=cut_question(answer, width=38))

    def ban_question_category(self, category):
        self.banned_categories.append(category)

        if category in ["kraje i kontynenty", "stolice", "wodne akweny",
                        "wyspy", "geografia", "miasta", "góry", "flagi"]:
            self.geography_counter = self.geography_counter + 1
        if self.geography_counter == 2:
            for category in ["kraje i kontynenty", "stolice", "wodne akweny",
                             "wyspy", "geografia", "miasta", "góry", "flagi"]:
                if category not in self.banned_categories:
                    self.banned_categories.append(category)

    def pick_random_question(self, prize):
        result = [q for q in self.question_list if (q.prize == prize and q.category not in self.banned_categories)]
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
        button_styles = {
            "A": (self.question_buttons['A']['button'], '#4D5CDC'),
            "B": (self.question_buttons['B']['button'], '#4D5CDC'),
            "C": (self.question_buttons['C']['button'], '#4D5CDC'),
            "D": (self.question_buttons['D']['button'], '#4D5CDC'),
            "start": (self.timer_start_button, '#4D5CDC'),
            "stop": (self.timer_stop_button, '#4D5CDC')
        }

        if button in button_styles:
            widget, fill_color = button_styles[button]
            self.canvas.itemconfig(widget, outline='#080E43', fill=fill_color)
        else:
            print("Bad argument - button")

    def on_stop_hover(self, event, button):
        button_styles = {
            "A": (self.question_buttons['A']['button'], '#080E43'),
            "B": (self.question_buttons['B']['button'], '#080E43'),
            "C": (self.question_buttons['C']['button'], '#080E43'),
            "D": (self.question_buttons['D']['button'], '#080E43'),
            "start": (self.timer_start_button, '#080E43'),
            "stop": (self.timer_stop_button, '#080E43')
        }

        if button in button_styles:
            widget, fill_color = button_styles[button]
            self.canvas.itemconfig(widget, outline='#4D5CDC', fill=fill_color)
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


def pick_top_results(num):
    data = []
    if os.path.exists("data/wyniki.txt"):
        with open("data/wyniki.txt", 'r', encoding="utf-8") as file:
            for line in file:
                print(line)
                print(line.strip().split(', '))
                nickname, end_prize, timestamp = line.strip().split(', ')
                data.append((nickname.strip(), int(end_prize.strip()), int(timestamp.strip())))
        sorted_data = sorted(data, key=itemgetter(1, 2), reverse=True)
        top_list = sorted_data[:num]
        top_list += [(None, None, None)] * (num - len(top_list))

        return top_list

    return [(None, None, None)] * 5


def substract_leader_padding(y1, y2, y3, y4, leader_padding):
    y1 -= leader_padding
    y2 -= leader_padding
    y3 -= leader_padding
    y4 -= leader_padding

    return y1, y2, y3, y4


class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.nickname = "Gość"
        self.background_image = None
        self.start_button = None
        self.start_button_text = None
        self.canvas = None
        self.menu_frame = None
        self.menu_entry = None
        self.entry = None
        self.exit = None
        self.exit_text = None
        self.save_entry = None
        self.save_entry_text = None
        self.leader_button = None
        self.leader_button_text = None
        self.leader_button1 = None
        self.leader_button_text1 = None
        self.leader_button_number1 = None
        self.leader_button2 = None
        self.leader_button_text2 = None
        self.leader_button_number2 = None
        self.leader_button3 = None
        self.leader_button_text3 = None
        self.leader_button_number3 = None
        self.leader_button4 = None
        self.leader_button_text4 = None
        self.leader_button_number4 = None
        self.leader_button5 = None
        self.leader_button_text5 = None
        self.leader_button_number5 = None
        self.leader_button6 = None
        self.leader_button_text6 = None
        self.leader_button_number6 = None
        self.leader_button7 = None
        self.leader_button_text7 = None
        self.leader_button_number7 = None
        self.leader_button8 = None
        self.leader_button_text8 = None
        self.leader_button_number8 = None
        self.leader_button9 = None
        self.leader_button_text9 = None
        self.leader_button_number9 = None
        self.leader_button10 = None
        self.leader_button_text10 = None
        self.leader_button_number10 = None


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

    def create_menu_options(self):
        button_width = 200
        button_height = 70
        button_edge = 20
        padding = 5
        leader_padding = 75
        text_padding = 130
        to_right = 100

        x1 = self.canvas.winfo_screenwidth() / 100 * 8 - button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 100 * 8 + button_width / 2
        x3 = x1 - button_edge
        x4 = x2 + button_edge
        y1 = self.canvas.winfo_screenheight() * 19 / 20 - button_height / 2 - 20
        y2 = self.canvas.winfo_screenheight() * 19 / 20 + button_height / 2 - 20
        y3 = y4 = self.canvas.winfo_screenheight() * 19 / 20 - 20

        x2 = x2 + 100
        x4 = x4 + 100

        self.exit = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                               outline='#4D5CDC', fill='#080E43', width=0)
        self.exit_text = self.canvas.create_text((x1 + x2) / 2 - text_padding + to_right, (y1 + y2) / 2,
                                                 text="EXIT",
                                                 font='Helvetica 15 bold',
                                                 fill="white",
                                                 anchor='w')

        y1 -= 9 * leader_padding
        y2 -= 9 * leader_padding
        y3 -= 9 * leader_padding
        y4 -= 9 * leader_padding

        self.save_entry = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                     outline='#4D5CDC', fill='#080E43', width=0)
        self.save_entry_text = self.canvas.create_text((x1 + x2) / 2 - text_padding + to_right, (y1 + y2) / 2,
                                                       text="ZAPISZ",
                                                       font='Helvetica 15 bold',
                                                       fill="white",
                                                       anchor='w')

        y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, leader_padding)

        self.menu_entry = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                     outline='#4D5CDC', fill='#080E43', width=0)
        self.entry = tk.Entry(self.canvas, font='Helvetica 26 bold', justify=tk.CENTER, width=15)
        self.entry.place(x=x1 + 5, y=y1 + 12)

    def create_polygons_and_text(self, x1, x2, x3, x4, y1, y2, y3, y4, text_padding, to_right, number):
        polygon = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                             outline='#4D5CDC', fill='#080E43', width=0)
        button_text = self.canvas.create_text((x1 + x2) / 2 - text_padding + to_right, (y1 + y2) / 2,
                                              text="",
                                              font='Helvetica 12 bold',
                                              fill="white",
                                              anchor='w')
        button_number = self.canvas.create_text((x1 + x2) / 2 - text_padding, (y1 + y2) / 2,
                                                text=f"{number}.",
                                                font='Helvetica 12 bold',
                                                fill="white")
        return polygon, button_text, button_number

    def create_leaderboard(self):
        button_width = 200
        button_height = 70
        button_edge = 20
        leader_padding = 75
        text_padding = 130
        to_right = 15

        # Initial coordinate calculations
        x1 = self.canvas.winfo_screenwidth() / 100 * 92 - button_width / 2
        x2 = self.canvas.winfo_screenwidth() / 100 * 92 + button_width / 2
        x3 = x1 - button_edge
        x4 = x2 + button_edge
        y1 = self.canvas.winfo_screenheight() * 19 / 20 - button_height / 2 - 20
        y2 = self.canvas.winfo_screenheight() * 19 / 20 + button_height / 2 - 20
        y3 = y4 = self.canvas.winfo_screenheight() * 19 / 20 - 20

        x1 -= 100
        x3 -= 100

        # Create leaderboard buttons and texts
        for number in range(10, 0, -1):
            polygon, button_text, button_number = self.create_polygons_and_text(
                x1, x2, x3, x4, y1, y2, y3, y4, text_padding, to_right, number
            )
            setattr(self, f'leader_button{number}', polygon)
            setattr(self, f'leader_button_text{number}', button_text)
            setattr(self, f'leader_button_number{number}', button_number)
            y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, leader_padding)

        # Create the "RANKING" button
        self.leader_button = self.canvas.create_polygon(
            [x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
            outline='#4D5CDC', fill='#080E43', width=0
        )
        self.leader_button_text = self.canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2,
            text="RANKING",
            font='Helvetica 15 bold',
            fill="white"
        )

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

        self.bind_menu_item_events(self.start_button, "start")
        self.bind_menu_item_events(self.start_button_text, "start")

        # Create other menu options
        self.create_menu_options()

        # Bind events for save entry and exit button
        self.bind_menu_item_events(self.save_entry, "save")
        self.bind_menu_item_events(self.save_entry_text, "save")
        self.bind_menu_item_events(self.exit, "exit")
        self.bind_menu_item_events(self.exit_text, "exit")

        self.menu_frame = tk.Frame(self.canvas, background="#080E43")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.menu_frame.lower()

        self.create_leaderboard()
        self.load_leaderboard()

        pygame.mixer.music.load("audio/menu.wav")
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    def bind_menu_item_events(self, item, param):
        """Bind events for a menu item, checking if item is valid first."""
        if not item:
            return

        # Bind mouse click, enter, and leave events
        events = {
            "<ButtonRelease-1>": lambda e, p=param: self.on_menu_item_click(e, p),
            "<Enter>": lambda e, p=param: self.on_menu_item_hover(e, p),
            "<Leave>": lambda e, p=param: self.on_menu_item_stop_hover(e, p),
        }

        for event, handler in events.items():
            self.canvas.tag_bind(item, event, handler)

    def mainloop(self):
        self.root.mainloop()

    def start_game(self, event):
        print("Game started")
        # Hide the menu frame
        self.menu_frame.pack_forget()
        game = Game(self, self.nickname, self.canvas, self.root, self.canvas, self.leader_button_text1,
                    self.leader_button_text2, self.leader_button_text3, self.leader_button_text4,
                    self.leader_button_text5, self.leader_button_text6, self.leader_button_text7,
                    self.leader_button_text8, self.leader_button_text9, self.leader_button_text10)
        game.read_questions()
        game.start()
        game.update_prize_buttons()
        game.load_new_question()

    def load_leaderboard(self):
        number_of_results = 10
        top_ten = pick_top_results(number_of_results)
        buttons = [self.leader_button_text1, self.leader_button_text2, self.leader_button_text3,
                   self.leader_button_text4, self.leader_button_text5, self.leader_button_text6,
                   self.leader_button_text7, self.leader_button_text8, self.leader_button_text9,
                   self.leader_button_text10]
        self.update_top_results(number_of_results, buttons, top_ten)

    def update_top_results(self, number, buttons, top_results):
        for i in range(number):
            if top_results[i][0] is not None:
                self.canvas.itemconfig(buttons[i], text=f"{top_results[i][0]} - {top_results[i][1]}")

    def on_menu_item_click(self, event, menu_item):
        if menu_item == "start":
            self.start_game(self.nickname)
        elif menu_item == "exit":
            exit(0)
        elif menu_item == "save":
            self.nickname = self.entry.get()

    def on_menu_item_hover(self, event, menu_item):
        if menu_item == "start":
            self.canvas.itemconfig(self.start_button, outline='#080E43', fill='#4D5CDC')
        elif menu_item == "exit":
            self.canvas.itemconfig(self.exit, outline='#080E43', fill='#4D5CDC')
        elif menu_item == "save":
            self.canvas.itemconfig(self.save_entry, outline='#080E43', fill='#4D5CDC')

    def on_menu_item_stop_hover(self, event, menu_item):
        if menu_item == "start":
            self.canvas.itemconfig(self.start_button, outline='#4D5CDC', fill='#080E43')
        elif menu_item == "exit":
            self.canvas.itemconfig(self.exit, outline='#4D5CDC', fill='#080E43')
        elif menu_item == "save":
            self.canvas.itemconfig(self.save_entry, outline='#4D5CDC', fill='#080E43')


def main():
    menu = Menu()
    menu.start_menu()
    menu.mainloop()


if __name__ == '__main__':
    main()
