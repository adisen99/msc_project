# Python script to combine temperature and precipitation data for binning

import numpy as np
import xarray as xr
import time
import dask
import dask.array as da
from dask.distributed import Client
from dask.diagnostics import ProgressBar

# the main function to run
def main():
    print("Importing GPM data ...")
    mfdata_DIR = '../data/test/gpm*.nc'
    gpm = xr.open_mfdataset(mfdata_DIR, chunks=dict(time=10000, lat=40, lon=40), engine='netcdf4', combine='nested', concat_dim='time', parallel=True)
    gpm.unify_chunks()
    print("done ...")
    time.sleep(1)

    print("Now resampling precip data ...")
    precip = gpm.precipCal.resample(time='1H').mean()
    precip = precip.chunk(dict(time=10000, lat=40, lon=40))
    precip.unify_chunks()
    print("done resampling ...")
    time.sleep(1)

    print("Importing era data ...")
    mfdata_DIR2 = '../data/test/era*.nc'
    era = xr.open_mfdataset(mfdata_DIR2, chunks=dict(time=10000, lat=40, lon=40), engine='netcdf4', combine='nested', concat_dim='time', parallel=True)
    with dask.config.set(**{'array.slicing.split_large_chunks':False}):
        era = era.reindex(latitude = era.latitude[::-1])

    era = era.sel(time = slice("2000-06-01 00:00:00","2021-06-30 23:00:00"))
    era.unify_chunks()
    # era = era.sel(expver=1, drop=True)
    era = era.transpose('time', 'latitude', 'longitude')
    era = era.rename_dims({'longitude':'lon', 'latitude':'lat'})
    era = era.rename({'longitude':'lon', 'latitude':'lat'})
    print("done ...")
    time.sleep(1)

    print("Now extracting T2 and D2 ...")
    t2m = era.t2m
    d2m = era.d2m
    t2m = t2m.chunk(dict(time=10000, lat=40, lon=40))
    d2m = d2m.chunk(dict(time=10000, lat = 40, lon=40))
    print("done ...")
    time.sleep(1)

    print("Now combining into new dataset ...")
    ds_comb = xr.merge([precip, t2m, d2m])
    print("done ...")
    time.sleep(1)

    print("Now exporting to disk ...")
    delayedObj = ds_comb.to_netcdf('../data/combined/ds_comb2.nc', compute=False)

    with ProgressBar():
        results = delayedObj.compute()

    print(results)

if __name__ == "__main__":
    main()
    print("Finished")
