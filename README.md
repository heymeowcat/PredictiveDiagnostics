# Broadband Router Diagnostic Predictor

This repository contains code for generating synthetic broadband router diagnostic data and a machine learning model to predict error codes based on router parameters.

## Contents

1.  [Data Generator](#data-generator)

2.  [Prediction Model](#prediction-model)

3.  [Usage](#usage)

4.  [File Descriptions](#file-descriptions)

5.  [Requirements](#requirements)

## Data Generator

The `bbRouter_data_generator.py` script creates a synthetic dataset that simulates diagnostic data from broadband routers. It generates multiple diagnostic entries per device over a specified time range.

Key features:

- Generates realistic broadband router parameters
- Creates multiple diagnostic entries per device
- Assigns random ErrorCodes to each diagnostic entry

## Prediction Model

The `bbRouter_error_predictor.py` script trains a machine learning model to predict ErrorCodes based on router diagnostic parameters.

Key features:

- Uses Random Forest Classifier with Multi-Output Classification

- Predicts multiple ErrorCodes for a given set of router parameters

- Provides probability scores for each ErrorCode prediction

## Usage

Generate synthetic data:

    python bbRouter_data_generator.py

This will create a CSV file named `bbRouter_diagnostics_data.csv`

Train the prediction model and make predictions::

    python bbRouter_error_code_predictor.py

This will train the model, save it, and provide an example prediction.

## File Descriptions

- `bbRouter_data_generator.py`: Script to generate synthetic broadband router diagnostic data

- `bbRouter_error_predictor.py`: Script to train the error prediction model and make predictions

- `bbRouter_diagnostics_data.csv`: Generated synthetic dataset (created by data generator)

- `bbRouter_error_code_prediction_model.pkl`: Trained model file (created by error predictor)

- `error_code_multilabelbinarizer.pkl`: MultiLabelBinarizer for ErrorCodes (created by error predictor)

- `bbRouter_model_features.pkl`: List of features used in the model (created by error predictor)

## Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- joblib

Install the required packages using:

    pip install pandas numpy scikit-learn joblib
