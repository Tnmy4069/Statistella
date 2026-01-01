import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Loads the NBA datasets from CSV files.
    Returns a dictionary containing pandas DataFrames.
    """
    try:
        teams = pd.read_csv('teams.csv')
        players = pd.read_csv('players.csv')
        ranking = pd.read_csv('ranking.csv')
        games = pd.read_csv('games.csv')
        games_details = pd.read_csv('games_details.csv')
        
        return {
            'teams': teams,
            'players': players,
            'ranking': ranking,
            'games': games,
            'games_details': games_details
        }
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}. Please ensure CSV files are in the root directory.")
        return None

def clean_data(data):
    """
    Performs basic data cleaning and preprocessing.
    """
    if not data:
        return None
    
    games = data['games']
    
    # Convert date columns to datetime
    if 'GAME_DATE_EST' in games.columns:
        games['GAME_DATE_EST'] = pd.to_datetime(games['GAME_DATE_EST'])
    
    # Sort games by date
    games = games.sort_values('GAME_DATE_EST')
    
    data['games'] = games
    
    return data

def get_team_stats(games_df, ranking_df, teams_df):
    """
    Aggregates team statistics.
    """
    # This is a placeholder for more complex aggregation logic
    # For now, we'll just return the raw dataframes or simple merges
    return games_df

def get_player_stats(games_details_df, players_df):
    """
    Aggregates player statistics.
    """
    # Placeholder
    return games_details_df
