import pyodbc
import os
from dotenv import load_dotenv

class MSSql:
    def __init__(self, connection_string):
        """
        Initializes the MSSQLConnection object with the connection string.
        
        :param connection_string: The connection string for the MSSQL database.
        """
        load_dotenv()
        self.connection_string = connection_string
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the MSSQL database.

        :return: A pyodbc connection object if successful, None otherwise.
        """
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("Successfully connected to the database.")
            return self.connection
        except pyodbc.Error as e:
            print(f"Error while connecting to MSSQL: {e}")
            return None

    def close(self):
        """
        Closes the database connection if it is open.
        """
        if self.connection:
            try:
                self.connection.close()
                print("Database connection closed.")
            except pyodbc.Error as e:
                print(f"Error while closing the connection: {e}")
            finally:
                self.connection = None
        else:
            print("No active connection to close.")

    # Context manager methods
    def __enter__(self):
        """
        Called at the start of the with block, opens the connection.
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """S
        Called at the end of the with block, closes the connection.
        Handles exceptions if they occur.
        """
        self.close()
        # Return False to propagate the exception if there is one
        return False
