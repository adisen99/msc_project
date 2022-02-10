# bunch of utility functions
import numpy as np
from scipy import stats
from scipy import integrate
from sklearn.metrics import mean_squared_error as mse

# util function to determine the number of bins
def equal_obs(x, nbin):
    nlen = len(x)
    return np.interp(np.linspace(0, nlen, nbin + 1),
                     np.arange(nlen),
                     np.sort(x, axis= None))

# util function to get the slope value
def get_res(x, y):
    # if np.isnan(np.sum(y)):
    #     slope, intercept, r, p, se = stats.linregress(x, y)
    # else:
    slope, _, _, p, _ = stats.linregress(x, np.log(y))

    return slope, p

# util function to find the values greater than or equal to p95 in precipitation array
# and use the indices of the events to get the meteorological values in the main function
def get_events_precip(p95, preciparr):
    idxs = np.where(preciparr >= p95)
    events = preciparr[idxs]
    return events, idxs

# util function to calculate value of qs
def get_qs(temp, pres):
    a1 = 6.1114
    temp0 = 273.16
    a3w = 17.269
    a4w = 35.86
    a3i = 21.875
    a4i = 7.66

    # calculating saturation vapor pressure using temperature values
    if temp > temp0:
        a3 = a3w
        a4 = a4w
        es = a1 * np.exp(a3 * ((temp - temp0)/(temp - a4)))
    elif temp < temp0 - 23:
        a3 = a3i
        a4 = a4i
        es = a1 * np.exp(a3 * ((temp - temp0)/(temp - a4)))
    else:
        esw = a1 * np.exp(a3w * ((temp - temp0)/(temp - a4w)))
        esi = a1 * np.exp(a3i * ((temp - temp0)/(temp - a4i)))
        es = esi + ((esw - esi)*(((temp - (temp0 - 23))/23)**2))

    # get saturation specific humidity value
    epsilon = 0.622
    qs = (epsilon * es) / (pres - ((1 - epsilon)*es))
    return qs

def calc_qs(temp, pres):
    pres_range = len(pres)
    time_range = len(temp)
    qs = np.empty((time_range, pres_range))
    for i in range(time_range):
        for j in range(pres_range):
            qs[i, j] = get_qs(temp[i, j], pres[j])
    return qs

# vert integral function (Simpson's method)
def vert_integ(x, y):
    int = integrate.simpson(y, x, even='avg')

    return int

# finite differnce methods to find derivative
def centered_diff(arr):
    arr_diff = np.empty(len(arr) - 2)
    for i in range((len(arr) - 2)):
        arr_diff[i] = arr[i+2] - arr[i]
    return arr_diff

def forward_diff(arr):
    arr_diff = np.diff(arr)
    return arr_diff

def backward_diff(arr):
    arr_diff = -(np.diff(arr[::-1])[::-1])
    return arr_diff

def get_pe1(omega, pres, qs):
    p_cdiff = centered_diff(pres)
    p_fdiff = forward_diff(pres)
    p_bdiff = backward_diff(pres)

    time_range = len(omega)
    pe = np.empty(time_range)
    thermo = np.empty(time_range)

    # taking mean omega of all extremes to get the thermodynamic contribution
    omega_mean = np.nanmean(omega)

    for i in range(time_range):
        qs_cdiff = centered_diff(qs[i])/(p_cdiff)
        qs_fdiff = forward_diff(qs[i])/(p_fdiff)
        qs_bdiff = backward_diff(qs[i])/(p_bdiff)

        qs_diff = np.insert(qs_cdiff, 0, qs_fdiff[0])
        qs_diff = np.append(qs_diff, qs_bdiff[-1])

        # TODO VARY: the value of 3600 will change for different time calculations
        # 1 hour -> 3600s
        # 3 hour -> 3600*3 and so on
        # '+' sign as pressure is from surface-to-top and not top-to-surface
        pe[i] = (+1/(9.806)) * vert_integ(pres, omega[i]*qs_diff) * 3600
        thermo[i] = (+1/(9.806)) * vert_integ(pres, omega_mean*qs_diff) * 3600

    dyn = pe - thermo
    return pe, dyn, thermo

def get_pe2(evap, u, v, omega, pres, q):
    p_cdiff = centered_diff(pres)
    p_fdiff = forward_diff(pres)
    p_bdiff = backward_diff(pres)

    time_range = len(omega)
    pe = np.empty(time_range)
    thermo = np.empty(time_range)
    v_adv = np.empty(time_range)
    h_adv = np.empty(time_range)

    # taking mean of all extremes to get the thermodynamic contribution
    omega_mean = np.nanmean(omega)

    for i in range(time_range):
        q_cdiff = centered_diff(q[i])/(p_cdiff)
        q_fdiff = forward_diff(q[i])/(p_fdiff)
        q_bdiff = backward_diff(q[i])/(p_bdiff)

        q_diff = np.insert(q_cdiff, 0, q_fdiff[0])
        q_diff = np.append(q_diff, q_bdiff[-1])

        # TODO VARY: the value of 3600 will change for different time calculations
        # 1 hour -> 3600s
        # 3 hour -> 3600*3 and so on
        v_adv[i] = (+1/(9.806)) * vert_integ(pres, omega[i]*q_diff) * 3600
        thermo[i] = (+1/(9.806)) * vert_integ(pres, omega_mean*q_diff) * 3600

        # calculating the gradient of q (TODO CHECK: check the dimensions order, should be [lat, lon, pres])
        gradq = np.gradient(q[i])
        h_adv[i] = (+1/(9.806)) * vert_integ(pres, (u[i] * gradq[0] + v[i] * gradq[1]))

        pe[i] = evap[i] - v_adv - h_adv

    dyn = v_adv - thermo
    # calculate recharge/discharge from the main program
    return pe, v_adv, h_adv, dyn, thermo

# get statistical measures
# NOTE : percentage bias will be calculated in the main loop
def get_stats(p, pe):
    mb = np.mean(pe - p)
    fb = np.sum(pe - p) / np.sum(pe + p)
    rmse = np.sqrt(mse(p, pe))
    return mb, fb, rmse
