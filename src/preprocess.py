import cfgrib
import xarray as xr

grib_file = "../data/era5_2025_01_01.grib"


def load_selected_variables(grib_file, selected_vars):
    dataset = {}
    for var in selected_vars:
        try:
            ds = xr.open_dataset(
                grib_file,
                engine="cfgrib",
                backend_kwargs={"filter_by_keys": {"shortName": var}}
            )
            variable_name = list(ds.data_vars.keys())[0]
            dataset[var] = ds[variable_name]
            print(f"Loaded: {var}")
        except Exception as e:
            print(f"❌ Could not load {var}: {e}")
    return dataset

selected_vars = ["t2m", "u10", "v10", "d2m", "msl", "sp"]
data = load_selected_variables(grib_file, selected_vars)

    selected_vars = ["t2m", "u10", "v10", "d2m", "msl", "sp"]

    dataset = {}

    for var in selected_vars:
        try:
            ds = xr.open_dataset(
                grib_file,
                engine="cfgrib",
                backend_kwargs={"filter_by_keys": {"shortName": var}},
            )

            variable_name = list(ds.data_vars.keys())[0]
            dataset[var] = ds[variable_name]

            print(f"Loaded: {var}")

        except Exception as e:
            print(f"❌ Could not load {var}: {e}")

    return dataset


if __name__ == "__main__":
    data = load_selected_variables("../data/era5_2025_01_01.grib")
    print("\nVariables loaded:", list(data.keys()))
