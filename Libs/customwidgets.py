import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from . import IMAGE_SUFFIXES

import logging
logger = logging.getLogger(__name__)

class Selector(tk.Toplevel):
    def __init__(self, master=None, x_entry=None, y_entry=None):
        super().__init__(master)
        self.title("Select Coordinates")
        self.geometry("1600x720")
        self.lift()
        self.x_entry = x_entry
        self.y_entry = y_entry
        self.ratio = {"X-axis": 1, "Y-axis": 1}
        self.selected_coords = {"x": 0, "y": 0}
        self.load_image_button = None
        self.select_coord_button = None
        self.coord_display_frame = None
        self.confirm_button = None
        self.left_frame = None
        self.right_frame = None
        self.image_canvas = None
        self.image_obj = None
        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self, width=1280, height=720, bg="white")
        self.left_frame.grid(row=0, column=0)

        self.right_frame = tk.Frame(self, width=120, height=720, bg="gray")
        self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ns")

        self.image_canvas = tk.Canvas(self.left_frame, width=1280, height=720, cursor="cross")
        self.image_canvas.pack()
        self.image_canvas.bind("<Button-1>", self.on_click)

        self.load_image_button = tk.Button(self.right_frame, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=5)

        self.coord_display_frame = tk.Frame(self.right_frame, width=120, height=50, bg="white")
        self.coord_display_frame.pack(pady=5)
        self.coord_label = tk.Label(self.coord_display_frame, text="Coordinates: ")
        self.coord_label.pack()

        self.confirm_button = tk.Button(self.right_frame, text="Confirm", command=self.confirm)
        self.confirm_button.pack(pady=5)

    def load_image(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("Image Files", IMAGE_SUFFIXES), ("All Files", "*.*")])
        if filename:
            image = Image.open(filename)
            ratio_x = 1280 / image.width
            ratio_y = 720 / image.height
            self.ratio = {"X-axis": ratio_x, "Y-axis": ratio_y}
            logger.debug(f"Ratio: {self.ratio}")
            image = image.resize((1280, 720), Image.ANTIALIAS)
            self.image_obj = ImageTk.PhotoImage(image)
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.image_obj)

    def on_click(self, event):
        if self.image_obj:
            logger.debug(f"Clicked at: {event.x}, {event.y}")
            x = int(event.x / self.ratio["X-axis"])
            y = int(event.y / self.ratio["Y-axis"])
            self.selected_coords = {"x": x, "y": y}
            logger.debug(f"Recorded selected coords: {self.selected_coords}")
            self.coord_label.configure(text=f"Coordinates: {self.selected_coords}")

    def confirm(self):
        if self.x_entry and self.y_entry:
            self.x_entry.delete(0, tk.END)
            self.x_entry.insert(0, self.selected_coords["x"])
            self.y_entry.delete(0, tk.END)
            self.y_entry.insert(0, self.selected_coords["y"])
        self.destroy()


# class ParamsSelector(tk.Toplevel):
#     def __init__(self, master, fish_num):
#         super().__init__(master)
#         self.master = master
#         self.fish_num = fish_num
#         self.coordinates = {f"Fish {i}": [None, None] for i in range(fish_num)}

#         self.ratio = None

#         self.LeftFrame = tk.Frame(self, width=1280, height=720)
#         self.LeftFrame.grid(row=0, column=0)

#         self.RightFrame = tk.Frame(self)
#         self.RightFrame.grid(row=0, column=1)

#         self.ImageLoad_button = tk.Button(self.RightFrame, text="Load Custom Image", command=self.load_image)
#         self.ImageLoad_button.grid(row=0, column=0)

#         self.Coord_labels_list = [tk.Button(self.RightFrame, text=f"Fish: {i}", command=lambda i=i: self.select_coord(i)) for i in range(fish_num)]
#         for i, button in enumerate(self.Coord_labels_list):
#             button.grid(row=i+1, column=0)
#             entry = tk.Entry(self.RightFrame, state='readonly')
#             entry.grid(row=i+1, column=1)

#         self.Confirm_button = tk.Button(self.RightFrame, text="Confirm", command=self.confirm)
#         self.Confirm_button.grid(row=fish_num+2, column=0)

#     def load_image(self):
#         file_path = filedialog.askopenfilename()
#         img = Image.open(file_path)
#         logger.debug(f"Image loaded, size: {img.size}")

#         img = img.resize((1280, 720), Image.ANTIALIAS)
#         self.ratio = img.size[0] / 1280, img.size[1] / 720
#         logger.debug(f"Image resized, ratio: {self.ratio}")

#         img = ImageTk.PhotoImage(img)
#         label = tk.Label(self.LeftFrame, image=img)
#         label.image = img
#         label.grid(row=0, column=0)
#         logger.debug(f"Image displayed")


#     def select_coord(self, i):
#         logger.debug(f"Selecting coord for fish {i}")
#         self.Coord_labels_list[i].config(relief=tk.SUNKEN)
#         self.LeftFrame.bind('<Button-1>', lambda event: self.get_coord(event, i))

#     def get_coord(self, event, i):
#         logger.debug(f"Got coord for fish {i}")
#         x, y = int(event.x * self.ratio[0]), int(event.y * self.ratio[1])
#         self.Coord_labels_list[i].config(relief=tk.RAISED)
#         self.RightFrame.grid_slaves(row=i+1, column=1)[0].config(state='normal')
#         self.RightFrame.grid_slaves(row=i+1, column=1)[0].delete(0, 'end')
#         self.RightFrame.grid_slaves(row=i+1, column=1)[0].insert(0, f"x = {x}, y = {y}")
#         self.RightFrame.grid_slaves(row=i+1, column=1)[0].config(state='readonly')
#         self.coordinates[f"Fish {i}"] = [x, y]

#     def confirm(self):
#         self.master.coords_dict = self.coordinates

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

class ParamsSelector(tk.Toplevel):
    def __init__(self, master=None, fish_num=1):
        super().__init__(master)
        self.geometry("1600x720")
        self.title("ParamsSelector")
        self.master = master
        self.ratio = [1, 1]
        self.entries_list = []
        self.image_obj = None




        # Split window into 2 frames
        self.LeftFrame = tk.Frame(self, width=1280, height=720)
        self.LeftFrame.grid(row=0, column=0)

        self.RightFrame = tk.Frame(self, width=320, height=720)
        self.RightFrame.grid(row=0, column=1)

        self.create_LF_widgets()
        self.create_RF_widgets(fish_num)


    def create_LF_widgets(self):
        self.image_canvas = tk.Canvas(self.LeftFrame, width=1280, height=720, cursor="cross")
        self.image_canvas.pack()

    def create_RF_widgets(self, fish_num):
        self.ImageLoad_button = tk.Button(self.RightFrame, text="Load Custom Image", command=self.load_image)
        self.ImageLoad_button.grid(row=0, column=0)

        for i in range(fish_num):
            label = tk.Label(self.RightFrame, text=f"Fish: {i}")
            label.grid(row=i+1, column=0)

            entry = tk.Entry(self.RightFrame, state='readonly')
            entry.grid(row=i+1, column=1)

            button = tk.Button(self.RightFrame, text=f"FishButton {i}", command=lambda i=i: self.activate(i))
            button.grid(row=i+1, column=2)

            self.entries_list.append([button, entry])

        self.Confirm_button = tk.Button(self.RightFrame, text="Confirm", command=self.confirm)
        self.Confirm_button.grid(row=fish_num+1, column=0)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            ratio_x = 1280 / image.width
            ratio_y = 720 / image.height
            self.ratio = [ratio_x, ratio_y]
            logger.debug(f"Ratio: {self.ratio}")
            image = image.resize((1280, 720), Image.ANTIALIAS)
            self.image_obj = ImageTk.PhotoImage(image)
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.image_obj)

        self.lift()

    def on_click(self, event, idx):
        if self.image_obj:
            logger.debug(f"Clicked at: {event.x}, {event.y}")

            recalculated_event_x = event.x * self.ratio[0]
            recalculated_event_y = event.y * self.ratio[1]
            self.entries_list[idx][1].config(state='normal')
            self.entries_list[idx][1].delete(0, 'end')
            self.entries_list[idx][1].insert(0, f"x = {recalculated_event_x}, y = {recalculated_event_y}")
            self.entries_list[idx][1].config(state='readonly')
            # change bg color of button to indicate that it has been clicked
            self.entries_list[idx][0].config(relief=tk.RAISED)
            self.image_canvas.unbind("<Button-1>")


    def activate(self, idx):
        self.entries_list[idx][0].config(relief=tk.SUNKEN)
        self.image_canvas.bind("<Button-1>", lambda event: self.on_click(event, idx))


    def confirm(self):
        fish_coords_dict = {f"Fish {i}": self.entries_list[i][1].get() for i in range(len(self.entries_list))}
        self.master.coords_dict = fish_coords_dict
        self.destroy()