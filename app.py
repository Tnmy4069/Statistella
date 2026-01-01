from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import plotly
import plotly.express as px
from data_processor import load_data, clean_data

app = Flask(__name__)

# Load Data once at startup
raw_data = load_data()
data = clean_data(raw_data)

@app.route('/')
def index():
    try:
        # Trends: Avg Points per Game over Seasons
        games = data['games']
        season_stats = games.groupby('SEASON')[['PTS_home', 'PTS_away']].mean().reset_index()
        
        # Create Stacked Area Chart
        fig = px.area(season_stats, x='SEASON', y=['PTS_home', 'PTS_away'], 
                      title='Average Points per Game per Season (Home vs Away)',
                      labels={'value': 'Points', 'variable': 'Type'},
                      color_discrete_map={'PTS_home': '#ef4444', 'PTS_away': '#3b82f6'})
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Insights
        games['TOTAL_PTS'] = games['PTS_home'] + games['PTS_away']
        highest_scoring_game = games.loc[games['TOTAL_PTS'].idxmax()]
        hsg_text = f"{pd.to_datetime(highest_scoring_game['GAME_DATE_EST']).strftime('%Y-%m-%d')}: {int(highest_scoring_game['TOTAL_PTS'])} Pts"
        
        best_season = season_stats.loc[(season_stats['PTS_home'] + season_stats['PTS_away']).idxmax()]
        bss_text = f"{int(best_season['SEASON'])}: {int(best_season['PTS_home'] + best_season['PTS_away'])} PPG"
        
        insights = {
            'highest_scoring_game': hsg_text,
            'best_scoring_season': bss_text
        }
        
        # Prepare data for table
        season_data = season_stats.sort_values('SEASON', ascending=False).to_dict('records')
        
        return render_template('index.html', graphJSON=graphJSON, insights=insights, season_data=season_data)
    except Exception as e:
        print(f"Error in index route: {e}")
        return str(e), 500
    
    # Insights
    # 1. Highest Scoring Game
    games['TOTAL_PTS'] = games['PTS_home'] + games['PTS_away']
    highest_scoring_game = games.loc[games['TOTAL_PTS'].idxmax()]
    hsg_text = f"{highest_scoring_game['GAME_DATE_EST'].strftime('%Y-%m-%d')}: {highest_scoring_game['TOTAL_PTS']} Pts"
    
    # 2. Highest Avg Points Season
    best_season = season_stats.loc[season_stats['Avg_PTS'].idxmax()]
    best_season_text = f"{int(best_season['SEASON'])}: {best_season['Avg_PTS']:.1f} PPG"
    
    # 3. Best Team Record (approx from ranking)
    # We need to be careful with ranking data, let's just use games data for wins if possible, 
    # but ranking has W_PCT pre-calculated for standings.
    # Let's find the max W_PCT in final standings across all seasons.
    # This might be slow if we iterate all, so let's just pick a fun fact from games.
    # Most wins in a season?
    # Let's stick to the Highest Scoring Game and Best Season for now to keep it fast.
    
    insights = {
        'highest_scoring_game': hsg_text,
        'best_scoring_season': best_season_text
    }
    
    return render_template('index.html', graphJSON=graphJSON, insights=insights)

@app.route('/teams')
def teams():
    teams_list = data['teams']['NICKNAME'].unique().tolist()
    teams_list.sort()
    return render_template('teams.html', teams=teams_list)

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

@app.route('/api/team/<team_name>')
def get_team_data(team_name):
    try:
        # Find Team ID
        team_info = data['teams'][data['teams']['NICKNAME'] == team_name].iloc[0]
        team_id = team_info['TEAM_ID']
        
        # Filter Games for this team (Home or Away)
        games = data['games']
        team_games = games[(games['HOME_TEAM_ID'] == team_id) | (games['VISITOR_TEAM_ID'] == team_id)].copy()
        
        # Calculate Win/Loss
        team_games['WIN'] = team_games.apply(lambda x: 1 if (x['HOME_TEAM_ID'] == team_id and x['HOME_TEAM_WINS'] == 1) or (x['VISITOR_TEAM_ID'] == team_id and x['HOME_TEAM_WINS'] == 0) else 0, axis=1)
        
        # Win Rate by Season
        season_wins = team_games.groupby('SEASON')['WIN'].mean().reset_index()
        season_wins['WIN_PCT'] = season_wins['WIN'] * 100
        
        # Points Trend
        team_games['PTS'] = team_games.apply(lambda x: x['PTS_home'] if x['HOME_TEAM_ID'] == team_id else x['PTS_away'], axis=1)
        season_points = team_games.groupby('SEASON')['PTS'].mean().reset_index()
        
        # Create Charts
        fig_wins = px.bar(season_wins, x='SEASON', y='WIN_PCT', title=f'{team_name} Win Percentage by Season', color='WIN_PCT', color_continuous_scale='Blues')
        fig_wins.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        fig_pts = px.line(season_points, x='SEASON', y='PTS', title=f'{team_name} Avg Points by Season', markers=True)
        fig_pts.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        # Prepare table data
        # Merge wins and points for the table
        team_season_stats = pd.merge(season_wins, season_points, on='SEASON')
        season_stats_data = team_season_stats.sort_values('SEASON', ascending=False).to_dict('records')
        
        return jsonify({
            'wins_chart': json.loads(json.dumps(fig_wins, cls=plotly.utils.PlotlyJSONEncoder)),
            'pts_chart': json.loads(json.dumps(fig_pts, cls=plotly.utils.PlotlyJSONEncoder)),
            'season_stats': season_stats_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/search')
def search_players():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    players = data['players']
    # Get unique players
    unique_players = players[['PLAYER_NAME', 'PLAYER_ID']].drop_duplicates()
    matches = unique_players[unique_players['PLAYER_NAME'].str.lower().str.contains(query)].head(10)
    
    # Replace NaN with None
    records = matches.to_dict('records')
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
    
    return jsonify(records)

@app.route('/api/player/<int:player_id>')
def get_player_data(player_id):
    try:
        # Get Player Info
        player_info = data['players'][data['players']['PLAYER_ID'] == player_id].iloc[0]
        player_name = player_info['PLAYER_NAME']
        
        # Get Game Details for this player
        details = data['games_details']
        player_games = details[details['PLAYER_ID'] == player_id].copy()
        
        # Merge with Games to get Season
        games = data['games'][['GAME_ID', 'SEASON', 'GAME_DATE_EST']]
        player_stats = pd.merge(player_games, games, on='GAME_ID')
        
        # Aggregate by Season
        season_stats = player_stats.groupby('SEASON')[['PTS', 'AST', 'REB']].mean().reset_index()
        
        # Create Charts
        fig = px.line(season_stats, x='SEASON', y=['PTS', 'AST', 'REB'], title=f'{player_name} Stats by Season', markers=True)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        
        return jsonify({
            'name': player_name,
            'stats_chart': json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)),
            'player_stats': season_stats.sort_values('SEASON', ascending=False).to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rankings/<season_id>')
def get_rankings(season_id):
    try:
        # Filter by Season
        rankings = data['ranking']
        # Season ID in CSV is like 22022 for 2022 season, or 12022?
        # Let's check the data. Assuming standard NBA season IDs.
        # If user passes 2022, we might need to adjust.
        # Let's just filter by string match or loose int match if possible.
        
        # Actually, let's look at unique SEASON_ID in ranking.csv
        # For now, let's assume the user selects from available seasons.
        
        season_rankings = rankings[rankings['SEASON_ID'].astype(str).str.endswith(str(season_id))]
        
        # Get latest date for this season to get final standings
        latest_date = season_rankings['STANDINGSDATE'].max()
        final_standings = season_rankings[season_rankings['STANDINGSDATE'] == latest_date]
        
        # Sort by Conference and Win PCT
        final_standings = final_standings.sort_values(['CONFERENCE', 'W_PCT'], ascending=[True, False])
        
        # Replace NaN with None for valid JSON
        records = final_standings.to_dict('records')
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/seasons')
def get_seasons():
    # Get list of available seasons from ranking
    seasons = data['ranking']['SEASON_ID'].unique()
    # Extract year (last 4 digits usually, or just use as is)
    # Let's just return unique SEASON_IDs sorted
    seasons = sorted([str(s) for s in seasons], reverse=True)
    return jsonify(seasons)

@app.route('/data')
def show_data():
    # Return a snippet of each dataset for debugging
    debug_info = {}
    for key, df in data.items():
        # Replace NaN with None
        records = df.head(5).to_dict('records')
        for record in records:
            for k, v in record.items():
                if pd.isna(v):
                    record[k] = None
        debug_info[key] = records
    return jsonify(debug_info)

if __name__ == '__main__':
    app.run(debug=True)
