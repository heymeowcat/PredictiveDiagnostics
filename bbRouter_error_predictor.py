import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

data = pd.read_csv('bbRouter_diagnostics_data.csv')

# Convert Error codes from JSON string to list
data['ErrorCodes'] = data['ErrorCodes'].apply(json.loads)

# Create MultiLabelBinarizer for Error codes
mlb = MultiLabelBinarizer()
error_codes_encoded = mlb.fit_transform(data['ErrorCodes'])

# Prepare features
features = [
    'Downstream Power (dBmV)', 'Upstream Power (dBmV)',
    'Downstream SNR (dB)', 'Upstream SNR (dB)',
    'Downstream Frequency (MHz)', 'Upstream Frequency (MHz)',
    'Packet Loss (%)', 'Latency (ms)', 'Jitter (ms)',
    'WiFi 2.4GHz Channel', 'WiFi 5GHz Channel',
    'Connected Devices Count', 'CPU Usage (%)', 'Memory Usage (%)',
    'Temperature (°C)', 'Uptime (hours)'
]

X = data[features]
y = error_codes_encoded

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
multi_target_rf = MultiOutputClassifier(rf_classifier, n_jobs=-1)
multi_target_rf.fit(X_train, y_train)

# Make predictions
y_pred = multi_target_rf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Print classification report for each Error Code
for i, error_code in enumerate(mlb.classes_):
    print(f"\nClassification Report for {error_code}:")
    print(classification_report(y_test[:, i], y_pred[:, i], target_names=['Not Present', 'Present']))

 


# Save the model and related objects
joblib.dump(multi_target_rf, 'bbRouter_error_code_prediction_model.pkl')
joblib.dump(mlb, 'error_code_multilabelbinarizer.pkl')
joblib.dump(features, 'bbRouter_model_features.pkl')

# Load the model and related objects
loaded_model = joblib.load('bbRouter_error_code_prediction_model.pkl')
loaded_mlb = joblib.load('error_code_multilabelbinarizer.pkl')
loaded_features = joblib.load('bbRouter_model_features.pkl')

# Example input (adjust values as needed)
example_input = pd.DataFrame([[
   0.5,   # Downstream Power (dBmV)
    45,    # Upstream Power (dBmV)
    40,    # Downstream SNR (dB)
    35,    # Upstream SNR (dB)
    270,   # Downstream Frequency (MHz)
    39,    # Upstream Frequency (MHz)
    1.5,   # Packet Loss (%)
    30,    # Latency (ms)
    5,     # Jitter (ms)
    6,     # WiFi 2.4GHz Channel
    36,    # WiFi 5GHz Channel
    5,     # Connected Devices Count
    50,    # CPU Usage (%)
    60,    # Memory Usage (%)
    45,    # Temperature (°C)
    720    # Uptime (hours)
]], columns=loaded_features)

# Predict Error codes probabilities
predicted_proba = loaded_model.predict_proba(example_input)

# Set a lower threshold for positive prediction (e.g., 0.3)
threshold = 0.3

# Get Error codes with probabilities above the threshold
predicted_error_codes = []
for i, class_probas in enumerate(predicted_proba):
    for j, proba in enumerate(class_probas[0]):
        if proba > threshold:
            error_code = loaded_mlb.classes_[j]
            predicted_error_codes.append((error_code, proba))

# Sort predicted Error codes by probability
predicted_error_codes.sort(key=lambda x: x[1], reverse=True)

if predicted_error_codes:
    print("Predicted Error codes (code, probability):")
    for error_code, prob in predicted_error_codes:
        print(f"{error_code}: {prob:.4f}")
else:
    print("No Error codes predicted above the threshold.")

# Print all probabilities for debugging
print("\nAll Error Code probabilities:")
for i, error_code in enumerate(loaded_mlb.classes_):
    print(f"{error_code}: {predicted_proba[i][0][1]:.4f}")