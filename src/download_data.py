import cdsapi
import os

def download_era5_month(year="2025", month="01"):
    # Ensure the data folder exists
    data_folder = '../data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Prepare list of days in the month (1–31, API will handle invalid dates automatically)
    days = [f"{day:02d}" for day in range(1, 32)]

    # Define dataset and request
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "mean_sea_level_pressure",
            "mean_wave_direction",
            "mean_wave_period",
            "sea_surface_temperature",
            "significant_height_of_combined_wind_waves_and_swell",
            "surface_pressure",
            "total_precipitation",
            "cloud_base_height",
            "total_column_cloud_ice_water",
            "potential_evaporation"
        ],
        "year": [year],
        "month": [month],
        "day": days,
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "format": "grib"
    }

    # Initialize client
    client = cdsapi.Client()

    # Download dataset
    output_file = os.path.join(data_folder, f'era5_{year}_{month}.grib')
    print(f"Downloading ERA5 data for {year}-{month} to {output_file} … ⬇️")
    client.retrieve(dataset, request, output_file)
    print("Download complete! ✅")

if __name__ == "__main__":
    # Change year and month here as needed
    download_era5_month(year="2025", month="01")
