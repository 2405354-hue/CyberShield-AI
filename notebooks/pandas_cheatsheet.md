# 🐼 Pandas Cheat Sheet

### 🛡️ CyberShield AI — Data Analysis Reference

> Quick reference for the Pandas commands used while working with the CyberShield AI dataset.

---

## 📥 1. Import Pandas

```python
import pandas as pd
```

**What it does:**  
Imports the Pandas library.

**Why we use it:**  
Pandas is used for loading, cleaning, analyzing, and manipulating tabular data.

---

## 📂 2. Load a Dataset

### `pd.read_csv()`

```python
df = pd.read_csv("file.csv")
```

**What it does:**  
Loads a CSV file into a Pandas DataFrame.

**Why we use it:**  
Allows us to work with CSV data as a table.

**CyberShield example:**

```python
df = pd.read_csv("Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
```

---

## 👀 3. View the Dataset

### `df.head()`

```python
df.head()
```

**What it does:**  
Shows the first 5 rows.

**Why we use it:**  
Quickly checks what the dataset looks like.

### Show a specific number of rows

```python
df.head(10)
```

Shows the first 10 rows.

### `df.tail()`

```python
df.tail()
```

**What it does:**  
Shows the last 5 rows.

```python
df.tail(10)
```

Shows the last 10 rows.

### `df.sample()`

```python
df.sample(5)
```

**What it does:**  
Shows 5 random rows.

**Why we use it:**  
Useful for checking random parts of a large dataset.

---

## 📏 4. Dataset Size

### `df.shape`

```python
df.shape
```

**What it does:**  
Returns the number of rows and columns.

**Format:**

```text
(rows, columns)
```

**Example:**

```text
(225745, 79)
```

**Meaning:**

| Value | Meaning |
|---:|---|
| 225745 | Number of rows |
| 79 | Number of columns |

> ⭐ `shape` is an attribute, so **do not use `()`**.
>
> ✅ `df.shape`  
> ❌ `df.shape()`

---

## 🏷️ 5. Column Names

### `df.columns`

```python
df.columns
```

**What it does:**  
Shows all column names.

**CyberShield examples:**

```text
Destination Port
Flow Duration
Total Fwd Packets
Total Backward Packets
Total Length of Fwd Packets
Total Length of Bwd Packets
Flow Bytes/s
Label
```

### `df.columns.tolist()`

```python
df.columns.tolist()
```

**What it does:**  
Converts the column names into a normal Python list.

**Why we use it:**  
Makes column names easier to work with in Python.

---

## 🔢 6. Data Types

### `df.dtypes`

```python
df.dtypes
```

**What it does:**  
Shows the data type of every column.

| Type | Meaning |
|---|---|
| `int64` | Integer number |
| `float64` | Decimal number |
| `object` | Text/String |
| `bool` | True/False |

**Why it matters for Machine Learning:**  
Most ML features need to be numerical.

### Count data types

```python
df.dtypes.value_counts()
```

**What it does:**  
Counts how many columns belong to each data type.

---

## ℹ️ 7. Dataset Information

### `df.info()`

```python
df.info()
```

**What it does:**  
Provides an overall summary of the DataFrame.

**Shows:**

- Number of rows
- Column names
- Non-null values
- Data types
- Memory usage

**Why we use it:**  
It gives a quick overview of the structure and quality of the dataset.

---

## 📊 8. Statistical Summary

### `df.describe()`

```python
df.describe()
```

**What it does:**  
Provides statistical information about numerical columns.

| Value | Meaning |
|---|---|
| `count` | Number of values |
| `mean` | Average |
| `std` | Standard deviation |
| `min` | Minimum |
| `25%` | First quartile |
| `50%` | Median |
| `75%` | Third quartile |
| `max` | Maximum |

---

## 🎯 9. Selecting Columns

### One column

```python
df["Label"]
```

**What it does:**  
Selects one column.

**Result:**  
A Pandas Series.

### Multiple columns

```python
df[
    [
        "Label",
        "Flow Duration",
        "Total Fwd Packets"
    ]
]
```

**What it does:**  
Selects multiple columns.

**Result:**  
A Pandas DataFrame.

---

## 🏷️ 10. Counting Values

### `value_counts()`

```python
df["Label"].value_counts()
```

**What it does:**  
Counts how many times each value appears.

**CyberShield use:**  
Counts different traffic or attack types.

**Example:**

```text
DDoS      128027
BENIGN     97718
```

This tells us how many records belong to each class.

### Percentage of each value

```python
df["Label"].value_counts(normalize=True) * 100
```

**What it does:**  
Calculates the percentage of each category.

**How it works:**

```text
normalize=True
      ↓
Converts counts to proportions
      ↓
× 100
      ↓
Percentage
```

---

## 🔍 11. Unique Values

### `unique()`

```python
df["Label"].unique()
```

**What it does:**  
Shows all different values in a column.

**Example:**

```text
['BENIGN' 'DDoS']
```

### `nunique()`

```python
df["Label"].nunique()
```

**What it does:**  
Counts the number of unique values.

**Example:**

```text
2
```

---

## 🧹 12. Missing Values

Missing values are important during Machine Learning preprocessing.

### `isnull()`

```python
df.isnull()
```

**What it does:**  
Checks whether values are missing.

```text
True  → Missing
False → Present
```

### Count missing values

```python
df.isnull().sum()
```

**What it does:**  
Counts missing values in every column.

### Count all missing values

```python
df.isnull().sum().sum()
```

**What it does:**  
Returns the total number of missing cells in the entire dataset.

### Check one column

```python
df["Flow Bytes/s"].isnull().sum()
```

**What it does:**  
Counts missing values specifically in `Flow Bytes/s`.

### Find rows containing missing values

```python
df[df.isnull().any(axis=1)]
```

**What it does:**  
Returns rows that contain at least one missing value.

---

## 📈 13. Basic Statistics

### `mean()`

```python
df["Flow Duration"].mean()
```

**What it does:**  
Calculates the average.

**Formula:**

```text
Mean = Sum of values / Number of values
```

### `median()`

```python
df["Flow Duration"].median()
```

**What it does:**  
Finds the middle value.

**Why it is useful:**  
Median is less affected by extreme values or outliers than the mean.

### `min()`

```python
df["Flow Duration"].min()
```

**What it does:**  
Finds the smallest value.

### `max()`

```python
df["Flow Duration"].max()
```

**What it does:**  
Finds the largest value.

### `std()`

```python
df["Flow Duration"].std()
```

**What it does:**  
Measures how spread out the values are.

```text
High standard deviation
→ Values are more spread out

Low standard deviation
→ Values are closer together
```

---

## 🔗 14. Grouping Data

### `groupby()`

```python
df.groupby("Label")
```

**What it does:**  
Divides the dataset into groups based on a column.

**CyberShield use:**

```text
Dataset
   ↓
groupby("Label")
   ↓
┌──────────┐
│  BENIGN  │
└──────────┘

┌──────────┐
│   DDoS   │
└──────────┘
```

**Why we use it:**  
To compare normal and malicious traffic.

### GroupBy + Mean

```python
df.groupby("Label")["Flow Duration"].mean()
```

**What it does:**  
Calculates the average Flow Duration separately for each label.

### GroupBy + Median

```python
df.groupby("Label")["Flow Duration"].median()
```

**What it does:**  
Calculates the median Flow Duration separately for each label.

### GroupBy + Multiple Features

```python
df.groupby("Label")[
    [
        "Flow Duration",
        "Total Fwd Packets",
        "Total Backward Packets"
    ]
].median()
```

**What it does:**  
Calculates median values for multiple features for each traffic type.

---

## 🔎 15. Filtering Data

### Select DDoS traffic

```python
df[df["Label"] == "DDoS"]
```

**What it does:**  
Returns only rows where the Label is `DDoS`.

### Select BENIGN traffic

```python
df[df["Label"] == "BENIGN"]
```

### Multiple conditions — AND

```python
df[
    (df["Label"] == "DDoS") &
    (df["Flow Duration"] > 1000000)
]
```

**Meaning:**

```text
Label must be DDoS
AND
Flow Duration must be > 1000000
```

### Multiple conditions — OR

```python
df[
    (df["Label"] == "DDoS") |
    (df["Label"] == "BENIGN")
]
```

**Meaning:**

```text
Label can be DDoS
OR
Label can be BENIGN
```

### Operators

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |
| `&` | AND |
| `|` | OR |

---

## ↕️ 16. Sorting Data

### Ascending

```python
df.sort_values("Flow Duration")
```

**What it does:**  
Sorts from smallest → largest.

### Descending

```python
df.sort_values(
    "Flow Duration",
    ascending=False
)
```

**What it does:**  
Sorts from largest → smallest.

---

## 🗑️ 17. Removing Columns

### Remove one column

```python
df.drop("ColumnName", axis=1)
```

**What it does:**  
Removes a column.

### Remove multiple columns

```python
df.drop(
    ["Column1", "Column2"],
    axis=1
)
```

### Important

```text
axis=1 → Columns
axis=0 → Rows
```

---

## 🧹 18. Handling Missing Values

### `dropna()`

```python
df.dropna()
```

**What it does:**  
Removes rows containing missing values.

⚠️ **CyberShield note:**  
Do not blindly use `dropna()`. We need to understand the missing data before deciding what to do.

### `fillna()`

```python
df["Column"].fillna(0)
```

**What it does:**  
Replaces missing values with `0`.

### Fill with Median

```python
df["Column"].fillna(
    df["Column"].median()
)
```

**What it does:**  
Replaces missing values with the column's median.

---

## 🔄 19. Duplicate Data

### Check duplicates

```python
df.duplicated().sum()
```

**What it does:**  
Counts duplicate rows.

### Remove duplicates

```python
df.drop_duplicates()
```

**What it does:**  
Removes duplicate rows.

---

## 🧽 20. Cleaning Column Names

### `str.strip()`

```python
df.columns = df.columns.str.strip()
```

**What it does:**  
Removes unwanted spaces from the beginning and end of column names.

**Example:**

```text
" Flow Duration "
```

becomes:

```text
"Flow Duration"
```

This was useful with our CICIDS2017 dataset.

---

## ✏️ 21. Rename Columns

```python
df.rename(
    columns={
        "old_name": "new_name"
    },
    inplace=True
)
```

**What it does:**  
Changes a column name.

---

# 🧠 Pandas Command Summary

| Command | What it does |
|---|---|
| `pd.read_csv()` | Load CSV |
| `df.head()` | First 5 rows |
| `df.tail()` | Last 5 rows |
| `df.sample()` | Random rows |
| `df.shape` | Rows and columns |
| `df.columns` | Column names |
| `df.dtypes` | Data types |
| `df.info()` | Dataset information |
| `df.describe()` | Statistical summary |
| `df["column"]` | Select column |
| `value_counts()` | Count values |
| `unique()` | Show unique values |
| `nunique()` | Count unique values |
| `isnull()` | Detect missing values |
| `mean()` | Average |
| `median()` | Middle value |
| `min()` | Minimum |
| `max()` | Maximum |
| `std()` | Standard deviation |
| `groupby()` | Group data |
| `sort_values()` | Sort data |
| `drop()` | Remove rows/columns |
| `dropna()` | Remove missing rows |
| `fillna()` | Fill missing values |
| `duplicated()` | Find duplicates |
| `drop_duplicates()` | Remove duplicates |
| `rename()` | Rename columns |

---

