import os
import math
from pathlib import Path
import json
from statistics import mean
from Libs.misc import hyploader
import tkinter
from PIL import Image, ImageTk

from . import ALLOWED_DECIMALS
from Libs.constants import STATICS

import logging
logger = logging.getLogger(__name__)



def dist_cal(x1, y1, x2, y2):

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def calculate_area(x1, y1, x2, y2, x3, y3):

    area = 0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    return area


def trimmer(df, target_rows, mode):

    cut = len(df) - target_rows

    if mode == 'head':
        df = df.iloc[cut:]
    elif mode == 'tail':
        df = df.iloc[:-cut]
    else:
        raise Exception('mode must be either head or tail')
    return df

#def a function that uppercase first letter of each word in a string
def upper_first(string):
    return ' '.join([word[0].upper() + word[1:] for word in string.split()])


class Loader():
    
    def __init__(self, testtype, project_hyp):

        self.root_dir = self.GetRoot()
        self.statics = self.StaticLoader()
        self.paths = self.PathsLoader()
        self.hyp_path = self.HypPathLoader(testtype)
        if project_hyp == {}:
            self.hyp = self.DefaultHypLoader(self.hyp_path)
        else:
            self.hyp = project_hyp


    def GetRoot(self):

        return Path(__file__).parent.parent
    

    def StaticLoader(self):

        # json_path = os.path.join(self.root_dir, 'Bin', 'statics.json')
        # with open(json_path, 'r') as file:
        #     data = file.read()
        # return json.loads(data)

        return STATICS
    

    def PathsLoader(self):

        paths = {}
        for key, value in self.statics['PATHS'].items():
            paths[key] = os.path.join(self.root_dir, value)
        return paths
    

    def HypPathLoader(self, testtype):

        try:
            hyp_path = os.path.join(self.paths['BIN'], f'hyp_{testtype}.json')
        except FileNotFoundError:
            raise Exception (f'hyp_{testtype}.json file not found')

        return hyp_path


    def DefaultHypLoader(self, hyp_path):

        data = hyploader(hyp_path)

        return data
    

    def BasicCalculation(self, input_df, fish_num):

        # reset index
        input_df = input_df.reset_index(drop=True)
        
        # print('First five row:', input_df[0:5])
        # print('Last five row', input_df[-5:])
        

        calculate_top_position = True

        conversion_rate = self.hyp["CONVERSION RATE"]
        fps = self.hyp["FRAME RATE"]
        duration = self.hyp["DURATION"]
        try:
            TBS_line = self.hyp["TOP"][fish_num]
        except KeyError:
            calculate_top_position = False

        # get names of columns
        cols = input_df.columns

        # Load speed thresholds
        speed_1, speed_2 = self.statics['SPEED_1'], self.statics['SPEED_2']

        # INITIALIZE RESULT DICTIONARY
        output_dict = {}
        units = {}

        # Calculate the distance traveled ( in cm ) each frame
        # Calculate the distance from the center of the tank
        output_dict['distance'] = []  # N-1 points
        units['distance'] = 'cm'

        output_dict['locations'] = []  # N points

        for index, row in input_df.iterrows():
            x1 = input_df.loc[index, cols[0]]
            y1 = input_df.loc[index, cols[1]]

            if index >= len(input_df) -1:
                break

            x2 = input_df.loc[index+1, cols[0]]
            y2 = input_df.loc[index+1, cols[1]]
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) / conversion_rate
            output_dict['distance'].append(distance)

            if calculate_top_position:
                # Calculate the location of the fish (top or bottom)
                if x1 < TBS_line:
                    output_dict['locations'].append(1)
                else:
                    output_dict['locations'].append(0)
        # print('Key = distance, length = ', len(output_dict['distance']))
        
        # Calculate the speed ( in cm/s ) each frame
        # N-1 points
        output_dict['speed'] = [x*fps for x in output_dict['distance']]
        units['speed'] = 'cm/s'

        # Calculate the total distance (cm)
        output_dict['total distance'] = sum(output_dict['distance'])
        units['total distance'] = 'cm'

        # Calculate the average speed (cm/s)
        output_dict['average speed'] = mean(output_dict['speed'])
        units['average speed'] = 'cm/s'

        # Count the frames TARGET the speed is in the following range
        # Freezing : < speed_1
        # Swimming : >= speed_1 and < speed_2
        # Rapid movement : >= speed_2

        # Initialize the dict
        output_dict['freezing count'] = 0
        output_dict['swimming count'] = 0
        output_dict['rapid movement count'] = 0

        units['freezing count'] = 'frames'
        units['swimming count'] = 'frames'
        units['rapid movement count'] = 'frames'

        for speed in output_dict['speed']:
            if speed < speed_1:
                output_dict['freezing count'] += 1
            elif speed >= speed_1 and speed < speed_2:
                output_dict['swimming count'] += 1
            else:
                output_dict['rapid movement count'] += 1

        # Calculate the percentage of time spent in each state
        output_dict['freezing percentage'] = output_dict['freezing count'] / len(output_dict['speed']) * 100
        output_dict['swimming percentage'] = output_dict['swimming count'] / len(output_dict['speed']) * 100
        output_dict['rapid movement percentage'] = output_dict['rapid movement count'] / len(output_dict['speed']) * 100

        units['freezing percentage'] = '%'
        units['swimming percentage'] = '%'
        units['rapid movement percentage'] = '%'

        # Calculate time spent in top
        output_dict['percentage time in top'] = sum(output_dict['locations']) / duration * 100
        units['percentage time in top'] = '%'
        output_dict['percentage time in bot'] = 100 - output_dict['percentage time in top']
        units['percentage time in bot'] = '%'

        return output_dict, units
    


    def distance_to(self, df, TARGET, fish_num, axis = 'Y'):

        assert axis in ['X', 'Y'], 'axis must be X or Y'

        try:
            marks = self.hyp[TARGET]
        except KeyError:
            raise Exception(f'{TARGET} is not defined in this test type ')
        
        try:
            mark = marks[fish_num]
        except KeyError:
            raise Exception(f'{fish_num} is not defined in this test type ')
        
        if isinstance(mark, list):
            mark = mark[0]
        else:
            try:
                mark = float(mark)
            except ValueError:
                raise Exception(f'JSON DATA STRUCTURE ERROR: {mark} is not a valid')

        cols = df.columns
        col_num = 0 if axis == 'X' else 1
        distance_list = []

        for idx, row in df.iterrows():
            distance = abs(row[cols[col_num]] - mark)/self.hyp['CONVERSION RATE']
            distance_list.append(distance)

        return Distance(distance_list, mark=mark)


    def timing(self, df, TARGET, fish_num, axis = 'X', smaller = True):

        assert axis in ['X', 'Y'], 'axis must be X or Y'

        interaction = [] # N points
        interaction_events = {} # N points

        indicator = 1 if smaller else 0
        col_num = 0 if axis == 'X' else 1
        cols = df.columns

        try:
            marks = self.hyp[TARGET]
        except KeyError:
            raise Exception(f'{TARGET} is not defined in this test type ')
        
        side = None

        mark = marks[fish_num]
        # "1" : ["536.0", 0]
        
        if isinstance(mark, list):
            side = mark[1]
            # 0
            mark = mark[0]
            # "536.0"
            try:
                side = int(side)
            except ValueError:
                try:
                    side = int(round(float(side)))
                except ValueError:
                    raise Exception(f'JSON Data Structure Error: {side} is not a boolean value')
      
        try:
            mark = float(mark)
            # 536.0
        except ValueError:
            raise Exception(f'JSON DATA STRUCTURE ERROR: {mark} is not a valid')
    
        if side is not None:
            if side == 1:
                indicator = 1 - indicator

        for _, row in df.iterrows():
            coord = row[cols[col_num]]

            # Calculate the mirror biting
            if coord < mark:
                interaction.append(indicator)
            elif coord > mark:
                interaction.append(1-indicator)
            else:
                if smaller:
                    interaction.append(1-indicator)
                else:
                    interaction.append(indicator)

        def consecutive_ones(binary_list):
            result = {}
            start, end = None, None

            for i in range(len(binary_list)):
                if binary_list[i] == 1:
                    if start is None:
                        start = i
                    end = i
                elif start is not None:
                    result[(start, end)] = end - start + 1
                    start, end = None, None

            if start is not None:
                result[(start, end)] = end - start + 1

            return result

        interaction_events = consecutive_ones(interaction)

        # for i in range(len(interaction)):
        #     if i == 0:
        #         if interaction[i] == 1:
        #             start_point = i
        #         continue
        #     if interaction[i] == 1 and interaction[i-1] == 0:
        #         start_point = i
        #     elif i == len(interaction)-1:
        #         if interaction[i] == 1:
        #             end_point = i
        #             interaction_events[(start_point, end_point)] = end_point - start_point + 1
        #     elif interaction[i] == 0 and interaction[i-1] == 1:
        #         end_point = i-1
        #         interaction_events[(start_point, end_point)] = end_point - start_point + 1

        # Convert values in mirror_biting_events to seconds
        interaction_events = {k: v/self.hyp["FRAME RATE"] for k, v in interaction_events.items()}

        # print('Number of interaction events:', len(interaction_events))
        if len(df) > 0 and len(interaction_events) == 0:
            interaction_events['-1'] = '-1'

        return Time(interaction, mark = mark), Events(interaction_events, self.hyp["DURATION"], mark = mark)


class CustomDisplay():

    def __init__(self):

        pass

    def get_variables(self, magic = False):

        self_dir = [x for x in dir(self) if x not in dir(CustomDisplay)]
        if magic:
            return self_dir
        else:
            return [x for x in self_dir if not x.startswith('__')]

    def __str__(self):

        message = "Variables:\n"
        for variable in self.get_variables():
            message += f'{str(variable)}: {str(getattr(self, variable))}\n'

        return message


class Time(CustomDisplay):

    def __init__(self, time_list, mark):

        self.list = time_list  # [1, 1, 1, 0, 0, 0, 1, 0]
        self.mark = mark

        self.duration = sum(self.list)  # in frames
        # print(f'Duration: {self.duration} / {len(self.list)}')
        self.percentage = self.duration / len(self.list) * 100
        self.not_duration = len(self.list) - self.duration  # in frames
        self.not_percentage = 100 - self.percentage
        self.unit = 's'

    

class Events(CustomDisplay):

    def __init__(self, event_dict, duration, mark):

        self.dict = event_dict
        self.mark = mark

        if '-1' in event_dict.keys():
            self.count = 0
            self.longest = 0
            self.percentage = 0
            # take out this key
            self.dict.pop('-1')
        else:
            self.count = len(self.dict)
            self.longest = max(self.dict.values())
            self.percentage = self.longest / duration * 100

        self.unit = 's'



class Area(CustomDisplay):

    def __init__(self, area_list):

        self.list = area_list
        self.avg = round(mean(self.list), ALLOWED_DECIMALS)
        self.unit = 'cm^2'
    

    def __add__(self, other):

        temp_list = self.list + other.list
        return Area(temp_list, self.hyp)
    


class Distance(CustomDisplay):

    def __init__(self, distance_list, mark=None):

        self.list = distance_list
        self.mark = mark

        self.total = round(sum(self.list), ALLOWED_DECIMALS)
        self.avg = round(mean(self.list), ALLOWED_DECIMALS)
        self.unit = 'cm'


    def __add__(self, other):

        temp_list = self.list + other.list
        return Distance(temp_list, self.hyp)
    


class Speed(CustomDisplay):

    def __init__(self, speed_list):

        self.list = speed_list
        self.max = round(max(self.list), ALLOWED_DECIMALS)
        self.min = round(min(self.list), ALLOWED_DECIMALS)
        self.avg = round(mean(self.list), ALLOWED_DECIMALS)
        self.unit = 'cm/s'

    
    def __add__(self, other):

        temp_list = self.list + other.list
        return Speed(temp_list, self.hyp)
    


def calculate_distance(start_point, end_point):
    return math.sqrt((start_point[0]-end_point[0])**2 + (start_point[1]-end_point[1])**2)

class Measurer(tkinter.Toplevel):
    def __init__(self, master, save_path, **kwargs):
        super().__init__(master=master, **kwargs)

        self.MEASURED = False
        self.save_path = save_path
        self.pixel_values = {}
        self.lines = ["A", "B", "C", "D"]
        self.tooltips = {
            "A": "In FrontView part (left side), draw a line from the left inner edge to the right inner edge of the tank",
            "B": "In FrontView part (left side), draw a line from the top inner edge to the bottom inner edge of the tank",
            "C": "In TopView part (right side), draw a line, following the water surface, from the top inner edge to the bottom inner edge of the tank",
            "D": "In TopView part (right side), draw a line from the water surface to the right inner edge of the tank"
        }
        for key in self.tooltips.keys():
            self.tooltips[key] += "\nPress 'Enter' to confirm drawing\nPress 'Esc' to cancel drawing"

        self.ImageFrame = tkinter.Frame(self)
        self.Panel = tkinter.Frame(self, width=512)

        # set initial size of self.ImageFrame to 1024x768
        self.ImageFrame.config(width=1280, height=720)

        # Adjust Panel height
        if self.ImageFrame.winfo_reqheight() < 512:
            self.Panel.config(height=720)
        else:
            self.Panel.config(height=self.ImageFrame.winfo_reqheight())

        self.loadImageButton = tkinter.Button(self.ImageFrame, text="Load Image", command=self.load_image)
        self.loadImageButton.pack(expand=True)

        self.PanelTop = tkinter.Frame(self.Panel)
        self.PanelTop.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        self.PanelMiddle = tkinter.Frame(self.Panel)
        self.PanelMiddle.pack(side=tkinter.TOP, expand=True, fill=tkinter.BOTH)

        self.PanelBottom = tkinter.Frame(self.Panel)
        self.PanelBottom.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.BOTH)

        column_names = ['']
        self.names = {}
        for i in range(len(column_names)):
            self.names[0] = tkinter.Label(self.PanelTop, text=column_names[i])
            self.names[0].grid(row=0, column=i+1, padx=10, pady=10, sticky="nsew")

        self.draw_Buttons = {}
        self.pixel_values_Label = {}
        self.values_Entry = {}
        for i, line_name in enumerate(self.lines):
            self.draw_Buttons[line_name] = tkinter.Button(self.PanelTop, 
                                                          text="Draw Line " + line_name, 
                                                          command= lambda line_name=line_name: self.draw(line_name)
                                                          )
            self.draw_Buttons[line_name].grid(row=i+1, column=0, padx=10, pady=10, stick="nsew")

            self.pixel_values_Label[line_name] = tkinter.Label(self.PanelTop)
            self.pixel_values_Label[line_name].grid(row=i+1, column=1, padx=10, pady=10, stick="nsew")

            if line_name == "A":
                self.values_Entry[line_name] = tkinter.Entry(self.PanelTop)
                self.values_Entry[line_name].grid(row=i+1, column=2, padx=10, pady=10, stick="nsew")
                self.values_unit = tkinter.Label(self.PanelTop, text="cm")
                self.values_unit.grid(row=i+1, column=3, padx=10, pady=10, stick="nsew")


        self.Tip = tkinter.Label(self.PanelMiddle, text="Instructions: ")
        self.Tip.grid(row=0, column=0, padx=10, pady=10, stick="nsew")
        self.TipText = tkinter.Label(self.PanelMiddle)

        self.Button_Confirm = tkinter.Button(self.PanelBottom, text="Confirm", command=self.confirm_draw)
        self.Button_Confirm.grid(row=0, column=0, padx=10, pady=10, stick="nsew")
        self.Button_Cancel = tkinter.Button(self.PanelBottom, text="Cancel", command=self.cancel_draw)
        self.Button_Cancel.grid(row=0, column=1, padx=10, pady=10, stick="nsew")

        self.ImageFrame.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        self.Panel.pack(side=tkinter.RIGHT, expand=True, fill=tkinter.BOTH)

    def load_image(self):
        file_path = tkinter.filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            logger.debug(f"Image loaded: {file_path}")
            logger.debug(f"Image size: {image.size}")
        else:
            logger.debug("No image selected")
            return
        # Resize the image
        # ratio = min(1024 / image.width, 768 / image.height)
        # image = image.resize((int(image.width * ratio), int(image.height * ratio)), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(image)

        # remove existed image in self.canvas
        try:
            self.canvas.delete("all")
        except:
            pass

        self.canvas = tkinter.Canvas(self.ImageFrame, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)
        self.canvas.pack()

        # bring the center of the window to the center of the screen
        logger.debug("winfo_screenwidth: {}, winfo_screenheight: {}".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.geometry("+%d+%d" % (self.winfo_screenwidth() / 2 - self.winfo_width() / 2, self.winfo_screenheight() / 2 - self.winfo_height() / 2))


    def start_draw_session(self, line_name):

        # replace image in self.canvas with the original image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

        self.canvas.bind("<Button-1>", self.button1_click)
        self.canvas.bind("<B1-Motion>", self.mouse_moving)
        self.canvas.bind("<ButtonRelease-1>", self.button1_release)
        # self.canvas.bind("<Button-3>", self.confirm_line)
        self.bind("<Return>", self.confirm_line)
        self.canvas.bind("<Button-3>", self.cancel_line)
        self.bind("<Escape>", self.cancel_line)
        # bind "Shift" to draw a straight line
        self.bind("<Shift_L>", self.draw_straight_line)
    
        self.line_name = line_name

        self.pseudo_window = tkinter.Toplevel(self)
        self.pseudo_window.withdraw()

        # wait for window to close before continuing
        self.pseudo_window.wait_window()

    def draw_straight_line(self, event):
        self.canvas.delete('line')
        temp_height = abs(event.y - self.start_point_temp[1])
        temp_width = abs(event.x - self.start_point_temp[0])
        if temp_width > temp_height:
            self.canvas.create_line(self.start_point_temp[0], self.start_point_temp[1], event.x, self.start_point_temp[1], fill="yellow", width=2, tags='line')
        elif temp_width < temp_height:
            self.canvas.create_line(self.start_point_temp[0], self.start_point_temp[1], self.start_point_temp[0], event.y, fill="yellow", width=2, tags='line')
        else:
            self.canvas.create_line(self.start_point_temp[0], self.start_point_temp[1], event.x, event.y, fill="yellow", width=2, tags='line')

    def button1_click(self, event):
        self.start_point_temp = event.x, event.y

    def mouse_moving(self, event):
        self.canvas.delete('line')
        self.canvas.create_line(self.start_point_temp[0], self.start_point_temp[1], event.x, event.y, fill="yellow", width=2, tags='line')

    def button1_release(self, event):
        self.end_point_temp = event.x, event.y
        logger.debug(f"start_point_temp: {self.start_point_temp}, end_point_temp: {self.end_point_temp}")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button-1>", self.cancel_line)

    def confirm_line(self, event):
        self.pixel_values[self.line_name] = [self.start_point_temp, self.end_point_temp]
        logger.debug(f"Updated pixel_values: {self.pixel_values}")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-2>")
        self.unbind("<Escape>")
        # self.canvas.unbind("<Button-3>")
        self.unbind("<Return>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")

        self.pseudo_window.destroy()

    def cancel_line(self, event):
        self.canvas.delete('line')
        self.canvas.unbind("<Button-1>")
        self.start_point_temp = event.x, event.y
        self.canvas.bind("<Button-1>", self.button1_click)
        self.canvas.bind("<B1-Motion>", self.mouse_moving)

    def draw(self, line_name):
        # tkinter.messagebox.showinfo("Instruction", self.tooltips[line_name])
        self.TipText.config(text=self.tooltips[line_name])
        try:
            self.TipText.grid(row=0, column=1, padx=10, pady=10, stick="nsew")
        except:
            pass
        # Wait for user to draw a line on the image and press Enter
        # Save the line length in self.pixel_values

        self.start_draw_session(line_name)

        logger.info(f"Starting point: {self.pixel_values[line_name][0]}")
        logger.info(f"Ending point: {self.pixel_values[line_name][1]}")

        distance = calculate_distance(self.pixel_values[line_name][0], self.pixel_values[line_name][1])
        logger.info("Distance: {}".format(distance))

        try:
            self.pixel_values_Label[line_name].config(text=str(distance))
        except:
            pass

    def get_real_values(self):

        real_values = {}

        for line_name in self.lines:
            if line_name in self.values_Entry:
                try:
                    real_values[line_name] = float(self.values_Entry[line_name].get())
                except:
                    tkinter.messagebox.showerror("Error", "Please enter a valid number for line {}".format(line_name))
                    return False
            else:
                try:
                    real_values[line_name] = float(self.values_Entry["A"].get())
                except:
                    tkinter.messagebox.showerror("Error", "Please enter a valid number for line A")
                    return False

        return real_values

    def confirm_draw(self):

        if self.save_path == None:        
            save_path = "Bin/essential_coords.json"
        else:
            save_path = self.save_path / "essential_coords.json"

        real_values = self.get_real_values()
        if real_values == False:
            return
        
        save_values = {}
        for line_name in self.pixel_values:
            save_values[line_name] = {
                "pixel": self.pixel_values[line_name],
                "real": real_values[line_name]
            }

        try:
            with open(save_path, 'w') as f:
                json.dump(save_values, f)
            logger.debug(f"Write essential coordinates successfully at Path = {save_path}")
        except:
            logger.debug(f"Write essential coordinates NOT successfully at Path = {save_path}")

        self.MEASURED = True
        self.destroy()


    def cancel_draw(self):
        self.MEASURED = False
        self.destroy()




    



