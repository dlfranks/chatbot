from models.user import User
from repository.baseRepository import BaseRepository


class UserRepository:
    def __init__(self):
        """
        Initializes the UserService with a database connection.

        :param connection: An instance of MSSQLConnection.
        """
        self.table_name = "Users"
        self.repository = BaseRepository(self.table_name)
        

    def create_user(self, user: User):
        """
        Inserts a new user into the database.

        :param user: An instance of the User class.
        """
        query = f"""
        INSERT INTO {self.table_name} 
        (username, firstName, lastName, email, password, DOB, sex, nativeLang, secondLang, occupation, createDate, updateDate, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.repository as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                user.username, user.first_name, user.last_name, user.email, user.password,
                user.dob, user.sex, user.native_lang, user.second_lang, user.occupation, user.createDate, user.updateDate, user.active
            ))
            conn.commit()

    def get_user_by_id(self, user_id: int) -> User:
        """
        Fetches a user by their ID.

        :param user_id: The ID of the user to fetch.
        :return: An instance of the User class or None if not found.
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return self._map_to_user(row) if row else None

    def get_all_users(self):
        """
        Fetches all users from the database.

        :return: A list of User instances.
        """
        query = f"SELECT * FROM {self.table_name}"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [self._map_to_user(row) for row in rows]

    def update_user(self, user: User):
        """
        Updates an existing user in the database.

        :param user: An instance of the User class with updated data.
        """
        query = f"""
        UPDATE {self.table_name}
        SET username = ?, firstName = ?, lastName = ?, email = ?, password = ?, DOB = ?, 
            sex = ?, nativeLang = ?, secondLang = ?, occupation = ?, createDate = ?, updateDate = ?, active = ?
        WHERE id = ?
        """
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                user.username, user.first_name, user.last_name, user.email, user.password,
                user.dob, user.sex, user.native_lang, user.second_lang, user.occupation, user.createDate, user.updateDate,
                user.active, user.id
            ))
            conn.commit()

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database by their ID.

        :param user_id: The ID of the user to delete.
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()

    def _map_to_user(self, row):
        """
        Maps a database row to a User instance.

        :param row: A row from the database.
        :return: An instance of the User class.
        """
        return User(
            id=row[0], username=row[1], first_name=row[2], last_name=row[3],
            email=row[4], password=row[5], dob=row[6], sex=row[7],
            native_lang=row[8], second_lang=row[9], occupation=row[10], createDate = row[11], updateDate = row[12], active=row[13]
        )
