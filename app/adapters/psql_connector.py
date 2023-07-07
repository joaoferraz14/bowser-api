import psycopg2


class DatabaseConnection:
    def __init__(self, host, username, password, database) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect_to_db(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            dbname=self.database,
        )
        self.cursor = self.connection.cursor()

    def disconnect_from_db(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


class QueryDatabase(DatabaseConnection):
    def __init__(self, host, username, password, database, query):
        super().__init__(host, username, password, database)
        self.query = query

    def execute_query(self):
        try:
            if not self.connection:
                self.connect_to_db()
            self.cursor.execute(self.query)
            return "Query ran successfully"
        except Exception as e:
            return e
