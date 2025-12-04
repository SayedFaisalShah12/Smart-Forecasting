# preprocess.py

import cfgrib
import xarray as xr

def load_variable(grib_file, param_id):
    """
    Loads a single variable from a GRIB file based on paramId.
    Returns an xarray DataArray.
    """

    try:
        ds = xr.open_dataset(
            grib_file,
            engine="cfgrib",
            backend_kwargs={
                "filter_by_keys": {"paramId": param_id},
                "indexpath": ""   # Avoid multiple index files
            }
        )
    except Exception as e:
        print(f"❌ Could not open GRIB for paramId={param_id}: {e}")
        return None

    # GRIB datasets typically have only 1 main variable
    var_name = list(ds.data_vars)[0]
    print(f"✅ Loaded {var_name} (paramId={param_id})")

    return ds[var_name]
