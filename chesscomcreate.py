import chess.pgn
import csv
import chess

input_file = 'ChessCom_dhawalplaysd4_202011.pgn'
output_file = 'ChessCom_games.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'Event', 
        'Platform',
        'White', 
        'Black', 
        'Result', 
        'WhiteElo', 
        'BlackElo', 
        'UTCDate', 
        'UTCTime', 
        'ECO', 
        'TimeControl', 
        'Termination', 
        'Link', 
        'Moves'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Open and parse the PGN file
    with open(input_file, 'r', encoding='utf-8') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            # Create a board to generate SAN notation
            board = game.board()
            moves_list = []

            # Iterate through all the moves in the game
            for move in game.mainline_moves():
                moves_list.append(board.san(move))
                board.push(move)

            # Extract game information and map new fields
            game_info = {
                'Event': game.headers.get('Event', ''),
                'Platform': game.headers.get('Site', ''),
                'White': game.headers.get('White', ''),
                'Black': game.headers.get('Black', ''),
                'Result': game.headers.get('Result', ''),
                'WhiteElo': game.headers.get('WhiteElo', ''),
                'BlackElo': game.headers.get('BlackElo', ''),
                'UTCDate': game.headers.get('UTCDate', ''),
                'UTCTime': game.headers.get('UTCTime', ''),
                'ECO': game.headers.get('ECO', ''),
                'TimeControl': game.headers.get('TimeControl', ''),
                'Termination': game.headers.get('Termination', ''),
                'Link': game.headers.get('Link', ''),
                'Moves': ' '.join(moves_list)
            }

            # Write the row to the CSV
            writer.writerow(game_info)

print(f"Data has been written to {output_file}")