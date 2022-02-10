# The new technique to determine the scaling
import numpy as np
import util

# 3d function
def get_scaling_3d(precip, t2m, d2m, pres, temp_levels, q, vimd, evap, omega, u, v):
    print("Starting the scaling process ...")

    print("Initializing zero arrays ...")

    xrange = len(t2m[0])
    yrange = len(t2m[0][0])

    # initialising the for loop by making zeros array for t2m and d2m to mutate
    slope_t2m_95 = np.empty((xrange, yrange))
    p_t2m_95 = np.empty((xrange, yrange))
    slope_d2m_95 = np.empty((xrange, yrange))
    p_d2m_95 = np.empty((xrange, yrange))

    vimd_t2m = np.empty((xrange, yrange))
    vimdp_t2m = np.empty((xrange, yrange))
    vimd_d2m = np.empty((xrange, yrange))
    vimdp_d2m = np.empty((xrange, yrange))

    m1_full_t2m_95 = np.empty((xrange, yrange))
    m1_fullp_t2m_95 = np.empty((xrange, yrange))
    m1_full_d2m_95 = np.empty((xrange, yrange))
    m1_fullp_d2m_95 = np.empty((xrange, yrange))
    m1_dyn_t2m_95 = np.empty((xrange, yrange))
    m1_dynp_t2m_95 = np.empty((xrange, yrange))
    m1_dyn_d2m_95 = np.empty((xrange, yrange))
    m1_dynp_d2m_95 = np.empty((xrange, yrange))
    m1_thermo_t2m_95 = np.empty((xrange, yrange))
    m1_thermop_t2m_95 = np.empty((xrange, yrange))
    m1_thermo_d2m_95 = np.empty((xrange, yrange))
    m1_thermop_d2m_95 = np.empty((xrange, yrange))

    m2_full_t2m_95 = np.empty((xrange, yrange))
    m2_fullp_t2m_95 = np.empty((xrange, yrange))
    m2_full_d2m_95 = np.empty((xrange, yrange))
    m2_fullp_d2m_95 = np.empty((xrange, yrange))
    m2_dyn_t2m_95 = np.empty((xrange, yrange))
    m2_dynp_t2m_95 = np.empty((xrange, yrange))
    m2_dyn_d2m_95 = np.empty((xrange, yrange))
    m2_dynp_d2m_95 = np.empty((xrange, yrange))
    m2_thermo_t2m_95 = np.empty((xrange, yrange))
    m2_thermop_t2m_95 = np.empty((xrange, yrange))
    m2_thermo_d2m_95 = np.empty((xrange, yrange))
    m2_thermop_d2m_95 = np.empty((xrange, yrange))
    v_adv_t2m_95 = np.empty((xrange, yrange))
    v_advp_t2m_95 = np.empty((xrange, yrange))
    v_adv_d2m_95 = np.empty((xrange, yrange))
    v_advp_d2m_95 = np.empty((xrange, yrange))
    h_adv_t2m_95 = np.empty((xrange, yrange))
    h_advp_t2m_95 = np.empty((xrange, yrange))
    h_adv_d2m_95 = np.empty((xrange, yrange))
    h_advp_d2m_95 = np.empty((xrange, yrange))

    precip95 = np.empty((xrange, yrange))
    precip_median = np.empty((xrange, yrange))
    vimd_median = np.empty((xrange, yrange))
    evap_median = np.empty((xrange, yrange))
    pe_median1 = np.empty((xrange, yrange))
    dyn_median1 = np.empty((xrange, yrange))
    thermo_median1 = np.empty((xrange, yrange))
    pe_median2 = np.empty((xrange, yrange))
    dyn_median2 = np.empty((xrange, yrange))
    thermo_median2 = np.empty((xrange, yrange))
    v_adv_median = np.empty((xrange, yrange))
    h_adv_median = np.empty((xrange, yrange))

    mb1 = np.empty((xrange, yrange))
    fb1 = np.empty((xrange, yrange))
    rmse1 = np.empty((xrange, yrange))

    mb2 = np.empty((xrange, yrange))
    fb2 = np.empty((xrange, yrange))
    rmse2 = np.empty((xrange, yrange))

    loc_change = np.empty((xrange, yrange))

    print("Starting the loop ...")

    # starting loop
    for lat in range(xrange):
        for lon in range(yrange):

            # redefine for convinience
            preciparr = precip.isel(lat = lat, lon = lon)
            t2marr = t2m.isel(lat = lat, lon = lon)
            d2marr = d2m.isel(lat = lat, lon = lon)
            temparr = temp_levels.isel(lat = lat, lon = lon)
            qarr = q.isel(lat = lat, lon = lon)
            vimdarr = vimd.isel(lat = lat, lon = lon)
            evaparr = evap.isel(lat = lat, lon = lon)
            omegaarr = omega.isel(lat = lat, lon = lon)
            uarr = u.isel(lat = lat, lon = lon)
            varr = v.isel(lat = lat, lon = lon)

            # start
            p95 = preciparr.quantile(0.95, interpolation='higher')
            precip_events, precip_idxs = util.get_events_precip(p95, preciparr)
            precip_events_median = np.median(precip_events)
            t2m_events = t2marr[precip_idxs]
            d2m_events = d2marr[precip_idxs]
            temp_events = temparr[precip_idxs]
            q_events = qarr[precip_idxs]
            vimd_events = vimdarr[precip_idxs]
            vimd_events_median = np.median(vimd_events)
            evap_events = evaparr[precip_idxs]
            evap_events_median = np.median(evap_events)
            omega_events = omegaarr[precip_idxs]
            u_events = uarr[precip_idxs]
            v_events = varr[precip_idxs]

            #### SCALING first

            # getting the slope and p-value for precipitation and vimd
            slope_t2m_95[lat, lon], p_t2m_95[lat, lon] = util.get_res(t2m_events, precip_events)
            slope_d2m_95[lat, lon], p_d2m_95[lat, lon] = util.get_res(d2m_events, precip_events)
            vimd_t2m[lat, lon], vimdp_t2m[lat, lon] = util.get_res(t2m_events, vimd_events)
            vimd_d2m[lat, lon], vimdp_d2m[lat, lon] = util.get_res(d2m_events, vimd_events)

            #### TODO CHECK: CALCULATING DYN AND THERMO USING METHOD-1

            # get the values of qs
            qs_events  = util.calc_qs(temp_events, pres)

            # get the value of precipitation estimate
            pe_events1, dyn_events1, thermo_events1 = util.get_pe1(omega_events, pres, qs_events)
            pe_events_median1 = np.median(pe_events1)
            dyn_events_median1 = np.median(dyn_events1)
            thermo_events_median1 = np.median(thermo_events1)

            # getting the slope and p-value for METHOD-1
            m1_full_t2m_95[lat, lon], m1_fullp_t2m_95[lat, lon] = util.get_res(t2m_events, pe_events1)
            m1_full_d2m_95[lat, lon], m1_fullp_d2m_95[lat, lon] = util.get_res(d2m_events, pe_events1)
            m1_dyn_t2m_95[lat, lon], m1_dynp_t2m_95[lat, lon] = util.get_res(t2m_events, dyn_events1)
            m1_dyn_d2m_95[lat, lon], m1_dynp_d2m_95[lat, lon] = util.get_res(d2m_events, dyn_events1)
            m1_thermo_t2m_95[lat, lon], m1_thermop_t2m_95[lat, lon] = util.get_res(t2m_events, thermo_events1)
            m1_thermo_d2m_95[lat, lon], m1_thermop_d2m_95[lat, lon] = util.get_res(d2m_events, thermo_events1)

            #### TODO CHECK: CALCULATING DYN AND THERMO USING METHOD-2

            pe_events2, v_adv_events, h_adv_events, dyn_events2, thermo_events2 = util.get_pe2(evap_events, u_events, v_events, omega_events, pres, q_events)
            pe_events_median2 = np.median(pe_events2)
            dyn_events_median2 = np.median(dyn_events2)
            thermo_events_median2 = np.median(thermo_events2)
            v_adv_events_median = np.median(v_adv_events)
            h_adv_events_median = np.median(h_adv_events)

            # getting the slope and p-value for METHOD-2
            m2_full_t2m_95[lat, lon], m2_fullp_t2m_95[lat, lon] = util.get_res(t2m_events, pe_events2)
            m2_full_d2m_95[lat, lon], m2_fullp_d2m_95[lat, lon] = util.get_res(d2m_events, pe_events2)
            m2_dyn_t2m_95[lat, lon], m2_dynp_t2m_95[lat, lon] = util.get_res(t2m_events, dyn_events2)
            m2_dyn_d2m_95[lat, lon], m2_dynp_d2m_95[lat, lon] = util.get_res(d2m_events, dyn_events2)
            m2_thermo_t2m_95[lat, lon], m2_thermop_t2m_95[lat, lon] = util.get_res(t2m_events, thermo_events2)
            m2_thermo_d2m_95[lat, lon], m2_thermop_d2m_95[lat, lon] = util.get_res(d2m_events, thermo_events2)
            v_adv_t2m_95[lat, lon], v_advp_t2m_95[lat, lon] = util.get_res(t2m_events, v_adv_events)
            v_adv_d2m_95[lat, lon], v_advp_d2m_95[lat, lon] = util.get_res(d2m_events, v_adv_events)
            h_adv_t2m_95[lat, lon], h_advp_t2m_95[lat, lon] = util.get_res(t2m_events, h_adv_events)
            h_adv_d2m_95[lat, lon], h_advp_d2m_95[lat, lon] = util.get_res(d2m_events, h_adv_events)

            #### OUTPUT results

            # make 2-D arrays
            precip95[lat, lon] = p95
            precip_median[lat, lon] = precip_events_median
            vimd_median[lat, lon] = vimd_events_median
            evap_median[lat, lon] = evap_events_median
            pe_median1[lat, lon] = pe_events_median1
            dyn_median1[lat, lon] = dyn_events_median1
            thermo_median1[lat, lon] = thermo_events_median1
            pe_median2[lat, lon] = pe_events_median2
            dyn_median2[lat, lon] = dyn_events_median2
            thermo_median2[lat, lon] = thermo_events_median2
            v_adv_median[lat, lon] = v_adv_events_median
            h_adv_median[lat, lon] = h_adv_events_median

            # caclulate errors for method1 and method-2 (pb is given outside the loop)
            mb1[lat, lon], fb1[lat, lon], rmse1[lat, lon] = util.get_stats(precip_events, pe_events1)
            mb2[lat, lon], fb2[lat, lon], rmse2[lat, lon] = util.get_stats(precip_events, pe_events2)

            # calculate the moisture discharge / recharge i.e. local change
            loc_change[lat, lon] = precip_events - pe_events2

            print(f"Completed {lat+1}/{xrange} lat and {lon+1}/{yrange} lon", end='\r')

    # get the percentage bias
    pb1 = ((precip_median - pe_median1) / precip_median) * 100
    pb2 = ((precip_median - pe_median2) / precip_median) * 100


    # return all the values as  dictionary
    res = {
            # general values and scaling
            "precip_95" : precip95, # 95th percentile precipitation obtaied from new scaling method
            "slope_t2m_95" : slope_t2m_95, # slope of 95th percentile vs SAT
            "p_t2m_95" : p_t2m_95, # p-value of 95th percentile vs SAT
            "slope_d2m_95" : slope_d2m_95, # slope of 95th percentile vs DPT
            "p_d2m_95" : p_d2m_95, # p-value of 95th percentile vs DPT
            # vimd scaling
            "vimd_t2m" : vimd_t2m,
            "vimdp_t2m" : vimdp_t2m,
            "vimd_d2m" : vimd_d2m,
            "vimdp_d2m" : vimdp_d2m,
            # the scaling obtained from M1
            "m1_full_t2m_95" : m1_full_t2m_95,
            "m1_fullp_t2m_95" : m1_fullp_t2m_95,
            "m1_full_d2m_95" : m1_full_d2m_95,
            "m1_fullp_d2m_95" : m1_fullp_d2m_95,
            "m1_dyn_t2m_95" : m1_dyn_t2m_95,
            "m1_dynp_t2m_95" : m1_dynp_t2m_95,
            "m1_dyn_d2m_95" : m1_dyn_d2m_95,
            "m1_dynp_d2m_95" : m1_dynp_d2m_95,
            "m1_thermo_t2m_95" : m1_thermo_t2m_95,
            "m1_thermop_t2m_95" : m1_thermop_t2m_95,
            "m1_thermo_d2m_95" : m1_thermo_d2m_95,
            "m1_thermop_d2m_95" : m1_thermop_d2m_95,
            # the scaling obtained from M2
            "m2_full_t2m_95" : m2_full_t2m_95,
            "m2_fullp_t2m_95" : m2_fullp_t2m_95,
            "m2_full_d2m_95" : m2_full_d2m_95,
            "m2_fullp_d2m_95" : m2_fullp_d2m_95,
            "m2_dyn_t2m_95" : m2_dyn_t2m_95,
            "m2_dynp_t2m_95" : m2_dynp_t2m_95,
            "m2_dyn_d2m_95" : m2_dyn_d2m_95,
            "m2_dynp_d2m_95" : m2_dynp_d2m_95,
            "m2_thermo_t2m_95" : m2_thermo_t2m_95,
            "m2_thermop_t2m_95" : m2_thermop_t2m_95,
            "m2_thermo_d2m_95" : m2_thermo_d2m_95,
            "m2_thermop_d2m_95" : m2_thermop_d2m_95,
            "v_adv_t2m_95" : v_adv_t2m_95,
            "v_advp_t2m_95" : v_advp_t2m_95,
            "v_adv_d2m_95" : v_adv_d2m_95,
            "v_advp_d2m_95" : v_advp_d2m_95,
            "h_adv_t2m_95" : h_adv_t2m_95,
            "h_advp_t2m_95" : h_advp_t2m_95,
            "h_adv_d2m_95" : h_adv_d2m_95,
            "h_advp_d2m_95" : h_advp_d2m_95,
            # medians
            "precip_median" : precip_median, # median of all extreme events at all grid points
            "vimd_median" : vimd_median, # median of all vimd associated with extremes at all grid points
            "evap_median" : evap_median, # median of all evap associated with extremes at all grid points
            "pe_median1" : pe_median1, # median of all precipitation estimates obtained using METHOD-1
            "dyn_median1" : dyn_median1, # median of all dyn estimates obtained using METHOD-1
            "thermo_median1" : thermo_median1, # median of all thermo estimates obtained using METHOD-1
            "pe_median2" : pe_median2, # median of all precipitation estimates obtained using METHOD-2
            "dyn_median2" : dyn_median2, # median of all dyn estimates obtained using METHOD-2
            "thermo_median2" : thermo_median2, # median of all thermo estimates obtained using METHOD-2
            "v_adv_median" : v_adv_median, # median of all v_adv estimates obtained using METHOD-2
            "h_adv_median" : h_adv_median, # median of all h_adv estimates obtained using METHOD-2
            # local change (recharge or discharge)
            "loc_change" : loc_change,
            # errors
            "mb1" : mb1,
            "fb1" : fb1,
            "pb1" : pb1,
            "rmse1" : rmse1,
            "mb2" : mb2,
            "fb2" : fb2,
            "pb2" : pb2,
            "rmse2" : rmse2,
            }

    return res
