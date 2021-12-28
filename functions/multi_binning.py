# NOT WORKING NOT USERFUL

# TODO return to this piece of code make it work

# Multiprocessing binning script

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import stats
from multiprocessing import Pool, freeze_support
import os
from itertools import repeat

# Utility function

# util function to determing the number of bins
def equalObs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x, axis= None))

# No longer required
# def get_mids(x):
#     bin_mids = []
#     for i in range(0, len(x)-1):
#         bin_mid = (x[i] + x[i + 1])*0.5
#         bin_mids.append(bin_mid)

#     return np.array(bin_mids)

def get_res(x, y):
    # if np.isnan(np.sum(y)):
    #     slope, intercept, r, p, se = stats.linregress(x, y)
    # else:
    slope, _, _, p, _ = stats.linregress(x, np.log(y))

    return slope, p


# def binned_statistic(x, y, bins):
#     xx = stats.binned_statistic(x, x, statistic="mean", bins=bins).statistic
#     xy = stats.binned_statistic(x, y, statistic=get_quant, bins=bins).statistic

#     slope, r = get_res(xx, xy)
#     return slope, r

#-----------------------------------------------------#

# TODO - NOTE that the this doesn't work as it maps to each element rather than a dimension
# # trying an alternate function for binning with mutliprocessing (but only for one temperature value)
def get_binned_3d(precip, temp, percentile_val=0.95, bin_nr = 12):
    # defnining inner function to get right quantile
    def get_quant(x):
        return np.quantile(x, percentile_val, axis=None, out=None, overwrite_input=False, keepdims=True)

    bins = equalObs(temp, bin_nr)
    p95 = stats.binned_statistic(temp, precip, statistic=get_quant, bins = bins).statistic
    mean_temp = stats.binned_statistic(temp, temp, statistic='mean', bins = bins).statistic

    slope, p = get_res(mean_temp, p95)

    return slope, p

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
    temp = np.random.uniform(low=280, high=320, size=(200, 161, 161))
    precip = np.random.randint(low=0, high=321, size=(200, 161, 161))

    # num_precip = len(precip[:,0,0])
    # num_temp = len(temp[:,0,0])
    print("running async loop")
    with Pool() as pool:
        slope, p = pool.starmap(get_binned_3d, zip(precip, temp, repeat(0.95), repeat(20)))
    print("done")

if __name__ == "__main__":
    freeze_support()
    main()
