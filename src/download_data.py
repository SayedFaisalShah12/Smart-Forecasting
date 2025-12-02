import cdsapi

def download_era5():
    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                '2m_temperature', 'surface_pressure', 'total_precipitation',
                '2m_dewpoint_temperature', 'u_component_of_wind_10m',
                'v_component_of_wind_10m'
            ],
            'year': '2025',
            'month': [f"{m:02d}" for m in range(1, 13)],
            'day': [f"{d:02d}" for d in range(1, 32)],
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'format': 'netcdf'
        },
        '../data/era5_2025.nc'
    )

if __name__ == "__main__":
    download_era5()
