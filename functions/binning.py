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
def get_binned(ds, percentile_val, bins = None, bin_nr = 12):
    t2m = ds.t2m
    if bins == None:
        #create histogram with equal-frequency bins
        n, bins, patches = plt.hist(t2m, equalObs(t2m, bin_nr))
        plt.show()
    else:
        bins = np.array(bins)

    binned_ds = ds.groupby_bins('t2m', bins).quantile(percentile_val, interpolation = 'midpoint')
    return binned_ds
