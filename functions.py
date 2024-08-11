import os
from PIL import ImageTk, Image
from operator import itemgetter


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


def load_image(image_path):
    """Load and resize an image, then convert it to PhotoImage."""
    image = Image.open(image_path)
    resized_image = image.resize((146, 101))
    return ImageTk.PhotoImage(resized_image)


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
