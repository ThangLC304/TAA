from Libs.general import *

import logging
logger = logging.getLogger(__name__)


class NovelTankTest(Loader): # 3000 * 7

    def __init__(self, 
                 input_df, 
                 project_hyp, 
                 fish_num, 
                #  segment = -1
                 ):

        super().__init__(testtype='novel', project_hyp=project_hyp)

        total_frames = self.hyp["FRAME RATE"] * self.hyp["DURATION"]
        input_df = input_df[:total_frames]

        # if segment == -1:
        #     self.df = input_df
        # else:
        #     self.df = self.segmentate(input_df, segment)
        self.df = input_df

        self.cols = self.df.columns
        self.basic, self.units = self.BasicCalculation(self.df, fish_num)

        self.distance = self.distance_to(self.df, "CENTER", fish_num)
        self.time, self.events = self.timing(self.df, "TOP",  fish_num, "X", smaller = True)

        self.others = {}
        # self.others['distance in top'], self.others['top/bottom ratio'] = self.distance_in_top()
        self.others['distance in top'] = self.distance_in_top()
        
        infinite_ratio = 999999

        try:
            self.others['top/bottom ratio'] = self.time.duration / self.time.not_duration
        except ZeroDivisionError:
            self.others['top/bottom ratio'] = infinite_ratio

        try:
            self.others['distance top/bottom ratio'] = self.others['distance in top'] / (self.basic["total distance"] - self.others['distance in top'])
        except ZeroDivisionError:
            self.others['distance top/bottom ratio'] = infinite_ratio

        self.others['latency in frames'], self.others['latency in seconds'] = self.calculate_latency()
        self.others['entry number'] = self.events.count
        try:
            self.others['average entry'] = self.time.duration / self.events.count / self.hyp["FRAME RATE"]
        except:
            self.others['average entry'] = 0
        

    def distance_in_top(self):
        
        distance_list = self.basic['distance']
        in_top_list = self.time.list

        distance_in_top = 0

        for i in range(len(distance_list)):
            if in_top_list[i] == 1:
                distance_in_top += distance_list[i]

        return distance_in_top

    def calculate_latency(self):

        try:
            latency = int(list(self.events.dict.keys())[0][0])+1
        except IndexError:
            latency = self.time.not_duration
        if latency == 0:
            latency = 1

        return latency, latency/self.hyp["FRAME RATE"]


### DONE ###
class ShoalingTest(Loader):

    def __init__(self, input_df1, input_df2, input_df3, project_hyp, fish_num):

        super().__init__(testtype='shoaling', project_hyp=project_hyp)

        total_frames = self.hyp["FRAME RATE"] * self.hyp["DURATION"]
        input_df1 = input_df1[:total_frames]
        input_df2 = input_df2[:total_frames]
        input_df3 = input_df3[:total_frames]

        self.df = {}

        self.df[1] = input_df1
        self.df[2] = input_df2
        self.df[3] = input_df3

        self.basic = {}

        self.basic[1], self.units = self.BasicCalculation(self.df[1], fish_num)
        self.basic[2], _ = self.BasicCalculation(self.df[2], fish_num)
        self.basic[3], _ = self.BasicCalculation(self.df[3], fish_num)

        self.equalize_mode = 'head'
        self.frames = self.df_shape_check()


    def df_shape_check(self):

        ORDINAL = ['First', 'Second', 'Third']

        min_length = min(len(self.df[1]), len(self.df[2]), len(self.df[3]))
        lowest_one = ''

        for i in range(1, 4):
            if len(self.df[i]) == min_length:
                lowest_one = i
            if len(self.df[i]) > min_length:
                print(f'The {ORDINAL[i-1]} dataframe has {len(self.df[i])} rows, more than the lowest one ({ORDINAL[lowest_one-1]}).')
                if self.equalize_mode == 'head':
                    self.df[i] = trimmer(self.df[i], target_rows = min_length, mode = self.equalize_mode)
        
        return min_length    

    # distance_to_center in general.py    

    def distance_to_other(self, dfA, dfB):

        A_cols = dfA.columns
        B_cols = dfB.columns
        distance_list = []
        for i in range(len(dfA)):
            distance = dist_cal(dfA.loc[i, A_cols[0]], dfA.loc[i, A_cols[1]], dfB.loc[i, B_cols[0]], dfB.loc[i, B_cols[1]])
            distance = distance / self.hyp['CONVERSION RATE']
            distance_list.append(distance)

        return Distance(distance_list)


    def shoal_area(self):

        #Calculate the shoal area per frame
        shoal_area_list = []

        cols1 = self.df[1].columns
        cols2 = self.df[2].columns
        cols3 = self.df[3].columns

        for i in range(len(self.df[1])):
            shoal_area = calculate_area(self.df[1].loc[i, cols1[0]], self.df[1].loc[i, cols1[1]], self.df[2].loc[i, cols2[0]], self.df[2].loc[i, cols2[1]], self.df[3].loc[i, cols3[0]], self.df[3].loc[i, cols3[1]])
            shoal_area = shoal_area / self.hyp['CONVERSION RATE']**2
            shoal_area_list.append(shoal_area)

        return Area(shoal_area_list)


    def distance_filter(self, df_num):

        others = [n for n in range(1, 4) if n != df_num]
        distance_1 = self.distance_to_other(self.df[df_num], self.df[others[0]]).list # converted
        distance_2 = self.distance_to_other(self.df[df_num], self.df[others[1]]).list # converted
        nearest_distance_list = []
        furthest_distance_list = []

        for i in range(len(distance_1)):
            nearest_distance_list.append(min(distance_1[i], distance_2[i]))
            furthest_distance_list.append(max(distance_1[i], distance_2[i]))

        return Distance(nearest_distance_list), Distance(furthest_distance_list)



### DONE ###
class MirrorBitingTest(Loader):

    def __init__(self, input_df, project_hyp, fish_num):

        super().__init__(testtype='mirror', project_hyp=project_hyp)

        total_frames = self.hyp["FRAME RATE"] * self.hyp["DURATION"]
        input_df = input_df[:total_frames]

        self.df = input_df
        try:
            self.cols = self.df.columns
        except Exception as e:
            logger.error(f"input_df = {input_df}, \nself.df = {self.df}")
            raise e
        self.basic, self.units = self.BasicCalculation(self.df, fish_num)

        self.distance = self.distance_to(self.df, "MIRROR", fish_num, "Y")
        self.time, self.events = self.timing(self.df, "MIRROR ZONE", fish_num, "Y", smaller = True)

   
### DONE ###
class SocialInteractionTest(Loader):

    def __init__(self, input_df, project_hyp, fish_num):

        super().__init__(testtype='social', project_hyp=project_hyp)

        total_frames = self.hyp["FRAME RATE"] * self.hyp["DURATION"]
        input_df = input_df[:total_frames]

        self.df = input_df
        self.cols = self.df.columns
        self.basic, self.units = self.BasicCalculation(self.df, fish_num)

        self.distance = self.distance_to(self.df, "SEPARATOR", fish_num, "Y")
        self.time, self.events = self.timing(self.df, "SEPARATOR ZONE", fish_num, "Y", smaller = False)


### DONE ###
class PredatorAvoidanceTest(Loader):
    
    def __init__(self, input_df, project_hyp, fish_num):

        super().__init__(testtype='predator', project_hyp=project_hyp)
        
        total_frames = self.hyp["FRAME RATE"] * self.hyp["DURATION"]
        input_df = input_df[:total_frames]

        self.df = input_df
        self.cols = self.df.columns
        self.basic, self.units = self.BasicCalculation(self.df, fish_num)

        self.distance = self.distance_to(self.df, "SEPARATOR", fish_num, "Y")
        self.time, self.events = self.timing(self.df, "SEPARATOR ZONE", fish_num, "Y", smaller = True)
