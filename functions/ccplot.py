import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# Preparation for the ideal C-C scaling background plots
# TODO - implement another background plot of 2*CC scaling or 1.5*CC scaling
def get_ideal_data(t2m_da, p11_inital_val, p12_initial_value):
    temparr = np.sort(t2m_da)
    p11 = [p11_inital_val]
    p12 = [p12_initial_value]

    for i in range(0, len(temparr) - 1):
        p21 = p11[i] * (1.068**(temparr[i + 1] - temparr[i]))
        p22 = p12[i] * (1.068**(temparr[i + 1] - temparr[i]))
        p11.append(p21)
        p12.append(p22)

    preciparr1 = np.array(p11)
    preciparr2 = np.array(p12)

    return temparr, preciparr1, preciparr2

# The main plot function
def plot(ds, binned_ds, temparr, preciparr1, preciparr2, percentile_val = 0.99):
    """
    Plot the C-C scaling plot between precipitation and temperature data after binning
    -----
    Input values - provide the dataset (containing both precipitation and temperature data for one
    particular lat and lon); bins (optional, default
    values are chosen by the method of data binning if equal frequencies); percentile_val (0.99, 0.5, etc.);
    p11_inital_val, and p12_initial_value (which are the initial values of precipitation for ideal C-C scaling
    background plot)
    -----
    Output - Plot of C-C scaling for the precipitation and temperature for that particular lat-lon combination
    """
    # set the data arrays to be used.
    t2m = ds.t2m
    precip = ds.precipitationCal

    # Make the figure
    fig = plt.figure(figsize=(7,5))
    binned_ds.quantile(percentile_val, interpolation = 'midpoint').precipitationCal.plot(marker = 'o', yscale = 'log', lw = 0., color = 'blue')
    plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.4)
    plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.4)
    plt.xlim(t2m.min(),t2m.max())
    plt.yticks([1, 10, 100])

    fig.gca().yaxis.set_ticks_position('both')
    fig.tight_layout()
