import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy import stats

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
def plot(ds, binned_ds, bin_var, temparr, preciparr1, preciparr2, preciparr3, preciparr4, fit = True, **kwargs):
    # get the mid points of the temperature bins
    bin_mids = []
    bin_array = binned_ds.coords[bin_var].to_numpy()

    for i in range(0, len(bin_array)):
        bin_mid = (bin_array[i].left + bin_array[i].right) * 0.5
        bin_mids.append(bin_mid)

    mids = np.array(bin_mids)

    # Make the figure
    if fit == True:
        # get the slope and intercept of the data to be plotted
        slope, intercept, r, _, _ = stats.linregress(mids, np.log(binned_ds.precipitationCal))
        # start plotting
        plt.semilogy(mids, binned_ds.precipitationCal, **kwargs)
        # binned_ds.precipitationCal.plot(**kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.plot(mids, slope*mids + intercept, color = 'k', ls = '-', alpha = 0.8, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}')
        plt.xlim(mids.min() - 0.2, mids.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)

    elif fit == False:
        slope, _, r, _, _ = stats.linregress(mids, np.log(binned_ds.precipitationCal))
        # start plotting
        plt.semilogy(mids, binned_ds.precipitationCal, label = f'C-C scale = {np.round(100*(np.exp(slope) - 1), 3)}; $R^2$ = {np.round(r,3)}', **kwargs)
        # binned_ds.precipitationCal.plot(**kwargs)
        plt.semilogy(temparr, preciparr1, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr2, 'k--', alpha = 0.3)
        plt.semilogy(temparr, preciparr3, 'k:', alpha = 0.3)
        plt.semilogy(temparr, preciparr4, 'k:', alpha = 0.3)
        plt.xlim(mids.min() - 0.2, mids.max() + 0.2)
        # plt.yticks([1, 10, 100])
        plt.legend(frameon = False)
