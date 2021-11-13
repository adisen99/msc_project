import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import stats
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Preparation for the ideal C-C scaling background plots
# TODO - implement another background plot of 2*CC scaling or 1.5*CC scaling
def get_ideal_data(da, p11_inital_val, p12_initial_value, time_scale=1):
    temparr = np.sort(da)
    p11 = [p11_inital_val]
    p12 = [p12_initial_value]

    for i in range(0, len(temparr) - 1):
        # C-C scaling
        p21 = p11[i] * ((1 + time_scale*0.068)**(temparr[i + 1] - temparr[i]))
        p22 = p12[i] * ((1 + time_scale*0.068)**(temparr[i + 1] - temparr[i]))
        p11.append(p21)
        p12.append(p22)

    preciparr1 = np.array(p11)
    preciparr2 = np.array(p12)

    return temparr, preciparr1, preciparr2

# The main plot function
def plot(binned_ds, bin_var, temparr, preciparr1, preciparr2, preciparr3, preciparr4, fit = True, **kwargs):
    # get the mid points of the temperature bins
    bin_mids = []
    bin_array = binned_ds.coords[bin_var].to_numpy()

    for i in range(0, len(bin_array)):
        bin_mid = (bin_array[i].left + bin_array[i].right) * 0.5
        bin_mids.append(bin_mid)

    mids = np.array(bin_mids)

    precip = binned_ds.precipitationCal.to_numpy()

    idx = np.argwhere(np.isnan(precip))
    precip = np.delete(precip, idx)
    mids = np.delete(mids, idx)

    # Make the figure
    if fit == True:
        # get the slope and intercept of the data to be plotted
        slope, intercept, r, _, _ = stats.linregress(mids, np.log(precip))
        # start plotting
        plt.semilogy(mids, precip, **kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.plot(mids, slope*mids + intercept, color = 'k', ls = '-', alpha = 0.8, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}')
        plt.xlim(mids.min() - 0.2, mids.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)

    elif fit == False:
        slope, _, r, _, _ = stats.linregress(mids, np.log(precip))
        # start plotting
        plt.semilogy(mids, precip, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}', **kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.xlim(mids.min() - 0.2, mids.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)

# Plotting function for 3d binning plot
def plot_3d(slope_da, r_da, title, extent_list, **kwargs):
    """
    Function to plot the output of binning 3d function
    -----
    inputs are -
    slope_da : datarray containing slope
    r_da : datarray containing R^2 values for goodness of fit
    title : The title of the output plot
    extent_list : [59.9, 100.1, -0.1, 40.1]
    """
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent_list, crs=ccrs.PlateCarree())
    (10**slope_da - 1).plot.contourf(ax = ax, cbar_kwargs={"label":"C-C scale"}, **kwargs)
    x, y = np.meshgrid(slope_da.coords['lon'], slope_da.coords['lat'])
    plt.scatter(x[(np.abs(r_da.to_numpy()) > 0.65)],y[(np.abs(r_da.to_numpy()) > 0.65)], marker='o', color = 'k', s=2)
    gridliner = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.05, linestyle='--')
    # ax.coastlines(alpha=0.7)
    # ax.add_feature(cfeature.BORDERS, alpha=0.7)
    ax.add_feature(cfeature.COASTLINE, alpha=1.0)
    gridliner.top_labels = False
    gridliner.right_labels = False
    gridliner.ylines = False  # you need False
    gridliner.xlines = False  # you need False
    ax.set_title(title)
    # ax.set_xlabel('Latitude')
    # ax.set_ylabel('Longitude')
    # ax.tick_params(axis='both', labelsize=12)
