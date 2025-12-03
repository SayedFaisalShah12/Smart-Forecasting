# preprocess.py

import cfgrib
import xarray as xr

def load_and_preprocess(grib_file, param_id=130):
    """
    Load and preprocess ERA5 GRIB file using cfgrib.

    Args:
        grib_file (str): Path to the GRIB file.
        param_id (int): Parameter ID (130 = temperature)

    Returns:
        xarray.DataArray or None: Extracted variable array, or None if error
    """
    try:
        ds = xr.open_dataset(
            grib_file,
            engine="cfgrib",
            backend_kwargs={
                "filter_by_keys": {"paramId": param_id},
            },
        )

        print("GRIB file loaded successfully")
        print("Available variables:", list(ds.data_vars))

        # Automatically pick the first variable
        variable_name = list(ds.data_vars.keys())[0]
        print("Using variable:", variable_name)

        variable_data = ds[variable_name]
        return variable_data

    except Exception as e:
        print("Error loading GRIB:", e)
        return None
