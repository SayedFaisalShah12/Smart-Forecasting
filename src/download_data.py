import cdsapi
import os

def download_era5():
    # Ensure the data folder exists
    data_folder = '../data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

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
        "year": ["2025"],
        "month": ["01"],
        "day": ["01"],
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "format": "grib"
    }

    # Initialize client
    client = cdsapi.Client()

    # Download dataset
    output_file = os.path.join(data_folder, 'era5_2025_01_01.grib')
    print(f"Downloading ERA5 data to {output_file} … ⬇️")
    client.retrieve(dataset, request, output_file)
    print("Download complete! ✅")

if __name__ == "__main__":
    download_era5()
