import numpy as np
import util

# ---------- 2d function ------------

# get binned data
def get_binned(precip, temp, percentile_val = 0.99, bins = None, bin_nr = 12):
    # Getting the equal frequency bins
    if bins == None:
        bins = util.equal_obs(temp, bin_nr)
    else:
        bins = np.array(bins)

    # group the precipitation data according to the bins of temperature data
    binned_precip = precip.groupby_bins(temp, bins, include_lowest=True, precision=10).quantile(percentile_val, interpolation = 'midpoint')
    # group the temperature data by temperature bins and take mean of each bin
    mean_temp = temp.groupby_bins(temp, bins, include_lowest=True, precision=10).mean(dim="time")
    # return them
    return binned_precip, mean_temp

# ---------- 3d function ------------

def get_binned_3d(precip, t2m, d2m, bin_nr = 12):
    """
    Binning function to get a 3-d map of slope and p-values of the regression
    between 95th / 50th percentiles of precipitation and mean temperature of each bin
    ______________________
    Input:
        precip : precipitation data-array loaded in memory
        t2m : SAT data-array loaded in memory
        d2m : DPT data-array loaded in memory
        bin_nr : number of bins to make (does't have a signigicant difference in the slope
                does make a difference in the p-value)
    Output :
        c-c scale regression slope and p-values for 50th percentile and 95th percentile precipitation and mean temperature values
    ______________________
    """
    print("Starting the binning process ...")

    print("Initializing empty arrays ...")

    xrange = len(t2m[0])
    yrange = len(t2m[0][0])

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
            bins_t2m = util.equal_obs(np.squeeze(t2m[:, lat, lon]), bin_nr)
            bins_d2m = util.equal_obs(np.squeeze(d2m[:, lat, lon]), bin_nr)
            # group the precipitation data according to the bins of temperature data
            grouped_precip_t2m = precip.isel(lat = lat, lon = lon).groupby_bins(t2m.isel(lat = lat, lon = lon), bins_t2m, include_lowest=True, precision=10)
            grouped_precip_d2m = precip.isel(lat = lat, lon = lon).groupby_bins(d2m.isel(lat = lat, lon = lon), bins_d2m, include_lowest=True, precision=10)
            precip_t2m_95 = grouped_precip_t2m.quantile(0.95, interpolation='midpoint')
            precip_t2m_50 = grouped_precip_t2m.quantile(0.50, interpolation='midpoint')
            precip_d2m_95 = grouped_precip_d2m.quantile(0.95, interpolation='midpoint')
            precip_d2m_50 = grouped_precip_d2m.quantile(0.50, interpolation='midpoint')

            # group the temperature data by temperature bins and take mean of each bin
            mean_t2m = t2m.isel(lat = lat, lon = lon).groupby_bins(t2m.isel(lat = lat, lon = lon), bins_t2m, include_lowest=True, precision=10).mean(dim='time')
            mean_d2m = d2m.isel(lat = lat, lon = lon).groupby_bins(d2m.isel(lat = lat, lon = lon), bins_d2m, include_lowest=True, precision=10).mean(dim='time')

            # getting the slope and p-value
            slope_t2m_95[lat, lon], p_t2m_95[lat, lon] = util.get_res(mean_t2m, precip_t2m_95)
            slope_t2m_50[lat, lon], p_t2m_50[lat, lon] = util.get_res(mean_t2m, precip_t2m_50)
            slope_d2m_95[lat, lon], p_d2m_95[lat, lon] = util.get_res(mean_d2m, precip_d2m_95)
            slope_d2m_50[lat, lon], p_d2m_50[lat, lon] = util.get_res(mean_d2m, precip_d2m_50)

            print(f"Completed {lat+1}/{xrange} lat and {lon+1}/{yrange} lon", end="\r")

    print("Done, now writing ...")

    return slope_t2m_95, p_t2m_95, slope_d2m_95, p_d2m_95, slope_t2m_50, p_t2m_50, slope_d2m_50, p_d2m_50

    print("... Completed")
