import streamlit as st
import numpy as np
import xarray as xr
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import cfgrib

# ------------------------------
# Load Trained Model
# ------------------------------

MODEL_PATH = Path("../models/trained_model.pkl")

@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        st.error("❌ Model not found. Train the model first.")
        return None

model = load_model()


# ------------------------------
# Load GRIB Data
# ------------------------------

def load_variable(grib_file, param_id):
    try:
        ds = xr.open_dataset(
            grib_file,
            engine="cfgrib",
            backend_kwargs={"filter_by_keys": {"paramId": param_id}}
        )
        var_name = list(ds.data_vars)[0]
        st.success(f"Loaded: {var_name} (paramId={param_id})")
        return ds[var_name]
    except Exception as e:
        st.warning(f"Skipping variable paramId={param_id}: {e}")
        return None


def preprocess(grib_file):
    t2m = load_variable(grib_file, 167)   # 2m temperature
    u10 = load_variable(grib_file, 165)   # 10m U wind
    v10 = load_variable(grib_file, 166)   # 10m V wind
    d2m = load_variable(grib_file, 168)   # 2m dewpoint

    variables = [t2m, u10, v10, d2m]
    variables = [v for v in variables if v is not None]

    if not variables:
        st.error("❌ No valid variables found in the GRIB file.")
        return None

    combined = np.stack([v.values.flatten() for v in variables], axis=1)
    return combined


# ------------------------------
# Streamlit UI
# ------------------------------

st.title("🌦️ Smart Weather Forecasting App")
st.write("Upload an ERA5 GRIB file and get predictions using the trained model.")

uploaded_file = st.file_uploader("Upload GRIB file (.grib)", type=["grib"])

if uploaded_file is not None:

    # Save uploaded file temporarily
    grib_path = "temp_input.grib"
    with open(grib_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Extracting weather variables...")

    X = preprocess(grib_path)

    if X is not None and model is not None:
        st.success("Variables extracted successfully!")

        # Make predictions
        st.subheader("📊 Predicted Temperature Values")
        predictions = model.predict(X)

        st.write(predictions)

        # Plot prediction graph
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(predictions, label="Predicted Temperature")
        ax.set_title("Temperature Prediction Curve")
        ax.set_xlabel("Data Index")
        ax.set_ylabel("Temperature (K)")
        ax.legend()

        st.pyplot(fig)

        st.success("🎉 Prediction completed!")

