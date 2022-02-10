# Trying it for calculation of qs at each grid point and pressure level
## test implementation

# TODO return to this piece of code make it work

# Multiprocessing calc test script

import numpy as np
import matplotlib.pyplot as plt
from numpy import matlib
import xarray as xr
from scipy import stats
from multiprocessing import Pool, freeze_support
import os
from itertools import repeat

def calc_qs(temp, pres):
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

def main():
    # print("Importing data ...")
    # # importing and preprocessing data
    # ds_comb = xr.open_dataset('../data/combined/ds_comb.nc')
    # print("done ...")

    # print("Getting mosoon data ...")
    # mon = [6,7,8,9]
    # ds_comb_mon = xr.concat([list(ds_comb.groupby('time.month'))[i-1][1] for i in mon], dim='time')
    # print("done ...")

    # precip = ds_comb_mon.precipCal
    # temp = ds_comb_mon.t2m

    # print("Getting daily precipitation rate ...")
    # precip_daily_rate = precip[::-1].rolling(time=24).sum()[::-1]

    # print("subsetting data using daily rate ...")
    # precip = xr.where(precip_daily_rate > 1, precip, np.nan).chunk(dict(time=-1, lat=40, lon=40))
    # precip = precip.where(precip > 0).chunk(dict(time=-1, lat=40, lon=40))
    # # precip = xr.where(precip > 0.1, precip, np.nan).chunk(dict(time=-1, lat=40, lon=40))
    # temp = temp.where(precip != np.nan).chunk(dict(time=-1, lat=40, lon=40))
    # print("done ...")

    np.random.seed(42)

    # main loop
    temp = np.random.uniform(low=240, high=320, size=(100, 20, 161, 161))
    pres_interim = matlib.repmat(np.linspace(1000, 50, 20), 161, 161*100)
    pres = np.transpose(np.reshape(pres_interim, (161,161,20, 100)), (3,2,0,1))

    print("running async loop")
    with Pool() as pool:
        qs = np.reshape(np.concatenate(pool.starmap(calc_qs, zip(temp, pres))), (100, 20, 161, 161))

    print(qs)

if __name__ == "__main__":
    freeze_support()
    main()

# ## TEST code not for use
# np.random.seed(42)

# def func(a, b):
#     return a + b

# def main():
#     a_args = np.random.randint(low=1, high=10, size=(2, 2, 4, 4))
#     second_arg = np.random.randint(low=11, high=20, size=(2, 2, 4, 4))
#     with Pool() as pool:
#         M = np.reshape(np.concatenate(pool.starmap(func, zip(a_args, second_arg))),(2, 2, 4, 4))

# if __name__=="__main__":
#     freeze_support()
#     main()
