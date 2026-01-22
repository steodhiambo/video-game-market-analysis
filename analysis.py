import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration
MIN_GAMES_PUBLISHER = 10  # Minimum games for publisher analysis
MIN_GAMES_COMBINATION = 5  # Minimum games for genre-platform combinations
FIGURE_SIZE = (12, 8)
FIGURE_SIZE_LARGE = (14, 8)

# Load the dataset
try:
    df = pd.read_csv('vgsales.csv')
except FileNotFoundError:
    print("Error: vgsales.csv not found. Please ensure the dataset is in the current directory.")
    print("You can download it from: https://www.kaggle.com/gregorut/videogamesales")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty or corrupted.")
    exit(1)
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit(1)

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

# Clean the data - handle missing values more intelligently
print(f"\nMissing values before cleaning: {df.isnull().sum().sum()}")

# Only drop rows where critical columns are missing
critical_columns = ['Name', 'Genre', 'Platform', 'Global_Sales']
df_clean = df.dropna(subset=critical_columns)

# Fill missing Year values with median year for the platform
df_clean['Year'] = df_clean.groupby('Platform')['Year'].transform(
    lambda x: x.fillna(x.median())
)

print(f"Shape after intelligent cleaning: {df_clean.shape}")
print(f"Rows preserved: {len(df_clean)/len(df)*100:.1f}%")

# TASK 1: Compare genre preferences in Japan vs North America
print("\n=== ANALYZING GENRE PREFERENCES IN JAPAN VS NORTH AMERICA ===")

# Calculate total sales by genre for each region
genre_na_sales = df_clean.groupby('Genre')['NA_Sales'].sum().sort_values(ascending=False)
genre_jp_sales = df_clean.groupby('Genre')['JP_Sales'].sum().sort_values(ascending=False)

print("Top genres by NA Sales:")
print(genre_na_sales.head(10))

print("\nTop genres by JP Sales:")
print(genre_jp_sales.head(10))

# Create comparison visualization with improved styling
fig, ax = plt.subplots(figsize=FIGURE_SIZE)
x = np.arange(len(genre_na_sales.index))
width = 0.35

# Use better colors and styling
colors = ['#2E86AB', '#A23B72']
bars1 = ax.bar(x - width/2, genre_na_sales.values, width, 
               label='North America', alpha=0.8, color=colors[0])
bars2 = ax.bar(x + width/2, genre_jp_sales.values, width, 
               label='Japan', alpha=0.8, color=colors[1])

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{height:.0f}M', ha='center', va='bottom', fontsize=8)
            
for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{height:.0f}M', ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Genre', fontsize=12)
ax.set_ylabel('Total Sales (Millions)', fontsize=12)
ax.set_title('Video Game Sales by Genre: North America vs Japan', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(genre_na_sales.index, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('genre_comparison.png', dpi=300, bbox_inches='tight')
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

# Visualize platform lifecycles with improved styling
plt.figure(figsize=FIGURE_SIZE)

# Select major platforms for cleaner visualization
major_platforms = ['PS3', 'PS4', 'X360', 'XOne', 'DS', '3DS', 'Wii', 'WiiU']
platform_data = platform_year_sales[
    platform_year_sales['Platform'].isin(major_platforms)
]

sns.lineplot(data=platform_data, x='Year', y='Global_Sales', 
             hue='Platform', marker='o', linewidth=2.5, markersize=6)
plt.title('Platform Lifecycle Analysis - Major Consoles', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Global Sales (Millions)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('platform_lifecycle.png', dpi=300, bbox_inches='tight')
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
publisher_stats_filtered = publisher_stats[
    publisher_stats['Game_Count'] >= MIN_GAMES_PUBLISHER
].sort_values('Avg_Sales_Per_Game', ascending=False)

print(f"Top publishers by average sales per game (with {MIN_GAMES_PUBLISHER}+ games):")
print(publisher_stats_filtered.head(10))

# Add additional analysis - success rate (games > 1M sales)
publisher_success = df_clean.groupby('Publisher').agg({
    'Global_Sales': lambda x: (x > 1.0).sum() / len(x) * 100  # % of games > 1M sales
}).round(1)
publisher_success.columns = ['Success_Rate_Percent']

# Merge with existing stats
publisher_complete = publisher_stats_filtered.merge(
    publisher_success, left_index=True, right_index=True
).sort_values('Avg_Sales_Per_Game', ascending=False)

print("\nPublisher performance with success rates:")
print(publisher_complete.head(10))

# TASK 4: Identify top performing genre/platform combinations
print("\n=== IDENTIFYING TOP GENRE/PLATFORM COMBINATIONS ===")

# Calculate average sales for each genre-platform combination
genre_platform_sales = df_clean.groupby(['Genre', 'Platform']).agg({
    'Global_Sales': ['mean', 'sum', 'count']
}).round(2)

genre_platform_sales.columns = ['Avg_Sales', 'Total_Sales', 'Game_Count']
genre_platform_sales = genre_platform_sales.reset_index()

# Filter for combinations with at least 5 games to ensure statistical significance
significant_combinations = genre_platform_sales[
    genre_platform_sales['Game_Count'] >= MIN_GAMES_COMBINATION
].sort_values('Avg_Sales', ascending=False)

print(f"Top genre/platform combinations by average sales (with {MIN_GAMES_COMBINATION}+ games):")
print(significant_combinations.head(10))

# Create visualization for top combinations with improved styling
top_combinations = significant_combinations.head(15)
plt.figure(figsize=FIGURE_SIZE_LARGE)

# Create color gradient for bars
colors = plt.cm.viridis(np.linspace(0, 1, len(top_combinations)))
bars = plt.bar(range(len(top_combinations)), top_combinations['Avg_Sales'], color=colors)

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
             f'{height:.2f}M', ha='center', va='bottom', fontsize=9)

plt.xlabel('Genre-Platform Combination', fontsize=12)
plt.ylabel('Average Global Sales (Millions)', fontsize=12)
plt.title('Top Genre-Platform Combinations by Average Sales', fontsize=14, fontweight='bold')
plt.xticks(range(len(top_combinations)), 
           [f"{row['Genre']}-{row['Platform']}" for _, row in top_combinations.iterrows()], 
           rotation=45, ha="right", fontsize=10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('top_combinations.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print("Generated visualizations:")
print("• genre_comparison.png - Regional genre preferences")
print("• platform_lifecycle.png - Platform performance over time")
print("• top_combinations.png - Best genre-platform combinations")
print("\nKey insights saved to PNG files with high resolution (300 DPI)")
print("Ready for presentation and strategic decision making!")