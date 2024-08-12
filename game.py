import pygame.mixer
import tkinter as tk
from PIL import ImageTk, Image
import random
from time import time_ns
import pandas as pd
import numpy as np
import functions
from question import Question

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


class Game:
    def __init__(self, menu, nickname, menu_frame, root, menu_canvas):
        self.time_of_load = None
        self.nickname = nickname
        self.root = root
        self.menu = menu
        self.menu_frame = menu_frame
        self.menu_canvas = menu_canvas
        self.game_frame = None
        self.background_image = None
        self.option_menu = None
        self.lifelines = {
            'specialist': {'image': None, 'button': None},
            '50': {'image': None, 'button': None},
            'phone': {'image': None, 'button': None},
            'swap': {'image': None, 'button': None},
            'exit': {'image': None, 'button': None},
        }
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
        self.timer_text = ""
        self.timer = {
            'start_button': None,
            'stop_button': None,
            'start_button_text': "",
            'stop_button_text': ""
        }
        self.end_prize_text = None
        self.start_button_clicked = None
        self.bad_answer = False
        self.end_prize = 0
        self.answer_clicked = False
        self.banned_categories = []
        self.geography_counter = 0
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
        if self.audio_channel_2:
            self.audio_channel_2.stop()

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
        lifeline_image = functions.load_image(image_path)
        lifeline = self.canvas.create_image(x, y,
                                            anchor=tk.NW,
                                            image=lifeline_image)
        self.lifelines[object_label]['image'] = lifeline_image
        self.lifelines[object_label]['button'] = lifeline

    def init_canvas(self):
        # Initialize canvas
        self.canvas = tk.Canvas(self.root,
                                width=self.root.winfo_screenwidth(),
                                height=self.root.winfo_screenheight(),
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Load and set background image
        self.set_background_image("photos/milionerzy_studio3.png")

        # Create black rectangle
        self.create_black_rectangle(200)

        # Define lifelines and their positions
        lifelines_info = [
            {"name": "specialist", "image": "photos/lifeline_specialist_black.png", "y_offset": 50},
            {"name": "50", "image": "photos/lifeline_50_black.png",
             "y_offset": self.root.winfo_screenheight() / 6 + 50},
            {"name": "phone", "image": "photos/lifeline_phone_black.png",
             "y_offset": 2 * self.root.winfo_screenheight() / 6 + 50},
            {"name": "swap", "image": "photos/lifeline_swap_black.png",
             "y_offset": 3 * self.root.winfo_screenheight() / 6 + 50},
            {"name": "exit", "image": "photos/lifeline_exit_black.png",
             "y_offset": self.root.winfo_screenheight() - 150},
        ]

        # Create lifeline images and buttons
        for lifeline in lifelines_info:
            self.put_image_in_object(lifeline["image"], lifeline["name"], 25, lifeline["y_offset"])
            self.bind_lifeline_events(lifeline["name"])

        # Create game frame
        self.game_frame = tk.Frame(self.canvas, background="#080E43")
        self.game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def set_background_image(self, image_path):
        """Helper method to set the background image."""
        image = Image.open(image_path)
        resized_image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def bind_lifeline_events(self, lifeline_name):
        """Helper method to bind events to lifeline buttons."""
        self.canvas.tag_bind(self.lifelines[lifeline_name]['button'], "<Double-Button-1>",
                             lambda event: self.on_lifeline_click(event, lifeline_name))
        self.canvas.tag_bind(self.lifelines[lifeline_name]['button'], "<Enter>",
                             lambda event: self.on_lifeline_hover(event, lifeline_name))
        self.canvas.tag_bind(self.lifelines[lifeline_name]['button'], "<Leave>",
                             lambda event: self.on_lifeline_stop_hover(event, lifeline_name))

    def update_lifeline_image(self, lifeline, color):
        """Helper method to update lifeline image based on hover state."""
        image_path = f"photos/lifeline_{lifeline}_{color}.png"
        lifeline_image = functions.load_image(image_path)
        self.canvas.itemconfig(self.lifelines[lifeline]['button'], image=lifeline_image)
        self.lifelines[lifeline]['image'] = lifeline_image

    def on_lifeline_hover(self, event, lifeline):
        if lifeline in self.lifelines:
            self.update_lifeline_image(lifeline, "blue")
        else:
            print(f"Bad argument - lifeline - on_lifeline_hover: {lifeline}")

    def on_lifeline_stop_hover(self, event, lifeline):
        if lifeline in self.lifelines:
            self.update_lifeline_image(lifeline, "black")
        else:
            print(f"Bad argument - lifeline - on_lifeline_stop_hover: {lifeline}")

    def update_lifeline(self, lifeline_key, lifeline_image):
        """Update the lifeline button and image."""
        self.canvas.itemconfig(self.lifelines[lifeline_key]['button'], image=lifeline_image)
        self.lifelines[lifeline_key]['image'] = lifeline_image
        self.unbind_button(self.lifelines[lifeline_key]['button'])

    def handle_lifeline_action(self, lifeline):
        """Perform actions based on the lifeline type."""
        actions = {
            "specialist": self.phone_a_friend,
            "50": self.fifty_fifty,
            "phone": self.phone_a_friend,
            "swap": self.swap_question,
            "exit": self.end_game
        }
        action = actions.get(lifeline)
        if action:
            self.audio_channel_1.stop()
            self.audio_channel_1.play(AUDIO_LIFELINE)
            action()
        else:
            print(f"Bad argument - lifeline - on_lifeline_click")

    def on_lifeline_click(self, event, lifeline):
        if not self.answer_clicked and not self.start_button_clicked:
            image_path = f"photos/lifeline_{lifeline}_red.png"
            lifeline_image = functions.load_image(image_path)
            if lifeline in self.lifelines:
                self.update_lifeline(lifeline, lifeline_image)
                self.handle_lifeline_action(lifeline)
            else:
                print("Bad argument - lifeline - on_lifeline_click")

    def fifty_fifty(self):
        answers = ["A", "B", "C", "D"]
        answers_text_dict = {"A": self.question_buttons['A']['button_text'],
                             "B": self.question_buttons['B']['button_text'],
                             "C": self.question_buttons['C']['button_text'],
                             "D": self.question_buttons['D']['button_text']}
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

        self.timer['start_button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                                outline='#4D5CDC', fill='#080E43', width=0)
        self.timer['start_button_text'] = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                                  text="START",
                                                                  font='Helvetica 15 bold',
                                                                  fill="white")

        y1, y2, y3, y4 = functions.substract_leader_padding(y1, y2, y3, y4, -(40 + padding))

        self.timer['stop_button'] = self.canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
                                                               outline='#4D5CDC', fill='#080E43', width=0)
        self.timer['stop_button_text'] = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                                                 text="STOP",
                                                                 font='Helvetica 15 bold',
                                                                 fill="white")

        self.timer_text = self.canvas.create_text(self.canvas.winfo_screenwidth() / 2,
                                                  self.canvas.winfo_screenheight() / 2 - to_top,
                                                  text="",
                                                  font='Helvetica 80 bold',
                                                  fill="white")
        for (button, param) in [('start_button', "start",), ('start_button_text', "start"),
                                ('stop_button', "stop"), ('stop_button_text', "stop")]:
            self.canvas.tag_bind(self.timer[button], "<Enter>",
                                 lambda e, param1=param: self.on_hover(e, param1))
            self.canvas.tag_bind(self.timer[button], "<Leave>",
                                 lambda e, param1=param: self.on_stop_hover(e, param1))
            if param == "start":
                self.canvas.tag_bind(self.timer[button], "<Double-Button-1>", self.start_timer)
            elif param == "stop":
                self.canvas.tag_bind(self.timer[button], "<Double-Button-1>", self.stop_timer)

    def bind_button_events(self, button_key, text_key, action):
        """Bind events to a button and its associated text."""
        self.canvas.tag_bind(self.timer[button_key], "<Enter>",
                             lambda e, param1=button_key: self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer[button_key], "<Leave>",
                             lambda e, param1=button_key: self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer[button_key], "<Double-Button-1>", action)

        self.canvas.tag_bind(self.timer[text_key], "<Enter>",
                             lambda e, param1=button_key: self.on_hover(e, param1))
        self.canvas.tag_bind(self.timer[text_key], "<Leave>",
                             lambda e, param1=button_key: self.on_stop_hover(e, param1))
        self.canvas.tag_bind(self.timer[text_key], "<Double-Button-1>", action)

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

    def create_question_button(self, name, x1, x2, x3, x4, y1, y2, y3, y4, to_left, answer_text_padding, left_padding):
        self.question_buttons[name]['button'] = self.canvas.create_polygon(
            [x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2],
            outline='#4D5CDC', fill='#080E43', width=0)
        self.question_buttons[name]['button_text'] = self.canvas.create_text(
            (x1 + x2) / 2 - to_left + answer_text_padding,
            (y1 + y2) / 2,
            text="A",
            font='Helvetica 10 bold',
            fill="white",
            anchor='w')
        self.question_buttons[name]['text'] = self.canvas.create_text((x1 + x2) / 2 - to_left - left_padding,
                                                                     (y1 + y2) / 2,
                                                                     text=f"{name}:",
                                                                     font='Helvetica 16 bold',
                                                                     fill="orange",
                                                                     anchor='w')

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

        self.create_question_button('A', x1, x2, x3, x4, y1, y2, y3, y4, to_left, answer_text_padding, left_padding)

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

        self.create_question_button('B', x1, x2, x3, x4, y1, y2, y3, y4, to_left, answer_text_padding, left_padding)
        y1, y2, y3, y4 = functions.substract_leader_padding(y1, y2, y3, y4, -(start_button_height + padding))
        self.create_question_button('D', x1, x2, x3, x4, y1, y2, y3, y4, to_left, answer_text_padding, left_padding)
        x1, x2, x3, x4 = functions.substract_leader_padding(x1, x2, x3, x4,
                                                            (start_button_width + padding + 2 * start_button_edge))
        self.create_question_button('C', x1, x2, x3, x4, y1, y2, y3, y4, to_left, answer_text_padding, left_padding)
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
        for key in "ABCD":
            self.canvas.itemconfig(self.question_buttons[key]['button'], outline='#4D5CDC', fill='#080E43')
            self.canvas.itemconfig(self.question_buttons[key]['button_text'], fill="white")

    def reset_attributes(self):
        self.current_question = None
        self.currently_clicked = None

    def reset_phone_lifeline(self):
        for key in ['start_button', 'start_button_text', 'stop_button', 'stop_button_text']:
            self.canvas.delete(self.timer[key])
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
            y1, y2, y3, y4 = functions.substract_leader_padding(y1, y2, y3, y4, 40 + padding)

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
        self.add_to_already_asked(self.current_question)
        # Ban question category
        self.ban_question_category(self.current_question.category)
        print(self.current_question.question)

    def update_question_texts(self):
        # Update the question text
        self.canvas.itemconfigure(self.question_buttons['Q']['button_text'],
                                  text=functions.cut_question(self.current_question.question, width=85))
        # Update answer texts using a loop
        answers = [
            (self.question_buttons['A']['button_text'], self.current_question.answer_A),
            (self.question_buttons['B']['button_text'], self.current_question.answer_B),
            (self.question_buttons['C']['button_text'], self.current_question.answer_C),
            (self.question_buttons['D']['button_text'], self.current_question.answer_D)
        ]

        for text_widget, answer in answers:
            self.canvas.itemconfigure(text_widget, text=functions.cut_question(answer, width=38))

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
            "start": (self.timer['start_button'], '#4D5CDC'),
            "stop": (self.timer['stop_button'], '#4D5CDC')
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
            "start": (self.timer['start_button'], '#080E43'),
            "stop": (self.timer['stop_button'], '#080E43')
        }

        if button in button_styles:
            widget, fill_color = button_styles[button]
            self.canvas.itemconfig(widget, outline='#4D5CDC', fill=fill_color)
        else:
            print("Bad argument - button")
