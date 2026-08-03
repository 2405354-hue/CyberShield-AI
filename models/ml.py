import pandas as pd

from sklearn.model_selection import train_test_split

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

print("\nAttack Types:")

print(y.unique())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Features :", X_train.shape)
print("Testing Features  :", X_test.shape)

print("Training Labels   :", y_train.shape)
print("Testing Labels    :", y_test.shape)