import os
import tkinter as tk
from PIL import ImageTk, Image
from functions import substract_leader_padding, pick_top_results
from game import Game
import pygame.mixer


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

        self.leader_buttons = {i: {
            'button': None,
            'button_text': None,
            'button_number': None
        } for i in range(1, 11)}

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

        y1, y2, y3, y4 = substract_leader_padding(y1, y2, y3, y4, 9 * leader_padding)

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
            self.leader_buttons[number]['button'] = polygon
            self.leader_buttons[number]['button_text'] = button_text
            self.leader_buttons[number]['button_number'] = button_number
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

        image = Image.open(f"photos{os.path.sep}milionerzy2.png")
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

        pygame.mixer.music.load(f"audio{os.path.sep}menu.wav")
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
        print("Startuje grę")
        # Hide the menu frame
        self.menu_frame.pack_forget()
        game = Game(self, self.nickname, self.canvas, self.root, self.canvas)
        game.read_questions()
        game.start()
        game.update_prize_buttons()
        game.load_new_question()

    def load_leaderboard(self):
        number_of_results = 10
        top_ten = pick_top_results(number_of_results)
        buttons = [self.leader_buttons[i]['button_text'] for i in range(1, 11)]
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