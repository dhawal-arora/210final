import chess.pgn
import csv
from collections import Counter

# File names
input_pgn_file = "lichess_dhawalplayse4_2024-12-04.pgn"
output_csv_file = "Lichessorg_games.csv"

# Step 1: Parse PGN and write to CSV
with open(input_pgn_file, "r", encoding="utf-8") as pgn, open(output_csv_file, mode="w", newline='', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Write the header row (same as the Chess.com format)
    writer.writerow([
        "Event", "Platform", "White", "Black", "Result", 
        "WhiteElo", "BlackElo", "UTCDate", "UTCTime", 
        "ECO", "TimeControl", "Termination", "Link", "Moves"
    ])
    
    # List to track months for analysis
    months = []
    
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        
        # Extract game data
        event = game.headers.get("Event", "")
        platform = "Lichess.org" 
        white = game.headers.get("White", "")
        black = game.headers.get("Black", "")
        result = game.headers.get("Result", "")
        white_elo = game.headers.get("WhiteElo", "")
        black_elo = game.headers.get("BlackElo", "")
        utc_date = game.headers.get("UTCDate", "")
        utc_time = game.headers.get("UTCTime", "")
        eco = game.headers.get("ECO", "")
        time_control = game.headers.get("TimeControl", "")
        termination = game.headers.get("Termination", "")
        link = game.headers.get("Site", "")

        # Record the month for analysis and check if it's November 2020
        if utc_date:
            year, month, _ = utc_date.split('.')
            if year == '2020' and month == '11':
                # Generate SAN notation for the moves
                board = game.board()
                moves_list = []
                for move in game.mainline_moves():
                    moves_list.append(board.san(move))
                    board.push(move)

                # Write data to CSV
                writer.writerow([
                    event, platform, white, black, result, 
                    white_elo, black_elo, utc_date, utc_time, 
                    eco, time_control, termination, link, 
                    ' '.join(moves_list)
                ])
        
        if utc_date:
            month = '-'.join(utc_date.split('.')[:2]) 
            months.append(month)

