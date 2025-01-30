from database import MSSql

class BaseRepository:
    def __init__(self, table_name: str):
        """
        Initializes the BaseRepository with a connection and a table name.

        :param connection: An instance of MSSQLConnection.
        :param table_name: The name of the table this repository interacts with.
        """
        self.connection = MSSql().connect()
        self.table_name = table_name

    def read_all(self):
        """
        Fetch all rows from the table.

        :return: List of rows from the table.
        """
        query = f"SELECT * FROM {self.table_name}"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def read_by_id(self, record_id):
        """
        Fetch a single row by ID.

        :param record_id: The ID of the row to fetch.
        :return: A single row if found, None otherwise.
        """
        query = f"SELECT * FROM {self.table_name} WHERE Id = ?"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            return cursor.fetchone()

    def create(self, columns, values):
        """
        Insert a new row into the table.

        :param columns: List of column names.
        :param values: List of values corresponding to the columns.
        """
        placeholders = ", ".join(["?"] * len(values))
        columns_str = ", ".join(columns)
        query = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def update(self, updates, record_id):
        """
        Update an existing row by ID.

        :param updates: A dictionary of columns and their new values.
        :param record_id: The ID of the row to update.
        """
        set_clause = ", ".join([f"{column} = ?" for column in updates.keys()])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE Id = ?"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(updates.values()) + [record_id])
            conn.commit()

    def delete(self, record_id):
        """
        Delete a row by ID.

        :param record_id: The ID of the row to delete.
        """
        query = f"DELETE FROM {self.table_name} WHERE Id = ?"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (record_id,))
            conn.commit()
