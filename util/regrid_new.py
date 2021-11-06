# Regridding using ESMF library in python (xesmf)
# the new regrid script using the ESMF regridding framework

import numpy as np
import xarray as xr
import dask.array as da
import xesmf as xe
import time
import os
from dask.distributed import Client
from dask.diagnostics import ProgressBar

# client = Client(n_workers = 8, threads_per_worker = 1, memory_limit = '64GB')

# after renaming the files nad moving to new directory
def main():
    with os.scandir('../data/GPM_data/') as it:
        for entry in it:
            if entry.name.endswith('.nc') and entry.is_file() and not os.path.exists('../data/GPM_lowres_data/' + entry.name):
                print("Starting the Regridding of - " + entry.name + " ...")
                # data = nc.open_data(entry.path)
                # data.to_latlon(lon = [60, 100], lat = [0, 40], res = [0.25, 0.25])
                # data.to_nc('../data/GPM_lowres_data/' + entry.name)
                # loading the data
                ds = xr.open_dataset(entry.path, chunks=dict(time=2000))
                ds.unify_chunks()
                ds = ds.drop_dims('bnds')
                ds = ds.transpose('time', 'lat', 'lon')

                print("Data is imported successfully ...")

                # prepare the regridding
                ds_out = xr.Dataset({'lat': (['lat'], np.arange(0, 40.25, 0.25)),
                    'lon': (['lon'], np.arange(60, 100.25, 0.25)),
                    }
                )
                regridder = xe.Regridder(ds, ds_out, 'bilinear')

                print("Data has been successfully prepared for regridding ...")

                # Do the regridding
                dr_out = regridder(ds.precipitationCal)

                print("The data has been regridded, now exporting ...")

                # Ooutput the data
                dr_out = dr_out.to_dataset(name = 'precipCal')
                delayedObj = dr_out.to_netcdf('../data/GPM_lowres_data/' + entry.name, compute=False)

                with ProgressBar():
                    results = delayedObj.compute()

                print(results)
                print("Finished Regridding and data exported " + entry.name)
                time.sleep(7)

if __name__ == "__main__":
    main()
    print("Finished the Regridding process")
