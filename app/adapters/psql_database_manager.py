import os
import time
import logging
from typing import Union, List, Dict, Any
from .psql_connection import DatabaseConnection


class QueryDatabase:
    def __init__(self, db_connection: DatabaseConnection):
        """
        This class handles database queries.

        Args:
        db_connection (DatabaseConnection): An instance of the DatabaseConnection class.
        """
        self.db_connection = db_connection

    def execute_query(self, query: str, *args) -> Union[str, Exception]:
        """
        This method executes the query on the connected database.

        Returns:
        str: Success message if query execution is successful.
        Exception: Exception message if query execution fails.
        """
        try:
            if not self.db_connection.connection:
                self.db_connection.connect_to_db()
            self.db_connection.cursor.execute(query, *args)
            return "Query ran successfully"
        except Exception as e:
            return logging.error(f"Failed to execute query: {e}")

    def commit_changes_to_db(self):
        try:
            self.db_connection.connection.commit()
        except Exception as e:
            return logging.error(f"Failed to commit changes to the database: {e}")

    def fetch_all_rows(self) -> Union[List[Dict[str, Any]], Exception]:
        """
        This method fetches all rows from the last executed query.

        Returns:
        List[Dict[str, Any]]: List of rows as dictionaries if fetch is successful.
        Exception: Exception message if fetch fails.
        """
        try:
            rows = self.db_connection.cursor.fetchall()
            return rows
        except Exception as e:
            return logging.error(f"Failed to fetch the records: {e}")


class DatabaseManager:
    """
    Manages the database connection and operations.
    """

    def __init__(self) -> None:
        self.connection = None

    def connect_to_database(self) -> None:
        """
        Establishes the connection to the database.
        """
        while True:
            try:
                self.connection = DatabaseConnection(
                    os.getenv("HOST"),
                    os.getenv("USERNAME"),
                    os.getenv("PASSWORD"),
                    os.getenv("DATABASE"),
                )
                self.connection.connect_to_db()
                logging.info("Database connection succeeded")
                print("Logged in successfully")
                return QueryDatabase(self.connection)
            except Exception as e:
                logging.error(f"Connection to database failed. Error: {e}")
                print(f"Connection to database failed. Error: {e}")
                time.sleep(2)
