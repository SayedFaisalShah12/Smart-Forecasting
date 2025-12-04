import xarray as xr
import os

def load_selected_variables(grib_file, selected_vars=None):
    if not os.path.exists(grib_file):
        print(f"❌ GRIB file not found: {grib_file}")
        return {}

    # ERA5 paramId mapping
    param_map = {
        "t2m": 167,
        "d2m": 168,
        "u10": 165,
        "v10": 166,
        "msl": 151,
        "sst": 34,
        "sp": 134,
        "tciw": 31,
    }

    loaded = {}

    for var in selected_vars:
        if var not in param_map:
            print(f"⚠ Unknown variable: {var}")
            continue

        paramId = param_map[var]

        try:
            ds = xr.open_dataset(
                grib_file,
                engine="cfgrib",
                backend_kwargs={
                    "filter_by_keys": {"paramId": paramId},
                    "read_keys": ["paramId", "shortName"],  # avoid merging
                },
            )

            data_var = list(ds.data_vars)[0]  # extract first variable
            loaded[var] = ds[data_var]

            print(f"✅ Loaded {var} (paramId={paramId})")

        except Exception as e:
            print(f"❌ Could not load {var}: {e}")

    return loaded
