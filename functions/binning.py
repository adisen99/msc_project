import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# Utility function

# util function to determing the number of bins
def equalObs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x, axis= None))

def get_slope(x, y):
    bin_mid = []
    for i in range(0, len(x)):
        bin_mid = (x[i].left + x[i].right)*0.5
        x.append(bin_mid)

    mids = np.array(x)

    if np.isnan(np.sum(y)):
        slope = np.nan
    else:
        slope = np.polyfit(mids, y, 1)[0]

    return slope

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

def get_binned_3d_old(ds, percentile_val = 0.99, var = "t2m", var_bin = "t2m_bins", bin_nr = 12):

    precip = ds.precipitationCal.to_numpy()
    temp = ds[var].to_numpy()

    bins = np.apply_along_axis(equalObs, 0, temp, bin_nr)

    binned_ds = np.zeros((len(bins[0]), len(bins[0][0])))

    for lat in range(len(bins[0])):
        for lon in range(len(bins[0][0])):
            y = ds.isel(lat = lat, lon = lon).groupby_bins(ds[var].isel(lat = lat, lon = lon), bins[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')

            bin_array = y.coords[var_bin].to_numpy()

            bin_mids = []

            for i in range(0, len(bin_array)):
                bin_mid = (bin_array[i].left + bin_array[i].right)*0.5
                bin_mids.append(bin_mid)

            mids = np.array(bin_mids)

            if np.isnan(np.sum(y.precipitationCal.to_numpy())):
                slope = np.nan
            else:
                slope = np.polyfit(mids, y.precipitationCal.to_numpy(), 1)[0]

            binned_ds[lat, lon] = binned_ds[lat, lon] + slope

    ccscale = xr.DataArray(binned_ds, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    return ccscale

def get_binned_3d(ds, percentile_val = 0.99, var = "t2m", var_bin = "t2m_bins", bin_nr = 12):
    # get the data arrays
    temp = ds[var].to_numpy()
    # precip = ds.precipitationCal.to_numpy()

    # get the bins and flatten them
    bins = np.apply_along_axis(equalObs, 0, temp, bin_nr)
    bins = bins.reshape(bin_nr + 1, len(bins[0] * len(bins[0][0])))

    # stack the input dataset
    stacked = ds.stack(allpoints = ("lat", "lon"))

    # loop through the dataset to get binned values and then unstack
    for point in range(len(bins[1])):
        y = stacked.isel(allpoints = point).groupby_bins(stacked[var].isel(allpoints = point), bins[:, point]).quantile(percentile_val, interpolation='midpoint')
    unstacked = y.unstack("allpoints")

    # get the slope using the bin array and precip
    bin_array = unstacked.coords[var_bin].to_numpy()
    precip = unstacked.precipitationCal.to_numpy()
    slope = np.apply_along_axis(get_slope, 0, bin_array, precip)

    # make the ccscale data array and return
    ccscale = xr.DataArray(slope, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))
    return ccscale
