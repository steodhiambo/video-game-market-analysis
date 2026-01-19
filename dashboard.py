import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Load the dataset
df = pd.read_csv('vgsales.csv')

# Clean the data
df_clean = df.dropna()

# Create an interactive dashboard
pio.renderers.default = "browser"  # This will open plots in browser

# Create subplots for the dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales by Genre: NA vs JP', 'Platform Lifecycle Trends', 
                    'Top Publishers by Hit Rate', 'Genre-Platform Performance'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# 1. Genre comparison: NA vs JP
genre_na_sales = df_clean.groupby('Genre')['NA_Sales'].sum().sort_values(ascending=False)
genre_jp_sales = df_clean.groupby('Genre')['JP_Sales'].sum().sort_values(ascending=False)

# Since we can't directly compare these on the same subplot, we'll create a combined dataframe
genres = set(genre_na_sales.index).union(set(genre_jp_sales.index))
combined_genre_data = pd.DataFrame({
    'Genre': list(genres),
    'NA_Sales': [genre_na_sales.get(g, 0) for g in genres],
    'JP_Sales': [genre_jp_sales.get(g, 0) for g in genres]
}).sort_values('NA_Sales', ascending=False)

# Add bar charts to the first subplot
fig.add_trace(
    go.Bar(name='NA Sales', x=combined_genre_data['Genre'], y=combined_genre_data['NA_Sales'],
           showlegend=True, legendgroup='NA', marker_color='blue', opacity=0.6),
    row=1, col=1
)

fig.add_trace(
    go.Bar(name='JP Sales', x=combined_genre_data['Genre'], y=combined_genre_data['JP_Sales'],
           showlegend=True, legendgroup='JP', marker_color='red', opacity=0.6),
    row=1, col=1
)

# 2. Platform lifecycle trends (PS3 vs PS4)
platform_year_sales = df_clean.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()

ps3_sales = platform_year_sales[platform_year_sales['Platform'] == 'PS3']
ps4_sales = platform_year_sales[platform_year_sales['Platform'] == 'PS4']

fig.add_trace(
    go.Scatter(x=ps3_sales['Year'], y=ps3_sales['Global_Sales'], 
               mode='lines+markers', name='PS3', line=dict(color='green')),
    row=1, col=2
)

fig.add_trace(
    go.Scatter(x=ps4_sales['Year'], y=ps4_sales['Global_Sales'], 
               mode='lines+markers', name='PS4', line=dict(color='orange')),
    row=1, col=2
)

# 3. Top publishers by hit rate
publisher_stats = df_clean.groupby('Publisher').agg({
    'Global_Sales': ['mean', 'sum', 'count']
}).round(2)
publisher_stats.columns = ['Avg_Sales_Per_Game', 'Total_Sales', 'Game_Count']
publisher_stats_filtered = publisher_stats[publisher_stats['Game_Count'] >= 10].sort_values(
    'Avg_Sales_Per_Game', ascending=False
).head(10)

fig.add_trace(
    go.Bar(x=publisher_stats_filtered.index, y=publisher_stats_filtered['Avg_Sales_Per_Game'],
           name='Avg Sales Per Game', marker_color='purple'),
    row=2, col=1
)

# 4. Top genre-platform combinations
genre_platform_sales = df_clean.groupby(['Genre', 'Platform']).agg({
    'Global_Sales': ['mean', 'sum', 'count']
}).round(2)
genre_platform_sales.columns = ['Avg_Sales', 'Total_Sales', 'Game_Count']
genre_platform_sales = genre_platform_sales.reset_index()
significant_combinations = genre_platform_sales[genre_platform_sales['Game_Count'] >= 5].sort_values(
    'Avg_Sales', ascending=False
).head(10)

fig.add_trace(
    go.Bar(x=[f"{row['Genre']}-{row['Platform']}" for _, row in significant_combinations.iterrows()], 
           y=significant_combinations['Avg_Sales'],
           name='Genre-Platform Avg Sales', marker_color='teal'),
    row=2, col=2
)

# Update layout
fig.update_layout(height=800, title_text="Video Game Market Analysis Dashboard", 
                  showlegend=True)

# Show the dashboard
fig.show()

# Also create individual interactive visualizations
# 1. Interactive genre comparison
fig_genre = px.bar(combined_genre_data.melt(id_vars=['Genre'], 
                                            value_vars=['NA_Sales', 'JP_Sales'],
                                            var_name='Region', value_name='Sales'),
                   x='Genre', y='Sales', color='Region',
                   title='Video Game Sales by Genre: North America vs Japan',
                   barmode='group',
                   height=600)
fig_genre.show()

# 2. Interactive platform lifecycle
platform_trends = platform_year_sales[
    platform_year_sales['Platform'].isin(['PS3', 'PS4', 'X360', 'XB', 'DS', '3DS'])
]
fig_platform = px.line(platform_trends, x='Year', y='Global_Sales', color='Platform',
                       title='Platform Lifecycle Analysis',
                       markers=True,
                       height=600)
fig_platform.show()

# 3. Interactive publisher hit rates
fig_publisher = px.bar(publisher_stats_filtered.reset_index(), 
                       x='Publisher', y='Avg_Sales_Per_Game',
                       title='Top Publishers by Hit Rate (Average Sales per Game)',
                       height=600)
fig_publisher.show()

# 4. Interactive genre-platform combinations
fig_combo = px.bar(significant_combinations.head(15), 
                   x='Genre', y='Avg_Sales', color='Platform',
                   title='Top Genre-Platform Combinations by Average Sales',
                   height=600)
fig_combo.show()

print("Interactive dashboard and visualizations created successfully!")