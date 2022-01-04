# Python module used for finding precipitation estimate
# using meteorological data

## TODO do i need to do the derivative or can I directly add the omega*dq values? Ask.

import numpy as np
from scipy import integrate

# utility functions

# vert integral function (Simpson's method)
def vert_integ(x, y):
    int = integrate.simpson(y, x, even='avg')

    return int

# finite differnce methods to find derivative
def centered_diff(arr):
    arr_diff = np.empty(len(arr) - 2)

    for i in range((len(arr) - 2)):
        arr_diff[i] = arr[i+2] - arr[i]

    return arr_diff

def forward_diff(arr):
    arr_diff = np.diff(arr)
    return arr_diff

def backward_diff(arr):
    arr_diff = -(np.diff(arr[::-1])[::-1])
    return arr_diff

# ------------------------------------

def get_qs(temp, pres):
    """
    Elemental Function to determine the precipitation estimate for each value of tempreature and omega at each grid point. (func to be used in starmap multithreading)
    ------------------
    Input :
        temp : temperature value at a grid point.
        omega_da : vertical velocity value at a grid point
    Output :
        qs : qs value at that grid point
    ------------------
    """
    a1 = 611.14
    temp0 = 273.16
    a3w = 17.269
    a4w = 35.86
    a3i = 21.875
    a4i = 7.66

    # calculating saturation vapor pressure using temperature values
    if temp > temp0:
        a3 = a3w
        a4 = a4w
        es = a1 * np.exp(a3 * ((temp - temp0)/(temp - a4)))
    elif temp < temp0 - 23:
        a3 = a3i
        a4 = a4i
        es = a1 * np.exp(a3 * ((temp - temp0)/(temp - a4)))
    else:
        esw = a1 * np.exp(a3w * ((temp - temp0)/(temp - a4w)))
        esi = a1 * np.exp(a3i * ((temp - temp0)/(temp - a4i)))
        es = esi + (esw - esi)*(((temp - (temp0 - 23))/23)**2)

    # get saturation specific humidity value
    epsilon = 0.622
    qs = (epsilon * es) / (pres - ((1 - epsilon)*es))
    return qs

# TODO : complete the following functions
def calc_qs(temp, pres):
    qs = np.empty((len(pres), len(pres)))
    for i in range(len(pres)):
        qs[i] = get_qs(temp[i], pres[i])
    return qs

def cal_precip(qs, omega, pres):
    """
    Function to determine the precipitation estimate for each value of
    qs and omega at each grid point.
    ------------------
    Input :
        qs : qs array with time at 0 axis and pressure at axis
        omega : vertical velocity array with time at 0 axis and pressure at 1 axis
    Output :
        precip_est : estimated precipitation array
    ------------------
    """
    print("Starting calculation ...")

    print("converting data-arrays to numpy arrays ...")
    # convert temperature data and omega to numpy array

    zrange = len(qs[0])
    xrange = len(qs[0][0])
    yrange = len(qs[0][0][0])
    pass


## ------------------old function ------------------
# def calc(temp_da, omega_da):
#     """
#     Function to determine the precipitation estimate for each value of
#     tempreature and omega at each grid point.
#     ------------------
#     Input :
#         temp_da : temperature dataarray with time at 0 axis and pressure at axis
#         omega_da : vertical velocity dataarray with time at 0 axis and pressure at axis
#     Output :
#         precip_est : precipitation_estimate data array
#     ------------------
#     """
#     print("Starting the binning process ...")

#     print("converting data-arrays to numpy arrays ...")
#     # convert temperature data and omega to numpy array
#     temp = temp_da = temp_da.to_numpy()
#     omega = omega_da = omega_da.to_numpy()

#     zrange = len(temp[0])
#     xrange = len(temp[0][0])
#     yrange = len(temp[0][0][0])

#     print("Done, now initializing empty arrays ...")
#     # initialising the for loop by making zeros array for t2m and d2m to mutate
#     precip_est = np.empty((xrange, yrange))

#     print("Starting the loop ...")

#     # start loop
#     for lat in range(xrange):
#         for lon in range(yrange):
#             for pres in range(zrange):
#                 pass

