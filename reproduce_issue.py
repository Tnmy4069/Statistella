import pandas as pd
import plotly.express as px
import plotly
import json
from data_processor import load_data

data = load_data()
games = data['games']
season_stats = games.groupby('SEASON')[['PTS_home', 'PTS_away']].mean().reset_index()

print("Season Stats Head:")
print(season_stats.head())
print("Dtypes:")
print(season_stats.dtypes)

try:
    # Create Stacked Area Chart
    fig = px.area(season_stats, x='SEASON', y=['PTS_home', 'PTS_away'], 
                  title='Average Points per Game per Season (Home vs Away)',
                  labels={'value': 'Points', 'variable': 'Type'},
                  color_discrete_map={'PTS_home': '#ef4444', 'PTS_away': '#3b82f6'})
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print("Graph JSON generated successfully.")
except Exception as e:
    print(f"Error generating graph: {e}")
