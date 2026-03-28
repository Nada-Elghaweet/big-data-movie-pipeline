import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("data_preprocessed.csv")


"""
# Histogram

Score : shows which movie scores are common.
Gross : shows most movies earn low/mid/high revenue.
Votes : shows popularity distribution.
"""

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].hist(df['score'], bins=20, color='skyblue', edgecolor='black')
axes[0].set_title("Distribution of Movie Scores")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Number of Movies")

axes[1].hist(df['gross'], bins=20, color='lightgreen', edgecolor='black')
axes[1].set_title("Distribution of Movie Gross Revenue")
axes[1].set_xlabel("Gross ($)")
axes[1].set_ylabel("Number of Movies")

axes[2].hist(df['votes'], bins=20, color='salmon', edgecolor='black')
axes[2].set_title("Distribution of Movie Votes")
axes[2].set_xlabel("Votes")
axes[2].set_ylabel("Number of Movies")

plt.tight_layout()
plt.savefig("summary_histograms.png")
plt.show()


"""
# Pairplot and Scatterplots

Exploring Relationships Between Movie Score, Votes, and Gross
"""

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

sns.scatterplot(x='votes', y='score', data=df, color='blue', ax=axes[0])
axes[0].set_title('Score vs Votes')
axes[0].set_xlim(0, 12.5)

sns.scatterplot(x='gross', y='score', data=df, color='red', ax=axes[1])
axes[1].set_title('Score vs Gross')
axes[1].set_xlim(0, 15)

plt.tight_layout()
plt.savefig("summary_scatter.png")
plt.show()

df_pair = df[['score', 'votes', 'gross']]
g = sns.pairplot(df_pair, height=4, aspect=1.2)

plt.show()
g.savefig("summary_pairplot.png")



"""
# Correlation Heatmap

Shows how numeric movie features relate to each other,
giving insight into what factors might affect popularity and revenue.
"""

cols_for_corr = ['score', 'votes', 'gross', 'budget', 'runtime']
corr = df[cols_for_corr].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap: Score, Votes, Gross, Budget, Runtime")
plt.savefig("summary_heatmap.png")
plt.show()