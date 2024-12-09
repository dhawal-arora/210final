import pandas as pd
from sqlalchemy import create_engine

# Connect to your MySQL database using SQLAlchemy
db_engine = create_engine("mysql+pymysql://root:xyz@localhost/chess_ratings")

# Load the chess_games table into a pandas DataFrame
query = "SELECT * FROM chess_games"
df = pd.read_sql(query, con=db_engine)

chesscom_username = "dhawalplaysd4"
lichess_username = "dhawalplayse4"

def calculate_result(row):
    if row['white'] in [chesscom_username, lichess_username]:
        if row['result'] == "1-0":
            return 1 
        elif row['result'] == "0-1":
            return 0
        elif row['result'] == "1/2-1/2":
            return 0.5
    elif row['black'] in [chesscom_username, lichess_username]:
        if row['result'] == "1-0":
            return 0
        elif row['result'] == "0-1":
            return 1
        elif row['result'] == "1/2-1/2":
            return 0.5
    return None

df['won'] = df.apply(calculate_result, axis=1)

df.to_sql('chess_games', con=db_engine, if_exists='replace', index=False)

# Close the database connection
db_engine.dispose()
