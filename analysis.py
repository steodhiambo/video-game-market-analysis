import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
df = pd.read_csv('vgsales.csv')

# Display basic info about the dataset
print("Dataset shape:", df.shape)
print("\nDataset info:")
print(df.info())
print("\nFirst few rows:")
print(df.head())

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Check date range
print(f"\nDate range: {int(df['Year'].min())} to {int(df['Year'].max())}")

# Clean the data
df_clean = df.dropna()  # Remove rows with missing values
print(f"\nShape after cleaning: {df_clean.shape}")

# TASK 1: Compare genre preferences in Japan vs North America
print("\n=== ANALYZING GENRE PREFERENCES IN JAPAN VS NORTH AMERICA ===")

# Calculate total sales by genre for each region
genre_na_sales = df_clean.groupby('Genre')['NA_Sales'].sum().sort_values(ascending=False)
genre_jp_sales = df_clean.groupby('Genre')['JP_Sales'].sum().sort_values(ascending=False)

print("Top genres by NA Sales:")
print(genre_na_sales.head(10))

print("\nTop genres by JP Sales:")
print(genre_jp_sales.head(10))

# Create comparison visualization
fig, ax = plt.subplots(figsize=(12, 8))
x = np.arange(len(genre_na_sales.index))
width = 0.35

ax.bar(x - width/2, genre_na_sales.values, width, label='North America', alpha=0.8)
ax.bar(x + width/2, genre_jp_sales.values, width, label='Japan', alpha=0.8)

ax.set_xlabel('Genre')
ax.set_ylabel('Total Sales (Millions)')
ax.set_title('Video Game Sales by Genre: North America vs Japan')
ax.set_xticks(x)
ax.set_xticklabels(genre_na_sales.index, rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig('genre_comparison.png')
plt.show()

# TASK 2: Analyze platform lifecycles
print("\n=== ANALYZING PLATFORM LIFECYCLES ===")

# Group sales by year and platform to see trends
platform_year_sales = df_clean.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()

# Focus on specific platforms like PS3 and PS4
ps3_sales = platform_year_sales[platform_year_sales['Platform'] == 'PS3']
ps4_sales = platform_year_sales[platform_year_sales['Platform'] == 'PS4']

print("PS3 Sales by Year:")
print(ps3_sales.sort_values('Year'))
print("\nPS4 Sales by Year:")
print(ps4_sales.sort_values('Year'))

# Visualize platform lifecycles
plt.figure(figsize=(12, 8))
sns.lineplot(data=platform_year_sales[
    (platform_year_sales['Platform'].isin(['PS3', 'PS4', 'X360', 'XB', 'DS', '3DS']))
], x='Year', y='Global_Sales', hue='Platform', marker='o')
plt.title('Platform Lifecycle Analysis')
plt.xlabel('Year')
plt.ylabel('Global Sales (Millions)')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('platform_lifecycle.png')
plt.show()

# TASK 3: Calculate publisher hit rates
print("\n=== CALCULATING PUBLISHER HIT RATES ===")

# Calculate average sales per game for each publisher
publisher_stats = df_clean.groupby('Publisher').agg({
    'Global_Sales': ['mean', 'sum', 'count']
}).round(2)

# Rename columns for clarity
publisher_stats.columns = ['Avg_Sales_Per_Game', 'Total_Sales', 'Game_Count']

# Filter out publishers with very few games to get meaningful averages
publisher_stats_filtered = publisher_stats[publisher_stats['Game_Count'] >= 10].sort_values(
    'Avg_Sales_Per_Game', ascending=False
)

print("Top publishers by average sales per game (with 10+ games):")
print(publisher_stats_filtered.head(10))

# TASK 4: Identify top performing genre/platform combinations
print("\n=== IDENTIFYING TOP GENRE/PLATFORM COMBINATIONS ===")

# Calculate average sales for each genre-platform combination
genre_platform_sales = df_clean.groupby(['Genre', 'Platform']).agg({
    'Global_Sales': ['mean', 'sum', 'count']
}).round(2)

genre_platform_sales.columns = ['Avg_Sales', 'Total_Sales', 'Game_Count']
genre_platform_sales = genre_platform_sales.reset_index()

# Filter for combinations with at least 5 games to ensure statistical significance
significant_combinations = genre_platform_sales[genre_platform_sales['Game_Count'] >= 5].sort_values(
    'Avg_Sales', ascending=False
)

print("Top genre/platform combinations by average sales (with 5+ games):")
print(significant_combinations.head(10))

# Create visualization for top combinations
top_combinations = significant_combinations.head(15)
plt.figure(figsize=(14, 8))
bars = plt.bar(range(len(top_combinations)), top_combinations['Avg_Sales'])
plt.xlabel('Genre-Platform Combination')
plt.ylabel('Average Global Sales (Millions)')
plt.title('Top Genre-Platform Combinations by Average Sales')
plt.xticks(range(len(top_combinations)), 
           [f"{row['Genre']}-{row['Platform']}" for _, row in top_combinations.iterrows()], 
           rotation=45, ha="right")
plt.tight_layout()
plt.savefig('top_combinations.png')
plt.show()

print("\nAnalysis complete! Created visualizations saved as PNG files.")