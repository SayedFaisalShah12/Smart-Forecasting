# train_model.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from preprocess import load_selected_variables

# Path to your GRIB file
grib_file = "data/era5_2025_01_01.grib"

# Choose the variable you want to train on
target_var = "t2m"  # temperature at 2m

# Load data
data_dict = load_selected_variables(grib_file, selected_vars=[target_var])

if target_var not in data_dict:
    print(f"{target_var} not loaded. Exiting.")
    exit()

# Extract the DataArray
data = data_dict[target_var]

# Handle NaNs if any
data = data.fillna(0)

# -------------------------------
# Prepare features
# -------------------------------
# We'll use a simple feature set: time, latitude, longitude
time_len = len(data['time'])
lat_len = len(data['latitude'])
lon_len = len(data['longitude'])

# Flatten data for ML
y = data.values.flatten()

# Create feature grid
time_grid, lat_grid, lon_grid = np.meshgrid(
    np.arange(time_len),
    np.arange(lat_len),
    np.arange(lon_len),
    indexing='ij'
)

X = np.column_stack([
    time_grid.flatten(),
    lat_grid.flatten(),
    lon_grid.flatten()
])

# -------------------------------
# Train/test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train the model
# -------------------------------
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# -------------------------------
# Evaluate the model
# -------------------------------
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.4f}")
print(f"R^2 Score: {r2:.4f}")

# -------------------------------
# Save the model
# -------------------------------
model_file = f"{target_var}_model.pkl"
joblib.dump(model, model_file)
print(f"Model saved to {model_file}")
