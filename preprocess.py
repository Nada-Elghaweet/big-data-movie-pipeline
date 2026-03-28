import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

df = pd.read_csv("data_raw.csv")

print("Dataset shape:", df.shape)

df.head()
df.info()


# Data Cleaning

# solving year vs released redunduncy
df['release_date'] = df['released'].str.split('(').str[0].str.strip()
df['release_country'] = df['released'].str.split('(').str[1].str.replace(')', '').str.strip()

df.drop(columns=['released', 'year'], inplace=True)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')


# Filling null values
print("Missing values per column:\n", df.isnull().sum())

for col in ['rating', 'writer', 'star', 'company', 'release_country', 'release_date']:
    mode_val = df[col].mode()[0]
    df[col] = df[col].fillna(mode_val)
    print(f"Filled missing values in '{col}' with mode: {mode_val}")

median_gross = df['gross'].median()
df['gross'] = df['gross'].fillna(median_gross)
print(f"Filled missing values in 'gross' with median: {median_gross}")


# Filling or dropping duplicates
# df.duplicated().sum() there was none


# Feature Transformation

# encoding categorical coloumns using label encoder
categorical_cols = ['rating', 'genre', 'country', 'director', 'writer', 'star', 'company', 'release_country']
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"Encoded column '{col}'")


# converting runtime,, into float , trimimg commas renaming it to runtime
df['runtime'] = df['runtime,,'].str.replace(',', '').astype(float)
df = df.drop(columns=['runtime,,'])


# Scaling numerical coloumns
numerical_cols = ['budget', 'gross', 'score', 'votes', 'runtime']
scaler = StandardScaler()
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
print("\nScaled numerical columns:", numerical_cols)

df.head()


# Dimensionality Reduction

# select subset of columns and dropping irrelevent ones
selected_cols = ['rating', 'genre', 'score', 'votes', 'budget', 'gross', 'runtime', 'release_country', 'release_date']
df_reduced = df[selected_cols].copy()
# descretization of score into 3 equal bins
df_reduced['score_bin'] = pd.qcut(df_reduced['score'], q=3, labels=['Low', 'Medium', 'High'])
# encoding of score after descretization
score_bin_mapping = {"Low": 0, "Medium": 1, "High": 2}
df_reduced['score_bin'] = df_reduced['score_bin'].map(score_bin_mapping)

df_reduced

df_reduced.to_csv("data_preprocessed.csv", index=False)
print("Saved preprocessed data as data_preprocessed.csv")