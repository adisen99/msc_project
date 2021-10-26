# Regridding using ncotoolkit (CDO installed)
#
# Make sure to run naming.sh program to change *.nc4 files to *.nc

import nctoolkit as nc
from tqdm import tqdm
import os

nc.deep_clean()

# after renaming the files nad moving to new directory
def main():
    with os.scandir('../data/GPM_data/') as it:
        for entry in tqdm(it):
            if entry.name.endswith('.nc4') and entry.is_file():
                data = nc.open_data(entry.path)
                data.to_latlon(lon = [60, 100], lat = [0, 40], res = [0.25, 0.25])
                data.to_nc('../data/GPM_lowres_data/' + entry.name)

if __name__ == "__main__":
    main()

####### Old code ###########

# ds = nc.open_data('data/*.nc') # Make sure to use directory named 'data'

# ds.to_latlon(lon = [50, 95], lat = [5, 40], res = [0.25, 0.25])

# ds.to_nc('./generic.nc') # change name before saving
