import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '210final',
    'database': 'chess_ratings'
}

try:
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    print("Database connection established successfully.")
    
    query = """
        SELECT event, platform, white, black, result, white_elo, black_elo, 
               match_date, match_time, eco, time_control, termination, link, moves, won
        FROM chess_games
    """
    data = pd.read_sql(query, engine)

    data['won'] = pd.to_numeric(data['won'], errors='coerce')
    data['white_elo'] = pd.to_numeric(data['white_elo'], errors='coerce')
    data['black_elo'] = pd.to_numeric(data['black_elo'], errors='coerce')
    data['platform'] = data['platform'].astype(str)

    # 1. Overall Win/Loss/Draw Ratio
    win_count = data[data['won'] == 1].shape[0]
    loss_count = data[data['won'] == 0].shape[0]
    draw_count = data[data['won'] == 0.5].shape[0]
    print(f"Overall Win/Loss/Draw:\nWins: {win_count}, Losses: {loss_count}, Draws: {draw_count}")

    # 2. Win Percentage by Platform
    platform_win_percentage = data.groupby('platform')['won'].mean() * 100
    print("\nWin Percentage by Platform:")
    print(platform_win_percentage)

    # 3. Win Percentage by Time Control
    time_control_win_percentage = data.groupby('time_control')['won'].mean() * 100
    print("\nWin Percentage by Time Control:")
    print(time_control_win_percentage)

    # 4. Most Common Openings and Win Ratio by ECO
    eco_stats = data.groupby('eco')['won'].agg(['count', 'mean']).sort_values(by='count', ascending=False)
    eco_stats.columns = ['Game Count', 'Win Ratio']
    print("\nMost Common Openings (ECO) and Win Ratio:")
    print(eco_stats.head(10))  # Display top 10 most common openings

    # Query to calculate the average opponent rating
    avg_opponent_rating_query = text("""
        SELECT AVG(
            CASE 
                WHEN white = 'dhawalplaysd4' OR white = 'dhawalplayse4' THEN black_elo
                WHEN black = 'dhawalplaysd4' OR black = 'dhawalplayse4' THEN white_elo
            END
        ) AS average_opponent_rating
        FROM chess_games
        WHERE (white = 'dhawalplaysd4' OR black = 'dhawalplaysd4' OR 
               white = 'dhawalplayse4' OR black = 'dhawalplayse4');
    """)
    
    with engine.connect() as connection:
        result = connection.execute(avg_opponent_rating_query).fetchone()
        average_rating = result[0] if result else None

    if average_rating is not None:
        print(f"Average Opponent Rating: {average_rating:.2f}")
    else:
        print("No games found for the specified usernames.")


    data['match_date'] = pd.to_datetime(data['match_date'], errors='coerce')

    # Combine `match_date` and `match_time` to form a proper datetime
    data['match_time'] = pd.to_timedelta(data['match_time'], errors='coerce')
    data['match_time'] = data['match_date'] + data['match_time']

    # Handle NaT values
    if data['match_time'].isna().any():
        print("\nThere are NaT values in the `match_time` column. Consider investigating the source data.")

    # Categorize time of day
    def categorize_time_of_day(time):
        if pd.isnull(time):
            return 'Unknown'
        hour = time.hour
        if 0 <= hour < 8:
            return 'Night'
        elif 8 <= hour < 16:
            return 'Morning'
        elif 16 <= hour < 24:
            return 'Evening'

    data['time_of_day'] = data['match_time'].apply(categorize_time_of_day)

    # Filter wins and analyze by time of day
    win_data = data[data['won'] == 1]
    time_of_day_win_counts = win_data.groupby(['time_of_day', 'platform'])['won'].count().unstack(fill_value=0)
    print(time_of_day_win_counts)

    max_wins = time_of_day_win_counts.max().max()
    best_time_of_day = time_of_day_win_counts.stack().idxmax()

    print("\nTime of Day Analysis for Wins:")
    print(f"{best_time_of_day[1]} platform during {best_time_of_day[0]} with {max_wins} wins")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'engine' in locals():
        engine.dispose()
        #print("Database connection closed.")
