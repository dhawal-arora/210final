import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xyz',
    'database': 'chess_ratings'
}

try:
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    #print("Database connection established successfully.")

    query = """
        SELECT event, platform, white, black, result, white_elo, black_elo, 
               match_date, match_time, eco, time_control, termination, link, moves, won
        FROM chess_games
    """
    data = pd.read_sql(query, engine)

    engine.dispose()
    #print("Database connection closed.")

    data['won'] = pd.to_numeric(data['won'], errors='coerce')
    data['white_elo'] = pd.to_numeric(data['white_elo'], errors='coerce')
    data['black_elo'] = pd.to_numeric(data['black_elo'], errors='coerce')
    data['platform'] = data['platform'].astype(str)

    user_usernames = ['dhawalplaysd4', 'dhawalplayse4']
    data = data[(data['white'].isin(user_usernames)) | (data['black'].isin(user_usernames))]

    data['won'] = data['won'].apply(lambda x: 1 if x == 1 else 0)

    data = data[['platform', 'eco', 'match_time', 'won', 'match_date']]

    data = data.dropna()

    data['match_date'] = pd.to_datetime(data['match_date'], errors='coerce')

    data['match_time'] = pd.to_timedelta(data['match_time'], errors='coerce')
    data['match_time'] = data['match_date'] + data['match_time']

    if data['match_time'].isna().any():
        print("\nThere are NaT values in the `match_time` column. Consider investigating the source data.")

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

    label_encoders = {}
    for col in ['platform', 'eco', 'time_of_day']:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    X = data[['platform', 'eco', 'time_of_day']]
    y = data['won']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nEnter details for the next game:")
    platform = input("Platform (Lichess.org/Chess.com): ").strip()
    eco = input("Your Valid Opening ECO code ('C00'/B01 etc): ").strip()
    time_of_day = input("Time of day (Morning'/'Evening'/'Night'): ").strip()

    next_game = pd.DataFrame({
        'platform': [platform],
        'eco': [eco],
        'time_of_day': [time_of_day]
    })

    for col in ['platform', 'eco', 'time_of_day']:
        if next_game[col].iloc[0] not in label_encoders[col].classes_:
            raise ValueError(f"Unseen label '{next_game[col].iloc[0]}' for column '{col}'")

        next_game[col] = label_encoders[col].transform(next_game[col])

    prediction = model.predict(next_game)
    win_probability = model.predict_proba(next_game)[0][1]

    print("\nPrediction for the Next Game:")
    if prediction[0] == 1:
        print(f"You are likely to WIN the next game with a probability of {win_probability:.2f}.")
    else:
        print(f"You are likely to LOSE the next game.")

except Exception as e:
    print(f"An error occurred: {e}")
