# Regridding using ncotoolkit (CDO installed)
#
# Make sure to run naming.sh program to change *.nc4 files to *.nc

import nctoolkit as nc
import os

# after renaming the files nad moving to new directory
with os.scandir('/home/aditya/github/msc_project/data/GPM_ncdata/') as it:
    for entry in it:
        if entry.name.endswith('.nc') and entry.is_file():
            data = nc.open_data(entry.path)
            data.to_latlon(lon = [50, 95], lat = [5, 40], res = [0.25, 0.25])
            data.to_nc('/home/aditya/github/msc_project/data/GPM_lowres_data/' + entry.name)

####### Old code ###########

# ds = nc.open_data('data/*.nc') # Make sure to use directory named 'data'

# ds.to_latlon(lon = [50, 95], lat = [5, 40], res = [0.25, 0.25])

# ds.to_nc('./generic.nc') # change name before saving
