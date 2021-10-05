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
    slope, _, _, p, _ = stats.linregress(x, y)

    return slope, p

def get_slope(x, y):
    # if np.isnan(np.sum(y)):
    #     slope, intercept, r, p, se = stats.linregress(x, y)
    # else:
    slope, _, _, _, _ = stats.linregress(x, y)

    return slope

def get_pval(x, y):
    # if np.isnan(np.sum(y)):
    #     slope, intercept, r, p, se = stats.linregress(x, y)
    # else:
    _, _, _, p, _ = stats.linregress(x, y)

    return p

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

def get_binned_3d(ds, percentile_val = 0.99, bin_nr = 12):

    # precip = ds.precipitationCal.to_numpy()
    t2m = ds['t2m'].to_numpy()
    d2m = ds['d2m'].to_numpy()

    bins_t2m = np.apply_along_axis(equalObs, 0, t2m, bin_nr)
    bins_d2m = np.apply_along_axis(equalObs, 0, d2m, bin_nr)
    mids_t2m = get_mids(bins_t2m)
    mids_d2m = get_mids(bins_d2m)

    binned_ds_t2m = np.zeros((len(bins_t2m[0]), len(bins_t2m[0][0])))
    binned_ds_sig_t2m = np.zeros((len(bins_t2m[0]), len(bins_t2m[0][0])))

    binned_ds_d2m = np.zeros((len(bins_d2m[0]), len(bins_d2m[0][0])))
    binned_ds_sig_d2m = np.zeros((len(bins_d2m[0]), len(bins_d2m[0][0])))

    for lat in range(len(bins_t2m[0])):
        for lon in range(len(bins_t2m[0][0])):
            y_t2m = ds.isel(lat = lat, lon = lon).groupby_bins(ds['t2m'].isel(lat = lat, lon = lon), bins_t2m[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')
            y_d2m = ds.isel(lat = lat, lon = lon).groupby_bins(ds['d2m'].isel(lat = lat, lon = lon), bins_d2m[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')

            slope_t2m, p_t2m = get_res(mids_t2m[:, lat, lon], y_t2m.precipitationCal.to_numpy())
            slope_d2m, p_d2m = get_res(mids_d2m[:, lat, lon], y_d2m.precipitationCal.to_numpy())

            binned_ds_t2m[lat, lon] = binned_ds_t2m[lat, lon] + slope_t2m
            binned_ds_sig_t2m[lat, lon] = binned_ds_sig_t2m[lat, lon] + p_t2m

            binned_ds_d2m[lat, lon] = binned_ds_d2m[lat, lon] + slope_d2m
            binned_ds_sig_d2m[lat, lon] = binned_ds_sig_d2m[lat, lon] + p_d2m

    ccscale_t2m_slope = xr.DataArray(binned_ds_t2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_t2m_p = xr.DataArray(binned_ds_sig_t2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_slope = xr.DataArray(binned_ds_d2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_p = xr.DataArray(binned_ds_sig_d2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    return ccscale_t2m_slope, ccscale_t2m_p, ccscale_d2m_slope, ccscale_d2m_p

def get_binned_3d_test(ds, percentile_val = 0.99, bin_nr = 12):

    # precip = ds.precipitationCal.to_numpy()
    t2m = ds['t2m'].to_numpy()
    d2m = ds['d2m'].to_numpy()

    bins_t2m = np.apply_along_axis(equalObs, 0, t2m, bin_nr)
    bins_d2m = np.apply_along_axis(equalObs, 0, d2m, bin_nr)
    mids_t2m = get_mids(bins_t2m)
    mids_d2m = get_mids(bins_d2m)

    binned_ds_t2m = np.zeros((bin_nr, len(bins_t2m[0]), len(bins_t2m[0][0])))
    binned_ds_d2m = np.zeros((bin_nr, len(bins_d2m[0]), len(bins_d2m[0][0])))

    for lat in range(len(bins_t2m[0])):
        for lon in range(len(bins_t2m[0][0])):
            y_t2m = ds.isel(lat = lat, lon = lon).groupby_bins(ds['t2m'].isel(lat = lat, lon = lon), bins_t2m[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')
            y_d2m = ds.isel(lat = lat, lon = lon).groupby_bins(ds['d2m'].isel(lat = lat, lon = lon), bins_d2m[:, lat, lon]).quantile(percentile_val, interpolation='midpoint')

            binned_ds_t2m[:, lat, lon] = binned_ds_t2m[:, lat, lon] + y_t2m.precipitationCal.to_numpy()
            binned_ds_d2m[:, lat, lon] = binned_ds_d2m[:, lat, lon] + y_t2m.precipitationCal.to_numpy()

    np.append(binned_ds_t2m, mids_t2m, axis = 0)
    np.append(binned_ds_d2m, mids_d2m, axis = 0)

    slope_t2m = np.squeeze(np.apply_over_axes(get_slope, binned_ds_t2m, [0,1]))
    slope_d2m = np.squeeze(np.apply_over_axes(get_slope, binned_ds_d2m, [0,1]))

    p_t2m = np.squeeze(np.apply_over_axes(get_pval, binned_ds_t2m, [0,1]))
    p_d2m = np.squeeze(np.apply_over_axes(get_pval, binned_ds_d2m, [0,1]))

    ccscale_t2m_slope = xr.DataArray(slope_t2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_t2m_p = xr.DataArray(p_t2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_slope = xr.DataArray(slope_d2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    ccscale_d2m_p = xr.DataArray(p_d2m, dims=("lat", "lon"), coords={"lat": ds.coords['lat'], "lon": ds.coords['lon']}, attrs=dict(description="C-C scale", units="degC$^{-1}$"))

    return ccscale_t2m_slope, ccscale_t2m_p, ccscale_d2m_slope, ccscale_d2m_p
