import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# Utility function

# util function to determing the number of bins
def equalObs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x))

#-----------------------------------------------------#

# Using function

# get binned data
def get_binned(ds, bins):
    t2m = ds.t2m
    # TODO - Allow the user to input the value of bins as int and make the default binning method as the only method
    if bins == None:
        #create histogram with equal-frequency bins
        n, bins, patches = plt.hist(t2m, equalObs(t2m, 12))
        plt.show()
    else:
        bins = np.array(bins)
    binned_ds = ds.groupby_bins('t2m', bins)
