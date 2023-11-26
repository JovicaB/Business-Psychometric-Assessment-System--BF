import os
from abc import ABC, abstractmethod
import MySQLdb
import psycopg2


class SingletonDatabase(type):
    """Implementation of a singleton design pattern for database connection"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SingletonDatabase, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(ABC):
    """Abstract method to establish a database connection."""
    
    @abstractmethod
    def connect(self):
        """Establish a database connection."""
        raise ValueError("Should be implemented in a child class")

    @abstractmethod
    def close(self):
        """Close the database connection."""
        raise ValueError("Should be implemented in a child class")


class MySQLConnection(DatabaseConnection):
    """
    Establish a MySQL database connection.

    Returns:
    The MySQL database connection.
    """
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        """Establish a MySQL database connection."""
        connection = MySQLdb.connect(
            host = os.environ.get('MYSQL_DB_HOST'),
            user = os.environ.get('MYSQL_DB_USER'),
            password = os.environ.get('MYSQL_DB_PASS'),
            database = os.environ.get('MYSQL_DB_NAME'),
            port = os.environ.get('MYSQL_DB_PORT'),
            charset='utf8mb4'
        )
        return connection

    def close(self):
        """Close MySQL database connection."""
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            return f"Error closing MySQL connection: {e}"


class PostgreSQLConnection(DatabaseConnection):
    """
    Establish a PostgreSQL database connection.

    Returns:
    The PostgreSQL database connection.
    """
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        """Establish a PostgreSQL database connection."""
        connection = psycopg2.connect(
            host = os.environ.get('PSQL_DB_HOST'),
            user = os.environ.get('PSQL_DB_USER'),
            password = os.environ.get('PSQL_DB_PASS'),
            database = os.environ.get('PSQL_DB_NAME'),
            port = os.environ.get('PSQL_DB_PORT'),
            charset='utf8mb4'
        )
        return connection

    def close(self):
        """Close PostgreSQL database connection."""
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            return f"Error closing PostgreSQL connection: {e}"


class DataManager(metaclass=SingletonDatabase):
    
    def __init__(self, connection_type):
        self.connection = self.create_connection(connection_type)

    def create_connection(self, connection_type):
        """
        Create a database connection based on the specified connection type.

        Parameters:
        - connection_type (str): The type of database connection ('mysql' or 'postgresql').

        Returns:
        An instance of the appropriate DatabaseConnection subclass based on the connection type.

        Raises:
        ValueError: If an unsupported database connection type is provided.
        """

        if connection_type == 'mysql':
            return MySQLConnection()
        elif connection_type == 'postgresql':
            return PostgreSQLConnection()
        else:
            raise ValueError("Unsupported database connection type")

    def read_data(self, sql_query, params=None):
        """
        Read data from the database using a custom SQL query with added parameters.

        This method establishes a database connection, executes the provided SQL query with optional parameters,
        and retrieves the data from the database.

        Parameters:
        - sql_query (str): The SQL query to retrieve data from the database.
        - params (tuple): Optional parameters for the SQL query.

        Example:
        >>> print(DataManager('mysql').read_data("SELECT * from login WHERE user_name = %s", ("Jovica B", ))))

        Returns:
        A list of tuples containing the retrieved data from the database.
        """
        try:
            connection = self.connection.connect()
            cursor = connection.cursor()
            cursor.execute(sql_query, params)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None
        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")

    def save_data(self, sql_query, data):
        """
        Saves data to the database using a provided SQL query and data.

        Parameters:
        - sql_query (str): The SQL query for saving data.
        - data (tuple): The data to be saved.

        Example:
        >>> data_manager = DataManager('mysql')
        >>> data = tuple(input_data,)
        >>> sql_query = "INSERT INTO p1_clients (client_id, company, city, industry, note, ci_name, ci_phone, ci_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        >>> data_manager.save_data(sql_query, data)

        Returns:
        None if successful, or an error message if an exception occurs.
        """

        try:
            connection = self.connection.connect()
            cursor = connection.cursor()
            cursor.execute(sql_query, data)
            connection.commit()
            connection.close()
        except Exception as e:
            print(
                f"An error occurred while saving the data to the database: {e}")
            return None

        return "Data successfully stored in the database "
    
print(DataManager('mysql').read_data("SELECT * from login WHERE user_name = %s", ("Jovica B", )))
