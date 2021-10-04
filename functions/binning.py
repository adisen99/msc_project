import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import stats

# Utility function

# util function to determing the number of bins
def equalObs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x, axis= None))

def get_mids(x):
    bin_mids = []
    for i in range(0, len(x)-1):
        bin_mid = (x[i] + x[i + 1])*0.5
        bin_mids.append(bin_mid)

    return np.array(bin_mids)

def get_res(x, y):
    # if np.isnan(np.sum(y)):
    #     slope, intercept, r, p, se = stats.linregress(x, y)
    # else:
    slope, intercept, r, p, se = stats.linregress(x, y)

    return slope, intercept, r, p, se

#-----------------------------------------------------#

# Using function

# get binned data
def get_binned(ds, percentile_val = 0.99, var = "t2m", bins = None, bin_nr = 12):
    if bins == None:
        #create histogram with equal-frequency bins
        # n, bins, patches = plt.hist(ds[var], equalObs(ds[var], bin_nr))
        # plt.show()
        bins = equalObs(ds[var], bin_nr)
    else:
        bins = np.array(bins)

    binned_ds = ds.groupby_bins(ds[var], bins).quantile(percentile_val, interpolation = 'midpoint')
    return binned_ds

def get_binned_3d(ds, percentile_val = 0.99, var = "t2m", var_bin = "t2m_bins", bin_nr = 12):

    precip = ds.precipitationCal.to_numpy()
    temp = ds[var].to_numpy()

    bins = np.apply_along_axis(equalObs, 0, temp, bin_nr)
    mids = get_mids(bins)

    binned_ds = np.zeros((len(bins[0]), len(bins[0][0])))
    binned_ds_sig = np.zeros((len(bins[0]), len(bins[0][0])))

    for lat in range(len(bins[0])):
        for lon in range(len(bins[0][0])):
            y = ds.isel(lat = lat, lon = lon).groupby_bins(ds[var].isel(lat = lat, lon = lon), bins[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')

            slope, intercept, r, p, se  = get_res(mids[:, lat, lon], y.precipitationCal.to_numpy())
            binned_ds[lat, lon] = binned_ds[lat, lon] + slope
            binned_ds_sig[lat, lon] = binned_ds_sig[lat, lon] + p

    ccscale_slope = xr.DataArray(binned_ds, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_p = xr.DataArray(binned_ds_sig, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    return ccscale_slope, ccscale_p
