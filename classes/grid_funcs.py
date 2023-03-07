import numpy as np

class map_grid():
    '''
    Map_grid creates a grid object of coordinates to simply selection of geographical areas.

    '''
    def __init__(self):
        
        self.nh_lat = np.genfromtxt('Airs_nh_lat.csv', delimiter=',')
        self.nh_lon = np.genfromtxt('Airs_nh_lon.csv', delimiter=',')
        self.sh_lat = np.genfromtxt('Airs_sh_lat.csv', delimiter=',')
        self.sh_lon = np.genfromtxt('Airs_sh_lon.csv', delimiter=',')

        self.nh_stacked = np.stack((self.nh_lat, self.nh_lon), axis=2)
        self.sh_stacked = np.stack((self.sh_lat, self.sh_lon), axis=2)

    def select_area_indexer(self, min_lat,max_lat,min_lon,max_lon):
        '''
        Selects coordinates for a range of longitudes and latitudes.
        Output is an array of indeces of shape (501,501) used to filter the output from  mamatlab_reader.select()
        '''
        if max_lat < 0:
            a = self.sh_stacked
        else:
            a = self.nh_stacked
        a = np.where((a[...,0] > min_lat) & (a[...,0] < max_lat) & (a[...,1] > min_lon) & (a[...,1] < max_lon) )
        return np.transpose(a)

class dataset():
    def __init__(self,data):
        ''' Data class : holds an array of data of shape 501x501'''
        self.data = data
        self.mean = np.nanmean(data)
        self.max = np.nanmax(data)
        self.min = np.nanmin(data)
    

class data_wizard():
    '''Colletion of functions to simplify filtering and agreggating geospatial matlab data'''
    def data_filtering(self,select_area_indexer,data):
        temp_data_select = data[select_area_indexer[:,0], select_area_indexer[:,1]]
        mask = np.full((501, 501), np.nan)
        mask[select_area_indexer[:,0], select_area_indexer[:,1]] = temp_data_select
        return mask