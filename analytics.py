import sys
import pandas as pd

input_path = sys.argv[1]

df = pd.read_csv(input_path)
df.head()


# Insight 1: what are the 3 top genres ?
genre_mean = df.groupby('genre')['score'].mean()
top3_genres = genre_mean.sort_values(ascending=False).head(3)

insight1 = "Insight 1: Top 3 genres by average score:\n"
insight1 += f"1. {top3_genres.index[0]}: {top3_genres.iloc[0]:.2f}\n"
insight1 += f"2. {top3_genres.index[1]}: {top3_genres.iloc[1]:.2f}\n"
insight1 += f"3. {top3_genres.index[2]}: {top3_genres.iloc[2]:.2f}\n"

print(insight1)

with open("insight1.txt", "w") as f:
    f.write(insight1)


# Insight 2 : What is the country with highest average movie score?
country_mean = df.groupby('release_country')['score'].mean()
best_country = country_mean.idxmax()
best_score = country_mean.max()

insight2 = f"Insight 2: Movies from {best_country} have the highest average score of {best_score:.2f}."
print(insight2)

with open("insight2.txt", "w") as f:
    f.write(insight2)


# Insight 3: Which rating has the highest average gross revenue?
rating_mean = df.groupby('rating')['gross'].mean()
top_rating_name = rating_mean.sort_values(ascending=False).index[0]
top_rating_gross = rating_mean.sort_values(ascending=False).iloc[0]

insight3 = f"Insight 3: Movies with rating '{top_rating_name}' have the highest average gross revenue of ${top_rating_gross:,.0f}."
print(insight3)

with open("insight3.txt", "w") as f:
    f.write(insight3)


import subprocess
subprocess.run(["python", "visualize.py", input_path])