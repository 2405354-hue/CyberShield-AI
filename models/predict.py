import joblib

import pandas as pd

model = joblib.load("cybershield_model.pkl")

data = pd.read_csv("../data/cicids2017_cleaned.csv")

X = data.drop("Attack Type", axis=1)

print("Model loaded successfully!")

print("\nModel expects:", model.n_features_in_, "features")

print("\nTraining feature count:", X.shape[1])

print("\nTraining feature names:")

for i, column in enumerate(X.columns, start=1):

    print(i, ":", column)