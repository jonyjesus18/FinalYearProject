from scipy import io
import numpy as np
import pandas as pd

class matlab_reader():
    '''
    # Example 

    matlab = matlab_reader('AIRS_40KM_2022/20220125_AIRS_3DST-1_40km_grid.mat')

    temp_data = matlab.select(
        hemisphere= 'nh',
        data_field='tp',
        daytime='night',
        altitude=24)      
    '''
    def __init__(self,file):
        self.file_path = file
        self.data = io.loadmat(file)
        self.data_info = io.whosmat(file)

        self.data_airs = self.data['Airs']

        # to get night values use mat_data['Airs']['NH'][x][x][x][x][1][x][x][x]
        # to get day values use   mat_data['Airs']['NH'][x][x][x][x][0][x][x][x]

        # to get tp values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][0] tempere perturbatio
        # to get bg values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][1] backgorund temperatue tb + bg = t (use bg and tp)
        # to get A  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][2] wave amplite
        # to get ha values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][3] ignore
        # to get k  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][4] temperature same as l and m in eastward direction
        # to get l  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][5] wave length in NS tidection 1/l is the wave length in NH direction
        # to get m  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][6] vertical wave 1/m wave length in vertical dirdction
        # to get mfx values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][7]
        # to get mfy values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][8]


        # new_data[0] gives the temperature matrix 501x501 for altitude at lowest level 24
        # new_data[1] gives the temperature matrix 501x501 for altitude at lowest level 30
        # new_data[2] gives the temperature matrix 501x501 for altitude at lowest level 36
        # new_data[3] gives the temperature matrix 501x501 for altitude at lowest level 42
        # new_data[4] gives the temperature matrix 501x501 for altitude at lowest level 48


        # [0] - > 30 ,[1] -> 36 ,[2] ->  42 for 125 grid
        
        self.mappings = {"day" : 0,
                        "night": 1,
                        "a" : 0,
                        "ha" : 1,
                        "bg" : 2,
                        "k" : 3,
                        "l" : 4,
                        "m" : 5,
                        "mfx" : 6,
                        "mfy" : 7,
                        0 : 0,
                        1 : 1,
                        2 : 2,
                        3 : 3,
                        4 : 4}
    def select(self,
        hemisphere = 'NH',
        daytime = 'Night',
        data_field = 'tp',
        altitude = None):
        ''' 
        Returns a selection on the dataset filtered based on the input values
        hemisphere : selects what hemisphere to select data, North or South
        daytime : selects what time of day to collect values, Night or Day
        data_field : selects data field from tp (temperature) , bg , a , ha , k, l , m , mfx and mfy.
        '''
        
        data_ = self.data_airs[hemisphere.upper()][0][0][0][0][self.mappings[daytime.lower()]][0][0][self.mappings[data_field.lower()]]
        
        # transpose the data to have 5, 501x501 arrays, each for a different altitude level
        new_data = np.transpose(np.transpose(data_, (2, 0, 1)), (0, 2, 1)) 
        
        if altitude is not None:
            new_data = new_data[self.mappings[altitude]]

        return new_data
