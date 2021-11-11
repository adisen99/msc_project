import cdsapi
import os
import time

c = cdsapi.Client()

def down():
    for year in range(2000,2009):
        for month in range(1,12):
            use_year = str(year)
            if month < 10:
                use_month = '0' + str(month)
            else:
                use_month = str(month)
            # Downloading data    
            if not os.path.exists('../data/era_pres_data/era_pres_' + use_year + use_month + '.nc'):
                print("Downloading data for year " + use_year + " and month " + use_month)
                c.retrieve(
                    'reanalysis-era5-pressure-levels',
                    {
                        'product_type': 'reanalysis',
                        'format': 'netcdf',
                        'variable': [
                            'specific_humidity', 'temperature', 'vertical_velocity',
                        ],
                        'pressure_level': [
                            '50', '70', '100',
                            '125', '150', '175',
                            '200', '225', '250',
                            '300', '350', '400',
                            '450', '500', '550',
                            '600', '650', '700',
                            '750', '775', '800',
                            '825', '850', '875',
                            '900', '925', '950',
                            '975', '1000',
                        ],
                        'year': use_year,
                        'month': use_month,
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
                        'area': [
                            40, 60, 0,
                            100,
                        ],
                    },
                    '../data/era_pres_data/era_pres_' + use_year + use_month + '.nc')

            time.sleep(5)

if __name__ == "__main__":
    down()
    print("Done ...")
