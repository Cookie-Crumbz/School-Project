import mysql.connector
from mysql.connector import Error
from typing import Any, Dict, List, Optional, Tuple, Union

class SQLHelper:
    def __init__(self, host: str, database: str, user: str, password: str, debug: bool = False) -> None:
        """
        Initialize the SQLHelper class with database connection parameters and debug mode.

        Parameters:
        - host (str): The host of the MySQL database.
        - database (str): The name of the database to connect to.
        - user (str): The username to authenticate with.
        - password (str): The password to authenticate with.
        - debug (bool): If True, print debug information. Default is False.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.debug = debug
        self.connection = None
        self.connect()

    def connect(self) -> int:
        """
        Establish a connection to the MySQL database.

        Returns:
        - int: 0 on success, error code on failure.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                collation="utf8mb4_unicode_ci",
                charset="utf8mb4"
            )
            if self.connection.is_connected():
                if self.debug:
                    print("Connected to the database")
            return 0
        except Error as e:
            if self.debug:
                print(f"Error connecting to the database: {e}")
            return e.errno

    def disconnect(self) -> int:
        """
        Close the database connection.

        Returns:
        - int: 0 on success.
        """
        if self.connection.is_connected():
            self.connection.close()
            if self.debug:
                print("Disconnected from the database")
        return 0

    def execute_query(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> int:
        """
        Execute a given SQL query with optional parameters.

        Parameters:
        - query (str): The SQL query to execute.
        - params (Optional[Union[Tuple, Dict[str, Any]]]): Optional parameters for the query.

        Returns:
        - int: 0 on success, error code on failure.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            if self.debug:
                print("Query executed successfully")
            return 0
        except Error as e:
            if self.debug:
                print(f"Error executing query: {e}")
            self.connection.rollback()
            return e.errno
        finally:
            cursor.close()

    def fetch_all(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> Tuple[Optional[List[Dict[str, Any]]], int]:
        """
        Fetch all results for a given SQL query with optional parameters.

        Parameters:
        - query (str): The SQL query to execute.
        - params (Optional[Union[Tuple, Dict[str, Any]]]): Optional parameters for the query.

        Returns:
        - Tuple[Optional[List[Dict[str, Any]]], int]: A tuple containing the results and an error code (0 on success, error code on failure).
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results, 0
        except Error as e:
            if self.debug:
                print(f"Error fetching data: {e}")
            return None, e.errno
        finally:
            cursor.close()

    def fetch_one(self, query: str, params: Optional[Union[Tuple, Dict[str, Any]]] = None) -> Tuple[Optional[Dict[str, Any]], int]:
        """
        Fetch a single result for a given SQL query with optional parameters.

        Parameters:
        - query (str): The SQL query to execute.
        - params (Optional[Union[Tuple, Dict[str, Any]]]): Optional parameters for the query.

        Returns:
        - Tuple[Optional[Dict[str, Any]], int]: A tuple containing the result and an error code (0 on success, error code on failure).
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result, 0
        except Error as e:
            if self.debug:
                print(f"Error fetching data: {e}")
            return None, e.errno
        finally:
            cursor.close()

    def update_data(self, table: str, data: Dict[str, Any], condition: str) -> int:
        """
        Update data in a table.

        Parameters:
        - table (str): The name of the table.
        - data (Dict[str, Any]): A dictionary of column-value pairs to update.
        - condition (str): A string representing the condition for the update.

        Returns:
        - int: 0 on success, error code on failure.
        """
        set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
        values = list(data.values())
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        return self.execute_query(query, values)

    def insert_data(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert data into a table.

        Parameters:
        - table (str): The name of the table.
        - data (Dict[str, Any]): A dictionary of column-value pairs to insert.

        Returns:
        - int: 0 on success, error code on failure.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        return self.execute_query(query, values)

    def delete_data(self, table: str, condition: str) -> int:
        """
        Delete data from a table.

        Parameters:
        - table (str): The name of the table.
        - condition (str): A string representing the condition for the deletion.

        Returns:
        - int: 0 on success, error code on failure.
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        
        return self.execute_query(query)
