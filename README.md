# 210final

# Chess Match Winning Chances Predictor and Skill Assessment

This project processes and analyzes your chess game data from Chess.com and Lichess.org using Python.

## Files Overview & Execution Order

1. **`chesscomcreate.py`**: Fetches and cleans data from Chess.com.
2. **`lichessorgcreate.py`**: Fetches and cleans data from Lichess.org.
3. **`create_table.py`**: Creates a SQL database table for storing data.
4. **`datastore.py`**: Inserts cleaned data into the database.
5. **`won.py`**: Adds a "won" column to the database table.
6. **`ds.py`**: Runs data science analysis on the data.
7. **`ml.py`**: Builds and evaluates predictive models.

## Notes

- Replace SQL credentials in the scripts as needed.
- Ensure all scripts are in the same folder before running.
- Execute requirements.txt with pip install -r requirements.txt
