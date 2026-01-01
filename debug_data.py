from data_processor import load_data, clean_data
import pandas as pd

print("Loading data...")
raw_data = load_data()
data = clean_data(raw_data)

if data:
    print("Data loaded successfully.")
    print("Games shape:", data['games'].shape)
    print("Teams shape:", data['teams'].shape)
    print("Players shape:", data['players'].shape)
    
    # Check for missing values or empty aggregations
    games = data['games']
    print("\nSample Games Data:")
    print(games[['SEASON', 'PTS_home', 'PTS_away']].head())
    
    season_stats = games.groupby('SEASON')[['PTS_home', 'PTS_away']].mean()
    print("\nSeason Stats (Head):")
    print(season_stats.head())
    
    if season_stats.empty:
        print("ERROR: Season stats is empty!")
else:
    print("ERROR: Failed to load data.")
