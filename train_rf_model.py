import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import joblib

# Load the dataset
data = pd.read_csv('modem_diagnostics_data.csv')

# Drop irrelevant columns (like serial numbers, model names)
data = data.drop(columns=['Customer Account ID', 'Site ID', 'Modem Serial Number', 'Model', 'Last Checkup Date', 'Failure Date'])

# Convert categorical columns (Error Type, Modulation Type) to numeric using one-hot encoding
data = pd.get_dummies(data, columns=['Error Type', 'Modulation Type'])

# Define the feature columns (input to the model) and target column (Next Predicted Failure)
X = data.drop(columns=['Next Predicted Failure (days)'])
y = data['Next Predicted Failure (days)']

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model on the training data
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Save the trained model
joblib.dump(rf_model, 'modem_failure_prediction_model.pkl')

# Save the column order for predictions later
joblib.dump(X_train.columns, 'modem_model_columns.pkl')

# Load the model and column structure for prediction
loaded_model = joblib.load('modem_failure_prediction_model.pkl')
model_columns = joblib.load('modem_model_columns.pkl')

# Example input for a new modem (Ensure that this input matches the column structure after one-hot encoding)
# Adjust the values and length to match the exact number of columns
example_input = pd.DataFrame([[300, -65, 1.5, 0.1, 35, -80, 0.02, 50, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]],
                             columns=model_columns)

# Predict using the loaded model
predicted_failure_days = loaded_model.predict(example_input)
print(f"Predicted Failure in {predicted_failure_days[0]:.2f} days")
