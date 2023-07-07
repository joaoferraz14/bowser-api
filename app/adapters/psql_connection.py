import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, host: str, username: str, password: str, database: str) -> None:
        """
        This class handles the database connection and operations related to it.

        Args:
        host (str): The hostname of the database.
        username (str): The username to access the database.
        password (str): The password to access the database.
        database (str): The database name.
        """
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect_to_db(self) -> None:
        """
        This method connects to the database using the credentials provided in the constructor.
        """
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            dbname=self.database,
            cursor_factory=RealDictCursor,
        )
        self.cursor = self.connection.cursor()

    def disconnect_from_db(self) -> None:
        """
        This method disconnects from the database.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
