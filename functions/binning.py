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
    slope, _, r, _, _ = stats.linregress(x, np.log(y))

    return slope, r

#-----------------------------------------------------#

# Using functions

# get binned data
def get_binned(precip_da, temp_da, percentile_val = 0.99, bins = None, bin_nr = 12):
    # Getting the equal frequency bins
    if bins == None:
        bins = equalObs(temp_da, bin_nr)
    else:
        bins = np.array(bins)

    # group the precipitation data according to the bins of temperature data
    binned_precip = precip_da.groupby_bins(temp_da, bins, include_lowest=True, precision=10).quantile(percentile_val, interpolation = 'midpoint')
    # group the temperature data by temperature bins and take mean of each bin
    mean_temp = temp_da.groupby_bins(temp_da, bins, include_lowest=True, precision=10).mean(dim="time")
    # return them
    return binned_precip, mean_temp

def get_binned_3d(precip_da, t2m_da, d2m_da, percentile_val = 0.99, bin_nr = 12):

    # convert temperature data to numpy array
    t2m = t2m_da.to_numpy()
    d2m = d2m_da.to_numpy()
    precip = precip_da.to_numpy()

    # get the equal freq. bins from the temperature data
    bins_t2m = np.apply_along_axis(equalObs, 0, t2m, bin_nr)
    bins_d2m = np.apply_along_axis(equalObs, 0, d2m, bin_nr)

    # initialising the for loop by making zeros array for t2m and d2m to mutate
    binned_ds_t2m = np.zeros((len(bins_t2m[0]), len(bins_t2m[0][0])))
    binned_ds_sig_t2m = np.zeros((len(bins_t2m[0]), len(bins_t2m[0][0])))
    binned_ds_d2m = np.zeros((len(bins_d2m[0]), len(bins_d2m[0][0])))
    binned_ds_sig_d2m = np.zeros((len(bins_d2m[0]), len(bins_d2m[0][0])))

    # starting loop
    for lat in range(len(bins_t2m[0])):
        for lon in range(len(bins_t2m[0][0])):
            # group the precipitation data according to the bins of temperature data
            precip_t2m = precip_da.isel(lat = lat, lon = lon).groupby_bins(t2m_da.isel(lat = lat, lon = lon), bins_t2m[:, lat, lon], include_lowest=True, precision=10).quantile(percentile_val, interpolation='midpoint')
            precip_d2m = precip_da.isel(lat = lat, lon = lon).groupby_bins(d2m_da.isel(lat = lat, lon = lon), bins_d2m[:, lat, lon], include_lowest=True, precision=10).quantile(percentile_val, interpolation='midpoint')

            # group the temperature data by temperature bins and take mean of each bin
            mean_t2m = t2m_da.isel(lat = lat, lon = lon).groupby_bins(t2m_da.isel(lat = lat, lon = lon), bins_t2m[:, lat, lon], include_lowest=True, precision=10).mean(dim='time')
            mean_d2m = d2m_da.isel(lat = lat, lon = lon).groupby_bins(d2m_da.isel(lat = lat, lon = lon), bins_d2m[:, lat, lon], include_lowest=True, precision=10).mean(dim='time')

            # convert to numpy_array()
            precip_t2m = precip_t2m.to_numpy()
            precip_d2m = precip_d2m.to_numpy()
            mean_t2m = mean_t2m.to_numpy()
            mean_d2m = mean_d2m.to_numpy()

            # idx_t2m = np.argwhere(np.isnan(precip_t2m))
            # idx_d2m = np.argwhere(np.isnan(precip_d2m))

            # precip_t2m = np.delete(precip_t2m, idx_t2m)
            # precip_d2m = np.delete(precip_d2m, idx_d2m)

            # mids_t2m = np.delete(mids_t2m, idx_t2m)
            # mids_d2m = np.delete(mids_d2m, idx_d2m)

            slope_t2m, r_t2m = get_res(mean_t2m, precip_t2m)
            slope_d2m, r_d2m = get_res(mean_d2m, precip_d2m)

            binned_ds_t2m[lat, lon] = binned_ds_t2m[lat, lon] + slope_t2m
            binned_ds_sig_t2m[lat, lon] = binned_ds_sig_t2m[lat, lon] + r_t2m

            binned_ds_d2m[lat, lon] = binned_ds_d2m[lat, lon] + slope_d2m
            binned_ds_sig_d2m[lat, lon] = binned_ds_sig_d2m[lat, lon] + r_d2m

    ccscale_t2m_slope = xr.DataArray(binned_ds_t2m, dims=("lat", "lon"), coords={"lat": precip_da.coords['lat'], "lon": precip_da.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_t2m_r = xr.DataArray(binned_ds_sig_t2m, dims=("lat", "lon"), coords={"lat": precip_da.coords['lat'], "lon": precip_da.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_slope = xr.DataArray(binned_ds_d2m, dims=("lat", "lon"), coords={"lat": precip_da.coords['lat'], "lon": precip_da.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_r = xr.DataArray(binned_ds_sig_d2m, dims=("lat", "lon"), coords={"lat": precip_da.coords['lat'], "lon": precip_da.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    return ccscale_t2m_slope, ccscale_t2m_r, ccscale_d2m_slope, ccscale_d2m_r
