# Regridding using ncotoolkit (CDO installed)
#
# This is the old regrrid script using python-cdo

import nctoolkit as nc
import time
import os

nc.deep_clean()

# after renaming the files nad moving to new directory
def main():
    with os.scandir('../data/GPM_data/') as it:
        for entry in it:
            if entry.name.endswith('.nc') and entry.is_file() and not os.path.exists('../data/GPM_lowres_data/' + entry.name):
                print("Starting the Regridding of - " + entry.name)
                data = nc.open_data(entry.path)
                data.to_latlon(lon = [60, 100], lat = [0, 40], res = [0.25, 0.25])
                data.to_nc('../data/GPM_lowres_data/' + entry.name)
                print("Finished Regridding - " + entry.name)
                time.sleep(30)

if __name__ == "__main__":
    main()
    print("Finished the Regridding process")

####### Old code ###########

# ds = nc.open_data('data/*.nc') # Make sure to use directory named 'data'

# ds.to_latlon(lon = [50, 95], lat = [5, 40], res = [0.25, 0.25])

# ds.to_nc('./generic.nc') # change name before saving
