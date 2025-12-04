# train_model.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from preprocess import load_variable

# --------------------------------------
# Load GRIB variable (example: t2m)
# --------------------------------------
grib_file = "data/era5_2025_01_01.grib"
param_id = 167  # t2m

data = load_variable(grib_file, param_id)

if data is None:
    print("❌ Variable not found. Exiting.")
    exit()

print(f"Loaded variable: paramId={param_id} shape={data.values.shape}")

# --------------------------------------
# Convert data to numpy
# --------------------------------------
y_full = data.values.flatten()

# --------------------------------------
# ⚠️ DOWNSAMPLE to avoid memory errors
# --------------------------------------
DOWNSAMPLE_FACTOR = 50  # reduce data size

y = y_full[::DOWNSAMPLE_FACTOR]
X = np.arange(len(y)).reshape(-1, 1)

print(f"Downsampled dataset from {len(y_full)} → {len(y)}")

# --------------------------------------
# Train-test split
# --------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------
# Choose Model (Safe on Low RAM)
# --------------------------------------
USE_RF = False  # switch to True if you want RandomForest

if USE_RF:
    print("Training RandomForest...")
    model = RandomForestRegressor(
        n_estimators=20,   # smaller
        max_depth=10,      # smaller
        random_state=42,
        n_jobs=-1
    )
else:
    print("Training LinearRegression (recommended)...")
    model = LinearRegression()

model.fit(X_train, y_train)

# --------------------------------------
# Evaluate
# --------------------------------------
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nMSE: {mse:.4f}")
print(f"R² Score: {r2:.4f}")

# --------------------------------------
# Save model
# --------------------------------------
save_path = "trained_model.pkl"
joblib.dump(model, save_path)
print(f"\nModel saved to {save_path}")
