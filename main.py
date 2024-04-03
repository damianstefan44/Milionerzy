import tkinter as tk
from PIL import ImageTk, Image


# ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Game:
    def __init__(self, nickname):
        self.nickname = nickname


class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.menu_image = None

    def end_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)

    def start_fullscreen(self, event):
        self.root.attributes('-fullscreen', True)

    def start_menu(self):
        self.root.title("Milionerzy")
        self.root.attributes('-fullscreen', True)
        self.root.pack_propagate(False)
        self.root.configure(background='#080E43')

        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind("<F11>", self.start_fullscreen)

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
    menu = Menu()
    menu.start_menu()
    menu.mainloop()


if __name__ == '__main__':
    main()
