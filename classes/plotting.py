%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(10, 8))

m = Basemap(projection='stere', resolution='c',
            width=8E6, height=8E6, 
            lat_0=-34, lat_1=-22,
            lon_0=-74,lon_1 = -22)

m.shadedrelief(scale=0.5)

m.pcolormesh(grid.sh_lon, 
             grid.sh_lat, 
             data,
             latlon=True, cmap='RdBu_r',
             shading='auto')

m.drawcoastlines(linewidth=0.5,linestyle='solid')
m.drawcountries(linewidth=0.5, linestyle='solid',color='k')
plt.clim(-2, 2)

plt.title('Temperature')
plt.colorbar(label='Temperature in (°C)')