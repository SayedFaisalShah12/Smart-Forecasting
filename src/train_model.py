import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from preprocess import load_and_preprocess
import os

def train_model():
    df = load_and_preprocess()
    
    # Features and target
    X = df[['t2m_1h_ago','t2m_6h_ago','u10','v10','tp','hour']]
    y = df['t2m']

    # Split train/test
    split_idx = int(len(df) * 0.75)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE: {mse:.2f}")

    # Save model
    if not os.path.exists("../models"):
        os.makedirs("../models")
    joblib.dump(model, "../models/era5_temp_model.pkl")
    print("Model saved to ../models/era5_temp_model.pkl")

if __name__ == "__main__":
    train_model()
