import rasterio as rio
import numpy as np
import xarray as xr
import pandas as pd
import os
import sys
import calendar

def main(year: str):
    if calendar.isleap(int(year)):
        days = 366
    else:
        days = 365
    lat = np.arange(-15.0, 55.1, 0.1)
    lon = np.arange(60.0, 150.1, 0.1)
    hourly_data = np.empty((24, 701, 901))
    precip = np.empty((days, 701, 901))
    day = 0
    hour = 0
    for file in sorted(os.listdir(year)):
        img = rio.open(year + '/' + file)
        if hour <= 23:
            hourly_data[hour, :, :] = img.read(1)
            hour += 1
        else:
            precip[day, :, :] = np.sum(hourly_data, axis=0)
            hour = 0
            day += 1
            print(f"Completed days {day + 1}/{days}", end = '\r')

    print("Exporting data to netcdf file")
    ds = xr.Dataset(
            data_vars = dict(
                precip = (["time", "lat", "lon"], precip)
                ),
            coords = dict(
                lon = (["lon"], lon),
                lat = (["lat"], lat[::-1]),
                time = (["time"], pd.date_range(start = f'{year}-01-01', end = f'{year}-12-31', freq = '1D'))
                ),
            )
    ds.to_netcdf(f'./Asia-ERA5_{year}.nc') 

if __name__ == "__main__":
    year = sys.argv[1]
    main(str(year))
    print("COMPLETE")
