import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import stats
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
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

def plot(binned_precip, mean_temp, temparr, preciparr1, preciparr2, preciparr3, preciparr4, fit = True, **kwargs):
    # convert data to numpy_array
    precip = binned_precip.to_numpy()
    temp = mean_temp.to_numpy()
    # Make the figure
    if fit == True:
        # get the slope and intercept of the data to be plotted
        slope, intercept, r, _, _ = stats.linregress(temp, np.log(precip))
        # start plotting
        plt.semilogy(temp, precip, **kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.plot(temp, slope*temp + intercept, color = 'k', ls = '-', alpha = 0.8, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}')
        plt.xlim(temp.min() - 0.2, temp.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)

    elif fit == False:
        slope, _, r, _, _ = stats.linregress(temp, np.log(precip))
        # start plotting
        plt.semilogy(temp, precip, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}', **kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.xlim(temp.min() - 0.2, temp.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)

# Plotting function for 3d binning plot

#### getting the file to plot for boundaries
fname = './shapefiles3/india-composite.shp'
fname_states = './shapefiles2/India_States.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(), ccrs.PlateCarree(), facecolor='none')
shape_feature_states = ShapelyFeature(Reader(fname_states).geometries(), ccrs.PlateCarree(), facecolor='none')

def plot_3d(slope_da, p_da, extent_list, title, threshold_sig=0.05, marker_size=1, freq=3, alpha_stipple=0.5, states=False, **kwargs):
    """
    Function to plot the output of binning 3d function
    -----
    inputs are -
    slope_da : datarray containing slope
    p_da : datarray containing R^2 values for goodness of fit
    title : The title of the output plot
    extent_list : [59.9, 100.1, -0.1, 40.1]
    """
    # choosing the shapefeature to add in the plot
    if states == False:
        ind_coastline = shape_feature
    else:
        ind_coastline = shape_feature_states

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent_list, crs=ccrs.PlateCarree())
    (100*(np.exp(slope_da) - 1)).plot.contourf(ax = ax, cbar_kwargs={"label":"C-C scale dP(%)/$^{o}$C$^{-1}$"}, **kwargs)
    # (100*(np.exp(slope_da) - 1)).plot.pcolormesh(ax = ax, cbar_kwargs={"label":"C-C scale"}, **kwargs)
    x, y = np.meshgrid(slope_da.coords['lon'], slope_da.coords['lat'])
    plt.scatter(x[(np.abs(p_da.to_numpy()) < threshold_sig)][::freq],y[(np.abs(p_da.to_numpy()) < threshold_sig)][::freq], marker='o', color = 'k', s=marker_size, alpha=alpha_stipple)
    gridliner = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.05, linestyle='--')
    # ax.coastlines(alpha=0.7)
    # ax.add_feature(cfeature.BORDERS, alpha=1.0, lw=0.2)
    ax.add_feature(ind_coastline, alpha=0.7, lw=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=1.0, lw=0.5)
    gridliner.top_labels = False
    gridliner.right_labels = False
    gridliner.ylines = False
    gridliner.xlines = False
    ax.set_title(title)
