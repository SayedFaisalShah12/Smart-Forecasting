# train_model.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib  # to save the trained model
from preprocess import load_and_preprocess

# Path to your GRIB file
grib_file = "data/era5_2025_01_01.grib"

# Load the data (temperature as an example)
temperature_data = load_and_preprocess(grib_file, param_id=130)

if temperature_data is None:
    print("Data loading failed. Exiting.")
    exit()

# -------------------------------
# Prepare the data for ML training
# -------------------------------

# Convert xarray.DataArray to numpy array
y = temperature_data.values.flatten()

# Create simple features: using indices as feature
X = np.arange(len(y)).reshape(-1, 1)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# Train a Random Forest Regressor
# -------------------------------

model = RandomForestRegressor(n_estimators=100, random_state=42)
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
# Save the trained model
# -------------------------------

model_file = "temperature_model.pkl"
joblib.dump(model, model_file)
print(f"Model saved to {model_file}")
