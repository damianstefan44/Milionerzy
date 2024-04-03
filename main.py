import tkinter as tk
from PIL import ImageTk, Image


# ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Game:
    def __init__(self, nickname):
        self.nickname = nickname

class Menu:
    #def __init__(self):
    #    self.nickname = nickname
    def start_menu(self):
        root = tk.Tk()
        root.title("Milionerzy")
        root.attributes('-fullscreen', True)
        root.pack_propagate(False)
        root.configure(background='#080E43')

        def end_fullscreen(event):
            root.attributes('-fullscreen', False)

        def start_fullscreen(event):
            root.attributes('-fullscreen', True)


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Milionerzy")
    root.attributes('-fullscreen', True)
    root.pack_propagate(False)
    root.configure(background='#080E43')

    def start_game():
        print("Game started")

    def end_fullscreen(event):
        root.attributes('-fullscreen', False)

    def start_fullscreen(event):
        root.attributes('-fullscreen', True)

    # Bind the Escape key to exit fullscreen
    root.bind("<Escape>", end_fullscreen)
    root.bind("<F11>", start_fullscreen)

    # Create a canvas
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    print(root.winfo_screenwidth())
    print(root.winfo_screenheight())

    # image = tk.PhotoImage(file="C:/Users/rivus/PycharmProjects/Milionerzy/photos/milionerzy_studio.jpg")
    image = ImageTk.PhotoImage(
        Image.open("photos/milionerzy2.png").resize((root.winfo_screenwidth(), root.winfo_screenheight())))
    # Display the image

    # Display the image on the canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=image)

    # Draw a polygon button
    button_width = 300
    button_height = 80
    button_edge = 20
    x1 = canvas.winfo_screenwidth() / 2 - button_width / 2
    x2 = canvas.winfo_screenwidth() / 2 + button_width / 2
    x3 = x1 - button_edge
    x4 = x2 + button_edge
    y1 = canvas.winfo_screenheight() / 2 - button_height / 2
    y2 = canvas.winfo_screenheight() / 2 + button_height / 2
    y3 = y4 = canvas.winfo_screenheight() / 2

    button = canvas.create_polygon([x3, y3, x1, y1, x2, y1, x4, y4, x2, y2, x1, y2], outline='#4D5CDC', fill='#080E43',
                                   width=4)
    button_text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="START", font='Helvetica 26 bold', fill="white")

    canvas.tag_bind(button, "<Button-1>", start_game)

    # Run the main loop
    root.mainloop()

if __name__ == '__main__':
    main()

