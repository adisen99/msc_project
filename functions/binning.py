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
    slope, _, _, p, _ = stats.linregress(x, np.log(y))

    return slope, p


# def binned_statistic(x, y, bins):
#     xx = stats.binned_statistic(x, x, statistic="mean", bins=bins).statistic
#     xy = stats.binned_statistic(x, y, statistic=get_quant, bins=bins).statistic

#     slope, r = get_res(xx, xy)
#     return slope, r

#-----------------------------------------------------#

# Using functions

# ---------- 2d functions ------------

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

# def get_binned_alter(precip, temp, percentile_val = 0.99, bins = None, bin_nr = 12):
#     # Getting the equal frequency bins
#     if bins == None:
#         bins = equalObs(temp, bin_nr)
#     else:
#         bins = np.array(bins)

#     # group the precipitation data according to the bins of temperature data
#     binned_precip = precip.groupby_bins(temp, bins, include_lowest=True, precision=10).quantile(percentile_val, interpolation = 'midpoint')
#     # group the temperature data by temperature bins and take mean of each bin
#     mean_temp = temp.groupby_bins(temp, bins, include_lowest=True, precision=10).mean(dim="time")
#     # return them
#     return binned_precip, mean_temp

# ---------- 3d function ------------

def get_binned_3d(precip_da, t2m_da, d2m_da, bin_nr = 12):
    """
    Binning function to get a 3-d map of slope and p-values of the regression
    between 95th / 50th percentiles of precipitation and mean temperature of each bin
    ______________________
    Input:
        precip_da : precipitation data-array loaded in memory
        t2m_da : SAT data-array loaded in memory
        d2m_da : DPT data-array loaded in memory
        bin_nr : number of bins to make (does't have a signigicant difference in the slope
                does make a difference in the p-value)
    Output :
        c-c scale regression slope and p-values for 50th percentile and 95th percentile precipitation and mean temperature values
    ______________________
    """
    print("Starting the binning process ...")

    print("converting data-arrays to numpy arrays ...")
    # convert temperature data to numpy array
    t2m = t2m_da.to_numpy()
    d2m = d2m_da.to_numpy()
    precip = precip_da.to_numpy()

    xrange = len(t2m_da[0])
    yrange = len(t2m_da[0][0])

    print("Done, now initializing empty arrays ...")
    # initialising the for loop by making zeros array for t2m and d2m to mutate
    slope_t2m_95 = np.empty((xrange, yrange))
    p_t2m_95 = np.empty((xrange, yrange))
    slope_t2m_50 = np.empty((xrange, yrange))
    p_t2m_50 = np.empty((xrange, yrange))
    slope_d2m_95 = np.empty((xrange, yrange))
    p_d2m_95 = np.empty((xrange, yrange))
    slope_d2m_50 = np.empty((xrange, yrange))
    p_d2m_50 = np.empty((xrange, yrange))

    print("Starting the loop ...")

    # starting loop
    for lat in range(xrange):
        for lon in range(yrange):
            bins_t2m = equalObs(np.squeeze(t2m_da[:, lat, lon]), bin_nr)
            bins_d2m = equalObs(np.squeeze(d2m_da[:, lat, lon]), bin_nr)
            # group the precipitation data according to the bins of temperature data
            grouped_precip_t2m = precip_da.isel(lat = lat, lon = lon).groupby_bins(t2m_da.isel(lat = lat, lon = lon), bins_t2m, include_lowest=True, precision=10)
            grouped_precip_d2m = precip_da.isel(lat = lat, lon = lon).groupby_bins(d2m_da.isel(lat = lat, lon = lon), bins_d2m, include_lowest=True, precision=10)
            precip_t2m_95 = grouped_precip_t2m.quantile(0.95, interpolation='midpoint')
            precip_t2m_50 = grouped_precip_t2m.quantile(0.50, interpolation='midpoint')
            precip_d2m_95 = grouped_precip_d2m.quantile(0.95, interpolation='midpoint')
            precip_d2m_50 = grouped_precip_d2m.quantile(0.50, interpolation='midpoint')

            # group the temperature data by temperature bins and take mean of each bin
            mean_t2m = t2m_da.isel(lat = lat, lon = lon).groupby_bins(t2m_da.isel(lat = lat, lon = lon), bins_t2m, include_lowest=True, precision=10).mean(dim='time')
            mean_d2m = d2m_da.isel(lat = lat, lon = lon).groupby_bins(d2m_da.isel(lat = lat, lon = lon), bins_d2m, include_lowest=True, precision=10).mean(dim='time')

            # getting the slope and p-value
            slope_t2m_95[lat, lon], p_t2m_95[lat, lon] = get_res(mean_t2m, precip_t2m_95)
            slope_t2m_50[lat, lon], p_t2m_50[lat, lon] = get_res(mean_t2m, precip_t2m_50)
            slope_d2m_95[lat, lon], p_d2m_95[lat, lon] = get_res(mean_d2m, precip_d2m_95)
            slope_d2m_50[lat, lon], p_d2m_50[lat, lon] = get_res(mean_d2m, precip_d2m_50)

            print(f"Completed {lat+1}/{xrange} lat and {lon+1}/{yrange} lon", end="\r")

    print("Done, now writing ...")

    return slope_t2m_95, p_t2m_95, slope_d2m_95, p_d2m_95, slope_t2m_50, p_t2m_50, slope_d2m_50, p_d2m_50

    print("... Completed")
