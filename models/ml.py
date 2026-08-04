import pandas as pd

import time

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (accuracy_score, confusion_matrix , classification_report)

data = pd.read_csv("../data/cicids2017_cleaned.csv")

#print(data.head())

print(data.shape)

#print(data.columns)

#print(data.info())

X = data.drop("Attack Type", axis=1)

y = data["Attack Type"]

print(X.head())

print(y.head())

print("Features Shape :", X.shape)

print("Target Shape   :", y.shape)

sample = data.sample(n=100000, random_state=42)

X = sample.drop("Attack Type", axis=1)
y = sample["Attack Type"]

print("\nAttack Types:")

print(y.unique())

start = time.time()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

end = time.time()

print("Model trained successfully!")
print(f"Training Time: {end-start:.2f} seconds")

print("Training Features :", X_train.shape)
print("Testing Features  :", X_test.shape)

print("Training Labels   :", y_train.shape)
print("Testing Labels    :", y_test.shape)

model = RandomForestClassifier(n_estimators=20,random_state=42,n_jobs=-1)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy*100:.2f}%")

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("First 10 Predictions:")
print(y_pred[:10])

print("Model trained successfully!")

print(X.dtypes.unique())