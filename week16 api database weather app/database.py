from typing import List, Tuple
import sqlite3
from datetime import datetime, timedelta


class WeatherDatabase:
    def __init__(self):
        """
Initialize a new WeatherDatabase instance.
"""
        self.db_path = "weather.db"
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS request")
        cursor.execute("DROP TABLE IF EXISTS response")
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS request (
    id INTEGER NOT NULL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    time DATETIME NOT NULL
);""")
        cursor.execute('''
    CREATE TABLE response (
    request_id INTEGER UNIQUE NOT NULL,
    city VARCHAR(50) NOT NULL,
    temperature NUMERIC NOT NULL,
    feels_like NUMERIC NOT NULL,
    last_update DATETIME NOT NULL,
    FOREIGN KEY (request_id) REFERENCES request("id")
);''')
        cursor.close()
        connection.close()

    def save_request_data(self, city_name: str, request_time: str) -> None:
        """
        Save request data for a city to the database.

        Args:
        - city_name (str): The name of the city to save request data for.
        - request_time (str): The time the request was made, in ISO format.

        Returns:
        - None
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO request (city, time)
        VALUES (?, ?);
        ''', (city_name, request_time))
        connection.commit()
        cursor.close()
        connection.close()

    def save_response_data(self, response_data: dict) -> None:
        """
        Save response data for a city to the database.
        Args:
        - response_data (dict): A dictionary containing weather information for the city, incl
        uding temperature, feels like temperature, city_name, and last updated time.
        Returns:
        - None
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT id FROM request ORDER BY time DESC LIMIT 1;')
        request_id = cursor.fetchone()

        if request_id is not None:
            cursor.execute('''
            INSERT INTO response (request_id, city, temperature, feels_like, last_update)
            VALUES (?, ?, ?, ?, ?);
            ''', (request_id[0], response_data["name"], response_data['temp'], response_data['feels_like'], response_data['last_updated_time']))
            connection.commit()

        cursor.close()
        connection.close()

    def get_request_count(self) -> int:
        """
        Get the total number of requests made to the server.
        Returns:
        - int: The total number of requests made to the server.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM request;')
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count

    def get_successful_request_count(self) -> int:
        """
        Get the total number of successful requests made to the server.
        Returns:
        - int: The total number of successful requests made to the server.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM response;')
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count

    def get_last_hour_requests(self) -> List[Tuple[str, str]]:
        """
        Get a list of requests made in the last hour.
        Returns:
        - List[Tuple[str, str]]: A list of tuples containing the name of the city and the time
        the request was made, in ISO format.
        """
        one_hour_ago = datetime.now() - timedelta(hours=1)
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COALESCE(res.city , req.city), req.time FROM request req
        LEFT JOIN response res on res.request_id = req.id
        WHERE time >= ?;
        ''', (one_hour_ago,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_city_request_count(self) -> List[Tuple[str, int]]:
        """
        Get a count of requests made for each city.
        Returns:
        - List[Tuple[str, int]]: A list of tuples containing the name of the city and the numb
        er of requests made for that city.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''
        SELECT COALESCE(res.city , req.city) AS city_name, COUNT(*) FROM request req
        LEFT JOIN response res on res.request_id = req.id
        GROUP BY city_name;
        ''')
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
