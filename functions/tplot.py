import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature

#### getting the file to plot for boundaries
fname = './shapefiles3/india-composite.shp'
fname_states = './shapefiles2/India_States.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(), ccrs.PlateCarree(), facecolor='none')
shape_feature_states = ShapelyFeature(Reader(fname_states).geometries(), ccrs.PlateCarree(), facecolor='none')

# main plotting function
def plot(slope_da, p_da, extent_list, title, threshold_sig=0.05, marker_size=1, freq=3, plot_type='slope', states=False, alpha_stipple=0.5, **kwargs):
    """"
    Function to plot the trends
    --------
    Inputs:
        slope_da : dataarray containing slope
        p_da : dataarray containing p-values
        title : The title of the output plot
        extent_list : e.g., [59.9, 100.1, -0.1, 40.1]
    Returns:
        Plot of the Sen's slope with significance stippling
    """
    # choosing the feature to add in the plot
    if states == False:
        ind_coastline = shape_feature
    else:
        ind_coastline = shape_feature_states

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent_list, crs=ccrs.PlateCarree())
    if plot_type == 'slope':
        slope_da.plot.contourf(ax = ax, cbar_kwargs={"label":"Theil-Sen slope"}, **kwargs)
    elif plot_type == 'tau':
        slope_da.plot.contourf(ax = ax, cbar_kwargs={"label":"Kendall Tau"}, **kwargs)
    else:
        print("Wrong value of plot_type")

    x, y = np.meshgrid(slope_da.coords['lon'], slope_da.coords['lat'])
    plt.scatter(x[(np.abs(p_da.to_numpy()) < threshold_sig)][::freq], y[(np.abs(p_da.to_numpy()) < threshold_sig)][::freq], marker='o', color='k', s=marker_size, alpha=alpha_stipple)
    # ax.coastlines(alpha=0.7)
    # ax.add_feature(cfeature.BORDERS, alpha=0.7, lw=0.5)
    ax.add_feature(ind_coastline, alpha=0.7, lw=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=1.0, lw=0.5)
    gridliner = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gridliner.top_labels=False
    gridliner.right_labels=False
    gridliner.ylines=False
    gridliner.xlines=False
    ax.set_title(title)
    # ax.set_xlabel('Latitude')
    # ax.set_ylabel('Longitude')
    # ax.tick_params(axis='both', label=12)
