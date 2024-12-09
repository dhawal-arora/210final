import mysql.connector

db_config = {
    'host': 'localhost', 
    'user': 'root', 
    'password': '210final',
    'database': 'chess_ratings'
}

def create_table(db_config):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS chess_games (
            id INT AUTO_INCREMENT PRIMARY KEY,
            `event` VARCHAR(255),
            `platform` VARCHAR(255),
            `white` VARCHAR(255),
            `black` VARCHAR(255),
            `result` VARCHAR(10),
            `white_elo` VARCHAR(10),
            `black_elo` VARCHAR(10),
            `match_date` DATE,
            `match_time` TIME,
            `eco` VARCHAR(10),
            `time_control` VARCHAR(50),
            `termination` TEXT,
            `link` VARCHAR(255),
            `moves` TEXT
        );
        """

        cursor.execute(create_table_query)
        print("Table `chess_games` has been created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

create_table(db_config)


# import mysql.connector

# # Database connection details
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '210final',
#     'database': 'chess_ratings'
# }

# def delete_table(db_config, table_name):
#     """Delete the specified table from the database."""
#     try:
#         # Connect to the database
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor()
        
#         # SQL query to drop the table
#         drop_query = f"DROP TABLE IF EXISTS {table_name};"
#         cursor.execute(drop_query)
#         connection.commit()

#         print(f"Table '{table_name}' has been deleted successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# # Call the function to delete the table
# delete_table(db_config, 'chess_games')
