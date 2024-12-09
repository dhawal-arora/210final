import chess.pgn
import csv
import mysql.connector
from collections import Counter

db_config = {
    'host': 'localhost', 
    'user': 'root',  
    'password': 'xyz',
    'database': 'chess_ratings'
}

def insert_data_from_csv(csv_file, db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO chess_games (
                `event`, `platform`, `white`, `black`, `result`, `white_elo`, `black_elo`, 
                `match_date`, `match_time`, `eco`, `time_control`, `termination`, `link`, `moves`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Read data from CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = (
                    row['Event'], row['Platform'], row['White'], row['Black'],
                    row['Result'], row['WhiteElo'], row['BlackElo'],
                    row['UTCDate'], row['UTCTime'], row['ECO'], 
                    row['TimeControl'], row['Termination'], row['Link'], 
                    row['Moves']
                )
                # Execute insert query
                cursor.execute(insert_query, data)

        # Commit the transaction
        connection.commit()
        print(f"Data from {csv_file} has been successfully inserted into the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# File paths and configuration
lichess_pgn_file = "lichess_dhawalplayse4_2024-12-04.pgn"
lichess_csv_file = "Lichessorg_games.csv"

chesscom_pgn_file = "ChessCom_dhawalplaysd4_202011.pgn"
chesscom_csv_file = "Chesscom_games.csv"

# Insert data into MySQL database
insert_data_from_csv(lichess_csv_file, db_config)
insert_data_from_csv(chesscom_csv_file, db_config)
