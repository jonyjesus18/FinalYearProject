import numpy as np
import pandas as pd
import scipy

# Load the .mat file with squeeze_me and struct_as_record options
mat_data = scipy.io.loadmat('AIRS_40KM_2022/20220125_AIRS_3DST-1_40km_grid.mat')
mat_data_info = scipy.io.whosmat('AIRS_40KM_2022/20220125_AIRS_3DST-1_40km_grid.mat')


class matlab_reader():
    def __init__(self,file):
        self.file_path = file
        self.data = scipy.io.loadmat(file)
        self.data_airs = self.data['Airs']

        # to get night values use mat_data['Airs']['NH'][x][x][x][x][1][x][x][x]
        # to get day values use   mat_data['Airs']['NH'][x][x][x][x][0][x][x][x]

        # to get tp values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][0]
        # to get bg values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][1]
        # to get A  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][2]
        # to get ha values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][3]
        # to get k  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][4]
        # to get l  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][5]
        # to get m  values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][6]
        # to get mfx values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][7]
        # to get mfy values use mat_data['Airs']['NH'][x][x][x][x][x][x][x][8]


        # new_data[0] gives the temperature matrix 501x501 for altitude at lowest level 24
        # new_data[1] gives the temperature matrix 501x501 for altitude at lowest level 30
        # new_data[2] gives the temperature matrix 501x501 for altitude at lowest level 36
        # new_data[3] gives the temperature matrix 501x501 for altitude at lowest level 42
        # new_data[4] gives the temperature matrix 501x501 for altitude at lowest level 48
        
        self.mappings = {"day" : 0,
                        "night": 1,
                        "tp" : 0,
                        "bg" : 1,
                        "a" : 2,
                        "ha" : 3,
                        "k" : 4,
                        "l" : 5,
                        "m" : 6,
                        "mfx" : 7,
                        "mfy" : 8,
                        24 : 0,
                        30 : 1,
                        36 : 2,
                        42 : 3,
                        48 : 4}
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

        print(np.shape(new_data))
        return new_data

# Example 

matlab = matlab_reader('AIRS_40KM_2022/20220125_AIRS_3DST-1_40km_grid.mat')

matlab.select(
    hemisphere= 'sh',
    data_field='bg',
    daytime='day',
    altitude=24)      
