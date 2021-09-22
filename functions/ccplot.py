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
def plot(ds, binned_ds, temparr, preciparr1, preciparr2, **kwargs):
    # set the data arrays to be used.
    t2m = ds.t2m
    precip = ds.precipitationCal

    # Make the figure
    binned_ds.precipitationCal.plot(**kwargs)
    # binned_ds.precipitationCal.plot(marker = 'o', yscale = 'log', lw = 0., color = 'blue')
    plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.4)
    plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.4)
    plt.xlim(t2m.min(),t2m.max())
    plt.yticks([1, 10, 100])
