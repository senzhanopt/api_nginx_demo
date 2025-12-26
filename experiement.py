# simple_mlflow_test.py

import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Generate random data
X = np.random.rand(100, 1)
y = 3 * X.squeeze() + np.random.randn(100) * 0.5  # y = 3*x + noise

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))  # Replace with your MLflow server URI

# Start MLflow run
with mlflow.start_run():
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    # Log parameters, metrics, and model
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(model, "linear_model")

    print(f"Logged MSE: {mse}")

