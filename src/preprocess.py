import cfgrib
import xarray as xr
import numpy as np

# Path to your GRIB file
grib_file = "data/era5_2025_01_01.grib"

# Open GRIB file using cfgrib
# Use 'filter_by_keys' to select only the variable you need to avoid conflicts

def load_and_preprocess(grib_file, param_id=130):
    try:
        ds = xr.open_dataset(
            grib_file,
            engine="cfgrib",
            backend_kwargs={
                "filter_by_keys": {"paramId": 130},  # Example: select temperature
            },
        )
        print(ds)
        return ds
    
    except cfgrib.dataset.DatasetBuildError as e:
        print("Dataset build error:", e)
        return None

