# New parallel download script

import cdsapi
import multiprocessing
import os

client = cdsapi.Client()

def cdsapi_worker(dataset):
    if not os.path.exists(dataset['file_name']):
        result = client.retrieve('reanalysis-era5-single-levels', dataset)
        result.download(dataset['file_name'])

def single_dataset(yr, file_prefix):
    return {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': ['vertical_integral_of_eastward_water_vapour_flux', 'vertical_integral_of_northward_water_vapour_flux'],
        'area': [
            40, 60, 0,
            100,
        ],
        'year': str(yr),
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        # making an arbitrary entry to the dict
        'file_name': file_prefix+'_'+str(yr)+'.nc'
    }

# make the changes to this file to get the necessary values parallely
datasets = [single_dataset(yr, 'wv_flux') for yr in range(2000,2021)]

# https://cds.climate.copernicus.eu/live/queue
# per-user requests that access online CDS data is 3 at maximum

# so we overbook by one with 4 processes
pool = multiprocessing.Pool(processes=4)
pool.map(cdsapi_worker, datasets)
