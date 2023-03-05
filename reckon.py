import numpy as np
import pandas as pd
import math
from pyproj import Geod
# Original MATLAB Code
'''
[Airs.X,Airs.Y] = ndgrid(Airs.x,Airs.y);
[Airs.NH.Lat,Airs.NH.Lon] = reckon( 89.999,0,km2deg(sqrt(Airs.X.^2 + Airs.Y.^2)),atan2d(Airs.X,Airs.Y)); 
[Airs.SH.Lat,Airs.SH.Lon] = reckon(-89.999,0,km2deg(sqrt(Airs.X.^2 + Airs.Y.^2)),atan2d(Airs.X,Airs.Y)); 
'''

def km_to_deg(km, radius = 6371.0):
    """
    Convert a distance in kilometers to degrees based on the radius of a sphere.

    Args:
        km (float): Distance in kilometers.
        radius (float): Radius of the sphere in kilometers.

    Returns:
        float: Equivalent distance in degrees.
    """
    earth_radius_km = 6371.0  # mean radius of the Earth in kilometers
    angle = km / earth_radius_km  # angle subtended by the distance at the center of the Earth
    deg = math.degrees(angle * radius / earth_radius_km)
    return deg


g = Geod(ellps='clrk66')

Airs = {}
# create ndgrid using meshgrid
Airs_X, Airs_Y = np.meshgrid(airs_x, airs_y)

# calculate latitude and longitude of NH and SH
distance = km_to_deg((np.sqrt(np.square(Airs_X) + np.square(Airs_Y))))
azimuth = np.degrees(np.arctan2(Airs_X, Airs_Y))

# nh_lat, nh_lon ,_ = g.fwd(90, 0, distance, azimuth)
# sh_lat, sh_lon ,_ = g.fwd(-90, 0, distance, azimuth)

# # assign the calculated values to the dictionary
# Airs['NH'] = {'Lat': nh_lat, 'Lon': nh_lon}
# Airs['SH'] = {'Lat': sh_lat, 'Lon': sh_lon}

def reckon(distance, azimuth):
   nh_lat, nh_lon, _ = g.fwd(90, 0, distance, azimuth)  # ignore third value
   return nh_lat, nh_lon

reckon_v = np.vectorize(reckon)

result = reckon_v(distance,azimuth)
np_result = np.asarray(result)



km2deg = np.vectorize(km_to_deg)