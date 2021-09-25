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

def get_binned_3d(ds, min = 1, percentile_val = 0.99, var = "t2m", var_bin = "t2m_bins", bin_nr = 12):

    precip = ds.precipitationCal
    temp = ds[var]

    precip = xr.where(precip < min, np.nan, precip)
    temp = temp.where(precip != np.nan)
    
    ds_comb = xr.merge([precip, temp]).chunk(dict(time=-1))

    precip = ds_comb.precipitationCal.to_numpy()
    temp = ds_comb[var].to_numpy()

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
